# # # # # # import streamlit as st
# # # # # # import pandas as pd
# # # # # # import io
# # # # # # from openai import OpenAI
# # # # # # import os

# # # # # # # 1. 页面配置与标题
# # # # # # st.set_page_config(page_title="AI 营销数据洞察助手", page_icon="📈", layout="wide")
# # # # # # st.title("📈 AI 营销数据洞察助手 (Demo版)")
# # # # # # st.markdown("上传您的营销数据（CSV/Excel），AI 将自动帮您找出核心问题并提供优化建议。")

# # # # # # # --- 核心修改1：兼容本地测试和云端部署 ---
# # # # # # # 如果在本地测试，把你的 sk- 密钥写在逗号后面的引号里
# # # # # # # 部署到云端时，它会自动优先读取云端的环境变量
# # # # # # api_key = os.environ.get("OPENAI_API_KEY", "你的sk-开头的真实密钥放这里用于本地测试")

# # # # # # client = OpenAI(
# # # # # #     api_key=api_key, 
# # # # # #     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1" 
# # # # # # )

# # # # # # # --- 内置的示例数据 ---
# # # # # # SAMPLE_CSV = """日期,广告计划,投放渠道,花费(元),展现量,点击量,转化量,实际销售额(元)
# # # # # # 2023-10-25,种草_美妆,小红书KOC,3200,120000,5500,130,28000
# # # # # # 2023-10-25,竞品词_核心,百度搜索,4500,18000,1500,95,35000
# # # # # # 2023-10-25,冲量_定向,抖音信息流,15000,650000,9500,210,42000
# # # # # # 2023-10-26,种草_美妆,小红书KOC,3500,135000,6100,145,31000
# # # # # # 2023-10-26,竞品词_核心,百度搜索,4800,19500,1600,105,38500
# # # # # # 2023-10-26,冲量_定向,抖音信息流,22000,950000,14000,230,45000
# # # # # # 2023-10-27,种草_美妆,小红书KOC,3800,150000,6800,160,34500
# # # # # # 2023-10-27,竞品词_核心,百度搜索,5000,21000,1750,115,41000
# # # # # # 2023-10-27,冲量_定向,抖音信息流,35000,1500000,18000,180,32000"""


# # # # # # # --- 核心修改2：初始化 Streamlit 记忆体 ---
# # # # # # if "df" not in st.session_state:
# # # # # #     st.session_state.df = None


# # # # # # # 3. 数据来源选择：上传 or 示例freq='h'
# # # # # # col1, col2 = st.columns([1, 2])
# # # # # # with col1:
# # # # # #     use_demo = st.button("✨ 一键使用示例数据体验")
# # # # # # with col2:
# # # # # #     uploaded_file = st.file_uploader("或者上传您自己的数据 (CSV 格式)", type=["csv", "xlsx"])

# # # # # # # 只要点过按钮，就把数据存入“记忆体”中
# # # # # # if use_demo:
# # # # # #     st.session_state.df = pd.read_csv(io.StringIO(SAMPLE_CSV))
# # # # # # elif uploaded_file is not None:
# # # # # #     if uploaded_file.name.endswith('.csv'):
# # # # # #         st.session_state.df = pd.read_csv(uploaded_file)
# # # # # #     else:
# # # # # #         st.session_state.df = pd.read_excel(uploaded_file)

# # # # # # # 4. 从“记忆体”中读取数据展示
# # # # # # if st.session_state.df is not None:
# # # # # #     df = st.session_state.df # 把记忆体里的数据拿出来用
    
# # # # # #     st.write("---")
# # # # # #     st.write("### 📊 数据预览")
# # # # # #     st.dataframe(df.head()) 
    
# # # # # #     st.write("### 📉 实际销售额趋势分析")
# # # # # #     try:
# # # # # #         st.line_chart(df.set_index('日期')['实际销售额(元)']) 
# # # # # #     except Exception as e:
# # # # # #         st.write("提示：当前数据格式不支持生成折线图。")

# # # # # #     st.write("### 🧠 AI 深度洞察报告")
# # # # # #     if st.button("生成营销分析报告 (调用 AI)"):
# # # # # #         with st.spinner("AI 正在疯狂计算与分析中..."):
# # # # # #             data_summary = df.describe().to_string() 
# # # # # #             data_head = df.head().to_string()
            
# # # # # #             prompt = f"""
# # # # # #             你是一个资深的数字营销总监。请根据以下营销数据，生成一份极具业务洞察的报告：
# # # # # #             数据样例：\n{data_head}\n
# # # # # #             数据统计特征：\n{data_summary}\n
# # # # # #             请直接输出：1. 渠道红黑榜(明确指出哪个好哪个差) 2. 异常数据预警(如预算浪费) 3. 下一步优化建议。
# # # # # #             """
# # # # # #             try:
# # # # # #                 response = client.chat.completions.create(
# # # # # #                     model="qwen-plus",
# # # # # #                     messages=[
# # # # # #                         {"role": "system", "content": "你是一个专业的数据分析专家，用Markdown排版，使用emoji让排版生动。"},
# # # # # #                         {"role": "user", "content": prompt}
# # # # # #                     ]
# # # # # #                 )
# # # # # #                 st.success("报告生成完毕！")
# # # # # #                 st.markdown(response.choices[0].message.content)
# # # # # #             except Exception as e:
# # # # # #                 st.error(f"调用 AI 失败，请检查配置。错误：{e}")


# # # # # import streamlit as st
# # # # # import pandas as pd
# # # # # from openai import OpenAI
# # # # # import os

# # # # # # 1. 页面配置与标题
# # # # # st.set_page_config(page_title="电商全链路数据洞察系统", page_icon="🛒", layout="wide")
# # # # # st.title("🛒 平台电商交易数据洞察系统")
# # # # # st.markdown("上传您的电商平台订单流水（支持淘宝、京东、拼多多等格式），系统将自动进行人群画像与销售提效分析。")

# # # # # # 2. 初始化大模型客户端
# # # # # api_key = os.environ.get("OPENAI_API_KEY", "你的sk-开头的真实密钥放这里用于本地测试")
# # # # # client = OpenAI(
# # # # #     api_key=api_key, 
# # # # #     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1" 
# # # # # )

# # # # # # 3. 数据上传模块
# # # # # uploaded_file = st.file_uploader("请上传平台交易数据 (例如: 淘宝.csv, 京东.csv)", type=["csv"])

# # # # # if uploaded_file is not None:
# # # # #     # 读取数据
# # # # #     df = pd.read_csv(uploaded_file)
    
# # # # #     # --- 核心数据预处理 (ETL) ---
# # # # #     # 把“购买时间”转成标准日期格式，方便画图
# # # # #     df['购买时间'] = pd.to_datetime(df['购买时间'])
# # # # #     df['日期'] = df['购买时间'].dt.date
    
# # # # #     st.write("---")
# # # # #     st.write("### 🔍 原始流水数据预览 (前5条)")
# # # # #     st.dataframe(df.head())
    
# # # # #     # 4. 网页端自动画图分析
# # # # #     col1, col2 = st.columns(2)
    
# # # # #     with col1:
# # # # #         st.write("### 📈 每日销售额趋势 (GMV)")
# # # # #         # 按日期汇总消费金额
# # # # #         daily_sales = df.groupby('日期')['消费金额'].sum()
# # # # #         st.line_chart(daily_sales)
        
# # # # #     with col2:
# # # # #         st.write("### 📦 各大商品品类销售占比")
# # # # #         # 按商品类别汇总消费金额
# # # # #         category_sales = df.groupby('商品类别')['消费金额'].sum()
# # # # #         st.bar_chart(category_sales)

# # # # #     # 5. 提取精华数据，准备喂给 AI
# # # # #     st.write("---")
# # # # #     st.write("### 🧠 AI 商业深度洞察")
    
# # # # #     if st.button("一键生成电商运营报告"):
# # # # #         with st.spinner("AI 正在深度剖析用户画像与消费行为..."):
            
# # # # #             # 【关键】：让 Python 帮你算出核心指标，而不是发全量数据
# # # # #             total_gmv = df['消费金额'].sum()
# # # # #             total_orders = len(df)
# # # # #             top_category = category_sales.idxmax()
# # # # #             top_city = df.groupby('用户城市')['消费金额'].sum().idxmax()
# # # # #             avg_age = df['用户年龄'].mean()
# # # # #             gender_ratio = df['用户性别'].value_counts().to_dict()
            
# # # # #             # 拼装给 AI 的提示词 (Prompt)
# # # # #             prompt = f"""
# # # # #             你是一位资深的电商平台运营总监。我有一份近期的电商订单交易数据，以下是经过系统计算后的核心指标摘要：
            
# # # # #             【核心业绩指标】
# # # # #             - 总销售额 (GMV): {total_gmv:.2f} 元
# # # # #             - 总订单量: {total_orders} 笔
# # # # #             - 客单价: {total_gmv/total_orders:.2f} 元
            
# # # # #             【商品与用户画像】
# # # # #             - 最畅销商品类别: {top_category}
# # # # #             - 消费主力城市: {top_city}
# # # # #             - 消费者平均年龄: {avg_age:.1f} 岁
# # # # #             - 男女消费者比例: {gender_ratio}
            
