# Content Repurposing Pipeline - CSAI 422 Assignment 5

A modular workflow for transforming blog content into multiple formats using LLM technology.

## Core Features
- **Key Point Extraction** - Identifies main ideas from source articles
- **Automated Summarization** - Generates concise overviews using LLMs
- **Multi-Platform Content Creation**:
  - Twitter/X posts
  - LinkedIn updates
  - Facebook content
- **Email Newsletter Generation** - Formats ready-to-use email campaigns

---

## Installation Guide

### 1. Clone the Project
2. Install Requirements
Prerequisites:

Python 3.10 or later

Install dependencies:

bash
Copy
pip install -r requirements.txt
3. Configure API Access
Create .env file with:

ini
Copy
# Primary LLM Provider (NGU)
NGU_API_KEY="your_ngu_api_key"
NGU_BASE_URL="https://ngullama.femtoid.com/v1"
NGU_MODEL="qwen2.5-coder:7b"

# Alternative Provider (Groq)
GROQ_API_KEY="your_groq_api_key"
GROQ_BASE_URL="https://api.groq.com/openai/v1"
GROQ_MODEL="llama-3.3-70b-versatile"

# Runtime Configuration
MODEL_SERVER="NGU"
4. Execute the Pipeline
bash
Copy
python llm_workflow.py
Workflow Process
Input: Reads from sample-blog-post.json

Analysis: Extracts core concepts via LLM API

Content Generation:

Creates summary

Produces platform-optimized social posts

Formats email newsletter

Sample Output
json
Copy
{
  "analysis": {
    "key_points": [
      "AI improves diagnostic accuracy",
      "AI accelerates drug discovery"
    ],
    "summary": "AI technologies are transforming healthcare through enhanced diagnostics and pharmaceutical research."
  },
  "social_content": {
    "twitter": "Healthcare revolution! AI is changing diagnostics and drug development. #AI #MedTech",
    "linkedin": "How artificial intelligence is advancing medical diagnostics and treatment development.",
    "facebook": "Discover the groundbreaking impact of AI on modern healthcare systems!"
  },
  "email": {
    "subject": "The AI Healthcare Revolution",
    "body": "Artificial intelligence is reshaping medicine... (continued)"
  }
}
