# 💎 HandsCheck

**HandsCheck** is a minimalist, on-chain wallet behavior analyzer. It scans Bitcoin (BTC) and Ethereum (ETH) activity over the last 24 hours to give users a blunt, honest verdict on their "hand strength."

Are you **Diamond Hands**, or are you just **Exit Liquidity**?

![HandsCheck Preview](https://img.shields.io/badge/Blockchain-Analysis-blueviolet)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🚀 Features

- **Multi-Chain Support:** Analyze both Bitcoin and Ethereum addresses.
- **Real-Time Data:** Fetches the most recent transactions using Etherscan and Blockstream APIs.
- **Behavioral Analysis:** Uses custom logic to determine if a wallet is:
  - 💎 **Diamond Hands:** No sells, just pure conviction.
  - 🧻 **Paper Hands:** Sold the dip or panicked early.
  - 🚪 **Exit Liquidity:** Sold a massive percentage of holdings.
  - 😬 **Weak Conviction:** Constant indecisive swapping.
- **Responsive UI:** Dark/Light mode support with a sleek "Glassmorphism" design.

---

## 🛠️ Tech Stack

- **Backend:** Python, FastAPI, Uvicorn
- **Data Fetching:** HTTPX (Asynchronous)
- **Frontend:** HTML5, CSS3 (Vanilla JS)
- **APIs:** Etherscan (ETH), Blockstream (BTC)

---

## 📂 Project Structure

```text
handscheck/
├── main.py            # FastAPI Application & Routing
├── eth.py             # Ethereum Blockchain Logic
├── btc.py             # Bitcoin Blockchain Logic
├── verdict.py         # The "Brain" (Scoring Logic)
├── requirements.txt   # Dependencies
├── .gitignore         # Safety (Hides .env)
└── static/            # Frontend Assets
    └── index.html     # The UI
