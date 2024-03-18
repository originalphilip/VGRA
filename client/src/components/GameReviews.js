import React, { useEffect, useState } from 'react';

function GameReviews({ filter }) {
  const [reviews, setReviews] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    console.log("Current Filter:", filter);
    setIsLoading(true);
    fetch('/api/reviews')
      .then(response => response.json())
      .then(data => {
        // Filter the reviews based on the filter prop
        let reviewsData = data.data;

        // Apply score filter if a score is specified
        if (filter.score) {
          if (filter.score === 'All Scores') {
            // No filtering needed
          } else if (filter.score.includes('-')) {
            const [minScore, maxScore] = filter.score.split('-').map(parseFloat);
            console.log(`Filtering scores between ${minScore} and ${maxScore}`);
            reviewsData = reviewsData.filter(review => {
              const reviewScore = parseFloat(review.NormalizedScore); // Ensure this matches your actual score field
              return reviewScore >= minScore && reviewScore <= maxScore;
            });
          } else {
            const exactScore = parseFloat(filter.score);
            console.log(`Filtering for exact score: ${exactScore}`);
            reviewsData = reviewsData.filter(review => parseFloat(review.NormalizedScore) === exactScore); // Ensure this matches your actual score field
          }
        }
        


        // Apply sorting based on the sort condition
        switch (filter.sort) {
          case 'latest-oldest':
            reviewsData.sort((a, b) => new Date(b.ReleaseDate) - new Date(a.ReleaseDate));
            break;
          case 'oldest-latest':
            reviewsData.sort((a, b) => new Date(a.ReleaseDate) - new Date(b.ReleaseDate));
            break;
          case 'score':
            reviewsData.sort((a, b) => b.NormalizedScore - a.NormalizedScore);
            break;
          default:
            break;
        }
        console.log("Modified Reviews Data:", reviewsData);
        // For other filters, implement similar conditional checks
        setReviews(reviewsData);
        setIsLoading(false); // Data has been loaded
      })
      .catch(error => console.error("Error fetching data:", error));
      setIsLoading(false); // Ensure loading state is updated even on error  
    }, [filter]); // Re-fetch or filter whenever the filter prop changes

    
  return (
    <div>
    {isLoading ? (
      <p>Loading...</p>
    ) : reviews.length > 0 ? (
        reviews.map((review, index) => (
          <div key={index} className="game-container">
            <img src={review.ImageURL} alt={review.CanonicalName} className="image-placeholder" />
            <div className="game-info">
            <h1>{review.CanonicalName} - <span className="review-score">{review.NormalizedScore}</span></h1>
            <p>{review.Description} - {review.ReleaseDate}</p>
            </div>
          </div>
        ))
      ) : (
        <p>No reviews found.</p> // Handle empty data state
      )}
    </div>
  );
  
}

export default GameReviews;
