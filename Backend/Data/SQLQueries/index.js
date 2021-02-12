'use strict';

const utils = require('../utils');
const config = require('../../config');
const sql = require('mssql');
const { request } = require('express');

const getArticles = async (category, requestNumber) => {
    try {
        let pool = await sql.connect(config.sql);
        const SQLQueries = await utils.loadSQLQueries('SQLQueries');
        const articles = await pool.request()
            .input('category', sql.VarChar, category)
            .input('minRow', sql.Int, requestNumber*10)
            .query(SQLQueries.getArticle);
        return articles.recordset;
    } catch (error) {
        return error.message
    }
}

const getArticleByID = async (ID) => {
    try {
        let pool = await sql.connect(config.sql);
        const SQLQueries = await utils.loadSQLQueries('SQLQueries');
        const articles = await pool.request()
            .input('ID', sql.VarChar, ID)
            .query(SQLQueries.getArticleByID);
        return articles.recordset;
    } catch (error) {
        return error.message
    }
}


module.exports = {getArticles, getArticleByID}