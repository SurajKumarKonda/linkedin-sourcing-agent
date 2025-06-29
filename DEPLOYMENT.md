# 🚀 Hugging Face Spaces Deployment Guide

This guide will help you deploy your LinkedIn Sourcing Agent API to Hugging Face Spaces.

## 📋 Prerequisites

1. **Hugging Face Account**: Sign up at https://huggingface.co/
2. **API Keys**: 
   - SerpAPI key (https://serpapi.com/)
   - RapidAPI key (https://rapidapi.com/)

## 🛠️ Deployment Steps

### Step 1: Create a New Space

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Fill in the details:
   - **Owner**: Your username
   - **Space name**: `linkedin-sourcing-agent` (or any name you prefer)
   - **License**: MIT
   - **SDK**: **Docker**
   - **Space hardware**: CPU (free tier) or upgrade if needed

### Step 2: Upload Files

Upload these files to your Space:

**Required Files:**
- `app.py` - Main FastAPI application
- `search.py` - LinkedIn search functionality
- `score.py` - Candidate scoring logic
- `outreach.py` - Outreach message generation
- `fetch_profile.py` - LinkedIn profile fetching
- `requirements_api.txt` - Python dependencies
- `Dockerfile` - Docker configuration
- `README.md` - Documentation

### Step 3: Set Environment Variables

1. Go to your Space settings
2. Navigate to "Repository secrets"
3. Add these secrets:
   - `SERPAPI_API_KEY`: Your SerpAPI key
   - `RAPIDAPI_KEY`: Your RapidAPI key

### Step 4: Deploy

1. The Space will automatically build and deploy
2. Wait for the build to complete (usually 2-5 minutes)
3. Your API will be available at: `https://your-username-linkedin-sourcing-agent.hf.space`

## 🔗 API Usage

### Base URL
```
https://your-username-linkedin-sourcing-agent.hf.space
```

### Endpoints

#### 1. Health Check
```bash
curl https://your-username-linkedin-sourcing-agent.hf.space/health
```

#### 2. Find Candidates
```bash
curl -X POST "https://your-username-linkedin-sourcing-agent.hf.space/sourcing" \
  -H "Content-Type: application/json" \
  -d '{
    "job_description": "Senior ML Engineer with LLM experience",
    "location": "Mountain View",
    "num_candidates": 5
  }'
```

### Python Example
```python
import requests

response = requests.post(
    "https://your-username-linkedin-sourcing-agent.hf.space/sourcing",
    json={
        "job_description": "Senior ML Engineer with LLM experience",
        "location": "Mountain View",
        "num_candidates": 5
    }
)

candidates = response.json()
print(f"Found {candidates['candidates_found']} candidates")
```

## 🔧 Troubleshooting

### Common Issues

1. **Build Fails**
   - Check that all required files are uploaded
   - Verify the Dockerfile is correct
   - Check the logs in the Space settings

2. **API Returns 500 Error**
   - Verify environment variables are set correctly
   - Check API key validity
   - Review the logs for specific error messages

3. **No Candidates Found**
   - Verify SerpAPI key is valid and has quota
   - Check if the search query is too specific
   - Try different locations or job descriptions

### Debugging

1. **Check Build Logs**: Go to Space settings → Build logs
2. **Check Runtime Logs**: Go to Space settings → Runtime logs
3. **Test Locally**: Run `python test_api.py` to verify functionality

## 📊 Monitoring

- **Space Status**: Check the Space homepage for status
- **API Health**: Use the `/health` endpoint
- **Usage**: Monitor API calls in your Space settings

## 🔄 Updates

To update your API:

1. Make changes to your local files
2. Upload the updated files to your Space
3. The Space will automatically rebuild and redeploy

## 🎯 Next Steps

1. **Customize**: Modify the scoring algorithm or search criteria
2. **Enhance**: Add more API endpoints or features
3. **Scale**: Upgrade to paid Hugging Face plan for better performance
4. **Integrate**: Connect with other recruitment tools

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review the Hugging Face Spaces documentation
3. Check the API logs for specific error messages 