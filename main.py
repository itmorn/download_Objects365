import time
import os
import shutil
import requests

dir_train = "train/"
dir_val = "val/"
shutil.rmtree(dir_train, ignore_errors=True)
shutil.rmtree(dir_val, ignore_errors=True)
os.makedirs(dir_train)
os.makedirs(dir_val)

lst = [
    f'https://dorc.ks3-cn-beijing.ksyun.com/data-set/2020Objects365%E6%95%B0%E6%8D%AE%E9%9B%86/val/zhiyuan_objv2_val.json',
    f'https://dorc.ks3-cn-beijing.ksyun.com/data-set/2020Objects365%E6%95%B0%E6%8D%AE%E9%9B%86/train/zhiyuan_objv2_train.tar.gz']

# 验证集
for i in range(44):
    for v_num in range(3,-1,-1):
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

def download_file(url, filename):
    while 1:
        try:
            torrent = requests.get(url, stream=True)
            if torrent.status_code==200:
                with open(filename, 'wb') as f:
                    for chunk in torrent.iter_content(1024):
                        f.write(chunk)
                break
            else:
                print(torrent.status_code, url)
                time.sleep(1)
        except Exception as e:
            print(e,url)
            time.sleep(1)


for url in lst:
    print(url)

    filename = os.path.basename(url)
    if "train" in url:
        filename = dir_train + filename
    else:
        filename = dir_val + filename

    download_file(url, filename)

