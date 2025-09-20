const express = require('express');
const router = express.Router();

// Simple auth routes for demo
router.post('/login', (req, res) => {
    res.json({ 
        success: true, 
        token: 'demo-jwt-token',
        user: { id: 1, username: 'commander', role: 'admin' }
    });
});

router.post('/logout', (req, res) => {
    res.json({ success: true, message: 'Logged out successfully' });
});

module.exports = router;