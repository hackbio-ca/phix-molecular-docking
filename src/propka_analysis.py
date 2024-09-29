import os
import subprocess

# Get the absolute path to the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the path to the output directory
output_dir = os.path.join(current_dir, 'output')

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Define the paths to your PDB files
enzyme_pdb = os.path.join(current_dir, 'data', 'EGFR_TK.pdb')
substrate_pdb = os.path.join(current_dir, 'data', 'Erlotinib.pdb')

# Function to run Propka via the command line and capture the results
def run_propka(pdb_file, output_dir):
    try:
        # Run Propka on the PDB file using propka3
        result = subprocess.run(['propka3', pdb_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode == 0:
            print(f"pKa calculation completed for {pdb_file}")
            pdb_filename = os.path.basename(pdb_file)
            generated_pka_file = os.path.join(current_dir, pdb_filename.replace('.pdb', '.pka'))
            
            # Move the .pka file to the output directory
            if os.path.exists(generated_pka_file):
                output_file = os.path.join(output_dir, pdb_filename.replace('.pdb', '.pka'))
                os.rename(generated_pka_file, output_file)
                print(f"Moved {generated_pka_file} to {output_file}")
            else:
                print(f"Error: {generated_pka_file} not found in {current_dir}.")
        else:
            print(f"Error running Propka for {pdb_file}: {result.stderr}")
    except FileNotFoundError:
        print(f"Propka not found. Ensure Propka is installed and available in your PATH or the file {pdb_file} exists.")

# Run Propka for both enzyme and substrate PDB files
print("Running Propka for enzyme (EGFR_TK):")
run_propka(enzyme_pdb, output_dir)

print("\nRunning Propka for substrate (Erlotinib):")
run_propka(substrate_pdb, output_dir)
