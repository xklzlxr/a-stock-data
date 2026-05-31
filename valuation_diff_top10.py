#!/usr/bin/env python3
"""
找出10只估值和市值差异最大的股票 - 简洁版本
"""

import requests
import pandas as pd
from a_stock_data import tencent_quote, UA

def main():
    # 备用股票池
    stock_pool = [
        "600519", "000858", "002475", "300059", "600309",
        "688017", "300750", "002594", "601318", "600036",
        "000001", "000002", "600030", "601012", "600887",
        "002415", "000725", "002460", "300124", "300144",
        "600900", "600809", "600176", "600585", "601888",
        "300750", "300760", "300761", "300763", "300770",
        "000568", "000596", "000651", "000725", "000858",
        "600009", "600027", "600030", "600031", "600036",
        "300290", "300308", "300327", "300347", "300357",
        "600596", "600600", "600606", "600690", "600741",
    ]
    
    print("=" * 80)
    print("📊 估值与市值差异最大的10只股票")
    print("=" * 80)
    
    # 获取行情数据
    quotes = tencent_quote(stock_pool)
    
    # 处理数据
    data_list = []
    for code, q in quotes.items():
        price = q.get("price", 0)
        pe_ttm = q.get("pe_ttm", 0)
        pb = q.get("pb", 0)
        mcap_yi = q.get("mcap_yi", 0)
        change_pct = q.get("change_pct", 0)
        
        if mcap_yi > 0 and pe_ttm > 0 and pb > 0:
            score = pe_ttm * pb / mcap_yi
            data_list.append({
                "code": code,
                "name": q["name"],
                "price": price,
                "change_pct": change_pct,
                "pe_ttm": pe_ttm,
                "pb": pb,
                "mcap_yi": mcap_yi,
                "score": score,
            })
    
    df = pd.DataFrame(data_list)
    df_sorted = df.sort_values("score", ascending=False).head(10)
    
    print("\n")
    print("排名 | 代码     | 名称         | PE(TTM) | PB    | 市值(亿)   | 涨跌幅  | 综合评分")
    print("-" * 90)
    
    for idx, (_, row) in enumerate(df_sorted.iterrows(), 1):
        print(f"{idx:2d}   | {row['code']:<8} | {row['name']:<10s} | {row['pe_ttm']:>7.2f} | {row['pb']:>5.2f} | {row['mcap_yi']:>10.2f} | {row['change_pct']:>6.2f}% | {row['score']:.4f}")
    
    print("\n" + "=" * 80)
    print("📈 重点关注：")
    print("=" * 80)
    
    top1 = df_sorted.iloc[0]
    print(f"\n🥇 {top1['name']}({top1['code']})")
    print(f"   • PE: {top1['pe_ttm']:.2f}x")
    print(f"   • PB: {top1['pb']:.2f}x")
    print(f"   • 市值: {top1['mcap_yi']:.2f}亿元")
    print(f"   • 综合评分: {top1['score']:.2f}")
    
    top2 = df_sorted.iloc[1]
    print(f"\n🥈 {top2['name']}({top2['code']})")
    print(f"   • PE: {top2['pe_ttm']:.2f}x")
    print(f"   • PB: {top2['pb']:.2f}x")
    print(f"   • 市值: {top2['mcap_yi']:.2f}亿元")
    print(f"   • 综合评分: {top2['score']:.2f}")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
