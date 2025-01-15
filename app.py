import streamlit as st
from streamlit_extras.colored_header import colored_header
import graphviz
import tempfile
from datetime import datetime

# 设置页面配置
st.set_page_config(
    page_title="DFD Generator Pro",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
    <style>
        .main-title {
            color: #1E88E5;
            font-size: 2.5rem !important;
            font-weight: bold;
            text-align: center;
            margin-bottom: 2rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        .sub-title {
            color: #43A047;
            font-size: 1.5rem !important;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        .info-box {
            padding: 1rem;
            border-radius: 10px;
            background-color: #E3F2FD;
            border-left: 5px solid #1E88E5;
            margin: 1rem 0;
        }
        .success-box {
            padding: 1rem;
            border-radius: 10px;
            background-color: #E8F5E9;
            border-left: 5px solid #43A047;
            margin: 1rem 0;
        }
        .stButton>button {
            background-color: #1E88E5;
            color: white;
            font-weight: bold;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            border: none;
            box-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        .stButton>button:hover {
            background-color: #1976D2;
            transform: translateY(-2px);
            transition: all 0.3s ease;
        }
        .stSelectbox {
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# 模拟数据
MOCK_DATA = {
    "branches": ["main", "develop", "feature/dfd-1", "feature/dfd-2"],
    "mrs": [
        {"title": "DFD: 用户登录流程", "id": 1, "branch": "feature/dfd-1"},
        {"title": "DFD: 支付流程", "id": 2, "branch": "feature/dfd-1"},
        {"title": "DFD: 订单处理", "id": 3, "branch": "feature/dfd-2"},
    ],
    "files": {
        1: ["login/auth.py", "login/validate.py", "login/user.py"],
        2: ["payment/pay.py", "payment/callback.py"],
        3: ["order/process.py", "order/status.py"]
    }
}

class MockDFDConverter:
    @staticmethod
    def convert_to_flowchart(file_path):
        # 创建示例流程图
        dot = graphviz.Digraph(comment='示例流程图')
        dot.attr(rankdir='TB')
        
        # 根据不同文件生成不同的示例图
        if "login" in file_path:
            dot.node('A', '开始')
            dot.node('B', '输入用户名密码')
            dot.node('C', '验证信息')
            dot.node('D', '登录成功')
            dot.node('E', '登录失败')
            
            dot.edge('A', 'B')
            dot.edge('B', 'C')
            dot.edge('C', 'D')
            dot.edge('C', 'E')
            
        elif "payment" in file_path:
            dot.node('A', '选择支付方式')
            dot.node('B', '创建订单')
            dot.node('C', '发起支付')
            dot.node('D', '支付完成')
            
            dot.edge('A', 'B')
            dot.edge('B', 'C')
            dot.edge('C', 'D')
            
        else:
            dot.node('A', '开始')
            dot.node('B', '处理中')
            dot.node('C', '结束')
            
            dot.edge('A', 'B')
            dot.edge('B', 'C')
        
        return dot

def main():
    # 侧边栏
    with st.sidebar:
        colored_header(
            label="DFD Generator",
            description="流程图生成工具",
            color_name="blue-70"
        )
        
        # 开始按钮
        if st.button("🚀 开始生成", use_container_width=True):
            st.session_state.started = True
        
        # 添加提示框
        st.markdown("""
            <div class="success-box">
                <p style='margin: 0; text-align: center;'>
                    ✨ 点击上方按钮开始生成流程图
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # 分支选择
        st.markdown('<p class="sub-title">📁 选择分支</p>', unsafe_allow_html=True)
        selected_branch = st.selectbox(
            "可用分支列表",
            MOCK_DATA["branches"]
        )
        
        # MR 选择
        if selected_branch:
            st.markdown('<p class="sub-title">🔄 选择 MR</p>', unsafe_allow_html=True)
            mrs = [mr["title"] for mr in MOCK_DATA["mrs"]]
            selected_mr = st.selectbox("可用 MR 列表", mrs)
            
            if selected_mr:
                selected_mr_id = next(
                    mr["id"] for mr in MOCK_DATA["mrs"] 
                    if mr["title"] == selected_mr
                )
                st.session_state.current_mr_id = selected_mr_id
    
    # 主界面
    if 'started' in st.session_state and st.session_state.started:
        left_col, right_col = st.columns(2)
        
        with left_col:
            colored_header(
                label="🚀 文件选择",
                description="选择要转换的文件",
                color_name="blue-70"
            )
            
            if 'current_mr_id' in st.session_state:
                files = MOCK_DATA["files"][st.session_state.current_mr_id]

                selected_file = st.selectbox(" ✨ 文件列表", files)
                
                if selected_file:
                    st.session_state.current_file = selected_file
        
        with right_col:
            colored_header(
                label="流程图生成",
                description="生成并预览流程图",
                color_name="green-70"
            )
            
            if st.button("✨ 生成流程图", use_container_width=True) and 'current_file' in st.session_state:
                try:
                    with st.spinner('🔄 正在生成流程图...'):
                        converter = MockDFDConverter()
                        flowchart = converter.convert_to_flowchart(st.session_state.current_file)
                        
                        with tempfile.NamedTemporaryFile(suffix='.png') as tmp:
                            flowchart.render(tmp.name, format='png', cleanup=True)
                            st.markdown("""
                                <div class="success-box">
                                    <p style='margin: 0; text-align: center;'>✅ 流程图生成成功！</p>
                                </div>
                            """, unsafe_allow_html=True)
                            st.image(f"{tmp.name}.png")
                            
                except Exception as e:
                    st.error(f"❌ 生成流程图时出错: {str(e)}")

if __name__ == "__main__":
    main()