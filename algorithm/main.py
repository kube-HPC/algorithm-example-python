import time
def start(args, hkubeapi):
    input=args['input']
    if input and input[0] == 'eval-alg':
        ret = hkubeapi.start_algorithm('eval-alg', [5, 6], resultAsRaw=True)
        time.sleep(2)    
        return ret.get('response') 
    time.sleep(1)
    return 42

def stop(args):
    print("stop called")
