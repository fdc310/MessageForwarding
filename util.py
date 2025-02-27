import base64

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

# 使用示例
image_path = r"I:\Pic\NewWen\234\0b8f4600f1a90a29fcfa7ec406e76863.png"  # 请替换为你的图片路径
base64_image = image_to_base64(image_path)
with open('test.txt','w') as f:
    f.write(base64_image)
print(base64_image)