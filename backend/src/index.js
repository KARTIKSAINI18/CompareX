require('dotenv').config();
const express = require('express');
const cors = require('cors');
const axios = require('axios');
const { verifyToken } = require('./middleware/auth');

const app = express();
const PORT = process.env.PORT || 5000;
const FASTAPI_URL = process.env.FASTAPI_URL || 'http://127.0.0.1:8000';

app.use(cors());
app.use(express.json());

// Public health check route
app.get('/health', (req, res) => {
    res.json({ status: 'Express Gateway is running' });
});

// Protected route that forwards to FastAPI
app.post('/api/ask', verifyToken, async (req, res) => {
    try {
        console.log(`Forwarding request for user ${req.user.uid} to FastAPI...`);
        
        // Forward the request to the FastAPI engine
        const response = await axios.post(`${FASTAPI_URL}/api/v1/ask`, req.body, {
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        // Return the AI response back to the client
        res.json(response.data);
    } catch (error) {
        console.error("Error communicating with FastAPI:", error.message);
        const status = error.response ? error.response.status : 500;
        const data = error.response ? error.response.data : { error: 'Internal Server Error connecting to AI engine' };
        res.status(status).json(data);
    }
});

app.listen(PORT, () => {
    console.log(`Express Gateway Server running on http://localhost:${PORT}`);
    console.log(`Forwarding AI requests to FastAPI at ${FASTAPI_URL}`);
});
