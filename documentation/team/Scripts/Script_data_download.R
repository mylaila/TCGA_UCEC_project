# ============================================================
# TCGA-UCEC: Download HTSeq-Counts + clinical metadata (GDC)
# Export for Python (CSV.GZ)
# ============================================================

if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager")
pkgs <- c("TCGAbiolinks", "SummarizedExperiment", "dplyr", "readr")
for (p in pkgs) {
  if (!requireNamespace(p, quietly = TRUE)) BiocManager::install(p, update = FALSE, ask = FALSE)
}
library(TCGAbiolinks)
library(SummarizedExperiment)
library(dplyr)
library(readr)

# ---- Parameters ----
project <- "TCGA-UCEC"
out_dir <- "tcga_ucec_counts_export"
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)

workflow_type <- "STAR - Counts"
keep_primary_tumor_only <- TRUE  # TCGA sample type code "01"

# ---- Query + Download + Prepare ----
query <- GDCquery(
  project = project,
  data.category = "Transcriptome Profiling",
  data.type = "Gene Expression Quantification",
  workflow.type = workflow_type
)
GDCdownload(query)
se <- GDCprepare(query)  # SummarizedExperiment

# ---- Extract counts (genes x samples) ----
counts <- assay(se)

# ---- Gene annotation ----
row_annot <- as.data.frame(rowData(se))
gene_annot <- row_annot %>%
  transmute(
    ensembl_gene_id = gene_id,
    gene_symbol     = gene_name,
    gene_type       = gene_type
  ) %>%
  distinct()

# ---- Sample + clinical metadata ----
col_meta <- as.data.frame(colData(se))
clinical <- GDCquery_clinic(project = project, type = "clinical")

sample_barcode <- colnames(counts)
patient_barcode <- substr(sample_barcode, 1, 12)

meta <- col_meta %>%
  mutate(
    sample_barcode = sample_barcode,
    patient_barcode = patient_barcode
  )

# Filter primary tumor samples only (code "01")
if (keep_primary_tumor_only) {
  sample_type_code <- substr(meta$sample_barcode, 14, 15)
  keep <- sample_type_code == "01"
  counts <- counts[, keep, drop = FALSE]
  meta <- meta[keep, , drop = FALSE]
}

# Merge clinical (by patient barcode)
meta2 <- meta %>%
  left_join(clinical, by = c("patient_barcode" = "submitter_id"))

# ---- Export for Python ----
# Python-friendly orientation: samples x genes
counts_t <- t(counts)

# Add sample_barcode as first column
counts_df <- as.data.frame(counts_t) %>% tibble::rownames_to_column("sample_barcode")

write_csv(counts_df, file.path(out_dir, "counts_samples_x_genes.csv.gz"))
write_csv(meta2,     file.path(out_dir, "metadata_clinical_merged.csv.gz"))
write_csv(gene_annot,file.path(out_dir, "gene_annotation.csv.gz"))

saveRDS(list(se = se, counts = counts, meta = meta2, gene_annot = gene_annot),
        file.path(out_dir, "tcga_ucec_counts_export.rds"))

message("Done. Exported to: ", normalizePath(out_dir))
message(" - counts_samples_x_genes.csv.gz")
message(" - metadata_clinical_merged.csv.gz")
message(" - gene_annotation.csv.gz")
