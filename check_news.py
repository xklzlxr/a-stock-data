#!/usr/bin/env python3
"""
检查300290的最新新闻
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
    
    # 方法1: 东财新闻API
    print("\n【1. 东财新闻】")
    try:
        url = "https://search-api-web.eastmoney.com/search/jsonp"
        inner_params = json.dumps({
            "uid": "",
            "keyword": "300290",
            "type": ["cmsArticleWebOld"],
            "client": "web",
            "clientType": "web",
            "clientVersion": "curr",
            "param": {"cmsArticleWebOld": {"searchScope": "default", "sort": "default",
                      "pageIndex": 1, "pageSize": 20, "preTag": "", "postTag": ""}},
        }, separators=(',', ':'))
        params = {"cb": "jQuery_news", "param": inner_params}
        headers = {"User-Agent": UA, "Referer": "https://so.eastmoney.com/"}
        
        r = requests.get(url, params=params, headers=headers, timeout=15)
        text = r.text
        json_str = text[text.index("(") + 1: text.rindex(")")]
        d = json.loads(json_str)
        
        articles = d.get("result", {}).get("cmsArticleWebOld", {}).get("list", [])
        
        if articles:
            print(f"  共找到 {len(articles)} 条新闻\n")
            for i, a in enumerate(articles[:10], 1):
                title = re.sub(r'<[^>]+>', '', a.get("title", ""))
                content = re.sub(r'<[^>]+>', '', a.get("content", ""))[:100]
                print(f"  {i}. {a.get('date', '')}")
                print(f"     {title}")
                print(f"     {content}...")
                print()
        else:
            print("  未找到东财新闻")
    except Exception as e:
        print(f"  获取东财新闻失败: {e}")
    
    # 方法2: 同花顺新闻
    print("\n【2. 同花顺新闻】")
    try:
        # 尝试同花顺的个股新闻接口
        url = f"http://news.10jqka.com.cn/tapp/news/push/stock/?page=1&tag=&track=website&pagesize=20&code=300290"
        headers = {
            "User-Agent": UA,
            "Referer": "https://www.10jqka.com.cn/",
        }
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            try:
                d = r.json()
                items = d.get("data", [])
                if items:
                    print(f"  共找到 {len(items)} 条新闻\n")
                    for i, item in enumerate(items[:5], 1):
                        print(f"  {i}. {item.get('ctime', '')}")
                        print(f"     {item.get('title', '')}")
                        print()
                else:
                    print("  未找到同花顺新闻")
            except:
                print("  同花顺新闻解析失败")
        else:
            print(f"  同花顺请求失败: {r.status_code}")
    except Exception as e:
        print(f"  获取同花顺新闻失败: {e}")
    
    # 方法3: 新浪财经新闻
    print("\n【3. 新浪财经新闻】")
    try:
        url = f"https://feed.mix.sina.com.cn/api/roll/get?pageid=372&lid=1686&k=300290&num=20&page=1&r=0.5"
        headers = {"User-Agent": UA, "Referer": "https://finance.sina.com.cn/"}
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            d = r.json()
            items = d.get("result", {}).get("data", [])
            if items:
                print(f"  共找到 {len(items)} 条新闻\n")
                for i, item in enumerate(items[:5], 1):
                    print(f"  {i}. {item.get('ctime', '')}")
                    print(f"     {item.get('intro', '')}")
                    print()
            else:
                print("  未找到新浪财经新闻")
    except Exception as e:
        print(f"  获取新浪财经新闻失败: {e}")
    
    print("="*60)

if __name__ == "__main__":
    get_news()
