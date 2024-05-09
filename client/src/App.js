import React, { useState, useEffect } from "react";
import "./styles/navbarstyles.css";
import "./styles/gameContainers.css";
import "./styles/buttons.css";
import "./styles/reviewlinks.css";
import Navbar from "./components/navbar.js";
import GameReviews from "./components/GameReviews.js";
import FilterButtons from "./components/filterButtons.js";
import LatestReview from "./components/latestReviews.js";

function App() {
  const [filter, setFilter] = useState({
    sort: "",
    score: [],
    platform: [],
    genre: [],
  });
  const [platforms, setPlatforms] = useState([]);
  const [genres, setGenres] = useState([]);
  const serverUrl =
    process.env.REACT_APP_BACKEND_URL || "http://localhost:5000/";

  useEffect(() => {
    fetch(`${serverUrl}api/platforms`)
      .then((response) => response.json())
      .then((data) => {
        if (data && data.data) {
          const platformNames = data.data.map((platform) => platform.Name);
          setPlatforms(platformNames);
        }
      })
      .catch((error) => console.error("Error fetching platform data:", error));
  }, [serverUrl]);

  const handleFilter = (filterObj) => {
    setFilter((prev) => ({ ...prev, ...filterObj }));
    console.log("Updated Filter State:", { ...filter, ...filterObj });
  };

  const clearFilters = () => {
    setFilter({ sort: "", score: [], platform: [], genre: [] });
  };

  const handlePlatformsFetched = (platforms) => {
    setPlatforms(platforms);
  };

  useEffect(() => {
    fetch(`${serverUrl}api/genres`)
      .then((response) => response.json())
      .then((data) => {
        if (data && data.data) {
          setGenres(data.data);
        }
      })
      .catch((error) => console.error("Error fetching genres:", error));
  }, [serverUrl]);

  return (
    <div>
      <Navbar />
      <div className="main-layout">
        <div className="content-container">
          <FilterButtons
            onFilter={handleFilter}
            onClearFilters={clearFilters}
            platforms={platforms}
            genres={genres}
            currentFilters={filter}
          />
          <GameReviews
            filter={filter}
            onPlatformsFetched={handlePlatformsFetched}
          />
        </div>
        <LatestReview />
      </div>
    </div>
  );
}

export default App;
