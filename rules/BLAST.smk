STRAINS = config["samples"]
GENES = list(config["blast_queries"].keys())

rule makeblastdb:
    input:
        fasta = config["fasta_dir"] + "/{strain}.fasta"
    output:
        nsq = config["blast_db_dir"] + "/{strain}.nsq",
        nin = config["blast_db_dir"] + "/{strain}.nin",
        nhr = config["blast_db_dir"] + "/{strain}.nhr"
    conda:
        "../envs/BLAST.yaml"
    shell:
        """
        makeblastdb -in {input.fasta} -dbtype nucl \
            -out {config[blast_db_dir]}/{wildcards.strain}
        """

rule tblastn:
    input:
        db_nsq = config["blast_db_dir"] + "/{strain}.nsq",
        query  = lambda wc: config["blast_queries"][wc.gene]
    output:
        config["blast_dir"] + "/{gene}/{strain}.txt"
    threads: 8
    conda:
        "../envs/BLAST.yaml"
    shell:
        """
        echo -e "strain\tquery_id\tsubject_id\tpercent_identity\talignment_length\t\
mismatches\tgap_opens\tq_start\tq_end\ts_start\ts_end\tevalue\tbit_score" > {output}
        tblastn -query {input.query} \
            -db {config[blast_db_dir]}/{wildcards.strain} \
            -num_threads {threads} \
            -evalue 1e-5 \
            -max_target_seqs 10 \
            -max_hsps 1 \
            -soft_masking true \
            -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore" \
        | awk -v base="{wildcards.strain}" 'BEGIN{{OFS="\t"}} {{print base, $0}}' >> {output}
        """

rule combine_blast:
    input:
        expand(config["blast_dir"] + "/{gene}/{strain}.txt", strain=STRAINS, allow_missing=True)
    output:
        config["blast_dir"] + "/{gene}_combined.txt"
    shell:
        """
        awk 'NR==1 || FNR!=1' {input} > {output}
        """
