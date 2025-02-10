# Address Book
| Section                                         | Subsection(s)                                                                                                                                              |
|-------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [Introduction](#introduction)                   |                                                                                                                                  
| [Features](#features)                           |                                                                                                                                  
| [Pages](#pages)                                 | <ol><li/>[Landing](#landing-page)<li/>[Login](#login-page)<li/>[Signup](#signup-page)<li/>[Address Book](#address-book)<li/>[Admin](#admin-dashboard)<ol/> |
| [Installation & Setup](#installation-and-setup) |
| [Tech stack](#technology-stack)                 |
## Introduction
The Address Book application is designed to help users manage their contacts efficiently. It provides user authentication, contact management features, calendar integration, and an admin dashboard for overseeing user access.

## Features
- **User Authentication:** Signup/Login functionality for secure access
- **Contact Management:** Add, update, and delete contacts
- **Calendar Integration:** Add events linked to contacts
- **User Settings:** Update or delete account
- **Admin Dashboard:** View and manage users and user groups

## Pages
### Landing Page
- First-time users can sign up
- Existing users can log in
- Displays local date, time, temperature, and humidity

### Login Page
- Existing users enter credentials to access the main application

### Signup Page
- New users register and are redirected to the login page

### Address Book
- **Add Contact**: Save new contacts
- **Update Contact**: Edit existing contact details
- **Delete Contact**: Remove unwanted contacts
- **Add Event to Calendar**: Schedule events linked to contacts
- **Settings**: Modify user details or delete account
- **Logout**: Sign out of the application

### Admin Dashboard
- View all users and user groups
- Manage user access permissions

## Installation and Setup
1. **Clone the Repository**  
   ```sh
   git clone https://github.com/AdamPalmerGithub/addressBook 
   cd address-book/myproject
   ```
2. **Run the Application**  
   ```sh
   python manage.py runserver
   ```
3. **Access the App**  
   Open `http://localhost:8000` in your browser

## API Endpoints
Utilising the open-meteo weather API, we give access to weather data, as well as current date and time information to the user. 

## Technology Stack
- **Frontend:** HTML / CSS / JS
- **Backend:** Django 
- **Database:** MySQL 
