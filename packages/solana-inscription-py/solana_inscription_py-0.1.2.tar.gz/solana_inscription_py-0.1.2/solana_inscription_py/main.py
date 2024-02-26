import json
from solana.rpc.api import Client
from solders.keypair import Keypair
from solana.transaction import Transaction
from spl.memo.constants import MEMO_PROGRAM_ID
from spl.memo.instructions import MemoParams, create_memo


class SolanaClient:
    rpc_url = "https://api.mainnet-beta.solana.com"

    def __init__(self, private_key, rpc_url=None):
        if rpc_url is not None:
            self.rpc_url = rpc_url

        self.keypair = Keypair.from_base58_string(s=private_key)
        self.public_key = self.keypair.pubkey()
        self.client = Client(endpoint=self.rpc_url)

    def _mint_bytes(self, p, tick, amt):
        message_json = json.dumps({
            "p": p,
            "op": "mint",
            "tick": tick,
            "amt": str(amt)
        }, separators=(",", ":"))
        return bytes(message_json, encoding="utf-8")

    def mint(self, p, tick, amt):
        memo_message_bytes = self._mint_bytes(
            p=p,
            tick=tick,
            amt=amt
        )
        memo_instruction = create_memo(
            MemoParams(
                program_id=MEMO_PROGRAM_ID,
                message=memo_message_bytes,
                signer=self.public_key
            )
        )
        txn = Transaction().add(memo_instruction)
        hash = self.client.send_transaction(
            txn, self.keypair
        )
        return hash