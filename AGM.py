import akshare as ak
import futu as ft
import streamlit as st

def get_hk_stock_listing_date(stock_code):
    """查询港股的上市日期"""
    try:
        # 获取港股基本信息
        stock_info = ak.stock_hk_hist(symbol=stock_code)
        if not stock_info.empty:
            # 假设上市日期是数据的第一行日期
            listing_date = stock_info['日期'].iloc[0]
            return listing_date
        else:
            return f"未找到代码为 {stock_code} 的港股"
    except Exception as e:
        return f"查询失败: {e}"

def get_us_stock_listing_date_futu(stock_code):
    """使用富途牛牛 API 查询美股的上市日期"""
    try:
        # 创建富途牛牛 API 客户端
        quote_ctx = ft.OpenQuoteContext(host="127.0.0.1", port=11111)
        
        # 检查连接状态
        st.write("富途牛牛 API 连接成功！")
        
        # 获取股票基本信息
        ret, data = quote_ctx.get_stock_basicinfo(market=ft.Market.US, code=stock_code)
        if ret == ft.RET_OK:
            listing_date = data.iloc[0]["listing_date"]
            return listing_date
        else:
            return f"未找到代码为 {stock_code} 的美股"
    except Exception as e:
        return f"查询失败: {e}"
    finally:
        quote_ctx.close()  # 关闭连接

def get_a_stock_listing_date(stock_code):
    """查询 A 股的上市日期"""
    try:
        # 使用 akshare 查询 A 股基本信息
        stock_info = ak.stock_individual_info_em(symbol=stock_code)
        listing_date = stock_info.loc[stock_info['item'] == '上市时间', 'value'].values[0]
        return listing_date
    except Exception as e:
        return f"查询失败: {e}"

def main():
    st.title("股票上市日期查询")
    
    # 选择查询类型
    query_type = st.radio("请选择查询类型：", ("A 股", "港股", "美股"))
    
    # 输入股票代码
    if query_type == "A 股":
        stock_code = st.text_input("请输入 A 股代码（例如：300630）：")
    elif query_type == "港股":
        stock_code = st.text_input("请输入港股代码（例如：00700）：")
    else:
        stock_code = st.text_input("请输入美股代码（例如：AAPL）：")
    
    if st.button("查询"):
        if stock_code:
            if query_type == "A 股":
                listing_date = get_a_stock_listing_date(stock_code)
                st.success(f"A 股 {stock_code} 的上市日期是：{listing_date}")
            elif query_type == "港股":
                listing_date = get_hk_stock_listing_date(stock_code)
                st.success(f"港股 {stock_code} 的上市日期是：{listing_date}")
            else:
                listing_date = get_us_stock_listing_date_futu(stock_code)
                st.success(f"美股 {stock_code} 的上市日期是：{listing_date}")
        else:
            st.error("请输入有效的股票代码")

if __name__ == "__main__":
    main()
