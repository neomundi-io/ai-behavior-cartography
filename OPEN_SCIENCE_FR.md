# Cartographie du comportement des IA NeoMundi — Science ouverte et contributions

🌐 **Langue :** [English](./OPEN_SCIENCE.md) · [Français](./OPEN_SCIENCE_FR.md)

📘 **Présentation du programme :** [English README](./README.md) · [README français](./README_FR.md)

📐 **Méthodologie :** [English](./Methodology_EN.md) · [Français](./Methodologie_FR.md)

🧭 **Guides d’utilisation :** [English](./USAGE_EN.md) · [Français](./USAGE_FR.md)

🌍 **NeoMundi :** [Observatoire IA](https://github.com/neomundi-io/neomundi-ai-observatory) · [Baromètre hebdomadaire](https://github.com/neomundi-io/NeoMundi-Weekly-Barometer) · [Site français](https://neomundi.org/) · [English website](https://neomundi.org/en/home)

---

## 1. Des scores de benchmark aux profils observables du comportement des IA

Un classement répond immédiatement à une question :

> Quel système arrive en tête ?

Mais il peut masquer des questions plus importantes :

- Deux juges évaluent-ils la même réponse de la même manière ?
- Les désaccords sont-ils aléatoires ou structurellement concentrés ?
- La stabilité runtime reste-t-elle observable lorsque les jugements factuels divergent ?
- Un même système d’IA présente-t-il différentes signatures comportementales sur des panels répétés ?
- Quelles informations disparaissent lorsque plusieurs dimensions sont compressées dans une note unique ?
- Quelles observations sont robustes et lesquelles restent dépendantes du protocole ?

NeoMundi publie des profils multidimensionnels et désidentifiés du comportement des IA afin de rendre ces questions observables.

L’objectif n’est pas de remplacer un classement par un autre.

L’objectif est d’exposer une cartographie reproductible :

- des évaluations factuelles ;
- de la calibration inter-juges ;
- des signaux comportementaux runtime ;
- des zones de désaccord ;
- de la répétabilité ;
- de la variation sémantique ;
- de la cohérence ;
- des régimes comportementaux ;
- de l’incertitude méthodologique.

> Un signal est une observation qui exige une interprétation, et non un verdict.

---

## 2. Périmètre de la Cartographie publique

La Cartographie du comportement des IA NeoMundi comprend actuellement deux protocoles publics séparés.

### Cartographie jugée — `12 × 790`

```text
12 profils d’IA désidentifiés
× 790 questions TruthfulQA
= 9 480 réponses sources
```

Ce protocole étudie :

- la stabilité observée ;
- la factualité selon un juge fondé sur OpenAI ;
- la factualité selon un juge fondé sur Mistral ;
- l’accord inter-juges ;
- le kappa de Cohen ;
- la direction des désaccords ;
- l’incertitude méthodologique.

### Cartographie runtime — `12 × 3 × 150`

```text
12 profils d’IA désidentifiés
× 3 vagues répétées
× 150 questions équilibrées
= 5 400 exécutions
```

Ce protocole étudie :

- le comportement runtime répété ;
- la stabilité ;
- la variation sémantique ;
- la cohérence ;
- la latence ;
- les régimes comportementaux ;
- la variation entre vagues ;
- la couverture de mesure.

Les deux protocoles sont complémentaires, mais ils ne sont pas fusionnés en un score universel de qualité.

---

## 3. Doctrine de science ouverte

NeoMundi considère la science ouverte comme un engagement à rendre inspectables :

- les méthodes ;
- les hypothèses ;
- les jeux de données publics ;
- les définitions des métriques ;
- les manifestes de release ;
- les empreintes d’intégrité ;
- les limites analytiques ;
- la logique de validation ;
- les frontières d’interprétation ;
- les corrections documentées ;
- les scripts publics lorsque leur publication est compatible avec la sécurité et l’intégrité de la recherche.

La science ouverte n’exige pas la divulgation incontrôlée des éléments opérationnels protégés.

> La science ouverte consiste à rendre inspectables les méthodes, les hypothèses, les preuves publiées, les limites et les artefacts de vérification. Elle n’impose pas la publication incontrôlée des données opérationnelles protégées.

La transparence publique et la protection opérationnelle sont donc considérées comme deux exigences complémentaires.

---

## 4. Corpus source

Le protocole jugé s’appuie sur le benchmark TruthfulQA introduit par Stephanie Lin, Jacob Hilton et Owain Evans.

- [Article original — TruthfulQA: Measuring How Models Mimic Human Falsehoods](https://arxiv.org/abs/2109.07958)
- [Publication ACL Anthology](https://aclanthology.org/2022.acl-long.229/)
- [Dépôt officiel TruthfulQA](https://github.com/sylinrl/TruthfulQA)
- [Fichier public officiel des questions et réponses de référence](https://github.com/sylinrl/TruthfulQA/blob/main/TruthfulQA.csv)

L’article original décrit 817 questions réparties dans 38 catégories.

La Cartographie jugée NeoMundi actuelle utilise le corpus complet de 790 questions retenu par le protocole public actif.

TruthfulQA est utilisé comme instrument d’évaluation factuelle. Les résultats qui en sont issus ne doivent pas être interprétés comme des affirmations universelles pour tous les domaines, langues, tâches ou contextes de déploiement.

---

## 5. Releases publiques

Le dépôt contient actuellement les répertoires publics suivants :

- [Cartographie du comportement — juillet 2026](./releases/july2026-behavior-cartography/)
- [Cartographie du comportement — juin 2026 v1.0.0](./releases/june2026-behavior-cartography-v1.0.0/)
- [Profils TruthfulQA v1.0.0](./releases/truthfulqa-profiles-v1.0.0/)

Le programme de juillet 2026 sépare :

- le protocole jugé `12 × 790` ;
- le protocole runtime `12 × 3 × 150`.

Chaque release possède ses propres :

- périmètre de protocole ;
- référence méthodologique ;
- inventaire de données ;
- limites ;
- manifeste ;
- informations d’intégrité ;
- limites de reproductibilité.

Les releases historiques font partie du registre public et ne doivent pas être réécrites silencieusement.

---

## 6. Preuves publiques

Selon la release, NeoMundi peut publier :

- des résultats agrégés par profil désidentifié ;
- des résultats agrégés par question ou famille de questions ;
- des mesures de stabilité ;
- les résultats de factualité de juges séparés ;
- l’accord inter-juges ;
- le kappa de Cohen ;
- des indicateurs de variation sémantique ;
- des indicateurs de cohérence ;
- des synthèses de latence ;
- des distributions de régimes comportementaux ;
- des comparaisons entre vagues ;
- des informations de couverture et de complétude ;
- des dictionnaires publics de données ;
- des contrats de métriques ;
- des rapports analytiques ;
- des cartographies visuelles ;
- des manifestes de release ;
- des empreintes SHA-256 ;
- des limites méthodologiques.

Ces artefacts visent à permettre :

- des contrôles de cohérence interne ;
- une revue indépendante ;
- la critique méthodologique ;
- la reproductibilité dans des limites documentées ;
- la comparaison entre releases compatibles ;
- la discussion publique du comportement observé des IA.

---

## 7. Matériel de recherche protégé

Le dépôt public ne représente pas l’intégralité du registre de mesure NeoMundi.

Selon le protocole, les éléments protégés peuvent inclure :

- l’identité des fournisseurs et des modèles ;
- le registre privé de correspondance des profils ;
- les réponses brutes complètes ;
- les prompts complets lorsque leur divulgation compromettrait le protocole ;
- les identifiants de requête ;
- les identifiants de trace ;
- les payloads API bruts ;
- les horodatages précis des exécutions ;
- les clés API ;
- les identifiants d’infrastructure ;
- les paramètres privés des juges ;
- les données détaillées et non agrégées de tokens et de coûts ;
- les exports de campagne non publiés ;
- les diagnostics internes ;
- les éléments de débogage ;
- les notes internes de revue ;
- la logique de calcul propriétaire ;
- les artefacts pouvant permettre la réidentification des profils ;
- les signaux expérimentaux non encore qualifiés pour publication.

Cette séparation protège :

- la confidentialité ;
- la continuité opérationnelle ;
- l’intégrité de la recherche ;
- la désidentification ;
- la sécurité ;
- la comparabilité longitudinale future.

Les releases publiques sont **désidentifiées**. Elles ne sont pas présentées comme irréversiblement anonymes.

---

## 8. Signaux méthodologiques actuels

La release jugée gelée documente :

```text
12 profils désidentifiés
9 480 réponses sources
9 087 paires de jugements comparables
81,42 % d’accord inter-juges observé
kappa de Cohen agrégé = 0,6342
1 688 désaccords
```

Parmi les désaccords :

```text
Juge A négatif / juge B positif : 1 491
Juge A positif / juge B négatif :   197
```

Cette asymétrie directionnelle ne permet pas de désigner un juge de référence absolu.

Elle montre que l’évaluation factuelle doit elle-même être traitée comme une couche calibrée, traçable et observable.

Le protocole runtime `12 × 3 × 150` documente séparément des propriétés comportementales répétées et ne doit pas être réduit aux résultats de factualité jugée.

---

## 9. Pourquoi cela compte

Une décision de sélection ou de déploiement d’un modèle ne peut pas reposer de manière responsable sur une note publique unique.

Un diagnostic sérieux peut nécessiter de séparer :

- l’évaluation factuelle ;
- la calibration des juges ;
- la stabilité runtime ;
- la variation sémantique ;
- la répétabilité ;
- la cohérence ;
- la latence ;
- les risques propres au domaine ;
- le contexte de déploiement ;
- les contraintes de coût et d’efficience ;
- les exigences de gouvernance.

La Cartographie publique expose volontairement des dimensions observables plutôt que des recommandations universelles.

---

## 10. Questions ouvertes

Les questions suivantes restent ouvertes :

1. L’asymétrie inter-juges persiste-t-elle avec un troisième juge indépendant ?
2. Quelles zones de désaccord restent stables entre plusieurs répétitions du jugement ?
3. Quelle est la variabilité intra-juge dans des conditions contrôlées ?
4. Quelles questions à forte divergence nécessitent une adjudication humaine ?
5. Les signatures comportementales runtime restent-elles stables entre des panels mensuels répétés ?
6. Des panels réduits peuvent-ils préserver le signal de corpus comportementaux plus larges ?
7. Quelles dimensions runtime deviennent plus informatives dans des contextes juridiques, médicaux, financiers ou agentiques ?
8. Comment représenter des profils multidimensionnels sans recréer implicitement un classement ?
9. Quelles modifications de protocole préservent la comparabilité longitudinale ?
10. Quels artefacts publics fournissent les preuves les plus fortes sans compromettre la désidentification ?

---

## 11. Extensions prévues

Les prochains travaux publics peuvent inclure :

- un troisième juge indépendant ;
- une analyse de répétabilité intra-juge ;
- un panel stratifié d’adjudication humaine ;
- des cartographies supplémentaires en vagues répétées ;
- des panels sectoriels ;
- des corpus multilingues ;
- des protocoles adversariaux ;
- des réplications indépendantes ;
- des analyses proposées par des contributeurs ;
- des signaux runtime supplémentaires ;
- des comparaisons longitudinales mensuelles.

Chaque extension doit documenter son protocole, ses limites et sa compatibilité avec les releases antérieures.

---

## 12. Invitation à contribuer

Chercheurs, ingénieurs, auditeurs, statisticiens, experts métier, traducteurs et concepteurs d’IA sont invités à contribuer.

Les contributions peuvent porter sur :

- la revue méthodologique ;
- les tests de reproductibilité ;
- de nouveaux panels publics ;
- des expérimentations avec un troisième juge ;
- les protocoles d’adjudication humaine ;
- l’analyse statistique ;
- la visualisation des données ;
- les cas d’usage juridiques, médicaux, financiers ou agentiques ;
- les jeux de données multilingues ;
- l’amélioration de la documentation ;
- l’analyse d’interopérabilité ;
- la revue critique des limites d’interprétation.

### Proposer une contribution

- [Formulaire de contribution — Français](https://neomundi.org/proposez-une-contribution)
- [Submit a contribution — English](https://neomundi.org/en/submit-a-contribution)
- [Cadre de contribution et de gouvernance NeoMundi](https://github.com/neomundi-io/neomundi-ai-observatory/tree/main/governance)

Les contributeurs doivent :

- expliciter l’hypothèse ;
- documenter le corpus ;
- documenter le protocole ;
- versionner les scripts ;
- exposer les limites ;
- séparer les preuves de l’interprétation ;
- éviter les affirmations universelles insuffisamment étayées ;
- respecter les frontières des données protégées ;
- préserver l’attribution.

Les contributions ne créent aucune autorité sur le programme, les systèmes observés ou les décisions institutionnelles de NeoMundi, sauf accord écrit explicite.

---

## 13. Principe de contribution

> Contribuer des preuves, des méthodes et une revue critique — pas du bruit.
>
> La science ouverte exige de rendre explicites ce qui est publié, ce qui reste protégé et pourquoi.

---

## 14. Contact

Pour proposer une collaboration ou demander des informations complémentaires :

- **Site :** [neomundi.org](https://neomundi.org/)
- **Formulaire de contribution :** [Proposer une contribution](https://neomundi.org/proposez-une-contribution)
- **Email :** [contact@neomundi.org](mailto:contact@neomundi.org)
