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

  // Load the pygbag game
  frame.src = "game_view/index.html";

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
    }, 1000);

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
