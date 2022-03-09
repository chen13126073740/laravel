import os
import time

from PIL import Image

old_path = "./data/pages/images/"  # 原图片的存放地址
new_path = "./data/pages/medium_images/medium_"  # 调整后图片的存放地址
pic_names = os.listdir(old_path)
width = 500


def resize_by_width(old_path, new_path, pic_name, width):
    im = Image.open(old_path + pic_name)
    (x, y) = im.size
    x_s = width
    y_s = int(y * x_s / x)
    out = im.resize((x_s, y_s), Image.ANTIALIAS)
    out.save(new_path + pic_name)


start = time.time()
a, b, c = 0, 0, 0
for pic_name in pic_names:
    a += 1
    try:
        resize_by_width(old_path, new_path, pic_name, width)
        b += 1
        print("第 %s 张图片 %s 调整完成" % (a, pic_name))
    except:
        c += 1
        print("------第 %s 张图片 %s 调整失败------" % (a, pic_name))
end = time.time()
print("共计 %s 张图片调整完成，成功 %s 张，失败 %s 张，耗时 %s 秒" % (a, b, c, (end - start)))
