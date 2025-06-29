# LinkedIn Sourcing Agent

An AI-powered LinkedIn candidate sourcing and outreach generation tool that helps recruiters find and engage with top talent.

## Features

- **Smart Candidate Search**: Uses SerpAPI to find relevant LinkedIn profiles
- **AI-Powered Scoring**: Multi-factor candidate evaluation (education, experience, skills, location, etc.)
- **Personalized Outreach**: Generates customized outreach messages highlighting key characteristics
- **Interactive CLI**: User-friendly command-line interface for job descriptions
- **JSON Output**: Structured results with detailed candidate information
- **FastAPI Backend**: REST API for integration with other systems

## Requirements

- Python 3.8+
- SerpAPI key (for LinkedIn profile search)
- RapidAPI key (for detailed profile data)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/linkedin-sourcing-agent.git
   cd linkedin-sourcing-agent
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root:
   ```
   SERPAPI_API_KEY=your_serpapi_key_here
   RAPIDAPI_KEY=your_rapidapi_key_here
   ```

## Usage

### Command Line Interface

Run the interactive CLI:
```bash
python main.py
```

The tool will prompt you for:
- Job description (multi-line input)
- Location (default: Mountain View)
- Number of candidates (default: 10)

### FastAPI Backend

Start the API server:
```bash
python api.py
```

Access the API at:
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Sourcing Endpoint**: POST http://localhost:8000/sourcing

### API Example

```bash
curl -X POST "http://localhost:8000/sourcing" \
  -H "Content-Type: application/json" \
  -d '{
    "job_description": "Senior ML Engineer with LLM experience",
    "location": "Mountain View",
    "num_candidates": 5
  }'
```

## Scoring System

The tool evaluates candidates across 6 key dimensions:

1. **Education** (0-10): Top-tier schools get higher scores
2. **Career Trajectory** (0-10): Based on number of roles and progression
3. **Company Prestige** (0-10): Experience at top tech companies
4. **Skills Match** (0-10): AI/ML keyword matching
5. **Location** (0-10): Bay Area preference
6. **Tenure** (0-10): Average job duration

## Project Structure

```
linkedin-sourcing-agent/
├── main.py              # Interactive CLI application
├── api.py               # FastAPI server
├── app.py               # Hugging Face Spaces deployment
├── search.py            # LinkedIn profile search
├── score.py             # Candidate scoring logic
├── outreach.py          # Outreach message generation
├── fetch_profile.py     # LinkedIn profile data fetching
├── requirements.txt     # Python dependencies
├── requirements_api.txt # API-specific dependencies
├── Dockerfile           # Docker configuration
├── README.md           # This file
└── .env                # Environment variables (not in repo)
```

## 🔧 Configuration

### API Keys

1. **SerpAPI**: Sign up at https://serpapi.com/ for LinkedIn search
2. **RapidAPI**: Sign up at https://rapidapi.com/ and subscribe to "Fresh LinkedIn Profile Data"

### Customization

- **Scoring Weights**: Modify weights in `score.py`
- **Search Keywords**: Update `COMMON_AI_KEYWORDS` in `search.py`
- **Top Schools**: Edit `TOP_SCHOOLS` and `MID_TIER_SCHOOLS` in `score.py`

## Deployment

### Hugging Face Spaces

1. Create a new Space on Hugging Face
2. Choose "Docker" as the SDK
3. Upload all files to the Space
4. Set environment variables in Space settings
5. Deploy

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run CLI version
python main.py

# Run API version
python api.py
```

## Output Format

The tool generates structured JSON output:

```json
{
  "job_id": "job-123456",
  "candidates_found": 25,
  "top_candidates": [
    {
      "name": "Jane Smith",
      "linkedin_url": "https://linkedin.com/in/janesmith",
      "fit_score": 8.5,
      "score_breakdown": {
        "education": 9.0,
        "trajectory": 8.0,
        "company": 8.5,
        "skills": 9.0,
        "location": 10.0,
        "tenure": 7.0
      },
      "outreach_message": "Personalized message...",
      "key_characteristics": [
        "Graduated from Stanford University",
        "Experience at Google",
        "Strong AI/ML background"
      ]
    }
  ]
}
```

## Important Notes

- **API Rate Limits**: Be aware of SerpAPI and RapidAPI rate limits
- **LinkedIn Terms**: This tool respects LinkedIn's terms of service
- **Data Privacy**: Handle candidate data responsibly
- **API Costs**: Monitor your API usage and costs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter issues:
1. Check the troubleshooting section in the documentation
2. Verify your API keys are correct
3. Check API rate limits and quotas
4. Open an issue on GitHub

## Links

- [SerpAPI Documentation](https://serpapi.com/docs)
- [RapidAPI Fresh LinkedIn Profile Data](https://rapidapi.com/letscrape-6bRBa3QguO5/api/fresh-linkedin-profile-data/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/) 