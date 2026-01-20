async function launchGame() {
  const btn = document.getElementById("play-btn");
  const status = document.getElementById("status");

  btn.disabled = true;
  btn.innerText = "LAUNCHING...";
  status.innerText = "Starting Chess Engine...";

  try {
    const res = await fetch("/launch", { method: "POST" });
    const data = await res.json();

    if (data.success) {
      status.innerText = "Game Running!";
      setTimeout(() => {
        btn.disabled = false;
        btn.innerText = "PLAY GAME";
        status.innerText = "";
      }, 3000);
    } else {
      status.innerText = "Error: " + data.message;
      btn.disabled = false;
      btn.innerText = "PLAY GAME";
    }
  } catch (e) {
    console.error(e);
    status.innerText = "Connection Error";
    btn.disabled = false;
    btn.innerText = "PLAY GAME";
  }
}