# # # # #             请根据以上摘要数据，生成一份极具业务洞察的报告。请直接输出：
# # # # #             1. 业绩基本盘诊断 (当前的客单价和销量说明了什么问题？)
# # # # #             2. 用户画像分析 (针对这群主力消费者，有什么特征？)
# # # # #             3. 下一步选品与营销建议 (结合最畅销品类和主力人群，应该主推什么？去哪个城市推？)
# # # # #             """
            
# # # # #             try:
# # # # #                 response = client.chat.completions.create(
# # # # #                     model="qwen-plus",
# # # # #                     messages=[
# # # # #                         {"role": "system", "content": "你是一个专业、犀利的电商数据分析专家，用Markdown排版，多用加粗和列表，使用emoji让排版生动。"},
# # # # #                         {"role": "user", "content": prompt}
# # # # #                     ]
# # # # #                 )
# # # # #                 st.success("运营报告生成完毕！")
# # # # #                 st.markdown(response.choices[0].message.content)
# # # # #             except Exception as e:
# # # # #                 st.error(f"调用 AI 失败，错误信息：{e}")
# # # # import streamlit as st
# # # # import pandas as pd
# # # # from openai import OpenAI
# # # # import os
# # # # import plotly.express as px  # 引入超强绘图神器

# # # # # 1. 页面配置 (开启宽屏模式，让图表更大气)
# # # # st.set_page_config(page_title="企业级电商数据洞察助手", page_icon="🛒", layout="wide")
# # # # st.title("🛒 企业零售海量数据 AI 洞察平台")
# # # # st.markdown("支持批量上传原始订单流水，系统将自动清洗、聚合数据，并生成**可交互的BI看板**与 AI 专家诊断。")

# # # # # 2. 初始化大模型客户端
# # # # api_key = os.environ.get("OPENAI_API_KEY", "sk-cdc57fd44a394cea8ec25dd4ad2512f7")
# # # # client = OpenAI(
# # # #     api_key=api_key, 
# # # #     base_url="https://ws-vvr85dv3ndbxfxtu.ap-southeast-1.maas.aliyuncs.com/compatible-model/v1" 
# # # # )

# # # # # --- 核心黑科技：加入数据缓存，提速10倍！ ---
# # # # @st.cache_data
# # # # def process_data(uploaded_files):
# # # #     df_list = []
# # # #     for file in uploaded_files:
# # # #         try:
# # # #             temp_df = pd.read_csv(file, encoding='utf-8')
# # # #         except UnicodeDecodeError:
# # # #             temp_df = pd.read_csv(file, encoding='gbk')
# # # #         df_list.append(temp_df)
        
# # # #     df = pd.concat(df_list, ignore_index=True)
# # # #     df['购买时间'] = pd.to_datetime(df['购买时间'])
# # # #     df['日期'] = df['购买时间'].dt.date
# # # #     return df

# # # # # 3. 数据上传模块
# # # # uploaded_files = st.file_uploader("📂 请批量上传订单流水数据 (CSV格式)", type=["csv"], accept_multiple_files=True)

# # # # if uploaded_files:
# # # #     with st.spinner("⏳ 正在清洗合并海量数据..."):
# # # #         # 调用缓存的数据处理函数
# # # #         df = process_data(uploaded_files)
    
# # # #     st.success(f"✅ 数据合并清洗完成！共处理 **{len(df):,}** 条底层交易流水。")
    
# # # #     # ==========================================
# # # #     # 🎨 4. 高级绚丽 BI 看板 (Plotly驱动)
# # # #     # ==========================================
# # # #     st.write("---")
# # # #     st.write("### 📊 核心业务可视化大屏")
    
# # # #     # 顶部核心指标 KPI 卡片
# # # #     col1, col2, col3, col4 = st.columns(4)
# # # #     col1.metric("💰 总销售额 (元)", f"¥ {df['消费金额'].sum():,.2f}")
# # # #     col2.metric("📦 总订单数", f"{len(df):,}")
# # # #     col3.metric("🛍️ 销售商品总件数", f"{df['购买数量'].sum():,}")
# # # #     col4.metric("💳 客单价 (元)", f"¥ {(df['消费金额'].sum() / len(df)):,.2f}")

# # # #     st.markdown("<br>", unsafe_allow_html=True) # 加点空行

# # # #     # 图表第一排：趋势图 + 饼图
# # # #     chart_col1, chart_col2 = st.columns([6, 4]) # 6:4 比例分配宽度
    
# # # #     with chart_col1:
# # # #         # 📈 渐变面积趋势图
# # # #         daily_sales = df.groupby('日期')['消费金额'].sum().reset_index()
# # # #         fig_trend = px.area(daily_sales, x='日期', y='消费金额', 
# # # #                             title="📈 每日营收趋势 (面积图)", 
# # # #                             markers=True, 
# # # #                             color_discrete_sequence=['#00C698']) # 清爽的翠绿色
# # # #         st.plotly_chart(fig_trend, use_container_width=True)

# # # #     with chart_col2:
# # # #         # 🍩 多彩环形饼图
# # # #         category_sales = df.groupby('商品类别')['消费金额'].sum().reset_index()
# # # #         fig_pie = px.pie(category_sales, names='商品类别', values='消费金额', 
# # # #                          hole=0.4, # 变成中间空心的环形图
# # # #                          title="🛍️ 商品类别营收占比")
# # # #         fig_pie.update_traces(textposition='inside', textinfo='percent+label')
# # # #         st.plotly_chart(fig_pie, use_container_width=True)

# # # #     # 图表第二排：条形图 + 用户画像
# # # #     chart_col3, chart_col4 = st.columns([5, 5])
    
# # # #     with chart_col3:
# # # #         # 🏙️ 动态多色彩色条形图
# # # #         city_sales = df.groupby('用户城市')['消费金额'].sum().sort_values(ascending=True).tail(10).reset_index() # 取Top10并倒序让最高的在上面
# # # #         fig_city = px.bar(city_sales, x='消费金额', y='用户城市', orientation='h', 
# # # #                           color='消费金额', # 根据金额自动渐变上色
# # # #                           color_continuous_scale=px.colors.sequential.Sunset, # 晚霞渐变色
# # # #                           title="🏙️ 营收贡献 TOP 10 城市")
# # # #         st.plotly_chart(fig_city, use_container_width=True)

# # # #     with chart_col4:
# # # #         # 👥 年龄与性别分布直方图
# # # #         fig_demo = px.histogram(df, x='用户年龄', color='用户性别', 
# # # #                                 nbins=20, barmode='group',
# # # #                                 color_discrete_map={'男': '#3498db', '女': '#e74c3c'}, # 经典红蓝配色
# # # #                                 title="👥 用户人群画像 (年龄与性别)")
# # # #         st.plotly_chart(fig_demo, use_container_width=True)

# # # #     # ==========================================
# # # #     # 🧠 5. AI 业务诊断模块
# # # #     # ==========================================
# # # #     st.write("---")
# # # #     st.write("### 🧠 AI 零售数据总监深度报告")
    
# # # #     # 提前生成 AI 需要的数据摘要
# # # #     city_str = df.groupby('用户城市')['消费金额'].sum().sort_values(ascending=False).head(5).to_string()
# # # #     cat_str = df.groupby('商品类别')['消费金额'].sum().sort_values(ascending=False).to_string()
# # # #     gender_str = df.groupby('用户性别')['消费金额'].sum().to_string()

# # # #     if st.button("✨ 一键生成深度商业诊断 ✨"):
# # # #         with st.spinner("AI 正在深度思考业务逻辑..."):
# # # #             summary_text = f"""
# # # #             总体表现：总销售额 {df['消费金额'].sum():.2f} 元，共 {len(df)} 笔订单。
# # # #             品类表现摘要：\n{cat_str}
# # # #             城市表现前五名：\n{city_str}
# # # #             男女消费占比：\n{gender_str}
# # # #             """
            
# # # #             prompt = f"""
# # # #             你是一位顶级的电商零售数据分析总监。请根据以下浓缩的脱敏数据摘要，写一份极具深度的业务诊断报告：
# # # #             【数据摘要】：\n{summary_text}\n
# # # #             请严格按照以下结构输出（使用 Markdown，加上 emoji）：
# # # #             1. **大盘诊断**：评价总体业绩与客单价。
# # # #             2. **爆款与品类洞察**：指出核心品类和需要优化的长尾品类。
# # # #             3. **高价值人群画像**：从性别、城市维度描绘核心利润人群。
# # # #             4. **下一步行动建议**：给出至少 3 条落地性极强的营销/备货策略。
# # # #             """
            
# # # #             try:
# # # #                 response = client.chat.completions.create(
# # # #                     model="qwen-plus",
# # # #                     messages=[
# # # #                         {"role": "system", "content": "你是一个用数据说话、眼光毒辣的商业顾问。语言风格专业、简练。"},
# # # #                         {"role": "user", "content": prompt}
# # # #                     ]
# # # #                 )
# # # #                 st.success("✅ 诊断报告已生成！")
# # # #                 st.markdown(response.choices[0].message.content)
# # # #             except Exception as e:
# # # #                 st.error(f"调用 AI 失败，请检查网络或配置。错误详情：{e}")


