const express = require('express');
const router = express.Router();

// Simulation routes
router.get('/status', (req, res) => {
    res.json({ 
        status: 'running',
        agents: 3,
        missions: 1,
        uptime: new Date().toISOString()
    });
});

router.post('/start', (req, res) => {
    res.json({ success: true, message: 'Simulation started' });
});

router.post('/stop', (req, res) => {
    res.json({ success: true, message: 'Simulation stopped' });
});

module.exports = router;