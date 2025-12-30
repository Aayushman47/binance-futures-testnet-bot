from binance import Client
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET_KEY")

client = Client(api_key, api_secret)

client.FUTURES_URL = "https://testnet.binancefuture.com"

try:
    balance = client.futures_account_balance()
    print("✅ Connection successful")
    print("USDT Balance:", balance)
except Exception as e:
    print("❌ Connection failed")
    print(e)