# FILA1_ArchiD_TP


### TP Flask, REST, and OpenAPI

**Original code: Hélène Coullon**

**Authors: Tom Freret, Clément Galiot**

This initial TP involves implementing four services that communicate with each other through REST APIs. You can observe a diagram above illustrating the architecture of the different services.

[![Services Architecture TP1](./archi1.png 'Codey the Codecademy mascot')]

There are four services: 
- The User service is directly and indirectly connected to the other services and could be linked to a user interface.
- The Times/Showtime service contains movie scheduling data.
- The Booking service represents user reservations for a specific showtime.
- The Movie service acts as the movie database.

#### To launch the various services:

1. Build the Docker images:
   ```
   docker-compose build
   ```

2. Start the services:
   ```
   docker-compose up
   ```

_Adresses of the service will be log (because in development mode)_

#### To test the different access points:

Import the TPx.postman_collection JSON file into Postman to test all endpoints. Please ensure to update the service addresses in the Postman workspace variables accordingly.

### TP Mixte

This TP involves implementing the same four services using different types of APIs:
- gRPC
- GraphQL

[![Services Architecture TP2](./archi2.png 'Codey the Codecademy mascot')]

The instructions to launch the different services are the same, Docker compose build/up. For testing, use the Postman workspace (gRPC cannot be tested using an external client like Postman; for more precise method testing, a dedicated test client is required. For GraphQL, use the GET /graphql endpoint of the Movie service and utilize the example queries in the ./FILA1_ArchiD_TP2/queries.txt file)
