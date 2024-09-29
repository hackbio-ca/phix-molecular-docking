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
    # Run propka on both enzyme and substrate
    subprocess.run(['propka3', enzyme_pdb], check=True)
    subprocess.run(['propka3', substrate_pdb], check=True)

    # Use PDB2PQR or another tool to adjust protonation state based on pH
    # Assuming the output goes to OUTPUT_FOLDER
    enzyme_output = os.path.join(OUTPUT_FOLDER, 'adjusted_' + os.path.basename(enzyme_pdb))
    substrate_output = os.path.join(OUTPUT_FOLDER, 'adjusted_' + os.path.basename(substrate_pdb))

    # Adjust protonation using PDB2PQR or another tool
    # Example command (adjust as needed for your setup):
    subprocess.run(['pdb2pqr', '--ph-calc-method=propka', '--with-ph', ph, enzyme_pdb, enzyme_output], check=True)
    subprocess.run(['pdb2pqr', '--ph-calc-method=propka', '--with-ph', ph, substrate_pdb, substrate_output], check=True)

if __name__ == "__main__":
    app.run(debug=True)
