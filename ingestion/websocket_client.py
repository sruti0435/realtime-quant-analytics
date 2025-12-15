import json
import websocket
from ingestion.tick_buffer import add_tick

def on_message(ws, message):
    data = json.loads(message)
    tick = {
        "timestamp": data["E"],
        "symbol": data["s"],
        "price": float(data.get("p", data.get("c", 0))),
        "qty": float(data["q"])
    }
    add_tick(tick)

def start_ws(symbols):
    streams = "/".join([f"{s.lower()}@trade" for s in symbols])
    url = f"wss://stream.binance.com:9443/ws/{streams}"
    ws = websocket.WebSocketApp(url, on_message=on_message)
    ws.run_forever()
