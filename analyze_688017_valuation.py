#!/usr/bin/env python3
"""
分析688017绿的谐波的估值与市值对应关系
"""

from a_stock_data import tencent_quote, full_valuation, ths_eps_forecast
import pandas as pd

def analyze_688017():
    code = "688017"
    
    print("=" * 80)
    print(f"📊 {code} 绿的谐波 - 估值与市值深度分析")
    print("=" * 80)
    
    # 获取行情数据
    quotes = tencent_quote([code])
    if code not in quotes:
        print("无法获取行情数据")
        return
    
    q = quotes[code]
    
    # 基础数据
    price = q["price"]
    mcap_yi = q["mcap_yi"]
    pe_ttm = q["pe_ttm"]
    pb = q["pb"]
    pe_static = q["pe_static"]
    
    print("\n【1. 当前数据】")
    print(f"  当前股价: {price:.2f} 元")
    print(f"  总市值: {mcap_yi:.2f} 亿元 ({mcap_yi*100000000:.0f} 元)")
    print(f"  流通市值: {q['float_mcap_yi']:.2f} 亿元")
    print(f"  PE(TTM): {pe_ttm:.2f}x")
    print(f"  PE(静): {pe_static:.2f}x")
    print(f"  PB: {pb:.2f}x")
    
    # 计算市值对应的估值指标
    print("\n【2. 市值对应关系计算】")
    
    # 假设净利润
    if pe_ttm > 0:
        implied_eps = price / pe_ttm
        implied_net_profit_yi = mcap_yi / pe_ttm  # 亿元
        implied_net_profit_wan = implied_net_profit_yi * 10000  # 万元
        
        print(f"\n  基于PE({pe_ttm:.2f}x)的推算:")
        print(f"    净利润 = 总市值 / PE = {mcap_yi:.2f}亿 / {pe_ttm:.2f}")
        print(f"          = {implied_net_profit_yi:.4f} 亿元")
        print(f"          = {implied_net_profit_wan:.2f} 万元")
        print(f"          = {implied_net_profit_yi*100000000:.0f} 元")
    
    # 假设净资产
    if pb > 0:
        implied_bps = price / pb
        implied_book_yi = mcap_yi / pb
        implied_book_wan = implied_book_yi * 10000
        
        print(f"\n  基于PB({pb:.2f}x)的推算:")
        print(f"    净资产 = 总市值 / PB = {mcap_yi:.2f}亿 / {pb:.2f}")
        print(f"          = {implied_book_yi:.4f} 亿元")
        print(f"          = {implied_book_wan:.2f} 万元")
        print(f"          = {implied_book_yi*100000000:.0f} 元")
    
    # 估算股本
    total_shares_yi = mcap_yi / price  # 亿股
    total_shares_wan = total_shares_yi * 10000  # 万股
    
    print(f"\n  估算总股本:")
    print(f"    总股本 = 总市值 / 股价 = {mcap_yi:.2f}亿 / {price:.2f}元")
    print(f"          = {total_shares_yi:.4f} 亿股")
    print(f"          = {total_shares_wan:.2f} 万股")
    print(f"          = {total_shares_yi*100000000:.0f} 股")
    
    # 计算EPS
    if pe_ttm > 0:
        eps_ttm = price / pe_ttm
        print(f"\n  推算每股收益(EPS):")
        print(f"    EPS = 股价 / PE = {price:.2f}元 / {pe_ttm:.2f}")
        print(f"        = {eps_ttm:.4f} 元/股")
        print(f"        = {eps_ttm*100:.2f} 角/股")
    
    # 计算每股净资产
    if pb > 0:
        bps = price / pb
        print(f"\n  推算每股净资产:")
        print(f"    BPS = 股价 / PB = {price:.2f}元 / {pb:.2f}")
        print(f"        = {bps:.4f} 元/股")
    
    # 对比分析
    print("\n【3. 市值与估值交叉分析】")
    
    # 假设不同的PE水平
    print(f"\n  如果PE分别假设为不同水平，对应的净利润和股价:")
    print(f"  {'PE假设':<10} | {'净利润(亿)':<12} | {'对应股价(元)':<15} | {'说明'}")
    print(f"  {'-'*70}")
    
    pe_assumptions = [
        (10, "低估"),
        (20, "合理偏低"),
        (30, "合理中枢"),
        (50, "合理偏高"),
        (100, "高估"),
        (pe_ttm, "当前实际"),
    ]
    
    for pe_val, desc in pe_assumptions:
        implied_price = eps_ttm * pe_val if pe_ttm > 0 else 0
        implied_profit = mcap_yi / pe_val if pe_val > 0 else 0
        print(f"  {pe_val:<10.0f} | {implied_profit:>10.4f}亿 | {implied_price:>14.2f}元 | {desc}")
    
    # 机构预期
    print("\n【4. 机构一致预期（如果有）】")
    try:
        df = ths_eps_forecast(code)
        if not df.empty:
            print(f"  获取到一致预期数据:")
            print(df.head(3))
        else:
            print("  暂未获取到机构一致预期数据")
    except Exception as e:
        print(f"  获取一致预期失败: {e}")
    
    # 估值合理性分析
    print("\n【5. 估值合理性分析】")
    
    print(f"\n  当前状态:")
    print(f"    • 市值560.99亿，在机器人概念股中属于中大型市值")
    print(f"    • PE高达{pe_ttm:.0f}x，说明市场对公司未来增长预期很高")
    print(f"    • PB为{pb:.2f}x，反映市场对公司净资产溢价很高")
    
    if pe_ttm > 100:
        print(f"\n  ⚠️ 风险提示:")
        print(f"    • PE超过100倍，估值极高")
        print(f"    • 需要非常高的业绩增长才能消化当前估值")
        if pe_ttm > 0:
            required_growth = 100 / pe_ttm * 100
            print(f"    • 需要保持 {required_growth:.1f}% 以上的年复合增长才能维持当前估值")
    
    # 市值对比
    print("\n【6. 同行业市值对比】")
    print(f"    • 绿的谐波市值: {mcap_yi:.2f}亿")
    print(f"    • 工业机器人龙头ABB市值约: 4,500亿 (参考)")
    print(f"    • 国内机器人龙头埃斯顿市值约: 180亿 (参考)")
    print(f"    • 绿的谐波市值处于国内机器人行业较高水平")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    analyze_688017()
