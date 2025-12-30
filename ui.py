import tkinter as tk
from tkinter import ttk, messagebox
from bot import BasicBot
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET_KEY")

bot = BasicBot(API_KEY, API_SECRET)


def clear_frames():
    for frame in frames.values():
        frame.pack_forget()


def on_order_type_change(event=None):
    clear_frames()
    frames[order_type_var.get()].pack(pady=10)


def place_order():
    try:
        symbol = symbol_var.get().upper()
        side = side_var.get()
        leverage = int(leverage_entry.get())
        order_type = order_type_var.get()

        if order_type == "Market":
            qty = float(market_qty.get())
            result = bot.place_market_order(symbol, side, qty, leverage)

        elif order_type == "Limit":
            qty = float(limit_qty.get())
            price = float(limit_price.get())
            result = bot.place_limit_order(symbol, side, qty, price, leverage)

        elif order_type == "Stop-Limit":
            qty = float(sl_qty.get())
            price = float(sl_price.get())
            stop = float(sl_stop.get())
            result = bot.place_stop_limit_order(symbol, side, qty, price, stop, leverage)

        elif order_type == "TWAP":
            qty = float(twap_qty.get())
            slices = int(twap_slices.get())
            interval = int(twap_interval.get())
            result = bot.place_twap_order(symbol, side, qty, slices, interval, leverage)

        elif order_type == "Grid":
            start = float(grid_start.get())
            end = float(grid_end.get())
            count = int(grid_count.get())
            qty = float(grid_qty.get())
            result = bot.place_grid_orders(symbol, side, start, end, count, qty, leverage)

        elif order_type == "OCO":
            qty = float(oco_qty.get())
            tp = float(oco_tp.get())
            sl = float(oco_sl.get())
            result = bot.place_oco_simulated(symbol, side, qty, tp, sl, leverage)

        output.delete("1.0", tk.END)
        output.insert(tk.END, str(result) if result else "Order placed (details pending).")

    except Exception as e:
        messagebox.showerror("Error", str(e))


#UI SETUP

root = tk.Tk()
root.title("Binance Futures Trading Bot")
root.geometry("420x520")

symbol_var = tk.StringVar(value="BTCUSDT")
side_var = tk.StringVar(value="BUY")
order_type_var = tk.StringVar(value="Market")

ttk.Label(root, text="Symbol").pack()
ttk.Entry(root, textvariable=symbol_var).pack()

ttk.Label(root, text="Side").pack()
ttk.Combobox(root, textvariable=side_var, values=["BUY", "SELL"]).pack()

ttk.Label(root, text="Order Type").pack()
order_menu = ttk.Combobox(
    root,
    textvariable=order_type_var,
    values=["Market", "Limit", "Stop-Limit", "TWAP", "Grid", "OCO"]
)
order_menu.pack()
order_menu.bind("<<ComboboxSelected>>", on_order_type_change)

ttk.Label(root, text="Leverage").pack()
leverage_entry = ttk.Entry(root)
leverage_entry.insert(0, "1")
leverage_entry.pack()

frames = {}

#Market

frames["Market"] = tk.Frame(root)
market_qty = ttk.Entry(frames["Market"])
ttk.Label(frames["Market"], text="Quantity").pack()
market_qty.pack()

#Limit

frames["Limit"] = tk.Frame(root)
limit_qty = ttk.Entry(frames["Limit"])
limit_price = ttk.Entry(frames["Limit"])
ttk.Label(frames["Limit"], text="Quantity").pack()
limit_qty.pack()
ttk.Label(frames["Limit"], text="Price").pack()
limit_price.pack()

#Stop-Limit

frames["Stop-Limit"] = tk.Frame(root)
sl_qty = ttk.Entry(frames["Stop-Limit"])
sl_price = ttk.Entry(frames["Stop-Limit"])
sl_stop = ttk.Entry(frames["Stop-Limit"])
ttk.Label(frames["Stop-Limit"], text="Quantity").pack()
sl_qty.pack()
ttk.Label(frames["Stop-Limit"], text="Limit Price").pack()
sl_price.pack()
ttk.Label(frames["Stop-Limit"], text="Stop Price").pack()
sl_stop.pack()

#TWAP

frames["TWAP"] = tk.Frame(root)
twap_qty = ttk.Entry(frames["TWAP"])
twap_slices = ttk.Entry(frames["TWAP"])
twap_interval = ttk.Entry(frames["TWAP"])
ttk.Label(frames["TWAP"], text="Total Quantity").pack()
twap_qty.pack()
ttk.Label(frames["TWAP"], text="Slices").pack()
twap_slices.pack()
ttk.Label(frames["TWAP"], text="Interval (sec)").pack()
twap_interval.pack()

#Grid

frames["Grid"] = tk.Frame(root)
grid_start = ttk.Entry(frames["Grid"])
grid_end = ttk.Entry(frames["Grid"])
grid_count = ttk.Entry(frames["Grid"])
grid_qty = ttk.Entry(frames["Grid"])
ttk.Label(frames["Grid"], text="Start Price").pack()
grid_start.pack()
ttk.Label(frames["Grid"], text="End Price").pack()
grid_end.pack()
ttk.Label(frames["Grid"], text="Grid Count").pack()
grid_count.pack()
ttk.Label(frames["Grid"], text="Quantity per Order").pack()
grid_qty.pack()

#OCO

frames["OCO"] = tk.Frame(root)
oco_qty = ttk.Entry(frames["OCO"])
oco_tp = ttk.Entry(frames["OCO"])
oco_sl = ttk.Entry(frames["OCO"])
ttk.Label(frames["OCO"], text="Quantity").pack()
oco_qty.pack()
ttk.Label(frames["OCO"], text="Take Profit").pack()
oco_tp.pack()
ttk.Label(frames["OCO"], text="Stop Loss").pack()
oco_sl.pack()

# Default frame

frames["Market"].pack(pady=10)

ttk.Button(root, text="Place Order", command=place_order).pack(pady=10)

output = tk.Text(root, height=6)
output.pack()

root.mainloop()
