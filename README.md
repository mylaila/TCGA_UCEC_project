# TCGA_UCEC_project
Projet M2 d'analyse transcriptomique des données TCGA-UCEC (Uterine Corpus Endometrial Carcinoma - Cancer de l'endomètre) avec apprentissage automatique pour la prédiction de survie à 5 ans.

## Contributeurs

<br>**Klervi Le Dortz** 
  1.Script_data_download.R / 
  1.visualization.ipynb / 
  4.Autoencoder+kNN_Target=reccurence.ipynb / 
  
<br>**Quentin Marandon** 
  3.QC_norm_scal.py / 
  4.histo_mlp.ipynb / 

<br>**Laïla EL BOUHALI** 
  0A_data_acquisition.ipynb / 
  0B_qc_normalization.ipynb / 
  0C_ml_preprocessing.ipynb / 
  0D_ml_supervised_mlp.ipynb / 
  0E_ml_autoencodeur.ipynb / 

## Vue d'ensemble

Pipeline complet d'acquisition, prétraitement et modélisation de données RNA-Seq TCGA :
- **Cohorte** : 553 patientes UCEC
- **Target** : Prédiction survie globale à 5 ans (OS5)
- **Approches ML** : MLP supervisé + Autoencodeur non-supervisé
- **Features** : Données transcriptomiques (jusqu'à 4096 gènes) + cliniques (FIGO stage, grade)

## Installation

**Environnement conda** : `tcga_tf`

```bash
# Créer l'environnement (si nécessaire)
conda create -n tcga_tf python=3.10

# Activer l'environnement
conda activate tcga_tf

# Installer les dépendances
pip install tensorflow pandas numpy scipy scikit-learn matplotlib seaborn lifelines umap-learn
```

**Dépendances principales** :
- Python 3.10
- TensorFlow / Keras
- pandas, numpy, scipy
- scikit-learn
- matplotlib, seaborn
- lifelines
- umap-learn
- R + TCGAbiolinks (pour 0A uniquement)

## Pipeline Notebooks

### [0A_data_acquisition.ipynb](0A_data_acquisition.ipynb)
**Acquisition des données TCGA**
- Téléchargement des données TCGA via **TCGAbiolinks** (script R)
- Extraction des comptages bruts RNA-Seq + métadonnées cliniques

**Fichiers de sortie** → utilisés par 0B :
- `data/raw/count_matrix_tcga_ucec.tsv` (comptages bruts)
- `data/raw/clinical_data_tcga_ucec.tsv` (métadonnées cliniques)

---

### [0B_qc_normalization.ipynb](0B_qc_normalization.ipynb)
**Contrôle qualité et normalisation**
- Mapping Ensembl ID → Gene Symbol
- Filtrage QC (gènes faiblement exprimés)
- Normalisation Log2-CPM
- Analyses exploratoires (PCA, t-SNE, UMAP)

**Fichiers d'entrée** :
- `data/raw/count_matrix_tcga_ucec.tsv`
- `data/raw/clinical_data_tcga_ucec.tsv`

**Fichiers de sortie** → utilisés par 0C :
- `data/processed/normalized/expr_norm_tcga_ucec.tsv` (matrice normalisée)
- `data/processed/normalized/expr_patient_level_tcga_ucec.tsv` (niveau patient)

---

### [0C_ml_preprocessing.ipynb](0C_ml_preprocessing.ipynb)
**Préparation des données pour ML**
- **Target Engineering** : Définition variable OS à 5 ans + audit temporalité
- **Feature Selection** :
  - Supervised (189 gènes + 5 cliniques) : Mann-Whitney (top 200) + filtrage corrélation > 0.85
  - Unsupervised (4096 gènes) : Sélection par haute variance (optimisée via test MSE)
- Intégration variables cliniques (FIGO stage, grade)

**Fichiers d'entrée** :
- `data/processed/normalized/expr_norm_tcga_ucec.tsv`
- `data/processed/normalized/expr_patient_level_tcga_ucec.tsv`

**Fichiers de sortie** → utilisés par 0D et 0E :
- `data/processed/ml_ready/X_supervised.csv` (189 gènes + 5 cliniques = 194 features)
- `data/processed/ml_ready/X_unsupervised.csv` (4096 gènes)
- `data/processed/ml_ready/y_target.csv` (target OS5)
- `data/processed/ml_ready/clinical_features.csv`

---

### [0D_ml_mlp.ipynb](0D_ml_mlp.ipynb) *(si applicable)*
**Modèle MLP supervisé**
- Entraînement MLP pour prédiction de survie
- Validation croisée et optimisation hyperparamètres

**Architecture** :
- 194 → Dense(64, ReLU) + BatchNorm + Dropout(0.5) → Dense(16, ReLU) + Dropout(0.3) → Dense(1, Sigmoid)
- Régularisation : L2(1e-4), ~13k paramètres
- Loss : Binary Crossentropy, Optimizer : Adam

**Fichiers d'entrée** :
- `data/processed/ml_ready/X_supervised.csv`
- `data/processed/ml_ready/y_target.csv`

**Fichiers de sortie** :
- `data/models/mlp/` (modèles sauvegardés)
- `data/results/mlp/` (prédictions et métriques)

---

### [0E_ml_autoencodeur.ipynb](0E_ml_autoencodeur.ipynb)
**Autoencodeur non-supervisé**
- Entraînement autoencodeur (4096 → 32 dim latent)
- Évaluation bottleneck (32 vs 64 dim)
- Extraction espace latent Z
- Validation kNN (k=10) : espace brut vs latent

**Architecture** :
- **Encodeur** : 4096 → Dense(2048) → Dense(1024) → Dense(512) → Bottleneck(32)
- **Décodeur** : Bottleneck(32) → Dense(512) → Dense(1024) → Dense(2048) → Dense(4096, Linear)
- Régularisation : BatchNorm + Dropout(0.2-0.3) + L2(0.001)
- Loss : MSE, Optimizer : Adam(0.001)

**Fichiers d'entrée** :
- `data/processed/ml_ready/X_unsupervised.csv`
- `data/processed/ml_ready/y_target.csv`

**Fichiers de sortie** :
- `data/models/autoencodeur/autoencoder_*.h5` (modèles Keras)
- `data/results/autoencodeur/latent_space_*.csv` (représentations latentes)
- `data/results/autoencodeur/figures/` (visualisations)

## Structure des données

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

## Utilisation

1. **Activer l'environnement** :
```bash
conda activate tcga_tf
```

2. **Lancer Jupyter** :
```bash
jupyter notebook
```

3. **Exécuter les notebooks dans l'ordre** :
   - `0A_data_acquisition.ipynb` → Acquisition des données brutes
   - `0B_qc_normalization.ipynb` → Normalisation et QC
   - `0C_ml_preprocessing.ipynb` → Feature engineering
   - `0D_ml_mlp.ipynb` → Modèle supervisé (optionnel)
   - `0E_ml_autoencodeur.ipynb` → Autoencodeur

4. Les résultats sont exportés automatiquement dans `data/processed/`, `data/models/` et `data/results/`

## Fichiers volumineux

Certains fichiers de données (>100 Mo) ne sont pas versionnés sur GitHub :
- `data/processed/normalized/expr_norm_tcga_ucec.tsv`
- `data/processed/normalized/expr_patient_level_tcga_ucec.tsv`

Ces fichiers sont générés automatiquement par le notebook `0B_qc_normalization.ipynb`.

## Références

- **TCGA-UCEC** : [The Cancer Genome Atlas - Uterine Corpus Endometrial Carcinoma](https://portal.gdc.cancer.gov/projects/TCGA-UCEC)
- **TCGAbiolinks** : Colaprico et al. (2016) - Package R pour l'accès aux données TCGA

---

**Auteur** : Projet M2 AIDA
**Année** : 2025-2026
