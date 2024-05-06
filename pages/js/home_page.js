document.addEventListener('DOMContentLoaded', function() {
  // Get all the buttons with the class "styled-button"
  const buttons = document.querySelectorAll('.styled-button');

  // Add a click event listener to each button
  buttons.forEach(button => {
    button.addEventListener('click', (event) => {
      buttons.forEach(otherButton => {
        if (otherButton !== button) {
          otherButton.classList.remove('clicked');
        }
      });

      button.classList.toggle('clicked');
    });
  });
});


/*document.addEventListener('DOMContentLoaded', function() {
  // Get all the buttons with the class "styled-button"
  const buttons = document.querySelectorAll('.styled-button');

  // Add a click event listener to each button
  buttons.forEach(button => {
    button.addEventListener('click', () => {
      button.classList.toggle('clicked');
    });
  });
});
/*function toggleShadow() {
    var button = document.querySelector('.styled-button');
    button.classList.toggle('clicked');
  }*/