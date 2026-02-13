// Usuarios de ejemplo
const usuarios = [
  { nombre: "Luna", especie: "Lobo", orientacion: "Lesbiana", rol: "Therian", intereses: ["Arte", "Gaming"], likes: [], matches: [] },
  { nombre: "Kai", especie: "Zorro", orientacion: "Bisexual", rol: "Furry", intereses: ["Música", "Anime"], likes: [], matches: [] },
  { nombre: "Mika", especie: "Felino", orientacion: "Pansexual", rol: "Ambos", intereses: ["Roleplay", "Espiritualidad"], likes: [], matches: [] }
];

let currentIndex = 0;
const currentUser = { nombre: "Tú", likes: [], matches: [] };

function mostrarUsuario(index) {
  const contenedor = document.getElementById("cardContainer");
  contenedor.innerHTML = "";
  if (index >= usuarios.length) {
    contenedor.innerHTML = "<p>No hay más usuarios disponibles.</p>";
    return;
  }
  const u = usuarios[index];
  const card = document.createElement("div");
  card.className = "card";
  card.innerHTML = `
    <h2>${u.nombre}</h2>
    <p><strong>Especie:</strong> ${u.especie}</p>
    <p><strong>Orientación:</strong> ${u.orientacion}</p>
    <p><strong>Rol:</strong> ${u.rol}</p>
    <p><strong>Intereses:</strong> ${u.intereses.join(", ")}</p>
  `;
  contenedor.appendChild(card);

  // Drag/swipe
  let startX = 0;
  let currentX = 0;

  card.addEventListener("mousedown", e => {
    startX = e.clientX;
    card.style.transition = "none";
  });

  card.addEventListener("mousemove", e => {
    if (startX !== 0) {
      currentX = e.clientX - startX;
      card.style.transform = `translateX(${currentX}px) rotate(${currentX/20}deg)`;
    }
  });

  card.addEventListener("mouseup", () => {
    if (currentX > 100) {
      darLike(u);
      card.style.transform = "translateX(1000px)";
      card.style.opacity = "0";
      setTimeout(() => {
        currentIndex++;
        mostrarUsuario(currentIndex);
      }, 300);
    } else if (currentX < -100) {
      skipUser();
      card.style.transform = "translateX(-1000px)";
      card.style.opacity = "0";
      setTimeout(() => {
        currentIndex++;
        mostrarUsuario(currentIndex);
      }, 300);
    } else {
      card.style.transition = "transform 0.3s ease";
      card.style.transform = "translateX(0)";
    }
    startX = 0;
    currentX = 0;
  });
}

function darLike(u) {
  currentUser.likes.push(u.nombre);
  if (u.likes.includes(currentUser.nombre)) {
    currentUser.matches.push(u.nombre);
    u.matches.push(currentUser.nombre);
    mostrarMatch(u.nombre);
  }
}

function skipUser() {
  // simplemente pasa al siguiente
}

function mostrarMatch(nombre) {
  const matchesDiv = document.getElementById("matches");
  matchesDiv.innerHTML += `<p>¡Match con ${nombre}! 🎉</p>`;
}

// Mostrar primer usuario
mostrarUsuario(currentIndex);