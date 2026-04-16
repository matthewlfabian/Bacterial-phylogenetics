rule gene_presence_absence:
    input:
        expand(config["blast_dir"] + "/{gene}_combined.txt", gene=GENES)
    output:
        txt = "BLAST/gene_presence_absence.txt"
    conda:
        "../envs/gene_presence_absence.yaml"
    log:
        "logs/gene_presence_absence.log"
    script:
        "../scripts/gene_presence_absence.py"
