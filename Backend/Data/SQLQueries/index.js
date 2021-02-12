'use strict';

const utils = require('../utils');
const config = require('../../config');
const sql = require('mssql');

// Takes in a category and requestNumber and returns the first 
// (requestNumber*10) articles from that category 
const getArticles = async (category, requestNumber) => {
    try {
        // Connects the sql database
        let pool = await sql.connect(config.sql);

        // Gets a dicitonary of all potential sql queries
        const SQLQueries = await utils.loadSQLQueries('SQLQueries');

        // Sends sql query and returns result
        const articles = await pool.request()
            .input('category', sql.VarChar, category)
            .input('minRow', sql.Int, requestNumber*10)
            .query(SQLQueries.getArticle);
        return articles.recordset;
    
    // Prints error message if necessary
    } catch (error) {
        return error.message
    }
}

// Takes in an ID and returns the article with the corresponding ID
const getArticleByID = async (ID) => {
    try {
        // Connects the sql database
        let pool = await sql.connect(config.sql);

        // Gets a dicitonary of all potential sql queries
        const SQLQueries = await utils.loadSQLQueries('SQLQueries');

        // Sends sql query and returns result
        const articles = await pool.request()
            .input('ID', sql.VarChar, ID)
            .query(SQLQueries.getArticleByID);
        return articles.recordset;
    
    // Prints error message if necessary
    } catch (error) {
        return error.message
    }
}


module.exports = {getArticles, getArticleByID}