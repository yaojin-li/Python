"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------------
 @Description : 模拟区块链结点2
 --------------------------------------
 @File        : blockchain_node1.py
 @Time        : 2018/4/24 16:51
 @Software    : PyCharm
 --------------------------------------
 @Author      : lixj
 @Contact     : lixj_zj@163.com
 --------------------------------------
"""

import hashlib
import json
from time import time
from urllib import parse
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse
from uuid import uuid4
from flask import Flask, jsonify, request
import requests
from argparse import ArgumentParser

# blockChain类用来管理链条，负责存储交易、加入新块等
class blockChain(object):
    def __init__(self):
        self.chain = []                     # 用于存储区块链
        self.current_transactions = []      # 用于存储交易记录
        self.nodes = set()                  # 用set来存储节点，避免重复添加节点（利用set的属性）

        # Create the genesis block 创建创世区块
        self.new_block(previous_hash = '1', proof = 100)


    # Creates a new block and adds it to the chain 生成新块并添加到区块链中
    # param proof: <int> The proof given by the proof of work algorithm
    # param previous_hash: (Optional 可选) <str> Hash of previous block
    # return: <dict> New block
    def new_block(self, proof, previous_hash: Optional[str]) -> Dict[str, Any]:
        # block
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions 将交易加入到区块后重置交易记录。目的：在新的区块中打包记录新的交易情况，不能含有之前的交易记录
        self.current_transactions = []

        # Add the new block to the list of chain
        self.chain.append(block)

        return block


    # Adds a new transaction to the list of transactions
    # 生成新的交易记录添加到交易列表中，新的交易记录将加入到下一个待挖的区块中，并返回该交易记录将被添加到的下一个待挖区块的索引
    # param sender: <str> Address of the sender 发送者地址
    # param recipient: <str> Address of the recipient 接收者地址
    # param amount: <str> Amount 发送比特币的数量
    # return: <int> The index of the block that will hold this transaction
    def new_transaction(self, sender: str, recipient: str, amount: int) -> int:
        self.current_transactions.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        })
        return self.last_block['index'] + 1


    # Hashes a block 生成块的SHA-256 hash值
    # param block: <dick> block
    # return: <str> Hash
    @staticmethod   # 静态方法
    def hash(block: Dict[str, Any]) -> str:
        block_string = json.dumps(block, sort_keys=True).encode()   # 序列化列表为json字符串格式
        return hashlib.sha256(block_string).hexdigest()             # hash.hexdigest()生成十六进制数据字符串值


    # Returns the last block in the chain
    @property       # 将一个方法变成属性调用
    def last_block(self) -> Dict[str, Any]:
        return self.chain[-1]


    # 简单工作量证明: 寻找一个数p，使得它与前一个区块的工作量证明值(proof)拼接成的字符串的 Hash 值(hash(last_proof, proof))以 4 个零开头。
    # param last_proof: <int> 前一个区块的工作量证明值
    # return: <int> proof 算力，工作量证明
    def proof_of_work(self, last_proof: int) -> int:
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof


    # 验证证明: hash(last_proof, proof)是否以四个零开头?
    # param last_proof: <int> Previous proof 前一个区块的工作量证明值
    # param proof: <int> Current Proof 当前区块的工作量证明值
    # return: <bool> True is current, false if not
    @staticmethod
    def valid_proof(last_proof: int, proof: int) -> bool:
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


    # 一致性（共识）：注册节点，在多个节点中添加一个新的节点
    # param address: <str> Address of node. Eg. 'http://192.168.0.5:5000'
    # return: None
    def register_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)       # 添加节点的地址和端口号，根据urlparse解析结果


    # Determine if a given blockchain is valid  检查是否是有效链，遍历每个块验证hash和proof
    # param chain: <list> A blockchain 区块链列表
    # return: <bool> True if valid, false if not
    def valid_chain(self, chain: List[Dict[str, Any]]) -> bool:
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n------------------\n")

            # Check that the hash of the block is correct 检测当前块是否正确可用。依据：当前块的previous_hash值是否等于前一个块的hash值
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Check that the proof of work is correct 检测工作量证明是否正确
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True


    # 共识算发解决冲突，使用网络中最长的链
    # return: <bool> 如果链被取代返回True，否则返回False
    def resolve_conflicts(self) -> bool:
        # 获取所有临近节点，nodes包含网络中的所有节点内容
        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        # 遍历所有邻居节点，并验证链的有效性，如果发现有效更长链，则替换掉自己的链
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            # 对于节点池nodes中可用的节点
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length of the chain is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return  False


# ----------------------------------------------------------------------------------


# Instantiate our node 创建节点
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate our node
blockChain = blockChain()

# 创建/transactions/new POST接口,可以给接口发送交易数据. 创建一个交易并添加到区块
@app.route("/transactions/new", methods = ["POST"])
def new_transaction():
    # values = request.get_json()  # 无交易数据返回

    # test 设置静态交易返回数据
    values = {
        'sender': '123',
        'recipient': '456',
        'amount': 5
    }

    # 检查必填字段是否在POST中
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return "Missing values", 400

    # 新建一笔交易
    index = blockChain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to block {index}'}
    return jsonify(response), 201


# 创建/chain接口，返回整个区块链
@app.route("/chain", methods = ["GET"])
def full_chain():
    response = {
        'chain': blockChain.chain,
        'length': len(blockChain.chain)
    }
    return jsonify(response), 200


# 创建/mine GET接口. 告诉服务器去挖掘新的区块
@app.route('/mine', methods = ['GET'])
def mine():
    ## 1. 运行工作证明算法以获得下一个证明，即计算工作量证明PoW。验证区块是否合格
    last_block = blockChain.last_block
    last_proof = last_block['proof']
    proof = blockChain.proof_of_work(last_proof)

    ## 2. 系统给拥有工作量证明的节点提供奖励, 即挖到合格的区块，授予矿工比特币奖励
    # 发送者为"0"表明是新挖出的币
    blockChain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    ## 3. 构造新区块并将其添加到区块链中
    block = blockChain.new_block(proof, None)
    response = {
        'message': "New block forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200


# 添加路由/nodes/register POST接口，注册节点
@app.route('/nodes/register', methods = ['POST'])
def register_nodes():
    print("begin register...")
    # values = request.get_json()
    # nodes = values.get('nodes')   # 无返回结果

    # test 设置假定的端口号为5021、5022；假定端口号第三位的2对应此文件node2
    nodes = ['http://192.168.2.111:5001',
             'http://192.168.2.111:5002',
             'http://192.168.2.111:5003']

    if nodes is None:
        return  "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockChain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockChain.nodes)
    }
    return jsonify(response), 201


# 添加路由/nodes/resolve GET接口，解决冲突
@app.route('/nodes/resolve', methods = ['GET'])
def consensus():
    print("begin resolve...")
    replaced = blockChain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockChain.chain,
            'length': len(blockChain.chain)
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockChain.chain,
            'length': len(blockChain.chain)
        }

    return jsonify(response), 200


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    # 服务运行在端口5002上
    app.run(host='192.168.2.111', port=5003)
