# Admin Panel Project (Python Flask-based)

This repository contains the source code for an Admin Panel developed using Python Flask. The Admin Panel offers an interface for managing various functionalities within the system.

## Screenshots

<p float="left">
  <img src="https://github.com/prsnt/ELT-Admin-Panel/assets/20899231/86d549ed-1942-420e-9529-71956ebd6b20" alt="Dashboard" width="900"/>
</p>
<p float="left">
  <img src="https://github.com/prsnt/CISWP-APP/assets/20899231/0e133be2-1735-497b-b3eb-6bc59f9925a9" alt="Dashboard" width="900"/>
</p>
<p float="left">
  <img src="https://github.com/prsnt/CISWP-APP/assets/20899231/6a601725-f510-4985-ba65-8c98aa3ec6af" alt="Dashboard" width="900"/>
</p>

## Overview
The Admin Panel allows users to:
- Perform user authentication and authorization.
- Manage various data related to OSH (Occupational Safety and Health) related ELTs (Education and Learning Technologies).
- Categorize, organize, and filter data based on different parameters such as categories, topics, countries, developers, etc.

## Features
- **User Authentication**: Supports user login and registration functionalities.
- **Data Management**: Handles OSH-related ELTs' information.
- **Filtering and Categorization**: Allows filtering and categorization of ELTs based on various parameters.
- **Database Connectivity**: Connects to a MySQL database for data storage and retrieval.
- **Model Views**: Provides Flask Admin ModelViews for efficient CRUD operations on different entities.

## Installation
To run the Admin Panel locally, follow these steps:
1. Clone the repository.
2. Set up a virtual environment (`virtualenv`) and activate it.
3. Install required dependencies using `pip install -r requirements.txt`.
4. Configure the MySQL database connection details in the code.
5. Run the Flask server with `python your_file_name.py`.

## Usage
- Access the Admin Panel via the defined routes (`/admin`, `/login`, `/register`).
- Log in using valid credentials or create a new account to access the panel functionalities.
- Perform CRUD operations on OSH-related ELTs.
- Filter and categorize data based on different attributes.

## Database Setup

The necessary database file for this project, named `elt_demo.sql`, is located in the `/database` directory of this repository. This file contains the required tables and initial data, including user information, to get started with the application.

### Importing the Database

To set up the database:

1. **Locate the Database File**: Find the database file named `elt_demo.sql` inside the `/database` directory.

2. **Import the Database**:
    - If you're using MySQL, you can import the database using the following command:
        ```bash
        mysql -u username -p database_name < path/to/elt_demo.sql
        ```
      Replace `username` with your MySQL username, `database_name` with the name of the database, and `path/to/elt_demo.sql` with the actual path to the SQL file.

    - For other database systems, please refer to their respective documentation on how to import SQL files.

3. **Verify the Import**: Once imported, ensure that the necessary tables and initial data, including user details, have been successfully added to your database.

### Database Configuration

To configure the application to connect to your database, modify the `config.py` or `config.ini` file and update the `SQLALCHEMY_DATABASE_URI` variable or configuration setting to match your database connection details.

---
