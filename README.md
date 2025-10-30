# Scraper de livres – Books to Scrape

## 1. Objectif du projet

Ce projet consiste à développer un scraper Python pour extraire des informations sur des livres depuis le site [Books to Scrape](https://books.toscrape.com/). L’objectif est de récupérer automatiquement les données des livres (titre, prix, note, stock, UPC, catégorie, URL, image) et de les sauvegarder dans des fichiers CSV, tout en téléchargeant les images associées dans des dossiers organisés par catégorie.

Le projet permet également de :

* Gérer la pagination pour récupérer tous les livres d’une catégorie.
* Limiter le nombre de pages scrappées pour des tests rapides.
* Ajouter un délai entre les requêtes pour éviter de surcharger le site.
* Sélectionner une ou plusieurs catégories à scraper via la ligne de commande.
* Organiser les données et images dans des dossiers spécifiques.

---

## 2. Prérequis et installation

### Prérequis

* Python 3.10 ou supérieur
* Connexion internet pour accéder au site cible

### Installation

1. Cloner le dépôt ou copier le projet sur votre machine.
2. Créer un environnement virtuel (recommandé) :

```bash
python -m venv venv
```

3. Activer l’environnement virtuel :

* **Windows** :

```bash
venv\Scripts\activate
```

* **Linux / macOS** :

```bash
source venv/bin/activate
```

4. Installer les dépendances :

```bash
pip install -r requirements.txt
```

> Le fichier `requirements.txt` contient toutes les bibliothèques nécessaires : `requests`, `parsel`, etc.

---

## 3. Structure du projet

```
project/
├── scrape.py          # Script principal pour lancer le scraping
├── parsers.py         # Fonctions pour parser les pages et catégories
├── utils.py           # Fonctions utilitaires (CSV, téléchargement images, dossiers)
├── settings.py        # Paramètres du projet (URL, headers, délais)
├── outputs/
│   ├── csv/           # CSV générés par catégorie
│   └── images/        # Images téléchargées par catégorie
├── README.md          # Documentation du projet
└── requirements.txt   # Dépendances Python
```

---

## 4. Utilisation du scraper

### Commandes de base

* Scraper une seule catégorie :

```bash
python scrape.py --categories Travel
```

* Scraper plusieurs catégories (séparées par une virgule) :

```bash
python scrape.py --categories Travel,Poetry
```

* Limiter le nombre de pages pour tester rapidement :

```bash
python scrape.py --categories Travel --max-pages 1
```

* Ajouter un délai entre les requêtes pour réduire la charge serveur :

```bash
python scrape.py --categories Travel --delay 1
```

* Modifier le dossier de sortie pour les CSV et images :

```bash
python scrape.py --categories Travel --outdir outputs
```

---

### 5. Résultat attendu

Après exécution, le projet génère :

1. **Fichiers CSV** :

```
outputs/csv/category_travel.csv
```

Contenant : Titre, Prix, Note, URL, Image, Stock, UPC, Catégorie

2. **Images téléchargées** :

```
outputs/images/travel/<UPC>_<slug-title>.jpg
```

Exemple de sortie console :

```
🚀 Starting category: Travel
🔎 Scraping page: https://books.toscrape.com/catalogue/category/books/travel_2/index.html
📥 Downloading image: https://books.toscrape.com/catalogue/media/cache/3e/ef/3eef99c9d9f93c8f1a0d0d2b7f1d03c1.jpg -> outputs/images/travel/a897_Its_Only_the_Himalayas.jpg
📸 Image saved: outputs/images/travel/a897_Its_Only_the_Himalayas.jpg
✅ [Travel] Saved: It's Only the Himalayas
💾 Category saved to: outputs/csv/category_travel.csv
```

---

## 6. Notes importantes

* Respectez les délais pour ne pas surcharger le site web.
* Les noms de fichiers sont sécurisés pour éviter les caractères invalides.
* Chaque catégorie possède son propre sous-dossier pour les images et CSV.

---
