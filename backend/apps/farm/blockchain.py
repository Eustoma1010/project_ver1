import json
import datetime
from web3 import Web3
from django.conf import settings

# Địa chỉ hợp đồng thông minh đã được deploy trên Hardhat local network
CONTRACT_ADDRESS = "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512"

# Hardhat local network RPC
RPC_URL = "http://127.0.0.1:8545"

# ABI của hợp đồng thông minh VerdantTraceability
ABI = json.loads('[{"anonymous": false, "inputs": [{"indexed": true, "internalType": "string", "name": "batchId", "type": "string"}, {"indexed": false, "internalType": "string", "name": "productName", "type": "string"}, {"indexed": false, "internalType": "string", "name": "farmName", "type": "string"}, {"indexed": false, "internalType": "uint256", "name": "timestamp", "type": "uint256"}], "name": "BatchRegistered", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "internalType": "string", "name": "batchId", "type": "string"}, {"indexed": true, "internalType": "bytes32", "name": "deliveryHash", "type": "bytes32"}, {"indexed": false, "internalType": "uint256", "name": "timestamp", "type": "uint256"}], "name": "DeliveryRecorded", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "internalType": "string", "name": "batchId", "type": "string"}, {"indexed": false, "internalType": "string", "name": "title", "type": "string"}, {"indexed": false, "internalType": "string", "name": "location", "type": "string"}, {"indexed": false, "internalType": "uint256", "name": "timestamp", "type": "uint256"}], "name": "MilestoneAdded", "type": "event"}, {"inputs": [{"internalType": "string", "name": "_batchId", "type": "string"}, {"internalType": "string", "name": "_title", "type": "string"}, {"internalType": "string", "name": "_description", "type": "string"}, {"internalType": "string", "name": "_location", "type": "string"}, {"internalType": "string", "name": "_actor", "type": "string"}], "name": "addMilestone", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "string", "name": "_batchId", "type": "string"}], "name": "getBatchJourney", "outputs": [{"internalType": "string", "name": "batchId", "type": "string"}, {"internalType": "string", "name": "productName", "type": "string"}, {"internalType": "string", "name": "farmName", "type": "string"}, {"components": [{"internalType": "string", "name": "title", "type": "string"}, {"internalType": "string", "name": "description", "type": "string"}, {"internalType": "string", "name": "location", "type": "string"}, {"internalType": "string", "name": "actor", "type": "string"}, {"internalType": "uint256", "name": "timestamp", "type": "uint256"}], "internalType": "struct VerdantTraceability.Milestone[]", "name": "milestones", "type": "tuple[]"}, {"internalType": "bytes32[]", "name": "deliveryHashes", "type": "bytes32[]"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "string", "name": "_batchId", "type": "string"}, {"internalType": "bytes32", "name": "_deliveryHash", "type": "bytes32"}], "name": "recordDelivery", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "string", "name": "_batchId", "type": "string"}, {"internalType": "string", "name": "_productName", "type": "string"}, {"internalType": "string", "name": "_farmName", "type": "string"}], "name": "registerBatch", "outputs": [], "stateMutability": "nonpayable", "type": "function"}]')

def get_web3_connection():
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    if w3.is_connected():
        # Dùng tài khoản đầu tiên làm tài khoản ký giao dịch mặc định (Hardhat Account #0)
        w3.eth.default_account = w3.eth.accounts[0]
        return w3
    return None

def register_batch_on_blockchain(batch_id, product_name, farm_name):
    """
    Đăng ký lô hàng mới (Giai đoạn Gieo hạt) lên Blockchain.
    """
    w3 = get_web3_connection()
    if not w3:
        print("Cảnh báo: Không thể kết nối với mạng Blockchain Hardhat.")
        return "PENDING_BLOCKCHAIN"
    
    try:
        contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)
        tx_hash = contract.functions.registerBatch(batch_id, product_name, farm_name).transact()
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt.transactionHash.hex()
    except Exception as e:
        print(f"Lỗi khi đăng ký lô hàng trên Blockchain: {e}")
        return "FAILED_BLOCKCHAIN"

