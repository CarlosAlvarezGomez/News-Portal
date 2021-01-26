'use strict';

const fs = require('fs-extra');
const {join} = require('path');

const loadSQLQueries = async (foldername) => {
    const filePath = join(process.cwd(), 'Data', foldername);
    const files = await fs.readdir(filePath);
    const SQLFiles = await files.filter(f => f.endsWith('.sql'));
    const queries = {};

    SQLFiles.forEach(file => {
        const query = fs.readFileSync(join(filePath, file), {encoding: "utf-8"});
        queries[file.replace('.sql', '')] = query;
    });

    return queries;
}

module.exports = {loadSQLQueries};