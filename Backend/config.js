'use strict';

// Imports necessary libraries
const dotenv = require('dotenv');
const assert = require('assert');

dotenv.config();

// Imports necessary configurations
const {PORT, HOST, HOST_URL, SQL_USER, SQL_PASSWORD, SQL_DATABASE, SQL_SERVER} = process.env;

const sqlEncrypt = process.env.ENCRYPT === "true";

// Checks that PORT and HOST were created
assert(PORT, 'PORT was not created');
assert(HOST, 'Host was not created');

// Exports variables
module.exports = {
    port: PORT,
    host: HOST,
    url: HOST_URL,
    sql: {
        server: SQL_SERVER,
        database: SQL_DATABASE,
        user: SQL_USER,
        password: SQL_PASSWORD,
        options: {
            encrypt: sqlEncrypt,
            enableArithAbort: true
        }
    }
}