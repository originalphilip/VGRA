import React, { useState } from 'react';
import './styles/navbarstyles.css';
import './styles/buttonstyles.css';
import './styles/gameContainers.css';
import Navbar from './components/navbar.js';
import GameReviews from './components/GameReviews.js';
import FilterButtons from './components/filterButtons.js';
import LatestReview from './components/latestReviews.js';

function App() {
  const [filter, setFilter] = useState({ sort: '', score: '' });

  const handleFilter = (filterObj) => {
    setFilter(prev => ({ ...prev, ...filterObj }));
    console.log("Updated Filter State:", filterObj);
  };

  return (
    <div>
      <Navbar />
      <div className="main-layout">
        <div className="content-container">
          <FilterButtons onFilter={handleFilter} />
          <GameReviews filter={filter} />
        </div>
        <LatestReview />
      </div>
    </div>
  );
}

export default App;
