
document.addEventListener("DOMContentLoaded", function () {
  const swiper = new Swiper(".tratamientos-swiper", {
    slidesPerView: 3,
    spaceBetween: 30,
    loop: true,
    speed: 600,
    autoplay: {
      delay: 8000,
      disableOnInteraction: false,
    },
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
    breakpoints: {
      0: {
        slidesPerView: 1,
      },
      768: {
        slidesPerView: 2,
      },
      992: {
        slidesPerView: 3,
      },
    },
  });
});
