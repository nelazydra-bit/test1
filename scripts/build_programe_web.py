import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = (
    "A.png",
    "B.png",
    "C.png",
    "D.png",
    "False_sound.ogg",
    "NPC.png",
    "True_sound.ogg",
    "bg_ground_new.ogg",
    "answer2_false1.png",
    "answer2_false2.png",
    "answer2_false3.png",
    "answer2_true.png",
    "answer_false1.jpg",
    "answer_false2.jpg",
    "answer_false3.jpg",
    "answer_true.jpg",
    "answer_false1.png",
    "answer_false2.png",
    "answer_false3.png",
    "answer_true.png",
    "duty_box1.jpg",
    "duty_box2.jpg",
    "duty_box3.jpg",
    "home1.png",
    "home2.png",
    "land_sky.png",
    "note1.png",
    "note2.png",
    "note3.png",
    "note4.png",
    "nothing.png",
    "player_walk_left1.png",
    "player_walk_left2.png",
    "player_walk_right1.png",
    "player_walk_right2.png",
    "question1.jpg",
    "question2.jpg",
    "question3.jpg",
    "sky.jpg",
    "stopper.png",
    "tree.png",
    "way.png",
    "wrong1.png",
    "wrong_mode2.png",
)


def main():
    with tempfile.TemporaryDirectory(prefix="healing-english-") as temp_dir:
        app_dir = Path(temp_dir) / "healing_english"
        app_dir.mkdir()
        shutil.copy2(ROOT / "programe" / "main.py", app_dir / "main.py")
        for asset in ASSETS:
            shutil.copy2(ROOT / asset, app_dir / asset)
        shutil.copy2(ROOT / "favicon.png", app_dir / "favicon.png")

        subprocess.run(
            [
                sys.executable,
                "-X",
                "utf8",
                "-m",
                "pygbag",
                "--build",
                "--title",
                "Healing English",
                "--ume_block",
                "0",
                "--icon",
                str(app_dir / "favicon.png"),
                str(app_dir),
            ],
            check=True,
        )

        web_build = app_dir / "build" / "web"
        if not (web_build / "index.html").is_file():
            raise FileNotFoundError(f"Pygbag did not produce {web_build / 'index.html'}")

        output = ROOT / "build" / "programe-web"
        if output.exists():
            shutil.rmtree(output)
        shutil.copytree(web_build, output)
        shutil.copy2(ROOT / "bg_ground_new.ogg", output / "bg_ground_new.ogg")

        index = output / "index.html"
        html = index.read_text(encoding="utf-8")
        music_control = """
<style>
#background-music-toggle { position: fixed; z-index: 10000; top: 12px; right: 12px; padding: 10px 14px; cursor: pointer; }
</style>
<audio id="background-music" loop preload="none">
  <source src="bg_ground_new.ogg" type="audio/ogg">
</audio>
<button id="background-music-toggle" type="button" aria-pressed="false">Play background music</button>
<script>
(() => {
  const audio = document.getElementById("background-music");
  const button = document.getElementById("background-music-toggle");
  button.addEventListener("click", () => {
    if (!audio.paused) {
      audio.pause();
      button.textContent = "Play background music";
      button.setAttribute("aria-pressed", "false");
      return;
    }

    audio.play().then(() => {
      button.textContent = "Pause background music";
      button.setAttribute("aria-pressed", "true");
    }).catch((error) => {
      button.textContent = "Tap to retry background music";
      console.error("Background music playback failed:", error);
    });
  });
})();
</script>
"""
        if "</body>" not in html:
            raise ValueError("Pygbag output is missing the closing body tag")
        index.write_text(html.replace("</body>", music_control + "</body>"), encoding="utf-8")


if __name__ == "__main__":
    main()
