# Analyse transcriptomique TCGA-UCEC

Projet M2 AIDA – Analyse différentielle de l'expression génique dans le cancer de l'endomètre  
(*Uterine Corpus Endometrial Carcinoma, TCGA-UCEC*)

**Repository** : https://github.com/mylaila/TCGA_UCEC_project

---

## Vue d'ensemble

Ce projet analyse des données RNA-seq issues du projet **TCGA-UCEC (The Cancer Genome Atlas – Uterine Corpus Endometrial Carcinoma)** afin d'identifier les gènes différentiellement exprimés et de caractériser les signatures moléculaires associées au cancer de l'endomètre.

L'analyse repose sur un pipeline structuré comprenant une exploration des données, un contrôle qualité, une sélection de cohorte, une préparation pseudobulk et une analyse différentielle avec **DESeq2**, suivie d'analyses d'enrichissement fonctionnel.

### Cohorte analysée
- Données TCGA-UCEC
- Échantillons tumoraux et normaux
- Définition finale de la cohorte réalisée après contrôle qualité (QC)

---

## Structure du projet

```
TCGA_UCEC_project/
├── data/
│   ├── raw/                              # Données brutes (intouchables)
│   │
│   ├── processed/                        # Données intermédiaires persistées
│   │   ├── normalized/                   # Données normalisées
│   │   ├── qc_filtered/                  # Données après contrôle qualité
│   │   ├── cohort_filtered/              # Données restreintes à la cohorte finale
│   │   ├── single_cell_objects/           # Objets intermédiaires (AnnData, Seurat…)
│   │   └── pseudobulk/                   # Matrices pseudobulk (entrée DESeq2)
│   │
│   └── artefacts/                        # Tables et figures par étape du pipeline
│       ├── exploratory_data_analysis/     # EDA
│       │   ├── tables/
│       │   └── figures/
│       │
│       ├── qc_analysis/                   # Analyse QC
│       │   ├── tables/
│       │   └── figures/
│       │
│       ├── cohort_selection/              # Sélection de cohorte
│       │   ├── tables/
│       │   └── figures/
│       │
│       ├── single_cell_analysis/           # Analyse principale
│       │   ├── tables/
│       │   └── figures/
│       │
│       ├── pseudobulk_preparation/         # Préparation pseudobulk
│       │   ├── counts/
│       │   └── metadata/
│       │
│       ├── differential_expression/        # Analyse différentielle (DESeq2)
│       │   ├── tables/
│       │   └── figures/
│       │
│       └── functional_enrichment/          # Enrichissement fonctionnel (GO, pathways)
│           ├── tables/
│           └── figures/
│
├── documentation/                         # Documentation du projet
├── tmp_cache/                             # Fichiers temporaires
└── notebooks/                             # Notebooks et scripts principaux
```

---

## Environnement technique

**Python** (3.8+) :
- pandas
- numpy
- matplotlib
- seaborn
- scipy
- scikit-learn

**R** (4.0+) :
- DESeq2
- clusterProfiler
- org.Hs.eg.db
- ggplot2
- pheatmap

---

**Auteurs** : Projet M2 AIDA - Groupe n  
**Date** : Janvier 2026
