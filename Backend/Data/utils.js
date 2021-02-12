'use strict';

// Imports necessary libraries
const fs = require('fs-extra');
const {join} = require('path');

// Goes to a folder and returns a set of all the names of .sql files in the
// folder
const loadSQLQueries = async (foldername) => {

    // Creates filepath, reads files, and then removes any iflename that does
    // not end in '.sql'
    const filePath = join(process.cwd(), 'Data', foldername);
    const files = await fs.readdir(filePath);
    const SQLFiles = await files.filter(f => f.endsWith('.sql'));

    const queries = {};

    // Goes through each sql file found and creates an item in the dictionary
    // with the name of the file as the key and the query in the file as the 
    // value
    SQLFiles.forEach(file => {
        const query = fs.readFileSync(join(filePath, file), {encoding: "utf-8"});
        queries[file.replace('.sql', '')] = query;
    });

    // Returns the dictionary of query items
    return queries;
}

// Exports function
module.exports = {loadSQLQueries};