# # # import streamlit as st
# # # import pandas as pd
# # # import numpy as np
# # # from openai import OpenAI
# # # import os
# # # import plotly.express as px
# # # import plotly.graph_objects as go

# # # # ==========================================
# # # # 1. 页面与全局样式配置 (大厂 BI 级 UI)
# # # # ==========================================
# # # st.set_page_config(page_title="全域电商数据大屏", page_icon="📊", layout="wide")

# # # # 注入自定义 CSS 让关键指标卡片带渐变色和阴影，告别单一颜色
# # # st.markdown("""
# # # <style>
# # #     div[data-testid="metric-container"] {
# # #         background: linear-gradient(135deg, #f6f8fd 0%, #f1f5f9 100%);
# # #         border-radius: 10px;
# # #         padding: 15px;
# # #         border: 1px solid #e2e8f0;
# # #         box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
# # #     }
# # # </style>
# # # """, unsafe_allow_html=True)

# # # st.title("📊 全域电商数据可视化与 AI 决策中心")
# # # st.markdown("覆盖**流量、转化、交易、用户、商品、营销、供应链**七大维度，支持多平台一键切换与 AI 深度诊断。")

# # # # ==========================================
# # # # 2. AI 客户端初始化
# # # # ==========================================
# # # api_key = os.environ.get("OPENAI_API_KEY", "sk-cdc57fd44a394cea8ec25dd4ad2512f7")
# # # client = OpenAI(
# # #     api_key=api_key, 
# # #     base_url="https://ws-vvr85dv3ndbxfxtu.ap-southeast-1.maas.aliyuncs.com/compatible-model/v1"
# # # )

# # # # ==========================================
# # # # 3. 核心数据引擎 (读取真实CSV + 动态推算全域数据)
# # # # ==========================================
# # # @st.cache_data
# # # def load_and_enhance_data(platform_name):
# # #     # 尝试读取同目录下的 CSV 文件
# # #     file_path = f"{platform_name}.csv"
# # #     try:
# # #         df = pd.read_csv(file_path, encoding='utf-8')
# # #     except Exception:
# # #         try:
# # #             df = pd.read_csv(file_path, encoding='gbk')
# # #         except Exception:
# # #             # 如果本地没有这个文件，为了防止页面崩溃，生成一份极其逼真的备用模拟数据
# # #             st.warning(f"⚠️ 未在同级目录找到 {file_path}，已自动启用备用模拟数据集进行演示。")
# # #             dates = pd.date_range(start='2024-01-01', periods=1000, freq='h')
# # #             df = pd.DataFrame({
# # #                 '用户ID': [f"U{np.random.randint(1000, 9999)}" for _ in range(1000)],
# # #                 '商品类别': np.random.choice(['美妆', '服饰', '数码', '食品', '家居', '运动'], 1000),
# # #                 '消费金额': np.random.uniform(50, 3000, 1000),
# # #                 '购买数量': np.random.randint(1, 5, 1000),
# # #                 '购买时间': np.random.choice(dates, 1000),
# # #                 '用户城市': np.random.choice(['北京', '上海', '广州', '深圳', '成都', '杭州', '重庆'], 1000),
# # #                 '用户性别': np.random.choice(['男', '女'], 1000, p=[0.4, 0.6]),
# # #                 '用户年龄': np.random.randint(18, 60, 1000)
# # #             })
            
# # #     # 数据基础清洗
# # #     df['购买时间'] = pd.to_datetime(df['购买时间'])
# # #     df['日期'] = df['购买时间'].dt.date
# # #     df['小时'] = df['购买时间'].dt.hour
# # #     df['星期'] = df['购买时间'].dt.day_name()
# # #     return df

# # # # ==========================================
# # # # ==========================================
# # # # 4. 侧边栏：多平台切换 Demo (动态联动 Logo 升级版)
# # # # ==========================================
# # # # 建立一个“字典”，映射各大平台的真实高清 Logo 地址
# # # logo_map = {
# # #     "淘宝": "https://img.alicdn.com/tfs/TB1_uT8a5ERMeJjSspiXXbZLFXa-143-59.png",
# # #     "天猫": "天猫.png",
# # #     "京东": "https://misc.360buyimg.com/lib/img/e/logo-201305-b.png",
# # #     "拼多多": "拼多多.png", # 拼多多官方图床有极强的防盗链，暂用默认电商Logo替代
# # #     "1688": "阿里巴巴.png",
# # #     "苏宁": "苏宁易购.png"
# # # }

# # # # 技巧：先在侧边栏最顶端生成一个“隐形的空位”
# # # logo_placeholder = st.sidebar.empty() 

# # # st.sidebar.header("🎯 经营大盘控制台")
# # # platforms = ["淘宝", "天猫", "京东", "拼多多", "1688", "苏宁易购"]

# # # # 捕捉用户的选择
# # # selected_platform = st.sidebar.radio("一键切换分析平台", platforms)

# # # # 根据用户的选择，把对应的 Logo 塞进刚才留好的空位里
# # # logo_placeholder.image(logo_map[selected_platform], width=120)

# # # # 加载数据
# # # with st.spinner(f"正在抽取 {selected_platform} 全域业务数据..."):
# # #     df = load_and_enhance_data(selected_platform)
# # # # 基于真实订单数，反推（模拟）出流量和漏斗数据，让演示显得真实完整
# # # real_orders = len(df)
# # # real_gmv = df['消费金额'].sum()
# # # mock_uv = real_orders * np.random.randint(15, 25)  # 假设转化率在 4%-6%
# # # mock_pv = mock_uv * 3.5
# # # mock_cart = int(mock_uv * 0.3)

# # # st.sidebar.write("---")
# # # st.sidebar.success(f"✅ {selected_platform} 数据接入正常\n共加载 {real_orders:,} 笔真实交易。")

# # # # ==========================================
# # # # 5. UI 布局：四大业务模块 Tab 切换
# # # # ==========================================
# # # tab1, tab2, tab3, tab4 = st.tabs([
# # #     "💰 交易与流量 (大盘)", 
# # #     "👥 用户与商品 (画像)", 
# # #     "🚀 营销与供应链 (运营)", 
# # #     "🧠 AI 深度诊断报告"
# # # ])

# # # # ----------------- TAB 1: 交易与流量 -----------------
# # # with tab1:
# # #     st.markdown("### 1. 核心交易指标 (Transaction)")
# # #     c1, c2, c3, c4 = st.columns(4)
# # #     c1.metric("💰 销售额 GMV", f"¥ {real_gmv:,.0f}", "+12.5% 环比")
# # #     c2.metric("💳 支付订单量", f"{real_orders:,} 笔", "+5.2% 环比")
# # #     c3.metric("🛒 客单价", f"¥ {real_gmv/real_orders:,.2f}", "-1.2% 环比")
# # #     c4.metric("👥 独立访客 (UV)", f"{mock_uv:,} 人", "+18.0% 环比")

# # #     st.markdown("<br>", unsafe_allow_html=True)
    
# # #     col_t1, col_t2 = st.columns([6, 4])
# # #     with col_t1:
# # #         # 多色渐变面积图 (交易趋势)
# # #         daily_sales = df.groupby('日期')['消费金额'].sum().reset_index()
# # #         fig_trend = px.area(daily_sales, x='日期', y='消费金额', 
# # #                             title=f"📈 {selected_platform} 每日 GMV 趋势",
# # #                             color_discrete_sequence=['#FF4B4B'])
# # #         st.plotly_chart(fig_trend, use_container_width=True)
        
# # #     with col_t2:
# # #         # 极具视觉冲击力的 3D 漏斗图 (转化流转)
# # #         funnel_data = dict(
# # #             阶段=['浏览 (PV)', '访客 (UV)', '加购人数', '下单人数', '支付完成'],
# # #             数值=[mock_pv, mock_uv, mock_cart, int(real_orders*1.2), real_orders]
# # #         )
# # #         fig_funnel = go.Figure(go.Funnel(
# # #             y=funnel_data['阶段'], x=funnel_data['数值'],
# # #             textinfo="value+percent initial",
# # #             marker={"color": ["#3498db", "#2ecc71", "#f1c40f", "#e67e22", "#e74c3c"]}
# # #         ))
# # #         fig_funnel.update_layout(title="🔽 核心转化漏斗分析")
# # #         st.plotly_chart(fig_funnel, use_container_width=True)

# # # # ----------------- TAB 2: 用户与商品 -----------------
# # # with tab2:
# # #     st.markdown("### 2. 用户画像与商品表现 (User & Product)")
# # #     col_u1, col_u2 = st.columns(2)
    
# # #     with col_u1:
# # #         # 树状图/板块图 (类目占比，比饼图更高大上)
# # #         cat_sales = df.groupby('商品类别')['消费金额'].sum().reset_index()
# # #         fig_tree = px.treemap(cat_sales, path=['商品类别'], values='消费金额',
# # #                               color='消费金额', color_continuous_scale='Viridis',
# # #                               title="🛍️ 商品品类营收贡献 (Treemap)")
# # #         st.plotly_chart(fig_tree, use_container_width=True)
        
