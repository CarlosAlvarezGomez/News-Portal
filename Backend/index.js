'use strict';
const express = require('express');
const config = require('./config');
const cors = require('cors');
const bodyParser = require('body-parser');
const articleRoutes = require('./Routes/articleRoutes');

const app = express();

app.use(cors());
app.use(bodyParser.json());

app.use(articleRoutes.routes);

app.listen(config.port, () => console.log('Server is listening on http://localhost:' + config.port));