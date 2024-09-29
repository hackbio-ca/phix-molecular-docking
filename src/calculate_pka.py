import propka
import propka.lib

# Path to your PDB files
enzyme_pdb = './data/EGFR_TK.pdb'
substrate_pdb = './data/Erlotinib.pdb'

# Function to calculate pKa using Propka
def calculate_pKa(pdb_file):
    # Parse the PDB file and calculate pKa
    options = propka.lib.loadOptions(['--quiet'])  # Quiet mode
    molecule = propka.lib.initialize_protein(pdb_file, options)
    molecule.calculate_pka()

    # Print out the predicted pKa values
    for group in molecule.groups:
        print(f"Residue: {group.resName} {group.resNumb} - pKa: {group.pKa:.2f}")

# Calculate pKa for enzyme and substrate
print("Enzyme (EGFR_TK) pKa values:")
calculate_pKa(enzyme_pdb)

print("\nSubstrate (Erlotinib) pKa values:")
calculate_pKa(substrate_pdb)
