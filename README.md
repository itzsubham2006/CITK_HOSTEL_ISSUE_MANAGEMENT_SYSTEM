 # CITK_HOSTEL_ISSUE_MANAGEMENT_SYSTEM
 
Live at : https://subham-8zpt.onrender.com
 

A Flask-based web application designed to help students of **Central Institute of Technology, Kokrajhar (CITK)** report hostel-related issues and allow administrators to manage and resolve them efficiently.

---

## 🚀 Features

- Student registration and login
- Secure password hashing using Bcrypt
- Issue/complaint reporting system
- Categorized hostel issues
- Admin panel for issue management
- Flask Blueprints for modular structure
- SQLAlchemy ORM for database handling

---

## 🛠 Tech Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, Jinja2
- **Database:** SQLite (can be upgraded to MySQL/PostgreSQL)
- **ORM:** Flask-SQLAlchemy
- **Authentication:** Flask-Bcrypt, Flask-WTF

---

## 📁 Project Structure

CITK_HOSTEL_ISSUE_MANAGEMENT_SYSTEM/
│
├── app/
│ ├── init.py
│ ├── config.py
│ ├── extensions.py
│
│ ├── models/
│ │ ├── init.py
│ │ ├── user.py
│ │ ├── category.py
│ │ └── complaints.py
│
│ ├── forms/
│ │ ├── init.py
│ │ └── forms.py
│
│ ├── routes/
│ │ ├── init.py
│ │ └── auth_routes.py
│
│ ├── templates/
│ │ └── auth/
│
│ └── static/
│
├── run.py
├── requirements.txt
├── README.md
└── .gitignore


---

## ⚙️ Installation & Setup
### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/citk-hostel-issue-reporting-system.git
cd CITK_HOSTEL_ISSUE_MANAGEMENT_SYSTEM
```



2️⃣ Create and activate virtual environment
python -m venv hackvenv
hackvenv\Scripts\activate   # Windows


3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run the application
python run.py



🌐 Routes

URL	Description
/auth/register	Student Registration
/auth/login	Student Login
/auth/home	Dashboard/Home

🔐 Security
Passwords are hashed using Flask-Bcrypt
CSRF protection using Flask-WTF



📌 Future Enhancements
Role-based access (Admin/Student)
Complaint status tracking
Email notifications
File uploads (images of issues)
REST API support


👨‍💻 Author
Subham Pathak, Nikesh Pathak, Subhadip Sarkar, Jitul Roy

Students of Central Institute of Technology, Kokrajhar

