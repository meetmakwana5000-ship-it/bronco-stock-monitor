import os
import requests
from bs4 import BeautifulSoup

URL = "https://broncopolos.com/buy/black-batman-compression-tshirt-for-men.html"

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


def send_telegram(message):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": message
        },
        timeout=20
    )


def check_stock():
    response = requests.get(
        URL,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    sizes = {}

    for size in ["M", "L"]:
        available = False

        for element in soup.find_all(
            string=lambda text: text and text.strip() == size
        ):
            parent = element.parent.parent
            html = str(parent)

            if (
                "line-through" not in html
                and "text-decoration:line-through" not in html
            ):
                available = True
                break

        sizes[size] = available

    return sizes["M"], sizes["L"]


try:
    m_available, l_available = check_stock()

    print(f"M: {m_available} | L: {l_available}")

    if m_available and l_available:
        send_telegram(
            "🚨 BRONCO STOCK ALERT!\n\n"
            "Batman Compression Tshirt\n"
            "✅ M available\n"
            "✅ L available\n\n"
            + URL
        )

except Exception as e:
    print(f"Error: {e}")
