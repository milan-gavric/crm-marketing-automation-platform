# Leads Manager Server

Django REST API server for Email Leads Manager application. This is a Python/Django port of the Node.js email-leads-manager-server.

## Features

- User authentication with JWT tokens
- Lead management with CSV upload support
- Account management
- Email management
- Message and Subject template management
- RESTful API endpoints
- CORS support

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file (optional):
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
JWT_SECRET=your-jwt-secret-key-here
FRONTEND_URL=http://localhost:3000
MONGODB_URI=mongodb://localhost:27017/
MONGODB_NAME=email-leads-manager
NYLAS_API_KEY=your-nylas-api-key-here
NYLAS_API_URI=https://api.nylas.com
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

The server will run on `http://localhost:8000` by default.

## API Endpoints

### Users (Authentication)
- `POST /api/user/login` - Login user
- `POST /api/user/logout` - Logout user

### Leads
- `GET /api/lead/` - Get all leads (with pagination, search, status, assignedTo filters)
- `POST /api/lead/` - Create a new lead
- `POST /api/lead/upload/` - Upload leads from CSV file
- `GET /api/lead/{id}/` - Get a specific lead
- `PUT /api/lead/{id}/` - Update a lead
- `DELETE /api/lead/{id}/` - Delete a lead

### Accounts
- `GET /api/account/` - Get all accounts (with pagination)
- `POST /api/account/` - Create a new account
- `GET /api/account/{id}/` - Get a specific account
- `PUT /api/account/{id}/` - Update an account
- `DELETE /api/account/{id}/` - Delete an account

### Emails
- `GET /api/email/` - Get all emails (with pagination and search)
- `POST /api/email/` - Create a new email
- `GET /api/email/{id}/` - Get a specific email
- `PUT /api/email/{id}/` - Update an email
- `DELETE /api/email/{id}/` - Delete an email
- `POST /api/email/send/` - Send email via Nylas

### Templates
- `GET /api/template/message/` - Get all message templates (with pagination, search, industry filters)
- `GET /api/template/subject/` - Get all subject templates (with pagination and search)

### Health Check
- `GET /health` - Server health check

## Send Email Endpoint

The send email endpoint (`POST /api/email/send/`) allows you to send emails using Nylas. 

### Request Body

```json
{
  "grant_id": "nylas_grant_id_here",
  "to": ["recipient@example.com"],
  "subject": "Email Subject",
  "body": "<html><body><h1>Hello</h1><p>This is the email body in HTML</p></body></html>",
  "cc": ["cc@example.com"],
  "bcc": ["bcc@example.com"],
  "reply_to": ["reply@example.com"],
  "body_type": "html"
}
```

### Required Fields
- `grant_id`: Nylas grant ID (connected account ID)
- `to`: Array of recipient email addresses
- `subject`: Email subject line
- `body`: Email body content (HTML or plain text)

### Optional Fields
- `cc`: Array of CC email addresses
- `bcc`: Array of BCC email addresses
- `reply_to`: Array of reply-to email addresses
- `body_type`: Either "html" or "text" (default: "html")

### Response

Success response (200):
```json
{
  "success": true,
  "message": "Email sent successfully",
  "data": {
    "success": true,
    "message_id": "message_id_from_nylas",
    "thread_id": "thread_id_from_nylas",
    "grant_id": "grant_id_used"
  }
}
```

Error response (400/500):
```json
{
  "error": "Error message",
  "details": "Detailed error information"
}
```

### Nylas Setup

1. Sign up for a Nylas account at https://www.nylas.com
2. Get your API key from the Nylas dashboard
3. Set up OAuth to connect email accounts and get grant IDs
4. Add `NYLAS_API_KEY` to your `.env` file
5. Optionally set `NYLAS_API_URI` if using a custom API URI

## Database

By default, the project uses SQLite. To use MongoDB, you'll need to:
1. Install `djongo` or `mongoengine`
2. Update the `DATABASES` configuration in `settings.py`

## Project Structure

The project is organized into modular Django apps, each handling a specific domain:

```
leads-manager-server/
├── leads_manager/          # Django project settings
│   ├── settings.py         # Project settings
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI configuration
├── users/                  # User management and authentication module
│   ├── models.py          # User model
│   ├── views.py           # Login/logout views
│   ├── serializers.py     # User serializers
│   ├── urls.py            # User routes (/api/user/)
│   ├── authentication.py  # JWT authentication
│   └── admin.py           # Django admin configuration
├── accounts/               # Account management module
│   ├── models.py          # Account model
│   ├── views.py           # Account views
│   ├── serializers.py     # Account serializers
│   ├── urls.py            # Account routes (/api/account/)
│   └── admin.py           # Django admin configuration
├── leads/                  # Lead management module
│   ├── models.py          # Lead model
│   ├── views.py           # Lead views (including CSV upload)
│   ├── serializers.py     # Lead serializers
│   ├── urls.py            # Lead routes (/api/lead/)
│   └── admin.py           # Django admin configuration
├── emails/                 # Email management module
│   ├── models.py          # Email model
│   ├── views.py           # Email views
│   ├── serializers.py     # Email serializers
│   ├── urls.py            # Email routes (/api/email/)
│   └── admin.py           # Django admin configuration
├── templates/              # Template management module
│   ├── models.py          # MessageTemplate and SubjectTemplate models
│   ├── views.py           # Template views
│   ├── serializers.py     # Template serializers
│   ├── urls.py            # Template routes (/api/template/)
│   └── admin.py           # Django admin configuration
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Development

The project uses Django REST Framework for API endpoints. Authentication is handled via JWT tokens stored in cookies or Authorization headers.

## Notes

- The authentication middleware is configured but can be enabled/disabled per route
- CSV upload supports flexible column naming (email, Email, firstname, first_name, etc.)
- All timestamps are automatically managed by Django
- The API follows RESTful conventions with pagination support

