
import os
import random
import time

"""

How to use:

 {"command":"codeAPI", "action": "start_alg", "name": "eval-alg", "input": [1,2,3]}
 {"command":"codeAPI", "action": "start_stored_subpipeline", "name": "simple", "input": [1,2,3]}

command:
 - none
 - dataSource
 - print
 - delay
 - codeAPI
 - bytes
 - object
 - array-bytes
 - array-object

"""

def start(args, hkubeApi=None):
    global isActive
    isActive = True
    input = args.get('input')
    nodeInput = input[0] if len(input) > 0 else None
    isStreaming = args.get('kind') == 'stream'

    if(isStreaming):
        stateType = args.get('stateType')
        isStateful = stateType == 'stateful'
        childs = args.get('childs')
        parents = args.get('parents')
        msgPerSec = nodeInput.get('msgPerSec')
        delay = nodeInput.get('delay')
        sleepTime = nodeInput.get('sleepTime')
        sleepFor = nodeInput.get('sleepFor')

        if(isStateful):
            if(childs):
                stream(hkubeApi, msgPerSec, sleepTime, sleepFor)
            if(parents):
                receive(hkubeApi, delay)

        elif(not isStateful and parents):
            time.sleep(delay)
            return 42

    if(not isinstance(nodeInput, dict)):
        time.sleep(1)
        return nodeInput

    command = nodeInput.get("command")

    if(command == 'dataSource'):
        (error, dataSource) = hkubeApi.getDataSource(nodeInput)
        if(error):
            print(error)
        else:
            print(dataSource)
            return dataSource

    if(command == 'print'):
        printData = nodeInput.get('input')
        print(printData)
    
    if(command == 'none'):
        return None

    elif(command == 'delay'):
        delay = nodeInput.get('delay')
        time.sleep(delay)

    elif (command == 'codeAPI'):
        action = nodeInput.get("action")
        if action == "start_alg":
            ret = hkubeApi.start_algorithm(nodeInput["name"], nodeInput.get("input"), includeResult=True)
            return ret

        if action == "start_stored_subpipeline":
            ret = hkubeApi.start_stored_subpipeline(
                nodeInput["name"],
                flowInput={"data": nodeInput.get("input")},
                includeResult=True)
            return ret

        if action == "start_alg_subpipeline":
            ret1 = hkubeApi.start_algorithm(nodeInput["name"], nodeInput.get("input"), includeResult=True)
            ret2 = hkubeApi.start_stored_subpipeline(
                nodeInput["name"],
                flowInput={"data": nodeInput.get("input")},
                includeResult=True)
            return (ret1, ret2)

    elif(command == 'bytes'):
        size = nodeInput.get('size')
        result = createBytes(size)
        return result
    
    elif(command == 'array-bytes'):
        itemSize = nodeInput.get('itemSize')
        arraySize = nodeInput.get('arraySize')
        result = createArrayBytes(itemSize, arraySize)
        return result

    elif(command == 'array-object'):
        itemSize = nodeInput.get('itemSize')
        arraySize = nodeInput.get('arraySize')
        result = createArrayObject(itemSize, arraySize)
        return result

    elif(command == 'object'):
        size = nodeInput.get('size')
        result = createObject(size)
        return result

    return nodeInput

def stop(args):
    global isActive
    isActive = False

def stream(hkubeApi, msgPerSec, sleepTime, sleepFor):
    i = 0
    sleep = 20
    if(msgPerSec):
        msgPerSec = float(msgPerSec)
        sleep = 1.0 / msgPerSec
    
    print("started sender with {msgPerSec} msg per second".format(msgPerSec=msgPerSec))
    if (sleepTime):
        timestamp = time.time() + sleepTime
    
    msg = {
        "ping": 0
    }
    
    while(isActive):
        i += 1
        if(sleepTime and time.time() > timestamp):
            timestamp = time.time() + sleepTime
            print("starting sleep for {sleepFor} seconds".format(sleepFor=sleepFor))
            time.sleep(sleepFor or 0)
            
        if(msgPerSec > 0):
            hkubeApi.sendMessage(msg)
        
        time.sleep(sleep)
       
def receive(hkubeApi, delay):
    print("started stateful receiver with {delay} delay".format(delay=delay))

    def handleMessage(msg, origin):
        hkubeApi.conFlow(msg)

    hkubeApi.registerInputListener(onMessage=handleMessage)
    hkubeApi.startMessageListening()
    
    while (isActive):
        time.sleep(1)

def randomString(n):
    min_lc = ord(b'a')
    len_lc = 26
    ba = bytearray(os.urandom(n))
    for i, b in enumerate(ba):
        ba[i] = min_lc + b % len_lc  # convert 0..255 to 97..122
    return ba.decode("utf-8")

def randomInt(size):
    return random.sample(range(0, size), size)

def createBytes(size):
    return bytearray(b'\xdd' * (size))

def createArrayBytes(itemSize, arraySize):
    return [createBytes(itemSize)] * (arraySize)

def createArrayObject(itemSize, arraySize):
    return [createObject(itemSize)] * (arraySize)

def createObject(size):
    obj = {
        "bytesData": createBytes(size),
        "array": createArrayBytes(5, size),
        "randomString": randomString(size),
        "randomIntArray": randomInt(size),
        "dataString": randomString(size),
        "bool": False,
        "anotherBool": False,
        "none": None,
        "nestedObj": {
            "dataString": randomString(size),
            "randomIntArray": randomInt(size)
        }
    }
    return obj

def createObjectSize(size):
    obj = {
        "data_test": createBytes(size)
    }
    return obj
