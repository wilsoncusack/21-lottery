from two1.lib.bitcoin.txn import TransactionOutput
from two1.lib.bitcoin.script import Script
from two1.lib.bitcoin.utils import address_to_key_hash
from two1.lib.bitcoin.utils import bytes_to_str

address = '137KzxStaf6vw5yGujViK3Tkigoix9N3v7'
_, hash160 = address_to_key_hash(address)
out_script = Script.build_p2pkh(hash160)
out1 = TransactionOutput(value=100000, script=out_script)

# Print the script
print("%s" % (out_script))

# Print the address
print("Addresses = %r" % (out1.get_addresses()))

# Print the value
print("Value: %d" % (out1.value))

# Serialize
out1_bytes = bytes(out1)
print(bytes_to_str(out1_bytes))