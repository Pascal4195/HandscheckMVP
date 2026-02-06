"""
HandsCheck Backend API
Main FastAPI application for wallet behavior analysis
"""

import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles # Needed to serve index.html
from pydantic import BaseModel
from dotenv import load_dotenv

# Import your custom modules
from btc import BTCAnalyzer
from eth import ETHAnalyzer
from verdict import calculate_verdict # Ensure this matches your function name in verdict.py

# Load environment variables (Etherscan key from .env or Replit Secrets)
load_dotenv()

app = FastAPI(
    title="HandsCheck API",
    description="On-chain wallet behavior analyzer",
    version="1.0.0"
)

# CORS allows your frontend to talk to your backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODELS ---

class AnalysisRequest(BaseModel):
    address: str
    asset: str  # 'BTC' or 'ETH'

class AnalysisResponse(BaseModel):
    verdict: str
    description: str
    address: str
    asset: str

# --- API ENDPOINTS ---

@app.get("/health")
async def health_check():
    """Check if the API keys are loaded correctly"""
    eth_key = os.getenv('ETHERSCAN_API_KEY')
    return {
        "status": "healthy",
        "eth_key_detected": bool(eth_key and eth_key != "YOUR_KEY_HERE"),
        "btc_ready": True
    }

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_wallet(request: AnalysisRequest):
    asset = request.asset.upper()
    address = request.address.strip()

    if not address:
        raise HTTPException(status_code=400, detail="Address is required")
    
    try:
        # Choose the right engine
        if asset == 'BTC':
            analyzer = BTCAnalyzer()
            wallet_data = await analyzer.get_wallet_data(address)
        elif asset == 'ETH':
            analyzer = ETHAnalyzer()
            wallet_data = await analyzer.get_wallet_data(address)
        else:
            raise HTTPException(status_code=400, detail="Invalid asset. Use BTC or ETH.")

        # Get the verdict from your brain module
        # wallet_data should contain 'transactions' and 'balance_info'
        result = calculate_verdict(
            wallet_data['transactions'],
            wallet_data['balance_info']
        )

        return AnalysisResponse(
            verdict=result['verdict'],
            description=result['description'],
            address=address,
            asset=asset
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- THE STATIC BRIDGE ---
# This MUST be at the bottom so it doesn't interfere with your /analyze route.
# It tells FastAPI: "Look inside the 'static' folder for index.html"
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    # Use port 8080 for Replit compatibility
    port = int(os.getenv("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
