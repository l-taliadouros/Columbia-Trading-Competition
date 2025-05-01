import asyncio
import websockets
import json
import random
import time

price_data = {
    "AD": [100.0],
    "TS": [200.0],
    "TT": [300.0]
}

price_enforcer_bid = {
    "AD": 99.0,
    "TS": 198.0,
    "TT": 297.0
}
price_enforcer_ask = {
    "AD": 101.0,
    "TS": 202.0,
    "TT": 303.0
}

def simulate_next_price(asset):
    drift = random.uniform(-0.1, 0.1)
    volatility = random.uniform(0.05, 0.3)
    last_price = price_data[asset][-1]
    new_price = last_price + drift + volatility * random.choice([-1, 1])
    new_price = max(1, round(new_price, 2))
    price_data[asset].append(new_price)
    return new_price

def build_gamestate():
    state = {"GameState": {}}
    for asset in ["AD", "TS", "TT"]:
        simulate_next_price(asset)
        order_book_bids = [{"price": price_data[asset][-1] - 0.5, "qty": random.randint(10, 50)} for _ in range(3)]
        order_book_asks = [{"price": price_data[asset][-1] + 0.5, "qty": random.randint(10, 50)} for _ in range(3)]
        state["GameState"][asset] = {
            "price_history": [[time.time(), p] for p in price_data[asset][-20:]],
            "price_enforcer_bid": price_enforcer_bid[asset],
            "price_enforcer_ask": price_enforcer_ask[asset],
            "buy_side_limit_levels": order_book_bids,
            "sell_side_limit_levels": order_book_asks
        }
    return json.dumps(state)

async def mock_feed(websocket, path=None):
    print("Client connected to mock feed.")
    try:
        while True:
            message = build_gamestate()
            await websocket.send(message)
            await asyncio.sleep(1)
    except websockets.ConnectionClosed:
        print("Client disconnected.")

async def main():
    print("Starting mock WebSocket server on ws://localhost:8765")
    async with websockets.serve(mock_feed, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
