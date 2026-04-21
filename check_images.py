import os
import re

# 读取main.py中的遗址名称
with open(r'C:\Users\王泽亚\Desktop\中华古址智鉴\main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 提取所有遗址名称
names = re.findall(r'"name":\s*"([^"]+)"', content)
ruins_names = list(set(names))

# 读取images目录中的文件
images_dir = r'C:\Users\王泽亚\Desktop\中华古址智鉴\images'
files = os.listdir(images_dir)

# 过滤掉非图片文件
image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))]

print(f'总遗址数量: {len(ruins_names)}')
print(f'images目录中的图片数量: {len(image_files)}')
print()

# 匹配检查
matched = []
unmatched = []

for name in sorted(ruins_names):
    found = False
    for img in image_files:
        img_name = os.path.splitext(img)[0]
        # 完全匹配
        if name == img_name:
            matched.append((name, img))
            found = True
            break
        # 部分匹配
        if name in img_name or img_name in name:
            matched.append((name, img))
            found = True
            break
    
    if not found:
        unmatched.append(name)

print('=== 已匹配的图片 ({}) ==='.format(len(matched)))
for name, img in matched:
    print(f'  [OK] {name} -> {img}')

print()
print('=== 缺少图片的遗址 ({}) ==='.format(len(unmatched)))
for name in unmatched:
    print(f'  [MISSING] {name}')

print()
print('=== 目录中存在但未匹配的图片 ({}) ==='.format(len(image_files) - len(matched)))
for img in image_files:
    if not any(m[1] == img for m in matched):
        print(f'  [UNUSED] {img}')