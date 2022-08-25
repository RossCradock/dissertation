# https://gist.github.com/CrackerHax/ec6964ea030d4b31d47b7d412036c623?permalink_comment_id=4237435#gistcomment-4237435
import web3

w3 = web3.Web3(web3.HTTPProvider('https://geth.golem.network:55555'))
# from hiveon
#tx = w3.eth.getTransaction('0xac7fd65cca4489edde2e1b84da0dc63e3d40bb563b73b4fb29e2d3f3af7c481d')

# to hiveon
tx = w3.eth.getTransaction('0xaf85f4b335d38473ae3cc441257bbeba68b355ed9924bc081f01588f702b11e7')
print(tx.hash)

from eth_account._utils.signing import extract_chain_id, to_standard_v

s = w3.eth.account._keys.Signature(vrs=(
    to_standard_v(extract_chain_id(tx.v)[1]),
    w3.toInt(tx.r),
    w3.toInt(tx.s)
))

print("signature: ", s)

from eth_account._utils.legacy_transactions import ALLOWED_TRANSACTION_KEYS
tt = {k:tx[k] for k in ALLOWED_TRANSACTION_KEYS - {'chainId', 'data'}}
tt['data']=tx.input
tt['chainId']=extract_chain_id(tx.v)[0]

print("Transaction: ", tt)

from eth_account._utils.legacy_transactions import serializable_unsigned_transaction_from_dict
ut = serializable_unsigned_transaction_from_dict(tt)

print("Hash:: ", ut.hash())

print("Public key: ", s.recover_public_key_from_msg_hash(ut.hash()))

# hiveon public key 0x344d5d3c2b6de8a5e90f66ac2f856980827a52ea7909acb748102be0027605733f2e39cf60f9e569aa49b4819fdd460814223581a4fd15a1edb807ae839e4a7a
# to hiveon pub key 0xdf5ca0f10674aa8ed040e4f82cd9c712bca3cbc5b21770005ea0acd1278390eafd1f76b4c03be09d2550035e4920846ba345de676e47e62130e11c14be35102f