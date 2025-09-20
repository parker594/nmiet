# Military AI Simulation Platform - Deployment Guide

## 🎯 Quick Start

This is a comprehensive military AI simulation platform for tactical operations, autonomous navigation, and threat detection.

### Prerequisites
- Python 3.8+
- Node.js 16+
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/parker594/nmiet.git
cd nmiet
```

### 2. Set Up Python Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Set Up Node.js Dependencies (Optional)
```bash
# Install Node.js dependencies if using frontend tools
npm install
```

### 4. Configure Environment Variables
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your API keys:
# - OPENAI_API_KEY=your_openai_api_key_here
# - GOOGLE_API_KEY=your_google_api_key_here
# - Add other required API keys
```

### 5. Run the Platform
```bash
# Start the main server
python main_server.py

# The server will start on http://localhost:8005
```

## 🚀 Quick Verification

1. **Check if server is running**: Visit `http://localhost:8005`
2. **Test AI endpoints**: The platform should load with military interface
3. **Verify APIs**: Run `python verify_all_apis.py` to check API connectivity

## 📁 Project Structure

```
nmiet/
├── main_server.py          # Main application server
├── frontend/               # Static HTML/CSS/JS files
├── features/               # Modular feature components
│   ├── ai-chat/           # AI conversational interface
│   ├── tactical-map/      # Military tactical mapping
│   └── heat-visualization/ # 3D heat mapping
├── backend/               # API backend services
├── requirements.txt       # Python dependencies
├── package.json          # Node.js dependencies (optional)
├── .env.example          # Environment variables template
└── docs/                 # API guides and documentation
```

## 🔧 API Configuration

### Required API Keys:
1. **OpenAI API** - For AI conversational capabilities
2. **Google APIs** - For mapping and earth engine data
3. **Weather APIs** - For environmental data (optional)

### Setup Guides:
- [API Keys Guide](API_KEYS_GUIDE.md)
- [Google Cloud APIs](GOOGLE_CLOUD_APIS_GUIDE.md)
- [Quick Start APIs](QUICK_START_APIS.md)

## 🎮 Features

- **🤖 AI Command Interface**: Military-grade conversational AI
- **🗺️ Tactical Operations Map**: Real-time tactical mapping
- **📊 3D Heat Visualization**: Advanced threat visualization
- **🚁 Autonomous Navigation**: Vehicle path planning
- **🔍 Threat Detection**: Computer vision-based detection
- **🔒 Secure Authentication**: Military-grade security

## 📱 Usage

1. **Access the Platform**: Open `http://localhost:8005` in your browser
2. **Navigate Features**: Use the military homepage to access different modules
3. **AI Chat**: Interact with military AI for tactical planning
4. **Tactical Maps**: View and plan military operations
5. **3D Visualization**: Analyze threat patterns and terrain

## 🛠️ Development

### Run in Development Mode
```bash
# For auto-reload during development
python main_server.py --debug
```

### Testing
```bash
# Run API tests
python test_ai_endpoints.py

# Test specific features
python test_openai_only.py
python test_google_ai.py
```

## 🔐 Security

- All API keys should be stored in `.env` file (never commit this file)
- Use HTTPS in production
- Implement proper authentication for production deployment
- Follow military-grade security practices

## 📚 Documentation

- [Pipeline Guide](PIPELINE_GUIDE.md) - Development workflow
- [API Documentation](API_KEYS_GUIDE.md) - API integration guide
- [Google Cloud Setup](GOOGLE_CLOUD_APIS_GUIDE.md) - Cloud services

## 🚀 Production Deployment

For production deployment:
1. Use environment variables for all sensitive configuration
2. Set up proper logging and monitoring
3. Implement SSL/TLS certificates
4. Use production-grade database
5. Set up load balancing for high availability

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit with descriptive messages
5. Push and create a pull request

## 📄 License

This project is developed for educational and research purposes in military simulation technology.

## 🆘 Troubleshooting

### Common Issues:

1. **Port 8005 already in use**:
   ```bash
   # Kill existing process
   netstat -ano | findstr :8005
   taskkill /PID <process_id> /F
   ```

2. **API Key errors**:
   - Verify `.env` file exists and contains valid API keys
   - Run `python verify_all_apis.py` to test connections

3. **Module import errors**:
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt` again

4. **Permission errors**:
   - Run as administrator if needed
   - Check file permissions

For additional support, check the documentation files or create an issue on GitHub.