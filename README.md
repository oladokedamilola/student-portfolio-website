# 🎓 EduPortfolio

A modern academic portfolio platform for final-year students, built with Django.  
Students can showcase their projects, research, and internships professionally, while clients (employers or mentors) can discover and connect with them.



## 🚀 Features

- Student registration with matric number verification
- Client registration (no matric required)
- Responsive, clean academic design
- Student portfolio pages inspired by GitHub
- Public search system for students
- Dashboard with sections for projects, research, and internships
- Profile editing and social links
- Notifications for visits, stars, and favorites
- Clients can favorite (star) students



## 💻 Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS (Bootstrap 5), JavaScript
- **Database:** SQLite (development), prepared for MySQL/PostgreSQL in production



## ⚙️ Setup Instructions

### Prerequisites

- Python 3.8+
- pip

### Steps

```bash
# Clone the repository
git clone https://github.com/oladokedamilola/eduportfolio.git
cd eduportfolio

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Run the development server
python manage.py runserver
````

---

## 🤝 Contributing

Pull requests are welcome.
For major changes, please open an issue first to discuss what you'd like to change.

---

## 📝 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 💬 Contact

Developed with ❤️ by [Oladoke Damilola](https://github.com/oladokedamilola).
Email: [oladokedamilola7@gmail.com](mailto:your.email@example.com)

```


