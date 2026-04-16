import pandas as pd
import numpy as np
from pathlib import Path

gene_files      = snakemake.config["gene_files"]
query_lengths   = snakemake.config["query_lengths"]
identity_thresh = snakemake.config["identity_thresh"]
coverage_thresh = snakemake.config["coverage_thresh"]
evalue_thresh   = snakemake.config["evalue_thresh"]

def load_blast_files(gene_files: dict, data_dir: str = ".") -> pd.DataFrame:
    frames = []
    for gene, fname in gene_files.items():
        path = Path(data_dir) / fname
        df = pd.read_csv(path, sep="\t", header=0)
        df["gene"] = gene
        frames.append(df)
    return pd.concat(frames, ignore_index=True)
df = load_blast_files(gene_files, data_dir=".")

def add_coverage(df: pd.DataFrame, query_lengths: dict) -> pd.DataFrame:
    df = df.copy()
    df["query_length"] = df["gene"].map(query_lengths)
    df["query_coverage"] = (df["q_end"] - df["q_start"] + 1) / df["query_length"] * 100
    return df
df = add_coverage(df, query_lengths)

def flag_true_hits(df: pd.DataFrame,
                   identity_thresh: float = identity_thresh,
                   coverage_thresh: float = coverage_thresh,
                   evalue_thresh:   float = evalue_thresh) -> pd.DataFrame:
    df = df.copy()
    df["true_hit"] = (
        (df["percent_identity"] >= identity_thresh) &
        (df["query_coverage"]   >= coverage_thresh) &
        (df["evalue"]           <= evalue_thresh)
    )
    return df
df = flag_true_hits(df)

presence = (
    df[df["true_hit"]]
    .groupby(["strain", "gene"])
    .size()
    .gt(0)
    .astype(int)
    .unstack(fill_value=0)
    .reset_index()
)

for gene in df["gene"].unique():
    if gene not in presence.columns:
        presence[gene] = 0
presence.to_csv("gene_presence_absence.txt", sep="\t", index=False)
