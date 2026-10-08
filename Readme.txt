Task - Items & Users API

A simple REST API built with FastAPI and SQLAlchemy using SQLite, tested with Postman.

What It Does

- Items API — Create, read, update, and delete items
- Users API — Create, read, update, and delete users

Requirements

- Python 3.10 or higher
- pip

Setup Instructions
1. Clone the repository

git clone <github-url>
cd <folder>

2. Create a virtual environment
python -m venv .env
.env\Scripts\activate

3. Install requirements mentioned in requrirements.txt
pip install -r requirements.txt

4. Run the api 
uvicorn main:app --reload