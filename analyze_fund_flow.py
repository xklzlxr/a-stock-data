#!/usr/bin/env python3
"""
详细分析300290的资金流向
"""

import requests

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

def analyze_fund_flow():
    """分析300290的资金流向"""
    print("="*70)
    print("💰 300290 荣科科技 - 资金流向详细分析")
    print("="*70)
    
    # 获取120日资金流数据
    secid = "0.300290"
    url = f"https://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get?secid={secid}&fields1=f1,f2,f3,f7&fields2=f51,f52,f53,f54,f55,f56,f57&lmt=120"
    
    print("\n【1. 获取120日资金流数据】")
    try:
        headers = {
            "User-Agent": UA,
            "Referer": "https://quote.eastmoney.com/",
        }
        r = requests.get(url, headers=headers, timeout=15)
        d = r.json()
        
        klines = d.get("data", {}).get("klines", [])
        print(f"  ✅ 成功获取 {len(klines)} 条数据\n")
        
        if not klines:
            print("  未获取到资金流数据")
            return
        
        # 解析数据
        data = []
        for line in klines:
            parts = line.split(",")
            if len(parts) >= 6:
                data.append({
                    "date": parts[0],
                    "main_net": float(parts[1]) if parts[1] != "-" else 0,
                    "small_net": float(parts[2]) if parts[2] != "-" else 0,
                    "mid_net": float(parts[3]) if parts[3] != "-" else 0,
                    "large_net": float(parts[4]) if parts[4] != "-" else 0,
                    "super_net": float(parts[5]) if parts[5] != "-" else 0,
                })
        
        # 打印近期10日数据
        print("【2. 近期10日资金流向明细】")
        print(f"{'日期':<12} {'主力净流入':>12} {'超大单':>12} {'大单':>12} {'中单':>12} {'小单':>12}")
        print("-" * 72)
        
        for d in data[-10:]:
            main_color = "+" if d["main_net"] >= 0 else ""
            super_color = "+" if d["super_net"] >= 0 else ""
            large_color = "+" if d["large_net"] >= 0 else ""
            mid_color = "+" if d["mid_net"] >= 0 else ""
            small_color = "+" if d["small_net"] >= 0 else ""
            
            print(f"{d['date']:<12} {main_color}{d['main_net']/10000:>10.1f}万 {super_color}{d['super_net']/10000:>10.1f}万 {large_color}{d['large_net']/10000:>10.1f}万 {mid_color}{d['mid_net']/10000:>10.1f}万 {small_color}{d['small_net']/10000:>10.1f}万")
        
        # 计算各周期汇总
        print("\n【3. 各周期资金流向汇总】")
        
        periods = [
            ("近5日", data[-5:]),
            ("近10日", data[-10:]),
            ("近20日", data[-20:]),
            ("近60日", data[-60:]),
            ("近120日", data),
        ]
        
        print(f"{'周期':<10} {'主力净流入':>15} {'超大单':>15} {'大单':>15} {'中单':>15} {'小单':>15}")
        print("-" * 85)
        
        for name, period in periods:
            if period:
                main_total = sum(d["main_net"] for d in period)
                super_total = sum(d["super_net"] for d in period)
                large_total = sum(d["large_net"] for d in period)
                mid_total = sum(d["mid_net"] for d in period)
                small_total = sum(d["small_net"] for d in period)
                
                main_str = f"{main_total/1e8:+.2f}亿" if abs(main_total) >= 1e8 else f"{main_total/10000:+.0f}万"
                super_str = f"{super_total/1e8:+.2f}亿" if abs(super_total) >= 1e8 else f"{super_total/10000:+.0f}万"
                large_str = f"{large_total/1e8:+.2f}亿" if abs(large_total) >= 1e8 else f"{large_total/10000:+.0f}万"
                mid_str = f"{mid_total/1e8:+.2f}亿" if abs(mid_total) >= 1e8 else f"{mid_total/10000:+.0f}万"
                small_str = f"{small_total/1e8:+.2f}亿" if abs(small_total) >= 1e8 else f"{small_total/10000:+.0f}万"
                
                print(f"{name:<10} {main_str:>15} {super_str:>15} {large_str:>15} {mid_str:>15} {small_str:>15}")
        
        # 资金流向分析
        print("\n【4. 资金流向分析】")
        
        # 近5日分析
        recent_5 = data[-5:]
        main_5 = sum(d["main_net"] for d in recent_5)
        
        print(f"\n  近5日主力资金动向:")
        if main_5 > 0:
            print(f"    🟢 净流入 {main_5/1e8:.2f}亿 (看多信号)")
        else:
            print(f"    🔴 净流出 {abs(main_5)/1e8:.2f}亿 (看空信号)")
        
        # 近10日分析
        recent_10 = data[-10:]
        main_10 = sum(d["main_net"] for d in recent_10)
        
        print(f"\n  近10日主力资金动向:")
        if main_10 > 0:
            print(f"    🟢 净流入 {main_10/1e8:.2f}亿 (看多信号)")
        else:
            print(f"    🔴 净流出 {abs(main_10)/1e8:.2f}亿 (看空信号)")
        
        # 近20日分析
        recent_20 = data[-20:]
        main_20 = sum(d["main_net"] for d in recent_20)
        
        print(f"\n  近20日主力资金动向:")
        if main_20 > 0:
            print(f"    🟢 净流入 {main_20/1e8:.2f}亿 (看多信号)")
        else:
            print(f"    🔴 净流出 {abs(main_20)/1e8:.2f}亿 (看空信号)")
        
        # 统计正流入天数
        positive_days = sum(1 for d in recent_20 if d["main_net"] > 0)
        print(f"\n  近20日中，主力资金净流入天数: {positive_days}/20 天 ({positive_days/20*100:.1f}%)")
        
        # 最新一天的分析
        latest = data[-1]
        print(f"\n【5. 最新一日资金流向】({latest['date']})")
        print(f"  主力净流入: {latest['main_net']/10000:.2f}万")
        print(f"  超大单净流入: {latest['super_net']/10000:.2f}万")
        print(f"  大单净流入: {latest['large_net']/10000:.2f}万")
        print(f"  中单净流入: {latest['mid_net']/10000:.2f}万")
        print(f"  小单净流入: {latest['small_net']/10000:.2f}万")
        
        # 判断资金结构
        main_total_latest = latest["main_net"]
        super_large = latest["super_net"] + latest["large_net"]
        mid_small = latest["mid_net"] + latest["small_net"]
        
        print(f"\n  资金结构分析:")
        if super_large > 0 and mid_small < 0:
            print(f"    ✅ 机构买入、散户卖出 (主力看多)")
        elif super_large < 0 and mid_small > 0:
            print(f"    ⚠️ 机构卖出、散户买入 (主力看空)")
        elif super_large > 0 and mid_small > 0:
            print(f"    📊 机构散户都在买 (分歧较小)")
        else:
            print(f"    📊 机构散户都在卖 (分歧较大)")
            
    except Exception as e:
        print(f"  ❌ 获取资金流数据失败: {e}")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    analyze_fund_flow()
