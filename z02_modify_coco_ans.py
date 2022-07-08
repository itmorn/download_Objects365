"""
@Auth: itmorn
@Date: 2022/7/8-8:26
@Email: 12567148@qq.com
"""
# 修改step3_labelme2coco.sh后的json文件，因为里面有一些错误
import os
import json
from tqdm import tqdm

if __name__ == '__main__':
    type = "train" #236686
    name_in = f"/data01/zhaoyichen/work_github/download_Objects365/shengkai/annotations/instance_{type}.json"
    set_errorImg_name = {"objects365_v2_01118660.jpg"}

    # dic_imgName_imgId = {i['file_name'].split('/')[-1]: i['id'] for i in images}
    # set_error_img_id = set([dic_imgName_imgId[i] for i in lst_errorImg_name])
    set_error_img_id = set()
    jsn= json.load(open(name_in))
    lst_img = []
    for dic_img in tqdm(jsn['images']):
        file_name = dic_img["file_name"]
        id = dic_img["id"]
        if file_name in set_errorImg_name:
            set_error_img_id.add(id)
            continue
        lst_img.append(dic_img)
    jsn['images'] = lst_img

    lst_ans = []
    for dic_ans in tqdm(jsn['annotations']):
        image_id = dic_ans['image_id']
        if image_id in set_error_img_id:
            continue
        lst_ans.append(dic_ans)
    jsn['annotations'] = lst_ans
    f = open(name_in,"w")
    f.write(json.dumps(jsn))
    f.close()
    print("done")