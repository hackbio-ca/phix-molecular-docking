from flask import Flask, request, render_template, send_file
import os
import subprocess

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
    if request.method == 'POST':
        # Get enzyme and substrate PDB files
        enzyme_file = request.files['enzyme']
        substrate_file = request.files['substrate']
        ph = request.form['ph']

        enzyme_path = os.path.join(UPLOAD_FOLDER, enzyme_file.filename)
        substrate_path = os.path.join(UPLOAD_FOLDER, substrate_file.filename)

        # Save the uploaded files
        enzyme_file.save(enzyme_path)
        substrate_file.save(substrate_path)

        # Run Propka and adjust protonation
        adjust_protonation(enzyme_path, substrate_path, ph)

        # Return modified PDB files to the user
        enzyme_output = os.path.join(OUTPUT_FOLDER, 'adjusted_' + enzyme_file.filename)
        return send_file(enzyme_output, as_attachment=True)




def adjust_protonation(enzyme_pdb, substrate_pdb, ph):
    # Define output file paths for enzyme and substrate (as .pqr files)
    enzyme_output = os.path.join(OUTPUT_FOLDER, 'adjusted_' + os.path.basename(enzyme_pdb).replace('.pdb', '.pqr'))
    substrate_output = os.path.join(OUTPUT_FOLDER, 'adjusted_' + os.path.basename(substrate_pdb).replace('.pdb', '.pqr'))

    try:
        # Step 1: Run Propka3 on the enzyme PDB file to generate the .pka file
        print(f"Running Propka3 on enzyme: {enzyme_pdb}")
        subprocess.run(['propka3', enzyme_pdb], check=True)

        # Step 2: Run pdb2pqr on the enzyme PDB file to adjust protonation based on pH
        print(f"Running pdb2pqr on enzyme to adjust for pH {ph}: {enzyme_pdb}")
        subprocess.run(['pdb2pqr', '--with-ph', ph, enzyme_pdb, enzyme_output], check=True)
        print(f"Enzyme adjusted output saved to: {enzyme_output}")

        # Step 3: Run Propka3 on the substrate PDB file to generate the .pka file
        print(f"Running Propka3 on substrate: {substrate_pdb}")
        subprocess.run(['propka3', substrate_pdb], check=True)

        # Step 4: Run pdb2pqr on the substrate PDB file to adjust protonation based on pH
        print(f"Running pdb2pqr on substrate to adjust for pH {ph}: {substrate_pdb}")
        subprocess.run(['pdb2pqr', '--with-ph', ph, substrate_pdb, substrate_output], check=True)
        print(f"Substrate adjusted output saved to: {substrate_output}")

    except subprocess.CalledProcessError as e:
        print(f"Error during Propka3 or pdb2pqr execution: {e.stderr}")
        raise

    return enzyme_output, substrate_output  # Return the paths to the adjusted PQR files






if __name__ == "__main__":
    app.run(debug=True)
