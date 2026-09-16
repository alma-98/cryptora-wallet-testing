from cryptora.assets import ASSETS
from cryptora.ledger import transfer, get_balance, history, wallets

WALLET = "0xb7c56C27AF6D9797ca694393f8Ce2A187d4Ee89D"


def wallet_info():
    print("\n=== WALLET INFORMATION ===")
    print("Wallet Address :", WALLET)
    print("Settlement     : CRYPTORA")
    print("Asset Model    : NATIVE")
    print("Smart Contract : NONE")
    print("Token Import   : NO")
    print("Network Import : NO")


def asset_list():
    print("\n=== ASSET LIST ===")
    print(f'{"NO":<5}{"SYMBOL":<10}{"ASSET NAME":<25}{"TYPE":<20}')
    print("-" * 60)
    for i, (symbol, item) in enumerate(ASSETS.items(), 1):
        print(f'{i:<5}{symbol:<10}{item["name"]:<25}{"NATIVE / NO CONTRACT":<20}')


def balance():
    print("\n=== WALLET BALANCE ===")
    data = wallets()
    balances = data.get(WALLET, {})
    for symbol in ASSETS:
        print(f"{symbol:<8} {balances.get(symbol, 0):,.2f}")


def send_transaction():
    print("\n=== SEND / WALLET-TO-WALLET ===")
    asset_list()

    try:
        index = int(input("\nSelect Asset : "))
        asset = list(ASSETS.keys())[index - 1]
    except (ValueError, IndexError):
        print("Invalid asset selection.")
        return

    destination = input("Destination Wallet : ").strip()

    try:
        amount = float(input("Amount : "))
        tenor = int(input("Tenor (days) : "))
    except ValueError:
        print("Invalid amount or tenor.")
        return

    print("\n=== TRANSACTION PREVIEW ===")
    print("Asset          :", asset)
    print("Amount         :", f"{amount:,.2f}")
    print("Destination    :", destination)
    print("Tenor          :", f"{tenor} Days")
    print("Transaction    : NATIVE")
    print("Smart Contract : NONE")
    print("Token Import   : NO")
    print("Network Import : NO")
    print("Settlement     : CRYPTORA")
    print("Redeemable     : NO")

    confirm = input("\nConfirm transaction? (yes/no): ").strip().lower()

    if confirm != "yes":
        print("Transaction cancelled.")
        return

    try:
        tx = transfer(WALLET, destination, asset, amount, tenor)
        print("\n=== TRANSACTION ACCEPTED ===")
        print("TX ID          :", tx["transaction_id"])
        print("Status         :", tx["status"])
        print("Asset          :", tx["asset"])
        print("Amount         :", f'{tx["amount"]:,.2f}')
        print("Tenor          :", f'{tx["tenor_days"]} Days')
        print("Expires        :", tx["expires_at"])
        print("Sender Balance :", f'{get_balance(WALLET, asset):,.2f}')
        print("Receiver Bal.  :", f'{get_balance(destination, asset):,.2f}')
    except ValueError as exc:
        print("\nTransaction failed:", exc)


def receive():
    print("\n=== RECEIVE ===")
    print("Wallet Address :", WALLET)
    print("Settlement     : CRYPTORA")
    print("No smart contract required.")
    print("No token import required.")
    print("No network import required.")


def transaction_history():
    print("\n=== TRANSACTION HISTORY ===")
    items = history()
    if not items:
        print("No transactions.")
        return

    for tx in items:
        print("-" * 60)
        print("TX ID       :", tx["transaction_id"])
        print("Asset       :", tx["asset"])
        print("Amount      :", f'{tx["amount"]:,.2f}')
        print("Sender      :", tx["sender"])
        print("Destination :", tx["destination"])
        print("Tenor       :", f'{tx["tenor_days"]} Days')
        print("Status      :", tx["status"])
        print("Expires     :", tx["expires_at"])


def tenor_manager():
    print("\n=== TENOR MANAGER ===")
    print("Available tenor:")
    print("1. 1 Day")
    print("2. 3 Days")
    print("3. 7 Days")
    print("4. 14 Days")
    print("5. 30 Days")
    print("Tenor is controlled by Cryptora settlement rules.")


def wallet_manager():
    print("\n=== WALLET MANAGER ===")
    for address in wallets():
        print(address)


def main():
    while True:
        print("\n" + "=" * 60)
        print("                 CRYPTORA WALLET")
        print("=" * 60)
        print("1. Wallet Information")
        print("2. Asset List")
        print("3. Balance")
        print("4. Send / Wallet-to-Wallet")
        print("5. Receive")
        print("6. Transaction History")
        print("7. Tenor Manager")
        print("8. Wallet Manager")
        print("0. Exit")
        print("=" * 60)

        choice = input("Select Menu : ").strip()

        if choice == "1":
            wallet_info()
        elif choice == "2":
            asset_list()
        elif choice == "3":
            balance()
        elif choice == "4":
            send_transaction()
        elif choice == "5":
            receive()
        elif choice == "6":
            transaction_history()
        elif choice == "7":
            tenor_manager()
        elif choice == "8":
            wallet_manager()
        elif choice == "0":
            print("Cryptora Wallet closed.")
            break
        else:
            print("Invalid menu.")


if __name__ == "__main__":
    main()
