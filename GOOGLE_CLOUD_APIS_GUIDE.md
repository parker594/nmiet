# 🗺️ Google Cloud Platform APIs for Military AI Simulation

## Overview
Google Cloud offers **many** mapping and geospatial APIs. Here's exactly which ones you need for your Military AI Simulation Platform and why.

---

## 🎯 **REQUIRED APIS** (Must Enable These)

### 1. **Maps JavaScript API** ⭐ **ESSENTIAL**
**Purpose**: Core 3D map rendering in your browser
```
API Name: Maps JavaScript API
Enable at: https://console.cloud.google.com/apis/library/maps-backend.googleapis.com
Used for: 3D terrain visualization, tactical map display
Cost: $7 per 1,000 map loads (free: $200 credit = ~28k loads)
```

### 2. **Places API** ⭐ **ESSENTIAL**
**Purpose**: Location search, geocoding, military base locations
```
API Name: Places API
Enable at: https://console.cloud.google.com/apis/library/places-backend.googleapis.com
Used for: Finding coordinates, military installations, strategic locations
Cost: $17 per 1,000 requests (free: $200 credit = ~11k requests)
```

### 3. **Geocoding API** ⭐ **ESSENTIAL**
**Purpose**: Convert addresses to coordinates for tactical planning
```
API Name: Geocoding API
Enable at: https://console.cloud.google.com/apis/library/geocoding-backend.googleapis.com
Used for: Address → coordinates, coordinate → address
Cost: $5 per 1,000 requests (free: $200 credit = ~40k requests)
```

### 4. **Directions API** ⭐ **ESSENTIAL**
**Purpose**: Route planning, navigation for military vehicles
```
API Name: Directions API
Enable at: https://console.cloud.google.com/apis/library/directions-backend.googleapis.com
Used for: Optimal route calculation, avoiding obstacles
Cost: $5 per 1,000 requests (free: $200 credit = ~40k requests)
```

---

## 🚀 **RECOMMENDED APIS** (For Advanced Features)

### 5. **Maps Static API** ⭐ **RECOMMENDED**
**Purpose**: Generate static map images for reports
```
API Name: Maps Static API
Enable at: https://console.cloud.google.com/apis/library/static-maps-backend.googleapis.com
Used for: Mission reports, tactical briefings, screenshots
Cost: $2 per 1,000 requests (free: $200 credit = ~100k requests)
```

### 6. **Street View Static API** ⭐ **RECOMMENDED**
**Purpose**: Ground-level reconnaissance views
```
API Name: Street View Static API
Enable at: https://console.cloud.google.com/apis/library/street-view-image-backend.googleapis.com
Used for: Ground-level intelligence, target reconnaissance
Cost: $7 per 1,000 requests (free: $200 credit = ~28k requests)
```

### 7. **Earth Engine API** ⭐ **RECOMMENDED**
**Purpose**: Satellite imagery, terrain analysis
```
API Name: Earth Engine API
Enable at: https://console.cloud.google.com/apis/library/earthengine.googleapis.com
Used for: Historical satellite data, terrain changes, environmental analysis
Cost: Free for research/education, contact for commercial pricing
Special: Requires separate registration at https://earthengine.google.com/
```

---

## 💼 **OPTIONAL APIS** (For Specialized Features)

### 8. **Maps Elevation API**
**Purpose**: Detailed terrain elevation data
```
API Name: Maps Elevation API
Enable at: https://console.cloud.google.com/apis/library/elevation-backend.googleapis.com
Used for: 3D terrain modeling, line-of-sight calculations
Cost: $5 per 1,000 requests
```

### 9. **Distance Matrix API**
**Purpose**: Calculate distances between multiple points
```
API Name: Distance Matrix API
Enable at: https://console.cloud.google.com/apis/library/distance-matrix-backend.googleapis.com
Used for: Multi-target distance calculations, resource optimization
Cost: $10 per 1,000 elements
```

### 10. **Roads API**
**Purpose**: Snap GPS coordinates to roads
```
API Name: Roads API
Enable at: https://console.cloud.google.com/apis/library/roads.googleapis.com
Used for: Accurate vehicle tracking, route validation
Cost: $10 per 1,000 requests
```

---

## 🔧 **STEP-BY-STEP SETUP GUIDE**

### Step 1: Create Google Cloud Project
1. Go to: https://console.cloud.google.com/
2. Click "New Project"
3. Name: "Military-AI-Simulation"
4. Click "Create"

### Step 2: Enable Required APIs
```bash
# Navigate to APIs & Services > Library
# Or use these direct links:

✅ Maps JavaScript API: https://console.cloud.google.com/apis/library/maps-backend.googleapis.com
✅ Places API: https://console.cloud.google.com/apis/library/places-backend.googleapis.com  
✅ Geocoding API: https://console.cloud.google.com/apis/library/geocoding-backend.googleapis.com
✅ Directions API: https://console.cloud.google.com/apis/library/directions-backend.googleapis.com
⭐ Maps Static API: https://console.cloud.google.com/apis/library/static-maps-backend.googleapis.com
⭐ Street View Static API: https://console.cloud.google.com/apis/library/street-view-image-backend.googleapis.com
```

### Step 3: Create API Key
1. Go to: APIs & Services > Credentials
2. Click "Create Credentials" > "API Key"
3. Copy the generated key
4. **IMPORTANT**: Restrict the key immediately!

