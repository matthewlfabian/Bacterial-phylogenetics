# Bacterial phylogenetics

A Snakemake workflow for conducting phylogenetics analyses (average nucleotide identity, 
multi-locus sequence analysis, and gene presence/absence) on fragmented, near-complete, &/or 
complete bacterial genomes.

# Overview

This pipeline utilizes genome FASTA files as initial input for the
following steps:

- Average nucleotide identity (FastANI)
- Preparation of ANI matrix (Python)
- Multi-locus sequence analysis (automlsa2)
- Gene presence/absence (BLAST, Python)
- Preparation of annotated MLSA tree (R)

Snakemake is a workflow management tool that facilitates organization & 
reproducibility in bioinformatics workflows. Packages are designated via .yaml
files ("envs" directory), & their corresponding parameters are found in .smk files in the "rules"
directory. The "rule all" section of the Snakefile lists target outputs for the workflow, & Snakemake 
automatically determines which part(s) of the workflow to run, skipping any step whose output file 
already exists.

# Dependencies

All dependencies are managed automatically via Conda using the 
environment files in the `envs/` directory.

- FastANI
- assign_species
- automlsa2
- gene_presence_absence
- design_tree

# Setup
1.) Clone the repository and activate the Snakemake environment:

  git clone https://github.com/matthewlfabian/Bacterial-genome-assembly_Illumina-reads.git](https://github.com/matthewlfabian/Bacterial-phylogenetics.git
  
  conda activate snakemake

2.) Verify the installed repository:

  git remote -v

3.) Edit `config/config.yaml` to include your strain/samples. For example, for paired-end reads, 
strain/sample names from FASTA files are identified as follows: <strain_1>_1.FASTA, <strain_1>_2.FASTA, <strain_2>_2.FASTA...

  samples:
    - SAMPLE1
    - SAMPLE2
    - ...

  

# PICK UP HERE

This pipeline is designed to be run... To run the Snakemake workflow on a HPCC:

```bash
snakemake --cores 10 --use-conda
```

At any stage, a "dry run" can be conducted to verify the logic of the workflow:

To preview what Snakemake will run without executing anything:

```bash
snakemake --dry-run --cores 10 --use-conda
```

To visualize the workflow structure via a directed acyclic graph (DAG):

```bash
snakemake --dag | dot -Tpng > docs/dag.png
```




# Adjusting parameters
By editing the .smk files for each package in the "rules" subdirectory, parameters can be 
individually adjusted as desired. For example...


# Other information

### Author

Matthew L. Fabian, Ph.D.


### References



...
