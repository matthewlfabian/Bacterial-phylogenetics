import pandas as pd
import networkx as nx

ani = pd.read_csv(snakemake.input.ani, sep="\t")
meta = pd.read_csv(snakemake.input.meta, sep="\t")

G = nx.Graph()
for _, row in ani.iterrows():
    if row["ANI"] >= 95:
        G.add_edge(row["strain_1"], row["strain_2"])

all_strains = set(ani["strain_1"]) | set(ani["strain_2"])
G.add_nodes_from(all_strains)
components = list(nx.connected_components(G))

strain_to_species = {}
species_counter = 1
meta_dict = dict(zip(meta["strain"], meta["species"]))

for comp in components:
    canonical = {
        meta_dict[s] for s in comp
        if s in meta_dict and pd.notna(meta_dict[s])
    }
    if canonical:
        species_name = sorted(canonical)[0]
    else:
        species_name = f"species_{species_counter:03d}"
        species_counter += 1
    for s in comp:
        strain_to_species[s] = species_name

strain_df = pd.DataFrame({
    "strain": list(all_strains),
    "species": [strain_to_species[s] for s in all_strains]
})
strain_df = strain_df.sort_values(["species", "strain"])

ani_matrix = ani.pivot(index="strain_1", columns="strain_2", values="ANI")
ani_matrix = ani_matrix.combine_first(ani_matrix.T)
for s in ani_matrix.index:
    ani_matrix.loc[s, s] = 100.0

order = strain_df["strain"].tolist()
ani_matrix = ani_matrix.reindex(index=order, columns=order)

strain_df.to_csv(snakemake.output.strain_species, sep="\t", index=False)
ani_matrix.to_csv(snakemake.output.ani_matrix, sep="\t")
