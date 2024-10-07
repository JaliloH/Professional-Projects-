/*
TO DO:
-----
READ ALL COMMENTS AND REPLACE VALUES ACCORDINGLY
*/

const mysql = require("mysql");
const bcrypt = require('bcrypt');

const dbCon = mysql.createConnection({
    host: "cse-mysql-classes-01.cse.umn.edu",
    user: "C4131NF23U27",               // replace with the database user provided to you
    password: "779",                  // replace with the database password provided to you
    database: "C4131NF23U27",           // replace with the database user provided to you
    port: 3306
});

console.log("Attempting database connection");
dbCon.connect(function (err) {
    if (err) {
        throw err;
    }

    console.log("Connected to database!");

    const rowToBeInserted = {
        event_id: 0,
        event_day: 'monday',
        event_event: 'CSCI2041 Lecture',
        event_start: '1:25',
        event_end: '2:15',
        event_location: 'Bruiniks Hall 220',
        event_phone: 'No Phone',
        event_info: 'Ocaml Induction',
        event_url: 'See Class Page'          // replace with acc_login chosen by you OR retain the same value
    };

    const row2ToBeInserted = {
        event_id: 0,
        event_day: 'monday',
        event_event: 'CSCI4061 lab',
        event_start: '3:35',
        event_end: '4:25',
        event_location: 'Keller Hall 1-250',
        event_phone: 'No Phone',
        event_info: 'Circular Buffers',
        event_url: 'See Class Page'          // replace with acc_login chosen by you OR retain the same value
    };

    console.log("Attempting to insert record into tbl_accounts");
    // dbCon.query('INSERT tbl_events SET ?', rowToBeInserted, function (err, result) {
    //     if (err) {
    //         throw err;
    //     }
    //     console.log("Table record inserted!");
    // });

    dbCon.query('DELETE FROM tbl_events WHERE event_id = 5', function (err, result) {
        if (err) throw err;
        console.log("Number of records deleted: " + result.affectedRows);
    });
    
    // dbCon.query('INSERT tbl_events SET ?', row2ToBeInserted, function (err, result) {
    //     if (err) {
    //         throw err;
    //     }
    //     console.log("Table record2 inserted!");
    // });

    dbCon.end();
});