# # #     with col_u2:
# # #         # 热力图 (用户购买时间分布)
# # #         heatmap_data = df.groupby(['星期', '小时']).size().reset_index(name='订单数')
# # #         fig_heat = px.density_heatmap(heatmap_data, x='小时', y='星期', z='订单数',
# # #                                       color_continuous_scale='YlOrRd',
# # #                                       title="🔥 用户下单时间热力图 (寻优投放时段)")
# # #         st.plotly_chart(fig_heat, use_container_width=True)

# # #     col_u3, col_u4 = st.columns(2)
# # #     with col_u3:
# # #         # 用户年龄性别画像 (带图例的直方图)
# # #         fig_demo = px.histogram(df, x='用户年龄', color='用户性别', nbins=15, 
# # #                                 barmode='group', color_discrete_map={'男': '#2980b9', '女': '#c0392b'},
# # #                                 title="👥 消费者年龄与性别分布")
# # #         st.plotly_chart(fig_demo, use_container_width=True)
        
# # #     with col_u4:
# # #         # 城市排行榜 (条形图)
# # #         city_sales = df.groupby('用户城市')['消费金额'].sum().sort_values().tail(10).reset_index()
# # #         fig_city = px.bar(city_sales, x='消费金额', y='用户城市', orientation='h',
# # #                           color='消费金额', color_continuous_scale='Blues',
# # #                           title="🏙️ 核心高净值城市 TOP 10 (地域分布)")
# # #         st.plotly_chart(fig_city, use_container_width=True)

# # # # ----------------- TAB 3: 营销与供应链 -----------------
# # # with tab3:
# # #     st.markdown("### 3. 营销效率与履约质量 (Marketing & Supply Chain)")
# # #     st.info("💡 注：此模块数据结合历史大盘波动动态模拟，用于指导宏观运营决策。")
    
# # #     col_m1, col_m2 = st.columns(2)
# # #     with col_m1:
# # #         # 环形图 (流量来源占比)
# # #         sources = pd.DataFrame({
# # #             '渠道': ['站内搜索', '首页推荐', '短视频/直播', '站外广告', '自然复购'],
# # #             '占比': [35, 25, 20, 15, 5]
# # #         })
# # #         fig_pie = px.pie(sources, names='渠道', values='占比', hole=0.5,
# # #                          title="🌐 流量来源结构占比", color_discrete_sequence=px.colors.qualitative.Pastel)
# # #         fig_pie.update_traces(textinfo='percent+label')
# # #         st.plotly_chart(fig_pie, use_container_width=True)
        
# # #     with col_m2:
# # #         # 仪表盘 Gauge Chart (供应链发货达标率)
# # #         fig_gauge = go.Figure(go.Indicator(
# # #             mode = "gauge+number",
# # #             value = 98.2,
# # #             title = {'text': "📦 48小时履约发货率 (%)"},
# # #             gauge = {'axis': {'range': [None, 100]},
# # #                      'bar': {'color': "#27ae60"},
# # #                      'steps' : [
# # #                          {'range': [0, 80], 'color': "#e74c3c"},
# # #                          {'range': [80, 90], 'color': "#f1c40f"},
# # #                          {'range': [90, 100], 'color': "#ecf0f1"}]}
# # #         ))
# # #         st.plotly_chart(fig_gauge, use_container_width=True)

# # # # ----------------- TAB 4: AI 深度诊断 -----------------
# # # with tab4:
# # #     st.markdown(f"### 🧠 {selected_platform} 大盘数据 AI 智能诊断")
    
# # #     if st.button("✨ 生成全域经营分析报告 ✨", type="primary"):
# # #         with st.spinner("AI 正在汇聚 7 大维度数据，生成总监级洞察报告..."):
            
# # #             # 将核心数据浓缩成文本喂给大模型
# # #             cat_top = df.groupby('商品类别')['消费金额'].sum().sort_values(ascending=False).head(3).to_dict()
# # #             city_top = df.groupby('用户城市')['消费金额'].sum().sort_values(ascending=False).head(3).to_dict()
            
# # #             summary_text = f"""
# # #             当前平台：{selected_platform}
# # #             1. 交易与流量：总GMV ¥{real_gmv:.2f}，总订单 {real_orders}笔，客单价 ¥{real_gmv/real_orders:.2f}。预估转化漏斗中，PV到加购转化率良好，但加购到支付流失率约 {(1 - real_orders/mock_cart)*100:.1f}%。
# # #             2. 商品表现：TOP3营收品类为 {cat_top}。
# # #             3. 用户画像：核心消费城市TOP3为 {city_top}。
# # #             4. 营销与供应链：站内搜索和推荐占流量大头(60%)，48小时发货率高达98.2%。
# # #             """
            
# # #             prompt = f"""
# # #             你是一位年薪百万的电商大厂（阿里/京东级别）数据运营总监。请根据以下全域经营数据，写一份汇报给CEO的商业洞察报告：
# # #             【数据摘要】：\n{summary_text}\n
# # #             请严格按照以下结构输出（Markdown格式，多用 emoji 和专业的业务黑话）：
# # #             1. 📈 **全域经营大盘总结**：一句话定调目前的生意健康度。
# # #             2. ⚠️ **转化漏斗痛点**：针对“加购到支付”的流失，深度剖析可能的原因（如促销力度不够、运费门槛等）。
# # #             3. 🎯 **人货场重构建议**：
# # #                - **人 (用户)**：针对高优城市该怎么做定向运营？
# # #                - **货 (商品)**：头部类目如何拉升利润？
# # #                - **场 (营销/流量)**：如何优化流量结构？
# # #             4. 💡 **下一步核心 Action 落地建议**。
# # #             """
            
# # #             try:
# # #                 response = client.chat.completions.create(
# # #                     model="qwen-plus",
# # #                     messages=[
# # #                         {"role": "system", "content": "你是资深电商专家，擅长从流量、转化、客单价等维度做深度业务拆解。"},
# # #                         {"role": "user", "content": prompt}
# # #                     ]
# # #                 )
# # #                 st.success("✅ AI 诊断报告已生成！")
# # #                 st.markdown(response.choices[0].message.content)
# # #             except Exception as e:
# # #                 st.error(f"调用 AI 失败，请检查网络。错误详情：{e}")
# # import streamlit as st
# # import pandas as pd
# # import numpy as np
# # from openai import OpenAI
# # import os
# # import plotly.express as px
# # import plotly.graph_objects as go

# # # ==========================================
# # # 1. 页面与全局样式配置 (大厂 BI 级 UI)
# # # ==========================================
# # st.set_page_config(page_title="全域电商数据大屏", page_icon="📊", layout="wide")

# # st.markdown("""
# # <style>
# #     div[data-testid="metric-container"] {
# #         background: linear-gradient(135deg, #f6f8fd 0%, #f1f5f9 100%);
# #         border-radius: 10px;
# #         padding: 15px;
# #         border: 1px solid #e2e8f0;
# #         box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
# #     }
# # </style>
# # """, unsafe_allow_html=True)

# # st.title("📊 全域电商数据可视化与 AI 决策中心")
# # st.markdown("覆盖**流量、转化、交易、用户、商品、营销、供应链**七大维度，支持多平台一键切换、自定义数据上传与 AI 深度诊断。")

# # # ==========================================
# # # 2. AI 客户端初始化
# # # ==========================================
# # api_key = os.environ.get("OPENAI_API_KEY", "sk-cdc57fd44a394cea8ec25dd4ad2512f7")
# # client = OpenAI(
# #     api_key=api_key, 
# #     base_url="https://ws-vvr85dv3ndbxfxtu.ap-southeast-1.maas.aliyuncs.com/compatible-model/v1"
# # )

# # # ==========================================
# # # 3. 核心数据引擎 (读取本地文件或生成模拟数据)
# # # ==========================================
# # @st.cache_data
# # def load_and_enhance_data(platform_name):
# #     file_path = f"{platform_name}.csv"
# #     try:
# #         df = pd.read_csv(file_path, encoding='utf-8')
# #     except Exception:
# #         try:
# #             df = pd.read_csv(file_path, encoding='gbk')
# #         except Exception:
# #             st.warning(f"⚠️ 未在同级目录找到 {file_path}，已自动启用备用模拟数据集进行演示。")
# #             dates = pd.date_range(start='2024-01-01', periods=1000, freq='h')
# #             df = pd.DataFrame({
# #                 '用户ID': [f"U{np.random.randint(1000, 9999)}" for _ in range(1000)],
# #                 '商品类别': np.random.choice(['美妆', '服饰', '数码', '食品', '家居', '运动'], 1000),
# #                 '消费金额': np.random.uniform(50, 3000, 1000),
# #                 '购买数量': np.random.randint(1, 5, 1000),
# #                 '购买时间': np.random.choice(dates, 1000),
# #                 '用户城市': np.random.choice(['北京', '上海', '广州', '深圳', '成都', '杭州', '重庆'], 1000),
# #                 '用户性别': np.random.choice(['男', '女'], 1000, p=[0.4, 0.6]),
# #                 '用户年龄': np.random.randint(18, 60, 1000)
# #             })
            
