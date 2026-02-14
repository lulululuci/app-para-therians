const contenedor = document.getElementById("contenedorCards");
const btnSi = document.getElementById("btnSi");
const btnNo = document.getElementById("btnNo");

let likes = JSON.parse(localStorage.getItem("likes")) || [];
let matches = JSON.parse(localStorage.getItem("matches")) || [];

const usuariosMock = [
  {
    id: 1,
    nombre: "Luna",
    especie: "Lobo",
    bio: "Amante de la luna 🌙",
    intereses: ["Arte", "Gaming"],
    likes: [99]
  },
  {
    id: 2,
    nombre: "Kai",
    especie: "Zorro",
    bio: "Música y anime",
    intereses: ["Música", "Anime"],
    likes: []
  }
];

let indiceActual = 0;

function mostrarUsuario() {
  contenedor.innerHTML = "";

  if (indiceActual >= usuariosMock.length) {
    contenedor.innerHTML = "<p>No hay más perfiles</p>";
    return;
  }

  const u = usuariosMock[indiceActual];

  const card = document.createElement("div");
  card.className = "card";
  card.innerHTML = `
    <h2>${u.nombre}</h2>
    <p><strong>Especie:</strong> ${u.especie}</p>
    <p>${u.bio}</p>
    <p><strong>Intereses:</strong> ${u.intereses.join(", ")}</p>
  `;

  contenedor.appendChild(card);

  // ---------- SWIPE ----------
  let inicioX = 0;
  let moviendo = false;

  card.addEventListener("mousedown", e => {
    inicioX = e.clientX;
    moviendo = true;
    card.style.transition = "none";
  });

  document.addEventListener("mousemove", e => {
    if (!moviendo) return;
    const desplazamiento = e.clientX - inicioX;
    card.style.transform = `translateX(${desplazamiento}px) rotate(${desplazamiento / 15}deg)`;
  });

  document.addEventListener("mouseup", e => {
    if (!moviendo) return;
    moviendo = false;

    const desplazamiento = e.clientX - inicioX;
    card.style.transition = "transform 0.3s ease";

    if (desplazamiento > 120) btnSi.click();
    else if (desplazamiento < -120) btnNo.click();
    else card.style.transform = "translateX(0)";
  });
}

// ---------- BOTÓN ----------
btnSi.addEventListener("click", () => {
  const card = document.querySelector(".card");
  if (!card) return;

  const usuario = usuariosMock[indiceActual];

  likes.push(usuario.id);
  localStorage.setItem("likes", JSON.stringify(likes));

  if (usuario.likes.includes(99)) {
    matches.push(usuario.id);
    localStorage.setItem("matches", JSON.stringify(matches));
    alert(`¡Match con ${usuario.nombre}! 🐾`);
  }

  card.classList.add("salida-derecha");

  setTimeout(() => {
    indiceActual++;
    mostrarUsuario();
  }, 300);
});

// ---------- BOTÓN ----------
btnNo.addEventListener("click", () => {
  const card = document.querySelector(".card");
  if (!card) return;

  card.classList.add("salida-izquierda");

  setTimeout(() => {
    indiceActual++;
    mostrarUsuario();
  }, 300);
});

mostrarUsuario();
