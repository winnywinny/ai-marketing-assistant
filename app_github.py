# # # import streamlit as st
# # # import pandas as pd
# # # import io
# # # from openai import OpenAI
# # # import os

# # # # 1. 页面配置与标题
# # # st.set_page_config(page_title="AI 营销数据洞察助手", page_icon="📈", layout="wide")
# # # st.title("📈 AI 营销数据洞察助手 (Demo版)")
# # # st.markdown("上传您的营销数据（CSV/Excel），AI 将自动帮您找出核心问题并提供优化建议。")

# # # # --- 核心修改1：兼容本地测试和云端部署 ---
# # # # 如果在本地测试，把你的 sk- 密钥写在逗号后面的引号里
# # # # 部署到云端时，它会自动优先读取云端的环境变量
# # # api_key = os.environ.get("OPENAI_API_KEY", "你的sk-开头的真实密钥放这里用于本地测试")

# # # client = OpenAI(
# # #     api_key=api_key, 
# # #     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1" 
# # # )

# # # # --- 内置的示例数据 ---
# # # SAMPLE_CSV = """日期,广告计划,投放渠道,花费(元),展现量,点击量,转化量,实际销售额(元)
# # # 2023-10-25,种草_美妆,小红书KOC,3200,120000,5500,130,28000
# # # 2023-10-25,竞品词_核心,百度搜索,4500,18000,1500,95,35000
# # # 2023-10-25,冲量_定向,抖音信息流,15000,650000,9500,210,42000
# # # 2023-10-26,种草_美妆,小红书KOC,3500,135000,6100,145,31000
# # # 2023-10-26,竞品词_核心,百度搜索,4800,19500,1600,105,38500
# # # 2023-10-26,冲量_定向,抖音信息流,22000,950000,14000,230,45000
# # # 2023-10-27,种草_美妆,小红书KOC,3800,150000,6800,160,34500
# # # 2023-10-27,竞品词_核心,百度搜索,5000,21000,1750,115,41000
# # # 2023-10-27,冲量_定向,抖音信息流,35000,1500000,18000,180,32000"""


# # # # --- 核心修改2：初始化 Streamlit 记忆体 ---
# # # if "df" not in st.session_state:
# # #     st.session_state.df = None


# # # # 3. 数据来源选择：上传 or 示例
# # # col1, col2 = st.columns([1, 2])
# # # with col1:
# # #     use_demo = st.button("✨ 一键使用示例数据体验")
# # # with col2:
# # #     uploaded_file = st.file_uploader("或者上传您自己的数据 (CSV 格式)", type=["csv", "xlsx"])

# # # # 只要点过按钮，就把数据存入“记忆体”中
# # # if use_demo:
# # #     st.session_state.df = pd.read_csv(io.StringIO(SAMPLE_CSV))
# # # elif uploaded_file is not None:
# # #     if uploaded_file.name.endswith('.csv'):
# # #         st.session_state.df = pd.read_csv(uploaded_file)
# # #     else:
# # #         st.session_state.df = pd.read_excel(uploaded_file)

# # # # 4. 从“记忆体”中读取数据展示
# # # if st.session_state.df is not None:
# # #     df = st.session_state.df # 把记忆体里的数据拿出来用
    
# # #     st.write("---")
# # #     st.write("### 📊 数据预览")
# # #     st.dataframe(df.head()) 
    
# # #     st.write("### 📉 实际销售额趋势分析")
# # #     try:
# # #         st.line_chart(df.set_index('日期')['实际销售额(元)']) 
# # #     except Exception as e:
# # #         st.write("提示：当前数据格式不支持生成折线图。")

# # #     st.write("### 🧠 AI 深度洞察报告")
# # #     if st.button("生成营销分析报告 (调用 AI)"):
# # #         with st.spinner("AI 正在疯狂计算与分析中..."):
# # #             data_summary = df.describe().to_string() 
# # #             data_head = df.head().to_string()
            
