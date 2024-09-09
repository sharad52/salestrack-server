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
![image](https://github.com/sharad52/salestrack-server/blob/master/screenshots/change_password.png) 

![image][https://github.com/sharad52/salestrack-server/blob/master/screenshots/create_family.png]

![image][https://github.com/sharad52/salestrack-server/blob/master/screenshots/create_product.png]

![image][https://github.com/sharad52/salestrack-server/blob/master/screenshots/get_family_by_id.png]

![image][https://github.com/sharad52/salestrack-server/blob/master/screenshots/get_product.png]

![image][https://github.com/sharad52/salestrack-server/blob/master/screenshots/get_total_sales_of_last_year.png]

![image][https://github.com/sharad52/salestrack-server/blob/master/screenshots/list_product.png]

![image][https://github.com/sharad52/salestrack-server/blob/master/screenshots/load_data_from_excel.png]

![image][https://github.com/sharad52/salestrack-server/blob/master/screenshots/login.png]

![image][https://github.com/sharad52/salestrack-server/blob/master/screenshots/logout.png]

![image][https://github.com/sharad52/salestrack-server/blob/master/screenshots/signup.png]

![image][https://github.com/sharad52/salestrack-server/blob/master/screenshots/testcase.png]

![image][https://github.com/sharad52/salestrack-server/blob/master/screenshots/update_product.png]

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
8. **To run unit tests**
  ```bash
  pytest -v
  ```

## Technologies Used
- **FastAPI:**
  - FastAPI is a web framework for building HTTP-based service APIs in Python 3.8+. It uses Pydantic and type hints to validate, serialize and deserialize data. FastAPI also automatically generates OpenAPI documentation for APIs built with it.
- **PostgreSQL**
  - A powerful open-source relational database management system used for data storage.
- **SQLAlchemy**
  - An SQL toolkit and Object-Relational Mapping (ORM) library for Python, useful for database interactions.
- **Psycopg2**
  - to connect sqlalchemy and postgresql
- **fire**
  - Python Fire is a library for automatically generating command line interfaces (CLIs) with a single line of code.
- **Poetry**
  - Poetry is a tool for dependency management and packaging in Python.
- **uvicorn**
  - A lightweight ASGI server that serves FastAPI applications. It is used for running FastAPI applications.
- **Python version**
  -3.12.3
- **pytest**
  - Python testing framework to write and test unit testcases.
- **pandas**
  - Used for data manipulation and analysis and retrieve data from excel
- **passlib**
  - A password hashing library for Python
- **PyJWT**
  - A Python library which allows you to encode and decode JSON Web Tokens (JWT). 

## Usage
1. **Mange product and environment**
  - copy env.sample and place as .env in your project and change variables as you wish to use.
2. **Run the FastAPI development Server**
  - ```bash
    poetry run cli salestrack serve
    ```
    The API will be accessible at [http://localhost:8000/]



