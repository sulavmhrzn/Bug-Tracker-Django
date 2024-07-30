# Django Bug Tracker Project

## Project Description
This Bug Tracker is a comprehensive project management and issue tracking system designed to streamline the software development process. It allows managers and developers to efficiently track and manage bugs across multiple projects.
## Features
- User account creation (Manager and Developer roles)
- Project management (Create, List, Update, Delete)
- Bug tracking (Create, List, Update, Delete)
- Developer assignment to projects
- Bug assignment to developers
- Customizable bug statuses and priorities
- Comment system for bugs
- Dashboard with project and bug statistics
- Email notifications for bug updates
- Advanced search and filtering options
- **TODO** File and screenshot attachments for bug reports

## Technologies Used
- Python 3.12
- Django 5
- SQLite
- Tailwind CSS

## Getting Started

### Prerequisites
- Python 3.12
- pip (Python package manager)

### Installation
1. Clone the repository:
   ```
   git clone https://github.com/sulavmhrzn/bug_tracker_django.git
   ```
2. Navigate to the project directory:
   ```
   cd bug_tracker_django
   ```
3. Create a virtual environment:
   ```
   python -m venv venv
   ```
4. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```
5. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
6. Apply database migrations:
   ```
   python manage.py migrate
   ```

### Running the Application
1. Create a superuser account:
   ```
   python manage.py createsuperuser
   ```
   Follow the prompts to create a new superuser account.
2. Start the Django development server:
   ```
   python manage.py runserver
   ```
3. The application will be available at `http://localhost:8000`

## Usage
- Access the admin panel at http://localhost:8000/admin/ to manage users and projects.
- Managers can create projects and assign developers.
- Developers can view assigned projects and manage bugs.
- Use the dashboard for an overview of project status and bug statistics.

## TODO: Deployment 

## Contributing
This project is part of my personal portfolio, but I welcome any suggestions or feedback. Feel free to open an issue or submit a pull request.

