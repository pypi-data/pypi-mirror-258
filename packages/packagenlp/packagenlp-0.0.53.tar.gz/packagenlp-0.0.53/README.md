# Package NLP

## Informations

> Initié : Février 2023

> Interlocuteurs : Marine CERCLIER, Grégory GAUTHIER, Tangi LE TALLEC, Alan BIGNON (Business & Décision)

> Dans le cadre des projets interne DataScience

## Description

L'objectif de ce projet est d'avoir un package NLP permettant d'effectuer différentes tâches de traitement du langage naturel de manière simple et configurable.
Vous pouvez y retrouver différents dossiers et eléments dont chacun répond à des objectifs précis :

* dossier packagenlp : Les différents scripts Python nécessaires au fonctionnement du projet sont enregistrés dans ce dossier.
    * dossier data : les différent fichier csv et images nécéssaires au pacakge 
    * dossier ressources : on y retrouve la ressources de Treetager pour l'installation automatique
* dossier .streamlit :
* dossier tests :
* fichier requirements.txt : Il contient les packages présents sur l'environnement de travail du développeur et qui sont donc nécessaires au bon fonctionnement du code.
* fichier LICENSE : Spécifie par quelle license juridique est couvert notre projet.
* fichier README.md : C'est le présent fichier. Il constitue la documentation principale du projet, c'est-à-dire celle qui doit être lue en premier par un utilisateur qui veut comprendre de quoi le projet traite.
* setup.py :
* gitlab_ci.yml :
* main.py :


## Présentation de la Class NLP

La class NLP est conçus pour effectuer diverses opérations de traitement du texte. Les principales caratéristiques de cette sont les suivantes :

* cleanStopWord : Nettoie un texte en retirant les StopWord spécifiés pour une langue donnée (français ou anglais). Prmet l'ajout ou la suppresion des StopWord
* cleanText : Nettoie le texte en retirant les accents, en convertissant le texte en minuscules, et en filtrant les caractères non désirés à l'aide d'une expression régulière. Permet de spécifier des exceptions dans les caractères à supprimer et offre la possibilité de conserver les chiffres.
* lemmatisation : Effectue la lemmatisation du texte en utilisant TreeTagger pour les langues française ou anglaise. Permet de conserver les nombres et d'exclure certains types de mots dans le processus de lemmatisation.


## Utilisation de la class analyse (streamlit)

* La classe analyse que nous avons créée est intégrée dans une application Streamlit, facilitant ainsi l'analyse interactive de données en utilisant des techniques de NLP (Natural Language Processing ou Traitement Automatique du Langage Naturel en français). Voici les étapes principales et les fonctionnalités offertes :

* Chargement du fichier CSV : l'utilisateur peut charger un fichier CSV dans l'application. Les données du fichier sont ensuite stockées et prêtes pour l'analyse.

* Application des fonctions de NLP : une fois le fichier CSV chargé, les différentes fonctions de NLP créées précédemment peuvent être appliquées sur les données textuelles présentes dans le fichier.

* Visualisation des informations : après avoir traité les données avec les fonctions de NLP, l'application permet de visualiser des informations pertinentes sous forme graphique. Cela peut inclure des histogrammes, des nuages de mots, des diagrammes de dispersion, etc., facilitant ainsi l'interprétation des résultats.

* Interactivité et personnalisation : L'utilisateur a la possibilité de personnaliser les analyses en choisissant les paramètres des fonctions de NLP à appliquer, ainsi que les types de visualisations à générer.

Afin de lancé l'application, il suffit après import du package, créer un fichier python (.py) en y rajoutant les lignes suivante :

```
from packagenlp.analyse import ClassAnalyse

if __name__ == "__main__":
    app = ClassAnalyse()
    app.main()
```
Après enregistrement, il suffira d'ouvrir un terminal et ce placer dans l'emplacement de votre fichié et lancé la commande suivante :

`streamlit run "nom_du_fichier.py"`


