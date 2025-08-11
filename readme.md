# AnomyForm - Anonymous Form System

A secure, anonymous form creation and submission system designed for organizations to collect honest feedback while maintaining complete privacy. Built with Django REST API backend and React frontend.

## 🎯 Overview

AnomyForm allows organizations to create anonymous forms that users can fill out using only their unique 6-character code. The system ensures complete anonymity while preventing duplicate submissions and maintaining data integrity.

## ✨ Key Features

### 🔐 **Complete Anonymity**
- No personal information collected with form responses
- Users identified only by unique 6-character codes
- One-time submission per form per user prevents duplicates
- No account creation required for form submission

### 🛡️ **Security & Access Control**
- Role-based form access restrictions
- Department and group-based permissions
- CSRF protection and secure file uploads
- JWT authentication for admin access

### 📝 **Flexible Question Types**
- **Text**: Short and long text responses with character limits
- **Number**: Numeric inputs with validation
- **Boolean**: Yes/No questions
- **Radio**: Single choice from multiple options
- **Checkbox**: Multiple choice selections
- **Select**: Dropdown menu selections
- **File Upload**: Document, image, and spreadsheet uploads

### 📁 **File Upload Support**
- Multiple file types: Images, PDFs, Word docs, Excel files, CSV, ZIP
- Configurable file size limits (min/max in MB)
- MIME type validation
- Secure file storage with unique naming

### 🎨 **Modern User Interface**
- Responsive design for all devices
- Real-time form validation
- Progress tracking for required questions
- Dark/light theme support
- Accessible design with screen reader support

## 🏗️ Architecture

### Backend (Django REST API)
- **Framework**: Django 5.2.4 + Django REST Framework
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Authentication**: Custom User model with email-based auth
- **File Storage**: Secure file upload handling
- **Email**: SMTP integration for user code delivery

### Frontend (React + TanStack)
- **Framework**: React 19 with TanStack Router & Query
- **Styling**: Tailwind CSS v4 + shadcn/ui components
- **Build Tool**: Vite
- **State Management**: TanStack Query for server state

## 📋 Database Schema

```python
# Core Models
User (email, first_name, last_name, code, role, department, group)
Role, Department, Group (organization structure)
Form (name, enable, roles, department, group)
Questions (question, required, answer_type, options, file_type)
FormQuestion (form, question, form_index)
FormResponse (form, response_json)
FormUser (user, form) # Tracks submissions
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- pnpm (recommended) or npm

### Backend Setup

1. **Clone and navigate to backend**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment configuration**
Create `.env` file:
```env
SECRET_KEY=your-secret-key-here
JWT_KEY=your-jwt-key-here
ENVIRONMENT=development
COOKIE_DOMAIN=localhost
EMAIL_HOST_USER=your-email@domain.com
EMAIL_HOST_PASSWORD=your-email-password
VERIFICATION_URL=http://localhost:3000/verify-email
PASSWORD_RESET_URL=http://localhost:3000/reset-password
```

5. **Database setup**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Run development server**
```bash
python manage.py runserver
```

### Frontend Setup

1. **Navigate to client directory**
```bash
cd client
```

2. **Install dependencies**
```bash
pnpm install
```

3. **Environment configuration**
Create `.env` file:
```env
VITE_BASE_URL=http://localhost:8000/api
```

4. **Run development server**
```bash
pnpm dev
```

## 📖 Usage Guide

### For Form Creators (Admins)

1. **Access Admin Panel**
   - Visit `http://localhost:8000/admin-back-office/`
   - Login with superuser credentials

2. **Create Organization Structure**
   - Add Roles, Departments, and Groups
   - Assign users to appropriate roles/departments/groups

3. **Create Forms**
   - Create new Form with name and access controls
   - Add Questions with appropriate types and validation
   - Link Questions to Forms with FormQuestion entries
   - Enable the form when ready

4. **Distribute User Codes**
   - Users receive unique 6-character codes via email
   - Share form URLs with target audience

### For Form Respondents

1. **Get User Code**
   - Visit the form page
   - Click "Get User Code" button
   - Enter email to receive unique code

2. **Fill Form**
   - Navigate to form URL: `/form/edit/{formId}/`
   - Complete all required questions
   - Upload files if required
   - Submit form with user code

3. **One-time Submission**
   - Each user can only submit once per form
   - System prevents duplicate submissions
   - Responses remain completely anonymous

## 🔧 API Endpoints

### Form Operations
- `GET /api/forms/{formId}/` - Retrieve form with questions
- `POST /api/forms/submit` - Submit anonymous form response
- `GET /api/csrf-token/` - Get CSRF token

### User Management
- `GET /api/resend_code/?email={email}` - Send user code via email

## 🛡️ Security Features

- **CSRF Protection**: All form submissions protected
- **File Validation**: Size and type restrictions
- **Access Control**: Role/department/group-based permissions
- **Secure Storage**: Files stored with unique names
- **CORS Configuration**: Controlled cross-origin requests
- **Input Validation**: Server-side validation for all inputs

## 🎨 Customization

### Email Templates
Customize email templates in `backend/templates/email/`:
- `verification_email.html` - User code delivery
- `forgot_password_email.html` - Password reset

### Question Types
Add new question types by extending the `Questions` model and updating the frontend `QuestionRenderer` component.

### Styling
Modify Tailwind CSS classes in frontend components or update the theme configuration.

## 🚀 Deployment

### Production Checklist

1. **Environment Variables**
   ```env
   ENVIRONMENT=production
   SECRET_KEY=your-production-secret-key
   JWT_KEY=your-production-jwt-key
   ```

2. **Database**
   - Configure PostgreSQL connection
   - Run migrations: `python manage.py migrate`

3. **Static Files**
   ```bash
   python manage.py collectstatic
   ```

4. **Security**
   - Set `DEBUG=False`
   - Configure `ALLOWED_HOSTS`
   - Use HTTPS in production
   - Set secure cookie settings

5. **Email**
   - Configure production SMTP settings
   - Update verification URLs to production domain

## 📁 Project Structure

```
anonymous-form/
├── backend/                 # Django REST API
│   ├── AppName/            # Main project settings
│   ├── authentication/     # User management
│   ├── forms/             # Form system
│   ├── organisation/      # Role/department/group models
│   ├── templates/         # Email templates
│   └── utils/            # Utility functions
├── client/                # React frontend
│   ├── src/
│   │   ├── components/   # UI components
│   │   ├── lib/         # Utilities and API
│   │   └── routes/      # Application routes
│   └── public/          # Static assets
└── nginx.conf           # Nginx configuration
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the Django and React documentation
2. Review the API endpoints at `/api/`
3. Open an issue in the repository

## 🎯 Roadmap

- [x] Complete anonymous form system
- [x] User code generation and email delivery
- [x] Multi-question type support
- [x] File upload with validation
- [x] One-time submission prevention
- [x] Modern responsive UI
- [ ] Role/department/group form restrictions
- [ ] Admin dashboard for form management
- [ ] Landing page improvements
- [ ] Analytics and reporting features
- [ ] Bulk user code generation
- [ ] Form templates and cloning

---

**Built with ❤️ using Django, React, and modern web technologies**