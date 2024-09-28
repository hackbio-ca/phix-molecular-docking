# Phix

Improve Enformer’s predictions of Single Nucleotide Variant effects on Alzheimer's Disease using diverse genomic datasets to address mis-directions in predicted gene expression changes.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Abstract

This project focuses on improving the predictive capabilities of Enformer, an advanced model for assessing the effects of Single Nucleotide Variants (SNVs) on Alzheimer's Disease (AD). Enformer, detailed by AlQuraishi et al. (2021), is currently the leading model for predicting functional outputs from sub-sequences of the reference genome. Despite its proficiency, a significant challenge remains: the model exhibits mis-direction in Pearson R correlations between predicted and observed gene expression levels caused by SNVs. Specifically, while Enformer can predict whether a variant affects gene expression and to what magnitude, it struggles to determine whether the effect is an increase or decrease.

This issue primarily arises from unsupported driver SNVs and the model's limited capacity to predict gene expression from genomic DNA regions distal to transcription start sites, even with the use of larger input DNA sequences.

To address these limitations, the project proposes training Enformer on a more diverse set of input-output pairs from various genomes and gene expression datasets. The original dataset used includes the [ROSMAP study on Alzheimer's in the U.S. population](https://www.synapse.org/Synapse:syn3219045), which provides a foundation for understanding gene expression in AD.

The project will explore additional datasets to enhance model training:

- **Japanese Population Dataset**: From a [study on Alzheimer's Disease](https://www.nature.com/articles/s41380-022-01483-0), which includes several Asian-specific rare pathogenic variants. This dataset promises greater diversity and the potential to uncover novel insights. Authors can be contacted for dataset access upon reasonable request.

- **European Population Dataset**: A large-scale dataset on Alzheimer's Disease in Finnish and other European populations ([Link to dataset](https://alz-journals.onlinelibrary.wiley.com/doi/10.1002/alz.12319)). While comprehensive, obtaining this dataset may be challenging and may not use the same metrics.

- **Smaller Dataset**: A study with a smaller scale but manageable size, including blood eQTLs ([Link to dataset](https://alz-journals.onlinelibrary.wiley.com/doi/pdf/10.1002/alz.043801)).

The proposed direction involves training Enformer on these new datasets to improve its performance in predicting both the magnitude and the sign (direction) of causal eQTLs. The evaluation will focus on these signed values and other applicable metrics to refine the model's predictive accuracy concerning AD-related gene expression changes.

## Installation

Provide instructions on how to install and set up the project, such as installing dependencies and preparing the environment.

```bash
# Example command to install dependencies (Python)
pip install project-dependencies

# Example command to install dependencies (R)
install.packages("project-dependencies")
```

## Quick Start

Provide a basic usage example or minimal code snippet that demonstrates how to use the project.

```python
# Example usage (Python)
import my_project

demo = my_project.example_function()
print(demo)
```
```r
# Example usage (R)
library(my_project)

demo <- example_function()
print(demo)
```

## Usage

Add detailed information and examples on how to use the project, covering its major features and functions.

```python
# More usage examples (Python)
import my_project

demo = my_project.advanced_function(parameter1='value1')
print(demo)
```
```r
# More usage examples (R)
library(demoProject)

demo <- advanced_function(parameter1 = "value1")
print(demo)
```

## Contribute

Contributions are welcome! If you'd like to contribute, please open an issue or submit a pull request. See the [contribution guidelines](CONTRIBUTING.md) for more information.

## Support

If you have any issues or need help, please open an [issue](https://github.com/hackbio-ca/snv-effect-prediction-alzheimers/issues) or contact the project maintainers.

## License

This project is licensed under the [MIT License](LICENSE).
