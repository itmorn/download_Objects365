python x2coco.py

# 将验证集的内容拷贝到训练集，然后一起切分训练集和验证集
--dataset_type  labelme
--json_input_dir  train_out_jsn
--image_input_dir  train_out_img
--output_dir  shengkai
--train_proportion 0.98 --val_proportion 0.02 --test_proportion 0.0

