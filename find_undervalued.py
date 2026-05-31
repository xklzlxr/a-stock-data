#!/usr/bin/env python3
"""
找出估值被低估的股票 - 专门寻找低估值标的
"""

from a_stock_data import tencent_quote
import pandas as pd

def find_undervalued_stocks():
    # 扩大的股票池
    stock_pool = [
        "600519", "000858", "002475", "300059", "600309",
        "688017", "300750", "002594", "601318", "600036",
        "000001", "000002", "600030", "601012", "600887",
        "002415", "000725", "002460", "300124", "300144",
        "600900", "600809", "600176", "600585", "601888",
        "300760", "300761", "300763", "300770", "000568",
        "000596", "000651", "600009", "600027", "600031",
        "300290", "300308", "300327", "300347", "300357",
        "600596", "600600", "600606", "600690", "600741",
        "300498", "300724", "300759", "300782", "600028",
        "600036", "601166", "601398", "601939", "601328",
        "000001", "002142", "002807", "600926", "601128",
    ]
    
    print("=" * 80)
    print("📊 估值被低估的股票 - 深入分析")
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
            # 低估评分：综合PE、PB，值越小越低估
            undervalue_score = pe_ttm * pb
            data_list.append({
                "code": code,
                "name": q["name"],
                "price": price,
                "change_pct": change_pct,
                "pe_ttm": pe_ttm,
                "pb": pb,
                "mcap_yi": mcap_yi,
                "undervalue_score": undervalue_score,
            })
    
    df = pd.DataFrame(data_list)
    
    # 按低估评分升序排序（越小越低估）
    df_undervalued = df.sort_values("undervalue_score", ascending=True)
    
    print("\n【1. 前15个低估标的初步筛选】")
    print(f"\n{'排名':<6} {'代码':<8} {'名称':<12} {'PE':<8} {'PB':<8} {'市值(亿)':<12} {'涨跌幅':<8} {'低估评分':<10}")
    print("-" * 85)
    
    for idx, (_, row) in enumerate(df_undervalued.head(15).iterrows(), 1):
        print(f"{idx:<6} {row['code']:<8} {row['name']:<12} {row['pe_ttm']:<8.2f} {row['pb']:<8.2f} {row['mcap_yi']:<12.2f} {row['change_pct']:<+8.2f} {row['undervalue_score']:<10.2f}")
    
    print("\n" + "=" * 80)
    print("【2. TOP 3 深度分析】")
    print("=" * 80)
    
    top3 = df_undervalued.head(3)
    
    for idx, (_, row) in enumerate(top3.iterrows(), 1):
        print(f"\n{'#'*80}")
        print(f"🥇 #{idx} {row['name']}({row['code']})")
        print(f"{'#'*80}")
        print(f"\n  股价: {row['price']:.2f}元, 涨跌幅: {row['change_pct']:+.2f}%")
        print(f"  总市值: {row['mcap_yi']:.2f}亿元")
        print(f"  PE(TTM): {row['pe_ttm']:.2f}倍")
        print(f"  PB: {row['pb']:.2f}倍")
        print(f"  低估评分: {row['undervalue_score']:.2f} (越低越低估)")
        
        # 估值分析
        print(f"\n  📊 估值评价:")
        if row['pe_ttm'] < 10:
            print(f"    ✅ PE {row['pe_ttm']:.2f}x < 10，非常低估")
        elif row['pe_ttm'] < 20:
            print(f"    ✅ PE {row['pe_ttm']:.2f}x < 20，比较低估")
        elif row['pe_ttm'] < 30:
            print(f"    ⚠️ PE {row['pe_ttm']:.2f}x < 30，估值适中")
        else:
            print(f"    ⚠️ PE {row['pe_ttm']:.2f}x，估值偏高")
            
        if row['pb'] < 1:
            print(f"    ✅ PB {row['pb']:.2f}x < 1，破净！！")
        elif row['pb'] < 2:
            print(f"    ✅ PB {row['pb']:.2f}x < 2，偏低估")
        elif row['pb'] < 3:
            print(f"    ⚠️ PB {row['pb']:.2f}x，适中")
        else:
            print(f"    ⚠️ PB {row['pb']:.2f}x，偏高")
            
        # 投资建议
        print(f"\n  💡 投资建议:")
        if row['pe_ttm'] < 15 and row['pb'] < 2:
            print(f"    🟢 强烈关注！低PE+低PB，安全边际高")
        elif row['pe_ttm'] < 20 and row['pb'] < 2.5:
            print(f"    🟡 值得关注，估值较低")
        else:
            print(f"    ⚪ 估值适中或偏高，谨慎评估")
    
    print("\n" + "=" * 80)
    print("📋 筛选标准说明:")
    print("=" * 80)
    print("  • 低估评分 = PE × PB，值越小表示估值越低")
    print("  • PE < 10 为非常低估，10-20 为比较低估")
    print("  • PB < 1 为破净（市值低于净资产）")
    print("  • 优先选择 PE < 15 且 PB < 2 的标的")
    
    print("\n" + "=" * 80)
    
    # 输出最终TOP3
    return df_undervalued.head(3)

if __name__ == "__main__":
    top3 = find_undervalued_stocks()
