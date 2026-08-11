console.log("MediGuide loaded.");

// ---------- Star rating input (doctor review form) ----------
// Supports mouse click/hover AND keyboard (Enter/Space to select,
// matching the role="radio" semantics added for screen reader users.
document.addEventListener("DOMContentLoaded", function () {
    const starContainer = document.getElementById("starInput");
    if (!starContainer) return;

    const stars = starContainer.querySelectorAll(".star-choice");
    const ratingInput = document.getElementById("ratingValue");

    function highlightStars(value) {
        stars.forEach(function (star) {
            const starValue = parseInt(star.getAttribute("data-value"), 10);
            const isActive = starValue <= value;
            star.classList.toggle("star-active", isActive);
        });
    }

    function selectRating(value) {
        ratingInput.value = value;
        highlightStars(value);
        stars.forEach(function (star) {
            const starValue = parseInt(star.getAttribute("data-value"), 10);
            star.setAttribute("aria-checked", starValue === value ? "true" : "false");
        });
    }

    stars.forEach(function (star) {
        star.addEventListener("click", function () {
            selectRating(parseInt(star.getAttribute("data-value"), 10));
        });

        star.addEventListener("mouseenter", function () {
            highlightStars(parseInt(star.getAttribute("data-value"), 10));
        });

        star.addEventListener("keydown", function (event) {
            if (event.key === "Enter" || event.key === " ") {
                event.preventDefault();
                selectRating(parseInt(star.getAttribute("data-value"), 10));
            }
        });
    });

    starContainer.addEventListener("mouseleave", function () {
        highlightStars(parseInt(ratingInput.value, 10) || 0);
    });
});
