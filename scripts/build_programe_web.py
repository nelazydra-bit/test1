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


if __name__ == "__main__":
    main()
