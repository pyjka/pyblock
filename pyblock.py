import hashlib
import time
import csv
import random

class Block:
    #A basic block contains, index (blockheight), the previous hash, a timestamp, tx information, a nonce, and the current hash
    def __init__(self, index, previousHash, timestamp, data, proof, currentHash):
        self.index = index
        self.previousHash = previousHash
        self.timestamp = timestamp
        self.data = data
        self.currentHash = currentHash
        self.proof = proof

def getGenesisBlock():
    return Block(0, '0', '1516636420.03901', "Initial block", 0, '02d779570304667b4c28ba1dbfd4428844a7cab89023205c66858a40937557f8')

def calculateHash(index, previousHash, timestamp, data, proof):
    value = str(index) + str(previousHash) + str(timestamp) + str(data) + str(proof)
    sha = hashlib.sha256(value.encode('utf-8'))
    return str(sha.hexdigest())

def calculateHashForBlock(block):
    return calculateHash(block.index, block.previousHash, block.timestamp, block.data, block.proof)

def getLatestBlock(blockchain):
    return blockchain[len(blockchain)-1]

def generateNextBlock(blockchain, blockData, timestamp, proof):
    previousBlock = getLatestBlock(blockchain)
    nextIndex = int(previousBlock.index) + 1
    nextTimestamp = timestamp
    nextHash = calculateHash(nextIndex, previousBlock.currentHash, nextTimestamp, proof, blockData)
    return Block(nextIndex, previousBlock.currentHash, nextTimestamp, blockData, proof, nextHash)

"""
writing blockchain into file
 """

def writeBlockchain(blockchain):
    blockchainList = []
    for block in blockchain:
        blockList = [block.index, block.previousHash, str(block.timestamp), block.data, block.proof, block.currentHash]
        blockchainList.append(blockList)
        
    with open("testtest.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerows(blockchainList)
    print('Blockchain written to blockchain.csv.')

def readBlockchain(blockchainFilePath):
    importedBlockchain = []
    try:
        with open(blockchainFilePath, 'r') as file:
            blockReader = csv.reader(file)
            for line in blockReader:
                block = Block(line[0], line[1], line[2], line[3], line[4], line[5])
                importedBlockchain.append(block)
        print("Pulling blockchain from csv...")
        return importedBlockchain
    except:
        print('No blockchain located. Generating new genesis block...')
        return [getGenesisBlock()]



def newData():
    #test purposes only
    some_data = {'sent_from':'user1' ,
              'sent_to': 'user2',
              'amount': 100
    }
    return some_data

def mineNewBlock(blockchainPath = 'testtest.csv'):
    blockchain = readBlockchain(blockchainPath)
    txData = newData()
    timestamp = time.time()
    proof = 0
    newBlockFound = False
    print('Mining a block...')
    while not newBlockFound:    
        #print("Trying new block proof...")
        newBlockAttempt = generateNextBlock(blockchain, txData, timestamp, proof)
        if newBlockAttempt.currentHash[0:1] == '5':
            stopTime = time.time()
            timer = stopTime - timestamp
            print('New block found with proof', proof, 'in', round(timer, 2), 'seconds.')
            
            newBlockFound = True
        else:
            proof += 1
    blockchain.append(newBlockAttempt)
    writeBlockchain(blockchain)

def mine(blocksToMine = 10):
    for _ in range(blocksToMine):
        mineNewBlock()

print (mine())