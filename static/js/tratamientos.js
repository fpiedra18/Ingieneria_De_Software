// Espera a que todo el contenido del DOM esté cargado antes de ejecutar el código
document.addEventListener("DOMContentLoaded", function () {
  // Inicializa un nuevo Swiper en el contenedor con la clase .tratamientos-swiper
  const swiper = new Swiper(".tratamientos-swiper", {
    // Número de slides visibles en pantalla
    slidesPerView: 3,
    // Espacio (en px) entre cada slide
    spaceBetween: 30,
    // Activa el loop para que al llegar al final vuelva al inicio
    loop: true,
    // Velocidad de transición entre slides (en ms)
    speed: 600,
    // Configuración del autoplay
    autoplay: {
      // Tiempo (en ms) que tarda en cambiar al siguiente slide automáticamente
      delay: 8000,
      // Si el usuario interactúa con el slider, no desactiva el autoplay
      disableOnInteraction: false,
    },
    // Flechas de navegación
    navigation: {
      // Selector del botón para ir al siguiente slide
      nextEl: ".swiper-button-next",
      // Selector del botón para ir al slide anterior
      prevEl: ".swiper-button-prev",
    },
    // Puntos de quiebre (breakpoints) para responsividad
    breakpoints: {
      0: {
        // En pantallas muy pequeñas, muestra solo 1 slide
        slidesPerView: 1,
      },
      768: {
        // A partir de 768px de ancho, muestra 2 slides
        slidesPerView: 2,
      },
      992: {
        // A partir de 992px de ancho, muestra 3 slides
        slidesPerView: 3,
      },
    },
  });
});

