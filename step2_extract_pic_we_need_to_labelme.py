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
import shutil


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
    for imageId, lstAnnotations in tqdm(dic_imageId_dicAnnotations.items()):
        imagePath = os.path.basename(dic_imageId_dicImages[imageId]['file_name'])
        # if imagePath == 'objects365_v1_00018748.jpg':
        #     print(lstAnnotations)
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
                "iscrowd": annotations['iscrowd'],
                "group_id": None,
                "shape_type": "rectangle",
                "flags": {}
            }
            dic["shapes"].append(dic_inner)
        name_jsn = dir_out_jsn + os.path.basename(imagePath).split(".")[0] + ".json"
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
                    f = open(dir_out_img + os.path.basename(name), "wb")
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

    # 有的图片标注的有问题，比如图像被旋转了，和标注的尺寸对不上
    dic_imgName_imgId = {i['file_name'].split('/')[-1]: i['id'] for i in images}
    lst_errorImg_name = ["objects365_v2_01118660.jpg"]
    set_error_img_id = set([dic_imgName_imgId[i] for i in lst_errorImg_name])

    # 只保留我们要的 annotations
    dic_imageId_dicAnnotations = defaultdict(list)
    for dic in annotations:
        if dic['category_id'] not in map_id2c:
            continue
        image_id = dic['image_id']
        if image_id in set_error_img_id:
            continue
        dic_imageId_dicAnnotations[image_id].append(dic)
    del annotations

    # 如果仅仅有人，过滤，因为包含别的类的图片中已经有足够多的人了
    dic_category_count = defaultdict(int)
    dic_imageId_dicAnnotations2 = defaultdict(list)
    for img_id, lst_ans in dic_imageId_dicAnnotations.items():
        if len(set([i['category_id'] for i in lst_ans]) - {1}) == 0:
            continue
        dic_imageId_dicAnnotations2[img_id] = lst_ans
        # 统计每个类别有多少个实例
        for dic in lst_ans:
            dic_category_count[map_id2c[dic['category_id']]] += 1

    print(dic_category_count)


    # 只保留我们要的 images
    dic_imageId_dicImages = {dic['id']: dic for dic in images if dic['id'] in dic_imageId_dicAnnotations2}
    del images

    # 抽取我们想要的物体 转出为labelme格式
    save_labelme(dic_imageId_dicAnnotations2, dic_imageId_dicImages, map_id2c)

    # 把对应的图像提取到指定文件夹
    extract_imgs(dic_imageId_dicImages)


if __name__ == '__main__':
    # 设置我们要抽取的类别，然后把相应的图片提取出来，
    # 并把每一张图片的标注汇总到一个json文件，以labelme的格式存储，便于观看和编辑
    # PS：在该脚本里，设置了一个个性化的过滤图像的需求（如果仅仅有人，过滤，因为包含别的类的图片中已经有足够多的人了），如果不需要，可以注释掉
    type = "train"  #train / val
    type = "val"  #train / val

    dir_in = f"{type}/"
    f_jsn = f"/data01/zhaoyichen/data/objects365/{dir_in}zhiyuan_objv2_{type}.json"
    dir_out_img = f"{type}_out_img/"
    dir_out_jsn = f"{type}_out_jsn/"

    # shutil.rmtree(dir_out_img, ignore_errors=True)
    # shutil.rmtree(dir_out_img, ignore_errors=True)
    #
    # os.makedirs(dir_out_img)
    # os.makedirs(dir_out_jsn)

    # have_a_look()

    # lst_catagory_we_need = ["Head Phone",  "earphone"] #9 pp2.0的coco不需要加背景
    lst_catagory_we_need = ["Moniter/TV", "Cell Phone", "Head Phone", "Telephone", "earphone",
                            "Person", "Book", "Notepaper", "Laptop"] #9 pp2.0的coco不需要加背景
    #{1: 'Person', 19: 'Book', 38: 'Moniter/TV', 62: 'Cell Phone', 74: 'Laptop', 124: 'Telephone', 126: 'Head Phone', 208: 'earphone', 282: 'Notepaper'}
    extract_catagory(lst_catagory_we_need=lst_catagory_we_need)
