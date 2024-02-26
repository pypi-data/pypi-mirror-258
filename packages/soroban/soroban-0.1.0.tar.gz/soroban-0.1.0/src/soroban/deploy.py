"""
contract_file_path = "/Users/overcat/repo/stellar/soroban-examples/hello_world/target/wasm32-unknown-unknown/release/soroban_hello_world_contract.wasm"

kp = Keypair.from_secret(secret)
soroban_server = SorobanServer(rpc_server_url)

print("uploading contract...")
source = soroban_server.load_account(kp.public_key)

# with open(contract_file_path, "rb") as f:
#     contract_bin = f.read()

tx = (
    TransactionBuilder(source, network_passphrase)
    .set_timeout(300)
    .append_upload_contract_wasm_op(
        contract=contract_file_path,  # the path to the contract, or binary data
    )
    .build()
)
"""