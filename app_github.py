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
# 1. 页面与全局样式配置 (炫酷背景与UI)
# ==========================================
st.set_page_config(page_title="全域电商数据可视化指挥舱", page_icon="🌐", layout="wide")

# 注入自定义 CSS，让页面颜色丰富、卡片化、高级感拉满
st.markdown("""
<style>
    /* 全局背景色微调 */
    .stApp {background-color: #f4f7f6;}
    /* 隐藏顶部默认空白 */
    .block-container {padding-top: 2rem;}
    /* 自定义指标卡片样式 */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #ffffff 0%, #f0f4f8 100%);
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border-left: 5px solid #00C698;
    }
    /* 标题样式渐变 */
    h1 {background: -webkit-linear-gradient(45deg, #1e3c72, #2a5298); -webkit-background-clip: text; -webkit-text-fill-color: transparent;}
</style>
""", unsafe_allow_html=True)

st.title("🌐 全域电商可视化数据指挥舱 (大厂级)")
st.markdown("覆盖**流量、转化、交易、用户、商品、营销、履约**七大维度，支持一键生成 AI 业务洞察。")

# ==========================================
# 2. 面试专属：一键生成大厂 Demo 数据
# ==========================================
# 预设城市经纬度用于画地图
CITY_COORDS = {
    '北京': [39.9042, 116.4074], '上海': [31.2304, 121.4737], '广州': [23.1291, 113.2644],
    '深圳': [22.5431, 114.0579], '成都': [30.5728, 104.0668], '杭州': [30.2741, 120.1551],
    '重庆': [29.5332, 106.5050], '武汉': [30.5928, 114.3055], '西安': [34.3416, 108.9398]
}

@st.cache_data
def load_mock_data(platform_name):
    """根据选择的平台，生成模拟的、符合表头的海量真实感数据"""
    np.random.seed(len(platform_name)) # 让每个平台数据不同
    size = np.random.randint(1500, 3000)
    
    dates = pd.date_range(end=datetime.date.today(), periods=30, freq='D')
    categories = ['服饰内衣', '美妆护肤', '3C数码', '食品生鲜', '家居日用']
    cities = list(CITY_COORDS.keys()) + ['其他城市'] * 5
    
    data = {
        '用户ID': [f"U{np.random.randint(10000, 99999)}" for _ in range(size)],
        '用户姓名': [f"测试用户{i}" for i in range(size)],
        '商品ID': [f"P{np.random.randint(100, 500)}" for _ in range(size)],
        '商品名称': [f"爆款商品{np.random.randint(1,50)}" for _ in range(size)],
        '商品类别': np.random.choice(categories, size, p=[0.3, 0.2, 0.15, 0.2, 0.15]),
        '单价': np.random.uniform(20, 1500, size).round(2),
        # 生成随机的购买时间（包含具体小时，用于画热力图）
        '购买时间': [np.random.choice(dates).strftime('%Y-%m-%d ') + f"{np.random.randint(0,24):02d}:{np.random.randint(0,60):02d}" for _ in range(size)],
        '购买数量': np.random.choice([1, 2, 3, 4, 5], size, p=[0.6, 0.2, 0.1, 0.05, 0.05]),
        '用户城市': np.random.choice(cities, size),
        '用户性别': np.random.choice(['男', '女'], size, p=[0.4, 0.6]),
        '用户年龄': np.random.normal(28, 6, size).clip(18, 65).astype(int)
    }
    df = pd.DataFrame(data)
    df['消费金额'] = df['单价'] * df['购买数量']
    df['购买时间'] = pd.to_datetime(df['购买时间'])
    df['日期'] = df['购买时间'].dt.date
    df['平台'] = platform_name
    return df

# 侧边栏：操作区
with st.sidebar:
    st.header("⚙️ 数据控制台")
    st.markdown("**【面试官专属体验区】**")
    
    platforms = ["淘宝", "天猫", "京东", "拼多多", "1688", "苏宁"]
    selected_platform = st.selectbox("👉 选择模拟电商平台：", ["请选择..."] + platforms)
    
    st.markdown("---")
    st.markdown("**或者上传本地 CSV 数据：**")
    uploaded_files = st.file_uploader("支持批量上传", type=["csv"], accept_multiple_files=True)

# 加载数据逻辑
df = None
if selected_platform != "请选择...":
    df = load_mock_data(selected_platform)
    st.success(f"✅ 已成功一键接入【{selected_platform}】亿级数据仓库（当前抽样 {len(df)} 条）。")
