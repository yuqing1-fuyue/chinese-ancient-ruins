# 中华古址智鉴 - 遗址图片下载脚本
# 用途：从官方网站下载66个遗址的真实图片，并命名为遗址名称

import os
import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# 66个遗址的官方链接
RUINS_DATA = {
    # 北京（6个）
    "周口店遗址": "https://www.zkd.cn/",
    "琉璃河遗址": "https://www.beijing.gov.cn/renwen/rwzyd/qgzdwwbhdw/llhyz/202211/t20221101_2849533.html",
    "圆明园遗址": "https://www.yuanmingyuanpark.cn/",
    "元大都遗址": "https://www.beijing.gov.cn/renwen/rwzyd/qgzdwwbhdw/yddcqyz/202210/t20221031_2848744.html",
    "明城墙遗址": "https://www.beijing.gov.cn/gate/big5/www.beijing.gov.cn/renwen/rwzyd/lyjq/4A/mczyzgy/202210/t20221019_2839418.html",
    "金中都遗址": "https://wwj.beijing.gov.cn/bjww/wwjzzcslm/1737418/1738088/1742747/743761575/index.html",
    
    # 西安（12个）
    "半坡遗址": "https://www.banpomuseum.com.cn/",
    "丰镐遗址": "https://xadfz.xa.gov.cn/xadq/rwxa/1932322902424690689.html",
    "阿房宫遗址": "https://wwj.xa.gov.cn/xwzx/wbzx/2005535230505029634.html",
    "汉长安城遗址": "https://www.zgbk.com/ecph/words?ID=496787&SiteID=1",
    "唐大明宫遗址": "https://www.dmgpark.com/",
    "秦始皇陵及兵马俑坑": "https://bmy.com.cn/",
    "汉阳陵": "https://www.hyly.com.cn/",
    "唐乾陵": "https://www.qianlingmuseum.com/",
    "唐兴庆宫遗址": "https://www.xa.gov.cn/",
    "西安城墙": "https://www.xacitywall.com/",
    "大雁塔（慈恩寺塔）": "https://www.dayanta.com/",
    "小雁塔（荐福寺塔）": "https://www.xiaoyenta.com/",
    
    # 南京（6个）
    "明故宫遗址": "https://www.nanjing.gov.cn/",
    "六朝建康城遗址": "https://www.njmuseum.cn/",
    "石头城遗址": "https://www.nanjing.gov.cn/",
    "南唐二陵遗址": "https://www.jiangsu.gov.cn/",
    "南京城墙遗址": "https://www.njcitywall.com/index.shtml",
    "牛首山弘觉寺遗址": "https://www.niushoushan.com/",
    
    # 洛阳（7个）
    "二里头遗址": "https://www.eltmuseum.com/",
    "偃师商城遗址": "https://www.ly.gov.cn/",
    "汉魏洛阳城遗址": "https://www.hwlc.cn/",
    "隋唐洛阳城遗址": "https://www.suitangluoyang.com/",
    "洛阳龙门石窟": "https://www.lmsk.cn/",
    "白马寺遗址": "https://www.baimasi.cn/",
    "关林遗址": "https://www.guanlin.cn/",
    
    # 开封（5个）
    "北宋东京城遗址": "https://www.kf.gov.cn/",
    "铁塔（开宝寺塔）": "https://www.kftieta.com/",
    "繁塔（繁台圣寿寺塔）": "https://www.kf.gov.cn/",
    "开封州桥遗址": "https://www.kf.gov.cn/",
    "龙亭宫遗址": "https://www.kflongting.com/",
    
    # 杭州（5个）
    "良渚古城遗址": "https://www.lzsite.cn/",
    "南宋皇城遗址": "https://www.hz.gov.cn/",
    "临安城遗址": "https://www.hz.gov.cn/",
    "雷峰塔遗址": "https://www.leifengta.com/",
    "西湖文化景观": "https://www.hzwestlake.gov.cn/",
    
    # 承德（3个）
    "避暑山庄": "https://www.bishushanzhuang.com.cn/",
    "外八庙": "https://www.chengde.gov.cn/",
    "普陀宗乘之庙": "https://www.chengde.gov.cn/",
    
    # 苏州（6个）
    "平江历史街区": "https://www.sz.gov.cn/",
    "盘门遗址": "https://www.szpanmen.com/",
    "拙政园": "https://www.szzzy.cn/",
    "留园": "https://www.szly.cn/",
    "虎丘遗址": "https://www.szhuqiu.com/",
    "网师园": "https://www.szwsy.cn/",
    
    # 平遥（5个）
    "平遥古城墙": "https://www.pygc.cn/",
    "日升昌票号遗址": "https://www.rishengchang.com/",
    "平遥古民居": "https://www.py.gov.cn/",
    "镇国寺": "https://www.pyzhenguosi.com/",
    "双林寺": "https://www.pyshuanglinsi.com/",
    
    # 大同（6个）
    "云冈石窟": "https://www.yungang.org.cn/",
    "大同平城遗址": "https://www.dt.gov.cn/",
    "华严寺": "https://www.dthyasi.com/",
    "善化寺": "https://www.dtshanhua.com/",
    "悬空寺": "https://www.dtxuankongsi.com/",
    "应县木塔（佛宫寺释迦塔）": "https://www.yingxianmuta.com/",
    
    # 扬州（5个）
    "扬州城遗址": "https://www.yangzhou.gov.cn/",
    "瘦西湖": "https://www.shouxihu.com/",
    "汉广陵城遗址": "https://www.yangzhou.gov.cn/",
    "隋炀帝陵遗址": "https://www.yangzhou.gov.cn/",
    "大明寺遗址": "https://www.damingsi.com/",
}

