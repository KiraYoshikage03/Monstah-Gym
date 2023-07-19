// For Sidebar
let btn = document.getElementById("btn");
let sidebar = document.querySelector(".sidebar_container");

btn.onclick = function () {
    sidebar.classList.toggle('active');
};

// Animation
ScrollReveal({
    reset: false,
    mobile: true,
    distance: '90px',
    duration: 1500,
    delay: 400,
    easing: 'ease-in-out'
});


// Navigation
ScrollReveal().reveal(".nav_container", {
    origin: 'top'
});

// Sidebar
ScrollReveal().reveal(".sidebar_container", {
    origin: 'left'
});

// Home
ScrollReveal().reveal(".home_container", {
    origin: 'bottom'
});

// Meal Planner

ScrollReveal().reveal(".meal_planner_container", {
    origin: 'left',
    delay: 500
});

ScrollReveal().reveal(".meal_planner_box1", {
    origin: 'left'
});

ScrollReveal().reveal(".meal_planner_box3", {
    origin: 'left'
});

ScrollReveal().reveal(".meal_planner_box4", {
    origin: 'left'
});

ScrollReveal().reveal(".meal_planner_box5", {
    origin: 'left'
});

// Routine
ScrollReveal().reveal(".routine_features_container", {
    origin: 'left'
});

ScrollReveal().reveal(".routine_description_container", {
    origin: 'right'
});

// Membership

ScrollReveal().reveal(".membership_title_text", {
    delay: 300,
    origin: 'top',
    reset: false
}); 

ScrollReveal().reveal(".monthly_box", {
    delay: 300,
    origin: 'top',
    reset: false
});

ScrollReveal().reveal(".annual_box", {
    delay: 400,
    origin: 'top',
    reset: false
});

ScrollReveal().reveal(".custom_box", {
    delay: 400,
    origin: 'top',
    reset: false
});

ScrollReveal().reveal(".choose_text", {
    delay: 400,
    origin: 'top',
    reset: false
})

ScrollReveal().reveal(".text_one", {
    delay: 400,
    origin: 'left',
    reset: false,
    duration: 1000
})