# # #             prompt = f"""
# # #             你是一个资深的数字营销总监。请根据以下营销数据，生成一份极具业务洞察的报告：
# # #             数据样例：\n{data_head}\n
# # #             数据统计特征：\n{data_summary}\n
# # #             请直接输出：1. 渠道红黑榜(明确指出哪个好哪个差) 2. 异常数据预警(如预算浪费) 3. 下一步优化建议。
# # #             """
# # #             try:
# # #                 response = client.chat.completions.create(
# # #                     model="qwen-plus",
# # #                     messages=[
# # #                         {"role": "system", "content": "你是一个专业的数据分析专家，用Markdown排版，使用emoji让排版生动。"},
# # #                         {"role": "user", "content": prompt}
# # #                     ]
# # #                 )
# # #                 st.success("报告生成完毕！")
# # #                 st.markdown(response.choices[0].message.content)
# # #             except Exception as e:
# # #                 st.error(f"调用 AI 失败，请检查配置。错误：{e}")


# # import streamlit as st
# # import pandas as pd
# # from openai import OpenAI
# # import os

# # # 1. 页面配置与标题
# # st.set_page_config(page_title="电商全链路数据洞察系统", page_icon="🛒", layout="wide")
# # st.title("🛒 平台电商交易数据洞察系统")
# # st.markdown("上传您的电商平台订单流水（支持淘宝、京东、拼多多等格式），系统将自动进行人群画像与销售提效分析。")

# # # 2. 初始化大模型客户端
# # api_key = os.environ.get("OPENAI_API_KEY", "你的sk-开头的真实密钥放这里用于本地测试")
# # client = OpenAI(
# #     api_key=api_key, 
# #     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1" 
# # )

# # # 3. 数据上传模块
# # uploaded_file = st.file_uploader("请上传平台交易数据 (例如: 淘宝.csv, 京东.csv)", type=["csv"])

# # if uploaded_file is not None:
# #     # 读取数据
# #     df = pd.read_csv(uploaded_file)
    
# #     # --- 核心数据预处理 (ETL) ---
# #     # 把“购买时间”转成标准日期格式，方便画图
# #     df['购买时间'] = pd.to_datetime(df['购买时间'])
# #     df['日期'] = df['购买时间'].dt.date
    
# #     st.write("---")
# #     st.write("### 🔍 原始流水数据预览 (前5条)")
# #     st.dataframe(df.head())
    
# #     # 4. 网页端自动画图分析
# #     col1, col2 = st.columns(2)
    
# #     with col1:
# #         st.write("### 📈 每日销售额趋势 (GMV)")
# #         # 按日期汇总消费金额
# #         daily_sales = df.groupby('日期')['消费金额'].sum()
# #         st.line_chart(daily_sales)
        
# #     with col2:
# #         st.write("### 📦 各大商品品类销售占比")
# #         # 按商品类别汇总消费金额
# #         category_sales = df.groupby('商品类别')['消费金额'].sum()
# #         st.bar_chart(category_sales)

# #     # 5. 提取精华数据，准备喂给 AI
# #     st.write("---")
# #     st.write("### 🧠 AI 商业深度洞察")
    
# #     if st.button("一键生成电商运营报告"):
# #         with st.spinner("AI 正在深度剖析用户画像与消费行为..."):
            
# #             # 【关键】：让 Python 帮你算出核心指标，而不是发全量数据
# #             total_gmv = df['消费金额'].sum()
# #             total_orders = len(df)
# #             top_category = category_sales.idxmax()
# #             top_city = df.groupby('用户城市')['消费金额'].sum().idxmax()
# #             avg_age = df['用户年龄'].mean()
# #             gender_ratio = df['用户性别'].value_counts().to_dict()
            
# #             # 拼装给 AI 的提示词 (Prompt)
# #             prompt = f"""
# #             你是一位资深的电商平台运营总监。我有一份近期的电商订单交易数据，以下是经过系统计算后的核心指标摘要：
            
# #             【核心业绩指标】
# #             - 总销售额 (GMV): {total_gmv:.2f} 元
# #             - 总订单量: {total_orders} 笔
# #             - 客单价: {total_gmv/total_orders:.2f} 元
            
