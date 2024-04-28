import React, { useEffect, useState, useRef, useCallback } from "react";
import ScoreBadge from './ScoreBadge';

function GameReviews({ filter, onPlatformsFetched }) {
  const extractDomain = (url) => {
    try {
      const domain = new URL(url).hostname.replace(/^www\./, '');
      return domain;
    } catch (e) {
      console.error("Invalid URL", url);
      return null;
    }
  };

  const [reviews, setReviews] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  const fetchPlatformsForGames = useCallback((gameIds) => {
    const queryParams = new URLSearchParams({ gameIds: gameIds.join(',') }).toString();
    const serverUrl = process.env.REACT_APP_BACKEND_URL  || 'http://localhost:5000'; // Default to localhost if the env variable is not set
    const url = `${serverUrl}api/platforms-for-games?${queryParams}`;

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
    const serverUrl = process.env.REACT_APP_BACKEND_URL  || 'http://localhost:5000'; // Default to localhost if the env variable is not set
    let isMounted = true; // Track if the component is mounted
    setIsLoading(true);
    let query = `${serverUrl}api/reviews`;
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
      {isLoading ? <p>Loading...</p> : reviews.length ? (
        reviews.map((review, index) => {
  const reviewURLs = review.ReviewURLs ? review.ReviewURLs.split(',') : [];
  const reviewSites = review.SourceWebsites ? review.SourceWebsites.split(',') : [];
  return(
    <div key={index} className="game-container">
      <div className="image-and-score">
        <img src={review.ImageURL} alt={review.GameName} className="image-placeholder" />
        <span className="score-text">Review Score</span>
        <ScoreBadge score={review.AverageScore} />
      </div>
      <div className="game-info">
        <h1>{review.GameName}</h1>
        <p>{review.Description} - {review.ReleaseDate}</p>
        {reviewURLs.length > 0 && (
          <div className="review-links">
            <h4>Review Sources:</h4>
            <ul>
              {reviewURLs.map((url, idx) => {
                const domain = extractDomain(url);
                const logoUrl = domain ? `https://logo.clearbit.com/${domain}` : "/path/to/default-logo.png";
                const siteName = reviewSites[idx] || 'Unknown Source'; 
                return (
                  <li key={idx} className="review-link">
                    <a href={url} target="_blank" rel="noopener noreferrer">
                      <img className="review-logo" src={logoUrl} alt={`${siteName} Logo`} onError={(e) => { e.target.src = '/path/to/default-logo.png'; }} />
                      {siteName}
                    </a>
                  </li>
                )
              })}
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
