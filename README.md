# FILA1_ArchiD_TP

## Flask, REST, and OpenAPI Lab

**Original Code: Hélène Coullon**

**Authors: Tom Freret, Clément Galiot**

This initial lab aims to implement four services communicating with each other via REST APIs. You can observe a diagram above illustrating the architecture of the various services.

![Services Architecture TP1](./archi1.png 'Codey, the Codecademy mascot')

There are four services:
- The User service is directly and indirectly connected to other services and could be linked to a user interface.
- The Times/Showtime service contains movie scheduling data.
- The Booking service represents user bookings for a specific screening.
- The Movie service acts as the movie database.

### Launching Services:

1. **Build Docker images:**
   ```bash
   docker-compose build
   ```

2. **Launch services:**
   ```bash
   docker-compose up
   ```

_Service addresses will be displayed in logs (as in development mode)_

### Endpoint Testing:

Import the TPx.postman_collection JSON file into Postman to test all endpoints. Make sure to update service addresses in Postman workspace variables accordingly.

## Mixed Lab

This lab involves implementing the same four services using different types of APIs:
- REST
- gRPC
- GraphQL

![Services Architecture TP2](./archi2.png 'Codey, the Codecademy mascot')

Instructions for launching different services remain the same, Docker compose build/up. For testing, utilize the Postman workspace (gRPC can't be tested with an external client like Postman; for more precise testing, a dedicated test client is required. For GraphQL, use the GET /graphql endpoint of the Movie service and utilize sample queries in the ./FILA1_ArchiD_TP2/queries.txt file).
