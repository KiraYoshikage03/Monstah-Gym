function scrollToTop() {
    window.scrollTo({
      top: 0,
      behavior: "smooth"
    });
  }
  
  window.addEventListener("scroll", function() {
    var button = document.getElementById("backToTopBtn");
    if (window.pageYOffset > 300) { // Adjust this value to control when the button appears
      button.style.display = "block";
    } else {
      button.style.display = "none";
    }
  });
  