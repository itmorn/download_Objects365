"""
@Auth: itmorn
@Date: 2022/7/5-14:22
@Email: 12567148@qq.com
"""
import os
import tarfile
import json
from collections import defaultdict
from tqdm import tqdm
import numpy as np
# dir_in = "train/"
# # os.system(f"tar -zxf train/zhiyuan_objv2_train.tar.gz -C {dir_in}")
# # my_tar = tarfile.open('train/zhiyuan_objv2_train.tar.gz')
# # names = my_tar.getnames()
# jsn = json.load(open(f"{dir_in}zhiyuan_objv2_train.json"))
# images = jsn["images"][:10]
# annotations = jsn["annotations"][:10]
# categories = jsn["categories"]
# del jsn


def have_a_look():
    jsn = json.load(open(f_jsn))
    images = jsn.pop("images")[:10]
    annotations = jsn.pop("annotations")[:10]
    categories = jsn["categories"]
    del jsn
    print(images)
    print(annotations)
    print(categories)


def get_map_id2c(categories, lst_catagory_we_need):
    set_we_need = set(lst_catagory_we_need)
    map_id2c = {}
    for dic in categories:
        if dic["name"] in set_we_need:
            id = dic["id"]
            map_id2c[id] = dic["name"]
    return map_id2c


def save_labelme(dic_imageId_dicAnnotations, dic_imageId_dicImages, map_id2c):
    # 每一张图像存一个json
    for imageId, lstAnnotations in dic_imageId_dicAnnotations.items():
        imagePath = os.path.basename(dic_imageId_dicImages[imageId]['file_name'])
        if imagePath=='objects365_v1_00018748.jpg':
            print(lstAnnotations)
        dic = {
            "version": "5.0.1",
            "flags": {},
            "shapes": [],
            "imagePath": imagePath,
            "imageData": None,
            "imageHeight": dic_imageId_dicImages[imageId]["height"],
            "imageWidth": dic_imageId_dicImages[imageId]["width"]
        }

        for annotations in lstAnnotations:
            category = map_id2c[annotations['category_id']]
            dic_inner = {
                "label": category,
                "points": [
                    annotations['bbox'][:2],
                    (np.array(annotations['bbox'][:2]) + np.array(annotations['bbox'][2:])
                     ).tolist()
                ],
                "group_id": None,
                "shape_type": "rectangle",
                "flags": {}
            }
            dic["shapes"].append(dic_inner)
        name_jsn = dir_out + os.path.basename(imagePath).split(".")[0] + ".json"
        f = open(name_jsn, "w", encoding="utf-8")
        f.write(json.dumps(dic, indent=2))
        # print(name_jsn)


def extract_imgs(dic_imageId_dicImages):
    set_url = set([v['file_name'][10:] for k, v in dic_imageId_dicImages.items()])
    set_patchx = {i.split("/")[0] for i in set_url}

    for patchx in set_patchx:
        print(patchx)
        with tarfile.open(dir_in + patchx + ".tar.gz") as tf:
            for entry in tqdm(tf):  # list each entry one by one
                name = entry.name
                if name in set_url:
                    fileobj = tf.extractfile(entry)
                    f = open(dir_out+os.path.basename(name), "wb")
                    f.write(fileobj.read())



def extract_catagory(lst_catagory_we_need):
    print(11)
    jsn = json.load(open(f_jsn))
    print(22)
    images = jsn.pop("images")
    annotations = jsn.pop("annotations")
    categories = jsn["categories"]
    del jsn
    print(33)

    # 获取映射表
    map_id2c = get_map_id2c(categories, lst_catagory_we_need)
    print(map_id2c)

    # 只保留我们要的 annotations
    dic_imageId_dicAnnotations = defaultdict(list)
    for dic in annotations:
        if dic['category_id'] not in map_id2c:
            continue
        image_id = dic['image_id']
        dic_imageId_dicAnnotations[image_id].append(dic)
    del annotations

    # 只保留我们要的 images
    dic_imageId_dicImages = {dic['id']: dic for dic in images if dic['id'] in dic_imageId_dicAnnotations}
    del images

    # 抽取我们想要的物体 转出为labelme格式
    save_labelme(dic_imageId_dicAnnotations, dic_imageId_dicImages, map_id2c)

    # 把对应的图像提取到指定文件夹
    # extract_imgs(dic_imageId_dicImages)


if __name__ == '__main__':
    dir_in = "val/"
    f_jsn = f"{dir_in}zhiyuan_objv2_val.json"
    dir_out = "val_out/"

    # if os.path.exists(dir_out):
    #     os.system(f"rm -f {dir_out}*")
    # else:
    #     os.makedirs(dir_out)

    # have_a_look()

    lst_catagory_we_need = ["Moniter/TV", "Cell Phone", "Head Phone",
                            "Telephone", "earphone", "Person", "Book", "Notepaper"]

    extract_catagory(lst_catagory_we_need=lst_catagory_we_need)

# lst_file = [dir_in + i for i in os.listdir(dir_in) if ".tar.gz" in i]
# lst_file.sort()
# for url_file in lst_file:
#     # print(url_file)
#     print(f"tar -zxf {url_file} -C {dir_in}")
#
# dir_in = "val/"
# lst_file = [dir_in + i for i in os.listdir(dir_in) if ".tar.gz" in i]
# lst_file.sort()
# for url_file in lst_file:
#     # print(url_file)
#     print(f"tar -zxf {url_file} -C {dir_in}")
