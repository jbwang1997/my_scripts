import time
import pynvml
import datetime
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='await')
    parser.add_argument('--gpu_id', type=int, default=0, help='gpu index')
    parser.add_argument('--used_thr', type=int, default=100,
                        help='The threshold of used gpu memo')
    parser.add_argument('--interval', type=int, default=60,
                        help='The interval of scaning gpu info')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()

    pynvml.nvmlInit()
    num_gpu = pynvml.nvmlDeviceGetCount()
    assert 0 <= args.gpu_id < num_gpu, 'invlid gpu index'
    assert args.interval >= 1

    handle = pynvml.nvml.nvmlDeviceGetHandleByIndex(0)
    while True:
        now = datetime.datetime.now().strftime('%Y%m%d_%H:%M:%S')

        meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
        used_memo = meminfo.used / 1024 / 1024

        print_info = '\r' + now + ' | GPU_id: ' + str(args.gpu_id) + \
                ' | Used Memo: ' + str(used_memo) + ' | Threshold: ' + \
                str(args.used_thr)
        print(print_info, end='', flush=True)
        if used_memo < args.used_thr:
            break
        time.sleep(args.interval)
        
    pynvml.nvmlShutdown()
