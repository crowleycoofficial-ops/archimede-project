# RFC v0.2 — Projet Archimède

**Titre :** Infrastructure expérimentale reproductible pour les systèmes physiques.

**Version :** 0.2

**Date :** 13 juillet 2026

**Statut :** En discussion.

---

## 1. Constat

Les systèmes physiques critiques — réseaux électriques, chaînes logistiques, procédés industriels, infrastructures énergétiques, systèmes hydriques — deviennent plus complexes plus rapidement que notre capacité à les modéliser, les simuler et les optimiser de manière reproductible.

Cette difficulté se manifeste par plusieurs symptômes :

- **Recherche fragmentée** : chaque équipe développe ses propres pipelines, rendant la comparaison et la réutilisation difficiles.
- **Reproductibilité insuffisante** : le code, les données et les hyperparamètres sont rarement publiés de manière exécutable.
- **Benchmarks hétérogènes** : les protocoles d'évaluation varient, empêchant des comparaisons robustes.
- **Simulation négligée** : l'évaluation se limite souvent à des données statiques, sans test de robustesse ou de généralisation en environnement simulé.
- **Incertitude et explicabilité en second ordre** : alors qu'elles sont déterminantes pour l'adoption industrielle.
- **Transfert lent vers l'industrie** : les modèles sont rarement validés dans des conditions proches du réel.

## 2. Pourquoi un nouveau cadre est nécessaire ?

Les outils existants couvrent partiellement ces besoins, mais aucun ne les intègre de manière cohérente :

- **Frameworks de modélisation** (PyTorch, JAX, scikit-learn) : puissants mais sans reproductibilité native.
- **Gestion d'expériences** (MLflow, Weights & Biases) : suivi des métriques, mais pas d'intégration simulation.
- **Simulation physique** (Grid2Op, PyPSA, OpenDSS, OpenFOAM) : excellents mais spécialisés, aux interfaces hétérogènes.
- **Orchestration de workflows** (Airflow, Prefect) : orientés production, peu adaptés à la recherche.
- **Gestion de données** (DVC, Git LFS) : versionnement des données, mais sans pipeline unifié.
- **Rapports** (Jupyter, R Markdown) : forte variabilité, faible standardisation.

**Archimède se distingue** en intégrant ces briques dans un cadre cohérent, modulaire, orienté vers les systèmes physiques. Il ne s'agit pas d'un outil isolé, mais d'une **infrastructure de recherche** qui permet de concevoir, comparer, simuler et valider des approches de manière reproductible et standardisée.

## 3. Mission

**Construire une infrastructure ouverte, reproductible et modulaire permettant d'accélérer la conception, l'évaluation et le déploiement de méthodes computationnelles pour les systèmes physiques complexes.**

L'objectif est de faire de l'expérimentation computationnelle une science reproductible.

## 4. Principes directeurs

### Vision (long terme)

1. **Reproductibilité native** : chaque expérience doit pouvoir être reproduite automatiquement (code, données, dépendances, hyperparamètres).
2. **Modularité** : chaque composant doit pouvoir être remplacé ou amélioré indépendamment.
3. **Simulation first** : l'évaluation des modèles doit inclure la simulation, pour tester robustesse, généralisation, et comportement en conditions réelles.
4. **Incertitude et explicabilité** : variables intégrées dès la conception.
5. **Ouverture** : code, données et benchmarks ouverts, sauf contraintes légitimes.
6. **Évaluation empirique** : progrès mesurés par des métriques physiques, reproductibles, et publiées.

### Principes d'architecture (mise en œuvre)

- **Composition plutôt que couplage fort.**
- **Interopérabilité avant réécriture.**
- **Interfaces stables, implémentations évolutives.**
- **Formats ouverts privilégiés.**
- **Calcul distribué lorsque pertinent.**
- **Automatisation par défaut.**

## 5. Hypothèses falsifiables

- **H1 :** Une infrastructure reproductible réduit significativement le temps nécessaire pour comparer des approches concurrentes.
- **H2 :** L'intégration native de la simulation améliore la transférabilité des modèles vers des cas réels.
- **H3 :** Une architecture modulaire favorise davantage les contributions externes.
- **H4 :** La standardisation des workflows augmente la réutilisation des résultats par d'autres équipes.

## 6. Critères d'abandon

Le projet sera réévalué si, après 18 mois :

- Aucun benchmark reproductible n'est utilisé par une équipe externe.
- Aucune collaboration n'a émergé.
- L'infrastructure n'apporte pas de gain mesurable par rapport aux outils existants.

## 7. Utilisateurs cibles

| Profil | Besoin | Valeur apportée |
|--------|--------|-----------------|
| Chercheur universitaire | Comparer des approches sur des benchmarks standardisés, publier des résultats reproductibles. | Benchmark reproductible, pipeline standardisé. |
| Doctorant / post-doctorant | Démarrer rapidement. | Infrastructure prête à l'emploi. |
| Laboratoire industriel | Valider des modèles sur des cas proches du réel. | Intégration simulation, robustesse. |
| Gestionnaire d'infrastructure | Évaluer des politiques, simuler des scénarios. | Aide à la décision, boucle simulation-optimisation. |
| Développeur open source | Contribuer sur un module spécifique. | Modularité, interfaces claires. |

## 8. Architecture cible (conceptuelle)
Données
│
▼
Préparation des données
│
▼
Moteur expérimental
│
┌───────────┴───────────┐
▼ ▼
Simulation Optimisation
│ │
└───────────┬───────────┘
▼
Évaluation
│
▼
Rapport reproductible

text

## 9. Niveaux de maturité

| Niveau | Composants | Statut |
|--------|------------|--------|
| A – Fondations | Architecture, données, reproductibilité, CI/CD, documentation. | À développer |
| B – Capacités | Modèles, optimisation, simulation, incertitude. | À développer |
| C – Applications (plugins) | Énergie, matériaux, logistique, eau... | À définir |

## 10. Feuille de route

| Horizon | Jalon | Critère de succès |
|---------|-------|-------------------|
| 6 mois | Première version fonctionnelle sur un jeu de données public (énergie). | Pipeline complet exécutable. |
| 12 mois | Premier benchmark reproductible publié. | Benchmark open source, exécutable, documenté. |
| 18 mois | Première collaboration externe. | Partenariat documenté. |
| 24 mois | Démonstration sur un cas industriel complexe. | Résultats validés par un partenaire. |
| 36 mois | Utilisation par plusieurs équipes externes. | ≥ 5 équipes déclarant l'utiliser. |

## 11. Non-objectifs

- Ne pas développer un nouveau framework de deep learning.
- Ne pas remplacer PyTorch, JAX, ou scikit-learn.
- Ne pas viser une couverture exhaustive de tous les domaines dès le départ.
- Ne pas construire un jumeau numérique universel.
- Ne pas optimiser uniquement les scores sur un benchmark.
- Ne pas reproduire des pipelines spécialisés qui existent déjà.

## 12. Prochaines étapes

1. Recueillir les retours sur cette RFC.
2. Identifier des premiers contributeurs.
3. Développer un prototype minimal sur un cas d'usage restreint (énergie).
4. Itérer vers RFC v1.0 après retour d'expérience.
