# Projet Archimède

**Accélérer la conception, l'évaluation et le déploiement de méthodes computationnelles pour les systèmes physiques complexes.**

Archimède est une infrastructure ouverte, reproductible et modulaire. Il ne développe pas de nouveaux algorithmes par défaut ; il accélère leur évaluation, leur comparaison et leur transfert vers des cas réels.

**Devise :** *Commencer par les premiers principes, mesurer systématiquement, construire de manière reproductible.*

---

## Pourquoi Archimède ?

Les systèmes physiques critiques (réseaux électriques, chaînes logistiques, procédés industriels, infrastructures énergétiques, systèmes hydriques) deviennent plus complexes plus rapidement que notre capacité à les modéliser, les simuler et les optimiser de manière reproductible.

La recherche progresse par silos, la reproductibilité est insuffisante, les benchmarks sont hétérogènes, et l'incertitude est trop souvent négligée.

Archimède fournit un cadre méthodologique et logiciel pour :
- Standardiser les pipelines d'expérimentation.
- Intégrer la simulation dès la conception.
- Garantir la reproductibilité native (code, données, hyperparamètres).
- Comparer systématiquement les approches sur des benchmarks communs.

---

## Principes fondamentaux

1. **Reproductibilité native** : une expérience qui ne peut pas être reproduite automatiquement n'est pas terminée.
2. **Modularité** : chaque composant (données, modèles, simulateurs, optimisation, rapport) est interchangeable.
3. **Simulation first** : l'évaluation ne s'arrête pas aux données statiques ; elle inclut la simulation pour tester robustesse et généralisation.
4. **Incertitude et explicabilité** : variables de premier ordre, évaluées systématiquement.
5. **Ouverture** : code, données et benchmarks sont ouverts, sauf contraintes légitimes (données sensibles, sécurité).

Voir le [Manifeste complet](MANIFEST.md).

---

## Structure du projet

- [`docs/rfc/v0.2.md`](docs/rfc/v0.2.md) : Request for Comments — vision, principes, hypothèses, feuille de route.
- [`docs/architecture/reference-v0.1.md`](docs/architecture/reference-v0.1.md) : Architecture de référence, modules, technologies, interfaces.
- [`MANIFEST.md`](MANIFEST.md) : Manifeste de reproductibilité.

---

## Prochaines étapes

1. **Démonstration "One Command"** : un prototype qui, en une commande, clone, télécharge des données, exécute plusieurs approches (baseline, ResNet, GNN) sur un cas d'usage d'optimisation de réseau électrique, simule, et génère un rapport reproductible.
2. **Première collaboration** : identifier un laboratoire académique ou un industriel intéressé par une validation sur un cas réel.
3. **Extension** : passer de l'énergie aux matériaux, à la logistique, à l'eau.

---

## Contribuer

Voir [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Licence

Ce projet est licencié sous la licence Apache License 2.0 — voir le fichier `LICENSE` pour le texte complet.
