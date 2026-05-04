# Todo App

A Django-based todo application.

Application URL: https://lawadvisorereyes.pythonanywhere.com/

## Criteria

- The user should be able to list all tasks in the TODO list
- The user should be able to add a task to the TODO list
- The user should be able to update the details of a task in the TODO list
- The user should be able to remove a task from the TODO list
- The user should be able to reorder the tasks in the TODO list
    - A task in the TODO list should be able to handle being moved more than 50 times
    - A task in the TODO list should be able to handle being moved to more than one task away from its current position
    - Note: You can think of this as an API endpoint that will be used to handle the drag-and-drop feature of a TODO list application
- The application should be able to handle 1 million tasks with a reasonable response time (under 5 seconds)

General requirements
- All endpoints should return JSON responses.
- Do not use sorting libraries, we’d prefer you write your own sorting strategy.

## Developer Notes
- I followed the Gap-based ordering approach to improve scalability specially in reordering
- I used infinite scroll approach to minimize the burden of returning large data to the frontend thus improving scalability.
- Currently using SQLite3 as default DB, scalability will improve if I upgrade.
- I am not able to confirm if this will run 1 mil tasks under 5 second.

## Deployment Notes:
- I deployed the application through pythonanywhere.com
- Using the credentials
    username: LawAdvisorEreyes
    password: testing321

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
SECRET_KEY='django-insecure-+mz6g2%m9fh0)jvvd6hjq*2-@s49=-e&ue$)sz7nmx!3%k)f*$'
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,LawAdvisorEreyes.pythonanywhere.com
```
Best Practice is to not display any credentials in the Repo. (This is only a technical app test)

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
