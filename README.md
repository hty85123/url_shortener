# url_shortener

## Overview
This project is a Django-based URL shortener application built using the MTV (Model-Template-View) framework. It supports third-party authentication via Google and Facebook OAuth, provides URL shortening services, and includes support for JWT-based API access to demonstrate potential for future frontend-backend separation.

## Features

1. **Django MTV Framework**: Implements a tightly integrated backend and frontend architecture, following Django's traditional MTV design.
2. **Third-Party Login**:
  - **Google OAuth**: Fully supported.
  - **Facebook OAuth**: Requires Facebook developer approval; currently, only developer accounts added to the application can log in using Facebook.
3. **URL Shortening Service**:
  - Utilizes a custom method combining a snowflake-like ID generation mechanism and 62-based encoding to generate unique short URLs.
  - Authenticated users can:
    - View their created short URLs.
    - Check click counts for each URL.
    - Access detailed click records, including timestamp and source IP address.
4. **Future-Proof API Support**:
  - Opened an API endpoint (`/api/auth/google/`) for Google OAuth token exchange, allowing:
    - Input: `access_token` and `id_token` from local console after logging, and `Code`="".
    - Output: JWT `access_token` and `refresh_token`.
  - Provides a secure API endpoint (`/api/urls/`) for retrieving user-specific URLs using the JWT `access_token`.
  - Access to `access_token` and `id_token` is currently limited to viewing via the local console.

## Quick Start Guide
### Prerequisites
- Python 3.9+
- Google and Facebook OAuth credentials
### Setup Instructions
1. Clone the Repository
2. Create and Activate Virtual Environment
3. Install Dependencies
```bash
pip install -r requirements.txt
```
4. Setup Environment Variables by Creating a `.env` File in the Project Root:
```.env
SECRET_KEY=your-secret-key
DB_NAME=your-database-name # Uncomment this to use default sqlite DB
DB_USER=your-database-user # Uncomment this to use default sqlite DB
DB_PASSWORD=your-database-password # Uncomment this to use default sqlite DB
DB_HOST=your-database-host # Uncomment this to use default sqlite DB
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
FACEBOOK_CLIENT_ID=your-facebook-client-id
FACEBOOK_CLIENT_SECRET=your-facebook-client-secret
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```
5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```
6. Run Development Server
```bash
python manage.py runserver
```

## Future-Proof API
1. Login with your Google Account
You can see something like this on you terminal:
```
Django version 4.2.17, using settings 'url_shortener.settings.local'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.

[03/Jan/2025 08:35:46] "GET /accounts/google/login/?process=login HTTP/1.1" 302 0
hty85123
Access Token: ya29.a0ARW5m74cOMnlWtHvfijgnMPN0KVTs_3sWFQyh05RWTQ6dz2etvYrL11XMB1GVNRjuU5CP9dIiHZXNRv7W9B6vM3nXoy1TInqhvsAu1dh9Z84NgkMJSM3wS99jOLwA5F3QY8KEMYaMSZ5gclUcgC2vUgFtGo742-rVwaCgYKAVUSARASFQHGX2MiQQs9CLWr8IC7sxUfoYwwqQ0169
ID Token:
[03/Jan/2025 08:35:51] "GET /accounts/google/login/callback/?state=DMhhTeJqck2RVe5L&code=4%2F0AanRRrt942JLTNseB9k-yxp0wS8PWIHV8cZJFK20gNjLxJXbXPB7EEWPpHDJq3J4j52eDw&scope=email+profile+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile+openid&authuser=0&prompt=none HTTP/1.1" 302 0
[03/Jan/2025 08:35:51] "GET / HTTP/1.1" 302 0
[03/Jan/2025 08:35:51] "GET /list/ HTTP/1.1" 200 1180
```
In the example, `Access Token` is `"ya29.a0ARW5m74cOMnlWtHvfijgnMPN0KVTs_3sWFQyh05RWTQ6dz2etvYrL11XMB1GVNRjuU5CP9dIiHZXNRv7W9B6vM3nXoy1TInqhvsAu1dh9Z84NgkMJSM3wS99jOLwA5F3QY8KEMYaMSZ5gclUcgC2vUgFtGo742-rVwaCgYKAVUSARASFQHGX2MiQQs9CLWr8IC7sxUfoYwwqQ0169"` and `ID Token` is `""`.

2. Go to the end point `http://localhost:8000/api/auth/google/`. Then, enter `Access Token` and `ID Token` from the previous step with `Code`=`""`.
3. You would get the JWT `access token` and `refresh token` from the previous step.
4. Using curl or Postman to access the endpoint (`api/urls`). You would get the results like this:
```json
{
    "urls": [
        {
            "original_url": "https://chatgpt.com/g/g-2DQzU5UZl-code-copilot/c/67650e0c-5098-800f-851e-da59c8966e25",
            "short_url": "246m1Ur",
            "clicks_count": 3
        },
        {
            "original_url": "https://www.google.co.jp/",
            "short_url": "3PfVQ61",
            "clicks_count": 1
        }
    ]
}
```
