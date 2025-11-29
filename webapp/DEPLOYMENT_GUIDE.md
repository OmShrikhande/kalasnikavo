# Deployment Guide: Flask Backend on Render & React Frontend on Netlify

## Prerequisites
- GitHub account with your repository pushed
- Render account (https://render.com)
- Netlify account (https://netlify.com)

---

## Part 1: Backend Deployment on Render

### Step 1: Prepare Your Repository

1. Ensure all files are committed and pushed to GitHub:
```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

2. Files created for deployment:
   - `requirements.txt` - Python dependencies
   - `Procfile` - Tells Render how to run the app
   - `.env.example` - Environment variables template

### Step 2: Create Render Service

1. Go to [https://render.com](https://render.com) and sign in
2. Click **New +** → **Web Service**
3. Select your GitHub repository (biometric authentication project)
4. Fill in the form:
   - **Name**: `biometric-auth-api` (or your choice)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app_enhanced:app`

### Step 3: Set Environment Variables

1. Scroll to **Environment** section in Render dashboard
2. Add these variables:
   ```
   FLASK_ENV = production
   SECRET_KEY = (generate a long random string, e.g., using https://randomkeygen.com/)
   JWT_SECRET = (generate another random string)
   ALLOWED_ORIGINS = https://your-netlify-domain.netlify.app,https://www.your-netlify-domain.netlify.app
   ```

3. Click **Deploy Web Service**

### Step 4: Get Your Backend URL
Once deployed, Render provides a URL like:
```
https://biometric-auth-api-xxxxx.onrender.com
```
**Save this URL** - you'll need it for the frontend.

---

## Part 2: Frontend Deployment on Netlify

### Step 1: Prepare Frontend Build

1. Update your API calls in React components to use the environment variable:
   ```javascript
   const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';
   ```

2. In your API calls, use:
   ```javascript
   fetch(`${API_URL}/api/endpoint`)
   ```

### Step 2: Connect to Netlify

1. Go to [https://netlify.com](https://netlify.com) and sign in
2. Click **Add new site** → **Import an existing project**
3. Choose **GitHub** and authorize
4. Select your repository
5. Fill in the form:
   - **Base directory**: Leave empty (root)
   - **Build command**: `npm run build`
   - **Publish directory**: `dist`

### Step 3: Set Environment Variables for Frontend

1. Go to **Site settings** → **Build & deploy** → **Environment**
2. Add variable:
   ```
   VITE_API_URL = https://biometric-auth-api-xxxxx.onrender.com
   ```
   (Replace with your actual Render backend URL)

3. Click **Deploy site**

### Step 4: Get Your Frontend URL
After deployment, Netlify provides a URL like:
```
https://your-site-name.netlify.app
```

---

## Part 3: Update Backend CORS Settings

1. Go back to your Render service dashboard
2. Update the `ALLOWED_ORIGINS` environment variable to include your Netlify URL:
   ```
   ALLOWED_ORIGINS = https://your-site-name.netlify.app,https://www.your-site-name.netlify.app
   ```
3. This change will auto-redeploy the backend

---

## Part 4: Test the Deployment

1. Visit your Netlify frontend URL
2. Test authentication endpoints:
   - Registration
   - Face recognition upload
   - Fingerprint upload
   - Login

Monitor Render logs if you encounter errors:
- Go to Render dashboard → Your service → Logs

---

## Troubleshooting

### Issue: CORS Errors
- ✓ Check `ALLOWED_ORIGINS` in Render environment variables
- ✓ Ensure Netlify URL matches exactly (including protocol)

### Issue: 404 on API Calls
- ✓ Verify `VITE_API_URL` environment variable in Netlify
- ✓ Check Render backend is running (check Logs)

### Issue: Large Dependencies Timeout on Render
- TensorFlow/OpenCV are large
- Can increase build timeout in Render settings
- Or consider using a separate ML API service

### Issue: Database Issues
- SQLite is used locally; consider migrating to PostgreSQL for production
- Go to Render → Create PostgreSQL database
- Update connection string in Flask app

---

## Security Notes

1. **Never commit `.env` files** - only commit `.env.example`
2. **Regenerate SECRET_KEY and JWT_SECRET** for production
3. **Use strong passwords** for all accounts
4. **Enable HTTPS** - Both Render and Netlify provide it by default

---

## Optional: Custom Domain

### For Netlify Frontend:
1. **Site settings** → **Domain settings**
2. **Add custom domain** and follow DNS configuration

### For Render Backend:
1. **Environment** → **Custom domain**
2. Configure DNS records

---

## Useful Commands for Local Development

```bash
# Install dependencies
npm install
pip install -r requirements.txt

# Run frontend (Vite)
npm run dev

# Run backend (Flask)
python app_enhanced.py

# Build frontend for production
npm run build
```

---

## Next Steps

1. Monitor both services for errors
2. Set up error logging/monitoring
3. Consider database backup strategies
4. Plan for scaling if needed
