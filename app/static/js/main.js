
document.addEventListener("DOMContentLoaded", function () {
    const sections = document.querySelectorAll(
        ".page-section, .cta-section, .contact-section"
    );

    if ("IntersectionObserver" in window) {
        const observer = new IntersectionObserver(
            function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("visible");
                        observer.unobserve(entry.target);
                    }
                });
            },
            {
                threshold: 0.08
            }
        );

        sections.forEach(function (section) {
            section.classList.add("reveal");
            observer.observe(section);
        });
    }

    const menu = document.getElementById("mainNavbar");
    const menuLinks = document.querySelectorAll(
        "#mainNavbar .nav-link, #mainNavbar .nav-contact"
    );

    menuLinks.forEach(function (link) {
        link.addEventListener("click", function () {
            if (
                menu &&
                menu.classList.contains("show") &&
                window.bootstrap
            ) {
                bootstrap.Collapse.getOrCreateInstance(menu).hide();
            }
        });
    });
});
