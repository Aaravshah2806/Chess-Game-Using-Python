function launchGame() {
  const container = document.getElementById("game-container");
  const frame = document.getElementById("game-frame");

  // Show the game container and loader
  container.classList.remove("hidden");
  const loader = document.getElementById("loader");
  loader.classList.remove("hidden");
  frame.classList.add("hidden");

  // Load the pygbag game
  frame.src = "game_view/index.html";

  const closeGame = () => {
    container.classList.add("hidden");
    frame.src = "";
    window.removeEventListener("keydown", parentHandle);
  };

  const parentHandle = (e) => {
    if (e.key === "Escape") closeGame();
  };

  window.addEventListener("keydown", parentHandle);

  frame.onload = () => {
    setTimeout(() => {
      loader.classList.add("hidden");
      frame.classList.remove("hidden");
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
