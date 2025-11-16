# Render.com Deployment Guide

This guide walks you through deploying TeraBoxAPIService on [Render.com](https://render.com).

## Prerequisites

- GitHub account with your repository pushed
- Render.com account (free tier available)
- MongoDB Atlas account (free tier available)

## Step-by-Step Deployment

### 1. Create MongoDB Atlas Database (Free)

1. Go to [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Sign up for a free account
3. Create a new project
4. Create a free cluster (M0 tier)
5. Set up a database user and get your connection string:
   ```
   mongodb+srv://username:password@cluster.mongodb.net/terabox_service
   ```
6. Save this `MONGO_URI` for later

### 2. Prepare Your Repository

Make sure your repo has:
- `Dockerfile` (for API)
- `Dockerfile.bot` (for Bot)
- `render.yaml` (deployment config)
- `TeraBoxAPIService/` folder
- `.env.example` file

Push all changes to GitHub:
```bash
git add -A
git commit -m "Prepare for Render deployment"
git push origin main
```

### 3. Deploy on Render

1. **Go to [render.com](https://render.com)** and sign in
2. **Click "Dashboard"** → **"New +"** → **"Blueprint"**
3. **Connect GitHub Repository**:
   - Choose your repository containing the code
   - Authorize Render to access your GitHub
4. **Select the Repository** and confirm
5. **Review the Services**:
   - `terabox-api` (Web Service on port 8000)
   - `terabox-bot` (Web Service for Telegram Bot)

### 4. Set Environment Variables

For both services, set these variables in Render:

| Variable | Value | Example |
|----------|-------|---------|
| `BOT_TOKEN` | Your Telegram bot token | `123456:ABCDEF...` |
| `API_ID` | Your Telegram API ID | `12345678` |
| `API_HASH` | Your Telegram API hash | `abcdef123...` |
| `MONGO_URI` | MongoDB Atlas connection string | `mongodb+srv://user:pass@cluster.mongodb.net/terabox_service` |
| `MONGO_DB` | Database name | `terabox_service` |
| `ADMIN_IDS` | Comma-separated admin Telegram IDs | `123456789,987654321` |
| `API_URL` | Your Render API URL | `https://terabox-api-xxxx.onrender.com` |
| `TERA_BASE_API` | Base parsing API | `https://teraapi.boogafantastic.workers.dev` |

### 5. Deploy

1. **Click "Deploy"**
2. Render will:
   - Build Docker images
   - Start both services
   - Assign public URLs to each

### 6. Get Your URLs

Once deployed, you'll receive two URLs:
- **API Service**: `https://terabox-api-xxxx.onrender.com`
- **Bot Service**: `https://terabox-bot-xxxx.onrender.com` (for health checks)

### 7. Update API_URL

1. Go to your **terabox-api** service settings
2. Update the `API_URL` environment variable to your actual API URL:
   ```
   https://terabox-api-xxxx.onrender.com
   ```
3. Redeploy the service

## Full API Endpoint

Once deployed, your complete API endpoint will be:

```
https://terabox-api-xxxx.onrender.com/run?key=YOUR_API_KEY&url=TERABOX_LINK
```

Share this with users for accessing your API!

## Services Structure

### terabox-api (FastAPI)
- **Port**: 8000
- **Endpoint**: `/run?key=...&url=...`
- **Health Check**: `GET /docs` (Swagger UI)

### terabox-bot (Pyrogram)
- **Type**: Background Telegram Bot
- **Runs on**: Long polling (no webhook needed)
- **Status**: Will be marked as "running" on Render

## Troubleshooting

### Bot Not Responding
- Check bot service logs in Render dashboard
- Verify `BOT_TOKEN`, `API_ID`, `API_HASH` are correct
- Ensure MongoDB is accessible

### API Errors
- Check API service logs
- Verify `MONGO_URI` connection string
- Test endpoint with: `curl https://your-api-url/docs`

### MongoDB Connection Failed
- Check MongoDB Atlas IP whitelist (allow all IPs for free tier)
- Verify `MONGO_URI` in environment variables
- Ensure database user password is correct

## Monitoring

### View Logs
1. Go to Render Dashboard
2. Select your service
3. Click "Logs" tab
4. Scroll through real-time logs

### Restart Services
1. Go to service page
2. Click "Settings"
3. Click "Restart Service"

## Updating Your Code

After pushing changes to GitHub:
1. Go to your service on Render
2. Services auto-redeploy (if auto-deploy is enabled)
3. Or manually click "Redeploy" to rebuild

## Free Tier Limits (Render)

- Services spin down after 15 minutes of inactivity
- Limited to 750 free hours/month
- For production, upgrade to paid plan

## To Always Keep Bot Running

Use Render's paid tier or add a simple keep-alive endpoint that external services ping periodically.

---

**Deployed! 🚀** Your TeraBox API Service is now live on Render.
