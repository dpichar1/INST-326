import base as b

def test_wallet_happy_path():
  wallet = b.Wallet()
  assert wallet.balance == 0
  wallet.deposit(1)
  assert wallet.balance == 1
  
def test_wallet_edge_case():
  wallet =b.Wallet()
  wallet.deposit(-5)
  assert wallet.balance == 0
  