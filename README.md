# &nbsp;Binance Futures Testnet Trading Bot







This project is a simplified trading bot built in **Python** using the **Binance Futures Testnet**.

It was created as part of an internship hiring assignment to demonstrate Python Development API integration, clean code structure, and basic understanding of trading systems.



The focus of this project is **correct API usage, error handling, and extensibility**, not trading profitability.



---



## &nbsp;Disclaimer

## 

&nbsp;This project is for educational and evaluation purposes only.

&nbsp;It uses Binance Futures Testnet and does not place real trades or use real funds.

## 

## &nbsp;What this project does?



\- Connects to **Binance Futures Testnet** (no real money involved).

\- Places futures orders using the official Binance API.

\- Supports both CLI and a simple desktop UI.

\- Handles common Futures-specific requirements like leverage and margin type.

\- Demonstrates advanced order logic such as TWAP, Grid, and OCO (simulated).



---



### &nbsp;Features



\### Core functionality

\- Market orders.

\- Limit orders.

\- Buy and Sell sides.

\- USDT-M Futures Testnet support.

\- Command-line interface (CLI).

\- Desktop UI using Tkinter.

\- Environment-based API key management.

\- Logging and safe error handling.



### &nbsp;Bonus / Advanced features

\- Stop-Limit orders (native Futures support).

\- TWAP (Time-Weighted Average Price) – simulated.

\- Grid trading – simulated.

\- OCO (One-Cancels-the-Other) – simulated.

\- Context-aware UI (only shows inputs relevant to the selected order type).



---



### &nbsp;Important notes about Futures \& Testnet



A few things worth mentioning and handled in this project:



\- Binance Futures requires leverage and margin type to be set per symbol.

\- Binance Futures Testnet is eventually consistent.

\- An order can be accepted before its details are immediately available.

\- The bot handles this without crashing.

\- TWAP, Grid, and OCO are not natively supported on Binance Futures.

\- These are implemented as execution-layer simulations, which is how such strategies are commonly handled in practice only.



---



### &nbsp;Project structure



binance\_trading\_bot/

│

├── bot.py #Core trading logic (reusable)

├── cli.py #Command-line interface

├── ui.py #Desktop UI (Tkinter)

├── logger.py #Logging setup

├── test\_connection.py #Testnet connectivity check

├── requirements.txt

├── .env #API keys (not committed to github)

└── README.md





---



### &nbsp;Setup instructions



##### 1\. Clone the repository



git clone <your-repo-url>

cd binance\_trading\_bot



##### 2\. Create and activate a virtual environment



venv\\Scripts\\activate





##### 3\. Install dependencies





pip install -r requirements.txt



##### 4\. API keys \& environment variables



* Create a testnet account at

https://testnet.binancefuture.com



* Generate API Key and Secret



* Create a .env file in the project root:

BINANCE\_API\_KEY=your\_testnet\_api\_key

BINANCE\_API\_SECRET\_KEY=your\_testnet\_api\_secret





##### 5\. Running the project



* For CLI: python cli.py



* For Desktop UI: python ui.py





---



#### Order types explained



* Market Order:

Executes immediately at the current market price.



* Limit Order:

Executes only at the specified price or better.



* Stop-Limit Order:

Uses a trigger price and a limit price for controlled exits.



* TWAP (Simulated):

Splits a large order into smaller market orders executed over time.



* Grid (Simulated):

Places multiple limit orders across a price range to capture price movement.



* OCO (Simulated):

Combines take-profit and stop-loss logic so only one outcome executes.





#### Logging \& error handling



* All API interactions are logged



* Binance API exceptions are handled explicitly



* The application avoids crashes caused by delayed testnet responses


## Sample Outputs

### CLI Output
![CLI Output](screenshots/cli_output.png)

### UI Output
![UI Output](screenshots/ui_output.png)


#### Author

###### 

###### Aayushman











