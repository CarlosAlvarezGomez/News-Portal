'use strict';

const express = require('express');
const articleController = require('../Controllers/ArticleController');
const router = express.Router();

const {getArticles, getArticleByID} = articleController;

router.get('/articles/', getArticles)

router.get('/article/', getArticleByID)

module.exports = {routes: router}