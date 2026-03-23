# import streamlit as st
# import pandas as pd
# import io
# from openai import OpenAI
# import os

# # 1. 页面配置与标题
# st.set_page_config(page_title="AI 营销数据洞察助手", page_icon="📈", layout="wide")
# st.title("📈 AI 营销数据洞察助手 (Demo版)")
# st.markdown("上传您的营销数据（CSV/Excel），AI 将自动帮您找出核心问题并提供优化建议。")

# # --- 核心修改1：兼容本地测试和云端部署 ---
# # 如果在本地测试，把你的 sk- 密钥写在逗号后面的引号里
# # 部署到云端时，它会自动优先读取云端的环境变量
# api_key = os.environ.get("OPENAI_API_KEY", "你的sk-开头的真实密钥放这里用于本地测试")

# client = OpenAI(
#     api_key=api_key, 
#     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1" 
# )

# # --- 内置的示例数据 ---
# SAMPLE_CSV = """日期,广告计划,投放渠道,花费(元),展现量,点击量,转化量,实际销售额(元)
# 2023-10-25,种草_美妆,小红书KOC,3200,120000,5500,130,28000
# 2023-10-25,竞品词_核心,百度搜索,4500,18000,1500,95,35000
# 2023-10-25,冲量_定向,抖音信息流,15000,650000,9500,210,42000
# 2023-10-26,种草_美妆,小红书KOC,3500,135000,6100,145,31000
# 2023-10-26,竞品词_核心,百度搜索,4800,19500,1600,105,38500
# 2023-10-26,冲量_定向,抖音信息流,22000,950000,14000,230,45000
# 2023-10-27,种草_美妆,小红书KOC,3800,150000,6800,160,34500
# 2023-10-27,竞品词_核心,百度搜索,5000,21000,1750,115,41000
# 2023-10-27,冲量_定向,抖音信息流,35000,1500000,18000,180,32000"""


# # --- 核心修改2：初始化 Streamlit 记忆体 ---
# if "df" not in st.session_state:
#     st.session_state.df = None


# # 3. 数据来源选择：上传 or 示例
# col1, col2 = st.columns([1, 2])
# with col1:
#     use_demo = st.button("✨ 一键使用示例数据体验")
# with col2:
#     uploaded_file = st.file_uploader("或者上传您自己的数据 (CSV 格式)", type=["csv", "xlsx"])

# # 只要点过按钮，就把数据存入“记忆体”中
# if use_demo:
#     st.session_state.df = pd.read_csv(io.StringIO(SAMPLE_CSV))
# elif uploaded_file is not None:
#     if uploaded_file.name.endswith('.csv'):
#         st.session_state.df = pd.read_csv(uploaded_file)
#     else:
#         st.session_state.df = pd.read_excel(uploaded_file)

# # 4. 从“记忆体”中读取数据展示
# if st.session_state.df is not None:
#     df = st.session_state.df # 把记忆体里的数据拿出来用
    
#     st.write("---")
#     st.write("### 📊 数据预览")
#     st.dataframe(df.head()) 
    
#     st.write("### 📉 实际销售额趋势分析")
#     try:
#         st.line_chart(df.set_index('日期')['实际销售额(元)']) 
#     except Exception as e:
#         st.write("提示：当前数据格式不支持生成折线图。")

#     st.write("### 🧠 AI 深度洞察报告")
#     if st.button("生成营销分析报告 (调用 AI)"):
#         with st.spinner("AI 正在疯狂计算与分析中..."):
#             data_summary = df.describe().to_string() 
#             data_head = df.head().to_string()
            
#             prompt = f"""
#             你是一个资深的数字营销总监。请根据以下营销数据，生成一份极具业务洞察的报告：
#             数据样例：\n{data_head}\n
#             数据统计特征：\n{data_summary}\n
#             请直接输出：1. 渠道红黑榜(明确指出哪个好哪个差) 2. 异常数据预警(如预算浪费) 3. 下一步优化建议。
#             """
#             try:
#                 response = client.chat.completions.create(
#                     model="qwen-plus",
#                     messages=[
#                         {"role": "system", "content": "你是一个专业的数据分析专家，用Markdown排版，使用emoji让排版生动。"},
#                         {"role": "user", "content": prompt}
#                     ]
#                 )
#                 st.success("报告生成完毕！")
#                 st.markdown(response.choices[0].message.content)
#             except Exception as e:
#                 st.error(f"调用 AI 失败，请检查配置。错误：{e}")


