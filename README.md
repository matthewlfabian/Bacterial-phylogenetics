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
- Preparation of MLSA tree (R)
- Gene presence/absence (BLAST, Python)

Snakemake is a workflow management tool that facilitates organization & 
reproducibility in bioinformatics workflows. Packages are designated via .yaml
files ("envs" directory), & their corresponding parameters are found in .smk files in the "rules"
directory. The "rule all" section of the Snakefile lists target (e.g., trimmed FASTQs, 
scaffold FASTAs) outputs for the workflow, & Snakemake automatically determines which
part(s) of the workflow to run, skipping any step whose output file already exists.

# Dependencies

All dependencies are managed automatically via Conda using the 
environment files in the `envs/` directory.

- FastANI
- ...

# Setup
1.) Clone the repository and activate the Snakemake environment:

  git clone https://github.com/matthewlfabian/Bacterial-genome-assembly_Illumina-reads.git](https://github.com/matthewlfabian/Bacterial-phylogenetics.git
  
  conda activate snakemake

2.) Verify the installed repository:

  git remote -v

3.) Edit `config/config.yaml` to include your strain/sample names. For example, for paired-end reads, 
strain/sample names from FASTA files are identified as follows: <strain_1>_1.FASTA, <strain_1>_2.FASTA, <strain_2>_2.FASTA...

  samples:
    - SAMPLE1
    - SAMPLE2
    - ...

# Running the Pipeline

This pipeline is designed to be run in 4 stages: 1.) initial quality assessment of raw FASTQs; 
2.) FASTQ trimming and quality assessment of trimmed reads; 3.) genome assembly and quality assessment; 
& 4.) genome annotation. By utilizing the comment mark (#) in the Snakefile, the workflow can be run stepwise, 
permitting the review of FastQC, MultiQC, & QUAST QC reports before subsequent steps. The workflow can be run 
in full by "uncommenting" all stages in the Snakefile. To run the Snakemake workflow on a HPCC:

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


#### Stage 1: Raw read quality assessment
To FastQC and MultiQC on raw reads, then review the MultiQC report 
before proceeding to FASTQ trimming, "comment out" (add "#") Stages 2-4
in the Snakefile, "rules" section, & run Snakemake. Review `MultiQC/raw/multiqc_report.html` 
before continuing.

#### Stage 2: Trimming & trimmed read quality assessment
To proceed with trimming and a subsequent MultiQC report, "uncomment" Stage 2
in the Snakefile & run Snakemake. Review `MultiQC/trimmed/multiqc_report.html` before 
continuing.

#### Stage 3: Assembly & quality assessment
To proceed with assembly & QC, "uncomment" Stage 3 in the Snakefile & run
Snakemake.

#### Stage 4: Annotation
To proceed with annotation, "uncomment" Stage 4 in the Snakefile & run
Snakemake.

# Adjusting parameters
By editing the .smk files for each package in the "rules" subdirectory, parameters can be 
individually adjusted as desired. For example, to adjust k-mer utilization for assembly 
via SPAdes, open SPAdes.smk & edit the "-k" parameter.


# Other information

### Author

Matthew L. Fabian, Ph.D.


### References



Seemann, T. (2014). Prokka: Rapid prokaryotic genome annotation. Bioinformatics, 30(14), 2068–2069. https://doi.org/10.1093/bioinformatics/btu153
