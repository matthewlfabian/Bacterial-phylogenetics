# Steps: FastANI & Python script => autoMLSA2 => tblastn

configfile: "config/config.yaml"

SAMPLES = config["samples"]

include: "rules/FastANI.smk"
include: "rules/assign_species.smk"

rule all:
    input:
        # Stage 1: ANI-based species assignment
        "FastANI/output.txt",
        "FastANI/output.txt.matrix",
        "FastANI/strain_species_assigned.txt",
        "FastANI/ANI_matrix_species_ordered.txt",

        # Stage 2: MLSA phylogeny; uncomment to continue
        # "automlsa2/[output]",

        # Stage 3: gene presence/absence; uncomment to continue
        # expand("tblastn/{sample}_results.tsv", sample=SAMPLES),
