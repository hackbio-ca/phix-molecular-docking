# pHix Molecular Docking
A pH-Adaptive Protein-Ligand Simulation Tool to Enhance Molecular Docking Accuracy

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Abstract

Molecular docking, which predicts how a protein and a small molecule (ligand) interact, is a cornerstone of drug discovery and biochemical research.<sup>1,2</sup> However, most current docking tools do not account for the impact of varying pH levels, which can significantly alter the charge and structure of proteins and ligands.<sup>3,4</sup> These changes influence the binding accuracy, leading to inconsistent results and limiting the effectiveness of such models in real-world applications.<sup>4</sup> This problem is critical because precise protein-ligand interactions are essential for understanding drug efficacy and biochemical mechanisms.<sup>1,2</sup>

To address this limitation, we introduce pHix, a novel tool designed to improve docking accuracy by dynamically adjusting protonation states of proteins and ligands based on their experimental or desired pH environments. With a user-defined pH, pHix asks users to upload PDB files for structure of proteins and their relavant ligands, and then adjusts them to ensure molecular docking simulations reflect those biologically relevant pH conditions. This leads to more accurate presentation/prediction of binding interactions and improves the overall reliability of docking models in diverse pH-sensitive systems.

Thus, by bridging the gap between experimental structural data and desired simulation conditions, pHix offers a transformative approach that allows researchers to create more accurate and context-sensitive models, paving the way for enhanced future drug discovery and deeper insights into biochemical processes.<sup>2</sup>

## Refrences

1- Morris, C. J., & Della Corte, D. (2021). USING MOLECULAR DOCKING AND MOLECULAR DYNAMICS TO INVESTIGATE PROTEIN-LIGAND INTERACTIONS. Modern Physics Letters B, 35(08), 2130002. https://doi.org/10.1142/S0217984921300022

2- Meng, X. Y., Zhang, H. X., Mezei, M., & Cui, M. (2011). MOLECULAR DOCKING: A POWERFUL APPROACH FOR STRUCTURE-BASED DRUG DISCOVERY. Current Computer-Aided Drug Design, 7(2), 146-157. https://doi.org/10.2174/157340911795677602

3- Antunes, D. A., Devaurs, D., & Kavraki, L. E. (2015). UNDERSTANDING THE CHALLENGES OF PROTEIN FLEXIBILITY IN DRUG DESIGN. Expert Opinion on Drug Discovery, 10(12), 1301–1313. https://doi.org/10.1517/17460441.2015.1094386

4- Onufriev, A. V., & Alexov, E. (2013). PROTONATION AND PK CHANGES IN PROTEIN–LIGAND BINDING. Quarterly Reviews of Biophysics, 46(2), 181–209. https://doi.org/10.1017/S0033583513000054



## Requirements

- Python 3.x
- Conda (package manager)

## Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### Step 2: Set Up Conda Environment

```bash
conda create -n bioinfo-env python=3.8
conda activate bioinfo-env
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install External Tools

```bash
conda install -c conda-forge propka pdb2pqr openbabel
```

Verify installations:

```bash
propka3 --version
pdb2pqr --version
obabel --version
```

## Running the App

```bash
python app.py
```

Open your browser at `http://127.0.0.1:5000`.

## Using the Web App

1. **Upload Files**: Upload enzyme and substrate PDB files.
2. **Enter pH**: Input pH value (0-14). Invalid pH values will display an error.
3. **Process**: The app will compute pKa and adjust protonation states.
4. **Download Files**: Download the adjusted files as a ZIP package.





## Contribute

Contributions are welcome! If you'd like to contribute, please open an issue or submit a pull request. See the [contribution guidelines](CONTRIBUTING.md) for more information.

## Support

If you have any issues or need help, please open an [issue](https://github.com/hackbio-ca/snv-effect-prediction-alzheimers/issues) or contact the project maintainers.

## License

This project is licensed under the [MIT License](LICENSE).
