# 🔑 Military AI Simulation Platform - API Keys Guide

## Overview
This guide provides step-by-step instructions to obtain all necessary API keys for the Military AI Simulation Platform. Each API key serves specific functions in our tactical intelligence system.

---

## 🤖 AI Model APIs

### 1. OpenAI API (GPT-4 for Tactical Analysis)
**Purpose**: Advanced tactical analysis, enemy behavior prediction, mission planning

**Steps to Get API Key**:
1. Visit: https://platform.openai.com/
2. Click "Sign Up" or "Log In"
3. Complete account verification (phone number required)
4. Go to "API Keys" section: https://platform.openai.com/api-keys
5. Click "Create new secret key"
6. Name it "Military-AI-Simulation"
7. Copy the key (starts with `sk-...`)

**Pricing**: $0.03 per 1K tokens (GPT-4)
**Free Tier**: $5 credit for new accounts

---

### 2. Google AI Studio (Gemini Pro)
**Purpose**: Multi-modal AI analysis, image recognition, strategic planning

**Steps to Get API Key**:
1. Visit: https://aistudio.google.com/
2. Sign in with Google account
3. Click "Get API key" in the top right
4. Select or create a Google Cloud project
5. Click "Create API key in existing project"
6. Copy the generated key

**Pricing**: Free tier: 60 requests/minute
**Cost**: $0.0015 per 1K characters

---

### 3. Hugging Face API
**Purpose**: Open-source models, computer vision, NLP tasks

**Steps to Get API Key**:
1. Visit: https://huggingface.co/
2. Click "Sign Up" (top right)
3. Verify email address
4. Go to Settings: https://huggingface.co/settings/tokens
5. Click "New token"
6. Name: "Military-AI-Simulation"
7. Set role to "read" or "write" (recommended: write)
8. Copy the token (starts with `hf_...`)

**Pricing**: Free tier available
**Cost**: Pay per inference for premium models

---

### 4. Azure Cognitive Services
**Purpose**: Computer vision, speech recognition, translation

**Steps to Get API Key**:
1. Visit: https://portal.azure.com/
2. Sign up for Azure account (credit card required, but free tier available)
3. Search for "Cognitive Services" in the search bar
4. Click "Create" → "Cognitive Services"
5. Fill in:
   - Resource group: Create new "military-ai-rg"
   - Region: Choose closest to you
   - Name: "military-ai-cognitive"
   - Pricing tier: F0 (free) or S0 (standard)
6. After deployment, go to resource
7. Click "Keys and Endpoint" in left menu
8. Copy Key 1 and Endpoint URL

**Free Tier**: 20 transactions/month for most services

---

### 5. AWS AI Services (Optional)
**Purpose**: Advanced ML models, Rekognition, Comprehend

**Steps to Get API Key**:
1. Visit: https://aws.amazon.com/
2. Click "Create an AWS Account"
3. Complete registration (credit card required)
4. Go to IAM Console: https://console.aws.amazon.com/iam/
5. Create new user:
   - Username: "military-ai-user"
   - Access type: Programmatic access
   - Attach policies: AmazonRekognitionFullAccess, ComprehendFullAccess
6. Download the CSV with Access Key ID and Secret Access Key

**Free Tier**: 12 months free tier for new accounts

---

## 🗺️ Mapping & Geospatial APIs

### 6. Google Maps Platform
**Purpose**: 3D terrain, satellite imagery, geocoding, routing

**Steps to Get API Key**:
1. Visit: https://console.cloud.google.com/
2. Create new project or select existing
3. Enable APIs:
   - Maps JavaScript API
   - Places API
   - Geocoding API
   - Directions API
   - Earth Engine API
4. Go to "Credentials" → "Create Credentials" → "API Key"
5. Restrict the key:
   - Application restrictions: HTTP referrers
   - API restrictions: Select the enabled APIs above
6. Copy the API key

**Free Tier**: $200 credit per month
**Pricing**: $7 per 1000 map loads

---

### 7. Mapbox API
**Purpose**: Custom 3D maps, terrain visualization, routing

**Steps to Get API Key**:
1. Visit: https://www.mapbox.com/
2. Click "Sign up"
3. Complete registration
4. Go to Account page: https://account.mapbox.com/
5. Scroll to "Access tokens"
6. Copy the default public token or create new token
7. For server-side: Create secret token with appropriate scopes

**Free Tier**: 50,000 map views/month
**Pricing**: $5 per 1000 map views after free tier

---

### 8. OpenStreetMap Nominatim (Free)
**Purpose**: Geocoding, reverse geocoding, address lookup

**Steps to Get API Access**:
1. No API key required for basic usage
2. For heavy usage, consider:
   - Self-hosting Nominatim
   - Using commercial providers like MapQuest
3. Respect usage policy: 1 request/second max

**Cost**: Free (with usage limits)

---

### 9. NASA APIs
**Purpose**: Satellite imagery, weather data, earth observation

**Steps to Get API Key**:
1. Visit: https://api.nasa.gov/
2. Fill in the form:
   - First Name, Last Name
   - Email address
   - Use Description: "Military AI Simulation for educational purposes"
3. Submit form
4. Check email for API key
5. API key will be in format: `DEMO_KEY` initially, then your personal key

**Cost**: Free with rate limits (1000 requests/hour)

---

### 10. Planet Labs (Satellite Imagery)
**Purpose**: High-resolution satellite imagery

**Steps to Get API Key**:
1. Visit: https://www.planet.com/
2. Sign up for Developer account
3. Complete verification process
4. Go to Account Settings → API Keys
5. Generate new API key
6. Educational discounts available

