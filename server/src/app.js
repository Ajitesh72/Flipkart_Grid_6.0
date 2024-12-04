const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
// const dotenv = require('dotenv');
// const connectDB = require('./config/db');
// const todoRoutes = require('./routes/todoRoutes');

// dotenv.config();
// connectDB();

const app = express();

app.use(cors());
app.use(bodyParser.json());

// app.use('/api/todos', todoRoutes);

app.get('/', (req, res) => {
    res.send("Welcome to the TODO API!");
});

module.exports = app;