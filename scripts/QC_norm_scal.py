#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 23 12:47:47 2025

@author: quentin
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt

#DATA LOADING

#counts
counts = pd.read_csv("/Users/quentin/Desktop/AI-DL_TCGA/counts_samples_x_genes.csv.gz",
    index_col=0
)

# Annotations gènes
gene_annot = pd.read_csv("/Users/quentin/Desktop/AI-DL_TCGA/gene_annotation.csv.gz",
    index_col=0
)

# Métadonnées cliniques
clinical = pd.read_csv(
    "/Users/quentin/Desktop/AI-DL_TCGA/metadata_clinical_merged.csv.gz",
    index_col=0
)



#MAPPING

# dictionnaire ENSG -> gene_name
gene_id_to_name = gene_annot["gene_symbol"].to_dict()
# remplacement des colonnes
counts = counts.rename(columns=gene_id_to_name)





#FILTERING QC


#QC genes
# Keep genes expressed in at least 20% of patients (équivalent min.cells sur seurat)
min_samples = int(0.2 * counts.shape[0])
genes_kept = (counts > 10).sum(axis=0) >= min_samples
counts_filtered = counts.loc[:, genes_kept]
# from 60 0000 we have 20 000

del counts
del gene_id_to_name



#Inutile ici
"""
#garder que les genes codant pour des proteines
protein_coding_genes = gene_annot[
    gene_annot["gene_type"] == "protein_coding"
].index

counts_filtered = counts_filtered.loc[
    :, counts_filtered.columns.intersection(protein_coding_genes)
]
"""



#NORMALISATION

library_size = counts_filtered.sum(axis=1)
cpm = counts_filtered.div(library_size, axis=0) * 1e6

counts_log_cpm = np.log2(cpm + 1)



#SCALING
scaler = StandardScaler()

counts_scaled = pd.DataFrame(
    scaler.fit_transform(counts_log_cpm),
    index=counts_log_cpm.index,
    columns=counts_log_cpm.columns
)



#EXPORT
counts_scaled.to_csv(
    "tcga_ucec_filtered_logCPM_scaled.csv.gz",
    compression="gzip"
)

#TEST

counts_scaled = pd.read_csv(
    "/Users/quentin/Desktop/AI-DL_TCGA/tcga_ucec_filtered_logCPM_scaled.csv.gz",
    index_col=0
)
