from cryptora.network import NETWORK

def test_network():
    assert NETWORK["chain_id"] == 20260916
    assert NETWORK["currency_name"] == "EtherCoin"
    assert NETWORK["currency_symbol"] == "ETC"
