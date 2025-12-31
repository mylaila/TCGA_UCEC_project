Analyse transcriptomique TCGA-UCEC

Projet M2 AIDA – Analyse et modélisation par Deep Learning des données du cancer de l'endomètre

(Uterine Corpus Endometrial Carcinoma, TCGA-UCEC)

Repository : https://github.com/mylaila/TCGA_UCEC_project

> Vue d'ensemble

Ce projet explore les profils transcriptomiques RNA-seq de la cohorte TCGA-UCEC afin de prédire des caractéristiques cliniques et d'identifier des signatures moléculaires via des approches supervisées (MLP) et non supervisées (Autoencodeurs).

Conformément aux exigences académiques, le pipeline a été conçu pour être totalement reproductible, repartant des données brutes du Genomic Data Commons (GDC) jusqu'à l'interprétation biologique finale.

📂 Structure du Projet

TCGA_UCEC_project/
├── 0A_data_acquisition.ipynb          # Acquisition GDC via R (TCGAbiolinks)
├── 0B_qc_normalization.ipynb          # QC gènes et Normalisation Log-CPM
├── 01_loading_sanity_check.ipynb      # Vérification de l'intégrité des données
├── 02_sample_harmonization.ipynb      # Alignement échantillons/clinique
├── 03_gene_qc_normalization.ipynb     # (Optionnel) Analyses complémentaires
├── 04A_patient_level_expression.ipynb # Agrégation au niveau patient
├── 05_labels_and_baseline_mlp.ipynb   # Modélisation supervisée (Baseline)
├── 06_autoencoder.ipynb               # Apprentissage de représentation (Espace Z)
├── data/
│   ├── raw/                           # Données brutes (STAR Counts .gz)
│   └── processed/                     # Datasets normalisés et labels
├── scripts/
│   └── Script_data_download.R         # Script moteur d'acquisition R
└── README.md                          # Documentation du projet

> Pipeline de traitement

Le projet est subdivisé en pipelines numérotés à exécuter séquentiellement :

1. Acquisition et Préparation (Amont)

0A - Acquisition : Utilise l'interopérabilité R-Python pour télécharger les counts STAR et les métadonnées cliniques depuis le GDC.

0B - QC & Normalisation :

Mapping ENSG vers Gene Symbols.

Filtrage des gènes (seuil : >10 counts dans au moins 20% des échantillons).

Normalisation par taille de bibliothèque (CPM) et transformation Log2.

2. Exploration et Harmonisation

01 & 02 : Sanity checks et alignement des identifiants patients pour garantir la cohérence entre l'expression génique et les phénotypes cliniques.

Ce découpage permet de distinguer la validation technique de la lecture des fichiers (01) de la résolution de l'alignement complexe des barcodes patients (02), assurant une base de données parfaitement intègre.

3. Modélisation et Deep Learning

04A & 05 : Préparation des données au niveau patient et entraînement d'un Multi-Layer Perceptron (MLP) pour la classification.

La séparation isole l'étape d'agrégation statistique au niveau patient (04A) de l'implémentation et de l'optimisation du modèle prédictif (05), facilitant les tests itératifs sur l'architecture du réseau.

06 - Autoencodeur : Réduction de dimension non supervisée pour explorer la structure latente (Espace $Z$) des profils tumoraux.

> Configuration technique

Environnement Conda

Le projet utilise l'environnement tcga_tf.

# Création et activation
conda create -n tcga_tf python=3.10 -y
conda activate tcga_tf

# Installation des dépendances
pip install pandas numpy matplotlib seaborn scikit-learn tensorflow

> Gestion des données massives

Pour optimiser l'espace disque, toutes les matrices d'expression sont stockées et lues directement au format compressé .gz via les fonctions natives de Pandas. Cette approche permet de gérer des fichiers volumineux sans décompression intermédiaire sur le disque.

Interopérabilité R

L'étape 0A nécessite une installation de R fonctionnelle et accessible via la commande Rscript.

# Vérifier l'installation de R
Rscript --version

# Installation manuelle des dépendances R (Optionnel)
# Note : Le script d'acquisition 0A tente de les installer automatiquement au premier lancement.
# Si besoin, lancez R (via RStudio ou votre terminal) et exécutez ces commandes :
Rscript -e "install.packages('BiocManager'); BiocManager::install(c('TCGAbiolinks', 'SummarizedExperiment', 'dplyr', 'readr'))"

# Exécution du script d'acquisition (géré par le notebook 0A)
Rscript scripts/Script_data_download.R

# Configuration du chemin dans le Notebook 0A
S'assurer que la variable R_EXECUTABLE pointe vers l'installation locale :
Exemple: R_EXECUTABLE = r"C:\Program Files\R\R-4.5.2\bin\x64\Rscript.exe"

> Auteurs

Klervi LE DORTZ
Quentin MARANDON
Laïla EL BOUHALI

Master 2 AIDA - Sorbonne Université (2025-2026)