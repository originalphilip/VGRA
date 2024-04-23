import React from "react";
import Select from 'react-select'

const customStyles = {
  control: (base, state) => ({
    ...base,
    minWidth: 50,
    margin: 8,
  }),
  container: (base) => ({
    ...base,
    flex: 1
  })
};

function FilterButtons({ onFilter,onClearFilters, platforms, genres, currentFilters }) {  
  const sortOptions = [
    { value: "latest-oldest", label: "Sort by latest-oldest" },
    { value: "oldest-latest", label: "Sort by oldest-latest" },
    { value: "score", label: "Sort by score" }
  ];

  const scoreOptions = [
    { value: "All Scores", label: "All Scores" },
    { value: "10", label: "10" },
    { value: "9-9.9", label: "9 - 9.9" },
    { value: "8-8.9", label: "8 - 8.9" },
    { value: "7-7.9", label: "7 - 7.9" },
    { value: "6-6.9", label: "6 - 6.9" },
    { value: "5-5.9", label: "5 - 5.9" },
    { value: "4-4.9", label: "4 - 4.9" },
    { value: "3-3.9", label: "3 - 3.9" },
    { value: "2-2.9", label: "2 - 2.9" },
    { value: "1-1.9", label: "1 - 1.9" },
    { value: "0-0.9", label: "0 - 0.9" }
  ];

  const platformOptions = platforms.map(platform => ({ value: platform, label: platform }));
  const genreOptions = genres.map(genre => ({ value: genre, label: genre }));

  const selectedScores = scoreOptions.filter(option => currentFilters.score.includes(option.value));
  const selectedPlatforms = platformOptions.filter(option => currentFilters.platform.includes(option.value));
  const selectedGenres = genreOptions.filter(option => currentFilters.genre.includes(option.value));

  return (
    <div style={{ display: 'flex', justifyContent: 'space-around', flexWrap: 'wrap' }}> {/* Added flexbox styling here */}
      <h1>Reviews</h1>
      <Select
        styles={customStyles}
        options={sortOptions}
        defaultValue={sortOptions[0]}
        placeholder="Sort Reviews"
        onChange={(selectedOption) => onFilter({ sort: selectedOption.value })}
      />
      <Select
        value={selectedScores}
        styles={customStyles}
        options={scoreOptions}
        isMulti
        placeholder="Filter by Score"
        onChange={(selectedOptions) => {
          onFilter({
          score: selectedOptions.map(option => option.value)
          });
      }}
      />
      <Select
        value={selectedPlatforms}
        styles={customStyles}
        options={platformOptions}
        isMulti
        placeholder="Filter by Platform"
        onChange={(selectedOptions) => onFilter({ platform: selectedOptions.map(option => option.value) })}
      />
      <Select
        value={selectedGenres}
        styles={customStyles}
        options={genreOptions}
        isMulti
        placeholder="Filter by Genre"
        onChange={(selectedOptions) => onFilter({ genre: selectedOptions.map(option => option.value) })}
      />
    <button onClick={onClearFilters} className="clear-filters-btn">Clear All Filters</button>
    </div>
  );
}

export default FilterButtons;
