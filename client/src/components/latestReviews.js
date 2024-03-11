import React, { useEffect, useState } from 'react';

function LatestReview() {
  const [reviews, setReviews] = useState([]);

  useEffect(() => {
    // Assuming '/api/reviews' is your endpoint for fetching game reviews
    fetch('/api/reviews')
      .then(response => response.json())
      .then(data => {
        console.log("Fetched data:", data);
        // Assuming the response body directly contains the array of reviews
        setReviews(data.data); // Adjust according to your actual data structure
      })
      .catch(error => console.error("There was an error!", error));
  }, []);
return (
    <div>
<div className="latest-review-container">
<h1>Latest Video Game Review</h1>
<div className="image-placeholder large"></div>
<h2>"title"</h2> {/* Adjust field names as per your data structure */}
<p>"description"</p>
</div>
</div>
  );
  
}

export default LatestReview