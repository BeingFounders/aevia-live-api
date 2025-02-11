from eth_account.messages import encode_typed_data
from web3 import Web3
from enum import IntEnum

class TokenType(IntEnum):
    ERC20 = 0
    ERC721 = 1
    ERC1155 = 2

class SignatureService:
    def __init__(self, contract_address: str, chain_id: int):
        self.contract_address = Web3.to_checksum_address(contract_address)
        self.chain_id = chain_id
        
    def get_signature_message(
                    self,
                    legacy_id: int,
                    token_type: TokenType,
                    token_address: str,
                    token_id: int,
                    amount: int,
                    from_address: str = None,
                    to_address: str = None) -> dict:
        """
        Creates the EIP-712 typed data structure for signing
        """
        
        # Convert addresses to checksum format
        token_address = Web3.to_checksum_address(token_address)
        from_address = Web3.to_checksum_address(from_address)
        to_address = Web3.to_checksum_address(to_address)
        
        domain_data = {
            "name": "AeviaProtocol",
            "version": "1.0.0",
            "chainId": str(self.chain_id),
            "verifyingContract": self.contract_address
        }
        
        message_data = {
            "legacyId": legacy_id,
            "tokenType": str(token_type),
            "tokenAddress": token_address,
            "tokenId": str(token_id or 0),
            "amount": str(amount or 0),
            "from": from_address,
            "to": to_address
        }
        
        typed_data = {
            "types": {
                "EIP712Domain": [
                    {"name": "name", "type": "string"},
                    {"name": "version", "type": "string"},
                    {"name": "chainId", "type": "uint256"},
                    {"name": "verifyingContract", "type": "address"}
                ],
                "Legacy": [
                    {"name": "legacyId", "type": "uint256"},
                    {"name": "tokenType", "type": "uint8"},
                    {"name": "tokenAddress", "type": "address"},
                    {"name": "tokenId", "type": "uint256"},
                    {"name": "amount", "type": "uint256"},
                    {"name": "from", "type": "address"},
                    {"name": "to", "type": "address"}
                ]
            },
            "primaryType": "Legacy",
            "domain": domain_data,
            "message": message_data
        }
        
        return typed_data
