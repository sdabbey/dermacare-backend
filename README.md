# Dermacare Backend

Welcome to the **Dermacare Backend** repository! This is the server-side implementation of the **Dermacare** platform, a dermatology management system designed to facilitate seamless communication between patients and medical staff.

## Table of Contents

- [Live API](#live-api)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Server](#running-the-server)
  - [Environment Variables](#environment-variables)
- [Project Structure](#project-structure)
- [License](#license)

## Live API

The API is hosted at:  
🔗 **[dermacare-backend.up.railway.app](https://dermacare-backend.up.railway.app/)**

## Features

- **User Authentication:** Secure authentication with JWT.
- **Prescription Management:** CRUD operations for patient prescriptions.
- **Messaging System:** Real-time chat between patients and medical staff.
- **Role-Based Access:** Separate functionalities for doctors, staff, and patients.
- **Database Management:** PostgreSQL integration with Django ORM.
- **Admin Dashboard:** Manage users, prescriptions, and hospital data.

## Tech Stack

- **Backend Framework:** Django, Django REST Framework (DRF)
- **Database:** PostgreSQL
- **Authentication:** Django Auth with JWT
- **Messaging:** WebSockets (Django Channels)
- **Deployment:** Railway

## Getting Started

### Prerequisites

Ensure you have the following installed:

- **Python** (v3.8+)
- **PostgreSQL**
- **Virtualenv** (optional but recommended)

### Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/sdabbey/dermacare-backend.git
   ```

2. **Navigate to the Project Directory:**
   ```bash
   cd dermacare-backend
   ```

3. **Create a Virtual Environment (Optional but Recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows
   ```

4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set Up the Database:**
   ```bash
   python manage.py migrate
   ```

6. **Create a Superuser (for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

### Running the Server

To start the development server, run:

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

### Environment Variables

Create a `.env` file in the root directory and configure the following:

```
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=your_postgres_database_url
ALLOWED_HOSTS=*
```

## Project Structure

```
dermacare-backend/
├── clinic/             # Main app (prescriptions, users, etc.)
│   ├── models.py       # Database models
│   ├── views.py        # API endpoints
│   ├── serializers.py  # Data serializers
│   ├── urls.py         # API routes
│   └── tests.py        # Unit tests
├── backend/            # Django project settings
│   ├── settings.py     # Project configurations
│   ├── urls.py         # Root URL config
│   ├── wsgi.py         # WSGI application
│   └── asgi.py         # ASGI application (WebSockets)
├── requirements.txt    # Python dependencies
├── manage.py           # Django CLI entry point
└── .env                # Example environment variables
```

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

🔗 *For frontend integration, check out the [Dermacare Frontend Repository](https://github.com/sdabbey/dermacare-frontend).*