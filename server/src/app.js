const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const dotenv = require('dotenv');
const connectDB = require('./config/db');
const memberRoutes = require('./routes/memberRoutes');

dotenv.config();
// connectDB();

const app = express();

app.use(cors({
    origin: 'http://localhost:5000', // Replace with your frontend URL
    methods: 'GET, POST, PUT, DELETE', // HTTP methods you want to allow
    allowedHeaders: 'Content-Type, Authorization', // Headers you want to allow
  }));
app.use(bodyParser.json());

app.use('/api/members', memberRoutes);

app.get('/', (req, res) => {
    res.send('Welcome to the Team Member API!');
});

module.exports = app;
