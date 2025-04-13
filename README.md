# Amris Web – Gestion de Prospection

## Description
L'application **Amris Web – Gestion de Prospection** est une application de bureau permettant de gérer les informations de prospection pour les clients. Elle permet d'ajouter, de modifier et de rechercher des clients dans une base de données locale au format JSON. L'application prend également en charge l'importation de données depuis des fichiers Excel.

## Fonctionnalités
- **Ajouter un client** : Permet d'ajouter un nouveau client avec des informations telles que le nom, l'activité, le téléphone, le lien, le statut et un commentaire.
- **Modifier un client** : Permet de modifier les informations d'un client existant.
- **Rechercher un client** : Permet de rechercher des clients par leur nom ou leur activité.
- **Importer depuis Excel** : Permet d'importer une liste de clients à partir d'un fichier Excel au format `.xlsx` ou `.xls`.
- **Affichage des clients** : Les clients sont affichés dans une liste avec leurs informations principales.

## Prérequis
- Python 3.6 ou supérieur
- Librairies Python : `customtkinter`, `pandas`

## Installation

1. Clonez ce dépôt ou téléchargez le code source.
2. Installez les dépendances nécessaires :

   ```bash
   pip install customtkinter pandas
   ```
## Fichier Excel attendu
Le fichier Excel doit contenir les colonnes suivantes :

Nom : Nom du client

Activité : Activité du client

Téléphone : Numéro de téléphone du client

Lien : Lien vers le site ou la page du client

Statut : Statut du client (Contacté, À contacter, À relancer)

Commentaire : Commentaire ou note concernant le client

Auteurs
Développé par Iyed A. pour AMRI'S WEB.
