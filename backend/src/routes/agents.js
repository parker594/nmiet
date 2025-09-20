const express = require('express');
const router = express.Router();

// Agent routes
router.get('/', (req, res) => {
    res.json([
        { id: 1, type: 'vehicle', status: 'active', position: [10, 10] },
        { id: 2, type: 'drone', status: 'patrol', position: [25, 30] },
        { id: 3, type: 'unit', status: 'standby', position: [5, 15] }
    ]);
});

router.post('/', (req, res) => {
    res.json({ success: true, id: Date.now(), message: 'Agent created' });
});

module.exports = router;