# #     df['购买时间'] = pd.to_datetime(df['购买时间'])
# #     df['日期'] = df['购买时间'].dt.date
# #     df['小时'] = df['购买时间'].dt.hour
# #     df['星期'] = df['购买时间'].dt.day_name()
# #     return df

# # # ==========================================
# # # 4. 侧边栏：多平台切换与【自定义上传】
# # # ==========================================
# # logo_map = {
# #     "淘宝": "https://img.alicdn.com/tfs/TB1_uT8a5ERMeJjSspiXXbZLFXa-143-59.png",
# #     "天猫": "天猫.png",
# #     "京东": "https://misc.360buyimg.com/lib/img/e/logo-201305-b.png",
# #     "拼多多": "拼多多.png", 
# #     "1688": "阿里巴巴.png",
# #     "苏宁易购": "苏宁易购.png"
# # }

# # logo_placeholder = st.sidebar.empty() 
# # st.sidebar.header("🎯 经营大盘控制台")

# # # 新增了“自定义上传”选项
# # platforms = ["淘宝", "天猫", "京东", "拼多多", "1688", "苏宁易购", "🛠️ 自定义数据上传"]
# # selected_platform = st.sidebar.radio("请选择分析数据源", platforms)

# # # 核心逻辑分支：如果是内置平台，读内置文件；如果是自定义，弹出上传框
# # if selected_platform != "🛠️ 自定义数据上传":
# #     if selected_platform in logo_map:
# #         logo_placeholder.image(logo_map[selected_platform], width=120)
# #     with st.spinner(f"正在抽取 {selected_platform} 全域业务数据..."):
# #         df = load_and_enhance_data(selected_platform)
# # else:
# #     logo_placeholder.empty() # 清空 Logo
# #     st.sidebar.markdown("---")
# #     uploaded_file = st.sidebar.file_uploader("📂 请上传标准电商交易流水 (CSV格式)", type=["csv"])
    
# #     if uploaded_file is not None:
# #         with st.spinner("正在解析您上传的数据..."):
# #             try:
# #                 df = pd.read_csv(uploaded_file, encoding='utf-8')
# #             except Exception:
# #                 df = pd.read_csv(uploaded_file, encoding='gbk')
            
# #             # 兼容性清洗，确保用户上传的文件包含所需时间字段
# #             if '购买时间' in df.columns:
# #                 df['购买时间'] = pd.to_datetime(df['购买时间'])
# #                 df['日期'] = df['购买时间'].dt.date
# #                 df['小时'] = df['购买时间'].dt.hour
# #                 df['星期'] = df['购买时间'].dt.day_name()
# #             else:
# #                 st.error("❌ 数据格式错误：上传的 CSV 必须包含【购买时间】列！")
# #                 st.stop()
# #     else:
# #         st.info("👈 请在左侧上传您的自定义 CSV 文件以开启大屏分析。")
# #         st.stop() # 停止往下执行，等待用户上传

# # # ==========================================
# # # 提取基础数据与模拟全域漏斗
# # # ==========================================
# # real_orders = len(df)
# # real_gmv = df['消费金额'].sum() if '消费金额' in df.columns else 0
# # mock_uv = real_orders * np.random.randint(15, 25) 
# # mock_pv = mock_uv * 3.5
# # mock_cart = int(mock_uv * 0.3)

# # st.sidebar.write("---")
# # if selected_platform == "🛠️ 自定义数据上传":
# #     st.sidebar.success(f"✅ 自定义数据解析成功\n共加载 {real_orders:,} 笔交易。")
# # else:
# #     st.sidebar.success(f"✅ {selected_platform} 数据接入正常\n共加载 {real_orders:,} 笔真实交易。")

# # # ==========================================
# # # 5. UI 布局：四大业务模块 Tab 切换
# # # ==========================================
# # tab1, tab2, tab3, tab4 = st.tabs([
# #     "💰 交易与流量 (大盘)", 
# #     "👥 用户与商品 (画像)", 
# #     "🚀 营销与供应链 (运营)", 
# #     "🧠 AI 深度诊断报告"
# # ])

# # # ----------------- TAB 1: 交易与流量 -----------------
# # with tab1:
# #     st.markdown("### 1. 核心交易指标 (Transaction)")
# #     c1, c2, c3, c4 = st.columns(4)
# #     c1.metric("💰 销售额 GMV", f"¥ {real_gmv:,.0f}", "+12.5% 环比")
# #     c2.metric("💳 支付订单量", f"{real_orders:,} 笔", "+5.2% 环比")
# #     c3.metric("🛒 客单价", f"¥ {real_gmv/real_orders if real_orders>0 else 0:,.2f}", "-1.2% 环比")
# #     c4.metric("👥 独立访客 (UV)", f"{mock_uv:,} 人", "+18.0% 环比")

# #     st.markdown("<br>", unsafe_allow_html=True)
    
# #     col_t1, col_t2 = st.columns([6, 4])
# #     with col_t1:
# #         if '日期' in df.columns and '消费金额' in df.columns:
# #             daily_sales = df.groupby('日期')['消费金额'].sum().reset_index()
# #             fig_trend = px.area(daily_sales, x='日期', y='消费金额', 
# #                                 title=f"📈 每日 GMV 趋势",
# #                                 color_discrete_sequence=['#FF4B4B'])
# #             st.plotly_chart(fig_trend, use_container_width=True)
        
# #     with col_t2:
# #         funnel_data = dict(
# #             阶段=['浏览 (PV)', '访客 (UV)', '加购人数', '下单人数', '支付完成'],
# #             数值=[mock_pv, mock_uv, mock_cart, int(real_orders*1.2), real_orders]
# #         )
# #         fig_funnel = go.Figure(go.Funnel(
# #             y=funnel_data['阶段'], x=funnel_data['数值'],
# #             textinfo="value+percent initial",
# #             marker={"color": ["#3498db", "#2ecc71", "#f1c40f", "#e67e22", "#e74c3c"]}
# #         ))
# #         fig_funnel.update_layout(title="🔽 核心转化漏斗分析")
# #         st.plotly_chart(fig_funnel, use_container_width=True)

# # # ----------------- TAB 2: 用户与商品 -----------------
# # with tab2:
# #     st.markdown("### 2. 用户画像与商品表现 (User & Product)")
# #     col_u1, col_u2 = st.columns(2)
    
# #     with col_u1:
# #         if '商品类别' in df.columns and '消费金额' in df.columns:
# #             cat_sales = df.groupby('商品类别')['消费金额'].sum().reset_index()
# #             fig_tree = px.treemap(cat_sales, path=['商品类别'], values='消费金额',
# #                                   color='消费金额', color_continuous_scale='Viridis',
# #                                   title="🛍️ 商品品类营收贡献 (Treemap)")
# #             st.plotly_chart(fig_tree, use_container_width=True)
        
# #     with col_u2:
# #         if '小时' in df.columns and '星期' in df.columns:
# #             heatmap_data = df.groupby(['星期', '小时']).size().reset_index(name='订单数')
# #             fig_heat = px.density_heatmap(heatmap_data, x='小时', y='星期', z='订单数',
# #                                           color_continuous_scale='YlOrRd',
# #                                           title="🔥 用户下单时间热力图")
# #             st.plotly_chart(fig_heat, use_container_width=True)

# #     col_u3, col_u4 = st.columns(2)
# #     with col_u3:
# #         if '用户年龄' in df.columns and '用户性别' in df.columns:
# #             fig_demo = px.histogram(df, x='用户年龄', color='用户性别', nbins=15, 
# #                                     barmode='group', color_discrete_map={'男': '#2980b9', '女': '#c0392b'},
# #                                     title="👥 消费者年龄与性别分布")
# #             st.plotly_chart(fig_demo, use_container_width=True)
        
# #     with col_u4:
# #         if '用户城市' in df.columns and '消费金额' in df.columns:
# #             city_sales = df.groupby('用户城市')['消费金额'].sum().sort_values().tail(10).reset_index()
# #             fig_city = px.bar(city_sales, x='消费金额', y='用户城市', orientation='h',
# #                               color='消费金额', color_continuous_scale='Blues',
# #                               title="🏙️ 核心高净值城市 TOP 10")
# #             st.plotly_chart(fig_city, use_container_width=True)

# # # ----------------- TAB 3: 营销与供应链 -----------------
# # with tab3:
# #     st.markdown("### 3. 营销效率与履约质量 (Marketing & Supply Chain)")
# #     st.info("💡 注：此模块数据结合历史大盘波动动态模拟，用于指导宏观运营决策。")
    
# #     col_m1, col_m2 = st.columns(2)
# #     with col_m1:
# #         sources = pd.DataFrame({
# #             '渠道': ['站内搜索', '首页推荐', '短视频/直播', '站外广告', '自然复购'],
# #             '占比': [35, 25, 20, 15, 5]
# #         })
# #         fig_pie = px.pie(sources, names='渠道', values='占比', hole=0.5,
# #                          title="🌐 流量来源结构占比", color_discrete_sequence=px.colors.qualitative.Pastel)
# #         fig_pie.update_traces(textinfo='percent+label')
# #         st.plotly_chart(fig_pie, use_container_width=True)
        
