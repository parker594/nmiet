const express = require('express');
const router = express.Router();

// Data routes
router.get('/terrain', (req, res) => {
    res.json({
        terrain_type: 'mountainous',
        elevation_data: Array(100).fill().map(() => Math.random() * 1000),
        weather: 'clear',
        visibility: 'high'
    });
});

router.get('/satellite', (req, res) => {
    res.json({
        last_update: new Date().toISOString(),
        resolution: '1m',
        coverage: '100%'
    });
});

module.exports = router;