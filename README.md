# Todo App

A Django-based todo application.

## Setup

### Prerequisites
- Python 3.8+
- Pipenv

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd todo-app
```

2. Install dependencies:
```bash
pipenv install
```

3. Activate the virtual environment:
```bash
pipenv shell
```

4. Create a `.env` file in the root directory and add:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Start the development server:
```bash
python manage.py runserver
```

The app will be available at `http://localhost:8000`

## Project Structure

- `main/` - Main app with templates and static files
- `tasks/` - Tasks app with API endpoints
- `todo_app/` - Project settings and configuration
