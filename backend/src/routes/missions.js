const express = require('express');
const router = express.Router();

// Mission routes
router.get('/', (req, res) => {
    res.json([
        { 
            id: 1, 
            name: 'Operation Thunder', 
            status: 'active',
            objective: 'Reconnaissance mission in sector 7',
            progress: 65
        }
    ]);
});

router.post('/', (req, res) => {
    res.json({ success: true, id: Date.now(), message: 'Mission created' });
});

module.exports = router;