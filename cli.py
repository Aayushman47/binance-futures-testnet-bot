from bot import BasicBot
from logger import setup_logger
from dotenv import load_dotenv
import os

load_dotenv()
setup_logger()

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET_KEY")


def print_menu():
    print("\nSelect Order Type:")
    print("1. Market Order")
    print("2. Limit Order")
    print("3. Stop-Limit Order")
    print("4. TWAP Order (Simulated)")
    print("5. Grid Orders (Simulated)")
    print("6. OCO Order (Simulated)")


def print_order_summary(result):
    if result is None:
        print("⚠️ Order placed, but details not yet available (testnet delay).")
        return

    print("\nOrder Summary")
    print("Order ID:", result.get("orderId"))
    print("Symbol:", result.get("symbol"))
    print("Side:", result.get("side"))
    print("Type:", result.get("type"))
    print("Status:", result.get("status"))
    print("Executed Qty:", result.get("executedQty"))


def main():
    bot = BasicBot(API_KEY, API_SECRET)

    print("=== Binance Futures Testnet Trading Bot ===")

    symbol = input("Symbol (e.g. BTCUSDT): ").upper()
    side = input("Side (BUY / SELL): ").upper()
    leverage = int(input("Leverage (e.g. 1): "))

    print_menu()
    choice = input("Enter choice (1-6): ")

    try:
        # MARKET
        if choice == "1":
            quantity = float(input("Quantity: "))
            result = bot.place_market_order(
                symbol, side, quantity, leverage
            )
            print("\n✅ Market order placed")
            print_order_summary(result)

        # LIMIT
        elif choice == "2":
            quantity = float(input("Quantity: "))
            price = float(input("Limit Price: "))
            result = bot.place_limit_order(
                symbol, side, quantity, price, leverage
            )
            print("\n✅ Limit order placed")
            print_order_summary(result)

        # STOP-LIMIT
        elif choice == "3":
            quantity = float(input("Quantity: "))
            price = float(input("Limit Price: "))
            stop_price = float(input("Stop Price: "))
            result = bot.place_stop_limit_order(
                symbol, side, quantity, price, stop_price, leverage
            )
            print("\n✅ Stop-Limit order placed")
            print_order_summary(result)

        # TWAP (implemented for bonus)
        elif choice == "4":
            total_qty = float(input("Total Quantity: "))
            slices = int(input("Number of slices: "))
            interval = int(input("Interval (seconds): "))

            executions = bot.place_twap_order(
                symbol, side, total_qty, slices, interval, leverage
            )

            print("\n✅ TWAP execution completed")
            for e in executions:
                print(f"Slice {e['slice']} → Qty {e['quantity']}")

        # GRID (implemented for bonus)
        elif choice == "5":
            start_price = float(input("Start Price: "))
            end_price = float(input("End Price: "))
            grid_count = int(input("Number of grid levels: "))
            qty_per_order = float(input("Quantity per order: "))

            prices = bot.place_grid_orders(
                symbol,
                side,
                start_price,
                end_price,
                grid_count,
                qty_per_order,
                leverage
            )

            print("\n✅ Grid orders placed at prices:")
            for p in prices:
                print("→", p)

        # OCO (implemented for bonus)
        elif choice == "6":
            quantity = float(input("Quantity: "))
            tp_price = float(input("Take Profit Price: "))
            sl_price = float(input("Stop Loss Price: "))

            result = bot.place_oco_simulated(
                symbol,
                side,
                quantity,
                tp_price,
                sl_price,
                leverage
            )

            print("\n✅ Simulated OCO placed")
            print("Take Profit:", result["take_profit"])
            print("Stop Loss:", result["stop_loss"])

        else:
            print("❌ Invalid choice")

    except Exception as e:
        print("❌ Error:", e)


if __name__ == "__main__":
    main()
