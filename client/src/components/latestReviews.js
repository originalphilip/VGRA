import React, { useEffect, useState } from 'react';

function LatestReview() {
  const [latestReview, setLatestReview] = useState(null);
  const serverUrl = process.env.REACT_APP_BACKEND_URL  || 'http://localhost:5000/';

  useEffect(() => {
    // Fetch the reviews data from your API
    fetch(`${serverUrl}api/reviews`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        console.log("Fetched data:", data);
        // Assuming the response body directly contains the array of reviews
        // and that they are sorted by date with the latest first
        if (data && data.data && data.data.length > 0) {
          setLatestReview(data.data[0]); // Set the first review as the latest
        }
      })
      .catch(error => console.error("There was an error fetching the reviews:", error));
  }, [serverUrl]);

  return (
    <div className="latest-review-container">
      <h1>Latest Video Game Review</h1>
      {latestReview ? (
        <>
          <div className="image-placeholder large">
                <img src={latestReview.ImageURL} alt={latestReview.GameName} />
            </div>
          <h2>{latestReview.GameName}</h2>
          <p>{latestReview.Description}</p>
        </>
      ) : (
        <p>No latest review available.</p>
      )}
    </div>
  );
}

export default LatestReview;
