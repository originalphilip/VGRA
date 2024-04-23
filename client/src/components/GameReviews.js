import React, { useEffect, useState, useRef, useCallback } from "react";

function GameReviews({ filter, onPlatformsFetched }) {
  const [reviews, setReviews] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

    const fetchPlatformsForGames = useCallback((gameIds) => {
    const queryParams = new URLSearchParams({ gameIds: gameIds.join(',') }).toString();
    const url = `/api/platforms-for-games?${queryParams}`;

    fetch(url)
      .then(response => response.json())
      .then(data => {
        if (data && data.data && onPlatformsFetched) {
          // Extract and format platform data as needed before calling onPlatformsFetched
          const platforms = data.data.map(item => item.Platforms.split(',')).flat();
          const uniquePlatforms = [...new Set(platforms)];
          onPlatformsFetched(uniquePlatforms);
        }
      })
      .catch(error => console.error("Error fetching platforms:", error));
  }, [onPlatformsFetched]);

  useEffect(() => {
    console.log("Current Filter:", filter);
    let isMounted = true; // Track if the component is mounted
    setIsLoading(true);
    let query = '/api/reviews';
    const queryParams = [];
    if (filter.platform) {
      queryParams.push(`platform=${encodeURIComponent(filter.platform)}`);
    }
    if (filter.genre) {
      queryParams.push(`genre=${encodeURIComponent(filter.genre)}`);
    }
    if (queryParams.length) {
      query += `?${queryParams.join('&')}`;
    }
    fetch(query)
      .then((response) => response.json())
      .then((data) => {
        if (isMounted) {
          // Filter the reviews based on the filter prop
          let reviewsData = data.data;

          // Apply score filter if a score is specified
          if (filter.score && filter.score.length > 0) {
            if (filter.score.includes("All Scores")) {
              // No filtering needed for 'All Scores'
            } else {
              reviewsData = reviewsData.filter((review) => {
                return filter.score.some((score) => {
                  if (score.includes("-")) {
                    const [minScore, maxScore] = score.split("-").map(parseFloat);
                    return review.AverageScore >= minScore && review.AverageScore <= maxScore;
                  } else {
                    const exactScore = parseFloat(score);
                    return review.AverageScore === exactScore;
                  }
                });
              });
            }
            console.log("Filtered Reviews Data:", reviewsData);
          }

          // Apply sorting based on the sort condition
          switch (filter.sort) {
            case "latest-oldest":
              reviewsData.sort(
                (a, b) => new Date(b.ReleaseDate) - new Date(a.ReleaseDate)
              );
              break;
            case "oldest-latest":
              reviewsData.sort(
                (a, b) => new Date(a.ReleaseDate) - new Date(b.ReleaseDate)
              );
              break;
            case "score":
              reviewsData.sort((a, b) => b.AverageScore - a.AverageScore);
              break;
            default:
              break;
          }
          console.log("Modified Reviews Data:", reviewsData);
          setReviews(reviewsData);
          // Fetch platforms for the games currently being displayed
          const gameIds = reviewsData.map(review => review.GameID).join(',');
          if (previousGameIds.current !== gameIds) {
            fetchPlatformsForGames(gameIds.split(','));
            previousGameIds.current = gameIds; // Store the current gameIds
          }
        }
      })
      .catch((error) => console.error("Error fetching data:", error))
      .finally(() => setIsLoading(false));

      // Cleanup function to set isMounted to false when the component unmounts
    return () => {
      isMounted = false;
    };
    }, [filter, fetchPlatformsForGames]); // Re-fetch or filter whenever the filter prop changes
    // Use a ref to store the previous game IDs
    const previousGameIds = useRef('');

  return (
    <div>
      {isLoading ? (
        <p>Loading...</p>
      ) : reviews.length > 0 ? (
        reviews.map((review, index) => {
          // Split ReviewURL string into an array of URLs
          const reviewURLs = review.ReviewURLs ? review.ReviewURLs.split(',') : [];
          const reviewSites = review.SourceWebsites ? review.SourceWebsites.split(',') : [];
          return (
            <div key={index} className="game-container">
              <img src={review.ImageURL} alt={review.GameName} className="image-placeholder" />
              <div className="game-info">
                <h1>
                  {review.GameName} -{" "}
                  <span className="review-score">
                    {review.AverageScore ? review.AverageScore.toFixed(2) : "N/A"}
                  </span>
                </h1>
                <p>{review.Description} - {review.ReleaseDate}</p>
                {/* Display Review URLs */}
                {reviewURLs.length > 0 && (
                  <div className="review-links">
                    <h4>Review Sources:</h4>
                    <ul>
                      {reviewURLs.map((url, idx) => (
                        <li key={idx}>
                          <a href={url} target="_blank" rel="noopener noreferrer">
                            {reviewSites[idx] || 'Review Source'}
                          </a>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          );
        })
      ) : (
        <p>No reviews found.</p>
      )}
    </div>
  );
}

export default GameReviews;
