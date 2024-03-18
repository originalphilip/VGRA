const sqlite3 = require('sqlite3').verbose();

// Connect to the SQLite database
let db = new sqlite3.Database('./reviewsDB', sqlite3.OPEN_READWRITE, (err) => {
  if (err) {
    console.error('Error opening database', err.message);
  } else {
    console.log('Connected to the SQLite database.');
  }
});

module.exports = db;