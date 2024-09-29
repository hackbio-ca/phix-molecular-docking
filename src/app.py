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

    # Define paths for the uploaded files
    enzyme_path = os.path.join(UPLOAD_FOLDER, enzyme_file.filename)
    substrate_path = os.path.join(UPLOAD_FOLDER, substrate_file.filename)

    # Save the uploaded files
    enzyme_file.save(enzyme_path)
    substrate_file.save(substrate_path)

    # Run Propka and adjust protonation for both enzyme and substrate
    enzyme_output, substrate_output = adjust_protonation(enzyme_path, substrate_path, ph)

    # Create a ZIP file containing both outputs
    zip_path = os.path.join(OUTPUT_FOLDER, 'adjusted_files.zip')
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(enzyme_output, os.path.basename(enzyme_output))
        zipf.write(substrate_output, os.path.basename(substrate_output))

    # Return JSON containing paths to the adjusted files and the ZIP file
    return jsonify({
        "enzyme_output": f'/output/{os.path.basename(enzyme_output)}',
        "substrate_output": f'/output/{os.path.basename(substrate_output)}',
        "zip_output": f'/output/{os.path.basename(zip_path)}'
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

    return enzyme_output, substrate_output

if __name__ == "__main__":
    app.run(debug=True)
