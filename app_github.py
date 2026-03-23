# # import streamlit as st
# # import pandas as pd
# # import io
# # from openai import OpenAI
# # import os

# # # 1. 页面配置与标题
# # st.set_page_config(page_title="AI 营销数据洞察助手", page_icon="📈", layout="wide")
# # st.title("📈 AI 营销数据洞察助手 (Demo版)")
# # st.markdown("上传您的营销数据（CSV/Excel），AI 将自动帮您找出核心问题并提供优化建议。")

# # # --- 核心修改1：兼容本地测试和云端部署 ---
# # # 如果在本地测试，把你的 sk- 密钥写在逗号后面的引号里
# # # 部署到云端时，它会自动优先读取云端的环境变量
# # api_key = os.environ.get("OPENAI_API_KEY", "你的sk-开头的真实密钥放这里用于本地测试")

# # client = OpenAI(
# #     api_key=api_key, 
# #     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1" 
# # )

# # # --- 内置的示例数据 ---
# # SAMPLE_CSV = """日期,广告计划,投放渠道,花费(元),展现量,点击量,转化量,实际销售额(元)
# # 2023-10-25,种草_美妆,小红书KOC,3200,120000,5500,130,28000
# # 2023-10-25,竞品词_核心,百度搜索,4500,18000,1500,95,35000
# # 2023-10-25,冲量_定向,抖音信息流,15000,650000,9500,210,42000
# # 2023-10-26,种草_美妆,小红书KOC,3500,135000,6100,145,31000
# # 2023-10-26,竞品词_核心,百度搜索,4800,19500,1600,105,38500
# # 2023-10-26,冲量_定向,抖音信息流,22000,950000,14000,230,45000
# # 2023-10-27,种草_美妆,小红书KOC,3800,150000,6800,160,34500
# # 2023-10-27,竞品词_核心,百度搜索,5000,21000,1750,115,41000
# # 2023-10-27,冲量_定向,抖音信息流,35000,1500000,18000,180,32000"""


# # # --- 核心修改2：初始化 Streamlit 记忆体 ---
# # if "df" not in st.session_state:
# #     st.session_state.df = None


# # # 3. 数据来源选择：上传 or 示例
# # col1, col2 = st.columns([1, 2])
# # with col1:
# #     use_demo = st.button("✨ 一键使用示例数据体验")
# # with col2:
# #     uploaded_file = st.file_uploader("或者上传您自己的数据 (CSV 格式)", type=["csv", "xlsx"])

# # # 只要点过按钮，就把数据存入“记忆体”中
# # if use_demo:
# #     st.session_state.df = pd.read_csv(io.StringIO(SAMPLE_CSV))
# # elif uploaded_file is not None:
# #     if uploaded_file.name.endswith('.csv'):
# #         st.session_state.df = pd.read_csv(uploaded_file)
# #     else:
# #         st.session_state.df = pd.read_excel(uploaded_file)

# # # 4. 从“记忆体”中读取数据展示
# # if st.session_state.df is not None:
# #     df = st.session_state.df # 把记忆体里的数据拿出来用
    
# #     st.write("---")
# #     st.write("### 📊 数据预览")
# #     st.dataframe(df.head()) 
    
# #     st.write("### 📉 实际销售额趋势分析")
# #     try:
# #         st.line_chart(df.set_index('日期')['实际销售额(元)']) 
# #     except Exception as e:
# #         st.write("提示：当前数据格式不支持生成折线图。")

# #     st.write("### 🧠 AI 深度洞察报告")
# #     if st.button("生成营销分析报告 (调用 AI)"):
# #         with st.spinner("AI 正在疯狂计算与分析中..."):
# #             data_summary = df.describe().to_string() 
# #             data_head = df.head().to_string()
            
