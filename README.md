# Bacterial phylogenetics

A Snakemake workflow for conducting phylogenetics analyses (average nucleotide identity, 
multi-locus sequence analysis, and gene presence/absence) on fragmented, near-complete, &/or 
complete bacterial genomes.

# Overview

This workflow utilizes genome FASTA files as initial input for the
following steps:

- Average nucleotide identity (FastANI)
- Preparation of ANI matrix (Python script)
- Multi-locus sequence analysis (automlsa2)
- Gene presence/absence (BLAST, Python script)
- Preparation of annotated MLSA tree (R script)

Snakemake is a workflow management tool that facilitates organization & 
reproducibility in bioinformatics workflows. Packages are designated via .yaml
files ("envs" directory), & their corresponding parameters are found in .smk files in the "rules"
directory. The "rule all" section of the Snakefile lists target outputs for the workflow, & Snakemake 
automatically determines which part(s) of the workflow to run, skipping any step whose output file 
already exists.

# Dependencies

All dependencies are managed automatically via Conda using the 
environment files in the `envs/` directory.

# Setup
1.) On your HPCC cluster or local machine, create a parent directory (e.g., "phylogenetics"). In that parent directory, clone the repository and activate the Snakemake environment:

  git clone https://github.com/matthewlfabian/Bacterial-genome-assembly_Illumina-reads.git](https://github.com/matthewlfabian/Bacterial-phylogenetics.git
  
  conda activate snakemake

2.) Verify the installed repository:

  git remote -v

3.) Edit "config/config.yaml" to include your strain/samples. For example, for paired-end reads, 
strain/sample names from FASTA files are identified as follows: <strain_1>.FASTA, <strain_2>.FASTA, etc.

  samples:
    - SAMPLE1
    - SAMPLE2
    - ...

4.) In the parent directory, create a subdirectory, "FASTA". In "FASTA", add your input samples in ".FASTA" format, matching the 
sample names entered in step 3.).

5.) In the parent directory, create a subdirectory, "FastANI". In "FastANI", & per "config/config.yaml", create the tab-delimited text file "strains.txt", which lists the 
user-defined strains (without ".FASTA" extension). This file should have a 2nd column, "species", to add designated species names for strains, as appropriate. This enables 
the "assign_species.py" Python script to utilize designated species names when assigning species groups to as-yet-unidentified strains.

6.) In the parent directory, create a subdirectory, "BLAST". In "BLAST", add the amino acid FASTA files (i.e., ".FAA" format) for each gene of interest. These files are utilized
as tblastn queries to identify the presence of those genes in the FASTA files for your input strains.

# Running the workflow

To run the Snakemake workflow on a HPCC:

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

### Overview
User-defined input genomes in ".FASTA" format are utilized by FastANI, in "all vs. all" mode, to calculate the pairwise average nucleotide identities (ANIs). Next, the 
"assign_species.py" Python script utilizes the FastANI outputs, as well as any user-defined species designations in "strains.txt", to assign strains to species-level 
groups. Gene presence/absence for user-defined gene queries (".FAA" format) is performed via BLAST (tblastn), followed by the "gene_presence_absence.py" Python script. AutoMLSA2 
is utilized to generate a Newick file (".nex.iqtree" format) for producing a phylogenetic tree. Lastly, the "phylogenetic_tree.R" R script utilizes the Newick file, as well as 
the gene presence/absence output, to produced an annotated, circular phylogenetic tree.


# Adjusting parameters
By editing the .smk files for each package in the "rules" subdirectory, parameters can be 
individually adjusted as desired. For example...


# Other information

### Author

Matthew L. Fabian, Ph.D.


### References



...