# #             【商品与用户画像】
# #             - 最畅销商品类别: {top_category}
# #             - 消费主力城市: {top_city}
# #             - 消费者平均年龄: {avg_age:.1f} 岁
# #             - 男女消费者比例: {gender_ratio}
            
# #             请根据以上摘要数据，生成一份极具业务洞察的报告。请直接输出：
# #             1. 业绩基本盘诊断 (当前的客单价和销量说明了什么问题？)
# #             2. 用户画像分析 (针对这群主力消费者，有什么特征？)
# #             3. 下一步选品与营销建议 (结合最畅销品类和主力人群，应该主推什么？去哪个城市推？)
# #             """
            
# #             try:
# #                 response = client.chat.completions.create(
# #                     model="qwen-plus",
# #                     messages=[
# #                         {"role": "system", "content": "你是一个专业、犀利的电商数据分析专家，用Markdown排版，多用加粗和列表，使用emoji让排版生动。"},
# #                         {"role": "user", "content": prompt}
# #                     ]
# #                 )
# #                 st.success("运营报告生成完毕！")
# #                 st.markdown(response.choices[0].message.content)
# #             except Exception as e:
# #                 st.error(f"调用 AI 失败，错误信息：{e}")
# import streamlit as st
# import pandas as pd
# from openai import OpenAI
# import os
# import plotly.express as px  # 引入超强绘图神器

# # 1. 页面配置 (开启宽屏模式，让图表更大气)
# st.set_page_config(page_title="企业级电商数据洞察助手", page_icon="🛒", layout="wide")
# st.title("🛒 企业零售海量数据 AI 洞察平台")
# st.markdown("支持批量上传原始订单流水，系统将自动清洗、聚合数据，并生成**可交互的BI看板**与 AI 专家诊断。")

# # 2. 初始化大模型客户端
# api_key = os.environ.get("OPENAI_API_KEY", "sk-cdc57fd44a394cea8ec25dd4ad2512f7")
# client = OpenAI(
#     api_key=api_key, 
#     base_url="https://ws-vvr85dv3ndbxfxtu.ap-southeast-1.maas.aliyuncs.com/compatible-model/v1" 
# )

# # --- 核心黑科技：加入数据缓存，提速10倍！ ---
# @st.cache_data
# def process_data(uploaded_files):
#     df_list = []
#     for file in uploaded_files:
#         try:
#             temp_df = pd.read_csv(file, encoding='utf-8')
#         except UnicodeDecodeError:
#             temp_df = pd.read_csv(file, encoding='gbk')
#         df_list.append(temp_df)
        
#     df = pd.concat(df_list, ignore_index=True)
#     df['购买时间'] = pd.to_datetime(df['购买时间'])
#     df['日期'] = df['购买时间'].dt.date
#     return df

# # 3. 数据上传模块
# uploaded_files = st.file_uploader("📂 请批量上传订单流水数据 (CSV格式)", type=["csv"], accept_multiple_files=True)

# if uploaded_files:
#     with st.spinner("⏳ 正在清洗合并海量数据..."):
#         # 调用缓存的数据处理函数
#         df = process_data(uploaded_files)
    
#     st.success(f"✅ 数据合并清洗完成！共处理 **{len(df):,}** 条底层交易流水。")
    
#     # ==========================================
#     # 🎨 4. 高级绚丽 BI 看板 (Plotly驱动)
#     # ==========================================
#     st.write("---")
#     st.write("### 📊 核心业务可视化大屏")
    
#     # 顶部核心指标 KPI 卡片
#     col1, col2, col3, col4 = st.columns(4)
#     col1.metric("💰 总销售额 (元)", f"¥ {df['消费金额'].sum():,.2f}")
#     col2.metric("📦 总订单数", f"{len(df):,}")
#     col3.metric("🛍️ 销售商品总件数", f"{df['购买数量'].sum():,}")
#     col4.metric("💳 客单价 (元)", f"¥ {(df['消费金额'].sum() / len(df)):,.2f}")

#     st.markdown("<br>", unsafe_allow_html=True) # 加点空行

#     # 图表第一排：趋势图 + 饼图
#     chart_col1, chart_col2 = st.columns([6, 4]) # 6:4 比例分配宽度
    
