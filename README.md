
# Cafe & Wifi Website

A Flask-based web application that lets users browse cafes with Wi-Fi, view details, and even request new cafes or changes. Administrators can add, edit, and delete cafes, while regular users can register, log in, and request updates via email notifications.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)

## Features

- **Browse Cafes:** View a list of cafes along with details such as location, available amenities (sockets, toilets, Wi-Fi), seating capacity, and coffee price.
- **View Details:** Click on a cafe to see additional details and images.
- **Admin Controls:**  
  - **Add Cafe:** Only the admin (user with `id=1`) can add new cafes.
  - **Edit Cafe:** Modify the details of an existing cafe.
  - **Delete Cafe:** Remove a cafe from the listing.
- **Request Cafe:** Users can submit requests for a new cafe or changes to an existing one. These requests are sent via email.
- **User Authentication:**  
  - **Register:** New users can sign up.
  - **Login/Logout:** Secure login with hashed passwords using Flask-Login and Werkzeug.

## Technologies Used

- **Python 3**  
- **Flask** – Web framework for Python.
- **Flask-Login** – User session management.
- **Flask-SQLAlchemy** – ORM for database operations.
- **Flask-WTF** – Form handling and validation.
- **SQLAlchemy** – Database toolkit.
- **Werkzeug** – Provides secure password hashing.
- **python-dotenv** – For loading environment variables.
- **Secrets** – For generating secure tokens.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/mhrafin/Cafe-Wifi-Website.git
   cd Cafe-Wifi-Website
   ```

2. **Set up a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use: venv\Scripts\activate
   ```

3. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**

   The project uses SQLite. When you run the application, it will automatically create the `project.db` file and the necessary tables.

## Configuration

1. **Environment Variables:**

   Create a `.env` file in the project root and add your email credentials. For example:

   ```env
   EMAIL=your-email@example.com
   PASSWORD=your-email-password
   ```

   These credentials are used by the `EmailSender` to send cafe request emails via Gmail's SMTP server.

2. **Secret Key:**

   The app generates a random secret key on startup using the `secrets` module. For production use, you may want to set a fixed secret key in your environment variables.

## Usage

1. **Run the Application:**

   ```bash
   python main.py
   ```

2. **Open in Browser:**

   Visit [http://127.0.0.1:5000](http://127.0.0.1:5000) in your web browser to start using the website.

3. **User Roles:**

   - **Admin:** The first registered user (with `id=1`) has administrative privileges. This user can add, edit, and delete cafes.
   - **Regular User:** Can browse cafes, view details, and submit cafe requests.

4. **Forms and Validation:**

   The app uses Flask-WTF to handle form data. Forms include validations for required fields, URLs, email formats, and more.
