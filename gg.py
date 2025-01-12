import akshare as ak
import streamlit as st

def get_listing_date(stock_code):
    try:
        stock_info = ak.stock_individual_info_em(symbol=stock_code)
        listing_date = stock_info.loc[stock_info['item'] == '上市时间', 'value'].values[0]
        return listing_date
    except Exception as e:
        return f"查询失败: {e}"

def main():
    st.title("股票上市日期查询")
    
    # 输入股票代码
    stock_code = st.text_input("请输入股票代码（例如：300630）：")
    
    if st.button("查询"):
        if stock_code:
            listing_date = get_listing_date(stock_code)
            st.success(f"股票 {stock_code} 的上市日期是：{listing_date}")
        else:
            st.error("请输入有效的股票代码")

if __name__ == "__main__":
    main()
