from PIL import Image
import numpy as np
import nrrd

# nrrd图片读取
# nrrd图片使用nrrd包gitHub中的data数据
nrrd_filename = r'G:\Hod\datasetZYH\nrrd_lung\ID00007637202177411956430_lung.nrrd'
nrrd_data, nrrd_options = nrrd.read(nrrd_filename)
nrrd_image = Image.fromarray(nrrd_data[:,:,29]*1.5)
#nrrd_data[:,:,29] 表示截取第30张切片
nrrd_image.show() # 显示这图片

