# 🔍 HandsCheck V2: Crypto Wallet Analyzer

**HandsCheck** is a specialized tool that analyzes Ethereum and Bitcoin wallet behavior over a 7-day window. It provides a real-time "Verdict" by combining activity levels with holding patterns to identify the psychological profile of a wallet owner.

---

## 🚀 New in V2.0
- **7-Day Deep Scan:** Analyzes transaction history over the last week (~50,400 blocks for ETH / ~1,008 blocks for BTC).
- **Double-Label Logic:** Assigns a dual status (e.g., *ACTIVE TRADER | DIAMOND HANDS*).
- **Refactored Engine:** Optimized Python code for faster API processing and cleaner data visualization.

## 🛠️ Tech Stack
- **Backend:** Python (FastAPI)
- **Frontend:** HTML5, CSS3, JavaScript
- **APIs:** Etherscan (ETH), Blockchain.info (BTC)
- **Deployment:** Replit / GitHub

## ⚙️ Setup & Installation
1. **Clone the repository:**
   `git clone https://github.com/YOUR_USERNAME/handscheck.git`
2. **Install dependencies:**
   `pip install -r requirements.txt`
3. **Environment Variables:**
   Create a secret for `ETHERSCAN_API_KEY` in your hosting environment.
4. **Run the app:**
   `python main.py`

## 🧠 The Verdict Logic
The app uses a proprietary scoring system based on the last 7 days:
- 💎 **Diamond Hands:** Majority of transactions are "Incoming" (Holding).
- 🧻 **Paper Hands:** High frequency of "Outgoing" transactions (Selling).
- 🔴 **Degen Trader:** 40+ transactions per week.
- 🟢 **Patient Holder:** Low-frequency, high-conviction moves.

## ⚖️ License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