# #             prompt = f"""
# #             你是一个资深的数字营销总监。请根据以下营销数据，生成一份极具业务洞察的报告：
# #             数据样例：\n{data_head}\n
# #             数据统计特征：\n{data_summary}\n
# #             请直接输出：1. 渠道红黑榜(明确指出哪个好哪个差) 2. 异常数据预警(如预算浪费) 3. 下一步优化建议。
# #             """
# #             try:
# #                 response = client.chat.completions.create(
# #                     model="qwen-plus",
# #                     messages=[
# #                         {"role": "system", "content": "你是一个专业的数据分析专家，用Markdown排版，使用emoji让排版生动。"},
# #                         {"role": "user", "content": prompt}
# #                     ]
# #                 )
# #                 st.success("报告生成完毕！")
# #                 st.markdown(response.choices[0].message.content)
# #             except Exception as e:
# #                 st.error(f"调用 AI 失败，请检查配置。错误：{e}")


# import streamlit as st
# import pandas as pd
# from openai import OpenAI
# import os

# # 1. 页面配置与标题
# st.set_page_config(page_title="电商全链路数据洞察系统", page_icon="🛒", layout="wide")
# st.title("🛒 平台电商交易数据洞察系统")
# st.markdown("上传您的电商平台订单流水（支持淘宝、京东、拼多多等格式），系统将自动进行人群画像与销售提效分析。")

# # 2. 初始化大模型客户端
# api_key = os.environ.get("OPENAI_API_KEY", "你的sk-开头的真实密钥放这里用于本地测试")
# client = OpenAI(
#     api_key=api_key, 
#     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1" 
# )

# # 3. 数据上传模块
# uploaded_file = st.file_uploader("请上传平台交易数据 (例如: 淘宝.csv, 京东.csv)", type=["csv"])

# if uploaded_file is not None:
#     # 读取数据
#     df = pd.read_csv(uploaded_file)
    
#     # --- 核心数据预处理 (ETL) ---
#     # 把“购买时间”转成标准日期格式，方便画图
#     df['购买时间'] = pd.to_datetime(df['购买时间'])
#     df['日期'] = df['购买时间'].dt.date
    
#     st.write("---")
#     st.write("### 🔍 原始流水数据预览 (前5条)")
#     st.dataframe(df.head())
    
#     # 4. 网页端自动画图分析
#     col1, col2 = st.columns(2)
    
#     with col1:
#         st.write("### 📈 每日销售额趋势 (GMV)")
#         # 按日期汇总消费金额
#         daily_sales = df.groupby('日期')['消费金额'].sum()
#         st.line_chart(daily_sales)
        
#     with col2:
#         st.write("### 📦 各大商品品类销售占比")
#         # 按商品类别汇总消费金额
#         category_sales = df.groupby('商品类别')['消费金额'].sum()
#         st.bar_chart(category_sales)

#     # 5. 提取精华数据，准备喂给 AI
#     st.write("---")
#     st.write("### 🧠 AI 商业深度洞察")
    
#     if st.button("一键生成电商运营报告"):
#         with st.spinner("AI 正在深度剖析用户画像与消费行为..."):
            
#             # 【关键】：让 Python 帮你算出核心指标，而不是发全量数据
#             total_gmv = df['消费金额'].sum()
#             total_orders = len(df)
#             top_category = category_sales.idxmax()
#             top_city = df.groupby('用户城市')['消费金额'].sum().idxmax()
#             avg_age = df['用户年龄'].mean()
#             gender_ratio = df['用户性别'].value_counts().to_dict()
            
#             # 拼装给 AI 的提示词 (Prompt)
#             prompt = f"""
#             你是一位资深的电商平台运营总监。我有一份近期的电商订单交易数据，以下是经过系统计算后的核心指标摘要：
            
#             【核心业绩指标】
#             - 总销售额 (GMV): {total_gmv:.2f} 元
#             - 总订单量: {total_orders} 笔
#             - 客单价: {total_gmv/total_orders:.2f} 元
            
#             【商品与用户画像】
#             - 最畅销商品类别: {top_category}
#             - 消费主力城市: {top_city}
#             - 消费者平均年龄: {avg_age:.1f} 岁
#             - 男女消费者比例: {gender_ratio}
            
#             请根据以上摘要数据，生成一份极具业务洞察的报告。请直接输出：
#             1. 业绩基本盘诊断 (当前的客单价和销量说明了什么问题？)
#             2. 用户画像分析 (针对这群主力消费者，有什么特征？)
#             3. 下一步选品与营销建议 (结合最畅销品类和主力人群，应该主推什么？去哪个城市推？)
#             """
            
