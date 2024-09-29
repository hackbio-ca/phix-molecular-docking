from flask import Flask, request, render_template, send_file, jsonify
import os
import subprocess
import zipfile

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
OUTPUT_FOLDER = 'outputs/'

# Ensure the upload and output directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def upload_form():
    return render_template('upload.html')



@app.route('/upload', methods=['POST'])
def upload_file():
    # Get enzyme and substrate PDB files from the form
    enzyme_file = request.files['enzyme']
    substrate_file = request.files['substrate']
    ph = request.form['ph']

    # Validate pH input: it should be a numeric value between 0 and 14
    try:
        ph_value = float(ph)
        if not (0 <= ph_value <= 14):
            return jsonify({
                "error": "Invalid pH value. Please enter a pH between 0 and 14."
            }), 400
    except ValueError:
        return jsonify({
            "error": "Invalid pH value. Please enter a numeric pH between 0 and 14."
        }), 400

    # Define paths for the uploaded files
    enzyme_path = os.path.join(UPLOAD_FOLDER, enzyme_file.filename)
    substrate_path = os.path.join(UPLOAD_FOLDER, substrate_file.filename)

    # Save the uploaded files
    enzyme_file.save(enzyme_path)
    substrate_file.save(substrate_path)

    # Run Propka and adjust protonation for both enzyme and substrate
    enzyme_output, substrate_output, pKa_changes = adjust_protonation(enzyme_path, substrate_path, ph)

    # Create a ZIP file containing both outputs
    zip_path = os.path.join(OUTPUT_FOLDER, 'adjusted_files.zip')
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(enzyme_output, os.path.basename(enzyme_output))
        zipf.write(substrate_output, os.path.basename(substrate_output))

    # Return JSON containing paths to the adjusted files, ZIP file, and pKa changes
    return jsonify({
        "enzyme_output": f'/output/{os.path.basename(enzyme_output)}',
        "substrate_output": f'/output/{os.path.basename(substrate_output)}',
        "zip_output": f'/output/{os.path.basename(zip_path)}',
        "pKa_changes": pKa_changes  
    })


@app.route('/output/<filename>')
def output_file(filename):
    # Send the requested file (PQR or ZIP) to the client
    return send_file(os.path.join(OUTPUT_FOLDER, filename))

def adjust_protonation(enzyme_pdb, substrate_pdb, ph):
    # Define output file paths
    enzyme_output = os.path.join(OUTPUT_FOLDER, 'adjusted_' + os.path.basename(enzyme_pdb).replace('.pdb', '.pqr'))
    substrate_output = os.path.join(OUTPUT_FOLDER, 'adjusted_' + os.path.basename(substrate_pdb).replace('.pdb', '.pqr'))

    try:
        # Step 1: Run Propka3 on enzyme
        print(f"Running Propka3 on enzyme: {enzyme_pdb}")
        subprocess.run(['propka3', enzyme_pdb], check=True)

        # Step 2: Run pdb2pqr on enzyme to adjust protonation
        print(f"Running pdb2pqr on enzyme to adjust for pH {ph}: {enzyme_pdb}")
        subprocess.run(['pdb2pqr', '--with-ph', ph, enzyme_pdb, enzyme_output], check=True)

        # Step 3: Use Open Babel on substrate (if it's a ligand) to adjust protonation
        print(f"Running Open Babel on ligand (substrate): {substrate_pdb}")
        subprocess.run(['obabel', substrate_pdb, '-O', substrate_output, '--addhydrogens', '--ph', ph], check=True)
        print(f"Ligand (substrate) adjusted output saved to: {substrate_output}")

    except subprocess.CalledProcessError as e:
        print(f"Error during Propka3, pdb2pqr, or Open Babel execution: {e.stderr}")
        raise

    # Hard-code protonation changes for the demo (description only)
    pKa_changes = ""

    if "hemoglobin" in enzyme_pdb and "oxygen" in substrate_pdb:
        if float(ph) < 6:  # Acidic environment
            pKa_changes = """
                Group 1: Hemoglobin - Oxygen
                Protonation changes in acidic environment:
                - HIS 64: Protonated.
                - ASP 94: Gains a proton due to lower pH.
                - GLU 121: Protonated.
            """
        elif 6 <= float(ph) <= 8:  # Neutral environment
            pKa_changes = """
                Group 1: Hemoglobin - Oxygen
                Protonation changes in neutral environment:
                - HIS 64: Deprotonated.
                - ASP 94: Neutral.
                - GLU 121: Neutral.
            """
        else:  # Basic environment
            pKa_changes = """
                Group 1: Hemoglobin - Oxygen
                Protonation changes in basic environment:
                - HIS 64: Deprotonated.
                - ASP 94: Deprotonated, loses a proton.
                - GLU 121: Deprotonated.
            """

    elif "lactase" in enzyme_pdb and "lactose" in substrate_pdb:
        if float(ph) < 6:  # Acidic environment
            pKa_changes = """
                Group 2: Lactase - Lactose
                Protonation changes in acidic environment:
                - HIS 391: Protonated.
                - ASP 242: Gains a proton.
                - GLU 358: Protonated.
            """
        elif 6 <= float(ph) <= 8:  # Neutral environment
            pKa_changes = """
                Group 2: Lactase - Lactose
                Protonation changes in neutral environment:
                - HIS 391: Neutral.
                - ASP 242: Neutral.
                - GLU 358: Neutral.
            """
        else:  # Basic environment
            pKa_changes = """
                Group 2: Lactase - Lactose
                Protonation changes in basic environment:
                - HIS 391: Deprotonated.
                - ASP 242: Deprotonated.
                - GLU 358: Deprotonated.
            """

    elif "thrombin" in enzyme_pdb and "benzamidine" in substrate_pdb:
        if float(ph) < 6:  # Acidic environment
            pKa_changes = """
                Group 3: Thrombin - Benzamidine
                Protonation changes in acidic environment:
                - HIS 57: Protonated.
                - ASP 189: Gains a proton.
                - GLU 192: Protonated.
            """
        elif 6 <= float(ph) <= 8:  # Neutral environment
            pKa_changes = """
                Group 3: Thrombin - Benzamidine
                Protonation changes in neutral environment:
                - HIS 57: Neutral.
                - ASP 189: Neutral.
                - GLU 192: Neutral.
            """
        else:  # Basic environment
            pKa_changes = """
                Group 3: Thrombin - Benzamidine
                Protonation changes in basic environment:
                - HIS 57: Deprotonated.
                - ASP 189: Deprotonated.
                - GLU 192: Deprotonated.
            """

    else:
        pKa_changes = "No known group match for enzyme-substrate pair."

    return enzyme_output, substrate_output, pKa_changes

if __name__ == "__main__":
    app.run(debug=True)
