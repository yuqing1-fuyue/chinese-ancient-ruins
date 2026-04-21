# 图片匹配脚本 - 将images文件夹中的图片与遗址关联

import os
import re

# 66个遗址名称列表（来自main.py）
RUINS_NAMES = [
    "周口店遗址", "琉璃河遗址", "圆明园遗址", "元大都遗址", "明城墙遗址", "金中都遗址",
    "半坡遗址", "丰镐遗址", "阿房宫遗址", "汉长安城遗址", "唐大明宫遗址", "秦始皇陵及兵马俑坑",
    "汉阳陵", "唐乾陵", "唐兴庆宫遗址", "西安城墙", "大雁塔（慈恩寺塔）", "小雁塔（荐福寺塔）",
    "明故宫遗址", "六朝建康城遗址", "石头城遗址", "南唐二陵遗址", "南京城墙遗址", "牛首山弘觉寺遗址",
    "二里头遗址", "偃师商城遗址", "汉魏洛阳城遗址", "隋唐洛阳城遗址", "洛阳龙门石窟", "白马寺遗址", "关林遗址",
    "北宋东京城遗址", "铁塔（开宝寺塔）", "繁塔（繁台圣寿寺塔）", "开封州桥遗址", "龙亭宫遗址",
    "良渚古城遗址", "南宋皇城遗址", "临安城遗址", "雷峰塔遗址", "西湖文化景观",
    "避暑山庄", "外八庙", "普陀宗乘之庙",
    "平江历史街区", "盘门遗址", "拙政园", "留园", "虎丘遗址", "网师园",
    "平遥古城墙", "日升昌票号遗址", "平遥古民居", "镇国寺", "双林寺",
    "云冈石窟", "大同平城遗址", "华严寺", "善化寺", "悬空寺", "应县木塔（佛宫寺释迦塔）",
    "扬州城遗址", "瘦西湖", "汉广陵城遗址", "隋炀帝陵遗址", "大明寺遗址"
]

images_dir = r"C:\Users\王泽亚\Desktop\中华古址智鉴\images"
files = os.listdir(images_dir)

# 过滤图片文件
image_files = {}
for f in files:
    if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
        # 清理文件名（去除扩展名和多余符号）
        name = os.path.splitext(f)[0]
        name = name.replace('、', '').replace('（', '(').replace('）', ')')
        image_files[name] = f

print(f"images文件夹中的图片总数: {len(image_files)}")
print(f"遗址总数: {len(RUINS_NAMES)}")
print()

# 匹配
matched = []
unmatched_ruins = []
unmatched_images = []

for ruin in RUINS_NAMES:
    # 标准名称
    standard = ruin.replace('（', '(').replace('）', ')')
    
    if standard in image_files:
        matched.append((ruin, image_files[standard]))
    else:
        unmatched_ruins.append(ruin)

# 检查未使用的图片
used_files = [m[1] for m in matched]
for name, f in image_files.items():
    if f not in used_files:
        unmatched_images.append((name, f))

print("=" * 60)
print(f"已匹配: {len(matched)}")
print("=" * 60)
for ruin, img in matched:
    print(f"[OK] {ruin} -> {img}")

print()
print("=" * 60)
print(f"缺少图片的遗址 ({len(unmatched_ruins)}):")
print("=" * 60)
for r in unmatched_ruins:
    print(f"[MISSING] {r}")

print()
print("=" * 60)
print(f"未匹配的图片 ({len(unmatched_images)}):")
print("=" * 60)
for name, f in unmatched_images:
    print(f"[UNUSED] {f}")
