# 多进程下载object365数据集
## step1_pool_download.py
线程池下载文件

## step2_extract_pic_we_need_to_labelme.py
设置我们要抽取的类别，然后把相应的图片提取出来，
并把每一张图片的标注汇总到一个json文件，以labelme的格式存储，便于观看和编辑。
PS：在该脚本里，设置了一个个性化的过滤图像的需求（如果仅仅有人，过滤，因为包含别的类的图片中已经有足够多的人了），如果不需要，可以注释掉

## step3_labelme2coco.sh
将验证集的内容拷贝到训练集，然后一起切分训练集和验证集