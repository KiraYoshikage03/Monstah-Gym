// Change the color of text on the admin and staff button

// Admin
const adminElement = document.getElementById('is_superuser');


adminElement.addEventListener('change', function() {
  if (this.value === 'False') {
    this.style.color = 'rgb(164, 76, 76)';
    this.style.backgroundColor = 'rgb(46, 34, 34)';
  } 
  else if (this.value === 'True') {
    this.style.color = 'rgb(80, 144, 205)';
    this.style.backgroundColor = 'rgb(46, 46, 75)';
  }
  else {
    // Default styling if the value is neither True nor False
    adminElement.style.background = "";
    adminElement.style.color = "";
  }
});

// Staff

const selectElement = document.getElementById('is_staff');


selectElement.addEventListener('change', function() {
  if (this.value === 'False') {
    this.style.color = 'rgb(164, 76, 76)';
    this.style.backgroundColor = 'rgb(46, 34, 34)';
  } 
  else if (this.value === 'True') {
    this.style.color = 'rgb(80, 144, 205)';
    this.style.backgroundColor = 'rgb(46, 46, 75)';
  }
  else {
    // Default styling if the value is neither True nor False
    selectElement.style.background = "";
    selectElement.style.color = "";
  }
});