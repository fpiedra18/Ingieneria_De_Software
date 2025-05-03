// static/js/agendar_protegido.js

document.addEventListener("DOMContentLoaded", function () {
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

  let yaEnviado = false;

  flatpickr("#calendarContainer", {
    inline: true,
    minDate: fechaInput.getAttribute("data-fecha-hoy"),
    dateFormat: "Y-m-d",
    locale: {
      firstDayOfWeek: 1,
    },
    onChange: function (selectedDates, dateStr) {
      fechaInput.value = dateStr;
      cargarHorarios();
    },
  });

  tratamientoSelect.addEventListener("change", cargarHorarios);

  function cargarHorarios() {
    const tratamientoNombre = tratamientoSelect.value;
    const fechaSeleccionada = fechaInput.value;
    const tratamientoOption = [...tratamientoSelect.options].find(
      (opt) => opt.value === tratamientoNombre
    );
    const tratamientoId = tratamientoOption?.getAttribute("data-id");

    if (tratamientoId && fechaSeleccionada) {
      fetch(
        `/api/horarios/?tratamiento_id=${tratamientoId}&fecha=${fechaSeleccionada}`
      )
        .then((response) => response.json())
        .then((data) => {
          listaHorarios.innerHTML = "";
          formFinal.style.display = "none";

          if (data.horarios.length > 0) {
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
            bloqueHorarios.style.display = "block";
          } else {
            listaHorarios.innerHTML =
              '<div class="text-danger fw-semibold">No hay horarios disponibles para esta fecha</div>';
          }
        });
    }
  }

  function seleccionarHora(hora) {
    document
      .querySelectorAll(".opcion-hora")
      .forEach((h) => h.classList.remove("activo"));
    event.target.classList.add("activo");

    resumenSeleccion.innerText = `${tratamientoSelect.value} | ${fechaInput.value} | ${hora}`;
    inputTratamiento.value = tratamientoSelect.value;
    inputFecha.value = fechaInput.value;
    inputHora.value = hora;

    formFinal.style.display = "block";
    formFinal.scrollIntoView({ behavior: "smooth", block: "start" });

    document.querySelectorAll(".opcion-hora").forEach((h) => {
      h.style.pointerEvents = "none";
      h.style.opacity = "0.6";
    });
  }

  inputContacto.addEventListener("input", function (e) {
    let val = e.target.value.replace(/\D/g, "");
    if (val.length > 4) {
      val = val.slice(0, 4) + "-" + val.slice(4, 8);
    }
    e.target.value = val;
  });

  formFinal.addEventListener("submit", function (e) {
    e.preventDefault();

    if (yaEnviado) return;

    let errores = [];
    const nombre = inputNombre.value.trim();
    const contacto = inputContacto.value.trim();
    const tratamiento = inputTratamiento.value.trim();
    const fecha = inputFecha.value.trim();
    const hora = inputHora.value.trim();

    const regexNombre = /^[A-Za-zÀ-ſ\s]{3,}$/;
    const regexTelefono = /^(2|6|7|8)\d{3}-\d{4}$/;

    if (!regexNombre.test(nombre)) {
      errores.push("⚠️ Ingresá un nombre válido (mínimo 3 letras, solo letras y espacios).");
    }

    if (!regexTelefono.test(contacto)) {
      errores.push("⚠️ El número debe empezar en 2, 6, 7 o 8 y tener el formato correcto: 8888-8888.");
    }

    if (!tratamiento) errores.push("⚠️ Seleccioná un tratamiento.");
    if (!fecha) errores.push("⚠️ Seleccioná una fecha válida.");
    if (!hora) errores.push("⚠️ Seleccioná un horario disponible.");

    if (errores.length > 0) {
      Swal.fire({
        icon: "error",
        title: "Corregí estos errores:",
        html: errores.join("<br>"),
        confirmButtonColor: "#5dc1b9",
        background: "#fff",
      });
    } else {
      // ✅ Bloquear segundo envío
      yaEnviado = true;
      submitBtn.disabled = true;
      submitBtn.innerHTML = `<span class="spinner-border spinner-border-sm" role="status"></span> Cargando...`;
      formFinal.submit();
    }
  });
  
});
