# Backend CRUD Operations(REST APIs)

Welcome to our state-of-the-art CRUD (Create, Read, Update, Delete) Application! This README will walk you through the ins and outs of our powerful backend REST APIs designed to provide seamless data management and user interaction.

## Table of Contents

- [About](#about)
- [Features](#features)
- [Why Choose Our APIs?](#why-choose-our-apis)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Usage](#usage)
  - [Running the App](#running-the-app)
  - [Accessing the App](#accessing-the-app)
  - [Performing CRUD Operations](#performing-crud-operations)
  - [API Testing](#api-testing)

## About

A Backend REST APIs project, where seamless user experiences come to life. Discover the power of below features.

## Features


**🚀 Effortless CRUD Operations:** Manage and manipulate your data effortlessly with our intuitive API endpoints.

**🔐 Simplified User Registration:** Streamline user onboarding using our user-friendly registration API.

**🔒 Advanced Token Generation:** Boost your application's security with cutting-edge token authentication.

## Why Choose Our APIs?

✅ Seamless Integration: Effortlessly incorporate our APIs into your application.

✅ Elegant Simplicity: Intuitive design that makes data management a breeze.

✅ Enhanced Security: Fortify your resources with advanced token-based security.

✅ Future-Ready Scalability: Designed to grow with your application's needs.

Get started now and elevate your application's potential!

## Getting Started

### Prerequisites


Thanks to Docker Compose, setting up and running our Django-based CRUD app is a breeze! You don't need to worry about individual prerequisites or installations. Simply follow these steps:

1. Install Docker: If you haven't already, download and install Docker from [docker.com](https://www.docker.com/get-started).

2. Clone the Repository: Clone this repository to your local machine using Git: `git clone https://github.com/Pawan243/DPDzero-assignment`.

3. Start the App: Open a terminal, navigate to the project directory, and run `docker-compose up`. Docker Compose will handle all the setup and configurations for you.

That's it! Docker Compose will take care of everything, including the Python environment, Django, and the database. Once the process is complete, you'll have the app up and running.

**Note**: While we recommend using Docker Compose for the easiest setup, if you prefer to install the components manually, you can follow these installation steps:

### Installation 

**Manual Installation (Optional):-**

1. **Python**: Ensure you have Python installed on your system. You can download Python from [python.org](https://www.python.org/).

2. **Create a Virtual Environment (Optional but Recommended)**: Before installing dependencies, consider creating a virtual environment using `python3.x -m venv venv_name` and activate it using `source venv_name/bin/activate` (Linux/macOS) or `venv_name\Scripts\activate` (Windows).

3. **Django**: Install Django by running the command: `pip install django`.

4. **Database**: Set up a compatible database system (e.g., PostgreSQL, MySQL) and have the necessary credentials ready. Or else you can move on with django's default database SQLite3.

5. **Clone Repository**: Clone this repository to your local machine: `git clone https://github.com/Pawan243/DPDzero-assignment`.

6. **Install Dependencies**: Navigate to the project directory and install the required dependencies: `pip install -r requirements.txt`.

7. **Migrations**: Apply migrations using `python manage.py migrate` to set up the database schema.

7. **Run the App**: Start the Django development server: `python manage.py runserver`.

Remember that Docker Compose simplifies the setup process significantly, making it easy for you to jump right into using our CRUD app without worrying about any prerequisites.

### Configuration

By default, Django utilizes the SQLite3 database. However, if you prefer the power and capabilities of PostgreSQL, follow these steps to make the switch:

1.Navigate to the settings.py file located in the root directory of your project.

2.Locate the database configuration section within the settings.py file.

3.Configure the following PostgreSQL details:

- **Database Name**: Set the name of your database.
- **User**: Provide the username for database access.
- **Password**: Enter the password associated with the user.
- **Host**: Specify the host where the PostgreSQL server resides.
- By making these adjustments, you'll harness the robustness of - **PostgreSQL**, enhancing your project's performance and scalability.







## Usage

Congratulations! You've successfully set up our Django-based CRUD app. Now, let's explore how to use it to manage and interact with your data.

### Running the App

1. **Docker Compose**:
    - Start the app by running:
        ```bash
        docker-compose up
        ```
    - The app will be accessible at [http://0.0.0.0:8000/](http://0.0.0.0:8000/).

2. **Manual Installation**:
    - Start the Django development server by running:
        ```bash
        python manage.py runserver
        ```
    - Access the app at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

### Accessing the App

Open your web browser and navigate to:

[http://127.0.0.1:8000/](http://127.0.0.1:8000/).

You should see the home page of the app.

### Performing CRUD Operations
You can test APIs in two ways:-

**1. Using Python Script:**
Experience the art of CRUD operations with our dynamic Python script, `tests.py`, stationed at the core of your project. This script serves as your testing ally, armed with methods tailored for each CRUD function.

Prepare for testing in two swift steps:

- **Preparation**: Before diving in, equip your environment. Open a new terminal and run:
   ```bash
   pip install requests
- **Execute:**
    ```bash
    python tests.py
    ```

**2.Using Postman:**

**Claim Your Access:-** For authenticated endpoints, such as CRUD operations, you'll need an authentication token. To obtain the token, start by registering a new user using this API first:
  
```bash
POST http://127.0.0.1:8000/api/register/
```
  Provide the following fields in the request body (form-data):
- username
- email
- password
- first_name
- last_name
- age
- gender

**Token Quest:** Once registered, secure your token by sending your credentials to the token API:
```bash
POST http://127.0.0.1:8000/api/token/
```
In the request body (form-data), provide:
- username
- password

Now you're equipped with the token required for authenticated requests.

**Data Alchemy:** When crafting a POST or PUT request, be sure to infuse the necessary data into the request body in JSON format. Consult our API documentation for precise data fields and formats.


## **API Testing**
The moment has come to wield your testing prowess. Fire up Postman and explore these routes:

**CREATE**: POST http://localhost:8000/api/data/ 
 - Fields in body(form-data):- key, value


**READ ALL Records**: GET http://localhost:8000/api/data/
**READ Single record**: GET http://localhost:8000/api/data/{key}/
**UPDATE**: PUT http://localhost:8000/api/data/{key}/ 
 - Fields in body(form-data):- key, value

**DELETE**: DELETE http://localhost:8000/api/data/{key}/

**Note:** Remember to replace {key} with the specific record key and include the authentication token in each API request as well.

That's it. Happy Testing!

