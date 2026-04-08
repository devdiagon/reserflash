# ReserFlash API

Simple Flask API for user authentication and room reservations.

## Main Endpoints

Base URL: `http://localhost:5000`

### Auth

- `POST /api/auth/register`
  - Creates a new user.
  - Body:
    ```json
    {
      "username": "alice",
      "password": "secret123"
    }
    ```

- `POST /api/auth/login`
  - Authenticates a user and returns a JWT token.
  - Body:
    ```json
    {
      "username": "alice",
      "password": "secret123"
    }
    ```
  - Response:
    ```json
    {
      "token": "<jwt>"
    }
    ```

### Reservations (JWT required)

Send header on protected endpoints:

```http
Authorization: Bearer <jwt>
```

- `GET /api/reservation`
  - Returns all reservations that belong to the authenticated user.

- `POST /api/reservation`
  - Creates a reservation for the authenticated user.
  - Body:
    ```json
    {
      "date": "08/04/2026",
      "room": "A",
      "hour": "09:30 AM"
    }
    ```
  - Validation:
    - `date` format: `DD/MM/YYYY`
    - `hour` format: `HH:MM AM/PM`
    - `room` values allowed: `A`, `B`, `C`

- `DELETE /api/reservation/<id>`
  - Deletes a reservation by UUID if it belongs to the authenticated user.

## Development Setup

### 1. Configure `.env`

Create `.env` from template:

```powershell
Copy-Item template.env .env
```

Default values in `template.env`:

- `SECRET_KEY`
- `JWT_SECRET`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`
- `DB_NAME`

Adjust them if needed.

### 2. Start PostgreSQL with Docker Compose

```powershell
docker compose up -d
```

This starts PostgreSQL on `localhost:5432`.

> *You may need to change docker-compose file to match the env values related to the database*

### 3. Install dependencies and start Flask server

Activate the virtual environment (already included in this project as `env`):

```powershell
.\env\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run the API:

```powershell
python app.py
```

Flask will be available at:

- `http://localhost:5000`

## Notes

- Database tables are created automatically on startup via `db.create_all()`.
- If PowerShell blocks script execution, run this once in the current shell:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```
