[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/TQZAUpJd)
# Job applications (AI/Backend/Frontend)

# Job Applications Helper Backend

## Purpose for Frontend Developers

This backend project provides a REST API designed specifically to support frontend applications in managing and displaying user resumes (CVs). It exposes endpoints that allow your frontend to create, read, update, and delete resume data, including nested details like job history, skills, and education.

With this backend:
- Your frontend can fetch resumes in a detailed JSON format ready to be rendered.
- Ownership controls ensure users can only modify their own data.
- The API is built with Django REST Framework for easy integration and extensibility.

## API Overview

- **Base URL:** `/api/v3/resumes/`
- Supports standard RESTful operations with JSON input/output.
- Nested data structure for `job_history`, `skills`, and `education_history`.
- Authentication required for modifying resumes.
  
## Getting Started

Use the API endpoints to integrate resume features into your frontend:

- **List resumes:** GET `/api/v3/resumes/`
- **Create resume:** POST `/api/v3/resumes/`  
  Include fields like `name`, `bio`, `address`, plus nested arrays for skills, job history, and education.
- **Detail/Update/Delete:** GET, PUT, DELETE `/api/v3/resumes/{id}/`

## Authentication

The backend expects authenticated requests to restrict modifications to resume owners only. Make sure your frontend manages user login and passes authentication tokens accordingly.

## Environment Setup (Backend Notes)

- Python 3, Django and Django REST Framework used.
- Environment variables manage secrets and debug settings.
- CORS is configured to allow frontend-server communication.

## Running the Backend Locally

Start the Django development server using:

python manage.py runserver

Access API docs or test endpoints through browsable API or via tools like Postman.

## Testing

Automated tests ensure API responses and permissions are correct:

python manage.py test resumes


---

This backend serves as a robust foundation allowing the frontend to focus on smooth user experience and UI without worrying about data storage and permission logic.