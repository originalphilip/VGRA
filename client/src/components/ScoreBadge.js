import React from "react";

const ScoreBadge = ({ score }) => {
  let backgroundColor;
  if (score >= 9) {
    backgroundColor = "#4CAF50"; // Green
  } else if (score >= 7) {
    backgroundColor = "#FFEB3B"; // Yellow
  } else if (score >= 5) {
    backgroundColor = "#FF9800"; // Orange
  } else {
    backgroundColor = "#F44336"; // Red
  }

  return (
    <span
      style={{
        backgroundColor,
        color: "white",
        padding: "0.5em 1em",
        borderRadius: "10px",
        fontSize: "2.0em",
      }}
    >
      {score.toFixed(1)}
    </span>
  );
};

export default ScoreBadge;
