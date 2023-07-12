import os
from web3 import Web3
from dotenv import load_dotenv
from scripts.deploy_survey_vault import survey_vault
from scripts.deploy_datanft_vault import dataNft_vault
from scripts.deploy_survey_factory import create_nft_datatoken, published_on_ocean
from scripts.approve_datanft_contract import approve_contract
from scripts.transfer_nft import transfer_nft_to_datanft_contract
from web3.middleware import geth_poa_middleware


load_dotenv()

w3 = Web3(Web3.HTTPProvider(os.getenv("PROVIDER")))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Check if connected (should return True)
print(w3.isConnected())

dataNft_contract_address = dataNft_vault(w3)
#return address of survey vault contract
vault_contract_address = survey_vault(w3, dataNft_contract_address)

# return nft address and token address (datatokenaddress, nftaddress)
info_address_nft_token = create_nft_datatoken(w3)

#published your nft on ocean market
ddo_id = published_on_ocean(w3, info_address_nft_token, vault_contract_address)

print(f"https://market.oceanprotocol.com/asset/{ddo_id}");

# w3, dataNft_contract_address, token_id, nftaddress
tx_recipt = approve_contract(w3, dataNft_contract_address, 1, info_address_nft_token[1])
print(f"transaction hash of transfer approve : {(tx_recipt.transactionHash).hex()}")

# vault_contract_address
tx_recipt_datanft = transfer_nft_to_datanft_contract(w3, dataNft_contract_address, 1, info_address_nft_token[1], vault_contract_address)
print(f"transaction hash of transfer datanft to datanft contract : {(tx_recipt_datanft.transactionHash).hex()}")