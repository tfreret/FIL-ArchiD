# FILA1_ArchiD_TP

## TP Flask, REST, and OpenAPI

**Code original : Hélène Coullon**

**Auteurs : Tom Freret, Clément Galiot**

Ce TP initial consiste à implémenter quatre services qui communiquent entre eux via des API REST. Vous pouvez observer un diagramme ci-dessus illustrant l'architecture des différents services.

![Architecture des services TP1](./archi1.png 'Codey, la mascotte de Codecademy')

Il y a quatre services :
- Le service User est directement et indirectement connecté aux autres services et pourrait être lié à une interface utilisateur.
- Le service Times/Showtime contient des données de programmation de films.
- Le service Booking représente les réservations d'utilisateurs pour une séance spécifique.
- Le service Movie agit comme base de données de films.

### Lancement des services :

1. **Construisez les images Docker :**
   ```bash
   docker-compose build
   ```

2. **Lancez les services :**
   ```bash
   docker-compose up
   ```

_Les adresses des services seront afficher dans les logs (car en mode développement)_

### Tests des points d'accès :

Importez le fichier JSON TPx.postman_collection dans Postman pour tester tous les points de terminaison. Assurez-vous de mettre à jour les adresses des services dans les variables de l'espace de travail de Postman en conséquence.

## TP Mixte

Ce TP consiste à implémenter les mêmes quatre services en utilisant différents types d'API :
- REST
- gRPC
- GraphQL

![Architecture des services TP2](./archi2.png 'Codey, la mascotte de Codecademy')

Les instructions pour lancer les différents services sont les mêmes, Docker compose build/up. Pour les tests, utilisez l'espace de travail Postman (gRPC ne peut pas être testé avec un client externe tel que Postman ; pour des tests plus précis, un client de test dédié est nécessaire. Pour GraphQL, utilisez le point de terminaison GET /graphql du service Film et utilisez les requêtes d'exemple dans le fichier ./FILA1_ArchiD_TP2/queries.txt)