import streamlit as st
import pandas as pd
from openai import OpenAI
import os

# 1. 页面配置与标题
st.set_page_config(page_title="电商全链路数据洞察系统", page_icon="🛒", layout="wide")
st.title("🛒 平台电商交易数据洞察系统")
st.markdown("上传您的电商平台订单流水（支持淘宝、京东、拼多多等格式），系统将自动进行人群画像与销售提效分析。")

# 2. 初始化大模型客户端
api_key = os.environ.get("OPENAI_API_KEY", "你的sk-开头的真实密钥放这里用于本地测试")
client = OpenAI(
    api_key=api_key, 
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1" 
)

# 3. 数据上传模块
uploaded_file = st.file_uploader("请上传平台交易数据 (例如: 淘宝.csv, 京东.csv)", type=["csv"])

if uploaded_file is not None:
    # 读取数据
    df = pd.read_csv(uploaded_file)
    
    # --- 核心数据预处理 (ETL) ---
    # 把“购买时间”转成标准日期格式，方便画图
    df['购买时间'] = pd.to_datetime(df['购买时间'])
    df['日期'] = df['购买时间'].dt.date
    
    st.write("---")
    st.write("### 🔍 原始流水数据预览 (前5条)")
    st.dataframe(df.head())
    
    # 4. 网页端自动画图分析
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### 📈 每日销售额趋势 (GMV)")
        # 按日期汇总消费金额
        daily_sales = df.groupby('日期')['消费金额'].sum()
        st.line_chart(daily_sales)
        
    with col2:
        st.write("### 📦 各大商品品类销售占比")
        # 按商品类别汇总消费金额
        category_sales = df.groupby('商品类别')['消费金额'].sum()
        st.bar_chart(category_sales)

    # 5. 提取精华数据，准备喂给 AI
    st.write("---")
    st.write("### 🧠 AI 商业深度洞察")
    
    if st.button("一键生成电商运营报告"):
        with st.spinner("AI 正在深度剖析用户画像与消费行为..."):
            
            # 【关键】：让 Python 帮你算出核心指标，而不是发全量数据
            total_gmv = df['消费金额'].sum()
            total_orders = len(df)
            top_category = category_sales.idxmax()
            top_city = df.groupby('用户城市')['消费金额'].sum().idxmax()
            avg_age = df['用户年龄'].mean()
            gender_ratio = df['用户性别'].value_counts().to_dict()
            
            # 拼装给 AI 的提示词 (Prompt)
            prompt = f"""
            你是一位资深的电商平台运营总监。我有一份近期的电商订单交易数据，以下是经过系统计算后的核心指标摘要：
            
            【核心业绩指标】
            - 总销售额 (GMV): {total_gmv:.2f} 元
            - 总订单量: {total_orders} 笔
            - 客单价: {total_gmv/total_orders:.2f} 元
            
            【商品与用户画像】
            - 最畅销商品类别: {top_category}
            - 消费主力城市: {top_city}
            - 消费者平均年龄: {avg_age:.1f} 岁
            - 男女消费者比例: {gender_ratio}
            
            请根据以上摘要数据，生成一份极具业务洞察的报告。请直接输出：
            1. 业绩基本盘诊断 (当前的客单价和销量说明了什么问题？)
            2. 用户画像分析 (针对这群主力消费者，有什么特征？)
            3. 下一步选品与营销建议 (结合最畅销品类和主力人群，应该主推什么？去哪个城市推？)
            """
            
            try:
                response = client.chat.completions.create(
                    model="qwen-plus",
                    messages=[
                        {"role": "system", "content": "你是一个专业、犀利的电商数据分析专家，用Markdown排版，多用加粗和列表，使用emoji让排版生动。"},
                        {"role": "user", "content": prompt}
                    ]
                )
                st.success("运营报告生成完毕！")
                st.markdown(response.choices[0].message.content)
            except Exception as e:
                st.error(f"调用 AI 失败，错误信息：{e}")


