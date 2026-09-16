import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
import uuid

LEDGER_FILE = Path("data/ledger.json")

def load_data():
    if not LEDGER_FILE.exists():
        return {"wallets": {}, "transactions": []}
    return json.loads(LEDGER_FILE.read_text())

def save_data(data):
    LEDGER_FILE.parent.mkdir(parents=True, exist_ok=True)
    LEDGER_FILE.write_text(json.dumps(data, indent=2))

def transfer(sender, destination, asset, amount, tenor_days):
    data = load_data()
    data["wallets"].setdefault(sender, {})
    data["wallets"].setdefault(destination, {})
    balance = float(data["wallets"][sender].get(asset, 0))
    if balance < amount:
        raise ValueError("Insufficient balance")
    created = datetime.now(timezone.utc)
    expires = created + timedelta(days=tenor_days)
    tx = {"transaction_id": "CRP-" + uuid.uuid4().hex[:16].upper(), "sender": sender, "destination": destination, "asset": asset, "amount": amount, "tenor_days": tenor_days, "created_at": created.isoformat(), "expires_at": expires.isoformat(), "status": "SETTLED", "smart_contract": False, "transaction_type": "NATIVE", "redeemable": False}
    data["wallets"][sender][asset] = balance - amount
    data["wallets"][destination][asset] = float(data["wallets"][destination].get(asset, 0)) + amount
    data["transactions"].append(tx)
    save_data(data)
    return tx