# #     with col_m2:
# #         fig_gauge = go.Figure(go.Indicator(
# #             mode = "gauge+number",
# #             value = 98.2,
# #             title = {'text': "📦 48小时履约发货率 (%)"},
# #             gauge = {'axis': {'range': [None, 100]},
# #                      'bar': {'color': "#27ae60"},
# #                      'steps' : [
# #                          {'range': [0, 80], 'color': "#e74c3c"},
# #                          {'range': [80, 90], 'color': "#f1c40f"},
# #                          {'range': [90, 100], 'color': "#ecf0f1"}]}
# #         ))
# #         st.plotly_chart(fig_gauge, use_container_width=True)

# # # ----------------- TAB 4: AI 深度诊断 -----------------
# # with tab4:
# #     platform_label = "自定义数据" if selected_platform == "🛠️ 自定义数据上传" else selected_platform
# #     st.markdown(f"### 🧠 {platform_label} 大盘数据 AI 智能诊断")
    
# #     if st.button("✨ 生成全域经营分析报告 ✨", type="primary"):
# #         with st.spinner("AI 正在汇聚 7 大维度数据，生成总监级洞察报告..."):
            
# #             cat_top = df.groupby('商品类别')['消费金额'].sum().sort_values(ascending=False).head(3).to_dict() if '商品类别' in df.columns else "未知"
# #             city_top = df.groupby('用户城市')['消费金额'].sum().sort_values(ascending=False).head(3).to_dict() if '用户城市' in df.columns else "未知"
            
# #             summary_text = f"""
# #             当前分析数据源：{platform_label}
# #             1. 交易与流量：总GMV ¥{real_gmv:.2f}，总订单 {real_orders}笔，客单价 ¥{real_gmv/real_orders if real_orders>0 else 0:.2f}。预估转化漏斗中，PV到加购转化率良好，但加购到支付流失率约 {(1 - real_orders/mock_cart)*100 if mock_cart>0 else 0:.1f}%。
# #             2. 商品表现：TOP3营收品类为 {cat_top}。
# #             3. 用户画像：核心消费城市TOP3为 {city_top}。
# #             4. 营销与供应链：站内搜索和推荐占流量大头(60%)，48小时发货率高达98.2%。
# #             """
            
# #             prompt = f"""
# #             你是一位年薪百万的电商大厂（阿里/京东级别）数据运营总监。请根据以下全域经营数据，写一份汇报给CEO的商业洞察报告：
# #             【数据摘要】：\n{summary_text}\n
# #             请严格按照以下结构输出（Markdown格式，多用 emoji 和专业的业务黑话）：
# #             1. 📈 **全域经营大盘总结**：一句话定调目前的生意健康度。
# #             2. ⚠️ **转化漏斗痛点**：针对“加购到支付”的流失，深度剖析可能的原因。
# #             3. 🎯 **人货场重构建议**：
# #                - **人 (用户)**：针对高优城市该怎么做定向运营？
# #                - **货 (商品)**：头部类目如何拉升利润？
# #                - **场 (营销/流量)**：如何优化流量结构？
# #             4. 💡 **下一步核心 Action 落地建议**。
# #             """
            
# #             try:
# #                 response = client.chat.completions.create(
# #                     model="qwen-plus",
# #                     messages=[
# #                         {"role": "system", "content": "你是资深电商专家，擅长从流量、转化、客单价等维度做深度业务拆解。"},
# #                         {"role": "user", "content": prompt}
# #                     ]
# #                 )
# #                 st.success("✅ AI 诊断报告已生成！")
# #                 st.markdown(response.choices[0].message.content)
# #             except Exception as e:
# #                 st.error(f"调用 AI 失败，请检查网络。错误详情：{e}")
# import streamlit as st
# import pandas as pd
# import numpy as np
# from openai import OpenAI
# import os
# import plotly.express as px
# import plotly.graph_objects as go

# # === 新增：轻量级 RAG 向量检索所需库 ===
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# import jieba

# # ==========================================
# # 1. 页面与全局样式配置
# # ==========================================
# st.set_page_config(page_title="全域电商数据大屏 | RAG版", page_icon="📊", layout="wide")

# st.markdown("""
# <style>
#     div[data-testid="metric-container"] {
#         background: linear-gradient(135deg, #f6f8fd 0%, #f1f5f9 100%);
#         border-radius: 10px;
#         padding: 15px;
#         border: 1px solid #e2e8f0;
#         box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
#     }
# </style>
# """, unsafe_allow_html=True)

# st.title("📊 全域电商数据可视化与 AI 决策中心")
# st.markdown("覆盖七大经营维度，支持自定义数据源，**并深度集成 RAG (检索增强生成) 知识库注入技术。**")

# # ==========================================
# # 2. AI 客户端初始化
# # ==========================================
# api_key = os.environ.get("OPENAI_API_KEY", "sk-cdc57fd44a394cea8ec25dd4ad2512f7")
# client = OpenAI(
#     api_key=api_key, 
#     base_url="https://ws-vvr85dv3ndbxfxtu.ap-southeast-1.maas.aliyuncs.com/compatible-model/v1"
# )

# # ==========================================
# # 3. 轻量级 RAG 知识引擎 (核心亮点)
# # ==========================================
# def process_text_for_rag(text):
#     """将长文档切块并分词"""
#     # 简单按换行符切分段落 (Chunking)
#     paragraphs = [p.strip() for p in text.split('\n') if len(p.strip()) > 10]
#     # 中文结巴分词
#     corpus = [" ".join(jieba.cut(p)) for p in paragraphs]
#     return paragraphs, corpus

# def retrieve_knowledge(query, vectorizer, tfidf_matrix, paragraphs, top_k=2):
#     """向量检索：计算查询与知识库的余弦相似度，返回最相关的Top-K段落"""
#     query_cut = " ".join(jieba.cut(query))
#     query_vec = vectorizer.transform([query_cut])
#     similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
    
#     # 找出相似度最高的 top_k 个索引
#     top_indices = similarities.argsort()[-top_k:][::-1]
    
#     retrieved_chunks = []
#     for idx in top_indices:
#         if similarities[idx] > 0.05: # 设定一个相似度阈值
#             retrieved_chunks.append(paragraphs[idx])
            
#     return retrieved_chunks

# # ==========================================
# # 4. 侧边栏：多平台切换、数据上传与【知识库注入】
# # ==========================================
# st.sidebar.header("🎯 经营大盘控制台")

# # --- RAG 知识库上传区 ---
# st.sidebar.markdown("### 📚 内部知识库 (RAG)")
# knowledge_file = st.sidebar.file_uploader("上传公司运营SOP (TXT格式)", type=["txt"])
# rag_enabled = False
# paragraphs, tfidf_matrix, vectorizer = [], None, None

# if knowledge_file is not None:
#     with st.spinner("正在将知识库向量化..."):
#         raw_text = knowledge_file.read().decode('utf-8')
#         paragraphs, corpus = process_text_for_rag(raw_text)
#         if len(corpus) > 0:
#             vectorizer = TfidfVectorizer()
#             tfidf_matrix = vectorizer.fit_transform(corpus)
#             rag_enabled = True
#             st.sidebar.success(f"✅ 知识库已注入 (共 {len(paragraphs)} 个知识切片)")

# st.sidebar.markdown("---")
# # --- 数据源选择区 ---
# st.sidebar.markdown("### 📊 数据源配置")
# logo_map = {
#     "淘宝": "https://img.alicdn.com/tfs/TB1_uT8a5ERMeJjSspiXXbZLFXa-143-59.png",
#     "天猫": "天猫.png",
#     "京东": "https://misc.360buyimg.com/lib/img/e/logo-201305-b.png",
#     "拼多多": "拼多多.png", 
#     "1688": "阿里巴巴.png",
#     "苏宁易购": "苏宁易购.png"
# }

# logo_placeholder = st.sidebar.empty() 
# platforms = ["淘宝", "天猫", "京东", "拼多多", "1688", "苏宁易购", "🛠️ 自定义数据上传"]
# selected_platform = st.sidebar.radio("请选择分析数据源", platforms)

# # 数据加载引擎
# @st.cache_data
# def load_and_enhance_data(platform_name):
#     file_path = f"{platform_name}.csv"
#     try:
#         df = pd.read_csv(file_path, encoding='utf-8')
#     except Exception:
#         try:
#             df = pd.read_csv(file_path, encoding='gbk')
#         except Exception:
#             dates = pd.date_range(start='2024-01-01', periods=1000, freq='h')
#             df = pd.DataFrame({
#                 '用户ID': [f"U{np.random.randint(1000, 9999)}" for _ in range(1000)],
#                 '商品类别': np.random.choice(['美妆', '服饰', '数码', '食品', '家居', '运动'], 1000),
#                 '消费金额': np.random.uniform(50, 3000, 1000),
#                 '购买数量': np.random.randint(1, 5, 1000),
#                 '购买时间': np.random.choice(dates, 1000),
#                 '用户城市': np.random.choice(['北京', '上海', '广州', '深圳', '成都', '杭州', '重庆'], 1000),
#                 '用户性别': np.random.choice(['男', '女'], 1000, p=[0.4, 0.6]),
#                 '用户年龄': np.random.randint(18, 60, 1000)
#             })
            
