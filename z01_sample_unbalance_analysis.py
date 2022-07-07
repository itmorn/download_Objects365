"""
@Auth: itmorn
@Date: 2022/7/7-10:31
@Email: 12567148@qq.com
"""
import os
import json
from tqdm import tqdm
from collections import defaultdict


def get_map_id2c(categories, lst_catagory_we_need):
    set_we_need = set(lst_catagory_we_need)
    map_id2c = {}
    for dic in categories:
        if dic["name"] in set_we_need:
            id = dic["id"]
            map_id2c[id] = dic["name"]
    return map_id2c


def extract_catagory(lst_catagory_we_need):
    jsn = json.load(open(f_jsn))
    images = jsn.pop("images")
    annotations = jsn.pop("annotations")
    categories = jsn["categories"]
    del jsn

    # 获取映射表
    map_id2c = get_map_id2c(categories, lst_catagory_we_need)
    print(map_id2c)

    # 只保留我们要的 annotations
    dic_imageId_dicAnnotations = defaultdict(list)

    for dic in tqdm(annotations):
        if dic['category_id'] not in map_id2c:
            continue
        image_id = dic['image_id']
        dic_imageId_dicAnnotations[image_id].append(dic)

    # 如果仅仅有人，则过滤
    dic_category_count = defaultdict(int)
    dic_imageId_dicAnnotations2 = defaultdict(list)
    for img_id, lst_ans in tqdm(dic_imageId_dicAnnotations.items()):
        if len(set([i['category_id'] for i in lst_ans]) - {1}) == 0:
            continue
        dic_imageId_dicAnnotations2[img_id] = lst_ans
        # 统计每个类别有多少个实例
        for dic in lst_ans:
            dic_category_count[map_id2c[dic['category_id']]] += 1
    print(dic_category_count)


if __name__ == '__main__':
    # {1: 'Person', 19: 'Book', 38: 'Moniter/TV', 62: 'Cell Phone', 74: 'Laptop', 124: 'Telephone', 126: 'Head Phone', 208: 'earphone', 282: 'Notepaper'}
    type = "val"  # {'Moniter/TV': 9228, 'Person': 11773, 'Telephone': 2798, 'Head Phone': 2126, 'Laptop': 4625, 'Book': 6827, 'Cell Phone': 4131, 'earphone': 1414, 'Notepaper': 1176}
    type = "train"  # {'Person': 780585, 'Book': 285707, 'Moniter/TV': 126331, 'Telephone': 16247, 'Cell Phone': 60771, 'Laptop': 46493, 'earphone': 5300, 'Head Phone': 17249, 'Notepaper': 1180}
    dir_in = f"{type}/"
    f_jsn = f"{dir_in}zhiyuan_objv2_{type}.json"
    lst_catagory_we_need = ["Moniter/TV", "Cell Phone", "Head Phone", "Telephone", "earphone",
                            "Person", "Book", "Notepaper", "Laptop"]
    extract_catagory(lst_catagory_we_need=lst_catagory_we_need)
