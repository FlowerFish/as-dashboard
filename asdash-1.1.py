import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# 頁面配置
st.set_page_config(layout="wide", page_title="汽車銷售綜合圖解儀表板")

# 添加頂部緩衝區以避免內容被遮蓋
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# 標題與描述
st.title("🚗 汽車銷售綜合圖解式分析儀表板")
st.markdown("""
- **設計:  Aries Yeh  V1.1**
- 整合銷售趨勢、產品表現、顧客行為、市場分布、價格策略、庫存管理、市場競爭、營銷效果、顧客反饋及進階分析
""")

# 應用 CSS 樣式，增加頂部內邊距
st.markdown("""
    <style>
        .main {background-color: #f5f7fa;}
        h1, h2, h3, h4 {color: #003366;}
        .block-container {padding: 4rem 2rem 2rem 2rem; margin-top: 20px;}
        .stPlotlyChart {height: 400px;}
    </style>
""", unsafe_allow_html=True)

# 資料載入與預處理
@st.cache_data
def load_data():
    df = pd.read_csv("Auto Sales data.csv")
    df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'], format='%d/%m/%Y')
    df['YEAR'] = df['ORDERDATE'].dt.year
    df['MONTH'] = df['ORDERDATE'].dt.to_period('M')
    return df

df = load_data()

# 用戶自訂儀表板
st.markdown("---")
st.subheader("📊 自訂儀表板")

# 用戶選擇顯示的圖塊
chart_options = {
    "銷售趨勢折線圖": 1,
    "產品表現柱狀圖": 2,
    "顧客行為散點圖": 3,
    "地理分布地圖圖": 4,
    "價格策略箱形圖": 5,
    "庫存管理熱力圖": 6,
    "市場競爭雷達圖": 7,
    "營銷效果柱狀圖": 8,
    "顧客反饋圓餅圖": 9,
    "客戶生命週期分群圖": 10,
    "銷售熱力地圖": 11,
    "單價 vs 數量利潤圖": 12,
    "回購週期雷達圖": 13,
    "國家 → 產品線流向圖": 14,
    "Deal Size 潛力矩陣圖": 15
}
selected_charts = st.multiselect(
    "選擇要顯示的分析圖塊",
    options=list(chart_options.keys()),
    default=list(chart_options.keys())  # 預設全選
)

# 用戶選擇每行欄數
cols_per_row = st.slider("選擇每行顯示的欄數", 1, 5, 3)

# 動態佈局：根據選擇的圖塊數量和欄數決定佈局
num_charts = len(selected_charts)
if num_charts == 0:
    st.warning("請至少選擇一個圖塊！")
