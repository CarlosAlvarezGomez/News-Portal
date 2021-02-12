'use strict';

// Imports necessary libraries
const articleData = require('../Data/SQLQueries');

// Handles a request to get multiple articles given a category and a 
// requestNumber
const getArticles = async (req, res, next) => {
    try {
        const articles = await articleData.getArticles(req.query.category, req.query.requestNumber);
        res.send(articles);
    // Returns error message if one is received
    } catch (error) {
        res.status(400).send(error.message);
    }
}

// Handles a request to a single article given an id
const getArticleByID = async (req, res, next) => {
    try {
        const article = await articleData.getArticleByID(req.query.ID);
        res.send(article);
    // Returns error message if one is received
    } catch (error) {
        res.status(400).send(error.message);
    }
}

// Exports both functions
module.exports = {getArticles, getArticleByID}