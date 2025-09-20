# 🚀 Quick Start API Guide - Priority Order

## ⚡ Essential APIs for Basic Functionality (Get These First!)

### 1. 🤖 OpenAI API - **HIGHEST PRIORITY**
- **Purpose**: Core AI tactical analysis and decision making
- **Free Tier**: $5 credit for new accounts
- **Get It**: https://platform.openai.com/api-keys
- **Why Essential**: Powers the main AI brain of your simulation

### 2. 🗺️ Google Maps API - **HIGHEST PRIORITY**  
- **Purpose**: 3D terrain visualization and mapping
- **Free Tier**: $200 credit monthly
- **Get It**: https://console.cloud.google.com/
- **Why Essential**: Required for the 3D tactical map display

### 3. 🌤️ OpenWeatherMap API - **HIGH PRIORITY**
- **Purpose**: Real-time weather data for tactical planning
- **Free Tier**: 1000 calls/day
- **Get It**: https://openweathermap.org/api
- **Why Essential**: Weather affects military operations

### 4. 🤗 Hugging Face API - **HIGH PRIORITY**
- **Purpose**: Additional AI models and computer vision
- **Free Tier**: Available with rate limits
- **Get It**: https://huggingface.co/settings/tokens
- **Why Essential**: Backup AI models and specialized tasks

---

## 🔥 Recommended for Full Features

### 5. 🧠 Google AI (Gemini) - **MEDIUM PRIORITY**
- **Purpose**: Advanced multimodal AI analysis
- **Free Tier**: 60 requests/minute
- **Get It**: https://aistudio.google.com/
- **Why Useful**: Enhanced AI capabilities

### 6. 🚀 NASA API - **MEDIUM PRIORITY**
- **Purpose**: Satellite imagery and earth data
- **Free Tier**: Completely free (use DEMO_KEY)
- **Get It**: https://api.nasa.gov/
- **Why Useful**: Free satellite data

### 7. 🗺️ Mapbox API - **MEDIUM PRIORITY**
- **Purpose**: Alternative mapping with better 3D terrain
- **Free Tier**: 50,000 views/month
- **Get It**: https://account.mapbox.com/
- **Why Useful**: Better terrain visualization

---

## 💼 Professional Features (Optional)

### 8. 🧠 Azure Cognitive Services - **LOW PRIORITY**
- **Purpose**: Enterprise-grade AI services
- **Free Tier**: Limited free transactions
- **Get It**: https://portal.azure.com/
- **Why Optional**: Advanced features for production

### 9. ☁️ AWS AI Services - **LOW PRIORITY**
- **Purpose**: Additional cloud AI capabilities
- **Free Tier**: 12 months for new accounts
- **Get It**: https://aws.amazon.com/
- **Why Optional**: Enterprise scaling

---

## 🎯 Quick Setup Steps

### Step 1: Get Essential APIs (15 minutes)
```bash
1. OpenAI API     → https://platform.openai.com/api-keys
2. Google Maps    → https://console.cloud.google.com/
3. OpenWeather    → https://openweathermap.org/api
4. Hugging Face   → https://huggingface.co/settings/tokens
```

### Step 2: Run Setup Script
```bash
python setup_env.py
```

### Step 3: Test Your APIs
```bash
python test_api_keys.py
```

### Step 4: Start the Simulation
```bash
python tactical_server.py
```

### Step 5: Open Tactical Map
```
http://localhost:8000/tactical-map
```

---

## 💰 Cost Breakdown for Development

### Free Tier Only (Recommended for Testing):
- **OpenAI**: $5 free credit (lasts ~1-2 weeks of testing)
- **Google Maps**: $200 free monthly (plenty for development)
- **OpenWeather**: 1000 calls/day (sufficient for demos)
- **Hugging Face**: Free with rate limits
- **NASA**: Completely free
- **Total Cost**: $0/month (after free credits)

### Minimal Paid Setup ($20-30/month):
- **OpenAI**: $20/month for regular usage
- **Google Maps**: Usually stays within free tier
- **OpenWeather**: Free tier sufficient
- **Others**: Free tiers
- **Total**: ~$20-30/month

---

## 🔧 Troubleshooting Quick Fixes

### "API Key Invalid" Error:
1. Check if you copied the full key (no spaces)
2. Verify the API service is enabled in your dashboard
3. Make sure billing is set up for paid services

### "Rate Limit Exceeded":
1. Wait a few minutes and try again
2. Check your usage in the API dashboard
3. Consider upgrading to paid tier

### "CORS Error" in Browser:
1. Use the tactical_server.py backend (not direct browser calls)
2. Check domain restrictions in API settings

---

## 🎖️ Success Indicators

You'll know everything is working when:
- ✅ `python test_api_keys.py` shows all green checkmarks
- ✅ Tactical server starts without errors
- ✅ 3D map loads at http://localhost:8000/tactical-map
- ✅ Heat signatures appear on the map
- ✅ Weather data updates in real-time
- ✅ AI provides tactical recommendations

---

## 📞 Get Help

- **Check the full guide**: `API_KEYS_GUIDE.md`
- **Run diagnostics**: `python test_api_keys.py`
- **Setup environment**: `python setup_env.py`
- **Start fresh**: Delete `.env` file and run setup again

**🎯 Ready to deploy your Military AI Simulation Platform!**