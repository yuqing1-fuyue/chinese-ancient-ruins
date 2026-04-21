import re
with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

local = re.findall(r'"image":\s*"/images/[^"]+"', content)
https = re.findall(r'"image":\s*"https?://[^"]+"', content)
print('本地图片路径数量:', len(local))
print('远程图片URL数量:', len(https))
if https:
    print('远程示例:', https[0][:80])
if local:
    print('本地示例:', local[0])
