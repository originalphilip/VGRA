import React, { useState, useEffect } from 'react';
import './styles/navbarstyles.css';
import './styles/buttonstyles.css';
import './styles/gameContainers.css';
import Navbar from './components/navbar.js';
import GameReviews from './components/GameReviews.js';
import FilterButtons from './components/filterButtons.js';
import LatestReview from './components/latestReviews.js';

function App() {
  const [filter, setFilter] = useState({ sort: '', score: '', platform: '' });
  const [platforms, setPlatforms] = useState([]);

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
    console.log("Updated Filter State:", filterObj);
  };

  const handlePlatformsFetched = (platforms) => {
    // platforms parameter is now just an array of platform names
    setPlatforms(platforms);
  };


  return (
    <div>
      <Navbar />
      <div className="main-layout">
        <div className="content-container">
          <FilterButtons onFilter={handleFilter} platforms={platforms}/>
          <GameReviews filter={filter} onPlatformsFetched={handlePlatformsFetched}/>
        </div>
        <LatestReview />
      </div>
    </div>
  );
}

export default App;
