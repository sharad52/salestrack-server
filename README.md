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
| Family List                       | GET         | `/sales/family/`                          | Get a list of all families                              |
| Retrieve Family by ID             | GET         | `/sales/family/{id}/`                     | Get details of specifif family by ID                    |
| Create Family                     | POST        | `/sales/family`                           | Create a new Family                                     |
| Update Family by ID               | PATCH       | `/sales/family/{id}/`                     | Update details of a specific family by ID               |
| Retrieve Product by ID            | GET         | `/sales/product/{id}/`                    | Get details of a specific product by ID                 |
| Create Product                    | POST        | `/sales/product/`                         | Create a new Product                                    |
| Update Product By ID              | PATCH       | `/sales/product/{id}/`                    | Update details of a specific product by ID              |
| Load Sales Data from Excel        | POST        | `/sales/load-data/`                       | Load Sales data using excel file                        | 
| Retrieve total sales of last year | GET         | `/sales/last-year/`                       | This endpoint will retrieve total sales of last year    |





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
