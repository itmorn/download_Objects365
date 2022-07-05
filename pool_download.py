import requests
import shutil
from multiprocessing import Pool
import os
import traceback


def get_lst_lines():
    lst = [
        f'https://dorc.ks3-cn-beijing.ksyun.com/data-set/2020Objects365%E6%95%B0%E6%8D%AE%E9%9B%86/val/zhiyuan_objv2_val.json',
        f'https://dorc.ks3-cn-beijing.ksyun.com/data-set/2020Objects365%E6%95%B0%E6%8D%AE%E9%9B%86/train/zhiyuan_objv2_train.tar.gz'
    ]

    # 验证集
    for i in range(44):
        for v_num in range(3, -1, -1):
            url = f"https://dorc.ks3-cn-beijing.ksyun.com/data-set/2020Objects365%E6%95%B0%E6%8D%AE%E9%9B%86/val/images/v{v_num}/patch{i}.tar.gz"
            torrent = requests.get(url, stream=True)
            if torrent.status_code == 200:
                print(url)
                lst.append(url)
                break

    # 训练集
    for i in range(51):
        url = f"https://dorc.ks3-cn-beijing.ksyun.com/data-set/2020Objects365%E6%95%B0%E6%8D%AE%E9%9B%86/train/patch{i}.tar.gz"
        lst.append(url)
    return lst


def thread_task(url):
    try:
        filename = os.path.basename(url)
        if "train" in url:
            filename = dir_train + filename
        else:
            filename = dir_val + filename

        os.system(f"wget {url} -O {filename}")
    except Exception as e:
        print(e)
        traceback.print_exc()


if __name__ == '__main__':
    dir_train = "train/"
    dir_val = "val/"
    shutil.rmtree(dir_train, ignore_errors=True)
    shutil.rmtree(dir_val, ignore_errors=True)
    os.makedirs(dir_train)
    os.makedirs(dir_val)

    lst_lines = get_lst_lines()
    p = Pool(8)
    try:
        result_list = p.map(thread_task, lst_lines)
        print(result_list)

        p.close()
        p.terminate()
    except Exception as e:
        print(e)
    finally:
        p.close()
        p.terminate()