# 图片搜索引擎备用链接（可尝试下载）
IMAGE_SEARCH = {
    "周口店遗址": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Zhoukoudian_Peking_Man_Site.jpg/800px-Zhoukoudian_Peking_Man_Site.jpg",
    "圆明园遗址": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Yuanmingyuan_Park.jpg/800px-Yuanmingyuan_Park.jpg",
    "元大都遗址": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Beijing_Ming_City_Wall.jpg/800px-Beijing_Ming_City_Wall.jpg",
    "半坡遗址": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Banpo_Museum.jpg/800px-Banpo_Museum.jpg",
    "秦始皇陵及兵马俑坑": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Terracotta_Army%2C_Cheon_01.jpg/800px-Terracotta_Army%2C_Cheon_01.jpg",
    "大雁塔（慈恩寺塔）": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/db/Dayan_Pagoda.jpg/800px-Dayan_Pagoda.jpg",
    "小雁塔（荐福寺塔）": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Xiaoyan_Pagoda.jpg/800px-Xiaoyan_Pagoda.jpg",
    "汉阳陵": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/Han_Yangling_Museum.jpg/800px-Han_Yangling_Museum.jpg",
    "洛阳龙门石窟": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Longmen_Grottoes.jpg/800px-Longmen_Grottoes.jpg",
    "云冈石窟": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Yungang_Grottoes.jpg/800px-Yungang_Grottoes.jpg",
    "悬空寺": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Hanging_Temple.jpg/800px-Hanging_Temple.jpg",
    "应县木塔（佛宫寺释迦塔）": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Yingxian_Wooden_Pagoda.jpg/800px-Yingxian_Wooden_Pagoda.jpg",
    "避暑山庄": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/Potala_Palace.jpg/800px-Potala_Palace.jpg",
    "拙政园": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Humble_Administrator%27s_Garden.jpg/800px-Humble_Administrator%27s_Garden.jpg",
    "留园": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Ling_Flower_Garden.jpg/800px-Ling_Flower_Garden.jpg",
    "平遥古城墙": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/Pingyao_Ancient_City.jpg/800px-Pingyao_Ancient_City.jpg",
    "西湖文化景观": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/West_Lake.jpg/800px-West_Lake.jpg",
}

def download_image(name, url, images_dir, timeout=10):
    """下载单个遗址图片"""
    # 清理文件名
    safe_name = name.replace('/', ' ').replace('\\', ' ').replace(':', '：')
    safe_name = safe_name.replace('（', '(').replace('）', ')')
    
    # 先尝试Wikimedia图片
    if name in IMAGE_SEARCH:
        img_url = IMAGE_SEARCH[name]
        for ext in ['.jpg', '.png', '.webp']:
            file_path = os.path.join(images_dir, safe_name + ext)
            if os.path.exists(file_path):
                return True, f"已有: {safe_name}{ext}"
            
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                response = requests.get(img_url, headers=headers, timeout=timeout)
                if response.status_code == 200:
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    return True, f"下载成功: {safe_name}{ext} ({len(response.content)} bytes)"
            except Exception as e:
                continue
    
    return False, f"需要手动下载: {name} - 访问: {url}"

def main():
    images_dir = r"C:\Users\王泽亚\Desktop\中华古址智鉴\images"
    os.makedirs(images_dir, exist_ok=True)
    
    print("=" * 60)
    print("中华古址智鉴 - 66个遗址图片下载工具")
    print("=" * 60)
    print(f"\n目标目录: {images_dir}")
    print(f"遗址总数: {len(RUINS_DATA)}")
    print()
    
    # 检查已有图片
    existing_files = [f for f in os.listdir(images_dir) if f.endswith(('.jpg', '.png', '.webp'))]
    print(f"已有图片: {len(existing_files)}")
    print()
    
    # 下载图片
    success_count = 0
    manual_count = 0
    results = []
    
    for name, url in sorted(RUINS_DATA.items()):
        ok, msg = download_image(name, url, images_dir)
        results.append((name, ok, msg))
        if ok:
            success_count += 1
        else:
            manual_count += 1
        print(f"[{'OK' if ok else '需手动':^6}] {msg}")
        time.sleep(0.5)  # 避免请求过快
    
    print()
    print("=" * 60)
    print(f"下载完成统计:")
    print(f"  自动下载成功: {success_count}")
    print(f"  需要手动下载: {manual_count}")
    print("=" * 60)
    
    # 生成手动下载清单
    manual_list = [f"  - {name}: {url}" for name, url in sorted(RUINS_DATA.items()) if name not in IMAGE_SEARCH]
    
    with open(os.path.join(images_dir, "手动下载清单.md"), 'w', encoding='utf-8') as f:
        f.write("# 遗址图片手动下载清单\n\n")
        f.write(f"共 {len(manual_list)} 个遗址需要手动下载图片\n\n")
        f.write("操作步骤：\n")
        f.write("1. 复制以下链接到浏览器打开\n")
        f.write("2. 在图片上右键 → 另存为\n")
        f.write("3. 保存到 images 文件夹，命名为遗址名称\n\n")
        f.write("## 下载清单\n\n")
        f.write("\n".join(manual_list))
    
    print(f"\n已生成手动下载清单: images/手动下载清单.md")
    
    return results

if __name__ == "__main__":
    main()
