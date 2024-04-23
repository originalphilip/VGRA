import React, { useState, useEffect } from 'react';
import './styles/navbarstyles.css';
import './styles/gameContainers.css';
import './styles/buttons.css';
import Navbar from './components/navbar.js';
import GameReviews from './components/GameReviews.js';
import FilterButtons from './components/filterButtons.js';
import LatestReview from './components/latestReviews.js';

function App() {
  const [filter, setFilter] = useState({ sort: '', score: [], platform: [], genre: [] });
  const [platforms, setPlatforms] = useState([]);
  const [genres, setGenres] = useState([]);

  useEffect(() => {
    // Fetch platforms from the server
    fetch('/api/platforms')
      .then(response => response.json())
      .then(data => {
        if (data && data.data) {
          const platformNames = data.data.map(platform => platform.Name);
          setPlatforms(platformNames);
        }
      })
      .catch(error => console.error('Error fetching platform data:', error));
  }, []); // Empty dependency array means this effect runs once on mount

  const handleFilter = (filterObj) => {
    setFilter(prev => ({ ...prev, ...filterObj }));
    console.log("Updated Filter State:",  { ...filter, ...filterObj });
  };

  const clearFilters = () => {
    setFilter({ sort: '', score: [], platform: [], genre: [] });
  };

  const handlePlatformsFetched = (platforms) => {
    // platforms parameter is now just an array of platform names
    setPlatforms(platforms);
  };

  useEffect(() => {
    fetch('/api/genres')
      .then(response => response.json())
      .then(data => {
        if (data && data.data) {
          setGenres(data.data);
        }
      })
      .catch(error => console.error('Error fetching genres:', error));
  }, []);


  return (
    <div>
      <Navbar />
      <div className="main-layout">
        <div className="content-container">
          <FilterButtons onFilter={handleFilter} onClearFilters={clearFilters} platforms={platforms} genres={genres} currentFilters={filter}/>
          <GameReviews filter={filter} onPlatformsFetched={handlePlatformsFetched}/>
        </div>
        <LatestReview />
      </div>
    </div>
  );
}

export default App;