#             try:
#                 response = client.chat.completions.create(
#                     model="qwen-plus",
#                     messages=[
#                         {"role": "system", "content": "你是一个专业、犀利的电商数据分析专家，用Markdown排版，多用加粗和列表，使用emoji让排版生动。"},
#                         {"role": "user", "content": prompt}
#                     ]
#                 )
#                 st.success("运营报告生成完毕！")
#                 st.markdown(response.choices[0].message.content)
#             except Exception as e:
#                 st.error(f"调用 AI 失败，错误信息：{e}")
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from openai import OpenAI
import os
import datetime

# ==========================================
# 1. 页面配置与全局 UI 美化
# ==========================================
st.set_page_config(page_title="全域电商数据大屏", page_icon="🌐", layout="wide")

# 注入自定义 CSS，让页面看起来更像高级大屏
st.markdown("""
<style>
    div[data-testid="metric-container"] {
        background-color: #f7f9fc;
        border: 1px solid #e2e8f0;
        padding: 5% 5% 5% 10%;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 5px 5px 0px 0px;
        padding: 0 20px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ebf2fa;
        color: #1f77b4;
        border-bottom: 3px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 核心黑科技：一键生成六大平台全维度模拟数据
# ==========================================
@st.cache_data
def generate_mock_data():
    platforms = ['淘宝', '天猫', '京东', '拼多多', '1688', '苏宁']
    categories = ['3C数码', '美妆个护', '服装鞋包', '家居日用', '食品生鲜']
    cities = {
        '北京': [39.9042, 116.4074], '上海': [31.2304, 121.4737], '广州': [23.1291, 113.2644], 
        '深圳': [22.5431, 114.0579], '杭州': [30.2741, 120.1551], '成都': [30.5728, 104.0665],
        '重庆': [29.5332, 106.5050], '武汉': [30.5928, 114.3055], '西安': [34.3416, 108.9398],
        '南京': [32.0603, 118.7969]
    }
    
    dates = pd.date_range(end=datetime.date.today(), periods=30)
    data = []
    
    for d in dates:
        for p in platforms:
            for c in categories:
                # 模拟转化漏斗基础数据
                uv = np.random.randint(5000, 50000)
                pv = int(uv * np.random.uniform(1.5, 3.5))
                cart = int(uv * np.random.uniform(0.1, 0.3))
                order = int(cart * np.random.uniform(0.3, 0.6))
                pay = int(order * np.random.uniform(0.8, 0.95))
                
                # 模拟营收与花费
                price = np.random.randint(50, 500)
                gmv = pay * price
                ad_cost = int(gmv * np.random.uniform(0.05, 0.2)) # ROI 约 5-20
                refund = int(gmv * np.random.uniform(0.02, 0.1))
                
                # 随机城市与满意度
                city = np.random.choice(list(cities.keys()))
                lat, lon = cities[city]
                satisfaction = np.random.uniform(3.5, 5.0)
                
                data.append([d, p, c, city, lat, lon, uv, pv, cart, order, pay, gmv, ad_cost, refund, satisfaction])
                
    df = pd.DataFrame(data, columns=[
        '日期', '平台', '品类', '城市', '纬度', '经度', '访客数(UV)', '浏览量(PV)', 
        '加购数', '下单数', '支付数', '销售额(GMV)', '营销花费', '退款金额', '用户满意度'
    ])
    return df

# 加载数据
with st.spinner("正在连接数据仓库加载核心业务数据..."):
    raw_df = generate_mock_data()

# ==========================================
# 3. 侧边栏：全局数据筛选器
# ==========================================
st.sidebar.image("https://img.icons8.com/color/96/000000/combo-chart--v1.png", width=60)
st.sidebar.title("全域数据看板配置")
st.sidebar.markdown("---")

# 平台多选
selected_platforms = st.sidebar.multiselect(
    "🛒 选择渠道平台", 
    options=raw_df['平台'].unique(), 
    default=raw_df['平台'].unique()
)

# 日期范围
min_date = raw_df['日期'].min().date()
max_date = raw_df['日期'].max().date()
date_range = st.sidebar.date_input("📅 选择分析周期", [min_date, max_date])

# 过滤数据
if len(date_range) == 2:
    start_date, end_date = date_range
    df = raw_df[(raw_df['平台'].isin(selected_platforms)) & 
                (raw_df['日期'].dt.date >= start_date) & 
                (raw_df['日期'].dt.date <= end_date)]
else:
    df = raw_df[raw_df['平台'].isin(selected_platforms)]

if df.empty:
    st.warning("⚠️ 暂无数据，请调整侧边栏的筛选条件。")
    st.stop()

# ==========================================
# 4. 主体内容：多维度 Tab 页面
# ==========================================
st.title("📊 全域电商数据洞察系统 (大厂体验版)")
st.markdown("覆盖流量、转化、交易、用户、商品、营销全生命周期的可视化监控平台。")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💰 交易与大盘", "🧲 流量与漏斗", "📦 商品与供应链", "👥 用户与区域", "🤖 AI 深度诊断"
])

# ----------------- Tab 1: 交易与大盘 -----------------
with tab1:
    st.subheader("大盘核心指标 (交易维)")
    c1, c2, c3, c4 = st.columns(4)
    total_gmv = df['销售额(GMV)'].sum()
    total_cost = df['营销花费'].sum()
    c1.metric("全域总销售额(GMV)", f"¥ {total_gmv / 10000:,.1f} 万")
    c2.metric("总支付订单数", f"{df['支付数'].sum():,} 笔")
    c3.metric("整体客单价", f"¥ {total_gmv / df['支付数'].sum():,.2f}")
    c4.metric("全域营销 ROI", f"{(total_gmv / total_cost):.2f}", delta="产出比")

    col1, col2 = st.columns([6, 4])
    with col1:
        # 趋势图
        daily_gmv = df.groupby(['日期', '平台'])['销售额(GMV)'].sum().reset_index()
        fig_trend = px.area(daily_gmv, x='日期', y='销售额(GMV)', color='平台',
                            title="📈 各平台 GMV 走势对比", template="plotly_white")
        st.plotly_chart(fig_trend, use_container_width=True)
    with col2:
        # 环形饼图
        platform_share = df.groupby('平台')['销售额(GMV)'].sum().reset_index()
        fig_pie = px.pie(platform_share, names='平台', values='销售额(GMV)', hole=0.4,
                         title="🌐 渠道销售额占比", color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_pie.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

# ----------------- Tab 2: 流量与漏斗 -----------------
with tab2:
    st.subheader("转化链路分析 (流量维)")
    col1, col2 = st.columns(2)
    with col1:
        # 核心：漏斗图
        funnel_data = {
            '环节': ['访客(UV)', '加购商品', '提交订单', '最终支付'],
            '人数': [df['访客数(UV)'].sum(), df['加购数'].sum(), df['下单数'].sum(), df['支付数'].sum()]
        }
        fig_funnel = go.Figure(go.Funnel(
            y=funnel_data['环节'], x=funnel_data['人数'],
            textinfo="value+percent initial",
            marker={"color": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]}
        ))
        fig_funnel.update_layout(title="🔽 全链路转化漏斗", template="plotly_white")
        st.plotly_chart(fig_funnel, use_container_width=True)
        
    with col2:
        # 热力图：平台 vs 品类的流量分布
        heatmap_data = df.groupby(['平台', '品类'])['访客数(UV)'].sum().reset_index()
        fig_heat = px.density_heatmap(heatmap_data, x="平台", y="品类", z="访客数(UV)",
                                      title="🔥 流量分布热力图 (UV)", color_continuous_scale="Viridis")
        st.plotly_chart(fig_heat, use_container_width=True)

# ----------------- Tab 3: 商品与供应链 -----------------
with tab3:
    st.subheader("货品表现与履约 (商品维)")
    c1, c2, c3 = st.columns(3)
    c1.metric("商品总动销件数", f"{df['下单数'].sum():,} 件")
    c2.metric("平均用户满意度", f"{df['用户满意度'].mean():.1f} / 5.0", delta="好评")
    c3.metric("整体退款率", f"{(df['退款金额'].sum() / total_gmv)*100:.2f}%", delta="-预警", delta_color="inverse")

    col1, col2 = st.columns(2)
    with col1:
        # 柱状图：品类销售排行
        cat_gmv = df.groupby('品类')['销售额(GMV)'].sum().sort_values(ascending=True).reset_index()
        fig_bar = px.bar(cat_gmv, x='销售额(GMV)', y='品类', orientation='h', 
                         title="📊 品类销售额排行榜", color='销售额(GMV)', color_continuous_scale="Blues")
        st.plotly_chart(fig_bar, use_container_width=True)
    with col2:
        # 树状图：展现更直观的结构
        fig_tree = px.treemap(df, path=['平台', '品类'], values='退款金额',
                              title="📦 退款金额结构分布 (Treemap)", color='退款金额', color_continuous_scale="Reds")
        st.plotly_chart(fig_tree, use_container_width=True)

# ----------------- Tab 4: 用户与区域 -----------------
with tab4:
    st.subheader("高价值人群地图 (用户维)")
    
    # 核心：全国城市气泡地图
    city_data = df.groupby(['城市', '纬度', '经度']).agg({'销售额(GMV)': 'sum', '访客数(UV)': 'sum'}).reset_index()
    # 使用 open-street-map 免费底图
    fig_map = px.scatter_mapbox(city_data, lat="纬度", lon="经度", size="销售额(GMV)", color="访客数(UV)",
                                hover_name="城市", hover_data=["销售额(GMV)"],
                                color_continuous_scale=px.colors.cyclical.IceFire, size_max=40, zoom=3,
                                title="🗺️ 全国核心城市消费力分布地图")
    fig_map.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":40,"l":0,"b":0})
    st.plotly_chart(fig_map, use_container_width=True)

# ----------------- Tab 5: AI 深度诊断 -----------------
with tab5:
    st.subheader("🧠 阿里云通义千问专家诊断")
    st.markdown("基于当前筛选的日期和平台数据，由 AI 生成总监级业务洞察。")
    
    api_key = os.environ.get("OPENAI_API_KEY", "sk-cdc57fd44a394cea8ec25dd4ad2512f7")
    client = OpenAI(
        api_key=api_key, 
        base_url="https://ws-vvr85dv3ndbxfxtu.ap-southeast-1.maas.aliyuncs.com/compatible-model/v1" 
    )

    if st.button("✨ 一键生成全域业务诊断报告 ✨", type="primary"):
        with st.spinner("AI 正在深度分析各项指标..."):
            # 聚合核心数据给大模型
            summary = f"""
            分析周期：{len(df['日期'].unique())}天。平台：{', '.join(df['平台'].unique())}。
            整体大盘：总访客 {df['访客数(UV)'].sum()}，支付订单 {df['支付数'].sum()}，总GMV {total_gmv}，营销花费 {total_cost}，退款率 {(df['退款金额'].sum() / total_gmv):.2%}。
            转化漏斗：UV到加购率 {(df['加购数'].sum()/df['访客数(UV)'].sum()):.2%}，加购到支付率 {(df['支付数'].sum()/df['加购数'].sum()):.2%}。
            Top2高营收品类及金额：{df.groupby('品类')['销售额(GMV)'].sum().nlargest(2).to_dict()}。
            """
            prompt = f"""
            你是一名年薪百万的电商数据总监。请根据以下大屏汇总数据，生成极具深度的业务诊断报告。
            【数据概况】：\n{summary}\n
            请严格包含以下4个部分（用Markdown及emoji）：
            1. **全局诊断**：一句话定调近期业绩健康度，点算整体 ROI 和退款率是否健康。
            2. **漏斗断层分析**：分析流量转化链路，指出哪个环节流失最严重。
            3. **品类/渠道红黑榜**：指出表现最好的摇钱树，和拖后腿的业务。
            4. **破局策略**：基于数据给出3条极其干货的实操改进建议（针对营销或供应链）。
            """
            
            try:
                response = client.chat.completions.create(
                    model="qwen-plus",
                    messages=[
                        {"role": "system", "content": "你是一个极其犀利、用数据说话的电商数据分析专家。"},
                        {"role": "user", "content": prompt}
                    ]
                )
                st.success("✅ 诊断完成！")
                st.markdown(response.choices[0].message.content)
            except Exception as e:
                st.error(f"调用失败，错误详情：{e}")
