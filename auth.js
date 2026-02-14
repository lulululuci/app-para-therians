const form = document.getElementById("registerForm");
const error = document.getElementById("error");

form.addEventListener("submit", e => {
  e.preventDefault();

  const nombre = document.getElementById("nombre").value.trim();
  const años = parseInt(document.getElementById("años").value);
  const rol = document.getElementById("rol").value;
  const orientacion = document.getElementById("orientacion").value;

  if (!nombre || !años || !rol || !orientacion) {
    error.textContent = "Completa todos los campos";
    return;
  }

  if (años < 18) {
    error.textContent = "Debes ser mayor de 18 años";
    return;
  }

  const userData = {
    nombre,
    años,
    rol,
    orientacion
  };

  console.log("Enviar datos:", userData);

  // Cuando esté listo el backend, voy a enviar estos datos al servidor con un POST.
// El backend se va a encargar de validar, guardar el usuario y devolver la respuesta.
/*
fetch("http://localhost:3000/register", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(userData)
})
.then(res => res.json())
.then(data => console.log(data))
.catch(err => console.error(err));
*/

});