else:
    # 計算所需行數
    rows_needed = (num_charts + cols_per_row - 1) // cols_per_row

    # 迭代生成圖塊
    chart_index = 0
    for row in range(rows_needed):
        cols = st.columns(cols_per_row)
        for col in cols:
            if chart_index < len(selected_charts):
                chart_name = selected_charts[chart_index]
                chart_id = chart_options[chart_name]
                
                with col:
                    # 圖塊 1: 銷售趨勢折線圖
                    if chart_id == 1:
                        st.markdown("#### 1️⃣ 銷售趨勢折線圖")
                        st.caption("月度銷售趨勢（折線圖）")
                        sales_trend = df.groupby('MONTH')['SALES'].sum().reset_index()
                        sales_trend['MONTH'] = sales_trend['MONTH'].astype(str)
                        avg_sales = sales_trend['SALES'].mean()
                        fig1 = px.line(
                            sales_trend,
                            x='MONTH',
                            y='SALES',
                            title='月度銷售趨勢',
                            markers=True,
                            color_discrete_sequence=px.colors.sequential.Plasma
                        )
                        fig1.add_hline(
                            y=avg_sales,
                            line_dash="dash",
                            line_color="orange",
                            annotation_text="平均銷售額",
                            annotation_position="top left"
                        )
                        fig1.update_layout(paper_bgcolor='lightblue', plot_bgcolor='white')
                        st.plotly_chart(fig1, use_container_width=True)

                    # 圖塊 2: 產品表現柱狀圖
                    elif chart_id == 2:
                        st.markdown("#### 2️⃣ 產品表現柱狀圖")
                        st.caption("產品線銷售表現（柱狀圖）")
                        product_sales = df.groupby('PRODUCTLINE')['SALES'].sum().reset_index()
                        fig2 = px.bar(product_sales, x='PRODUCTLINE', y='SALES', title='產品線銷售表現', 
                                     color='PRODUCTLINE', color_discrete_sequence=px.colors.sequential.Greens)
                        st.plotly_chart(fig2, use_container_width=True)

                    # 圖塊 3: 顧客行為散點圖
                    elif chart_id == 3:
                        st.markdown("#### 3️⃣ 顧客行為散點圖")
                        st.caption("顧客訂單量與銷售額關係（散點圖）")
                        customer_behavior = df.groupby('CUSTOMERNAME').agg({'QUANTITYORDERED': 'sum', 'SALES': 'sum'}).reset_index()
                        fig3 = px.scatter(customer_behavior, x='QUANTITYORDERED', y='SALES', color='CUSTOMERNAME', 
                                        title='顧客訂單量與銷售額關係', color_discrete_sequence=px.colors.sequential.Reds)
                        fig3.add_hline(y=customer_behavior['SALES'].mean(), line_dash='dash', line_color='black', annotation_text='平均銷售額')
                        fig3.add_vline(x=customer_behavior['QUANTITYORDERED'].mean(), line_dash='dash', line_color='black', annotation_text='平均訂單量')
                        trend = np.polyfit(customer_behavior['QUANTITYORDERED'], customer_behavior['SALES'], 1)
                        fig3.add_trace(go.Scatter(x=customer_behavior['QUANTITYORDERED'], 
                                                y=np.poly1d(trend)(customer_behavior['QUANTITYORDERED']), 
                                                mode='lines', name='趨勢線'))
                        st.plotly_chart(fig3, use_container_width=True)

                    # 圖塊 4: 地理分布地圖圖
                    elif chart_id == 4:
                        st.markdown("#### 4️⃣ 地理分布地圖圖")
                        st.caption("全球銷售分布（地圖圖）")
                        country_sales = df.groupby('COUNTRY')['SALES'].sum().reset_index()
                        fig4 = px.choropleth(country_sales, locations='COUNTRY', locationmode='country names', 
                                            color='SALES', title='全球銷售分布', color_continuous_scale=px.colors.sequential.Purples)
                        st.plotly_chart(fig4, use_container_width=True)

                    # 圖塊 5: 價格策略箱形圖
                    elif chart_id == 5:
                        st.markdown("#### 5️⃣ 價格策略箱形圖")
                        st.caption("交易規模與價格關係（箱形圖）")
                        fig5 = px.box(df, x='DEALSIZE', y='PRICEEACH', title='交易規模與價格關係', 
                                     color='DEALSIZE', color_discrete_sequence=px.colors.sequential.Oranges)
                        st.plotly_chart(fig5, use_container_width=True)

                    # 圖塊 6: 庫存管理熱力圖
                    elif chart_id == 6:
                        st.markdown("#### 6️⃣ 庫存管理熱力圖")
                        st.caption("產品訂單量熱力圖")
                        product_quantity = df.groupby(['PRODUCTCODE', 'PRODUCTLINE'])['QUANTITYORDERED'].sum().reset_index()
                        fig6 = px.density_heatmap(product_quantity, x='PRODUCTCODE', y='PRODUCTLINE', z='QUANTITYORDERED', 
                                                title='產品訂單量熱力圖', color_continuous_scale='YlOrRd')
                        st.plotly_chart(fig6, use_container_width=True)

                    # 圖塊 7: 市場競爭雷達圖
                    elif chart_id == 7:
                        st.markdown("#### 7️⃣ 市場競爭雷達圖")
                        st.caption("產品線競爭力（雷達圖）")
                        product_competition = df.groupby('PRODUCTLINE')['SALES'].mean().reset_index()
                        fig7 = go.Figure()
                        fig7.add_trace(go.Scatterpolar(r=product_competition['SALES'], theta=product_competition['PRODUCTLINE'], 
                                                     fill='toself', fillcolor='#00BFFF', opacity=0.6, line=dict(color='#00BFFF', width=2)))
                        fig7.update_layout(polar=dict(radialaxis=dict(visible=True, tickfont=dict(color='red')), 
                                                    angularaxis=dict(tickfont=dict(color='limegreen'))), 
                                         title='產品線競爭力雷達圖')
                        st.plotly_chart(fig7, use_container_width=True)

                    # 圖塊 8: 營銷效果柱狀圖
                    elif chart_id == 8:
                        st.markdown("#### 8️⃣ 營銷效果柱狀圖")
                        st.caption("營銷活動銷售效果（柱狀圖）")
                        marketing_effect = df.groupby('DEALSIZE')['SALES'].sum().reset_index()
                        fig8 = px.bar(marketing_effect, x='DEALSIZE', y='SALES', title='營銷活動銷售效果', 
                                     color='DEALSIZE', color_discrete_sequence=px.colors.sequential.Greens)
                        st.plotly_chart(fig8, use_container_width=True)

                    # 圖塊 9: 顧客反饋圓餅圖
                    elif chart_id == 9:
                        st.markdown("#### 9️⃣ 顧客反饋圓餅圖")
                        st.caption("顧客滿意度分析（圓餅圖）")
                        feedback = df['STATUS'].value_counts().reset_index()
                        feedback.columns = ['STATUS', 'COUNT']
                        fig9 = px.pie(feedback, values='COUNT', names='STATUS', title='顧客滿意度分析', 
                                     color_discrete_sequence=px.colors.sequential.Reds)
                        st.plotly_chart(fig9, use_container_width=True)

                    # 圖塊 10: 客戶生命週期分群圖
                    elif chart_id == 10:
                        st.markdown("#### 🔟 客戶生命週期分群圖")
                        st.caption("活躍、流失與潛力客戶（氣泡圖）")
                        latest_orders = df.groupby("CUSTOMERNAME")['ORDERDATE'].max().reset_index()
                        latest_orders['DAYS_SINCE_LASTORDER'] = (df['ORDERDATE'].max() - latest_orders['ORDERDATE']).dt.days
                        sales_sum = df.groupby("CUSTOMERNAME")['SALES'].sum().reset_index()
                        merged = pd.merge(latest_orders, sales_sum, on="CUSTOMERNAME")
                        fig10 = px.scatter(merged, x="DAYS_SINCE_LASTORDER", y="SALES", size="SALES", color="SALES",
                                         hover_name="CUSTOMERNAME", title="客戶活躍程度與貢獻氣泡圖",
                                         labels={"DAYS_SINCE_LASTORDER": "距上次訂單天數", "SALES": "總銷售金額"})
                        st.plotly_chart(fig10, use_container_width=True)

                    # 圖塊 11: 銷售熱力地圖
                    elif chart_id == 11:
                        st.markdown("#### 1️⃣1️⃣ 銷售熱力地圖")
                        st.caption("國家對產品線的偏好（熱力交叉表）")
                        pivot = df.pivot_table(values='SALES', index='COUNTRY', columns='PRODUCTLINE', aggfunc='sum', fill_value=0)
                        fig11 = px.imshow(pivot, text_auto=True, color_continuous_scale='Blues', aspect="auto",
                                         title="不同國家對產品線的銷售熱度")
                        st.plotly_chart(fig11, use_container_width=True)

                    # 圖塊 12: 單價 vs 數量利潤圖
                    elif chart_id == 12:
                        st.markdown("#### 1️⃣2️⃣ 單價 vs 數量利潤圖")
                        st.caption("單價與數量，氣泡代表營收")
                        fig12 = px.scatter(df, x='PRICEEACH', y='QUANTITYORDERED', size='SALES', color='PRODUCTLINE',
                                         title="單價與數量的利潤分布圖",
                                         labels={'PRICEEACH': '單價', 'QUANTITYORDERED': '數量'})
                        st.plotly_chart(fig12, use_container_width=True)

                    # 圖塊 13: 回購週期雷達圖
                    elif chart_id == 13:
                        st.markdown("#### 1️⃣3️⃣ 回購週期雷達圖")
                        st.caption("各產品線的平均回購週期")
                        repurchase = df.groupby(['CUSTOMERNAME', 'PRODUCTLINE'])['ORDERDATE'].agg(['min', 'max', 'count']).reset_index()
                        repurchase['DAYS_BETWEEN'] = (repurchase['max'] - repurchase['min']).dt.days / repurchase['count'].clip(lower=1)
                        radar_data = repurchase.groupby('PRODUCTLINE')['DAYS_BETWEEN'].mean().reset_index()
                        fig13 = go.Figure()
                        fig13.add_trace(go.Scatterpolar(
                            r=radar_data['DAYS_BETWEEN'],
                            theta=radar_data['PRODUCTLINE'],
                            fill='toself',
                            name='平均回購週期 (天)'
                        ))
                        fig13.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=False,
                                          title="各產品線平均回購週期雷達圖")
                        st.plotly_chart(fig13, use_container_width=True)

                    # 圖塊 14: 國家 → 產品線流向圖
                    elif chart_id == 14:
                        st.markdown("#### 1️⃣4️⃣ 國家 → 產品線流向圖")
                        st.caption("各國家顧客的產品線偏好（Sankey圖）")
                        sankey_data = df.groupby(['COUNTRY', 'PRODUCTLINE'])['SALES'].sum().reset_index()
                        countries = sankey_data['COUNTRY'].unique().tolist()
                        products = sankey_data['PRODUCTLINE'].unique().tolist()
                        labels = countries + products
                        source = sankey_data['COUNTRY'].apply(lambda x: countries.index(x)).tolist()
                        target = sankey_data['PRODUCTLINE'].apply(lambda x: len(countries) + products.index(x)).tolist()
                        values = sankey_data['SALES'].tolist()
                        fig14 = go.Figure(data=[go.Sankey(
                            node=dict(pad=15, thickness=20, line=dict(color="black", width=0.5), label=labels),
                            link=dict(source=source, target=target, value=values)
                        )])
                        fig14.update_layout(title_text="國家 → 產品線 銷售流向圖", font_size=10)
                        st.plotly_chart(fig14, use_container_width=True)

                    # 圖塊 15: Deal Size 潛力矩陣圖
                    elif chart_id == 15:
                        st.markdown("#### 1️⃣5️⃣ Deal Size 潛力矩陣圖")
                        st.caption("客戶數與平均交易額的策略象限")
                        deal_data = df.groupby(['CUSTOMERNAME', 'DEALSIZE'])['SALES'].sum().reset_index()
                        deal_summary = deal_data.groupby('DEALSIZE').agg({'CUSTOMERNAME': 'nunique', 'SALES': 'mean'}).reset_index()
                        fig15 = px.scatter(deal_summary, x='CUSTOMERNAME', y='SALES', text='DEALSIZE',
                                         title="交易規模潛力象限圖",
                                         labels={'CUSTOMERNAME': '客戶數', 'SALES': '平均交易額'}, size=[30]*len(deal_summary))
                        fig15.update_traces(textposition='top center')
                        st.plotly_chart(fig15, use_container_width=True)

                chart_index += 1

# 頁尾
st.markdown("---")
st.info("📈 儀表板完畢。可根據業務策略需求進一步延伸分析，如客戶留存率、產品升級率、促銷反應等。")