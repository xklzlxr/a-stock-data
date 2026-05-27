#!/usr/bin/env python3
"""
检查300290的最新新闻 - 增强版
"""

import requests
import json
import re

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

def get_news():
    """获取300290的新闻"""
    print("="*60)
    print("📰 300290 荣科科技 - 最新新闻")
    print("="*60)
    
    # 方法1: 使用搜索引擎API
    print("\n【1. 搜索最新新闻】")
    try:
        # 尝试使用百度的股市通新闻接口
        url = f"https://finance.pae.baidu.com/vapi/v1/listinfo?pn=1&rn=10&from=pc&word=300290%20荣科科技&srcid=51178"
        headers = {
            "User-Agent": UA,
            "Referer": "https://gushitong.baidu.com/",
        }
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            try:
                d = r.json()
                results = d.get("Result", [])
                if results:
                    print(f"  共找到 {len(results)} 条新闻\n")
                    for i, item in enumerate(results[:10], 1):
                        title = item.get('title', '')
                        time = item.get('time', '')
                        source = item.get('src', '')
                        print(f"  {i}. [{time}] {source}")
                        print(f"     {title}")
                        print()
                else:
                    print("  未找到百度新闻")
            except Exception as e:
                print(f"  解析失败: {e}")
        else:
            print(f"  请求失败: {r.status_code}")
    except Exception as e:
        print(f"  获取百度新闻失败: {e}")
    
    # 方法2: 巨潮资讯公告
    print("\n【2. 巨潮资讯公告】")
    try:
        url = "https://www.cninfo.com.cn/new/hisAnnouncement/query"
        if "300290".startswith("6"):
            org_id = f"gssh0300290"
        else:
            org_id = f"gssz0300290"
        
        payload = {
            "stock": f"300290,{org_id}",
            "tabName": "fulltext",
            "pageSize": "10",
            "pageNum": "1",
            "column": "",
            "category": "",
            "plate": "",
            "seDate": "",
            "searchkey": "",
            "secid": "",
            "sortName": "",
            "sortType": "",
            "isHLtitle": "true",
        }
        headers = {
            "User-Agent": UA,
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://www.cninfo.com.cn/new/disclosure",
        }
        
        r = requests.post(url, data=payload, headers=headers, timeout=15)
        d = r.json()
        
        announcements = d.get("announcements", [])
        if announcements:
            print(f"  共找到 {len(announcements)} 条公告\n")
            for i, a in enumerate(announcements[:10], 1):
                import time as time_module
                ts = a.get("announcementTime", 0)
                if isinstance(ts, (int, float)):
                    date = time_module.strftime("%Y-%m-%d", time_module.localtime(ts / 1000))
                else:
                    date = str(ts)[:10]
                print(f"  {i}. [{date}] {a.get('announcementTypeName', '')}")
                print(f"     {a.get('announcementTitle', '')}")
                print()
        else:
            print("  未找到公告")
    except Exception as e:
        print(f"  获取巨潮公告失败: {e}")
    
    # 方法3: 直接访问东财
    print("\n【3. 东财个股新闻】")
    try:
        # 使用东财的新闻接口
        url = f"https://np-anotice-stock.eastmoney.com/api/security/ann?cb=jQuery&sr=-1&page_size=10&page_index=1&ann_type=A&client_source=web&f_node=0&s_node=0&stock_list=300290"
        headers = {"User-Agent": UA, "Referer": "https://data.eastmoney.com/"}
        r = requests.get(url, headers=headers, timeout=15)
        
        if r.status_code == 200:
            text = r.text
            try:
                json_str = text[text.index("(") + 1: text.rindex(")")]
                d = json.loads(json_str)
                data = d.get("data", {})
                list_data = data.get("list", [])
                
                if list_data:
                    print(f"  共找到 {len(list_data)} 条新闻\n")
                    for i, item in enumerate(list_data[:10], 1):
                        print(f"  {i}. [{item.get('notice_date', '')}] {item.get('title', '')}")
                        print(f"     {item.get('summary', '')[:100]}...")
                        print()
                else:
                    print("  未找到东财新闻")
            except:
                print(f"  东财新闻解析失败")
        else:
            print(f"  东财请求失败: {r.status_code}")
    except Exception as e:
        print(f"  获取东财新闻失败: {e}")
    
    print("="*60)

if __name__ == "__main__":
    get_news()
