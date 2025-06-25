# 🛠️ Feedback Management Backend (Django + Docker)

This is a backend application for managing structured feedback between employees and managers. It uses Django REST Framework, supports role-based access, and is fully Dockerized for easy setup.

---

## 🔧 Tech Stack

- **Backend**: Django, Django REST Framework
- **Authentication**: JWT (via `djangorestframework-simplejwt`)
- **Database**: SQLite3 (locally via Docker Compose, configurable)
- **Containerization**: Docker

---

## 🐳 Setup Instructions (Using Docker)

### 1. Clone the Repository

```bash
git clone https://github.com/yadavp473131/feedback-backend.git
cd feedback-app

### 2. Create Environment File

Create a `.env` file from the example:

```bash
cp .env.example .env


#### ✅ Step 3 build and run
```markdown
### 3. Build and Run the App with Docker

```bash
docker build -t feedback-backend .

docker run -p 8000:8000 feedback-backend

Now open: http://localhost:8000

### 4. Frontend which is deployed on render
 link - https://feeback-frontend.onrender.com


### Project Structure

feedback_app/
│
├── feedback/               # Feedback models, views, serializers
├── users/                  # Custom user logic
├── manage.py
├── requirements.txt
├── Dockerfile
├── .env.example
├── README.md
└── ...

### Endpoints for employees

| Method | Endpoint                           | Description                 |
| ------ | ---------------------------------- | --------------------------- |
| POST   | `/api/reports/`                    | Submit a work report        |
| GET    | `/api/reports/`                    | List employee's own reports |
| GET    | `/api/feedbacks/`                  | View feedback received      |
| POST   | `/api/feedbacks/<id>/acknowledge/` | Acknowledge feedback        |

### Endpoints for managers

| Method | Endpoint               | Description                        |
| ------ | ---------------------- | ---------------------------------- |
| GET    | `/api/team/`           | View list of team members          |
| GET    | `/api/reports/team/`   | View all reports from team members |
| POST   | `/api/feedbacks/`      | Submit feedback for a report       |
| PATCH  | `/api/feedbacks/<id>/` | Update existing feedback           |
| GET    | `/api/feedbacks/team/` | View all submitted feedbacks       |

### Sample users


    Manager Role Signup
    Name: Rahul Thakur
    email: rahul8120@gmail.com
    password: 123456789
    manager Id : 123456
    team id : 1234
    feedback for employee 1 : you created basic app. you did not mention about database and tables.
    feedback for employee 2 : you are doing better than others.

 
    employee 1
   
    Name: Pushpendra yadav
    email: push123@gmail.com
    password: 123456788
    employee Id : 1234567
    team Id : 1234
    
    work summary : created backend app
    Add On : I created this application using React in frontend and django in backend.

    employee 2
  
    Name : Ashwin Kumar 
    email : ashwin321@gmail.com
    password : 123456787
    employee Id : 12345678
    team ID : 1234

    work summary : deployed full stack web app
    detail : I created full stack web application using React nodejs in frontend and 
    python django in backend. I used sqlite databasea and tables USER, Report and feedback. 
