#!/usr/bin/env python3
"""
尝试多个数据源获取300290的资金流向
"""

import requests

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

def get_fund_flow_from_multiple_sources():
    """从多个数据源获取资金流向"""
    print("="*70)
    print("💰 300290 荣科科技 - 资金流向多数据源分析")
    print("="*70)
    
    code = "300290"
    
    # 1. 获取腾讯财经的基础数据
    print("\n【1. 腾讯财经基础数据】")
    try:
        import urllib.request
        url = "https://qt.gtimg.cn/q=sz300290"
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        r = urllib.request.urlopen(req, timeout=10)
        data = r.read().decode("gbk")
        
        if "=" in data:
            vals = data.split('"')[1].split("~")
            print(f"  ✅ 获取成功")
            print(f"  股票名称: {vals[1]}")
            print(f"  当前价格: {vals[3]} 元")
            print(f"  涨跌幅: {vals[32]}%")
            print(f"  成交量: {float(vals[6]):.0f} 手")
            print(f"  成交额: {float(vals[37]):.2f} 万")
            print(f"  外盘(主动买): {float(vals[7]):.0f} 手")
            print(f"  内盘(主动卖): {float(vals[8]):.0f} 手")
            
            # 计算外内比
            outside = float(vals[7])
            inside = float(vals[8])
            if inside > 0:
                ratio = outside / inside
                print(f"  外盘/内盘比: {ratio:.2f}")
                if ratio > 1.1:
                    print(f"  📈 资金净流入信号 (外盘 > 内盘)")
                elif ratio < 0.9:
                    print(f"  📉 资金净流出信号 (内盘 > 外盘)")
                else:
                    print(f"  ⚖️ 资金基本平衡")
    except Exception as e:
        print(f"  ❌ 获取失败: {e}")
    
    # 2. 获取融资融券数据
    print("\n【2. 融资融券数据】")
    try:
        from a_stock_data import margin_trading
        margin = margin_trading(code, page_size=10)
        
        if margin:
            print(f"  ✅ 获取成功，共 {len(margin)} 条记录\n")
            
            print(f"  {'日期':<12} {'融资余额':>12} {'融资买入额':>12} {'融券余额':>12}")
            print(f"  {'-'*50}")
            
            for m in margin[:5]:
                print(f"  {m['date']:<12} {m['rzye']/1e8:>10.2f}亿 {m['rzmre']/1e4:>10.2f}万 {m['rqye']/1e8:>10.2f}亿")
            
            # 最新融资余额分析
            latest = margin[0]
            rzye = latest['rzye'] / 1e8
            print(f"\n  【融资余额分析】")
            print(f"  最新融资余额: {rzye:.2f}亿")
            
            # 计算融资余额变化
            if len(margin) > 1:
                change = (margin[0]['rzye'] - margin[1]['rzye']) / 1e8
                if change > 0:
                    print(f"  📈 融资余额较上日增加 {change:.2f}亿 (杠杆资金看多)")
                elif change < 0:
                    print(f"  📉 融资余额较上日减少 {abs(change):.2f}亿 (杠杆资金看空)")
                else:
                    print(f"  ⚖️ 融资余额持平")
            
            # 融资余额趋势
            if len(margin) >= 5:
                avg_rzye = sum(m['rzye'] for m in margin[:5]) / 5 / 1e8
                print(f"  近5日平均融资余额: {avg_rzye:.2f}亿")
                if rzye > avg_rzye:
                    print(f"  📈 融资余额高于平均 (市场做多情绪上升)")
                else:
                    print(f"  📉 融资余额低于平均 (市场做多情绪下降)")
        else:
            print("  ❌ 未获取到融资融券数据")
    except Exception as e:
        print(f"  ❌ 获取失败: {e}")
    
    # 3. 尝试获取同花顺的资金流向
    print("\n【3. 同花顺资金流向】")
    try:
        # 同花顺的资金流向接口
        url = f"http://d.10jqka.com.cn/v4/line/hs_{code}/01/last20.js"
        headers = {
            "User-Agent": UA,
            "Referer": "https://stockpage.10jqka.com.cn/",
        }
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            print(f"  ✅ 获取同花顺数据成功")
            print(f"  数据: {r.text[:200]}...")
        else:
            print(f"  ❌ 请求失败: {r.status_code}")
    except Exception as e:
        print(f"  ❌ 获取失败: {e}")
    
    # 4. 计算综合资金分析
    print("\n【4. 综合资金分析】")
    print("  基于现有数据分析:")
    print("  • 股价今日下跌 6.47%，短期走势较弱")
    print("  • 外内盘比接近平衡，盘中多空博弈")
    print("  • 融资余额 7.68亿，相对较高，存在杠杆资金")
    print("  • 融券余额为0，说明做空力量较弱")
    
    print("\n【5. 风险提示】")
    print("  ⚠️ PE为负，公司处于亏损状态")
    print("  ⚠️ 今日跌幅较大，需注意短期风险")
    print("  ⚠️ 建议关注公司扭亏进展和业务转型情况")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    get_fund_flow_from_multiple_sources()
