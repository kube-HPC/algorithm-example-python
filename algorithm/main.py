import time
def start(args, hkubeapi):
    print('Algorithm start called')
    print('jobId: {0}, taskId: {1}'.format(args.get('jobId'), args.get('taskId')))
    input=args['input']
    if input and input[0] == 'eval-alg':
        ret = hkubeapi.start_algorithm('eval-alg', [5, 6], resultAsRaw=True)
        time.sleep(2)
        return ret.get('response') 
    time.sleep(1)
    return 42

def stop(args):
    print("stop called")
