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
from openai import OpenAI
import os
import io

# ==========================================
# 1. 页面全局配置 (宽屏模式，更像大厂后台)
# ==========================================
st.set_page_config(page_title="电商智能数据洞察中台", page_icon="🛒", layout="wide")

# 初始化 AI 客户端
api_key = os.environ.get("OPENAI_API_KEY", "你的sk-开头的真实密钥放这里用于本地测试")
client = OpenAI(
    api_key=api_key, 
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1" 
)

# ==========================================
# 2. 侧边栏设计 (控制面板)
# ==========================================
with st.sidebar:
    st.title("⚙️ 控制面板")
    st.markdown("请选择您要分析的数据源，或者上传自有数据。")
    
    # 选项卡：让面试官随意切换平台
    data_source = st.radio(
        "📌 选择数据来源",
        ("🛒 淘宝 (模拟案例)", "🐶 京东 (模拟案例)", "💖 拼多多 (模拟案例)", "📁 自定义上传 CSV")
    )
    
    uploaded_file = None
    if data_source == "📁 自定义上传 CSV":
        uploaded_file = st.file_uploader("请拖拽上传您的电商流水", type=["csv"])
        
    st.markdown("---")
    st.caption("✨ Powered by 阿里云通义大模型 & Streamlit")

# ==========================================
# 3. 数据加载与预处理核心逻辑
# ==========================================
df = None

# 根据侧边栏的选择加载对应的数据
try:
    if data_source == "🛒 淘宝 (模拟案例)":
        df = pd.read_csv("淘宝.csv") # 读取你本地文件夹里的同名文件
    elif data_source == "🐶 京东 (模拟案例)":
        df = pd.read_csv("京东.csv")
    elif data_source == "💖 拼多多 (模拟案例)":
        df = pd.read_csv("拼多多.csv")
    elif data_source == "📁 自定义上传 CSV" and uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
except FileNotFoundError:
    st.error(f"⚠️ 找不到文件！请确保 {data_source[3:5]}.csv 和 app.py 在同一个文件夹内。")

# ==========================================
# 4. 主界面展示 (仪表盘与图表)
# ==========================================
st.title("🛒 电商全链路智能洞察中台")

if df is not None:
    # --- 数据清洗 ---
    df['购买时间'] = pd.to_datetime(df['购买时间'])
    df['日期'] = df['购买时间'].dt.date
    
    # --- 顶部核心指标卡片 (大字报) ---
    total_gmv = df['消费金额'].sum()
    total_orders = len(df)
    avg_price = total_gmv / total_orders if total_orders > 0 else 0
    top_city = df.groupby('用户城市')['消费金额'].sum().idxmax()
    
    # 使用 4 列布局展示指标
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 总销售额 (GMV)", f"¥ {total_gmv:,.2f}")
    col2.metric("📦 总订单量", f"{total_orders:,} 笔")
    col3.metric("🎫 平均客单价", f"¥ {avg_price:,.2f}")
    col4.metric("🏙️ 消费最强城市", top_city)
    
    st.markdown("---")
    
    # --- 多标签页设计 (图表、数据、AI洞察 分开展示) ---
    tab1, tab2, tab3 = st.tabs(["📊 数据可视化大屏", "🗂️ 底层流水明细", "🤖 AI 深度诊断报告"])
    
    with tab1:
        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            st.subheader("📈 每日销售额走势")
            daily_sales = df.groupby('日期')['消费金额'].sum()
            st.line_chart(daily_sales)
        with chart_col2:
            st.subheader("📦 各大品类销售排行")
            category_sales = df.groupby('商品类别')['消费金额'].sum().sort_values(ascending=True)
            st.bar_chart(category_sales)
            
    with tab2:
        st.subheader("🗂️ 原始订单流水 (前 100 条)")
        st.dataframe(df.head(100), use_container_width=True)
        
    with tab3:
        st.subheader("🤖 一键生成业务报告")
        st.info("💡 点击下方按钮，AI 将结合左侧选择的平台特性及当前数据，为您生成专属的运营优化方案。")
        
        if st.button("✨ 召唤 AI 总监生成报告", type="primary"): # type="primary" 让按钮变成醒目的红色/蓝色
            with st.spinner("AI 正在深度剖析多维数据中，请稍候..."):
                top_category = category_sales.index[-1]
                avg_age = df['用户年龄'].mean()
                gender_ratio = df['用户性别'].value_counts().to_dict()
                
                prompt = f"""
                你是一位资深的电商平台运营总监。当前分析的平台是：{data_source}。
                以下是近期的真实订单数据摘要：
                - 总GMV: {total_gmv:.2f} 元，总订单量: {total_orders} 笔，客单价: {avg_price:.2f} 元
                - 最畅销品类: {top_category}
                - 消费主力城市: {top_city}
                - 消费者平均年龄: {avg_age:.1f} 岁，男女比例: {gender_ratio}
                
                请结合【{data_source}】这个平台的固有特性（例如淘宝重丰富度、京东重物流和3C、拼多多重下沉市场等），给出：
                1. 当前业绩与用户画像的一句话精准总结。
                2. 针对该平台特性的异常点诊断（比如客单价是否符合该平台调性）。
                3. 下一步的“选品拓流”与“精准营销”实操建议（分点列出）。
                """
                
                try:
                    response = client.chat.completions.create(
                        model="qwen-plus",
                        messages=[
                            {"role": "system", "content": "你是一个专业、犀利的电商数据专家，输出Markdown格式，条理清晰，多用emoji。"},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    st.success("✅ 报告生成完毕！")
                    st.markdown(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"调用 AI 失败，错误信息：{e}")
else:
    # 当还没有数据时，在主界面显示提示
    st.info("👈 请在左侧边栏选择一个模拟案例平台，或上传您的专属 CSV 数据文件。")
