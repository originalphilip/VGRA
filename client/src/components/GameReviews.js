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
          reviewsData = reviewsData.filter(review => filter.score === 'All Scores' ? true : review.review_score.toString() === filter.score);
        }

        // Apply sorting based on the sort condition
        switch (filter.sort) {
          case 'latest-oldest':
            reviewsData.sort((a, b) => new Date(b.review_date) - new Date(a.review_date));
            break;
          case 'oldest-latest':
            reviewsData.sort((a, b) => new Date(a.review_date) - new Date(b.review_date));
            break;
          case 'score':
            reviewsData.sort((a, b) => b.review_score - a.review_score);
            break;
          default:
            break;
        }

        // Filter by score if filter action is for score
        // if (filter.actionType === 'filter' && filter.type === 'score' && filter.value) {
        //   reviewsData = reviewsData.filter(review => review.review_score.toString() === filter.value);
        // }
              // Sorting logic
        // if (filter.actionType === 'sort') {
        //   switch (filter.value) {
        //     case 'latest-oldest':
        //      reviewsData.sort((a, b) => new Date(b.review_date) - new Date(a.review_date));
        //       break;
        //     case 'oldest-latest':
        //       reviewsData.sort((a, b) => new Date(a.review_date) - new Date(b.review_date));
        //       break;
        //     case 'score':
        //       reviewsData.sort((a, b) => b.review_score - a.review_score);
        //       break;
        //       default:
        //         // Handle other cases or default behavior
        //         break;
        //   // Handle other sorting criteria as needed
        //   }
        // } else if (filter.actionType === 'filter') {
        //   // Assuming filter.type is included in the filter object for score filtering
        //   if (filter.value !== 'All Scores') {
        //     reviewsData = reviewsData.filter(review => review.review_score.toString() === filter.value);
        //   }
        // }
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
            <div className="image-placeholder"></div> {/* If you have images, dynamically set the src attribute here */}
            <div className="game-info">
              <h1>{review.game_title} - {review.review_score}</h1> {/* Display the review data */}
              <p>{review.description} - {review.review_date}</p>
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
