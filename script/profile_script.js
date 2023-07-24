document.addEventListener('DOMContentLoaded', function () {
  const navLinks = document.querySelectorAll('nav ul li a');

  navLinks.forEach(link => {
    link.addEventListener('click', function (event) {
      event.preventDefault();
      const target = document.querySelector(link.getAttribute('href'));
      const headerHeight = document.querySelector('header').offsetHeight;
      const offsetTop = target.getBoundingClientRect().top + window.scrollY - headerHeight;

      window.scroll({
        top: offsetTop,
        behavior: 'smooth'
      });
    });
  });
});

window.onload = function() {
  const message = "{{ get_flashed_messages(with_categories=true) }}";
  if (message) {
      alert(message);
  }
};
