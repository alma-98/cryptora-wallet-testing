from cryptora.assets import ASSETS

def test_ethercoin():
    assert "ETC" in ASSETS
    assert ASSETS["ETC"]["name"] == "EtherCoin"
    assert ASSETS["ETC"]["smart_contract"] is False