def add_milestone_on_blockchain(batch_id, title, description, location, actor):
    """
    Thêm một mốc nhật ký canh tác (chăm sóc/thu hoạch) cho lô hàng.
    """
    w3 = get_web3_connection()
    if not w3:
        print("Cảnh báo: Không thể kết nối với mạng Blockchain Hardhat.")
        return "PENDING_BLOCKCHAIN"
    
    try:
        contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)
        tx_hash = contract.functions.addMilestone(batch_id, title, description, location, actor).transact()
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt.transactionHash.hex()
    except Exception as e:
        print(f"Lỗi khi thêm mốc lịch sử trên Blockchain: {e}")
        return "FAILED_BLOCKCHAIN"

def record_delivery_on_blockchain(batch_id, order_id, customer_name, address, phone):
    """
    Tính mã băm SHA-256 bảo mật thông tin đơn hàng và ghi nhận giao vận thành công lên Blockchain.
    """
    w3 = get_web3_connection()
    if not w3:
        print("Cảnh báo: Không thể kết nối với mạng Blockchain Hardhat.")
        return "PENDING_BLOCKCHAIN"
    
    try:
        # Băm thông tin giao vận (Keccak256 / SHA3 dạng bytes32)
        delivery_hash = w3.solidity_keccak(
            ['string', 'string', 'string', 'string'],
            [str(order_id), str(customer_name), str(address), str(phone)]
        )
        
        contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)
        tx_hash = contract.functions.recordDelivery(batch_id, delivery_hash).transact()
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt.transactionHash.hex()
    except Exception as e:
        print(f"Lỗi khi ghi nhận giao vận trên Blockchain: {e}")
        return "FAILED_BLOCKCHAIN"

def get_batch_journey_from_blockchain(batch_id):
    """
    Truy vấn lịch sử hành trình lô hàng và mảng mã băm giao nhận trực tiếp từ Blockchain.
    """
    w3 = get_web3_connection()
    if not w3:
        return None
        
    try:
        contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)
        res = contract.functions.getBatchJourney(batch_id).call()
        
        # res là tuple: (batchId, productName, farmName, milestones_list, deliveryHashes_list)
        milestones = []
        for m in res[3]:
            # m: (title, description, location, actor, timestamp)
            milestones.append({
                "title": m[0],
                "description": m[1],
                "location": m[2],
                "actor": m[3],
                "timestamp": m[4]
            })
            
        delivery_hashes = [h.hex() for h in res[4]]
        
        return {
            "batch_id": res[0],
            "product_name": res[1],
            "farm_name": res[2],
            "milestones": milestones,
            "delivery_hashes": delivery_hashes
        }
    except Exception as e:
        print(f"Lỗi khi đọc dữ liệu truy xuất từ Blockchain: {e}")
        return None


def get_recent_blockchain_transactions(limit=15):
    """
    Truy vấn các giao dịch gần đây trên Hardhat Blockchain cục bộ.
    """
    w3 = get_web3_connection()
    if not w3:
        return []
        
    try:
        transactions = []
        latest_block_number = w3.eth.block_number
        
        # Quét các block gần nhất
        for block_num in range(latest_block_number, max(-1, latest_block_number - 15), -1):
            block = w3.eth.get_block(block_num, full_transactions=True)
            block_time = datetime.datetime.fromtimestamp(block.timestamp)
            for tx in block.transactions:
                try:
                    receipt = w3.eth.get_transaction_receipt(tx.hash)
                    status = "Success" if receipt.status == 1 else "Failed"
                    gas_used = receipt.gasUsed
                    to_addr = receipt.contractAddress if receipt.contractAddress else tx.to
                except Exception:
                    status = "Success"
                    gas_used = tx.gas
                    to_addr = tx.to

                if not to_addr:
                    to_addr = "Hợp đồng mới"

                transactions.append({
                    "tx_hash": tx.hash.hex(),
                    "block_number": tx.blockNumber,
                    "timestamp": block_time,
                    "from_addr": tx["from"],
                    "to_addr": to_addr,
                    "gas_used": gas_used,
                    "status": status
                })
                if len(transactions) >= limit:
                    break
            if len(transactions) >= limit:
                break
        return transactions
    except Exception as e:
        print(f"Lỗi khi đọc danh sách giao dịch Blockchain: {e}")
        return []