### Step 4: Secure Your API Key
1. Click "Restrict Key" 
2. **Application restrictions**: Choose one:
   - **HTTP referrers**: Add `localhost:*`, `127.0.0.1:*`, your domain
   - **IP addresses**: Add your server IPs
3. **API restrictions**: Select only the APIs you enabled above
4. Click "Save"

---

## 🔐 **SECURITY BEST PRACTICES**

### Browser vs Server Keys
**For your Military AI Simulation, you need BOTH:**

#### **Browser Key** (for frontend tactical map):
- Restrict to your domains: `localhost:*`, `your-domain.com`
- Enable: Maps JavaScript API, Places API
- Use in: tactical-map.html frontend

#### **Server Key** (for backend operations):
- Restrict to your server IPs
- Enable: Geocoding API, Directions API, Earth Engine API
- Use in: tactical_server.py backend

### Key Restrictions Example:
```javascript
// Frontend Key (restricted to localhost)
GOOGLE_MAPS_API_KEY_FRONTEND=AIza...restricted-to-localhost

// Backend Key (restricted to server operations)  
GOOGLE_MAPS_API_KEY_BACKEND=AIza...restricted-to-server-ip
```

---

## 💰 **COST OPTIMIZATION TIPS**

### Free Tier Strategy ($200/month credit):
- **Maps JavaScript API**: 28,571 map loads
- **Geocoding API**: 40,000 requests  
- **Directions API**: 40,000 requests
- **Places API**: 11,764 requests
- **Total value**: ~$200/month FREE

### Development Best Practices:
1. **Cache API responses** (especially geocoding)
2. **Batch requests** when possible
3. **Use static maps** for reports instead of interactive maps
4. **Implement rate limiting** in your application
5. **Monitor usage** in Google Cloud Console

### Alert Setup:
1. Go to: Billing > Budgets & Alerts
2. Set budget: $50 (safety buffer)
3. Set alerts at: 50%, 90%, 100%

---

## 🛠️ **CONFIGURATION FOR YOUR PROJECT**

### Update Your .env File:
```env
# Google Maps APIs
GOOGLE_MAPS_API_KEY=AIza_your_primary_api_key_here
GOOGLE_MAPS_API_KEY_FRONTEND=AIza_frontend_restricted_key_here
GOOGLE_MAPS_API_KEY_BACKEND=AIza_backend_restricted_key_here

# Google Earth Engine (separate registration required)
GOOGLE_EARTH_ENGINE_KEY=your_earth_engine_key_here
GOOGLE_EARTH_ENGINE_PROJECT=your_gcp_project_id_here

# API Configuration
GOOGLE_MAPS_REGION=US
GOOGLE_MAPS_LANGUAGE=en
```

### In Your Tactical Map (tactical-map.html):
```html
<!-- Use frontend-restricted key -->
<script src="https://maps.googleapis.com/maps/api/js?key=YOUR_FRONTEND_KEY&libraries=places"></script>
```

### In Your Python Backend (tactical_server.py):
```python
# Use backend-restricted key
GOOGLE_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY_BACKEND')
```

---

## 🧪 **TESTING YOUR SETUP**

### Test Script Addition:
Add this to your `test_api_keys.py`:

```python
def test_google_maps_detailed():
    """Test all Google Maps APIs"""
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    
    tests = [
        ("Geocoding", f"https://maps.googleapis.com/maps/api/geocode/json?address=Pentagon&key={api_key}"),
        ("Directions", f"https://maps.googleapis.com/maps/api/directions/json?origin=Pentagon&destination=White+House&key={api_key}"),
        ("Places", f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=military+base&key={api_key}"),
    ]
    
    for name, url in tests:
        response = requests.get(url)
        status = "✅ Working" if response.status_code == 200 else "❌ Failed"
        print(f"{name} API: {status}")
```

---

## 🎯 **RECOMMENDED SETUP FOR YOUR PROJECT**

### **Minimum Viable Product** (Start with these 4):
1. ✅ **Maps JavaScript API** - Core mapping
2. ✅ **Geocoding API** - Address conversion  
3. ✅ **Directions API** - Route planning
4. ✅ **Places API** - Location search

### **Enhanced Features** (Add these next):
5. ⭐ **Maps Static API** - Report generation
6. ⭐ **Earth Engine API** - Satellite imagery

### **Advanced Military Features** (Future expansion):
7. 💼 **Street View Static API** - Ground reconnaissance
8. 💼 **Elevation API** - Terrain analysis
9. 💼 **Distance Matrix API** - Multi-point optimization

---

## 🚨 **COMMON MISTAKES TO AVOID**

1. **Don't use unrestricted API keys** in production
2. **Don't enable unnecessary APIs** (increases costs)
3. **Don't forget to set up billing alerts**
4. **Don't commit API keys to code** (use environment variables)
5. **Don't use the same key for frontend and backend**

---

## 📞 **Next Steps**

1. **Enable the 4 essential APIs** listed above
2. **Create and restrict your API key**
3. **Update your .env file** with the new key
4. **Run your test script** to verify functionality
5. **Launch your tactical server** and test the 3D map

**🎖️ Your Google Cloud APIs are now optimized for military-grade mapping!**