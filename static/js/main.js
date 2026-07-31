// main.js
// Shared JS interactions across MediGuide.

console.log("MediGuide loaded.");

// ---------- Star rating input (doctor review form) ----------
document.addEventListener("DOMContentLoaded", function () {
    const starContainer = document.getElementById("starInput");
    if (!starContainer) return;

    const stars = starContainer.querySelectorAll(".star-choice");
    const ratingInput = document.getElementById("ratingValue");

    function highlightStars(value) {
        stars.forEach(function (star) {
            const starValue = parseInt(star.getAttribute("data-value"), 10);
            star.classList.toggle("star-active", starValue <= value);
        });
    }

    stars.forEach(function (star) {
        star.addEventListener("click", function () {
            const value = parseInt(star.getAttribute("data-value"), 10);
            ratingInput.value = value;
            highlightStars(value);
        });

        star.addEventListener("mouseenter", function () {
            const value = parseInt(star.getAttribute("data-value"), 10);
            highlightStars(value);
        });
    });

    starContainer.addEventListener("mouseleave", function () {
        highlightStars(parseInt(ratingInput.value, 10) || 0);
    });
});
