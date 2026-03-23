import streamlit as st
import pandas as pd
import io
from openai import OpenAI
import os
# 1. 页面配置与标题
st.set_page_config(page_title="AI 营销数据洞察助手", page_icon="📈", layout="wide")
st.title("📈 AI 营销数据洞察助手 (Demo版)")
st.markdown("上传您的营销数据（CSV/Excel），AI 将自动帮您找出核心问题并提供优化建议。")

# 核心修改：从环境变量读取API Key，不写死在代码里
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),  # 关键行
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"  # 通义千问的兼容地址，不用改
)



# --- 内置的示例数据 ---
SAMPLE_CSV = """日期,广告计划,投放渠道,花费(元),展现量,点击量,转化量,实际销售额(元)
2023-10-25,种草_美妆,小红书KOC,3200,120000,5500,130,28000
2023-10-25,竞品词_核心,百度搜索,4500,18000,1500,95,35000
2023-10-25,冲量_定向,抖音信息流,15000,650000,9500,210,42000
2023-10-26,种草_美妆,小红书KOC,3500,135000,6100,145,31000
2023-10-26,竞品词_核心,百度搜索,4800,19500,1600,105,38500
2023-10-26,冲量_定向,抖音信息流,22000,950000,14000,230,45000
2023-10-27,种草_美妆,小红书KOC,3800,150000,6800,160,34500
2023-10-27,竞品词_核心,百度搜索,5000,21000,1750,115,41000
2023-10-27,冲量_定向,抖音信息流,35000,1500000,18000,180,32000"""

# 3. 数据来源选择：上传 or 示例
df = None
col1, col2 = st.columns([1, 2])
with col1:
    use_demo = st.button("✨ 一键使用示例数据体验")
with col2:
    uploaded_file = st.file_uploader("或者上传您自己的数据 (CSV 格式)", type=["csv", "xlsx"])

if use_demo:
    df = pd.read_csv(io.StringIO(SAMPLE_CSV))
    st.info("当前正在使用内置的【双十一营销测试数据】")
elif uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

# 4. 如果有数据，则展示分析界面
if df is not None:
    st.write("---")
    st.write("### 📊 数据预览")
    st.dataframe(df.head()) 
    
    st.write("### 📉 实际销售额趋势分析")
    try:
        # 画图：如果有多渠道，按渠道拆分画线会更好看，这里做简单处理
        st.line_chart(df.set_index('日期')['实际销售额(元)']) 
    except Exception as e:
        st.write("提示：当前数据格式不支持生成折线图。")

    st.write("### 🧠 AI 深度洞察报告")
    if st.button("生成营销分析报告 (调用 AI)"):
        with st.spinner("AI 正在疯狂计算与分析中..."):
            data_summary = df.describe().to_string() 
            data_head = df.head().to_string()
            
            prompt = f"""
            你是一个资深的数字营销总监。请根据以下营销数据，生成一份极具业务洞察的报告：
            数据样例：\n{data_head}\n
            数据统计特征：\n{data_summary}\n
            请直接输出：1. 渠道红黑榜(明确指出哪个好哪个差) 2. 异常数据预警(如预算浪费) 3. 下一步优化建议。
            """
            try:
                response = client.chat.completions.create(
                    model="qwen-plus",
                    messages=[
                        {"role": "system", "content": "你是一个专业的数据分析专家，用Markdown排版，使用emoji让排版生动。"},
                        {"role": "user", "content": prompt}
                    ]
                )
                st.success("报告生成完毕！")
                st.markdown(response.choices[0].message.content)
            except Exception as e:
                st.error(f"调用 AI 失败，请检查配置。错误：{e}")
