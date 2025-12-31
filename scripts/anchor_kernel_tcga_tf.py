# ============================================================
# TCGA-UCEC: Download STAR-Counts + clinical metadata (GDC)
# ============================================================

library(TCGAbiolinks)
library(SummarizedExperiment)
library(dplyr)
library(readr)
library(tibble)

# ---- Configuration des Chemins ----
# On cible directement le dossier data/raw du projet
out_dir <- file.path("data", "raw")
if (!dir.exists(out_dir)) {
  dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)
}

project <- "TCGA-UCEC"
workflow_type <- "STAR - Counts"

# ---- Query + Download + Prepare ----
message("✅ Connexion au GDC en cours...")
query <- GDCquery(
  project = project,
  data.category = "Transcriptome Profiling",
  data.type = "Gene Expression Quantification",
  workflow.type = workflow_type
)

message("✅ Téléchargement des données (GDC)...")
GDCdownload(query)
se <- GDCprepare(query)

# ---- Extraction des counts (gènes x échantillons) ----
counts <- assay(se)

# ---- Annotation des gènes ----
row_annot <- as.data.frame(rowData(se))
gene_annot <- row_annot %>%
  transmute(
    ensembl_gene_id = gene_id,
    gene_symbol     = gene_name,
    gene_type       = gene_type
  ) %>%
  distinct()

# ---- Métadonnées cliniques ----
col_meta <- as.data.frame(colData(se))
clinical <- GDCquery_clinic(project = project, type = "clinical")

sample_barcode <- colnames(counts)
patient_barcode <- substr(sample_barcode, 1, 12)

meta <- col_meta %>%
  mutate(
    sample_barcode = sample_barcode,
    patient_barcode = patient_barcode
  )

# Filtrage : Tumeurs primaires uniquement (code "01")
sample_type_code <- substr(meta$sample_barcode, 14, 15)
keep <- sample_type_code == "01"
counts <- counts[, keep, drop = FALSE]
meta <- meta[keep, , drop = FALSE]

# Fusion avec les données cliniques
meta_final <- meta %>%
  left_join(clinical, by = c("patient_barcode" = "submitter_id"))

# ---- Export pour Python (Orientation: Samples x Genes) ----
counts_t <- t(counts)
counts_df <- as.data.frame(counts_t) %>% 
  tibble::rownames_to_column("sample_barcode")

message("✅ Sauvegarde des fichiers dans data/raw/...")

write_csv(counts_df, file.path(out_dir, "counts_samples_x_genes.csv.gz"))
write_csv(meta_final, file.path(out_dir, "metadata_clinical_merged.csv.gz"))
write_csv(gene_annot, file.path(out_dir, "gene_annotation.csv.gz"))

message("✅ Acquisition terminée avec succès.")