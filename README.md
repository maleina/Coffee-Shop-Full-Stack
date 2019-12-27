# Coffee Shop Full Stack Project

## Introduction

This project was created as part of Udacity's Full Stack Developer Nanodegree program in order to practice implementing a full stack web application with API endpoints and authorization using development best practices. 

The project simulates a coffee shop menu application which:

1) Displays graphics representing the ratios of ingredients in each drink.
2) Allows public users to view drink names and graphics.
3) Allows the shop baristas to see the recipe information.
4) Allows the shop managers to create new drinks and edit or delete existing drinks.

The backend code follows PEP8 style guidelines.

## Getting Started

### Pre-requisites and Local Development

This project requires that you install Python 3, node and pip on your development workstation. If you wish to do further development on the project, it is recommended that you set up a virtual environment. Please see specific, additional requirements for both the backend and frontend below. It is recommended that you set up the backend before the frontend.

### Backend

Install dependencies by navigating to the `/backend` directory and typing the following into a command terminal:

```bash
pip install -r requirements.txt
```

#### Database Setup

Initialize the database by uncommenting line 21 of ./backend/src/api.py the first time that you run the code. You should then comment out the line once the application has been run for the first time. See additional instructions in the api.py file.

#### Running the Server

Open a new terminal session and run:

```bash
export FLASK_APP=api.py;
flask run --reload
```

(The `--reload` flag will detect any file changes and restart the server automatically.)

#### Auth0 Configuration

