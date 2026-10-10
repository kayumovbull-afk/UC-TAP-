"""webapp/app.tpl.html dan Telegram uchun webapp/index.html ni yig'adi.

app.tpl.html: sarlavha + uslub + markup + skript. Yig'ishda ichiga tanga rasmi (uc-coin.jpg)
va sinov rejimi uchun o'yinlar ro'yxati (catalog.json) joylanadi.
Telegram ichida SDK ulanadi (haqiqiy rejim), oddiy brauzerda esa SDK yo'q, shuning uchun
sahifa o'zi sinov rejimiga o'tadi (localStorage bilan).
"""
import base64
import json
from pathlib import Path

root = Path(__file__).parent
web = root / "webapp"
src = (web / "app.tpl.html").read_text(encoding="utf-8")
coin = "data:image/jpeg;base64," + base64.b64encode((web / "uc-coin.jpg").read_bytes()).decode()
catalog = json.loads((root / "catalog.json").read_text(encoding="utf-8"))
MIME = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp", ".svg": "image/svg+xml"}
for g in catalog:  # o'yin rasmlari: webapp/games/<id>.jpg|png|webp
    for ext, mime in MIME.items():
        f = web / "games" / (g["id"] + ext)
        if f.exists():
            g["image"] = f"data:{mime};base64," + base64.b64encode(f.read_bytes()).decode()
            break
STARS = {60: 70, 120: 140, 180: 210, 240: 280, 325: 380}  # server.py dagi STAR_PACKS bilan bir xil (sinov uchun)
for g in catalog:  # PUBG paketlariga Stars narxi
    for pk in g.get("packages", []):
        n = pk["title"].split()[0] if g["id"] == "pubg" else ""
        if n.isdigit() and int(n) in STARS and "stars" not in pk:
            pk["stars"] = STARS[int(n)]
for g in catalog:  # ilova kutadigan maydonlar
    g.setdefault("short", g["name"][:2].upper())
    g.setdefault("color", "#556677")
    g.setdefault("id_label", "O’yin ID")
    g.setdefault("id_pattern", ".{3,64}")
    g.setdefault("popular", False)
src = src.replace("__COIN__", coin).replace("__CATALOG__", json.dumps(catalog, ensure_ascii=False).replace("</", "<\\/"))
head = (
    '<!doctype html>\n<html lang="uz">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">\n'
    '<script src="https://telegram.org/js/telegram-web-app.js"></script>\n'
)
(web / "index.html").write_text(head + src + "\n</body>\n</html>\n", encoding="utf-8")
print("webapp/index.html tayyor", len(src) // 1024, "KB")
