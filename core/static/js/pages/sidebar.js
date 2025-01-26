document.addEventListener('DOMContentLoaded', function() {
    const sidebarToggle = document.querySelector("#sidebar-toggle");
    sidebarToggle.addEventListener("click", function() {
        document.querySelector("#sidebar").classList.toggle("collapsed");
    });
});