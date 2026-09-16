import json
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

LEDGER_FILE = Path("data/ledger.json")


def load_data():
    if not LEDGER_FILE.exists():
        return {"wallets": {}, "transactions": []}
    text = LEDGER_FILE.read_text().strip()
    if not text:
        return {"wallets": {}, "transactions": []}
    return json.loads(text)


def save_data(data):
    LEDGER_FILE.parent.mkdir(parents=True, exist_ok=True)
    LEDGER_FILE.write_text(json.dumps(data, indent=2))


def expire_transactions(data):
    now = datetime.now(timezone.utc)

    for tx in data.get("transactions", []):
        if tx.get("status") != "ACTIVE":
            continue

        expires_at = datetime.fromisoformat(tx["expires_at"])
        if now >= expires_at:
            wallet = tx["destination"]
            asset = tx["asset"]
            amount = float(tx["amount"])

            data["wallets"].setdefault(wallet, {})
            current = float(data["wallets"][wallet].get(asset, 0))
            data["wallets"][wallet][asset] = max(0, current - amount)

            tx["status"] = "EXPIRED"
            tx["expired_at"] = now.isoformat()


def transfer(sender, destination, asset, amount, tenor_days):
    if amount <= 0:
        raise ValueError("Amount must be greater than zero")

    if tenor_days <= 0:
        raise ValueError("Tenor must be greater than zero")

    data = load_data()
    expire_transactions(data)

    data["wallets"].setdefault(sender, {})
    data["wallets"].setdefault(destination, {})

    balance = float(data["wallets"][sender].get(asset, 0))

    if balance < amount:
        raise ValueError(
            f"Insufficient balance: {asset} balance is {balance:,.2f}"
        )

    created = datetime.now(timezone.utc)
    expires = created + timedelta(days=tenor_days)

    tx = {
        "transaction_id": "CRP-" + uuid.uuid4().hex[:16].upper(),
        "sender": sender,
        "destination": destination,
        "asset": asset,
        "amount": amount,
        "tenor_days": tenor_days,
        "created_at": created.isoformat(),
        "expires_at": expires.isoformat(),
        "status": "ACTIVE",
        "smart_contract": False,
        "transaction_type": "NATIVE",
        "redeemable": False,
        "settlement": "CRYPTORA"
    }

    data["wallets"][sender][asset] = balance - amount

    receiver_balance = float(
        data["wallets"][destination].get(asset, 0)
    )

    data["wallets"][destination][asset] = receiver_balance + amount

    data["transactions"].append(tx)

    save_data(data)

    return tx


def get_balance(wallet, asset):
    data = load_data()
    expire_transactions(data)
    save_data(data)

    return float(
        data.get("wallets", {})
        .get(wallet, {})
        .get(asset, 0)
    )


def history():
    data = load_data()
    expire_transactions(data)
    save_data(data)

    return data.get("transactions", [])


def wallets():
    data = load_data()
    expire_transactions(data)
    save_data(data)

    return data.get("wallets", {})
