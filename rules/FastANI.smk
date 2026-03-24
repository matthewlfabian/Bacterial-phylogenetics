# --matrix: outputs pairwise distance matrix
# --threads: parallel threads

rule FastANI:
    input:
        expand("FASTA/{sample}.fasta", sample=SAMPLES)
    output:
        ani = "FastANI/output.txt",
        matrix = "FastANI/output.txt.matrix"
    threads: 16
    conda: "../envs/FastANI.yaml"
    shell:
        "ls FASTA/*.fasta > FastANI/file_list.txt && "
        "fastANI --ql FastANI/file_list.txt "
        "--rl FastANI/file_list.txt "
        "--matrix "
        "-o {output.ani} "
        "--threads {threads}"