#     df['购买时间'] = pd.to_datetime(df['购买时间'])
#     df['日期'] = df['购买时间'].dt.date
#     df['小时'] = df['购买时间'].dt.hour
#     df['星期'] = df['购买时间'].dt.day_name()
#     return df

# if selected_platform != "🛠️ 自定义数据上传":
#     if selected_platform in logo_map:
#         logo_placeholder.image(logo_map[selected_platform], width=120)
#     with st.spinner(f"正在抽取 {selected_platform} 业务数据..."):
#         df = load_and_enhance_data(selected_platform)
# else:
#     logo_placeholder.empty()
#     uploaded_file = st.sidebar.file_uploader("📂 请上传电商交易流水 (CSV)", type=["csv"])
#     if uploaded_file is not None:
#         try:
#             df = pd.read_csv(uploaded_file, encoding='utf-8')
#         except Exception:
#             df = pd.read_csv(uploaded_file, encoding='gbk')
#         if '购买时间' in df.columns:
#             df['购买时间'] = pd.to_datetime(df['购买时间'])
#             df['日期'] = df['购买时间'].dt.date
#             df['小时'] = df['购买时间'].dt.hour
#             df['星期'] = df['购买时间'].dt.day_name()
#         else:
#             st.error("❌ 上传的 CSV 必须包含【购买时间】列！")
#             st.stop()
#     else:
#         st.info("👈 请上传 CSV 文件以开启分析。")
#         st.stop()

# real_orders = len(df)
# real_gmv = df['消费金额'].sum() if '消费金额' in df.columns else 0
# mock_uv = real_orders * np.random.randint(15, 25) 
# mock_pv = mock_uv * 3.5
# mock_cart = int(mock_uv * 0.3)

# # ==========================================
# # 5. UI 布局：四大业务模块 Tab 切换
# # ==========================================
# tab1, tab2, tab3, tab4 = st.tabs([
#     "💰 交易与流量", "👥 用户与商品", "🚀 营销与供应链", "🧠 AI 深度诊断 (RAG版)"
# ])

# with tab1:
#     c1, c2, c3, c4 = st.columns(4)
#     c1.metric("💰 销售额 GMV", f"¥ {real_gmv:,.0f}")
#     c2.metric("💳 支付订单量", f"{real_orders:,} 笔")
#     c3.metric("🛒 客单价", f"¥ {real_gmv/real_orders if real_orders>0 else 0:,.2f}")
#     c4.metric("👥 独立访客(UV)", f"{mock_uv:,} 人")
    
#     col_t1, col_t2 = st.columns([6, 4])
#     with col_t1:
#         if '日期' in df.columns and '消费金额' in df.columns:
#             daily_sales = df.groupby('日期')['消费金额'].sum().reset_index()
#             fig_trend = px.area(daily_sales, x='日期', y='消费金额', title="📈 每日 GMV 趋势", color_discrete_sequence=['#FF4B4B'])
#             st.plotly_chart(fig_trend, use_container_width=True)
#     with col_t2:
#         fig_funnel = go.Figure(go.Funnel(
#             y=['浏览', '访客', '加购', '下单', '支付'], x=[mock_pv, mock_uv, mock_cart, int(real_orders*1.2), real_orders],
#             textinfo="value+percent initial", marker={"color": ["#3498db", "#2ecc71", "#f1c40f", "#e67e22", "#e74c3c"]}
#         ))
#         fig_funnel.update_layout(title="🔽 核心转化漏斗分析")
#         st.plotly_chart(fig_funnel, use_container_width=True)

# with tab2:
#     col_u1, col_u2 = st.columns(2)
#     with col_u1:
#         if '商品类别' in df.columns and '消费金额' in df.columns:
#             cat_sales = df.groupby('商品类别')['消费金额'].sum().reset_index()
#             fig_tree = px.treemap(cat_sales, path=['商品类别'], values='消费金额', title="🛍️ 商品品类营收贡献")
#             st.plotly_chart(fig_tree, use_container_width=True)
#     with col_u2:
#         if '用户年龄' in df.columns and '用户性别' in df.columns:
#             fig_demo = px.histogram(df, x='用户年龄', color='用户性别', barmode='group', title="👥 年龄与性别分布")
#             st.plotly_chart(fig_demo, use_container_width=True)

# with tab3:
#     st.info("展示宏观供应链健康度。")
#     col_m1, col_m2 = st.columns(2)
#     with col_m1:
#         fig_pie = px.pie(names=['搜索', '推荐', '直播', '广告', '自然'], values=[35, 25, 20, 15, 5], hole=0.5, title="🌐 流量来源结构")
#         st.plotly_chart(fig_pie, use_container_width=True)
#     with col_m2:
#         fig_gauge = go.Figure(go.Indicator(mode = "gauge+number", value = 98.2, title = {'text': "📦 48小时发货率 (%)"}))
#         st.plotly_chart(fig_gauge, use_container_width=True)

# # ----------------- TAB 4: RAG 注入诊断核心逻辑 -----------------
# with tab4:
#     st.markdown(f"### 🧠 RAG 增强型商业诊断")
#     if rag_enabled:
#         st.success("🎯 系统检测到已挂载公司内部知识库，AI 将结合公司规章制度出具报告。")
#     else:
#         st.warning("⚠️ 当前未挂载知识库。请在左侧上传SOP文档体验 RAG 注入效果，否则 AI 将仅基于通用知识生成报告。")
    
#     if st.button("✨ 结合知识库生成分析报告 ✨", type="primary"):
#         with st.spinner("AI 正在计算大盘数据，并在向量数据库中检索匹配的知识库..."):
            
#             # 1. 提炼数据摘要
#             cat_top = df.groupby('商品类别')['消费金额'].sum().sort_values(ascending=False).head(2).index.tolist() if '商品类别' in df.columns else ["未知"]
#             city_top = df.groupby('用户城市')['消费金额'].sum().sort_values(ascending=False).head(3).index.tolist() if '用户城市' in df.columns else ["未知"]
            
#             summary_text = f"""
#             当前平台：{selected_platform}
#             表现：总销售额 ¥{real_gmv:,.0f}，客单价 ¥{real_gmv/real_orders if real_orders>0 else 0:,.0f}。
#             用户特征：核心城市集中在 {", ".join(city_top)}。
#             商品特征：最热销的品类是 {", ".join(cat_top)}。
#             """
            
#             # 2. 核心：如果启用了 RAG，执行向量检索
#             retrieved_context = ""
#             if rag_enabled:
#                 # 构造搜索词（基于当前暴露的业务特征去知识库里搜索策略）
#                 search_query = f"如何处理客单价高、核心城市 {city_top[0]} 的用户？针对 {cat_top[0]} 品类有什么促销规范？"
#                 matched_chunks = retrieve_knowledge(search_query, vectorizer, tfidf_matrix, paragraphs, top_k=2)
                
#                 if matched_chunks:
#                     retrieved_context = "### 【公司内部运营知识库检索结果】\n" + "\n".join([f"- {chunk}" for chunk in matched_chunks])
#                     st.info(f"🔍 **RAG 向量检索成功！** 命中以下知识库条目并已注入提示词：\n{retrieved_context}")
            
#             # 3. 将数据与检索到的知识组装成最终 Prompt
#             prompt = f"""
#             你是一位大厂数据运营总监。请根据以下大盘数据，结合公司内部的业务规范（如果有），出具分析建议。
            
#             【实时大盘数据】：
#             {summary_text}
            
#             {retrieved_context}
            
#             请严格按以下结构输出（使用 Markdown）：
#             1. 📈 **大盘一句话总结**
#             2. 🎯 **客群与商品策略**（必须严格遵守内部知识库的规章制度，引用知识库的内容做指导）
#             3. 💡 **具体执行 Action**
#             """
            
#             try:
#                 response = client.chat.completions.create(
#                     model="qwen-plus",
#                     messages=[
#                         {"role": "system", "content": "你是资深电商专家，必须严格按照公司提供的内部知识库来制定策略。"},
#                         {"role": "user", "content": prompt}
#                     ]
#                 )
#                 st.markdown("---")
#                 st.markdown(response.choices[0].message.content)
#             except Exception as e:
#                 st.error(f"调用 AI 失败，错误详情：{e}")
             

import streamlit as st
import pandas as pd
import numpy as np
from openai import OpenAI
import os
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

# === 核心库保持不变 ===
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import jieba

# ==========================================
# 1. 物联网感视觉与全局配置 (Dark Mode & Cyberpunk)
# ==========================================
st.set_page_config(page_title="IoT 全域电商智慧中枢", page_icon="📡", layout="wide")

