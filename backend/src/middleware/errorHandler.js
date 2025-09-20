const errorHandler = (err, req, res, next) => {
    console.error(err.stack);
    
    if (err.type === 'validation') {
        return res.status(400).json({ 
            error: 'Validation Error', 
            message: err.message 
        });
    }
    
    if (err.type === 'auth') {
        return res.status(401).json({ 
            error: 'Authentication Error', 
            message: err.message 
        });
    }
    
    res.status(500).json({ 
        error: 'Internal Server Error',
        message: process.env.NODE_ENV === 'development' ? err.message : 'Something went wrong'
    });
};

module.exports = errorHandler;