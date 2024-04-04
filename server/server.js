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
  const platformFilter = req.query.platform ? ` AND Platforms.Name = '${req.query.platform}'` : '';
  const genreFilter = req.query.genre ? `AND Games.Genre = '${req.query.genre}'` : '';
  const sql = `
    SELECT 
      Games.GameID,
      Games.CanonicalName,
      Games.Description,
      Games.ImageURL,
      Games.ReleaseDate,
      Games.Genre,
      GROUP_CONCAT(DISTINCT Platforms.Name) AS Platforms,
      GROUP_CONCAT(DISTINCT Reviews.SourceWebsite) AS SourceWebsites,
      GROUP_CONCAT(DISTINCT Reviews.ReviewURL) AS ReviewURLs,
      AVG(Reviews.NormalizedScore) AS AverageScore,
      COUNT(DISTINCT Reviews.ReviewID) AS NumberOfReviews
    FROM 
      Games
    JOIN 
      Reviews ON Games.GameID = Reviews.GameID
    LEFT JOIN 
      GamePlatforms ON Games.GameID = GamePlatforms.GameID
    LEFT JOIN 
      Platforms ON GamePlatforms.PlatformID = Platforms.PlatformID
    WHERE 1=1 ${platformFilter} ${genreFilter}
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

    // Filter out games with reviews from only identical source websites
    const data = rows
      .filter((row) => {
        // Ensure that we have multiple source websites
        const sourceWebsites = row.SourceWebsites.split(",");
        const allSitesIdentical = sourceWebsites.every((val, i, arr) => val === arr[0]);
        return !allSitesIdentical;
      })
      .map((row) => ({
        ...row,
        Platforms: row.Platforms ? row.Platforms.split(',') : []
      }));

    console.log("Sending filtered data to client:", data);
    res.json({
      message: "success",
      data: data,
    });
  });
});

app.get("/api/platforms", (req, res) => {
  const sql = `SELECT * FROM Platforms`;

  db.all(sql, [], (err, rows) => {
    if (err) {
      // Send a 500 Internal Server Error response if there's a problem with the database query
      res.status(500).json({ error: err.message });
      return;
    }
    
    // Send a 200 OK response along with the platform data
    res.json({
      message: "success",
      data: rows
    });
  });
});

app.get("/api/platforms-for-games", (req, res) => {
  // Extract gameIds from query parameters and split by comma
  const gameIds = req.query.gameIds ? req.query.gameIds.split(',') : [];

  // SQL query to fetch platforms for the given game IDs
  const sql = `
      SELECT GamePlatforms.GameID, GROUP_CONCAT(Platforms.Name) AS Platforms
      FROM GamePlatforms
      JOIN Platforms ON GamePlatforms.PlatformID = Platforms.PlatformID
      WHERE GamePlatforms.GameID IN (${gameIds.map(id => '?').join(',')})
      GROUP BY GamePlatforms.GameID;
  `;

  db.all(sql, gameIds, (err, rows) => {
      if (err) {
          res.status(400).json({ error: err.message });
          return;
      }
      res.json({
          message: "success",
          data: rows
      });
  });
});

app.get("/api/genres", (req, res) => {
  const sql = `SELECT DISTINCT Genre FROM Games`;

  db.all(sql, [], (err, rows) => {
    if (err) {
      res.status(500).json({ error: err.message });
      return;
    }
    res.json({
      message: "success",
      data: rows.map(row => row.Genre),
    });
  });
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
