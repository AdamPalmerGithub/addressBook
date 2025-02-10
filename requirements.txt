Introduction:
    -Purpose: Users will be able to login and manage their contacts
    -Project scope: It will have CRUD functionalitiesfor the users and contacts

Overall Description
    -Product Perspective: A brand new product for team02. Interfacing with the user and a database
    -User Classes: All users are expected, down to the tech inept. To be able to store their contacts information.
    -Operating Enviroment: The users will interact with the program requiring an internet connection. 
    -Constraints: Deadline of the 11/02/2025
    -Dependencies: Python, Django, MySQL

Functional Requirements
    -Actor: System
    -Action(verb): Storing login and Contact information
    -Object(noun): internet connection, web browser and server for database.
    -Qualifier: Built in Django auth

Data Requirements
    -Data Model: MySQL
    -Data Dictionary: user id and auth id, also information about contacts(fName, lName, email, pNum, postcode and date added)
    -Data Maintenance: Data is stored in a MySQL database with users as primary keys, When an account is deleted the relating info is deleted

External Requirements
    -User interface: users interact with website, including login and main page with contact
    -Software Interface: requires a web interface, internet connection and Mysql database
    -Communication interface: email for account and an internet connection

Nonfunctional Requirements
    -Performance expectations: should load within 5 seconds on a 4G connection
    -Scalability: support up to 500 users

Reporting Requirements
    -Reports on stored contacts
    -Log of login attempts or failed authentications.
