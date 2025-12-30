from binance import Client
from binance.exceptions import BinanceAPIException
import logging
import time


class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.client = Client(api_key, api_secret)

        if testnet:
            self.client.FUTURES_URL = "https://testnet.binancefuture.com"

        logging.info("BasicBot initialized")


    def set_margin_type(self, symbol, margin_type="ISOLATED"):
        try:
            self.client.futures_change_margin_type(
                symbol=symbol,
                marginType=margin_type
            )
            logging.info(f"Margin type set to {margin_type} for {symbol}")
        except BinanceAPIException as e:
            if "No need to change margin type" in str(e):
                logging.info("Margin type already set")
            else:
                raise

    def set_leverage(self, symbol, leverage=1):
        self.client.futures_change_leverage(
            symbol=symbol,
            leverage=leverage
        )
        logging.info(f"Leverage set to {leverage}x for {symbol}")

    def _prepare_symbol(self, symbol, leverage):
        self.set_margin_type(symbol)
        self.set_leverage(symbol, leverage)
        time.sleep(0.3)  # testnet sync delay

   
    # Helpers (These make my bot crash-proof)
    

    def _get_latest_order(self, symbol):
        for _ in range(5):
            orders = self.client.futures_get_all_orders(
                symbol=symbol,
                limit=1
            )
            if orders:
                return orders[-1]
            time.sleep(0.3)
        return None

    
    #  ORDER TYPES

    def place_market_order(self, symbol, side, quantity, leverage=1):
        self._prepare_symbol(symbol, leverage)

        self.client.futures_create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity
        )

        return self._get_latest_order(symbol)

    def place_limit_order(self, symbol, side, quantity, price, leverage=1):
        self._prepare_symbol(symbol, leverage)

        self.client.futures_create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            timeInForce="GTC",
            quantity=quantity,
            price=price
        )

        return self._get_latest_order(symbol)

    def place_stop_limit_order(
        self,
        symbol,
        side,
        quantity,
        price,
        stop_price,
        leverage=1
    ):
        self._prepare_symbol(symbol, leverage)

        self.client.futures_create_order(
            symbol=symbol,
            side=side,
            type="STOP",
            quantity=quantity,
            price=price,
            stopPrice=stop_price,
            timeInForce="GTC"
        )

        return self._get_latest_order(symbol)

    
    # Bonus additions
    

    def place_twap_order(
        self,
        symbol,
        side,
        total_quantity,
        slices,
        interval_seconds,
        leverage=1
    ):
        """
        Simulated TWAP using multiple market orders
        """
        self._prepare_symbol(symbol, leverage)

        qty_per_slice = round(total_quantity / slices, 6)
        executions = []

        for i in range(slices):
            self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=qty_per_slice
            )
            executions.append({
                "slice": i + 1,
                "quantity": qty_per_slice
            })
            time.sleep(interval_seconds)

        return executions

    def place_grid_orders(
        self,
        symbol,
        side,
        start_price,
        end_price,
        grid_count,
        quantity_per_order,
        leverage=1
    ):
        """
        Simulated Grid using multiple limit orders
        """
        self._prepare_symbol(symbol, leverage)

        price_step = (end_price - start_price) / grid_count
        prices = []

        for i in range(grid_count):
            price = round(start_price + i * price_step, 2)

            self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="LIMIT",
                timeInForce="GTC",
                quantity=quantity_per_order,
                price=price
            )

            prices.append(price)

        return prices

    def place_oco_simulated(
        self,
        symbol,
        side,
        quantity,
        take_profit_price,
        stop_price,
        leverage=1
    ):
        """
        Simulated OCO (TP + SL)
        """
        self._prepare_symbol(symbol, leverage)

        self.client.futures_create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            timeInForce="GTC",
            quantity=quantity,
            price=take_profit_price
        )

        self.client.futures_create_order(
            symbol=symbol,
            side=side,
            type="STOP",
            quantity=quantity,
            stopPrice=stop_price,
            timeInForce="GTC"
        )

        return {
            "take_profit": take_profit_price,
            "stop_loss": stop_price
        }
