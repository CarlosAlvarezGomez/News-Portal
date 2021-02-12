'use strict';

// Imports necessary libraries
const express = require('express');
const articleController = require('../Controllers/ArticleController');

// Gets functions from articleController
const {getArticles, getArticleByID} = articleController;

// Creates router
const router = express.Router();

// Adds routes for articles and article
router.get('/articles/', getArticles)
router.get('/article/', getArticleByID)

// Exports the router
module.exports = {routes: router}