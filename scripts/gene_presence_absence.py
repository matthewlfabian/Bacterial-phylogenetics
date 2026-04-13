import pandas as pd
import numpy as np
from pathlib import Path

def load_blast_files(gene_files: dict, data_dir: str = ".") -> pd.DataFrame:
    frames = []
    for gene, fname in gene_files.items():
        path = Path(data_dir) / fname
        df = pd.read_csv(path, sep="\t", header=1)
        df.columns = COL_NAMES
        df["gene"] = gene
        frames.append(df)
    return pd.concat(frames, ignore_index=True)
df = load_blast_files(GENE_FILES, data_dir=".")

def add_coverage(df: pd.DataFrame, query_lengths: dict) -> pd.DataFrame:
                    df = df.copy()
    df["query_length"] = df["gene"].map(query_lengths)
    df["query_coverage"] = (df["q_end"] - df["q_start"] + 1) / df["query_length"] * 100
    return df
df = add_coverage(df, QUERY_LENGTHS)

IDENTITY_THRESH = 40.0
COVERAGE_THRESH = 70.0
EVALUE_THRESH   = 1e-5  

def flag_true_hits(df: pd.DataFrame,
                   identity_thresh: float = IDENTITY_THRESH,
                   coverage_thresh: float = COVERAGE_THRESH,
                   evalue_thresh:   float = EVALUE_THRESH) -> pd.DataFrame:
    df = df.copy()
    df["true_hit"] = (
        (df["percent_identity"] >= identity_thresh) &
        (df["query_coverage"]   >= coverage_thresh) &
        (df["evalue"]           <= evalue_thresh)
    )
    return df
df = flag_true_hits(df)

print(df[["strain", "gene", "percent_identity", "query_coverage", "evalue", "true_hit"]].head(12))
df.to_excel("hits_all.xlsx", index=False)
