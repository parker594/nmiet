const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');
const User = require('../models/User');
const logger = require('../config/logger');

// JWT Authentication Middleware
const authMiddleware = async (req, res, next) => {
  try {
    const token = req.header('Authorization')?.replace('Bearer ', '') || 
                  req.cookies?.token;
    
    if (!token) {
      return res.status(401).json({ 
        message: 'Access denied. No token provided.',
        code: 'NO_TOKEN'
      });
    }

    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    const user = await User.findById(decoded.userId).select('-password');
    
    if (!user) {
      return res.status(401).json({ 
        message: 'Invalid token. User not found.',
        code: 'INVALID_USER'
      });
    }

    if (!user.isActive) {
      return res.status(401).json({ 
        message: 'Account deactivated. Contact administrator.',
        code: 'ACCOUNT_DEACTIVATED'
      });
    }

    req.user = user;
    req.token = token;
    
    // Log access for security audit
    logger.info(`User ${user.username} accessed ${req.method} ${req.path}`, {
      userId: user._id,
      ip: req.ip,
      userAgent: req.get('User-Agent')
    });
    
    next();
  } catch (error) {
    logger.error('Authentication error:', error);
    
    if (error.name === 'JsonWebTokenError') {
      return res.status(401).json({ 
        message: 'Invalid token format.',
        code: 'INVALID_TOKEN'
      });
    }
    
    if (error.name === 'TokenExpiredError') {
      return res.status(401).json({ 
        message: 'Token expired. Please login again.',
        code: 'TOKEN_EXPIRED'
      });
    }
    
    return res.status(500).json({ 
      message: 'Server error during authentication.',
      code: 'AUTH_SERVER_ERROR'
    });
  }
};

// Role-based Authorization Middleware
const authorize = (...roles) => {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({ 
        message: 'Access denied. Authentication required.',
        code: 'NO_USER'
      });
    }

    if (!roles.includes(req.user.role)) {
      logger.warn(`Unauthorized access attempt by ${req.user.username} to ${req.path}`, {
        userId: req.user._id,
        requiredRoles: roles,
        userRole: req.user.role
      });
      
      return res.status(403).json({ 
        message: 'Access denied. Insufficient permissions.',
        code: 'INSUFFICIENT_PERMISSIONS',
        required: roles,
        current: req.user.role
      });
    }

    next();
  };
};

// Command Level Authorization (for critical operations)
const commandAuth = async (req, res, next) => {
  try {
    if (req.user.role !== 'COMMANDER' && req.user.role !== 'ADMIN') {
      return res.status(403).json({ 
        message: 'Command level authorization required.',
        code: 'COMMAND_AUTH_REQUIRED'
      });
    }

    // Additional verification for critical commands
    const { commandPassword } = req.body;
    if (!commandPassword) {
      return res.status(401).json({ 
        message: 'Command password required for this operation.',
        code: 'COMMAND_PASSWORD_REQUIRED'
      });
    }

    const isValidCommand = await bcrypt.compare(commandPassword, req.user.commandPasswordHash);
    if (!isValidCommand) {
      logger.warn(`Invalid command password attempt by ${req.user.username}`, {
        userId: req.user._id,
        operation: req.path
      });
      
      return res.status(401).json({ 
        message: 'Invalid command password.',
        code: 'INVALID_COMMAND_PASSWORD'
      });
    }

    // Log critical operation
    logger.info(`Critical operation authorized: ${req.method} ${req.path}`, {
      userId: req.user._id,
      username: req.user.username,
      timestamp: new Date().toISOString()
    });

    next();
  } catch (error) {
    logger.error('Command authorization error:', error);
    return res.status(500).json({ 
      message: 'Server error during command authorization.',
      code: 'COMMAND_AUTH_ERROR'
    });
  }
};

// Session Validation Middleware
const validateSession = async (req, res, next) => {
  try {
    if (!req.user.lastActivity) {
      req.user.lastActivity = new Date();
      await req.user.save();
      return next();
    }

    const sessionTimeout = 30 * 60 * 1000; // 30 minutes
    const timeSinceLastActivity = new Date() - new Date(req.user.lastActivity);
    
    if (timeSinceLastActivity > sessionTimeout) {
      return res.status(401).json({ 
        message: 'Session expired due to inactivity.',
        code: 'SESSION_EXPIRED'
      });
    }

    // Update last activity
    req.user.lastActivity = new Date();
    await req.user.save();
    
    next();
  } catch (error) {
    logger.error('Session validation error:', error);
    next(); // Continue on session validation errors
  }
};

// Rate limiting for sensitive operations
const sensitiveRateLimit = require('express-rate-limit')({
  windowMs: 5 * 60 * 1000, // 5 minutes
  max: 10, // limit each IP to 10 requests per windowMs for sensitive operations
  message: {
    message: 'Too many sensitive operation attempts. Please try again later.',
    code: 'RATE_LIMIT_SENSITIVE'
  },
  standardHeaders: true,
  legacyHeaders: false,
});

module.exports = {
  authMiddleware,
  authorize,
  commandAuth,
  validateSession,
  sensitiveRateLimit
};