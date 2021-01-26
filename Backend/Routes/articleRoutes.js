'use strict';

const express = require('express');
const articleController = require('../Controllers/ArticleController');
const router = express.Router();

const {getArticles} = articleController;

router.get('/articles/', getArticles)

module.exports = {routes: router}