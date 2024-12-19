document.addEventListener("DOMContentLoaded", () => {
    const genreTags = document.querySelectorAll(".genre-tag");
    const searchForm = document.querySelector(".search-bar form");

    // Show a loading spinner during form submission
    searchForm.addEventListener("submit", () => {
        document.getElementById("book-list").innerHTML = "<p>Loading...</p>";
    });

    // Handle genre tag clicks
    genreTags.forEach(tag => {
        tag.addEventListener("click", () => {
            document.getElementById("book-list").innerHTML = "<p>Loading...</p>";
        });
    });
});
