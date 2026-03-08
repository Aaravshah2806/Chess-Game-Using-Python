function launchGame() {
  const container = document.getElementById("game-container");
  const frame = document.getElementById("game-frame");
  const closeBtn = document.getElementById("close-game-btn");

  // Show the game container and loader
  container.classList.remove("hidden");
  const loader = document.getElementById("loader");
  loader.classList.remove("hidden");

  // Hide iframe & remove animation class initially
  frame.classList.add("hidden");
  frame.classList.remove("loaded");
  closeBtn.classList.add("hidden");

  // Load the pygbag game with settings passed via Hash
  const diffSelect = document.getElementById("difficulty-select");
  const timeSelect = document.getElementById("timer-select");
  const mode = diffSelect.value;
  const time = timeSelect.value;
  frame.src = `game_view/index.html#mode=${mode}&time=${time}`;

  const closeGame = () => {
    container.classList.add("hidden");
    frame.src = "";
    frame.classList.remove("loaded");
    window.removeEventListener("keydown", parentHandle);
    closeBtn.removeEventListener("click", closeGame);
  };

  const parentHandle = (e) => {
    if (e.key === "Escape") closeGame();
  };

  window.addEventListener("keydown", parentHandle);
  closeBtn.addEventListener("click", closeGame);

  frame.onload = () => {
    setTimeout(() => {
      loader.classList.add("hidden");
      frame.classList.remove("hidden");
      closeBtn.classList.remove("hidden");

      // Trigger CSS transition
      requestAnimationFrame(() => {
        frame.classList.add("loaded");
      });

      frame.contentWindow.focus();
    }, 4000);

    try {
      frame.contentWindow.addEventListener("keydown", (e) => {
        if (e.key === "Escape") closeGame();
      });
      frame.contentWindow.focus();
    } catch (err) {
      console.warn("Could not attach key listener to iframe:", err);
    }
  };
}

// Logic to hide Timer when playing against AI
document.addEventListener("DOMContentLoaded", () => {
  const diffSelect = document.getElementById("difficulty-select");
  const timeGroup = document.getElementById("time-group");

  const toggleTimerVisibility = () => {
    if (diffSelect.value !== "player") {
      timeGroup.classList.add("hidden");
    } else {
      timeGroup.classList.remove("hidden");
    }
  };

  // Run on load
  toggleTimerVisibility();

  // Run on change
  diffSelect.addEventListener("change", toggleTimerVisibility);
});

// ----------------------------------------------------
// New Loading Screen Logic
// ----------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
  const squares = document.querySelectorAll(".loading-square");
  if (squares.length === 0) return;

  let currentSquare = 0;

  function updateLoadingBar() {
    if (currentSquare < squares.length) {
      squares[currentSquare].classList.add("filled");
      currentSquare++;
    } else {
      squares.forEach((sq) => sq.classList.remove("filled"));
      currentSquare = 0;
    }
  }

  setInterval(updateLoadingBar, 600);

  // Floating Ghost Pieces Logic
  const ghostContainer = document.getElementById("ghost-container");
  if (!ghostContainer) return;

  const pieceSymbols = ["♟", "♞", "♝", "♜"];
  const numGhosts = 6;

  function createGhostPiece() {
    const ghostRef = document.createElement("div");
    ghostRef.className = "ghost-piece";

    const startX = 15 + Math.random() * 70; // 15vw - 85vw
    const startY = 15 + Math.random() * 70; // 15vh - 85vh
    ghostRef.style.left = `${startX}vw`;
    ghostRef.style.top = `${startY}vh`;

    const dx = (Math.random() - 0.5) * 350 + "px";
    const dy = (Math.random() - 0.5) * 350 + "px";
    const rot = (Math.random() - 0.5) * 120 + "deg";

    ghostRef.style.setProperty("--dx", dx);
    ghostRef.style.setProperty("--dy", dy);
    ghostRef.style.setProperty("--rot", rot);

    const driftDuration = 12 + Math.random() * 15;
    const fadeDuration = 4 + Math.random() * 4;

    ghostRef.style.animation = `
            drift ${driftDuration}s ease-in-out infinite alternate, 
            fadeOutIn ${fadeDuration}s ease-in-out infinite alternate
        `;

    ghostRef.style.animationDelay = `-${Math.random() * 20}s, -${Math.random() * 10}s`;

    const inner = document.createElement("div");
    inner.textContent =
      pieceSymbols[Math.floor(Math.random() * pieceSymbols.length)];
    const sizeScale = 0.8 + Math.random() * 1.5;
    inner.style.transform = `scale(${sizeScale})`;

    ghostRef.appendChild(inner);
    ghostContainer.appendChild(ghostRef);
  }

  for (let i = 0; i < numGhosts; i++) {
    createGhostPiece();
  }
});
