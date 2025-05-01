// mock_competition_feed.js

import { WebSocketServer } from 'ws';

const server = new WebSocketServer({ port: 9000 });
console.log("Mock competition feed running on ws://localhost:9000");

function generateMockGameState() {
  const now = Date.now();
  return {
    GameState: {
      TS: {
        price_history: Array.from({ length: 20 }, (_, i) => [now - i * 1000, 80 + Math.random() * 5]),
        price_enforcer_bid: 82.5,
        price_enforcer_ask: 83.5,
        buy_side_limit_levels: [{ price: 82, qty: 15 }, { price: 81.5, qty: 10 }],
        sell_side_limit_levels: [{ price: 84, qty: 15 }, { price: 84.5, qty: 10 }]
      },
      AD: {
        price_history: Array.from({ length: 20 }, (_, i) => [now - i * 1000, 50 + Math.random() * 3]),
        price_enforcer_bid: 51,
        price_enforcer_ask: 52,
        buy_side_limit_levels: [{ price: 50.5, qty: 20 }],
        sell_side_limit_levels: [{ price: 52.5, qty: 20 }]
      },
      TT: {
        price_history: Array.from({ length: 20 }, (_, i) => [now - i * 1000, 95 + Math.random() * 2]),
        price_enforcer_bid: 96,
        price_enforcer_ask: 97,
        buy_side_limit_levels: [{ price: 95.5, qty: 10 }],
        sell_side_limit_levels: [{ price: 97.5, qty: 10 }]
      }
    }
  };
}

server.on('connection', (socket) => {
  console.log("Connected to mock server.");

  const interval = setInterval(() => {
    const message = JSON.stringify(generateMockGameState());
    socket.send(message);
  }, 1000); // every second

  socket.on('close', () => {
    console.log("Client disconnected.");
    clearInterval(interval);
  });
});
