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


## Screenshots
![image](url)
![image][url]

## Installation
1. **Clone the repository:**
  ```bash
  git clone git@github.com:sharad52/salestrack-server.git
  ```
  OR
  Extract the zip file and open In your IDE(e.g. VS Code/Atom/pycharm)

  Also install Poetry i am using poetry to manage the project here.
2. **Navigate to the project directory**
  ```bash
    salestrack-server
    ```
3. **Create a virtual environment**
  Using pyenv 
  ```bash
  pyenv create virtualenv virtualenv_name python_version(here 3.12.3)
  ```
  or using python
  ```bash
  python -m venv environment_name
  ```

4. **Activate virtual environment**
  ```bash
  pyenv activate virtualenv_name
  ```


5. **Install Dependencies**
 I am using poetry in this project.
 Using poetry
 ```bash
 poetry install
 ```
6. **Nvaigate to the project direcotry and Active Poetry Shell**
  ```bash
  Poetry Shell
  ```
7. **Run the project**
  ```bash
    poetry run cli salestrack serve
    ```
 




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
