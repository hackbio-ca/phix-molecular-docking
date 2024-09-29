from flask import Flask, request, render_template, send_file
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
        enzyme_pqr, substrate_pqr = adjust_protonation(enzyme_path, substrate_path, ph)

        # Create a ZIP file with both PQR and PDB outputs
        zip_path = os.path.join(OUTPUT_FOLDER, 'adjusted_files.zip')
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            # Add PQR files to the ZIP
            zipf.write(enzyme_pqr, os.path.basename(enzyme_pqr))
            zipf.write(substrate_pqr, os.path.basename(substrate_pqr))
            # Optionally add original PDB files too
            zipf.write(enzyme_path, os.path.basename(enzyme_path))
            zipf.write(substrate_path, os.path.basename(substrate_path))

        # Send the ZIP file to the user
        if os.path.exists(zip_path):
            return send_file(zip_path, as_attachment=True)
        else:
            return f"File {zip_path} not found", 404

def adjust_protonation(enzyme_pdb, substrate_pdb, ph):
    enzyme_output = os.path.join(OUTPUT_FOLDER, 'adjusted_' + os.path.basename(enzyme_pdb).replace('.pdb', '.pqr'))
    substrate_output = os.path.join(OUTPUT_FOLDER, 'adjusted_' + os.path.basename(substrate_pdb).replace('.pdb', '.pqr'))

    try:
        # Step 1: Run Propka3 on enzyme
        print(f"Running Propka3 on enzyme: {enzyme_pdb}")
        subprocess.run(['propka3', enzyme_pdb], check=True)

        # Step 2: Run pdb2pqr on enzyme
        print(f"Running pdb2pqr on enzyme to adjust for pH {ph}: {enzyme_pdb}")
        subprocess.run(['pdb2pqr', '--with-ph', ph, enzyme_pdb, enzyme_output], check=True)

        # Step 3: Preprocess the substrate using Open Babel (if it's a small molecule/ligand)
        print(f"Running Open Babel on ligand (substrate): {substrate_pdb}")
        subprocess.run(['obabel', substrate_pdb, '-O', substrate_output, '--addhydrogens', '--ph', ph], check=True)
        print(f"Ligand (substrate) adjusted output saved to: {substrate_output}")

    except subprocess.CalledProcessError as e:
        print(f"Error during Propka3, pdb2pqr, or Open Babel execution: {e.stderr}")
        raise

    return enzyme_output, substrate_output  # Return the paths to the adjusted PQR files

if __name__ == "__main__":
    app.run(debug=True)
