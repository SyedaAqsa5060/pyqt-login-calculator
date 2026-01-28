PyQt5 Login, Signup & Calculator Application📖 Overview

This project is a desktop-based application built with Python and PyQt5.
It includes a user authentication system (Login & Signup) integrated with a SQL database, and a GUI-based calculator accessible after successful login.

The project demonstrates GUI development, database connectivity, and structured application design.

✨ Features

🔐 User Signup & Login System

🗄️ Database integration using Microsoft SQL Server

🧮 Fully functional GUI Calculator

🎨 Modern UI designed using Qt Designer

🧱 Modular code structure (separate UI & logic)

⚠️ Input validation & error handling

🛠️ Technologies Used

Python

PyQt5

Qt Designer

Microsoft SQL Server

pyodbc

SQL

Object-Oriented Programming (OOP)

📂 Project Structure
├── main.py              # Application entry point
├── login.py             # Login logic
├── sign_Up.py           # Signup logic
├── cal.py               # Calculator logic
├── login.ui             # Login UI (Qt Designer)
├── sign_Up.ui           # Signup UI (Qt Designer)
├── cal.ui               # Calculator UI
├── signup_cal.sql       # Database schema
├── README.md            # Project documentation

🧑‍💻 How It Works

User signs up using the signup form

User credentials are stored in the SQL database

User logs in with valid credentials

After successful login, the calculator window opens

User can perform basic arithmetic operations

🚀 How to Run the Project
1️⃣ Install Required Libraries
pip install pyqt5 pyodbc

2️⃣ Configure Database

Create a database in Microsoft SQL Server

Run signup_cal.sql

Update database credentials in your Python files

3️⃣ Run the Application
python main.py

📚 What I Learned

Building GUI applications using PyQt5

Connecting Python with SQL databases

Managing user authentication systems

Improving UI/UX using Qt Designer

Writing clean and maintainable code

🔮 Future Improvements

Password hashing for better security

Dark / Light theme support

Advanced calculator features

Improved UI animations

👩‍💻 Author

Syeda Aqsa
Data Science Student | Python Developer
