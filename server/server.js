const express = require('express');
const app = express();
const port = 5000;
const cors = require('cors');

// Import database module
const db = require('./database.js');

app.use(cors());
app.use(express.json()); // Middleware to parse JSON bodies

// Define routes
app.get('/api/reviews', (req, res) => {
  const sql = `
  SELECT Reviews.*, Games.CanonicalName, Games.Description, Games.ImageURL, Games.ReleaseDate, Games.Genre
  FROM Reviews
  JOIN Games ON Reviews.GameID = Games.GameID`;
  db.all(sql, [], (err, rows) => {
    if (err) {
      res.status(400).json({"error":err.message});
      return;
    }
    res.json({
      "message":"success",
      "data":rows
    });
  });
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
