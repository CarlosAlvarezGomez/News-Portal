'use strict';

const articleData = require('../Data/SQLQueries');

const getArticles = async (req, res, next) => {
    try {
        const articles = await articleData.getArticles(req.query.category, req.query.requestNumber);
        res.send(articles);
    } catch (error) {
        res.status(400).send(error.message);
    }
}

module.exports = {getArticles}