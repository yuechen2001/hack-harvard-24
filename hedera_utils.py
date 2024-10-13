import os
from dotenv import load_dotenv
from hedera import (
    Client,
    AccountId,
    PrivateKey,
    ContractId,
    ContractExecuteTransaction,
    ContractFunctionParameters,
)
from hedera import Hbar

# Load environment variables from the .env file
load_dotenv()

# Load and convert credentials
HEDERA_OPERATOR_ID = os.getenv("HEDERA_OPERATOR_ID")
HEDERA_OPERATOR_KEY = os.getenv("HEDERA_OPERATOR_KEY")
HEDERA_CONTRACT_ID = os.getenv("HEDERA_CONTRACT_ID")

if not HEDERA_OPERATOR_ID or not HEDERA_OPERATOR_KEY or not HEDERA_CONTRACT_ID:
    raise ValueError("Hedera credentials not set. Please check your .env file.")

# Debugging: Print loaded environment variables
print(f"HEDERA_OPERATOR_ID: {HEDERA_OPERATOR_ID}")
print(f"HEDERA_CONTRACT_ID: {HEDERA_CONTRACT_ID}")

# Convert string IDs to Hedera SDK objects
operator_id = AccountId.fromString(HEDERA_OPERATOR_ID)
operator_key = PrivateKey.fromString(HEDERA_OPERATOR_KEY)

# Initialize the Hedera client
client = Client.forTestnet()
client.setOperator(operator_id, operator_key)


def store_transaction_on_blockchain(transaction):
    try:
        # Prepare contract function parameters in the correct order
        params = (
            ContractFunctionParameters()
            .addString(transaction["datetime"])  # _datetime
            .addString(transaction["traded_to"])  # _tradedTo
            .addUint32(transaction["REC_credits_traded"])  # _recCreditsTraded
            .addUint32(transaction["company_credits_earned"])  # company_credits_earned
            .addString(transaction["user"])  # _user
        )

        # Create the contract execute transaction without freezing or signing manually
        txn = (
            ContractExecuteTransaction()
            .setContractId(ContractId.fromString(HEDERA_CONTRACT_ID))
            .setGas(1000000)
            .setFunction("storeTransaction", params)
        )

        # Debugging: Print before executing transaction
        print("Executing transaction...")

        # Execute the transaction and get the receipt
        txn_response = txn.execute(client)
        receipt = txn_response.getReceipt(client)

        txn_status = receipt.status
        print(f"Transaction status: {txn_status}")

        if txn_status.toString() == "SUCCESS":
            txn_id = txn_response.transactionId
            print(
                f"Transaction successfully stored on Hedera blockchain with txn ID: {txn_id}"
            )
            return txn_id
        else:
            print(f"Transaction failed with status: {txn_status}")
            return None

    except Exception as e:
        print(f"Error while storing transaction on Hedera: {str(e)}")
        return None


transaction = {
    "datetime": "2024-10-12 21:45:28",
    "traded_to": "business",
    "REC_credits_traded": 250,
    "company_credits_earned": 3,
    "user": "consumer@gmail.com",
}

txn_id = store_transaction_on_blockchain(transaction)

if txn_id:
    print(f"Transaction stored with ID: {txn_id}")
else:
    print("Failed to store transaction on blockchain")

print(f"Operator ID: {HEDERA_OPERATOR_ID}")
print(f"Operator Key: {operator_key.toString()[:10]}...")  # Do not print the full key
