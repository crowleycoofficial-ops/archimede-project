# Architecture de référence v0.1 — Projet Archimède

**Version :** 0.1

**Date :** 13 juillet 2026

**Statut :** Proposition technique, évolutive.

---

## Objectif

Ce document décrit l'architecture cible du noyau logiciel d'Archimède (`archimede-core`). Il ne fige pas les choix technologiques à long terme, mais fournit une base pour les premières implémentations.

## Principes d'architecture

- **Composition** : les modules communiquent via des interfaces claires, pas par couplage fort.
- **Interopérabilité** : priorité à l'utilisation et à l'adaptation de bibliothèques existantes plutôt qu'à la réécriture.
- **Évolutivité** : les interfaces restent stables ; les implémentations peuvent changer.
- **Ouverture** : formats de données et de sérialisation ouverts (JSON, HDF5, Parquet, NetCDF).
- **Automatisation** : tout ce qui peut être automatisé (téléchargement, exécution, rapport) l'est par défaut.

## Modules conceptuels

### 1. Ingestion des données
- Chargement de données depuis des sources locales ou distantes.
- Conversion vers un format canonique (ex : `xarray.Dataset`, `pandas.DataFrame`, `networkx.Graph`).
- Versionnement des données (via DVC ou équivalent).

### 2. Préparation des données
- Nettoyage, normalisation, imputation, feature engineering.
- Split entraînement / validation / test, avec graines reproductibles.

### 3. Moteur expérimental
- Définition des pipelines (étapes, modèles, hyperparamètres).
- Orchestration des exécutions (parallélisation, GPU, distribution).
- Suivi des expériences (métriques, hyperparamètres, code, environnement).

### 4. Simulation
- Intégration de simulateurs physiques (Grid2Op, PyPSA, OpenDSS, OpenFOAM, etc.).
- Interface commune pour l'appel, la configuration, et la récupération des résultats.
- Tests de robustesse (sensibilité aux paramètres, bruit, incertitude).

### 5. Optimisation
- Recherche d'hyperparamètres (grid search, bayésienne).
- Optimisation sous contraintes (réseaux, stockage, coût).
- Méta-apprentissage ou transfert si pertinent.

### 6. Évaluation
- Métriques physiques (pertes, coût, résilience, etc.).
- Métriques d'incertitude (calibration, intervalle de confiance).
- Comparaison automatique avec des baselines (publiques ou internes).

### 7. Rapport reproductible
- Génération automatique d'un rapport HTML/PDF.
- Inclus : code, données, hyperparamètres, résultats, figures, métriques, temps d'exécution.
- Téléchargeable et partageable.

## Technologies de référence (évolutives)

| Module | Technologies de référence actuelles |
|--------|--------------------------------------|
| Langage | Python 3.10+ |
| Deep Learning | PyTorch (ou JAX) |
| Données | pandas, xarray, numpy, networkx |
| Simulation | Grid2Op, PyPSA, OpenDSS (via interfaces) |
| Orchestration | Hydra (configuration), DVC (données) |
| Suivi d'expériences | MLflow (ou équivalent) |
| Rapports | Jupyter, nbconvert, ou génération directe HTML/PDF |
| CI/CD | GitHub Actions |

## Interfaces et plugins

Le noyau (`archimede-core`) expose des interfaces pour :

- Ajouter un nouveau domaine (énergie, matériaux, etc.).
- Ajouter un nouveau modèle (ResNet, GNN, transformer, etc.).
- Ajouter un nouveau simulateur.
- Ajouter une nouvelle métrique d'évaluation.

Les plugins sont des dépôts séparés, qui implémentent ces interfaces.

## Prochaines étapes techniques

1. Définir les interfaces minimales des modules (dataclasses, classes abstraites).
2. Implémenter un pipeline de bout en bout sur le cas d'usage de l'énergie (Grid2Op).
3. Ajouter le support de la reproductibilité (versionnement des hyperparamètres, des données, et de l'environnement).
4. Générer un premier rapport reproductible.
5. Itérer sur l'architecture avant d'ajouter des domaines supplémentaires.
