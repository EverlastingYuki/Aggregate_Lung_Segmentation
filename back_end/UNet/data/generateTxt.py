import os


def walk_dir(dir):
    dir_list=[]
    for image in os.listdir(dir):
        dir_list.append(os.path.join(dir,image))
    return dir_list

original_dir=r'G:\Hod\UNet_lungCT_segmentation-master\data\CT_image'
save_dir=r'G:\Hod\UNet_lungCT_segmentation-master\data\CT_txt'
if not save_dir:
    os.mkdir(save_dir)
img_dir=os.listdir(original_dir)
img_test=walk_dir(os.path.join(original_dir,img_dir[0]))
img_test_label=walk_dir(os.path.join(original_dir,img_dir[1]))
img_t_v=walk_dir(os.path.join(original_dir,img_dir[2]))
img_t_v_label=walk_dir(os.path.join(original_dir,img_dir[3]))
img_train=img_t_v[:188]
img_val=img_t_v[188:]
img_train_label=img_t_v_label[:188]
img_val_label=img_t_v_label[188:]

# 查看每个图片与标签是否对应
# sum=0
# for index in range(len(img_train)):
#     train=img_train[index].split("\\")[-1]
#     train_label=img_train_label[index].split("\\")[-1]
#     if train==train_label:
#         print(train," ",train_label)
#         sum+=1
# print(sum)

# 将训练集写入train.txt
with open(os.path.join(save_dir, 'train.txt'), 'a')as f:
    for index in range(len(img_train)):
        f.write(img_train[index] + '\t' +img_train_label[index]  + '\n')
    print("训练集及标签写入完毕")
# 将验证集写入val.txt
with open(os.path.join(save_dir, 'val.txt'), 'a')as f:
    for index in range(len(img_val)):
        f.write(img_val[index] + '\t' +img_val_label[index]  + '\n')
    print("验证集及标签写入完毕")
# 测试集
with open(os.path.join(save_dir, 'test.txt'), 'a')as f:
    for index in range(len(img_test)):
        f.write(img_test[index] + '\t' +img_test_label[index]+ '\n')