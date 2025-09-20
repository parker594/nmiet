const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const socketIo = require('socket.io');
const http = require('http');
require('dotenv').config();

// Import routes
const authRoutes = require('./src/routes/auth');
const simulationRoutes = require('./src/routes/simulation');
const agentRoutes = require('./src/routes/agents');
const missionRoutes = require('./src/routes/missions');
const aiRoutes = require('./src/routes/ai');
const dataRoutes = require('./src/routes/data');

// Import middleware
const authMiddleware = require('./src/middleware/auth');
const errorHandler = require('./src/middleware/errorHandler');
const logger = require('./src/config/logger');

const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
  cors: {
    origin: process.env.FRONTEND_URL || "http://localhost:3000",
    methods: ["GET", "POST"]
  }
});

// Security middleware
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'unsafe-inline'", "https://cdnjs.cloudflare.com"],
      styleSrc: ["'self'", "'unsafe-inline'", "https://cdnjs.cloudflare.com"],
      imgSrc: ["'self'", "data:", "https:"],
    },
  },
}));

app.use(cors({
  origin: process.env.FRONTEND_URL || "http://localhost:3000",
  credentials: true
}));

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});
app.use(limiter);

// Body parsing middleware
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Serve static files
app.use(express.static('frontend/public'));

// Database connection
mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/military-ai-sim', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
})
.then(() => logger.info('Connected to MongoDB'))
.catch(err => logger.error('MongoDB connection error:', err));

// Routes
app.use('/api/auth', authRoutes);
app.use('/api/simulation', authMiddleware, simulationRoutes);
app.use('/api/agents', authMiddleware, agentRoutes);
app.use('/api/missions', authMiddleware, missionRoutes);
app.use('/api/ai', authMiddleware, aiRoutes);
app.use('/api/data', authMiddleware, dataRoutes);

// Serve frontend
app.get('/', (req, res) => {
  res.sendFile(__dirname + '/frontend/views/index.html');
});

app.get('/dashboard', authMiddleware, (req, res) => {
  res.sendFile(__dirname + '/frontend/views/dashboard.html');
});

app.get('/simulation', authMiddleware, (req, res) => {
  res.sendFile(__dirname + '/frontend/views/simulation.html');
});

// Health check
app.get('/health', (req, res) => {
  res.json({ 
    status: 'OK', 
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    memory: process.memoryUsage()
  });
});

// Socket.IO for real-time communication
io.use((socket, next) => {
  // Add socket authentication here
  next();
});

io.on('connection', (socket) => {
  logger.info('Client connected:', socket.id);
  
  socket.on('join-simulation', (simulationId) => {
    socket.join(`simulation-${simulationId}`);
    logger.info(`Socket ${socket.id} joined simulation ${simulationId}`);
  });
  
  socket.on('agent-update', (data) => {
    socket.to(`simulation-${data.simulationId}`).emit('agent-status', data);
  });
  
  socket.on('mission-command', (data) => {
    socket.to(`simulation-${data.simulationId}`).emit('new-command', data);
  });
  
  socket.on('disconnect', () => {
    logger.info('Client disconnected:', socket.id);
  });
});

// Global error handler
app.use(errorHandler);

// Handle 404
app.use('*', (req, res) => {
  res.status(404).json({ message: 'Route not found' });
});

const PORT = process.env.PORT || 3000;

server.listen(PORT, () => {
  logger.info(`Military AI Simulation Server running on port ${PORT}`);
  console.log(`🚀 Server running at http://localhost:${PORT}`);
  console.log(`📊 Dashboard: http://localhost:${PORT}/dashboard`);
  console.log(`🎮 Simulation: http://localhost:${PORT}/simulation`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  logger.info('SIGTERM received, shutting down gracefully');
  server.close(() => {
    mongoose.connection.close();
    process.exit(0);
  });
});

module.exports = { app, io };