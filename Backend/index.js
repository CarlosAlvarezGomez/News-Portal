'use strict';
// Imports necessary libraries
const express = require('express');
const config = require('./config');
const cors = require('cors');
const bodyParser = require('body-parser');
const articleRoutes = require('./Routes/articleRoutes');

// Creates app
const app = express();

app.use(cors());
app.use(bodyParser.json());

// Makes app use router
app.use(articleRoutes.routes);

// Starts server
app.listen(config.port, () => console.log('Server is listening on http://localhost:' + config.port));