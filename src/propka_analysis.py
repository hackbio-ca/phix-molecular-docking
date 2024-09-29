import subprocess
import os

# Get the absolute path to the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the absolute paths to your PDB files
enzyme_pdb = os.path.join(current_dir, 'data', 'EGFR_TK.pdb')
substrate_pdb = os.path.join(current_dir, 'data', 'Erlotinib.pdb')

# Function to run Propka via the command line and capture the results
def run_propka(pdb_file):
    try:
        # Run Propka on the PDB file using propka3
        result = subprocess.run(['propka3', pdb_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode == 0:
            print(f"pKa calculation completed for {pdb_file}")
            output_file = pdb_file.replace('.pdb', '.pka')
            
            # Check if the .pka output file exists
            if os.path.exists(output_file):
                with open(output_file, 'r') as f:
                    print(f"\n{output_file} contents:")
                    for line in f:
                        print(line.strip())
            else:
                print(f"Error: {output_file} not found.")
        else:
            print(f"Error running Propka for {pdb_file}: {result.stderr}")
    except FileNotFoundError:
        print("Propka not found. Ensure Propka is installed and available in your PATH.")

# Run Propka for both enzyme and substrate PDB files
print("Running Propka for enzyme (EGFR_TK):")
run_propka(enzyme_pdb)

print("\nRunning Propka for substrate (Erlotinib):")
run_propka(substrate_pdb)
