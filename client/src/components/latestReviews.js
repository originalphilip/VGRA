import React, { useEffect, useState } from "react";

function LatestReview() {
  const [latestReview, setLatestReview] = useState(null);
  const serverUrl =
    process.env.REACT_APP_BACKEND_URL || "http://localhost:5000/";

  useEffect(() => {
    fetch(`${serverUrl}api/reviews`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        console.log("Fetched data:", data);
        if (data && data.data && data.data.length > 0) {
          setLatestReview(data.data[0]);
        }
      })
      .catch((error) =>
        console.error("There was an error fetching the reviews:", error)
      );
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
