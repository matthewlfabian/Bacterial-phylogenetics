rule assign_species:
    input:
        ani="FastANI/output.txt",
        meta=config["strains_meta"]
    output:
        strain_species="FastANI/strain_species_assigned.txt",
        ani_matrix="FastANI/ANI_matrix_species_ordered.txt"
    conda:
        "envs/assign_species.yaml"
    log:
        "logs/assign_species.log"
    script:
        "scripts/assign_species.py"
