import os, requests, yaml
from datetime import datetime
from zoneinfo import ZoneInfo

VENTANA = 5  # minutos, igual que el intervalo del cron
cfg = yaml.safe_load(open("reminders.yml", encoding="utf-8"))
ahora = datetime.now(ZoneInfo(cfg["timezone"]))
dias = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

# Local
#from dotenv import load_dotenv
#load_dotenv()

for r in cfg["reminders"]:
    if dias[ahora.weekday()] not in r.get("days", dias):
        continue

    # Acepta "times" (lista) o "time" (una sola hora)
    horas = r.get("times") or [r["time"]]

    for hora in horas:
        h, m = map(int, hora.split(":"))
        programado = ahora.replace(hour=h, minute=m, second=0, microsecond=0)
        minutos = (ahora - programado).total_seconds() / 60
        if 0 <= minutos < VENTANA:
            requests.post(
                f"https://api.telegram.org/bot{os.environ['TELEGRAM_TOKEN']}/sendMessage",
                data={"chat_id": os.environ["CHAT_ID"], "text": r["text"]},
            )