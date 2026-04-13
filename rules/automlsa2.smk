rule automlsa2:
    input:
        expand(config["fasta_dir"] + "/{sample}.fasta", sample=SAMPLES)
    output:
        directory("automlsa2/output")
    threads: 8
    conda: "../envs/automlsa2.yaml"
    log:
        "logs/automlsa2.log"
    shell:
        "automlsa2 "
        "--dups "
        "--dir {config[fasta_dir]} "
        "--outgroup {config[automlsa2_outgroup]} "
        "--query {config[automlsa2_query]} "
        "--allow_missing 1 "
        "-t {threads} "
        "-- output"
