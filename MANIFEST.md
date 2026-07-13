# Manifeste de reproductibilité d'Archimède

1. **Une expérience qui ne peut pas être reproduite automatiquement n'est pas terminée.**
   - Le code, les données, les hyperparamètres et l'environnement sont versionnés et exécutables.

2. **Une comparaison sans baseline solide n'est pas une comparaison.**
   - Toute nouvelle approche est évaluée par rapport à des références pertinentes, sur des protocoles standardisés.

3. **Une simulation sans validation n'est pas une preuve.**
   - Les modèles sont testés non seulement sur des données statiques, mais aussi dans des environnements simulés qui reflètent les incertitudes et les contraintes du monde réel.

4. **Une métrique sans incertitude est incomplète.**
   - Toute évaluation quantitative est accompagnée d'une estimation de l'incertitude (intervalles de confiance, calibration, sharpness).

5. **Un résultat sans artefacts associés est difficilement réutilisable.**
   - Toute publication ou communication s'accompagne du code, des données, des hyperparamètres et des scripts de génération des figures.

6. **Un échec documenté vaut mieux qu'un succès non reproductible.**
   - Les expériences négatives sont conservées et documentées ; elles sont aussi informatives que les succès.

7. **Une infrastructure qui ne peut pas évoluer avec les méthodes n'est pas une infrastructure de recherche.**
   - Les interfaces sont stables ; les implémentations sont évolutives. Les choix technologiques sont justifiés et documentés.
