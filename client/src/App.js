import React, { useState } from 'react';
import './styles/navbarstyles.css';
import './styles/buttonstyles.css';
import './styles/gameContainers.css';
import Navbar from './components/navbar.js';
import GameReviews from './components/GameReviews.js';
import FilterButtons from './components/filterButtons.js';

function App() {
  const [filter, setFilter] = useState({type: '', value: ''});

  const handleFilter = (filterObj) => {
    setFilter(filterObj);
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
        <div className="latest-review-container">
          <h1>Latest Video Game Review</h1>
          <div className="image-placeholder large"></div>
          <h2>"title"</h2>
          <p>"description"</p>
        </div>
      </div>
    </div>
  );
}

export default App;
