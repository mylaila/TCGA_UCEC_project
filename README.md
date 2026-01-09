# TCGA_UCEC_project

Projet d'analyse transcriptomique des données TCGA-UCEC (Uterine Corpus Endometrial Carcinoma) avec apprentissage automatique pour la prédiction de survie à 5 ans.

## 📋 Vue d'ensemble

Pipeline complet d'acquisition, prétraitement et modélisation de données RNA-Seq TCGA :
- **Cohorte** : 553 patientes UCEC
- **Target** : Prédiction survie globale à 5 ans (OS5)
- **Approches ML** : MLP supervisé + Autoencodeur non-supervisé
- **Features** : Données transcriptomiques (jusqu'à 4096 gènes) + cliniques (FIGO stage, grade)

## 🔧 Environnement

**Environnement conda** : `tcga_tf`

**Dépendances principales** :
- Python 3.x
- TensorFlow / Keras (autoencodeur)
- pandas, numpy, scipy
- scikit-learn
- matplotlib, seaborn
- lifelines (analyse de survie)
- umap-learn
- R + TCGAbiolinks (acquisition des données)

Pour créer l'environnement :
```bash
conda activate tcga_tf
```

## 📓 Pipeline Notebooks

### [0A_data_acquisition.ipynb](0A_data_acquisition.ipynb)
- Téléchargement des données TCGA via **TCGAbiolinks** (script R)
- Extraction des comptages bruts RNA-Seq + métadonnées cliniques
- Export dans `data/raw/`

### [0B_qc_normalization.ipynb](0B_qc_normalization.ipynb)
- Mapping Ensembl ID → Gene Symbol
- Filtrage QC (gènes faiblement exprimés)
- Normalisation Log2-CPM
- Analyses exploratoires (PCA, t-SNE, UMAP)
- Export dans `data/processed/normalized/`

### [0C_ml_preprocessing.ipynb](0C_ml_preprocessing.ipynb)
- **Target Engineering** : Définition variable OS à 5 ans + audit temporalité
- **Feature Selection** :
  - Supervised (1000 gènes) : Mann-Whitney + filtrage redondance
  - Unsupervised (3000 gènes) : Variance + filtrage colinéarité
- Intégration variables cliniques (FIGO stage, grade)
- Export dans `data/processed/ml_ready/`

### [0E_ml_autoencodeur.ipynb](0E_ml_autoencodeur.ipynb)
- Entraînement autoencodeur (4096 → 32 dim latent)
- Évaluation bottleneck (32 vs 64 dim)
- Extraction espace latent Z
- Validation kNN (k=10) : espace brut vs latent
- Export dans `data/results/autoencodeur/` et `data/models/autoencodeur/`

## 📂 Structure des données

```
data/
├── raw/                    # Comptages bruts + métadonnées TCGA
├── processed/
│   ├── normalized/         # Données normalisées (Log2-CPM)
│   ├── ml_ready/           # Features sélectionnées + target
│   └── clinical/           # Variables cliniques
├── artefacts/              # Figures + statistiques intermédiaires
│   ├── qc_analysis/
│   ├── exploratory_data_analysis/
│   ├── survival_analysis/
│   └── feature_selection/
├── models/
│   └── autoencodeur/       # Modèles Keras sauvegardés
└── results/
    └── autoencodeur/       # Espace latent Z + figures
```

## ⚠️ Fichiers volumineux

Certains fichiers de données (>100 Mo) ne sont pas versionnés sur GitHub :
- `expr_norm_tcga_ucec.tsv`
- `expr_patient_level_tcga_ucec.tsv`

**Pour obtenir ces fichiers**, merci de contacter l'auteur ou consulter le stockage externe.

## 🚀 Utilisation

1. Activer l'environnement conda :
```bash
conda activate tcga_tf
```

2. Exécuter les notebooks dans l'ordre (0A → 0B → 0C → 0E)

3. Les résultats sont exportés automatiquement dans les répertoires `data/`