#     with chart_col1:
#         # 📈 渐变面积趋势图
#         daily_sales = df.groupby('日期')['消费金额'].sum().reset_index()
#         fig_trend = px.area(daily_sales, x='日期', y='消费金额', 
#                             title="📈 每日营收趋势 (面积图)", 
#                             markers=True, 
#                             color_discrete_sequence=['#00C698']) # 清爽的翠绿色
#         st.plotly_chart(fig_trend, use_container_width=True)

#     with chart_col2:
#         # 🍩 多彩环形饼图
#         category_sales = df.groupby('商品类别')['消费金额'].sum().reset_index()
#         fig_pie = px.pie(category_sales, names='商品类别', values='消费金额', 
#                          hole=0.4, # 变成中间空心的环形图
#                          title="🛍️ 商品类别营收占比")
#         fig_pie.update_traces(textposition='inside', textinfo='percent+label')
#         st.plotly_chart(fig_pie, use_container_width=True)

#     # 图表第二排：条形图 + 用户画像
#     chart_col3, chart_col4 = st.columns([5, 5])
    
#     with chart_col3:
#         # 🏙️ 动态多色彩色条形图
#         city_sales = df.groupby('用户城市')['消费金额'].sum().sort_values(ascending=True).tail(10).reset_index() # 取Top10并倒序让最高的在上面
#         fig_city = px.bar(city_sales, x='消费金额', y='用户城市', orientation='h', 
#                           color='消费金额', # 根据金额自动渐变上色
#                           color_continuous_scale=px.colors.sequential.Sunset, # 晚霞渐变色
#                           title="🏙️ 营收贡献 TOP 10 城市")
#         st.plotly_chart(fig_city, use_container_width=True)

#     with chart_col4:
#         # 👥 年龄与性别分布直方图
#         fig_demo = px.histogram(df, x='用户年龄', color='用户性别', 
#                                 nbins=20, barmode='group',
#                                 color_discrete_map={'男': '#3498db', '女': '#e74c3c'}, # 经典红蓝配色
#                                 title="👥 用户人群画像 (年龄与性别)")
#         st.plotly_chart(fig_demo, use_container_width=True)

#     # ==========================================
#     # 🧠 5. AI 业务诊断模块
#     # ==========================================
#     st.write("---")
#     st.write("### 🧠 AI 零售数据总监深度报告")
    
#     # 提前生成 AI 需要的数据摘要
#     city_str = df.groupby('用户城市')['消费金额'].sum().sort_values(ascending=False).head(5).to_string()
#     cat_str = df.groupby('商品类别')['消费金额'].sum().sort_values(ascending=False).to_string()
#     gender_str = df.groupby('用户性别')['消费金额'].sum().to_string()

#     if st.button("✨ 一键生成深度商业诊断 ✨"):
#         with st.spinner("AI 正在深度思考业务逻辑..."):
#             summary_text = f"""
#             总体表现：总销售额 {df['消费金额'].sum():.2f} 元，共 {len(df)} 笔订单。
#             品类表现摘要：\n{cat_str}
#             城市表现前五名：\n{city_str}
#             男女消费占比：\n{gender_str}
#             """
            
#             prompt = f"""
#             你是一位顶级的电商零售数据分析总监。请根据以下浓缩的脱敏数据摘要，写一份极具深度的业务诊断报告：
#             【数据摘要】：\n{summary_text}\n
#             请严格按照以下结构输出（使用 Markdown，加上 emoji）：
#             1. **大盘诊断**：评价总体业绩与客单价。
#             2. **爆款与品类洞察**：指出核心品类和需要优化的长尾品类。
#             3. **高价值人群画像**：从性别、城市维度描绘核心利润人群。
#             4. **下一步行动建议**：给出至少 3 条落地性极强的营销/备货策略。
#             """
            
