import React from 'react';

function FilterButtons({ onFilter }) {
  // Handle dropdown toggle
  const toggleDropdown = (event) => {
    let dropdownContent = event.currentTarget.nextElementSibling;
    dropdownContent.style.display = dropdownContent.style.display === 'block' ? 'none' : 'block';
  };

  // Example for handling a sorting action
  const handleSort = (sortCondition) => {
    onFilter({ sort: sortCondition });
  };

// Example for handling a score filter action
  const handleScoreFilter = (score) => {
    onFilter({ score: score });
  };

  // const handleAction = (actionType, value) => {
  //   // Call onFilter with an object indicating the action type and value
  //   console.log("Action Type:", actionType, "Value:", value);
  //   onFilter({ actionType, value });
  // };

  //Handle filter content
  const filterContent = (actionType,value) => {
    // Here you can call onFilter with the filter type
    if (value.includes('-')) {
      // If the value includes a range (e.g., "9 - 9.9"), it's a score range filter
      actionType = 'scoreRange'; // Use 'scoreRange' or a similar identifier for ranges
    }else if (!isNaN(value)) {
      // If the value is a number (e.g., "9"), it's a specific score filter
      actionType = 'filter';
    } else {
      // For any other filter type, you can decide on the logic
      actionType = actionType.toLowerCase(); // Example logic
    } 
    console.log("Action Type:", actionType, "Value:", value);
    onFilter({ actionType, value });
  };


  return (
    <div>
      <h1>Reviews</h1>
      {/* Corrected structure for each dropdown you need */}
      <div className="dropdown">
        <button className="dropbtn" onClick={toggleDropdown}>Sort by latest-oldest <span className="dropdown-icon">&#9662;</span></button>
        <div className="dropdown-content">
          {/* Pass the filter type as an argument to filterContent */}
          <a href="#" onClick={() => handleSort('latest-oldest')}>Sort by latest-oldest</a>
          <a href="#" onClick={() => handleSort('oldest-latest')}>Sort by oldest-latest</a>
          <a href="#" onClick={() => handleSort('score')}>Sort by score</a>
        </div>
      </div>
      <div className="dropdown">
        <button className="dropbtn" onClick={toggleDropdown}>All Platforms <span className="dropdown-icon">&#9662;</span></button>
        <div className="dropdown-content">
            <a href="#" onClick={() => filterContent('All Platforms')}>All Platforms</a>
            <a href="#" onClick={() => filterContent('PS5')}>PS5</a>
            <a href="#" onClick={() => filterContent('Xbox Series X/S')}>Xbox Series X/S</a>
            <a href="#" onClick={() => filterContent('Nintendo Switch')}>Nintendo Switch</a>
            <a href="#" onClick={() => filterContent('PC')}>PC</a>
        </div>
       </div>
       <div className="dropdown">
        <button className="dropbtn" onClick={toggleDropdown}>All Scores <span className="dropdown-icon">&#9662;</span></button>
        <div className="dropdown-content">
            <a href="#" onClick={() => handleScoreFilter('All Scores')}>All Scores</a>
            <a href="#" onClick={() => handleScoreFilter('10')}>10</a>
            {/*<a href="#" onClick={() => filterContent('9')}>9 - 9.9</a> change to this when i have the averge done */}
            <a href="#" onClick={() => handleScoreFilter('9')}>9 - 9.9</a>
            <a href="#" onClick={() => handleScoreFilter('8')}>8 - 8.9</a>
            <a href="#" onClick={() => handleScoreFilter('7')}>7 - 7.9</a>
            <a href="#" onClick={() => handleScoreFilter('6')}>6 - 6.9</a>
            <a href="#" onClick={() => handleScoreFilter('5')}>5 - 5.9</a>
            <a href="#" onClick={() => handleScoreFilter('4')}>4 - 4.9</a>
            <a href="#" onClick={() => handleScoreFilter('3')}>3 - 3.9</a>
            <a href="#" onClick={() => handleScoreFilter('2')}>2 - 2.9</a>
            <a href="#" onClick={() => handleScoreFilter('1')}>1 - 1.9</a>
            <a href="#" onClick={() => handleScoreFilter('0')}>0 - 0.9</a>
        </div>
      </div>
    </div>
  );
}

export default FilterButtons;