elif uploaded_files:
    df_list = []
    for file in uploaded_files:
        temp_df = pd.read_csv(file, encoding='utf-8' if 'utf' in file.name else 'gbk')
        df_list.append(temp_df)
    df = pd.concat(df_list, ignore_index=True)
    df['购买时间'] = pd.to_datetime(df['购买时间'])
    df['日期'] = df['购买时间'].dt.date
    st.success(f"✅ 本地数据清洗完毕！共 {len(df)} 条。")

# ==========================================
# 3. 核心可视化大屏 (分 Tab 标签页展示)
# ==========================================
if df is not None:
    # 模拟推演：基于订单量推演流量与营销数据 (展示数据处理思维)
    total_orders = len(df)
    total_gmv = df['消费金额'].sum()
    mock_pv = total_orders * 125  # 模拟浏览量
    mock_uv = total_orders * 85   # 模拟访客数
    mock_cart = total_orders * 12 # 模拟加购数
    mock_pay = int(total_orders * 0.92) # 模拟支付订单
    
    # 顶部全局 KPI
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("💰 整体 GMV (元)", f"¥ {total_gmv:,.0f}", "+12.5%")
    c2.metric("📦 有效支付订单", f"{mock_pay:,}", "-2.1%")
    c3.metric("💳 笔单价 (元)", f"¥ {(total_gmv/total_orders):,.1f}", "+5.4%")
    c4.metric("👁️ 平台访客数 (UV)", f"{mock_uv:,}", "+18.2%")
    c5.metric("🎯 整体转化率", f"{(mock_pay/mock_uv)*100:.2f}%", "+0.3%")
    
    st.write("---")
    
    # 分设 5 个模块标签页
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 交易与转化链路", "👥 用户画像与地域", "🛍️ 商品与履约分析", "📢 流量与营销引擎", "🧠 AI 总监级商业洞察"
    ])

    # ----------- TAB 1: 交易与转化 -----------
    with tab1:
        st.subheader("1. 交易趋势与转化漏斗")
        col1, col2 = st.columns([6, 4])
        with col1:
            daily_gmv = df.groupby('日期')['消费金额'].sum().reset_index()
            fig1 = px.area(daily_gmv, x='日期', y='消费金额', title="📈 近30天销售额 GMV 趋势 (渐变面积图)",
                           color_discrete_sequence=['#3498db'])
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            # 漏斗图
            funnel_data = dict(
                阶段=['浏览 (PV)', '访客 (UV)', '加购 (Cart)', '下单 (Order)', '支付 (Pay)'],
                数值=[mock_pv, mock_uv, mock_cart, total_orders, mock_pay]
            )
            fig2 = px.funnel(funnel_data, x='数值', y='阶段', title="🔽 核心流量转化漏斗图",
                             color_discrete_sequence=px.colors.sequential.Teal)
            st.plotly_chart(fig2, use_container_width=True)

    # ----------- TAB 2: 用户画像与地域 -----------
    with tab2:
        st.subheader("2. 用户多维切片分析")
        col1, col2 = st.columns([4, 6])
        with col1:
            # 年龄性别直方图
            fig3 = px.histogram(df, x='用户年龄', color='用户性别', nbins=15,
                                title="🧑‍🤝‍🧑 用户年龄与性别画像分布",
                                color_discrete_map={'男':'#2c3e50', '女':'#e74c3c'})
            st.plotly_chart(fig3, use_container_width=True)
        with col2:
            # 地域气泡地图 / 树状图
            city_gmv = df.groupby('用户城市')['消费金额'].sum().reset_index()
            # 过滤出有经纬度的城市画地图，其他画树状图
            map_data = []
            for _, row in city_gmv.iterrows():
                if row['用户城市'] in CITY_COORDS:
                    map_data.append({'城市': row['用户城市'], 'GMV': row['消费金额'], 
                                     'lat': CITY_COORDS[row['用户城市']][0], 'lon': CITY_COORDS[row['用户城市']][1]})
            
            if map_data:
                map_df = pd.DataFrame(map_data)
                fig4 = px.scatter_mapbox(map_df, lat="lat", lon="lon", size="GMV", color="GMV",
                                         hover_name="城市", size_max=40, zoom=3, 
                                         mapbox_style="carto-positron", title="🗺️ 消费力核心地域分布 (散点地图)",
                                         color_continuous_scale=px.colors.sequential.Plasma)
                st.plotly_chart(fig4, use_container_width=True)
            else:
                fig4 = px.treemap(city_gmv, path=['用户城市'], values='消费金额', title="🗺️ 地域消费力结构热力图")
                st.plotly_chart(fig4, use_container_width=True)

    # ----------- TAB 3: 商品与履约 -----------
    with tab3:
        st.subheader("3. 货品动销与供应链模拟")
        col1, col2, col3 = st.columns([3, 4, 3])
        with col1:
            cat_gmv = df.groupby('商品类别')['消费金额'].sum().reset_index()
            fig5 = px.pie(cat_gmv, names='商品类别', values='消费金额', hole=0.5, title="🍩 品类营收贡献度")
            st.plotly_chart(fig5, use_container_width=True)
        with col2:
            # 购买时间热力图
            df['小时'] = df['购买时间'].dt.hour
            df['星期'] = df['购买时间'].dt.day_name()
            heatmap_data = df.groupby(['星期', '小时']).size().reset_index(name='订单量')
            fig6 = px.density_heatmap(heatmap_data, x='小时', y='星期', z='订单量', 
                                      title="🔥 用户下单时间热力图 (寻最优转化点)",
                                      color_continuous_scale="Viridis")
            st.plotly_chart(fig6, use_container_width=True)
        with col3:
            st.markdown("#### 📦 供应链预警 (基于单量推算)")
            st.progress(0.85, text="当前整体库存动销率：85% (健康)")
            st.progress(0.12, text="爆款单品缺货率预警：12% (需补货)")
            st.progress(0.96, text="48小时发货履约率：96%")
            st.info("💡 提示：服装品类退货率已达 18%，建议优化详情页尺码说明。")

    # ----------- TAB 4: 流量与营销 -----------
    with tab4:
        st.subheader("4. 营销投放与 ROI (大盘推演)")
        mc1, mc2 = st.columns(2)
        with mc1:
            # 模拟流量来源饼图
            traffic_sources = pd.DataFrame({
                '来源': ['站内搜索', '个性化推荐', '直播带货', '外部广告CPC', '私域/社群'],
                '占比': [35, 25, 20, 15, 5]
            })
            fig7 = px.pie(traffic_sources, names='来源', values='占比', title="🌐 核心流量来源渠道结构")
            st.plotly_chart(fig7, use_container_width=True)
        with mc2:
            st.markdown("#### 📢 各渠道投放 ROI 监控")
            st.metric("站内直通车/搜索 ROI", "1 : 4.2", "表现优秀")
            st.metric("短视频/直播带货 ROI", "1 : 2.8", "流失严重", delta_color="inverse")
            st.metric("外部信息流广告 CPC", "¥ 1.2 / 点击", "成本上升")

    # ----------- TAB 5: AI 洞察报告 -----------
    with tab5:
        st.subheader("🧠 接入大模型：生成专属商业研判")
        api_key = os.environ.get("OPENAI_API_KEY", "sk-cdc57fd44a394cea8ec25dd4ad2512f7") 
        client = OpenAI(api_key=api_key, base_url="https://ws-vvr85dv3ndbxfxtu.ap-southeast-1.maas.aliyuncs.com/compatible-model/v1")
        
        if st.button("🚀 一键生成总监级数据洞察报告", type="primary"):
            with st.spinner("AI 正在扫描七大维度数据，撰写业务诊断书..."):
                top_cat = df.groupby('商品类别')['消费金额'].sum().idxmax()
                top_city = df.groupby('用户城市')['消费金额'].sum().idxmax()
                
                prompt = f"""
                你是一个顶级的电商总监。基于当前电商数据大盘：
                总GMV {total_gmv:.2f}元，转化率 {(mock_pay/mock_uv)*100:.2f}%。
                第一大品类是 {top_cat}，核心消费城市是 {top_city}。
                请严格用以下结构（Markdown排版）输出报告：
                1. 📈 **流量与转化诊断**（分析转化瓶颈）
                2. 🛍️ **货品与履约建议**（针对核心品类的供应链建议）
                3. 🎯 **用户与营销策略**（根据人群与城市给后续投放建议）
                """
                try:
                    response = client.chat.completions.create(
                        model="qwen-plus",
                        messages=[{"role": "system", "content": "你是一个资深业务专家，语言极其犀利干练。"},
                                  {"role": "user", "content": prompt}]
                    )
                    st.success("✅ 诊断报告生成完毕！")
                    st.markdown(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"调用 AI 失败，错误：{e}")
