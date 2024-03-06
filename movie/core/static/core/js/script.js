document.addEventListener("DOMContentLoaded", function() {
    var main = document.querySelector("main");

    updateBackgroundOpacity();

    window.addEventListener("scroll", function() {
        updateBackgroundOpacity();
    });

    function updateBackgroundOpacity() {
        var scrollPosition = window.scrollY || document.documentElement.scrollTop;

        var maxOpacity = 0.8;
        var opacity = Math.min(scrollPosition / (document.body.scrollHeight - window.innerHeight), maxOpacity);

        main.style.backgroundColor = "rgba(0, 0, 0, " + opacity + ")";
    }
});