**Cost**: Paid service, contact for pricing

---

## 🌤️ Weather APIs

### 11. OpenWeatherMap
**Purpose**: Real-time weather, forecasts, historical data

**Steps to Get API Key**:
1. Visit: https://openweathermap.org/api
2. Click "Sign Up"
3. Complete registration and email verification
4. Go to API Keys tab: https://home.openweathermap.org/api_keys
5. Copy the default API key or create new one
6. Name: "Military-AI-Weather"

**Free Tier**: 1000 calls/day
**Pricing**: $40/month for 100,000 calls/month

---

### 12. AccuWeather API
**Purpose**: Detailed weather forecasts, severe weather alerts

**Steps to Get API Key**:
1. Visit: https://developer.accuweather.com/
2. Register for free account
3. Verify email address
4. Create new app:
   - App Name: "Military AI Simulation"
   - Description: "Weather integration for tactical planning"
5. Copy the API key from your app dashboard

**Free Tier**: 50 calls/day
**Pricing**: Various plans starting at $25/month

---

### 13. Weather.gov API (US Only - Free)
**Purpose**: National Weather Service data

**Steps to Get API Access**:
1. No API key required
2. Visit: https://www.weather.gov/documentation/services-web-api
3. Use endpoints directly with proper User-Agent header
4. Format: `User-Agent: (myweatherapp.com, contact@myweatherapp.com)`

**Cost**: Free (US government service)

---

## 🛡️ Security & Authentication APIs

### 14. Auth0 (Optional)
**Purpose**: Advanced authentication, user management

**Steps to Get API Key**:
1. Visit: https://auth0.com/
2. Sign up for free account
3. Create new application:
   - Name: "Military AI Simulation"
   - Type: Single Page Application
4. Go to Settings tab
5. Copy Domain, Client ID, and Client Secret
6. Configure callback URLs

**Free Tier**: 7000 active users
**Pricing**: $23/month per 1000 active users

---

## 🔧 Setup Instructions

### Step 1: Create .env File
Copy your `.env.example` to `.env` and fill in the obtained API keys:

```bash
cp .env.example .env
```

### Step 2: Fill in API Keys
Edit the `.env` file with your obtained keys:

```env
# AI Model APIs
OPENAI_API_KEY=sk-your-openai-key-here
GOOGLE_AI_API_KEY=your-google-ai-key-here
HUGGINGFACE_API_KEY=hf_your-huggingface-key-here
AZURE_COGNITIVE_KEY=your-azure-key-here
AZURE_COGNITIVE_ENDPOINT=https://your-region.cognitiveservices.azure.com/

# Mapping APIs
GOOGLE_MAPS_API_KEY=your-google-maps-key-here
MAPBOX_ACCESS_TOKEN=pk.your-mapbox-token-here
NASA_API_KEY=your-nasa-api-key-here

# Weather APIs
OPENWEATHER_API_KEY=your-openweather-key-here
ACCUWEATHER_API_KEY=your-accuweather-key-here

# Optional
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AUTH0_DOMAIN=your-auth0-domain.auth0.com
AUTH0_CLIENT_ID=your-auth0-client-id
```

### Step 3: Test API Keys
Run the test script to verify all keys are working:

```bash
python test_api_keys.py
```

---

## 💰 Cost Estimation

### Free Tier Only (Recommended for Development):
- **Total Cost**: $0/month
- **Limitations**: Rate limits, fewer features
- **Suitable for**: Development, testing, small demos

### Basic Production Setup:
- **OpenAI**: $20-50/month
- **Google Maps**: $50-100/month
- **Weather APIs**: $40-65/month
- **Azure Cognitive**: $30-60/month
- **Total**: ~$140-275/month

### Full Enterprise Setup:
- **All APIs with high limits**: $500-1000/month
- **Suitable for**: Production deployment, high traffic

---

## 🔒 Security Best Practices

1. **Never commit API keys to version control**
2. **Use environment variables only**
3. **Rotate keys regularly (monthly)**
4. **Set up billing alerts for paid APIs**
5. **Restrict API keys by domain/IP when possible**
6. **Monitor API usage regularly**
7. **Use separate keys for development/production**

---

## 📞 Support & Troubleshooting

### Common Issues:

1. **"API key invalid"**
   - Verify the key is copied correctly
   - Check if the API service is enabled
   - Ensure billing is set up for paid services

2. **"Rate limit exceeded"**
   - Check your usage against the API limits
   - Consider upgrading to paid tier
   - Implement request throttling

3. **"CORS errors"**
   - Configure proper domain restrictions
   - Use server-side requests for sensitive keys

### Getting Help:
- **OpenAI**: https://help.openai.com/
- **Google**: https://cloud.google.com/support
- **Azure**: https://docs.microsoft.com/en-us/azure/cognitive-services/
- **GitHub Issues**: Create issue in this repository

---

## 🎯 Priority APIs for Quick Start

If you want to start quickly, get these APIs first:

1. **OpenAI API** - Core AI functionality
2. **Google Maps API** - 3D visualization
3. **OpenWeatherMap API** - Weather data
4. **NASA API** - Satellite imagery (free)
5. **Hugging Face API** - Additional AI models

The rest can be added later as needed.

---

## 📝 Next Steps

1. Obtain the priority API keys listed above
2. Update your `.env` file
3. Run the test script to verify functionality
4. Start with basic features and gradually add more APIs
5. Monitor usage and upgrade plans as needed

---

**🎖️ Ready for deployment? Your Military AI Simulation Platform awaits your API keys!**