# Solana Inscription

This package allows you to mint solana inscriptions

```python
from solana_inscription_py import SolanaClient

client = SolanaClient(private_key="your private key")
client.mint(
    p="protocol",
    tick="tick",
    amt=1000
)
```
