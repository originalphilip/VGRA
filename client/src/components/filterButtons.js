import React from "react";

function FilterButtons({ onFilter, platforms, genres }) {
  const toggleDropdown = (event) => {
    let dropdownContent = event.currentTarget.nextElementSibling;
    dropdownContent.style.display =
      dropdownContent.style.display === "block" ? "none" : "block";
  };
  
  const handleSort = (sortCondition) => {
    onFilter({ sort: sortCondition });
  };

  const handleScoreFilter = (score) => {
    onFilter({ score: score });
  };

  const handlePlatformFilter = (platform) => {
    onFilter({ platform: platform });
  };

  const handleGenreFilter = (genre) => {
    onFilter({ genre: genre });
  };

  return (
    <div>
      <h1>Reviews</h1>
      <div className="dropdown">
        <button className="dropbtn" onClick={toggleDropdown}>
          Sort by latest-oldest <span className="dropdown-icon">&#9662;</span>
        </button>
        <div className="dropdown-content">
          {/* Pass the filter type as an argument to filterContent */}
          <a href="#" onClick={() => handleSort("latest-oldest")}>
            Sort by latest-oldest
          </a>
          <a href="#" onClick={() => handleSort("oldest-latest")}>
            Sort by oldest-latest
          </a>
          <a href="#" onClick={() => handleSort("score")}>
            Sort by score
          </a>
        </div>
      </div>

      <div className="dropdown">
        <button className="dropbtn" onClick={toggleDropdown}>
          All Scores <span className="dropdown-icon">&#9662;</span>
        </button>
        <div className="dropdown-content">
          <a href="#" onClick={() => handleScoreFilter("All Scores")}>
            All Scores
          </a>
          <a href="#" onClick={(e) => { e.preventDefault(); handleScoreFilter("10"); }}>
            10
          </a>
          {/*<a href="#" onClick={() => filterContent('9')}>9 - 9.9</a> change to this when i have the averge done */}
          <a href="#" onClick={(e) => { e.preventDefault(); handleScoreFilter("9-9.9"); }}>
            9 - 9.9
          </a>
          <a href="#" onClick={(e) => { e.preventDefault(); handleScoreFilter("8-8.9"); }}>
            8 - 8.9
          </a>
          <a href="#" onClick={(e) => { e.preventDefault(); handleScoreFilter("7-7.9"); }}>
            7 - 7.9
          </a>
          <a href="#" onClick={(e) => { e.preventDefault(); handleScoreFilter("6-6.9"); }}>
            6 - 6.9
          </a>
          <a href="#" onClick={(e) => { e.preventDefault(); handleScoreFilter("5-5.9"); }}>
            5 - 5.9
          </a>
          <a href="#" onClick={(e) => { e.preventDefault(); handleScoreFilter("4-4.9"); }}>
            4 - 4.9
          </a>
          <a href="#" onClick={(e) => { e.preventDefault(); handleScoreFilter("3-3.9"); }}>
            3 - 3.9
          </a>
          <a href="#" onClick={(e) => { e.preventDefault(); handleScoreFilter("2-2.9"); }}>
            2 - 2.9
          </a>
          <a href="#" onClick={(e) => { e.preventDefault(); handleScoreFilter("1-1.9"); }}>
            1 - 1.9
          </a>
          <a href="#" onClick={(e) => { e.preventDefault(); handleScoreFilter("0-0.9"); }}>
            0 - 0.9
          </a>
        </div>
      </div>

      <div className="dropdown">
        <button className="dropbtn" onClick={toggleDropdown}>
          Filter by Platform <span className="dropdown-icon">&#9662;</span>
        </button>
        <div className="dropdown-content">
          {platforms.map((platform, idx) => (
            // Assuming 'platforms' is an array of strings
            <a
              key={idx}
              href="#"
              onClick={() => handlePlatformFilter(platform)}
            >
              {platform}
            </a>
          ))}
        </div>
      </div>

      <div className="dropdown">
        <button className="dropbtn" onClick={toggleDropdown}>Filter by Genre <span className="dropdown-icon">&#9662;</span></button>
        <div className="dropdown-content">
          {genres.map((genre, idx) => (
            <a key={idx} href="#" onClick={() => handleGenreFilter(genre)}>
              {genre}
            </a>
          ))}
        </div>
      </div>
    </div>
  );
}

export default FilterButtons;