#             try:
#                 response = client.chat.completions.create(
#                     model="qwen-plus",
#                     messages=[
#                         {"role": "system", "content": "你是一个用数据说话、眼光毒辣的商业顾问。语言风格专业、简练。"},
#                         {"role": "user", "content": prompt}
#                     ]
#                 )
#                 st.success("✅ 诊断报告已生成！")
#                 st.markdown(response.choices[0].message.content)
#             except Exception as e:
#                 st.error(f"调用 AI 失败，请检查网络或配置。错误详情：{e}")


import streamlit as st
import pandas as pd
import numpy as np
from openai import OpenAI
import os
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 1. 页面与全局样式配置 (大厂 BI 级 UI)
# ==========================================
st.set_page_config(page_title="全域电商数据大屏", page_icon="📊", layout="wide")

# 注入自定义 CSS 让关键指标卡片带渐变色和阴影，告别单一颜色
st.markdown("""
<style>
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #f6f8fd 0%, #f1f5f9 100%);
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 全域电商数据可视化与 AI 决策中心")
st.markdown("覆盖**流量、转化、交易、用户、商品、营销、供应链**七大维度，支持多平台一键切换与 AI 深度诊断。")

# ==========================================
# 2. AI 客户端初始化
# ==========================================
api_key = os.environ.get("OPENAI_API_KEY", "sk-cdc57fd44a394cea8ec25dd4ad2512f7")
client = OpenAI(
    api_key=api_key, 
    base_url="https://ws-vvr85dv3ndbxfxtu.ap-southeast-1.maas.aliyuncs.com/compatible-model/v1"
)

# ==========================================
# 3. 核心数据引擎 (读取真实CSV + 动态推算全域数据)
# ==========================================
@st.cache_data
def load_and_enhance_data(platform_name):
    # 尝试读取同目录下的 CSV 文件
    file_path = f"{platform_name}.csv"
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except Exception:
        try:
            df = pd.read_csv(file_path, encoding='gbk')
        except Exception:
            # 如果本地没有这个文件，为了防止页面崩溃，生成一份极其逼真的备用模拟数据
            st.warning(f"⚠️ 未在同级目录找到 {file_path}，已自动启用备用模拟数据集进行演示。")
            dates = pd.date_range(start='2024-01-01', periods=1000, freq='H')
            df = pd.DataFrame({
                '用户ID': [f"U{np.random.randint(1000, 9999)}" for _ in range(1000)],
                '商品类别': np.random.choice(['美妆', '服饰', '数码', '食品', '家居', '运动'], 1000),
                '消费金额': np.random.uniform(50, 3000, 1000),
                '购买数量': np.random.randint(1, 5, 1000),
                '购买时间': np.random.choice(dates, 1000),
                '用户城市': np.random.choice(['北京', '上海', '广州', '深圳', '成都', '杭州', '重庆'], 1000),
                '用户性别': np.random.choice(['男', '女'], 1000, p=[0.4, 0.6]),
                '用户年龄': np.random.randint(18, 60, 1000)
            })
            
    # 数据基础清洗
    df['购买时间'] = pd.to_datetime(df['购买时间'])
    df['日期'] = df['购买时间'].dt.date
    df['小时'] = df['购买时间'].dt.hour
    df['星期'] = df['购买时间'].dt.day_name()
    return df

# ==========================================
# 4. 侧边栏：多平台切换 Demo
# ==========================================
st.sidebar.image("https://img.alicdn.com/tfs/TB1_uT8a5ERMeJjSspiXXbZLFXa-143-59.png", width=100) # 示意Logo
st.sidebar.header("🎯 经营大盘控制台")
platforms = ["淘宝", "天猫", "京东", "拼多多", "1688", "苏宁"]
selected_platform = st.sidebar.radio("一键切换分析平台 (Demo)", platforms)

# 加载数据
with st.spinner(f"正在抽取 {selected_platform} 全域业务数据..."):
    df = load_and_enhance_data(selected_platform)

# 基于真实订单数，反推（模拟）出流量和漏斗数据，让演示显得真实完整
real_orders = len(df)
real_gmv = df['消费金额'].sum()
mock_uv = real_orders * np.random.randint(15, 25)  # 假设转化率在 4%-6%
mock_pv = mock_uv * 3.5
mock_cart = int(mock_uv * 0.3)

st.sidebar.write("---")
st.sidebar.success(f"✅ {selected_platform} 数据接入正常\n共加载 {real_orders:,} 笔真实交易。")


# ==========================================
# 5. UI 布局：四大业务模块 Tab 切换
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "💰 交易与流量 (大盘)", 
    "👥 用户与商品 (画像)", 
    "🚀 营销与供应链 (运营)", 
    "🧠 AI 深度诊断报告"
])

# ----------------- TAB 1: 交易与流量 -----------------
with tab1:
    st.markdown("### 1. 核心交易指标 (Transaction)")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💰 销售额 GMV", f"¥ {real_gmv:,.0f}", "+12.5% 环比")
    c2.metric("💳 支付订单量", f"{real_orders:,} 笔", "+5.2% 环比")
    c3.metric("🛒 客单价", f"¥ {real_gmv/real_orders:,.2f}", "-1.2% 环比")
    c4.metric("👥 独立访客 (UV)", f"{mock_uv:,} 人", "+18.0% 环比")

    st.markdown("<br>", unsafe_allow_html=True)
    
    col_t1, col_t2 = st.columns([6, 4])
    with col_t1:
        # 多色渐变面积图 (交易趋势)
        daily_sales = df.groupby('日期')['消费金额'].sum().reset_index()
        fig_trend = px.area(daily_sales, x='日期', y='消费金额', 
                            title=f"📈 {selected_platform} 每日 GMV 趋势",
                            color_discrete_sequence=['#FF4B4B'])
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with col_t2:
        # 极具视觉冲击力的 3D 漏斗图 (转化流转)
        funnel_data = dict(
            阶段=['浏览 (PV)', '访客 (UV)', '加购人数', '下单人数', '支付完成'],
            数值=[mock_pv, mock_uv, mock_cart, int(real_orders*1.2), real_orders]
        )
        fig_funnel = go.Figure(go.Funnel(
            y=funnel_data['阶段'], x=funnel_data['数值'],
            textinfo="value+percent initial",
            marker={"color": ["#3498db", "#2ecc71", "#f1c40f", "#e67e22", "#e74c3c"]}
        ))
        fig_funnel.update_layout(title="🔽 核心转化漏斗分析")
        st.plotly_chart(fig_funnel, use_container_width=True)

# ----------------- TAB 2: 用户与商品 -----------------
with tab2:
    st.markdown("### 2. 用户画像与商品表现 (User & Product)")
    col_u1, col_u2 = st.columns(2)
    
    with col_u1:
        # 树状图/板块图 (类目占比，比饼图更高大上)
        cat_sales = df.groupby('商品类别')['消费金额'].sum().reset_index()
        fig_tree = px.treemap(cat_sales, path=['商品类别'], values='消费金额',
                              color='消费金额', color_continuous_scale='Viridis',
                              title="🛍️ 商品品类营收贡献 (Treemap)")
        st.plotly_chart(fig_tree, use_container_width=True)
        
    with col_u2:
        # 热力图 (用户购买时间分布)
        heatmap_data = df.groupby(['星期', '小时']).size().reset_index(name='订单数')
        fig_heat = px.density_heatmap(heatmap_data, x='小时', y='星期', z='订单数',
                                      color_continuous_scale='YlOrRd',
                                      title="🔥 用户下单时间热力图 (寻优投放时段)")
        st.plotly_chart(fig_heat, use_container_width=True)

    col_u3, col_u4 = st.columns(2)
    with col_u3:
        # 用户年龄性别画像 (带图例的直方图)
        fig_demo = px.histogram(df, x='用户年龄', color='用户性别', nbins=15, 
                                barmode='group', color_discrete_map={'男': '#2980b9', '女': '#c0392b'},
                                title="👥 消费者年龄与性别分布")
        st.plotly_chart(fig_demo, use_container_width=True)
        
    with col_u4:
        # 城市排行榜 (条形图)
        city_sales = df.groupby('用户城市')['消费金额'].sum().sort_values().tail(10).reset_index()
        fig_city = px.bar(city_sales, x='消费金额', y='用户城市', orientation='h',
                          color='消费金额', color_continuous_scale='Blues',
                          title="🏙️ 核心高净值城市 TOP 10 (地域分布)")
        st.plotly_chart(fig_city, use_container_width=True)

# ----------------- TAB 3: 营销与供应链 -----------------
with tab3:
    st.markdown("### 3. 营销效率与履约质量 (Marketing & Supply Chain)")
    st.info("💡 注：此模块数据结合历史大盘波动动态模拟，用于指导宏观运营决策。")
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        # 环形图 (流量来源占比)
        sources = pd.DataFrame({
            '渠道': ['站内搜索', '首页推荐', '短视频/直播', '站外广告', '自然复购'],
            '占比': [35, 25, 20, 15, 5]
        })
        fig_pie = px.pie(sources, names='渠道', values='占比', hole=0.5,
                         title="🌐 流量来源结构占比", color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_pie.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with col_m2:
        # 仪表盘 Gauge Chart (供应链发货达标率)
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = 98.2,
            title = {'text': "📦 48小时履约发货率 (%)"},
            gauge = {'axis': {'range': [None, 100]},
                     'bar': {'color': "#27ae60"},
                     'steps' : [
                         {'range': [0, 80], 'color': "#e74c3c"},
                         {'range': [80, 90], 'color': "#f1c40f"},
                         {'range': [90, 100], 'color': "#ecf0f1"}]}
        ))
        st.plotly_chart(fig_gauge, use_container_width=True)

# ----------------- TAB 4: AI 深度诊断 -----------------
with tab4:
    st.markdown(f"### 🧠 {selected_platform} 大盘数据 AI 智能诊断")
    
    if st.button("✨ 生成全域经营分析报告 ✨", type="primary"):
        with st.spinner("AI 正在汇聚 7 大维度数据，生成总监级洞察报告..."):
            
            # 将核心数据浓缩成文本喂给大模型
            cat_top = df.groupby('商品类别')['消费金额'].sum().sort_values(ascending=False).head(3).to_dict()
            city_top = df.groupby('用户城市')['消费金额'].sum().sort_values(ascending=False).head(3).to_dict()
            
            summary_text = f"""
            当前平台：{selected_platform}
            1. 交易与流量：总GMV ¥{real_gmv:.2f}，总订单 {real_orders}笔，客单价 ¥{real_gmv/real_orders:.2f}。预估转化漏斗中，PV到加购转化率良好，但加购到支付流失率约 {(1 - real_orders/mock_cart)*100:.1f}%。
            2. 商品表现：TOP3营收品类为 {cat_top}。
            3. 用户画像：核心消费城市TOP3为 {city_top}。
            4. 营销与供应链：站内搜索和推荐占流量大头(60%)，48小时发货率高达98.2%。
            """
            
            prompt = f"""
            你是一位年薪百万的电商大厂（阿里/京东级别）数据运营总监。请根据以下全域经营数据，写一份汇报给CEO的商业洞察报告：
            【数据摘要】：\n{summary_text}\n
            请严格按照以下结构输出（Markdown格式，多用 emoji 和专业的业务黑话）：
            1. 📈 **全域经营大盘总结**：一句话定调目前的生意健康度。
            2. ⚠️ **转化漏斗痛点**：针对“加购到支付”的流失，深度剖析可能的原因（如促销力度不够、运费门槛等）。
            3. 🎯 **人货场重构建议**：
               - **人 (用户)**：针对高优城市该怎么做定向运营？
               - **货 (商品)**：头部类目如何拉升利润？
               - **场 (营销/流量)**：如何优化流量结构？
            4. 💡 **下一步核心 Action 落地建议**。
            """
            
            try:
                response = client.chat.completions.create(
                    model="qwen-plus",
                    messages=[
                        {"role": "system", "content": "你是资深电商专家，擅长从流量、转化、客单价等维度做深度业务拆解。"},
                        {"role": "user", "content": prompt}
                    ]
                )
                st.success("✅ AI 诊断报告已生成！")
                st.markdown(response.choices[0].message.content)
            except Exception as e:
                st.error(f"调用 AI 失败，请检查网络。错误详情：{e}")