1. Create a new Auth0 Account at auth0.com
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:drinks-detail`
    - `post:drinks`
    - `patch:drinks`
    - `delete:drinks`
6. Create new roles for:
    - Barista
        - can `get:drinks-detail`
    - Manager
        - can perform all actions
7. Update configuration settings (constants) in the auth.py file:
    - The Auth0
    - Domain Name
    - The Auth0 Client ID
8. Likewise, modify ./frontend/src/environment/environment.ts file with the appropriate Auth0 settings.


### Frontend

#### Installing Node and NPM

This project depends upon Nodejs and Node Package Manager (NPM). You must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

#### Installing Ionic Cli

The Ionic Command Line Interface is required to serve and build the frontend. Instructions for installing the CLI  are in the [Ionic Framework Docs](https://ionicframework.com/docs/installation/cli).

#### Installing project dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

#### Configure Environment Variables

Ionic uses a configuration file to manage environment variables. These variables ship with the transpiled software and should not include secrets.

In `./src/environments/environments.ts`, ensure that the variables correspond to the the same system you set up for the backend. See the comments in the code for more details.

#### Running the Frontend in Development Mode

To run the development server, cd into the `frontend` directory and run:

```bash
ionic serve
```

### Testing

Endpoints can be tested using [Postman](https://getpostman.com). 
1. Register 2 users - assign the Barista role to one and Manager role to the other.
2. Sign into each account and make note of the JWT.
3. Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
4. Right-click on the collection folder for barista and manager, navigate to the authorization tab, and update the JWT in the token field (you should have noted these JWTs).
5. Run the collection and correct any errors.

## API Reference 

### Base URL

In its present form, the app can only be run locally. The frontend is hosted locally at http://127.0.0.1:8100/, while the backend can be accessed at http://127.0.0.1:5000/.

### Authentication

To access or change detailed drink information, the application requires authentication using a valid Json Web Token (JWT). For more information, see the Auth0 Configuration section above.

### Error Handling

Errors are returned as JSON objects. The object below is an example of an error returned if the user tries to retrieve a page of questions that does not exist:

```
{
  "error": 404, 
  "message": "resource not found", 
  "success": false
}
```

The API will return the following error types:
- 400: Bad Request
- 401: Unauthorized
- 404: Resource Not Found
- 422: Not Processable

### Resource Endpoint Library

#### GET /drinks

This is a public endpoint that returns a list of all drink items with their "short" form recipe representation, i.e. the ingredient colors and their proportions, but not the ingredient names themselves. Also, it returns a status code of 200 or the appropriate error code indicating the reason for failure.

##### Sample Request

```
curl localhost:5000/drinks
```

##### Sample Response

```
{
    "drinks": [
        {
            "id": 1,
            "recipe": [
                {
                    "color": "grey",
                    "parts": 1
                },
                {
                    "color": "green",
                    "parts": 3
                }
            ],
            "title": "Matcha Shake"
        },
        {
            "id": 2,
            "recipe": [
                {
                    "color": "grey",
                    "parts": 3
                },
                {
                    "color": "brown",
                    "parts": 1
                }
            ],
            "title": "Flat White"
        },
        {
            "id": 3,
            "recipe": [
                {
                    "color": "white",
                    "parts": 1
                },
                {
                    "color": "grey",
                    "parts": 2
                },
                {
                    "color": "brown",
                    "parts": 1
                }
            ],
            "title": "Capuccino"
        }
    ],
    "success": true
}
```

#### GET /drinks-detail

This endpoint returns a list of all drink items with their "long" form recipe representation, i.e. the ingredient names, colors, and their proportions. It requires the 'get:drinks-detail' permission.  It also returns a status code of 200 or the appropriate status code indicating the reason for failure.

##### Sample Request

```
curl --location --request GET 'localhost:5000/drinks-detail' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik1qQkNOMEV5TURkR1JqSXhPRVJFT0RORE9UZzFORGxFTVRBd09USTVOekZCT1RNek1URTFNUSJ9.eyJpc3MiOiJodHRwczovL21jYmNvZmZlZS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWUwMGM3MWM2MDhjMWEwZTc3YjY4NWZjIiwiYXVkIjoiZHJpbmtzIiwiaWF0IjoxNTc3NDU5Mzc0LCJleHAiOjE1Nzc0NjY1NzQsImF6cCI6ImZEbXFlMDBobjdwb3NjV3NTaUZjaElVd1VsbmgxUm9uIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6ZHJpbmtzIiwiZ2V0OmRyaW5rcy1kZXRhaWwiLCJwYXRjaDpkcmlua3MiLCJwb3N0OmRyaW5rcyJdfQ.Jmh9AIQFE5C9b122FkhHYsAynya-m0STHHFINEtc-fFy5NxGq0PmpRCTPEvhs6tO2-hxSoysQBz5zXdPwGUnnkMWLOL0-bviSFWs3S8wAPLDr6_gH0bf7D5Lw-HhWJozeuAOzvl6n0Ey_QYj6_MwVnRn_a6zcN65E_AoC872yDz1rykrMQdli5xcU42OUzkGxMi3b84H4x-oRqKYrbKM6Jdffk24Clf5sRK5V8dpFd_2xouuB3iqHF3l7weROHmhAv1RSYOTXqsN2COtu-qE196QoZWTn9O2xPczvF9P07Q9HczUVtStoZt4jerBGC-yr_olGItHMtlW-QbqUgnBGw'
```

##### Sample Response

```
{
    "drinks": [
        {
            "id": 1,
            "recipe": [
                {
                    "color": "blue",
                    "name": "Water",
                    "parts": 1
                }
            ],
            "title": "Water3"
        }
    ],
    "success": true
}
```

#### POST /drinks

This endpoint creates a new drink, i.e. a new row in the drinks table. It require the 'post:drinks' permission.  It returns an array containing only the newly created drink and a status code of 200 or the appropriate status code indicating the reason for failure.

##### Sample Request

```
curl --location --request POST 'localhost:5000/drinks' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik1qQkNOMEV5TURkR1JqSXhPRVJFT0RORE9UZzFORGxFTVRBd09USTVOekZCT1RNek1URTFNUSJ9.eyJpc3MiOiJodHRwczovL21jYmNvZmZlZS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWUwMGM3MWM2MDhjMWEwZTc3YjY4NWZjIiwiYXVkIjoiZHJpbmtzIiwiaWF0IjoxNTc3NDU5Mzc0LCJleHAiOjE1Nzc0NjY1NzQsImF6cCI6ImZEbXFlMDBobjdwb3NjV3NTaUZjaElVd1VsbmgxUm9uIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6ZHJpbmtzIiwiZ2V0OmRyaW5rcy1kZXRhaWwiLCJwYXRjaDpkcmlua3MiLCJwb3N0OmRyaW5rcyJdfQ.Jmh9AIQFE5C9b122FkhHYsAynya-m0STHHFINEtc-fFy5NxGq0PmpRCTPEvhs6tO2-hxSoysQBz5zXdPwGUnnkMWLOL0-bviSFWs3S8wAPLDr6_gH0bf7D5Lw-HhWJozeuAOzvl6n0Ey_QYj6_MwVnRn_a6zcN65E_AoC872yDz1rykrMQdli5xcU42OUzkGxMi3b84H4x-oRqKYrbKM6Jdffk24Clf5sRK5V8dpFd_2xouuB3iqHF3l7weROHmhAv1RSYOTXqsN2COtu-qE196QoZWTn9O2xPczvF9P07Q9HczUVtStoZt4jerBGC-yr_olGItHMtlW-QbqUgnBGw' \
--data-raw '{
    "title": "Water3",
    "recipe": {
        "name": "Water",
        "color": "blue",
        "parts": 1
    }
}'
```

##### Sample Response

```
{
    "drinks": [
        {
            "id": 1,
            "recipe": [
                {
                    "color": "blue",
                    "name": "Water",
                    "parts": 1
                }
            ],
            "title": "Water3"
        }
    ],
    "success": true
}
```

#### PATCH /drinks/<id>

This endpoint updates an existing drink with the given <id>. It should respond with a 404 error if <id> is not found. It requires the 'patch:drinks' permission.  It returns an array containing only the updated drink information and a status code of 200 or the appropriate status code indicating the reason for failure.

##### Sample Request

```
curl --location --request PATCH 'localhost:5000/drinks/1' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik1qQkNOMEV5TURkR1JqSXhPRVJFT0RORE9UZzFORGxFTVRBd09USTVOekZCT1RNek1URTFNUSJ9.eyJpc3MiOiJodHRwczovL21jYmNvZmZlZS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWUwMGM3MWM2MDhjMWEwZTc3YjY4NWZjIiwiYXVkIjoiZHJpbmtzIiwiaWF0IjoxNTc3NDU5Mzc0LCJleHAiOjE1Nzc0NjY1NzQsImF6cCI6ImZEbXFlMDBobjdwb3NjV3NTaUZjaElVd1VsbmgxUm9uIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6ZHJpbmtzIiwiZ2V0OmRyaW5rcy1kZXRhaWwiLCJwYXRjaDpkcmlua3MiLCJwb3N0OmRyaW5rcyJdfQ.Jmh9AIQFE5C9b122FkhHYsAynya-m0STHHFINEtc-fFy5NxGq0PmpRCTPEvhs6tO2-hxSoysQBz5zXdPwGUnnkMWLOL0-bviSFWs3S8wAPLDr6_gH0bf7D5Lw-HhWJozeuAOzvl6n0Ey_QYj6_MwVnRn_a6zcN65E_AoC872yDz1rykrMQdli5xcU42OUzkGxMi3b84H4x-oRqKYrbKM6Jdffk24Clf5sRK5V8dpFd_2xouuB3iqHF3l7weROHmhAv1RSYOTXqsN2COtu-qE196QoZWTn9O2xPczvF9P07Q9HczUVtStoZt4jerBGC-yr_olGItHMtlW-QbqUgnBGw' \
--data-raw '{
    "title": "Water5"
}'
```

##### Sample Response

```
{
    "drinks": [
        {
            "id": 1,
            "recipe": [
                {
                    "color": "blue",
                    "name": "Water",
                    "parts": 1
                }
            ],
            "title": "Water5"
        }
    ],
    "success": true
}
```


#### DELETE /drinks/<id>

This endpoint deletes an existing drink with the given <id>. It responds with a 404 error if <id> is not found. It requires the 'delete:drinks' permission and it returns the the id of the deleted record, as well as a status code of 200 or the appropriate status code indicating the reason for failure.

##### Sample Request

```
curl --location --request DELETE 'localhost:5000/drinks/1' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik1qQkNOMEV5TURkR1JqSXhPRVJFT0RORE9UZzFORGxFTVRBd09USTVOekZCT1RNek1URTFNUSJ9.eyJpc3MiOiJodHRwczovL21jYmNvZmZlZS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWUwMGM3MWM2MDhjMWEwZTc3YjY4NWZjIiwiYXVkIjoiZHJpbmtzIiwiaWF0IjoxNTc3NDU5Mzc0LCJleHAiOjE1Nzc0NjY1NzQsImF6cCI6ImZEbXFlMDBobjdwb3NjV3NTaUZjaElVd1VsbmgxUm9uIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6ZHJpbmtzIiwiZ2V0OmRyaW5rcy1kZXRhaWwiLCJwYXRjaDpkcmlua3MiLCJwb3N0OmRyaW5rcyJdfQ.Jmh9AIQFE5C9b122FkhHYsAynya-m0STHHFINEtc-fFy5NxGq0PmpRCTPEvhs6tO2-hxSoysQBz5zXdPwGUnnkMWLOL0-bviSFWs3S8wAPLDr6_gH0bf7D5Lw-HhWJozeuAOzvl6n0Ey_QYj6_MwVnRn_a6zcN65E_AoC872yDz1rykrMQdli5xcU42OUzkGxMi3b84H4x-oRqKYrbKM6Jdffk24Clf5sRK5V8dpFd_2xouuB3iqHF3l7weROHmhAv1RSYOTXqsN2COtu-qE196QoZWTn9O2xPczvF9P07Q9HczUVtStoZt4jerBGC-yr_olGItHMtlW-QbqUgnBGw'
```

##### Sample Response

```
{
    "delete": 1,
    "success": true
}
```


## Authors

Maleina Bidek.

Udacity Team. (Some of this readme has been paraphrased from the project instructions and the team also provided the initial starter code.)

## Acknowledgements

Thanks to the entire Udacity Team, especially to our instructor, Gabe, and to my mentor, Sabrina!