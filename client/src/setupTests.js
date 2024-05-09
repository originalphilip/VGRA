import "@testing-library/jest-dom";

import { render, fireEvent } from "@testing-library/react";
import FilterButtons from "./components/filterButtons.js";

import React from "react";

describe("FilterButtons", () => {
  const mockOnFilter = jest.fn();
  const platforms = ["PC", "PlayStation", "Xbox"];
  const genres = ["Action", "Adventure", "Strategy"];

  it("should call onFilter with the correct arguments when sort button is clicked", () => {
    const { getAllByText } = render(
      <FilterButtons
        onFilter={mockOnFilter}
        platforms={platforms}
        genres={genres}
      />
    );

    const sortButtons = getAllByText("Sort by latest-oldest");
    fireEvent.click(sortButtons[0]); // Click the first button found
    fireEvent.click(getAllByText("Sort by score")[0]); // Click the first occurrence of 'Sort by score'
    expect(mockOnFilter).toHaveBeenCalledWith({ sort: "score" });
  });
});
