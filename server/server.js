const express = require("express");
const app = express();
const port = 5000;
const cors = require("cors");

// Import database module
const db = require("./database.js");

app.use(cors());
app.use(express.json()); // Middleware to parse JSON bodies

// Define routes
app.get("/api/reviews", (req, res) => {
  //SQL Query to average reviews that have the same GameID and return games with more than 1 review
  const sql = `
    SELECT 
      Games.GameID,
      Games.CanonicalName,
      Games.Description,
      Games.ImageURL,
      Games.ReleaseDate,
      Games.Genre,
      AVG(Reviews.NormalizedScore) AS AverageScore,
      COUNT(Reviews.ReviewID) AS NumberOfReviews
    FROM 
      Games
    JOIN 
      Reviews ON Games.GameID = Reviews.GameID
    GROUP BY 
      Games.GameID
    HAVING 
      COUNT(Reviews.ReviewID) > 1;
  `;

  db.all(sql, [], (err, rows) => {
    if (err) {
      res.status(400).json({ error: err.message });
      return;
    }

    const data = rows.map((row) => ({
      ...row,
    }));
    console.log("Sending data to client:", data);
    res.json({
      message: "success",
      data: data,
    });
  });
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
