# Salestrack Server With FastAPI

A prototype of salestrack server made with FastAPI 

## Table of Contents

- [SalesTrack with Fast API Framework](#)
  - [Table of Contents](#table-of-contents)
  - [Demo](#demo)
  - [Features](#features)
  - [Technologies Used](#technologies-used)
  - [API Endpoints](#api-endpoints)
  - [Screenshots](#screenshots)
  - [Installation](#installation)
  - [Usage](#usage)




## API Endpoints



| Endpoint                          | HTTP Method | Path                                      | Description                                             |
|-----------------------------------|-------------|-------------------------------------------|---------------------------------------------------------|
| Register New User                 | POST        | `/user/signup/`                           | Create a new User                                       |
| User Login                        | POST        | `/user/login/`                            | Login  a new user                                       |
| Logout                            | POST        | `/user/logout/`                           | Logout User                                             |
| Change Password                   | POST        | `/user/change-password/`                  | change User password                                    |
| Delete Product by ID              | DELETE      | `/products/{id}/`                         | Delete a specific product by ID                         |
| Category List                     | GET         | `/categories/`                            | Get a list of all categories                            |
| Create Category                   | POST        | `/categories/`                            | Create a new category                                   |
| Retrieve Category by ID           | GET         | `/categories/{id}/`                       | Get details of a specific category by ID                |
| Update Category by ID             | PUT         | `/categories/{id}/`                       | Update details of a specific category by ID             |
| Delete Category by ID             | DELETE      | `/categories/{id}/`                       | Delete a specific category by ID                        |
| User List (Admin Only)            | GET         | `/users/`                                 | Get a list of all users (admin-only)                    |
| Get User By ID (Admin Only)       | GET         | `/users/{user_id}/`                       | Get details of a specific user by ID (admin-only)       | 
| Create User (Admin Only)          | POST        | `/users/`                                 | Create a new user (admin-only)                          |
| Update User By ID (Admin Only)    | PUT         | `/users/{user_id}/`                       | Update details of a specific user by ID (admin-only)    | 
| Delete User By ID (Admin Only)    | DELETE      | `/users/{user_id}/`                       | Delete a specific user by ID (admin-only)               | 
| Get My Account Info               | GET         | `/account/`                               | Get information about the authenticated user            | 
| Edit My Account Info              | PUT         | `/account/`                               | Edit the information of the authenticated user          |
| Remove My Account                 | DELETE      | `/account/`                               | Remove the account of the authenticated user            |
| User Signup                       | POST        | `/auth/signup/`                           | Register a new user                                     |
| User Login                        | POST        | `/auth/login/`                            | Authenticate and generate access tokens for a user      |
| Refresh Access Token              | POST        | `/auth/refresh/`                          | Refresh an access token using a refresh token           | 
| Swagger UI                        | -           | `/docs/`                                  | Swagger UI for API documentation                        |
| Swagger JSON (without UI)         | -           | `/openapi.json`                           | OpenAPI JSON for API documentation without UI           |
| ReDoc UI                          | -           | `/redoc/`                                | ReDoc UI for API documentation                           | 








Poetry - to manage 
fire - for Cli

sqlalchemy - orm to manage database

to run a project
``` poetry run cli salestrack serve
```

psycopg2 - to connect sqlalchemy and postgresql

uvicorn

python --version: 3.12.3

<!-- alembic -- database migration tool to simplify the porcess of managing database changes. -->
pytest => for test cases

pandas => to read data from excel

passlib[bcrypt] ==> to get hashed password
