python x2coco.py

--dataset_type  labelme
--json_input_dir  val_out_jsn
--image_input_dir  val_out_img
--output_dir  shengkai
--train_proportion 0.9 --val_proportion 0.1 --test_proportion 0.0

--dataset_type  labelme
--json_input_dir  train_out_jsn
--image_input_dir  train_out_img
--output_dir  shengkai
--train_proportion 1.0 --val_proportion 0.0 --test_proportion 0.0


将提取后的文件放到生成的位置，并将img的文件夹改名为train和val，注释掉x2coco的拷贝图片，可以避免多拷贝一遍图片
--dataset_type  labelme
--json_input_dir  shengkai/val_out_jsn
--image_input_dir  shengkai/val
--output_dir  shengkai
--train_proportion 0.0 --val_proportion 1.0 --test_proportion 0.0

--dataset_type  labelme
--json_input_dir  shengkai/train_out_jsn
--image_input_dir  shengkai/train
--output_dir  shengkai
--train_proportion 1.0 --val_proportion 0.0 --test_proportion 0.0
