document.addEventListener("DOMContentLoaded", function () {
    const navToggle = document.querySelector(".nav-toggle");
    const navLinks = document.querySelector(".nav-links");
    const socialItems = document.querySelectorAll(".social-item a");

    // Toggle mobile menu
    navToggle.addEventListener("click", () => {
        navLinks.classList.toggle("open");
    });

    // Close mobile menu on link click
    document.querySelectorAll(".nav-links a").forEach(link => {
        link.addEventListener("click", () => {
            navLinks.classList.remove("open");
        });
    });

    // Smooth scroll for all internal links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener("click", function (e) {
            const targetId = this.getAttribute("href").slice(1);
            const targetEl = document.getElementById(targetId);

            if (targetEl) {
                e.preventDefault();
                window.scrollTo({
                    top: targetEl.offsetTop - 60,
                    behavior: "smooth"
                });
            }
        });
    });

    // Animate social icons on hover
    socialItems.forEach(icon => {
        icon.addEventListener("mouseenter", () => {
            icon.style.transform = "scale(1.15)";
            icon.style.transition = "transform 0.2s ease";
        });
        icon.addEventListener("mouseleave", () => {
            icon.style.transform = "scale(1)";
        });
    });
});
