#!/usr/bin/env python3
"""
找出估值和市值差异最大的股票
"""

import requests
import pandas as pd
from a_stock_data import tencent_quote, UA
import random

def get_stock_pool():
    """获取一个股票池（使用东财API获取A股列表）"""
    print("正在获取A股股票列表...")
    
    # 尝试获取A股列表
    try:
        url = "https://push2.eastmoney.com/api/qt/clist/get"
        params = {
            "pn": "1",
            "pz": "500",  # 先获取500只股票
            "po": "1",
            "np": "1",
            "fltt": "2",
            "invt": "2",
            "fid": "f3",
            "fs": "m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23",  # 沪深A股
            "fields": "f12,f13,f14,f2,f3,f6,f9,f10,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f45,f46",
        }
        headers = {"User-Agent": UA}
        r = requests.get(url, params=params, headers=headers, timeout=15)
        d = r.json()
        items = d.get("data", {}).get("diff", [])
        
        if items:
            codes = [item.get("f12", "") for item in items if item.get("f12", "")]
            print(f"获取到 {len(codes)} 只股票")
            return codes
    except Exception as e:
        print(f"获取股票列表失败: {e}")
    
    # 备用：使用一些代表性股票
    print("使用备用股票池...")
    return [
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

def analyze_valuation_market_cap_diff():
    """分析估值和市值差异最大的股票"""
    print("=" * 80)
    print("📊 估值与市值差异最大股票分析")
    print("=" * 80)
    
    # 1. 获取股票池
    stock_pool = get_stock_pool()
    
    # 2. 批量获取行情数据
    print(f"\n正在获取 {len(stock_pool)} 只股票的行情数据...")
    quotes = tencent_quote(stock_pool)
    print(f"成功获取 {len(quotes)} 只股票的完整数据")
    
    # 3. 处理数据
    data_list = []
    for code, q in quotes.items():
        name = q.get("name", "")
        price = q.get("price", 0)
        pe_ttm = q.get("pe_ttm", 0)
        pb = q.get("pb", 0)
        mcap_yi = q.get("mcap_yi", 0)
        float_mcap_yi = q.get("float_mcap_yi", 0)
        change_pct = q.get("change_pct", 0)
        
        # 过滤无效数据
        if mcap_yi <= 0 or price <= 0:
            continue
        
        # 计算估值指标（PE必须有效，不能为负或0）
        if pe_ttm > 0:
            # 方法1: 计算PE与市值的比率 (高PE + 小市值 = 高比值)
            pe_mcap_ratio = pe_ttm / mcap_yi
            
            # 方法2: 计算PB与市值的比率
            pb_mcap_ratio = pb / mcap_yi if pb > 0 else 0
            
            # 方法3: 综合评分（归一化）
            score = pe_ttm * pb / mcap_yi if mcap_yi > 0 else 0
        else:
            pe_mcap_ratio = 0
            pb_mcap_ratio = 0
            score = 0
        
        data_list.append({
            "code": code,
            "name": name,
            "price": price,
            "change_pct": change_pct,
            "pe_ttm": pe_ttm,
            "pb": pb,
            "mcap_yi": mcap_yi,
            "float_mcap_yi": float_mcap_yi,
            "pe_mcap_ratio": pe_mcap_ratio,
            "pb_mcap_ratio": pb_mcap_ratio,
            "score": score,
        })
    
    df = pd.DataFrame(data_list)
    print(f"\n有效数据样本: {len(df)} 只股票")
    
    if len(df) == 0:
        print("没有有效数据！")
        return
    
    # 4. 按不同指标排序
    print("\n" + "=" * 80)
    print("【1. 按 PE/市值 比率排序（前10名，高估值+小市值）】")
    print("=" * 80)
    df_pe_sorted = df[df["pe_ttm"] > 0].sort_values("pe_mcap_ratio", ascending=False).head(10)
    
    print(f"\n{'排名':<6} {'代码':<8} {'名称':<12} {'价格(元)':<10} {'涨跌幅':<10} {'PE(TTM)':<12} {'市值(亿)':<12} {'PE/市值':<15}")
    print("-" * 95)
    for idx, (_, row) in enumerate(df_pe_sorted.iterrows(), 1):
        print(f"{idx:<6} {row['code']:<8} {row['name']:<12} {row['price']:<10.2f} {row['change_pct']:<10.2f} {row['pe_ttm']:<12.2f} {row['mcap_yi']:<12.2f} {row['pe_mcap_ratio']:<15.6f}")
    
    print("\n" + "=" * 80)
    print("【2. 按 PB/市值 比率排序（前10名）】")
    print("=" * 80)
    df_pb_sorted = df[df["pb"] > 0].sort_values("pb_mcap_ratio", ascending=False).head(10)
    
    print(f"\n{'排名':<6} {'代码':<8} {'名称':<12} {'价格(元)':<10} {'涨跌幅':<10} {'PB':<12} {'市值(亿)':<12} {'PB/市值':<15}")
    print("-" * 95)
    for idx, (_, row) in enumerate(df_pb_sorted.iterrows(), 1):
        print(f"{idx:<6} {row['code']:<8} {row['name']:<12} {row['price']:<10.2f} {row['change_pct']:<10.2f} {row['pb']:<12.2f} {row['mcap_yi']:<12.2f} {row['pb_mcap_ratio']:<15.6f}")
    
    print("\n" + "=" * 80)
    print("【3. 按综合评分（PE*PB/市值）排序（前10名）】")
    print("=" * 80)
    df_score_sorted = df[(df["pe_ttm"] > 0) & (df["pb"] > 0)].sort_values("score", ascending=False).head(10)
    
    print(f"\n{'排名':<6} {'代码':<8} {'名称':<12} {'价格(元)':<10} {'涨跌幅':<10} {'PE(TTM)':<12} {'PB':<12} {'市值(亿)':<12} {'综合评分':<15}")
    print("-" * 105)
    for idx, (_, row) in enumerate(df_score_sorted.iterrows(), 1):
        print(f"{idx:<6} {row['code']:<8} {row['name']:<12} {row['price']:<10.2f} {row['change_pct']:<10.2f} {row['pe_ttm']:<12.2f} {row['pb']:<12.2f} {row['mcap_yi']:<12.2f} {row['score']:<15.6f}")
    
    print("\n" + "=" * 80)
    print("【4. 估值最低+市值最小的10只股票（潜在低估值标的）】")
    print("=" * 80)
    
    # 筛选市值较小且PE较低的股票
    df_low = df[(df["pe_ttm"] > 0) & (df["mcap_yi"] > 0)].copy()
    df_low["low_val_score"] = df_low["pe_ttm"] * df_low["mcap_yi"]  # 越小越好
    df_low_sorted = df_low.sort_values("low_val_score", ascending=True).head(10)
    
    print(f"\n{'排名':<6} {'代码':<8} {'名称':<12} {'价格(元)':<10} {'涨跌幅':<10} {'PE(TTM)':<12} {'PB':<12} {'市值(亿)':<12}")
    print("-" * 100)
    for idx, (_, row) in enumerate(df_low_sorted.iterrows(), 1):
        print(f"{idx:<6} {row['code']:<8} {row['name']:<12} {row['price']:<10.2f} {row['change_pct']:<10.2f} {row['pe_ttm']:<12.2f} {row['pb']:<12.2f} {row['mcap_yi']:<12.2f}")
    
    print("\n" + "=" * 80)
    print("📊 分析说明")
    print("=" * 80)
    print("""
- 【1. PE/市值比率】: 表示每1亿市值对应的PE倍数，数值越大表示估值相对市值越偏高
- 【2. PB/市值比率】: 类似，但用PB衡量估值
- 【3. 综合评分】: PE*PB/市值，综合考虑两种估值指标
- 【4. 低估值标的】: PE较低且市值较小的股票，可能存在低估机会
    """)

if __name__ == "__main__":
    analyze_valuation_market_cap_diff()
