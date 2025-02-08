import akshare as ak
import streamlit as st
import re
import pandas as pd

def clean_stock_code(stock_code):
    """清除股票代码中的后缀（如 .SH, .SZ, .HK）"""
    return re.sub(r'\.\w+$', '', stock_code.strip())

def get_a_stock_listing_date(stock_code):
    """查询 A 股的上市日期"""
    try:
        stock_info = ak.stock_individual_info_em(symbol=stock_code)
        listing_date = stock_info.loc[stock_info['item'] == '上市时间', 'value'].values[0]
        listing_date_with_time = f"{listing_date}0930"
        return listing_date_with_time
    except Exception as e:
        return f"查询失败: {e}"

def get_hk_stock_listing_date(stock_code):
    """查询港股的上市日期"""
    try:
        stock_info = ak.stock_hk_hist(symbol=stock_code)
        if not stock_info.empty:
            listing_date = stock_info['日期'].iloc[0]
            return listing_date
        else:
            return f"未找到代码为 {stock_code} 的港股"
    except Exception as e:
        return f"查询失败: {e}"

def main():
    st.title("A 股/港股上市日期查询")
    
    query_type = st.radio("请选择查询类型：", ("A 股", "港股"))
    batch_query = st.checkbox("批量查询", value=False)
    
    if batch_query:
        stock_codes_input = st.text_area(
            "请输入股票代码，每行一个或用逗号分隔",
            help="支持带有后缀的代码（如 688530.SH 或 00700.HK）"
        )
        stock_codes = [clean_stock_code(code) for code in re.split(r'[,\n]', stock_codes_input) if code.strip()]
    else:
        stock_code = st.text_input(
            "请输入股票代码（支持带后缀如 688530.SH）" if query_type == "A 股" else "请输入港股代码（支持带后缀如 00700.HK）"
        )
        stock_codes = [clean_stock_code(stock_code)] if stock_code.strip() else []
    
    if st.button("查询"):
        if not stock_codes:
            st.error("请输入有效的股票代码")
        else:
            results = []
            if query_type == "A 股":
                for code in stock_codes:
                    listing_date = get_a_stock_listing_date(code)
                    results.append({"股票代码": code, "上市日期": listing_date})
            else:
                for code in stock_codes:
                    listing_date = get_hk_stock_listing_date(code)
                    results.append({"股票代码": code, "上市日期": listing_date})
            
            # 将结果转换为 DataFrame 后展示
            df_results = pd.DataFrame(results)
            st.dataframe(df_results)

if __name__ == "__main__":
    main()
