#!/usr/bin/env python3
"""
专门检查300290的估值和市值
"""

import requests
import urllib.request

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

def check_valuation():
    """检查300290的估值和市值"""
    print("="*60)
    print("📊 300290 荣科科技 - 估值与市值分析")
    print("="*60)
    
    # 1. 获取腾讯财经的详细数据
    print("\n【1. 基本估值与市值】")
    try:
        url = "https://qt.gtimg.cn/q=sz300290"
        r = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=10)
        data = r.read().decode("gbk")
        if "=" in data:
            vals = data.split('"')[1].split("~")
            print(f"  股票名称: {vals[1]}")
            print(f"  当前价格: {float(vals[3]):.2f} 元")
            print(f"  涨跌幅: {float(vals[32]):.2f}%")
            print(f"  昨收价: {float(vals[4]):.2f} 元")
            print(f"  今开价: {float(vals[5]):.2f} 元")
            print(f"  最高价: {float(vals[33]):.2f} 元")
            print(f"  最低价: {float(vals[34]):.2f} 元")
            print(f"\n  【估值指标】")
            print(f"  PE(TTM): {float(vals[39]):.2f}")
            print(f"  PB: {float(vals[46]):.2f}")
            print(f"  PE(静): {float(vals[52]):.2f}")
            print(f"\n  【市值信息】")
            print(f"  总市值: {float(vals[44]):.2f} 亿")
            print(f"  流通市值: {float(vals[45]):.2f} 亿")
            print(f"  总股本: {float(vals[44])/float(vals[3])*100000000:.0f} 股")
            print(f"  流通股本: {float(vals[45])/float(vals[3])*100000000:.0f} 股")
            print(f"\n  【交易信息】")
            print(f"  成交量: {float(vals[6]):.0f} 手")
            print(f"  成交额: {float(vals[37]):.2f} 万")
            print(f"  换手率: {float(vals[38]):.2f}%")
            print(f"  量比: {float(vals[49]):.2f}")
            print(f"  涨停价: {float(vals[47]):.2f} 元")
            print(f"  跌停价: {float(vals[48]):.2f} 元")
    except Exception as e:
        print(f"  获取数据失败: {e}")
    
    # 2. 获取东财的个股信息
    print("\n【2. 东财个股信息】")
    try:
        secid = "0.300290"
        url = f"https://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields=f57,f58,f127,f84,f85,f116,f117,f189,f43"
        r = requests.get(url, headers={"User-Agent": UA}, timeout=10)
        if r.status_code == 200:
            d = r.json().get("data", {})
            if d:
                print(f"  行业: {d.get('f127', '-')}")
                print(f"  上市日期: {d.get('f189', '-')}")
    
    except Exception as e:
        print(f"  获取东财信息失败: {e}")
    
    # 3. 估值分析
    print("\n【3. 估值分析】")
    try:
        # 获取腾讯数据进行分析
        url = "https://qt.gtimg.cn/q=sz300290"
        r = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=10)
        data = r.read().decode("gbk")
        if "=" in data:
            vals = data.split('"')[1].split("~")
            pe_ttm = float(vals[39])
            pb = float(vals[46])
            
            print(f"  PE(TTM): {pe_ttm:.2f}x")
            print(f"  PB: {pb:.2f}x")
            
            if pe_ttm < 0:
                print("  ⚠️ PE为负，说明公司目前亏损")
            elif pe_ttm < 30:
                print("  ✅ PE较低，估值相对合理")
            elif pe_ttm < 60:
                print("  ⚠️ PE中等，估值一般")
            else:
                print("  🚨 PE较高，估值偏贵")
            
            if pb < 1:
                print("  ✅ PB低于1，破净状态")
            elif pb < 5:
                print("  ⚠️ PB中等")
            else:
                print("  🚨 PB较高，估值偏贵")
    except Exception as e:
        print(f"  估值分析失败: {e}")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    check_valuation()