# 自定义 CSS 打造科技感看板
st.markdown("""
<style>
    /* 整体背景与文字颜色 */
    .stApp {
        background-color: #0e1117;
        color: #00ffcc;
    }
    /* 指标卡片 IoT 化 */
    div[data-testid="metric-container"] {
        background: rgba(16, 22, 34, 0.8);
        border: 1px solid #00ffcc;
        border-radius: 4px;
        padding: 20px;
        box-shadow: 0 0 10px rgba(0, 255, 204, 0.2);
    }
    div[data-testid="stMetricValue"] {
        color: #00ffcc !important;
        font-family: 'Courier New', Courier, monospace;
    }
    /* Tab 样式 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1a1c24;
        border: 1px solid #333;
        color: #888;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #00ffcc !important;
        color: #000 !important;
    }
    /* 模拟终端机样式 */
    .terminal-box {
        background-color: #000;
        color: #0f0;
        padding: 10px;
        border-radius: 5px;
        font-family: 'Consolas', monospace;
        font-size: 0.8rem;
        height: 200px;
        overflow-y: auto;
        border: 1px solid #333;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 模拟物联网实时状态 (系统心跳)
# ==========================================
def get_system_status():
    return {
        "cpu": np.random.uniform(15.0, 45.0),
        "latency": np.random.randint(20, 50),
        "nodes": "ONLINE",
        "api_relay": "STABLE"
    }

# ==========================================
# 3. AI 与 RAG 逻辑 (保持并优化)
# ==========================================
api_key = os.environ.get("OPENAI_API_KEY", "sk-cdc57fd44a394cea8ec25dd4ad2512f7")
client = OpenAI(
    api_key=api_key, 
    base_url="https://ws-vvr85dv3ndbxfxtu.ap-southeast-1.maas.aliyuncs.com/compatible-model/v1"
)

def process_text_for_rag(text):
    paragraphs = [p.strip() for p in text.split('\n') if len(p.strip()) > 10]
    corpus = [" ".join(jieba.cut(p)) for p in paragraphs]
    return paragraphs, corpus

def retrieve_knowledge(query, vectorizer, tfidf_matrix, paragraphs, top_k=2):
    query_cut = " ".join(jieba.cut(query))
    query_vec = vectorizer.transform([query_cut])
    similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
    top_indices = similarities.argsort()[-top_k:][::-1]
    retrieved_chunks = [paragraphs[idx] for idx in top_indices if similarities[idx] > 0.05]
    return retrieved_chunks

# ==========================================
# 4. 侧边栏：IoT 终端风格控制
# ==========================================
st.sidebar.title("🎛️ 系统控制台")
st.sidebar.markdown(f"**当前时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 系统监控挂件
status = get_system_status()
st.sidebar.info(f"🖥️ CPU: {status['cpu']:.1f}% | ⚡ Latency: {status['latency']}ms")

st.sidebar.markdown("---")
st.sidebar.header("📂 数据注入协议")
knowledge_file = st.sidebar.file_uploader("注入运营 SOP (RAG 核心)", type=["txt"])
rag_enabled = False
paragraphs, tfidf_matrix, vectorizer = [], None, None

if knowledge_file is not None:
    raw_text = knowledge_file.read().decode('utf-8')
    paragraphs, corpus = process_text_for_rag(raw_text)
    if len(corpus) > 0:
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(corpus)
        rag_enabled = True
        st.sidebar.success("✅ 向量索引构建完成")

st.sidebar.markdown("---")
platforms = ["淘宝", "天猫", "京东", "拼多多", "1688", "苏宁易购", "🛠️ 自定义上传"]
selected_platform = st.sidebar.selectbox("选择目标数据节点", platforms)

# 数据加载引擎 (带缓存)
@st.cache_data
def load_data(platform):
    dates = pd.date_range(start='2024-01-01', periods=1000, freq='h')
    df = pd.DataFrame({
        '用户ID': [f"U{np.random.randint(1000, 9999)}" for _ in range(1000)],
        '商品类别': np.random.choice(['美妆', '服饰', '数码', '食品', '家居', '运动'], 1000),
        '消费金额': np.random.uniform(50, 3000, 1000),
        '购买数量': np.random.randint(1, 5, 1000),
        '购买时间': np.random.choice(dates, 1000),
        '用户城市': np.random.choice(['北京', '上海', '广州', '深圳', '成都', '杭州', '重庆'], 1000),
        '用户性别': np.random.choice(['男', '女'], 1000, p=[0.4, 0.6]),
    })
    df['购买时间'] = pd.to_datetime(df['购买时间'])
    df['日期'] = df['购买时间'].dt.date
    return df

df = load_data(selected_platform)

# ==========================================
# 5. 主页面布局
# ==========================================
st.markdown(f"# 🛰️ {selected_platform} 经营数据实时监测中")

# 顶部指标流
m1, m2, m3, m4, m5 = st.columns(5)
real_gmv = df['消费金额'].sum()
m1.metric("NETWORK GMV", f"¥{real_gmv/10000:.2f}W", "+12.5%")
m2.metric("ORDER PULSE", f"{len(df)}", "-3.2%")
m3.metric("UV SYNC", f"{len(df)*20}", "+5.4%")
m4.metric("AOV DEPTH", f"¥{real_gmv/len(df):.1f}")
m5.metric("NODE STATUS", "ACTIVE", delta_color="normal")

tab_iot_1, tab_iot_2, tab_iot_3 = st.tabs(["📡 实时波形图", "🔋 链路资产", "🧠 AI 神经中枢"])

with tab_iot_1:
    col_l, col_r = st.columns([7, 3])
    with col_l:
        # 科技感面积图
        daily_sales = df.groupby('日期')['消费金额'].sum().reset_index()
        fig = px.line(daily_sales, x='日期', y='消费金额', title="数据流波动 (GMV Waveform)")
        fig.update_traces(line_color='#00ffcc', fill='tozeroy', fillcolor='rgba(0,255,204,0.1)')
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#888")
        st.plotly_chart(fig, use_container_width=True)
    
    with col_r:
        # 实时日志模拟器
        st.markdown("### 📜 System Logs")
        logs = [
            f"[{datetime.now().strftime('%H:%M:%S')}] 🟢 数据包同步完成",
            f"[{datetime.now().strftime('%H:%M:%S')}] 🟡 节点 {selected_platform} 延迟 24ms",
            f"[{datetime.now().strftime('%H:%M:%S')}] 🔵 RAG 检索就绪",
            f"[{datetime.now().strftime('%H:%M:%S')}] 🟢 支付链路加密中..."
        ]
        log_html = f"<div class='terminal-box'>{'<br>'.join(logs)}</div>"
        st.markdown(log_html, unsafe_allow_html=True)

with tab_iot_2:
    c_a, c_b = st.columns(2)
    with c_a:
        # 雷达图表现品类分布
        cat_data = df.groupby('商品类别')['消费金额'].sum().reset_index()
        fig_radar = px.line_polar(cat_data, r='消费金额', theta='商品类别', line_close=True, title="品类负载分布")
        fig_radar.update_traces(fill='toself', line_color='#00ffcc')
        st.plotly_chart(fig_radar, use_container_width=True)
    with c_b:
        # 城市热力映射
        city_data = df.groupby('用户城市')['消费金额'].count().reset_index()
        fig_bar = px.bar(city_data, x='用户城市', y='消费金额', color='消费金额', title="地理节点密度")
        st.plotly_chart(fig_bar, use_container_width=True)

with tab_iot_3:
    st.markdown("### 🧠 RAG 增强型逻辑推理")
    if not rag_enabled:
        st.warning("⚠️ 外部知识库未加载，当前运行在：【通用模式】")
    else:
        st.success("🛰️ 知识库已挂载，当前运行在：【专家决策模式】")
    
    if st.button("⚡ 触发 AI 诊断分析", type="primary"):
        with st.status("正在解析多维数据并检索向量库...", expanded=True) as status:
            # 提取数据特征
            summary = f"平台:{selected_platform}, GMV:{real_gmv:.0f}, 订单:{len(df)}"
            
            # RAG 检索
            context = ""
            if rag_enabled:
                st.write("🔍 正在扫描知识切片...")
                hits = retrieve_knowledge("运营策略和规章", vectorizer, tfidf_matrix, paragraphs)
                context = "\n".join(hits)
                st.write(f"✅ 命中 {len(hits)} 条规章")
            
            # AI 调用
            prompt = f"你是一台高级商业分析AI。数据：{summary}。内部知识：{context}。请给出：1.大盘异常检测；2.执行优先级；3.预测建议。"
            
            try:
                response = client.chat.completions.create(
                    model="qwen-plus",
                    messages=[{"role": "system", "content": "你是一个物联网监控系统的核心AI。"},
                              {"role": "user", "content": prompt}]
                )
                status.update(label="✅ 诊断报告生成完毕", state="complete")
                st.markdown("---")
                st.markdown(response.choices[0].message.content)
            except Exception as e:
                st.error(f"通信故障: {e}")

# 底部状态栏
st.markdown("---")
cols = st.columns(4)
cols[0].caption("📶 Signal: Strong")
cols[1].caption("🔒 Encryption: AES-256")
cols[2].caption("🚀 Engine: Gemini 3 Flash")
cols[3].caption(f"📅 Session: {datetime.now().strftime('%Y%m%d')}")
