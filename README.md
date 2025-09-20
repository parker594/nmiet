# Military AI Simulation Platform

A comprehensive military AI simulation platform combining autonomous navigation, threat detection, swarm intelligence, and real-time 3D visualization for hackathon demonstration.

## 🚀 Features

### Core AI Capabilities
- **Autonomous Navigation**: Deep Q-Network based navigation with prioritized experience replay
- **Threat Detection**: Computer vision-based threat identification using YOLO and custom models
- **Swarm Intelligence**: Multi-agent coordination with formation control and consensus algorithms
- **Real-time Decision Making**: Military-grade AI systems with confidence scoring

### Visualization & Interface
- **3D Visualization**: Three.js based real-time terrain and agent rendering
- **Command Dashboard**: Military-style control interface with tactical displays
- **Real-time Monitoring**: WebSocket-based live updates and alerts
- **Multi-view Support**: Tactical, satellite, thermal, and surveillance views

### Security & Integration
- **Military-grade Authentication**: JWT with role-based access control
- **API Integration**: Google Earth Engine, OpenStreetMap, Weather APIs
- **Encrypted Communication**: Secure WebSocket and REST API endpoints
- **Audit Logging**: Comprehensive activity tracking and monitoring

## 📁 Project Structure

```
military-ai-simulation/
├── ai-models/                          # AI/ML Components
│   ├── navigation/
│   │   └── autonomous_navigation.py    # DQN-based navigation system
│   ├── threat-detection/
│   │   └── threat_detection.py         # Computer vision threat detection
│   └── swarm-intelligence/
│       └── swarm_coordinator.py        # Multi-agent coordination
├── backend/                            # Node.js Backend
│   ├── src/
│   │   ├── middleware/
│   │   │   └── auth.js                 # Authentication middleware
│   │   ├── models/
│   │   │   └── User.js                 # User model with military ranks
│   │   └── services/
│   │       └── api_integration.py      # External API integration
│   ├── server.js                       # Main Express server
│   └── package.json                    # Dependencies
├── frontend/                           # Frontend Interface
│   ├── dashboard.html                  # Main command dashboard
│   └── 3d-visualization.html          # 3D terrain visualization
├── main_server.py                      # FastAPI integration server
├── requirements.txt                    # Python dependencies
└── README.md                           # This file
```

## 🛠️ Technology Stack

### Backend
- **Node.js** with Express.js framework
- **MongoDB** for data persistence
- **Socket.io** for real-time communication
- **FastAPI** for AI model integration
- **JWT** authentication with bcrypt encryption

### AI/ML
- **Python 3.8+** with PyTorch/TensorFlow
- **OpenCV** for computer vision
- **YOLO** for object detection
- **NumPy/SciPy** for mathematical operations
- **OpenAI Gym** for reinforcement learning

### Frontend
- **HTML5/CSS3/JavaScript**
- **Three.js** for 3D visualization
- **WebSocket** for real-time updates
- **Canvas API** for tactical displays

### External APIs
- **Google Earth Engine** for satellite imagery
- **OpenStreetMap** for mapping data
- **OpenWeatherMap** for weather conditions
- **NASA APIs** for enhanced terrain data

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ and npm
- Python 3.8+
- MongoDB (local or cloud)
- Git

### 1. Clone Repository
```bash
git clone <repository-url>
cd military-ai-simulation
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install Node.js Dependencies
```bash
cd backend
npm install
cd ..
```

### 4. Environment Configuration
Create `.env` file in project root:
```env
# Database
MONGODB_URI=mongodb://localhost:27017/military_ai_sim

# Authentication
JWT_SECRET=your_super_secure_jwt_secret_key_here
BCRYPT_ROUNDS=12

# API Keys (Optional - for full functionality)
OPENWEATHER_API_KEY=your_openweather_api_key
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
NASA_API_KEY=your_nasa_api_key
GEE_SERVICE_ACCOUNT_KEY=your_earth_engine_key

# Server Configuration
PORT=8000
NODE_ENV=development
```

### 5. Start the Simulation
```bash
# Start MongoDB (if local)
mongod

# Start the integrated server
python main_server.py
```

### 6. Access the Interface
- **Command Dashboard**: http://localhost:8000/static/dashboard.html
- **3D Visualization**: http://localhost:8000/static/3d-visualization.html
- **API Documentation**: http://localhost:8000/docs

## 🎮 Usage Guide

### Command Dashboard
1. **Mission Control**: Select operation type and formation
2. **Agent Deployment**: Configure and deploy AI agents
3. **Threat Detection**: Monitor and respond to threats
4. **Real-time Status**: View system metrics and logs

### 3D Visualization
1. **Camera Controls**: Mouse to orbit, zoom, and pan
2. **Agent Tracking**: Real-time agent movement and status
3. **Formation Control**: Dynamic formation changes
4. **Threat Visualization**: Visual threat indicators

### API Endpoints

#### System Status
```bash
GET /api/status
```

#### Start Mission
```bash
POST /api/mission/start
Content-Type: application/json

