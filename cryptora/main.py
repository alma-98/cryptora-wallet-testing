from datetime import datetime, timedelta
from cryptora.assets import ASSETS

WALLET = "0xb7c56C27AF6D9797ca694393f8Ce2A187d4Ee89D"

def line():
    print("=" * 72)

def header(title):
    print()
    line()
    print(f"{title:^72}")
    line()

def asset_list():
    header("CRYPTORA ASSET LIST")
    print(f"{\"NO\":<5}{\"SYMBOL\":<10}{\"ASSET NAME\":<25}{\"TYPE\":<20}")
    print("-" * 72)
    for i, (symbol, item) in enumerate(ASSETS.items(), 1):
        print(f"{i:<5}{symbol:<10}{item[\"name\"]:<25}{\"NATIVE / NO CONTRACT\":<20}")

def wallet_info():
    header("WALLET INFORMATION")
    print(f"Wallet Address : {WALLET}")
    print("Wallet Type    : Cryptora Native Wallet")
    print("Smart Contract : NONE")
    print("Network        : Cryptora")
    print("Status         : ACTIVE")

def balance():
    header("WALLET BALANCE")
    print(f"Wallet: {WALLET}")
    print("-" * 72)
    for symbol, item in ASSETS.items():
        print(f"{symbol:<8}{item[\"name\"]:<25}0.00000000")

def send_transaction():
    header("SEND / WALLET-TO-WALLET")
    print("Available Assets:")
    for i, (symbol, item) in enumerate(ASSETS.items(), 1):
        print(f"  {i}. {symbol:<6} - {item[\"name\"]}")
    print()
    choice = input("Asset               : ").strip()
    try:
        index = int(choice)
        asset = list(ASSETS.keys())[index - 1]
    except (ValueError, IndexError):
        print("ERROR: Asset tidak valid.")
        return
    destination = input("Destination Wallet   : ").strip()
    amount = input("Amount              : ").strip()
    tenor = input("Tenor (days)        : ").strip()
    try:
        amount_value = float(amount)
        tenor_value = int(tenor)
        if amount_value <= 0 or tenor_value <= 0:
            raise ValueError
    except ValueError:
        print("ERROR: Amount atau tenor tidak valid.")
        return
    created = datetime.now()
    expires = created + timedelta(days=tenor_value)
    line()
    print("TRANSACTION PREVIEW")
    line()
    print(f"From                : {WALLET}")
    print(f"To                  : {destination}")
    print(f"Asset               : {asset}")
    print(f"Amount              : {amount_value}")
    print(f"Tenor               : {tenor_value} days")
    print(f"Created             : {created}")
    print(f"Expires             : {expires}")
    print("Smart Contract      : NONE")
    print("Transaction Type    : NATIVE")
    print("Settlement          : CRYPTORA")
    print("Redeemable          : NO")
    line()
    confirm = input("Confirm transaction? [Y/N]: ").strip().upper()
    if confirm == "Y":
        print("TRANSACTION ACCEPTED")
        print("Status              : SETTLED")
        print("Transaction ID      : CRP-DEMO-000001")
    else:
        print("Transaction cancelled.")

def receive():
    header("RECEIVE")
    print("Wallet Address:")
    print(WALLET)
    print("Smart Contract: NONE")

def history():
    header("TRANSACTION HISTORY")
    print("No transaction recorded yet.")

def tenor_manager():
    header("TENOR MANAGER")
    print("Default Tenor : 7 Days")
    print("Minimum Tenor : 1 Day")
    print("Maximum Tenor : 365 Days")
    print("Status        : CONFIGURABLE")

def main():
    while True:
        header("CRYPTORA WALLET MANAGER")
        print("  [1] Wallet Information")
        print("  [2] Asset List")
        print("  [3] Balance")
        print("  [4] Send / Wallet-to-Wallet")
        print("  [5] Receive")
        print("  [6] Transaction History")
        print("  [7] Tenor Manager")
        print("  [0] Exit")
        print()
        choice = input("Cryptora > ").strip()
        if choice == "1": wallet_info()
        elif choice == "2": asset_list()
        elif choice == "3": balance()
        elif choice == "4": send_transaction()
        elif choice == "5": receive()
        elif choice == "6": history()
        elif choice == "7": tenor_manager()
        elif choice == "0": break
        else: print("Menu tidak tersedia.")
        input("\\nPress ENTER to continue...")

if __name__ == "__main__":
    main()
