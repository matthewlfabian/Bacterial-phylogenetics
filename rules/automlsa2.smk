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
        "--missing_check "
        "--allow_missing 1 "
        "-t {threads} "
        "-- output"
        "> {log} 2>&1 && "
        "mv output automlsa2/output"