{
  "type": "patrol",
  "formation": "wedge",
  "coordinates": {"lat": 35.0844, "lon": -106.6504},
  "agent_count": 10,
  "priority": "high"
}
```

#### Deploy Agents
```bash
POST /api/agents/deploy
Content-Type: application/json

{
  "count": 15,
  "formation": "line",
  "coordinates": {"lat": 35.0844, "lon": -106.6504}
}
```

### WebSocket Communication
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

// Send ping
ws.send(JSON.stringify({type: 'ping'}));

// Request status update
ws.send(JSON.stringify({type: 'request_status'}));

// Emergency stop
ws.send(JSON.stringify({type: 'emergency_stop'}));
```

## 🎯 Demo Instructions

### For Hackathon Judges
1. **Start the system**: `python main_server.py`
2. **Open dashboard**: Navigate to command interface
3. **Deploy agents**: Use the control panel to deploy 15 agents
4. **Start mission**: Select "reconnaissance" with "wedge" formation
5. **Monitor real-time**: Watch 3D visualization and threat detection
6. **Emergency features**: Test abort mission and emergency stop

### Key Demonstration Points
- **AI Decision Making**: Show autonomous navigation with obstacle avoidance
- **Threat Response**: Demonstrate real-time threat detection and agent response
- **Formation Control**: Display dynamic formation changes and coordination
- **Command Interface**: Highlight military-grade security and control systems
- **Real-time Communication**: Show WebSocket updates and live monitoring

## 🏆 Hackathon Highlights

### Innovation
- **Advanced AI**: Deep Q-Network navigation with military decision-making
- **Real-time Coordination**: Multi-agent swarm intelligence with formation control
- **Comprehensive Security**: Military-grade authentication and encryption
- **Full-stack Integration**: Seamless connection of AI, backend, and frontend

### Technical Excellence
- **Scalable Architecture**: Modular design supporting multiple deployment scenarios
- **Performance Optimization**: GPU acceleration and efficient algorithms
- **Production Ready**: Comprehensive error handling and monitoring
- **API Integration**: External data sources for enhanced realism

### Impact Potential
- **Defense Applications**: Direct applicability to military operations
- **Research Value**: Advanced AI algorithms for autonomous systems
- **Commercial Viability**: Adaptable to civilian applications
- **Educational Use**: Platform for AI and robotics research

---

**Built for hackathon demonstration - showcasing advanced military AI simulation capabilities with real-time coordination and visualization.**
- **Secure Access**: Military-grade encryption and authentication
- **API Integration**: Google Earth Engine, OpenStreetMap, weather data

## 🛠️ Technology Stack
- **Backend**: Node.js, Express, MongoDB
- **AI Models**: Python, TensorFlow, PyTorch, OpenAI Gym
- **Frontend**: HTML5, CSS3, JavaScript, Three.js
- **APIs**: Google Earth Engine, OpenStreetMap, Weather APIs
- **Security**: JWT, bcrypt, military-grade encryption

## 📦 Installation

### Prerequisites
- Node.js (v16+)
- Python (v3.8+)
- MongoDB
- Git

### Setup
```bash
# Clone repository
git clone <repository-url>
cd military-ai-simulation

# Install dependencies
npm run install-all

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Start the application
npm run dev
```

## 🔧 Configuration
1. Get API keys from:
   - Google Earth Engine
   - OpenWeatherMap
   - OpenStreetMap Nominatim
2. Configure MongoDB connection
3. Set up JWT secrets
4. Configure encryption keys

## 🎮 Usage
1. Start the backend server: `npm run dev`
2. Access dashboard: `http://localhost:3000`
3. Login with commander credentials
4. Deploy AI agents and monitor missions

## 📁 Project Structure
```
military-ai-simulation/
├── backend/              # Express.js API server
├── ai-models/           # Python AI/ML models
├── frontend/            # HTML/CSS/JS dashboard
├── data/               # Terrain and satellite data
├── scripts/            # Build and deployment scripts
└── docs/              # Documentation
```

## 🔐 Security Features
- Role-based access control
- End-to-end encryption
- Secure API authentication
- Audit logging
- Session management

## 🤖 AI Models
- **Navigation**: Reinforcement learning for autonomous pathfinding
- **Vision**: YOLO-based object detection and tracking
- **Swarm**: Multi-agent coordination algorithms
- **Prediction**: Threat assessment and risk analysis

## 🌍 API Integrations
- Google Earth Engine for satellite imagery
- OpenStreetMap for mapping data
- Weather APIs for environmental conditions
- Terrain elevation services

## 📊 Real-time Analytics
- Agent status monitoring
- Mission progress tracking
- Threat level assessment
- Resource utilization metrics

## 🏆 Hackathon Ready
- Complete prototype implementation
- Demo scenarios included
- Presentation materials
- Live demonstration capabilities

## 📝 License
MIT License - see LICENSE file for details

## 👥 Team
Military AI Simulation Development Team