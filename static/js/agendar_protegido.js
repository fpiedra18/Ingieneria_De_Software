// static/js/agendar_protegido.js

// Espera que todo el contenido del DOM esté cargado
document.addEventListener("DOMContentLoaded", function () {
  // Obtener referencias a los elementos del DOM
  const tratamientoSelect = document.getElementById("tratamientoSelect");
  const fechaInput = document.getElementById("fechaInput");
  const bloqueHorarios = document.getElementById("bloqueHorarios");
  const listaHorarios = document.getElementById("listaHorarios");
  const formFinal = document.getElementById("formFinal");
  const resumenSeleccion = document.getElementById("resumenSeleccion");
  const inputTratamiento = document.getElementById("inputTratamiento");
  const inputFecha = document.getElementById("inputFecha");
  const inputHora = document.getElementById("inputHora");
  const inputContacto = document.getElementById("inputContacto");
  const inputNombre = document.querySelector('input[name="nombre"]');
  const submitBtn = formFinal.querySelector('button[type="submit"]');

  // Bandera para evitar envíos dobles del formulario
  let yaEnviado = false;

  // Configuración del calendario con flatpickr
  flatpickr("#calendarContainer", {
    inline: true, // Muestra el calendario de forma embebida
    minDate: fechaInput.getAttribute("data-fecha-hoy"), // Fecha mínima permitida
    dateFormat: "Y-m-d", // Formato de fecha
    locale: {
      firstDayOfWeek: 1, // Lunes como primer día de la semana
    },
    onChange: function (selectedDates, dateStr) {
      // Al cambiar la fecha, actualiza el input y carga los horarios
      fechaInput.value = dateStr;
      cargarHorarios();
    },
  });

  // Evento para cargar horarios cuando se cambia el tratamiento
  tratamientoSelect.addEventListener("change", cargarHorarios);

  // Función para cargar los horarios disponibles desde el backend
  function cargarHorarios() {
    const tratamientoNombre = tratamientoSelect.value;
    const fechaSeleccionada = fechaInput.value;
    const tratamientoOption = [...tratamientoSelect.options].find(
      (opt) => opt.value === tratamientoNombre
    );
    const tratamientoId = tratamientoOption?.getAttribute("data-id");

    if (tratamientoId && fechaSeleccionada) {
      // Petición a la API para obtener horarios disponibles
      fetch(
        `/api/horarios/?tratamiento_id=${tratamientoId}&fecha=${fechaSeleccionada}`
      )
        .then((response) => response.json())
        .then((data) => {
          listaHorarios.innerHTML = ""; // Limpia horarios anteriores
          formFinal.style.display = "none"; // Oculta el formulario

          if (data.horarios.length > 0) {
            // Por cada horario disponible, crea un botón seleccionable
            data.horarios.forEach((hora) => {
              const div = document.createElement("div");
              div.className = "opcion-hora";
              div.textContent = hora;
              div.addEventListener("click", function () {
                if (!div.classList.contains("activo")) {
                  seleccionarHora(hora);
                }
              });
              listaHorarios.appendChild(div);
            });
            bloqueHorarios.style.display = "block"; // Muestra el bloque de horarios
          } else {
            // Muestra mensaje si no hay horarios disponibles
            listaHorarios.innerHTML =
              '<div class="text-danger fw-semibold">No hay horarios disponibles para esta fecha</div>';
          }
        });
    }
  }

  // Función que se ejecuta al seleccionar una hora
  function seleccionarHora(hora) {
    // Quitar clase activa a todas las opciones
    document
      .querySelectorAll(".opcion-hora")
      .forEach((h) => h.classList.remove("activo"));
    event.target.classList.add("activo"); // Marcar la hora seleccionada

    // Actualiza el resumen de selección
    resumenSeleccion.innerText = `${tratamientoSelect.value} | ${fechaInput.value} | ${hora}`;
    // Asigna los valores al formulario oculto
    inputTratamiento.value = tratamientoSelect.value;
    inputFecha.value = fechaInput.value;
    inputHora.value = hora;

    // Muestra el formulario final y hace scroll hacia él
    formFinal.style.display = "block";
    formFinal.scrollIntoView({ behavior: "smooth", block: "start" });

    // Deshabilita el resto de opciones para evitar doble selección
    document.querySelectorAll(".opcion-hora").forEach((h) => {
      h.style.pointerEvents = "none";
      h.style.opacity = "0.6";
    });
  }

  // Formateo automático del número de teléfono mientras se escribe
  inputContacto.addEventListener("input", function (e) {
    let val = e.target.value.replace(/\D/g, ""); // Elimina todo lo que no sea número
    if (val.length > 4) {
      val = val.slice(0, 4) + "-" + val.slice(4, 8); // Aplica el formato 8888-8888
    }
    e.target.value = val;
  });

  // Validación y envío del formulario
  formFinal.addEventListener("submit", function (e) {
    e.preventDefault(); // Previene el envío por defecto

    if (yaEnviado) return; // Evita múltiples envíos

    let errores = [];
    const nombre = inputNombre.value.trim();
    const contacto = inputContacto.value.trim();
    const tratamiento = inputTratamiento.value.trim();
    const fecha = inputFecha.value.trim();
    const hora = inputHora.value.trim();

    // Expresiones regulares para validar nombre y teléfono
    const regexNombre = /^[A-Za-zÀ-ſ\s]{3,}$/;
    const regexTelefono = /^(2|6|7|8)\d{3}-\d{4}$/;

    // Validación de nombre
    if (!regexNombre.test(nombre)) {
      errores.push("⚠️ Ingresá un nombre válido (mínimo 3 letras, solo letras y espacios).");
    }

    // Validación de número de contacto
    if (!regexTelefono.test(contacto)) {
      errores.push("⚠️ El número debe empezar en 2, 6, 7 o 8 y tener el formato correcto: 8888-8888.");
    }

    // Validaciones básicas de campos obligatorios
    if (!tratamiento) errores.push("⚠️ Seleccioná un tratamiento.");
    if (!fecha) errores.push("⚠️ Seleccioná una fecha válida.");
    if (!hora) errores.push("⚠️ Seleccioná un horario disponible.");

    if (errores.length > 0) {
      // Si hay errores, mostrar alerta con SweetAlert
      Swal.fire({
        icon: "error",
        title: "Corregí estos errores:",
        html: errores.join("<br>"),
        confirmButtonColor: "#5dc1b9",
        background: "#fff",
      });
    } else {
      // Si todo está bien, bloquea el botón y envía el formulario
      yaEnviado = true;
      submitBtn.disabled = true;
      submitBtn.innerHTML = `<span class="spinner-border spinner-border-sm" role="status"></span> Cargando...`;
      formFinal.submit(); // Envía el formulario
    }
  });

});