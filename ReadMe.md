### 1. Introduction

  

Le projet consiste à scraper des données sur le web en utilisant un projet Scrapy, puis à les sauvegarder dans une base de données MongoDB. L'ensemble du projet est exécuté dans un environnement Docker à l'aide d'un fichier docker-compose. Par la suite, les données sont récupérées de la base de données depuis pour être affichées sur un site web le tout en utilisant Flask. Nous avons choisi de scraper les données d'un site de vente de protéines alimentaires (Whey). Ce document fournira un aperçu détaillé de l'architecture, de l'installation, de la configuration, et des différentes étapes du processus.

  
  

### 2. Architecture système

  

L'architecture du système est conçue pour permettre le scraping de données web, leur stockage dans une base de données MongoDB via Docker, et leur affichage ultérieur via Flask. Voici une description de l'architecture avec les points d'entrée et de sortie des données :

  

![Architecture du système](lien_vers_l'image)

  

#### Composantes :

1. **Scrapy Project** :

- Contient les scripts de scraping pour extraire les données du site web de vente de protéines alimentaires (Whey).

- À la racine du projet, on trouve un fichier docker-compose et un Dockerfile pour la configuration des conteneurs.

  

2. **Docker** :

- Utilisé pour la conteneurisation de l'ensemble du projet.

- Le fichier docker-compose définit les services et leurs configurations, notamment les conteneurs pour Scrapy et MongoDB.

  

3. **Scrapy Container** :

- Responsable du scraping des données à partir du site web.

- Lancé à l'aide de la commande `docker-compose up`, ce conteneur récupère les données, les traite et les stocke dans la base de données MongoDB.

  

4. **MongoDB Container** :

- Conteneur Docker hébergeant la base de données MongoDB.

- Les données scrappées sont stockées dans cette base de données.

  

5. **Flask Container** :

- Utilisé pour l'affichage des données.

- Une fois les données scrappées et stockées dans MongoDB, elles sont récupérées dans la base de données par l’application Flask.

- Flask est ensuite utilisé pour créer un site web où les données sont affichées.

  

#### Interaction :

1. La commande ‘docker-compose’ build est utilisée pour construire les images des services définis.

2. L'utilisateur lance le projet en exécutant la commande `docker-compose up` à la racine du projet Scrapy.

3. Docker déploie les conteneurs Scrapy et MongoDB.

4. Le conteneur Scrapy scrappe les données à partir du site web et les stocke dans la base de données MongoDB.

5. Une fois le scraping terminé, le conteneur Scrapy se ferme.

6. L’application Flask se lance , récupérant les données et les affichant sur une page web visible sur ‘http://localhost:5000/’.

  

### 4. Scraping des données

  

Le scraping des données est réalisé à l'aide du framework Scrapy et de la bibliothèque Beautiful Soup pour l'analyse HTML. Voici un aperçu du processus :

  

- **Outils utilisés** :

- Scrapy : Pour le scraping des données à partir des pages web spécifiées.

- Beautiful Soup : Pour l'analyse HTML et l'extraction des données spécifiques.

  

- **Exemples de sources de données** :

- Pages de différents produits de protéines alimentaires de MyProtein, comme Impact Whey Protein, Impact Whey Isolate, etc.

  

- **Méthode de scraping** :

- Pour chaque URL spécifiée dans la liste `start_urls`, le Spider Scrapy `MyProteinSpider` est invoqué.

- Les données scrappées comprennent :

- Prix, noms des produits, données de la table nutritionnelle, nombre de variantes de poids, nombre d'arômes disponibles, évaluations des produits, etc.

- Les données sont structurées et stockées dans une base de données MongoDB.

  

Ce processus itératif permet de récupérer les données nécessaires à partir des pages web spécifiées et de les organiser pour une utilisation ultérieure dans le projet.

  
  

### 5. Stockage dans MongoDB

  

#### Structure de la base de données MongoDB :

- **Collections** :

- Chaque collection représente une protéines spécifique de la manière suivante:

{"_id":{"$oid":"65c516a65771f20d15f1fb52"},"product_name":"Clear Whey Isolate","product_price":"27,99 €","size":"20 servings","weight_count":1,"arome_count":3,"table_data":{"Nutrient":["Energie","Lipides","dont saturés","Glucides","dont sucre","Protéines","Sel"],"Per 100g":["1397 kJ/334 kcal","0,5 g","0,2 g","2,7 g","1,0 g","80 g","0,1 g"],"Per Portion":["349 kJ/83 kcal","0,1 g","0,1 g","0,7 g","0,2 g","20 g","0,0 g"]},"product_grade":["4.38"],”image_src”: ‘lien_vers_l’imagesource’}

  

#### Transfert des données dans la base de données :

- Une fois les données scrappées extraites et traitées dans le Spider Scrapy, elles sont converties en un tuple ou un dictionnaire structuré.

- Ces données sont ensuite insérées dans la base de données MongoDB à l'aide de la bibliothèque pymongo.

  

### 6. Conteneurisation avec Docker

  

Le projet est conteneurisé avec Docker pour simplifier son déploiement et sa gestion. Voici un aperçu de la configuration des conteneurs pour MongoDB, Scrapy et Flask :

  

#### Configuration des conteneurs Docker pour MongoDB :

- **Image** : MongoDB

- **Nom du conteneur** : mongodb

- **Ports exposés** : 27017

- **Redémarrage automatique** : Toujours (restart: always)

  

#### Configuration des conteneurs Docker pour Scrapy :

- **Image de base** : Python 3.8

- **Installation des dépendances** : Selenium et Google Chrome

- **Copie des fichiers du projet** dans le conteneur

- **Commande d'exécution du Spider Scrapy** : `scrapy crawl myprotein`

  

#### Configuration des conteneurs Docker pour Flask :

- **Image de base** : Construite à partir du répertoire `./app` (Dockerfile nécessaire dans ce répertoire)

- **Ports exposés** : 5000

- **Dépendances** : Dépend de MongoDB (déclaré avec `depends_on`)

- **Commande d'exécution** : Le conteneur Flask doit être configuré pour démarrer l'application Flask sur le port 5000.

  

Le fichier Docker-compose fourni définit la configuration pour les services MongoDB, Scrapy et Flask. Le service MongoDB utilise l'image Docker officielle de MongoDB et expose le port 27017. Le service Scrapy utilise le Dockerfile actuel (dans le répertoire courant) pour construire l'image et démarre le Spider Scrapy après avoir vérifié que le service MongoDB est disponible. Le service Flask construit son image à partir du répertoire `./app` et expose l'application sur le port 5000, en dépendant également du service MongoDB pour assurer la disponibilité de la base de données lors du démarrage.

  
  

### 7. Déploiement et exécution

  

Pour déployer et exécuter le projet, suivez ces étapes simples :

  

1. Assurez-vous d'être dans le fichier test2 du projet où se trouve le fichier `docker-compose.yml`.

  

2. Tout d'abord, exécutez la commande suivante pour construire les images des services définis dans le fichier `docker-compose.yml` :

```bash

docker-compose build

```

Cette commande construira les images Docker nécessaires à partir des Dockerfiles et des configurations définies.

  

3. Ensuite, lancez les conteneurs à l'aide de la commande suivante :

```bash

docker-compose up

```

Cette commande démarrera les conteneurs Docker pour tous les services définis dans le fichier `docker-compose.yml`. Les conteneurs seront exécutés en arrière-plan.

  

4. Après le démarrage réussi des conteneurs, vous pouvez accéder à l'application Flask en ouvrant votre navigateur Web et en accédant à l'adresse suivante :

```

http://localhost:5000

```

Assurez-vous que le service Flask est exposé sur le port 5000 comme défini dans le fichier `docker-compose.yml`.

  
  

En suivant ces étapes, vous pourrez facilement déployer et exécuter votre projet Dockerisé.

  
  

### 8. Affichage des données avec Flask

  

#### Récupération des données depuis MongoDB via Flask :

  

Les données scrappées et stockées dans la base de données MongoDB sont récupérées de manière dynamique grâce à l'utilisation de Flask. Ce framework python agit comme une interface entre la base de données et le navigateur, permettant d'afficher les informations sur une interface web.

  

Pour récupérer les données depuis MongoDB, on utilise la bibliothèque pymongo pour établir une connexion à la base de données. Une fois connecté, Flask peut interroger la base de données et récupérer les documents nécessaires pour les afficher sur les pages web.

  

Voici un exemple de code pour la récupération des données dans l'application Flask :

  

```python

from flask import Flask, render_template

from pymongo import MongoClient

from bson import ObjectId

  

app = Flask(__name__)

  

# Configuration de la connexion à MongoDB

client = MongoClient('mongodb://localhost:27017/')

db = client['myprotein_database']

collection = db['products']

  

# Route pour la page d'accueil

@app.route('/')

def home():

products = collection.find()

return render_template('index.html', products=products)

  

# Route pour une page de produit individuelle

@app.route('/product/<product_id>')

def product(product_id):

product = collection.find_one({'_id': ObjectId(product_id)}) # Récupérer un produit spécifique par son ID

return render_template('product.html', product=product)

  
  

if __name__ == "__main__":

app.run(debug=True)

```

  

#### Routes Flask pour l'affichage des données :

  

Les routes définies dans l'application Flask déterminent les différents points d'accès auxquels les utilisateurs peuvent accéder afin de visualiser les données. Dans cet exemple, deux routes principales sont définies :

  

1. **Route pour la page d'accueil (`/`) :**

- Cette route récupère tous les produits depuis la base de données et les transmet au template HTML pour affichage.

- Les données sont affichées sous forme de liste, avec des liens vers des pages individuelles de chaque produit.

  

2. **Route pour une page de produit individuelle (`/product/<product_name>`) :**

- Cette route prend un identifiant de produit en tant que paramètre.

- Elle utilise cet identifiant pour récupérer les détails spécifiques du produit depuis la base de données.

- Les détails du produit sont ensuite affichés sur la page web.
