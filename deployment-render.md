# Deployment Guide for Render

## Prerequisites
- GitHub repository with the BotanIQ AI project
- Render account (sign up at render.com)

## Step 1: Prepare the Codebase
- Ensure settings.py is updated for Render (CSRF_TRUSTED_ORIGINS should be configurable)
- Commit and push changes to GitHub

## Step 2: Create Render Web Service
1. Go to Render dashboard
2. Click "New" > "Web Service"
3. Connect your GitHub repo
4. Configure:
   - Name: botaniq-ai
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn botaniq.wsgi:application --bind 0.0.0.0:$PORT`
   - Python Version: 3.13.9 (or latest supported)

## Step 3: Add PostgreSQL Database
1. In Render dashboard, click "New" > "PostgreSQL"
2. Create database (note the connection string)

## Step 4: Set Environment Variables
In the web service settings, add:
- SECRET_KEY: [generate a new secret key]
- DEBUG: False
- ALLOWED_HOSTS: [your-render-app.onrender.com]
- DATABASE_URL: [from PostgreSQL database]
- CSRF_TRUSTED_ORIGINS: https://[your-render-app.onrender.com]

## Step 5: Deploy
- Click "Create Web Service"
- Render will build and deploy automatically
- Monitor logs for any issues

## Troubleshooting
- If static files 404: WhiteNoise is configured
- If DB issues: Check DATABASE_URL
- If CSRF errors: Verify CSRF_TRUSTED_ORIGINS

## Post-Deployment
- Run migrations if needed: Use Render's shell or add a build script
- Seed data: Run management command if necessary