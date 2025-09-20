const express = require('express');
const router = express.Router();

// AI routes
router.post('/navigation', (req, res) => {
    res.json({
        action: 'SOUTHEAST',
        confidence: 0.85,
        reasoning: 'Optimal path with minimal threat exposure',
        threat_level: 'LOW'
    });
});

router.post('/threat-detection', (req, res) => {
    res.json({
        threats_detected: 0,
        confidence: 0.95,
        status: 'clear'
    });
});

module.exports = router;