# Mudi Dokan Management System - Beginner Friendly Flask Project

This is a very beginner-friendly grocery shop management project using:

- Flask
- SQLAlchemy
- SQLite database
- HTML
- CSS
- JavaScript

## Project Features

1. View all products
2. Search product by name
3. Search product by category
4. Add new product
5. Sell product
6. Automatically reduce stock after sale
7. Restock product
8. View sales history
9. Calculate total sales and profit
10. Show low stock alert
11. Delete product
12. Delete sale and restore stock

## Folder Structure

```text
mudi_dokan_management_system/
│
├── app.py
├── requirements.txt
├── README.md
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── add_product.html
│   ├── sell.html
│   ├── restock.html
│   ├── sales.html
│   └── about.html
│
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── script.js
```

## How to Run This Project

### Step 1: Open the project folder

```bash
cd mudi_dokan_management_system
```

### Step 2: Create virtual environment

For Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

For Mac/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install required packages

```bash
pip install -r requirements.txt
```

### Step 4: Run the Flask app

```bash
python app.py
```

### Step 5: Open browser

Go to:

```text
http://127.0.0.1:5000
```

## Database Note

The database file `mudi_dokan.db` will be created automatically when you run the project.

## Beginner Learning Notes

### What is Flask?
Flask is a Python web framework. It helps us create websites using Python.

### What is SQLAlchemy?
SQLAlchemy helps us work with a database using Python classes instead of writing SQL manually.

### What is SQLite?
SQLite is a simple database. It stores data in a file.

### What are templates?
Templates are HTML files. Flask uses them to show dynamic data on web pages.

## Important Files

### app.py
This is the main Python file. Routes, database models and backend logic are here.

### templates folder
All HTML files are here.

### static/css/style.css
All design code is here.

### static/js/script.js
All JavaScript code is here.
