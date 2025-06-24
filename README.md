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

