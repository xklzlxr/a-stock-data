#!/usr/bin/env python3
"""
专门检查300290的资金流入情况
"""

import requests
import json

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

def check_300290():
    """检查300290的资金流入"""
    print("="*60)
    print("📊 300290 荣科科技 - 资金流入检查")
    print("="*60)
    
    # 1. 先查一下基本行情
    print("\n【1. 基本行情】")
    try:
        url = "https://qt.gtimg.cn/q=sz300290"
        r = requests.get(url, headers={"User-Agent": UA}, timeout=10)
        if r.status_code == 200:
            data = r.text
            if "=" in data:
                vals = data.split('"')[1].split("~")
                print(f"  名称: {vals[1]}")
                print(f"  现价: {vals[3]}")
                print(f"  涨跌幅: {vals[32]}%")
                print(f"  成交量: {vals[6]}")
                print(f"  成交额: {float(vals[37])/10000:.2f}万")
    except Exception as e:
        print(f"  获取行情失败: {e}")
    
    # 2. 尝试用不同的API获取资金流向
    print("\n【2. 资金流向检查】")
    
    # 方法1: 东财的API尝试
    print("\n  → 尝试获取东财资金流数据...")
    secid = "0.300290"
    urls = [
        f"https://push2.eastmoney.com/api/qt/stock/fflow/kline/get?secid={secid}&klt=1&fields1=f1,f2,f3,f7&fields2=f51,f52,f53,f54,f55,f56,f57",
        f"https://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get?secid={secid}&fields1=f1,f2,f3,f7&fields2=f51,f52,f53,f54,f55,f56,f57&lmt=20",
    ]
    
    for url in urls:
        try:
            r = requests.get(url, headers={"User-Agent": UA, "Referer": "https://quote.eastmoney.com/"}, timeout=10)
            if r.status_code == 200:
                d = r.json()
                if d.get("data", {}).get("klines"):
                    klines = d["data"]["klines"]
                    print(f"\n  ✅ 成功获取资金流数据，共 {len(klines)} 条记录")
                    
                    if klines:
                        # 最新一条
                        latest = klines[-1].split(",")
                        if len(latest) >= 6:
                            print("\n  【最新资金流向】")
                            print(f"    时间: {latest[0]}")
                            print(f"    主力净流入: {float(latest[1])/10000:.2f}万")
                            print(f"    小单净流入: {float(latest[2])/10000:.2f}万")
                            print(f"    中单净流入: {float(latest[3])/10000:.2f}万")
                            print(f"    大单净流入: {float(latest[4])/10000:.2f}万")
                            print(f"    超大单净流入: {float(latest[5])/10000:.2f}万")
                            
                            total_main = float(latest[1])
                            if total_main > 0:
                                print(f"\n  🟢 主力资金净流入 {total_main/10000:.2f}万")
                            elif total_main < 0:
                                print(f"\n  🔴 主力资金净流出 {abs(total_main)/10000:.2f}万")
                            else:
                                print(f"\n  ⚪ 主力资金持平")
                        break
        except Exception as e:
            print(f"  请求失败: {e}")
            continue
    
    # 3. 尝试查看同花顺的融资融券数据
    print("\n【3. 融资融券数据】")
    try:
        from a_stock_data import margin_trading
        data = margin_trading("300290", page_size=5)
        if data:
            latest = data[0]
            print(f"  日期: {latest['date']}")
            print(f"  融资余额: {latest['rzye']/100000000:.2f}亿")
            print(f"  融券余额: {latest['rqye']/100000000:.2f}亿")
            print(f"  融资买入额: {latest['rzmre']/10000:.2f}万")
    except Exception as e:
        print(f"  获取融资融券失败: {e}")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    check_300290()
