import streamlit as st

st.set_page_config(page_title="EE-Learning", page_icon="", layout="wide")

# ── 全量 CSS 注入 ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.stApp { font-family: 'Inter', system-ui, sans-serif !important; }
.block-container { padding-top: 2rem !important; padding-bottom: 1rem !important; max-width: 1000px !important; }
section[data-testid="stMain"] { background: #f8fafc !important; }
html { font-size: 15.5px; }
[data-testid="stHeader"] { background: #f8fafc !important; }
[data-testid="stToolbar"] { display: none !important; }
#MainMenu { display: none !important; }
footer { display: none !important; }

/* ── 顶级 Tab 栏 (st.tabs 第一层) ── */
.stTabs:first-of-type [data-baseweb="tab-list"] {
    gap: 0 !important; background: #fff !important; border-bottom: 1px solid #e2e8f0 !important;
    padding: 0 !important;
}
.stTabs:first-of-type [data-baseweb="tab"] {
    border-radius: 0 !important; padding: 14px 28px !important;
    font-size: 1rem !important; font-weight: 500 !important; color: #64748b !important;
    background: transparent !important; border: none !important;
    border-bottom: 3px solid transparent !important;
}
.stTabs:first-of-type [aria-selected="true"] {
    color: #0f172a !important; border-bottom: 3px solid #3b82f6 !important;
    font-weight: 600 !important; background: #fff !important;
}

/* ── 子 Tab 栏 (嵌套的 st.tabs) ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0 !important; background: transparent !important; border-bottom: 1px solid #e2e8f0 !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 0 !important; padding: 10px 18px !important;
    font-size: 0.92rem !important; font-weight: 500 !important; color: #64748b !important;
    background: transparent !important; border: none !important;
    border-bottom: 2px solid transparent !important;
}
.stTabs [aria-selected="true"] {
    color: #0f172a !important; border-bottom: 2px solid #3b82f6 !important;
    font-weight: 600 !important; background: transparent !important;
}

/* ── 展开器 ── */
.stExpander {
    border: 1px solid #e2e8f0 !important; border-left: 3px solid #e2e8f0 !important;
    border-radius: 8px !important; margin-bottom: 6px !important;
    background: #ffffff !important; box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
}
.stExpander:hover {
    border-left-color: #3b82f6 !important;
    box-shadow: 0 2px 8px rgba(59,130,246,0.08) !important;
}
.stExpander summary {
    font-size: 0.98rem !important; font-weight: 500 !important; color: #1e293b !important;
    padding: 0.7rem 1rem !important;
}
.stExpander div[data-testid="stExpander"] p {
    font-size: 0.95rem !important; line-height: 1.8 !important; color: #475569 !important;
}

/* ── 子标题 ── */
.sub-header {
    font-size: 0.88rem; font-weight: 600; color: #64748b;
    text-transform: uppercase; letter-spacing: 0.06em;
    padding-bottom: 6px; margin-bottom: 12px; border-bottom: 1px solid #e2e8f0;
}

/* ── 按钮 ── */
.stButton > button {
    border-radius: 8px !important; border: 1px solid #e2e8f0 !important;
    background: #ffffff !important; color: #1e293b !important;
    font-weight: 500 !important; text-align: left !important;
    padding: 0.75rem 1rem !important; box-shadow: 0 1px 2px rgba(0,0,0,0.04) !important;
}
.stButton > button:hover {
    border-color: #3b82f6 !important; background: #f0f7ff !important;
}

.stAlert { border-radius: 8px !important; font-size: 0.9rem !important; border-left-width: 3px !important; }

.footer-line {
    text-align: center; padding: 1rem 0; margin-top: 2rem;
    border-top: 1px solid #e2e8f0; color: #94a3b8; font-size: 0.82rem;
}

/* ── 公式区 ── */
.formula-box {
    background: #f1f5f9; border-left: 3px solid #3b82f6; border-radius: 6px;
    padding: 12px 16px; margin: 8px 0; font-size: 0.93rem;
    text-align: center; color: #0f172a; line-height: 1.8;
    font-family: 'Inter', monospace;
}

</style>
""", unsafe_allow_html=True)


def _clean_latex(text: str) -> str:
    """将 LaTeX 公式转为可读纯文本（纯字符串操作，无正则）"""
    # 统一双反斜杠为单反斜杠
    while '\\\\' in text:
        text = text.replace('\\\\', '\\')
    # \frac{a}{b} → (a)/(b)
    while '\\frac{' in text:
        i = text.find('\\frac{')
        if i < 0: break
        # 找到第一个 }
        j = text.find('}', i + 6)
        if j < 0: break
        num = text[i+6:j]
        # 找到第二个 \frac{ 后的 }
        k = text.find('\\frac{', j+1)
        # 也可能直接是 }
        if k < 0 or k > j + 10:
            # 可能是 }{b} 格式
            if text[j+1] == '{':
                m = text.find('}', j+2)
                if m < 0: break
                den = text[j+2:m]
                text = text[:i] + f'({num})/({den})' + text[m+1:]
            else:
                break
        else:
            # 找 }{b} 模式
            brace_start = text.find('{', j)
            if brace_start == j + 1:
                brace_end = text.find('}', brace_start)
                if brace_end < 0: break
                den = text[brace_start+1:brace_end]
                text = text[:i] + f'({num})/({den})' + text[brace_end+1:]
            else:
                break
    # \sqrt{a} → √(a)
    while '\\sqrt{' in text:
        i = text.find('\\sqrt{')
        if i < 0: break
        j = text.find('}', i + 6)
        if j < 0: break
        inner = text[i+6:j]
        text = text[:i] + f'√({inner})' + text[j+1:]
    # 希腊字母和数学符号
    for s, r in [('\\sum','Σ'),('\\prod','Π'),('\\int','∫'),('\\oint','∮'),
        ('\\infty','∞'),('\\pi','π'),('\\omega','ω'),('\\zeta','ζ'),
        ('\\alpha','α'),('\\beta','β'),('\\gamma','γ'),('\\delta','δ'),
        ('\\theta','θ'),('\\phi','φ'),('\\sigma','σ'),('\\mu','μ'),
        ('\\tau','τ'),('\\lambda','λ'),('\\Delta','Δ'),
        ('\\angle','∠'),('\\circ','°'),('\\cdot','·'),('\\times','×'),
        ('\\pm','±'),('\\leq','≤'),('\\geq','≥'),('\\neq','≠'),
        ('\\approx','≈'),('\\rightarrow','→'),('\\Rightarrow','⇒'),
        ('\\cdots','⋯'),('\\ldots','…'),('\\mathcal{L}','ℒ'),
        ('\\sin','sin'),('\\cos','cos'),('\\tan','tan'),
        ('\\log','log'),('\\lim','lim'),('\\lg','lg'),
        ('\\text{',''),('\\mathrm{',''),('\\mathbf{','')]:
        text = text.replace(s, r)
    # \dot{x} → ·x
    while '\\dot{' in text:
        i = text.find('\\dot{')
        j = text.find('}', i + 5)
        if j < 0: break
        text = text[:i] + '·' + text[i+5:j] + text[j+1:]
    # 括号清理
    for old, new in [('\\left(','('),('\\right)',')'),('\\left[','['),('\\right]',']'),
                     ('\\{','{'),('\\}','}')]:
        text = text.replace(old, new)
    # 去掉 $
    text = text.replace('$', '')
    # 清理所有剩余反斜杠
    text = text.replace('\\', '')
    # _{abc} → 下标  ^{abc} → 上标
    sub_map = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')
    sup_map = str.maketrans('0123456789+-=()nikj', '⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿⁱᵏʲ')
    while '_{' in text:
        i = text.find('_{')
        j = text.find('}', i + 2)
        if j < 0: break
        inner = text[i+2:j]
        text = text[:i] + inner.translate(sub_map) + text[j+1:]
    while '^{' in text:
        i = text.find('^{')
        j = text.find('}', i + 2)
        if j < 0: break
        inner = text[i+2:j]
        text = text[:i] + inner.translate(sup_map) + text[j+1:]
    # 单字符 _x 和 ^x
    result = []
    i = 0
    while i < len(text):
        if text[i] == '_' and i+1 < len(text) and text[i+1].isalnum():
            result.append(text[i+1].translate(sub_map))
            i += 2
        elif text[i] == '^' and i+1 < len(text) and text[i+1].isalnum():
            result.append(text[i+1].translate(sup_map))
            i += 2
        else:
            result.append(text[i])
            i += 1
    text = ''.join(result)
    # 清理残余花括号和 HTML 实体
    text = text.replace('{', '').replace('}', '')
    text = text.replace('&emsp;', '    ').replace('&nbsp;', ' ')
    return text.strip()


def knowledge_section(title: str, items: list[tuple[str, str, str]]):
    """渲染一个知识板块。items = [(标题, 解释, 公式), ...]"""
    st.markdown(f'<div class="sub-header">{title}</div>', unsafe_allow_html=True)
    for name, desc, formula in items:
        with st.expander(name, expanded=False):
            st.markdown(f'<div style="font-size:0.95rem; line-height:1.8; color:#475569;">{_clean_latex(desc)}</div>',
                        unsafe_allow_html=True)
            if formula:
                st.markdown(f'<div class="formula-box">{_clean_latex(formula)}</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
#  数据
# ════════════════════════════════════════════════════════════════════

CIRCUIT_THEORY = [
    ("1. 基尔霍夫定律 (KCL / KVL)",
     """想象你站在一个十字路口，四条路上的人同时进出。如果进来了10个人，出去了也必须是10个人——这就是**基尔霍夫电流定律 (KCL)** 的直觉：对于任意一个节点，流入的电流总和等于流出的电流总和。KCL的本质是电荷守恒。

**基尔霍夫电压定律 (KVL)** 说：沿着电路中的任何一条闭合回路走一圈，电压的升降总和为零，就像你绕操场跑一圈，海拔的上升和下降总和为零。KVL的本质是能量守恒。

KCL和KVL是整个电路理论的公理体系，所有后续的分析方法——支路电流法、网孔法、节点法——都建立在这两个定律之上。""",
     "KCL: $\\sum_{k=1}^{n} i_k = 0$ &emsp; KVL: $\\sum_{k=1}^{n} v_k = 0$"),

    ("2. 电阻串并联与等效变换",
     """电阻串联就像几个人手拉手排成一列过独木桥——通行难度是各段之和。并联则像多条平行的桥同时供你选择，等效电阻反而比最小的单条桥还小。串联电路中电流处处相同，各电阻按阻值比例分担总电压（分压原理）；并联电路中各支路电压相同，各电阻按阻值反比分配总电流（分流原理）。

实际电路中常出现混联电路，需要从内向外逐步化简——层层剥洋葱直到整个电路化为一个等效电阻。掌握等效化简是分析复杂电路的第一步，也是理解"等效"这一工程思想的起点。""",
     "串联: $R_{eq} = R_1 + R_2 + \\cdots + R_6$ &emsp; 并联: $\\frac{1}{R_{eq}} = \\frac{1}{R_1} + \\frac{1}{R_2} + \\cdots + \\frac{1}{R_n}$"),

    ("3. 支路电流法、网孔法与节点法",
     """面对复杂电路，**支路电流法**把每条支路的电流都设为未知数，对每个节点列KCL、每个回路列KVL。假设电路有 $b$ 条支路、$n$ 个节点，则需要 $b$ 个方程。

**网孔电流法**假设每个网孔有一个虚拟的"网孔电流"，未知数从 $b$ 个降为网孔个数 $m = b - (n-1)$，方程数大幅减少。**节点电压法**选定参考节点，对其余每个节点列KCL方程——当电路支路多但节点少时效率远高于网孔法。这是SPICE等电路仿真软件的核心算法基础。""",
     "网孔法: $\\mathbf{R}\\mathbf{i}_m = \\mathbf{v}_s$ &emsp; 节点法: $\\mathbf{Y}_n \\mathbf{V}_n = \\mathbf{I}_s$"),

    ("4. 戴维南定理与诺顿定理",
     """面对一台被黑箱封住的复杂电路，你不需要知道里面是什么——只需测量两个端口的**开路电压** $V_{oc}$ 和**等效电阻** $R_{th}$，就能用一个电压源串联一个电阻完全替代它。这就是**戴维南定理**。

对偶地，**诺顿定理**说同一个黑箱也可以等效为一个电流源并联同一个电阻。当负载电阻等于 $R_{th}$ 时，负载获得最大功率——这是阻抗匹配的理论基础。""",
     "$V_{th} = V_{oc}$, $R_{th} = \\frac{V_{oc}}{I_{sc}}$ &emsp; 最大功率: $P_{max} = \\frac{V_{th}^2}{4R_{th}}$"),

    ("5. 正弦稳态与相量法",
     """交流电的电压和电流随时间做正弦振荡。直接用三角函数运算非常繁琐，我们引入**相量法**——把正弦量映射到复平面上的一个旋转向量，用复数的代数运算代替微积分运算。

在相量域中，电容的伏安关系从微分方程变成 $\\dot{I}=j\\omega C\\dot{V}$，电感变成 $\\dot{V}=j\\omega L\\dot{I}$。由此引入**阻抗**的概念：$Z_R=R$，$Z_C=\\frac{1}{j\\omega C}$，$Z_L=j\\omega L$。有了阻抗，交流电路的分析完全转化为"复数版的直流电路"。""",
     "$v(t) = V_m \\cos(\\omega t + \\phi) \\longleftrightarrow \\dot{V} = V_m\\angle\\phi$"),

    ("6. 一阶 RC / RL 电路时域分析",
     """给手机充电时，电池电量不是瞬间充满而是逐渐上升——RC电路的充电过程完全类似。时间常数 $\\tau = RC$ 就是"充到63.2%需要多久"的度量。$5\\tau$ 后过渡过程基本结束。

RL电路中电感阻碍电流变化，就像一个沉重的飞轮，电流从零开始逐渐增大。掌握**"三要素法"**——找到初始值 $x(0^+)$、稳态值 $x(\\infty)$ 和时间常数 $\\tau$，直接套公式即可免去求解微分方程。""",
     "全响应: $x(t) = x(\\infty) + [x(0^+) - x(\\infty)]e^{-t/\\tau}$"),

    ("7. 二阶 RLC 电路",
     """当电路同时包含电容和电感时，能量在两者之间来回交换，电阻不断消耗，系统响应有三种模式：**过阻尼**（像在蜂蜜中运动的弹簧）、**欠阻尼**（衰减振荡，像被拨动的音叉）、**临界阻尼**（最快回到平衡且不振荡）。

工程师需要通过特征方程的根来判断响应类型，这直接决定了滤波器的截止特性和控制系统的稳定性。""",
     "串联RLC: $\\alpha=\\frac{R}{2L}$, $\\omega_0=\\frac{1}{\\sqrt{LC}}$"),

    ("8. 正弦稳态功率分析",
     """在交流电路中，电压和电流之间可能存在相位差，使得"瞬时功率"忽正忽负。**有功功率** $P$ 是净吸收的能量速率，**无功功率** $Q$ 是能量在电源和储能元件之间来回搬运的速率，**视在功率** $S=VI$ 是电压电流有效值的乘积。

功率因数 $\\cos\\varphi=P/S$ 衡量了"有多少视在功率转化为了有功功率"。工业中常并联电容器进行**功率因数校正**，用电容的容性无功抵消电动机的感性无功。""",
     "$P = VI\\cos\\varphi$, $Q = VI\\sin\\varphi$, $S = \\sqrt{P^2+Q^2}$"),

    ("9. 互感与变压器",
     """两个靠近的线圈，当其中一个电流变化时，变化的磁场会在另一个中感应出电压——这就是**互感**。理想变压器的核心关系：电压比等于匝数比，电流比等于匝数反比，阻抗变换。

变压器是电力系统的核心设备——发电厂发出的电经升压变压器提高电压降低线路损耗，到达用户端再经降压变压器降至安全电压。""",
     "$\\frac{v_1}{v_2}=\\frac{N_1}{N_2}$, $Z_{in}=\\left(\\frac{N_1}{N_2}\\right)^2 Z_L$"),

    ("10. 频率响应与谐振",
     """收音机选台就是一个频率选择过程——内部的**谐振电路**充当"频率过滤器"。串联RLC谐振时感抗和容抗恰好抵消，电流达到最大值。品质因数 $Q$ 衡量了谐振的"尖锐程度"，$Q$ 值越高，频率选择性越好。

根据频率响应，电路可分为低通、高通、带通、带阻等类型，这是信号处理和通信系统设计的基础。""",
     "$\\omega_0=\\frac{1}{\\sqrt{LC}}$, $Q=\\frac{\\omega_0 L}{R}$, $BW=\\frac{f_0}{Q}$"),

    ("11. 三相电路基础",
     """工业用电常用三相电，三股相差120°的水流同时推动涡轮机，总功率恒定不变、运转平稳。Y接时线电压等于相电压的 $\\sqrt{3}$ 倍，Δ接时线电流等于相电流的 $\\sqrt{3}$ 倍。

三相系统最核心的优势：对称三相负载的总瞬时功率为常数，电动机转矩无脉动。此外三相输电只需三根导线即可传输同等功率，节省约25%导线材料。""",
     "$V_L = \\sqrt{3}V_P$ (Y接), $P = \\sqrt{3}V_L I_L\\cos\\varphi$"),

    ("12. 非正弦周期电路与傅里叶分析",
     """任何周期信号都可以分解为一系列不同频率的正弦波之和——就像白光可以被棱镜分解为彩虹。**谐波分析法**：①将激励源做傅里叶展开；②对每个频率分量分别用相量法求解；③叠加得到总响应。

非正弦周期量的有效值 $V_{rms}=\\sqrt{V_0^2+\\sum V_{n,rms}^2}$，功率也需要对各次谐波分别计算再求和。""",
     "$f(t)=\\frac{a_0}{2}+\\sum_{n=1}^{\\infty}[a_n\\cos(n\\omega_0 t)+b_n\\sin(n\\omega_0 t)]$"),

    ("13. 拉普拉斯变换与电路的 s 域分析",
     """拉普拉斯变换将微分方程翻译成代数方程——微分变成乘以 $s$，积分变成除以 $s$。在s域中，电路元件的伏安关系变得极其对称，初始条件被自动包含在等效电路中。

通过分析网络函数 $H(s)$ 的极点和零点，可以判断系统稳定性、瞬态响应特性和频率响应——这是从电路分析过渡到信号与系统、自动控制理论的桥梁。""",
     "$Z_R=R$, $Z_L=sL$, $Z_C=\\frac{1}{sC}$ &emsp; $H(s)=\\frac{Y(s)}{X(s)}$"),
]

ENGINEERING_MATH = [
    ("1. 复数与相量运算",
     """复数是电气工程师的"万能钥匙"。$z = a + jb$（工程中用 $j$ 代替 $i$）可看作复平面上的向量。两个复数相乘，模相乘、角度相加——这正是交流电路中幅值缩放和相位移动的数学本质。

欧拉公式 $e^{j\\theta}=\\cos\\theta+j\\sin\\theta$ 将指数函数与三角函数统一，被誉为"最美的数学公式"。共轭复数 $z\\cdot z^*=|z|^2$ 在功率计算中常用。""",
     "$z = a + jb = r e^{j\\theta} = r\\angle\\theta$, $|z|=\\sqrt{a^2+b^2}$"),

    ("2. 一阶 / 二阶微分方程",
     """一阶方程描述RC/RL电路的指数充放电过程。通解由齐次解和特解组成。

二阶方程出现在RLC电路中：过阻尼（两不等负实根）、欠阻尼（共轭复根，衰减振荡）、临界阻尼（两相等负实根，最快无振荡回到平衡）。判别式 $\\Delta = a_1^2 - 4a_0 a_2$ 决定响应类型。""",
     "特征根: $s_{1,2}=\\frac{-a_1 \\pm \\sqrt{a_1^2-4a_0 a_2}}{2a_2}$"),

    ("3. 矩阵与线性方程组",
     """分析复杂电路时会得到一组线性方程。矩阵提供高效、标准化的求解流程。在计算机时代，大型电路的分析完全依赖矩阵的稀疏存储和数值求解算法。特征值和特征向量决定了系统的固有频率和振型。""",
     "$\\mathbf{A}\\mathbf{x}=\\mathbf{b} \\Rightarrow \\mathbf{x}=\\mathbf{A}^{-1}\\mathbf{b}$, $|\\mathbf{A}-\\lambda\\mathbf{I}|=0$"),

    ("4. 傅里叶级数与傅里叶变换",
     """傅里叶级数将周期信号分解为正弦分量之和。有三角形式、指数形式和振幅-相位形式三种等价表示。系数衰减速度反映信号光滑程度。

傅里叶变换 $F(\\omega)=\\int f(t)e^{-j\\omega t}dt$ 将非周期信号从时域直接映射到频域，是信号处理的核心工具。""",
     "$F(\\omega)=\\int_{-\\infty}^{\\infty}f(t)e^{-j\\omega t}dt$"),

    ("5. 拉普拉斯变换",
     """拉普拉斯变换是傅里叶变换的推广，引入复频率 $s=\\sigma+j\\omega$。微分变乘法、积分变除法、卷积变乘积。它自动包含初始条件，是求解线性微分方程的最强大工具。

常用变换对：$e^{-at}\\leftrightarrow\\frac{1}{s+a}$, $\\sin\\omega t\\leftrightarrow\\frac{\\omega}{s^2+\\omega^2}$。部分分式展开是求逆变换的关键技巧。""",
     "$\\mathcal{L}\\{f'(t)\\}=sF(s)-f(0^-)$, $\\mathcal{L}\\{e^{-at}\\}=\\frac{1}{s+a}$"),

    ("6. 留数定理与复变函数基础",
     """留数定理：$\\oint_C f(z)dz = 2\\pi j\\sum\\text{Res}[f(z),z_k]$。围道积分的值只取决于曲线内部的奇点。

在电气工程中直接用于：拉普拉斯逆变换、频率响应分析、电磁场边值问题。一阶极点留数 $\\text{Res}[f(z),z_0]=\\lim_{z\\to z_0}(z-z_0)f(z)$。""",
     "$\\oint_C f(z)dz=2\\pi j\\sum_{k=1}^{n}\\text{Res}[f(z),z_k]$"),

    ("7. 常用积分变换对比与应用",
     """傅里叶变换分析稳态频率特性，拉普拉斯变换分析连续系统瞬态和稳定性，Z变换分析离散系统。三者核心思想一致：将时域复杂运算转化为频域简单乘法。

关系：令 $s=j\\omega$ 得傅里叶变换，令 $z=e^{sT}$ 得Z变换。""",
     "傅里叶: $s=j\\omega$; 拉普拉斯: $s=\\sigma+j\\omega$; Z变换: $z=e^{sT}$"),
]

ANALOG_ELECTRONICS = [
    ("1. PN结与二极管",
     """PN结是所有半导体器件的基础。P型和N型半导体接触后，扩散和漂移达到动态平衡形成耗尽层。正向偏压削弱内建电场，电流导通（硅管约0.7V导通）；反向偏压截止，直到击穿电压。

三种常用模型：**理想模型**（导通短路/截止开路）、**恒压降模型**（0.7V压降）、**小信号模型**（动态电阻 $r_d=26\\text{mV}/I_D$）。应用：整流、钳位、检波、稳压。""",
     "$I_D = I_S(e^{v_D/V_T}-1)$, $V_T \\approx 26\\text{mV}$ (300K)"),

    ("2. 双极结型晶体管 (BJT)",
     """BJT是电流控制器件——基极小电流控制集电极大电流。三个工作区：**放大区**（$I_C=\\beta I_B$）、**饱和区**（$V_{CE}\\approx 0.3V$，等效闭合开关）、**截止区**（$I_C\\approx 0$，等效断开开关）。

三种组态：共射极（电压电流增益都大，反相）、共基极（高频特性好）、共集电极/射极跟随器（电压增益≈1，高输入低输出阻抗，用于缓冲和匹配）。""",
     "$I_C = \\beta I_B$, $I_E = (1+\\beta)I_B$, $r_{be} \\approx 300\\Omega + (1+\\beta)\\frac{26\\text{mV}}{I_{EQ}}$"),

    ("3. 场效应管 (FET / MOSFET)",
     """MOSFET是电压控制器件——栅极电压控制漏极电流，输入阻抗极高（$10^{12}\\Omega$）。分增强型和耗尽型。N沟道增强型转移特性 $I_D = K(v_{GS}-V_{TN})^2$。

MOSFET优势：输入阻抗极高、功耗低、热稳定性好、易于集成。一颗芯片上可集成数十亿个MOSFET——这是现代处理器和存储器的物理基础。""",
     "$I_D = K(v_{GS}-V_{TN})^2$, $g_m = 2\\sqrt{KI_D}$"),

    ("4. 基本放大电路",
     """放大电路的核心是设置合适的**静态工作点(Q点)**。最常用**分压偏置**：通过 $R_E$ 引入直流负反馈自动稳定Q点。

分析采用"先直流后交流"：直流分析求Q点，交流分析用小信号等效模型计算增益 $A_v$、输入电阻 $R_i$、输出电阻 $R_o$。""",
     "$A_v = -\\beta\\frac{R_C \\parallel R_L}{r_{be}}$, $R_i = R_{B1}\\parallel R_{B2}\\parallel r_{be}$"),

    ("5. 多级放大电路与频率响应",
     """级间耦合方式有阻容耦合、直接耦合和变压器耦合。**频率响应**描述增益随频率的变化：低频段电容容抗增大导致增益下降，高频段晶体管结电容限制高频性能。

通频带 $BW = f_H - f_L$，**增益带宽积**为常数。**密勒效应**使跨接电容在输入端等效放大 $(1+|A_v|)$ 倍，是限制高频性能的主要因素。""",
     "$BW = f_H - f_L$, $GBP = |A_{vM}| \\cdot BW = \\text{const}$"),

    ("6. 负反馈放大电路",
     """将输出信号送回来与输入相减，利用偏差信号驱动放大器。负反馈降低增益但带来巨大好处：增益稳定性提高、带宽展宽、失真减小、输入输出阻抗按需调整。

四种拓扑：电压串联、电压并联、电流串联、电流并联。深度负反馈时 $A_f \\approx 1/F$——闭环增益只取决于反馈网络。""",
     "$A_f = \\frac{A}{1+AF}$, 深度负反馈: $A_f \\approx \\frac{1}{F}$"),

    ("7. 运算放大器基础",
     """理想运放两个"黄金法则"：**虚短**（$v_+=v_-$）和**虚断**（$i_+=i_-=0$）。

经典电路：反相放大 $A_v=-R_f/R_1$，同相放大 $A_v=1+R_f/R_1$，积分器、微分器，施密特触发器。运放是模拟电路的"瑞士军刀"。""",
     "反相: $A_v=-\\frac{R_f}{R_1}$, 同相: $A_v=1+\\frac{R_f}{R_1}$"),

    ("8. 功率放大电路",
     """A类：全程导通，失真最小但效率最高仅25%。B类：两管推挽交替工作，效率最高78.5%但有交越失真。AB类：微偏置消除交越失真，效率接近B类，是实际最常用方案。D类：PWM开关方式，效率可达90%以上。""",
     "A类效率 $\\leq 25\\%$, B类 $\\leq 78.5\\%$, $P_{om}=\\frac{V_{CC}^2}{2R_L}$"),

    ("9. 信号发生电路",
     """振荡器自发产生周期性波形，本质是**正反馈**——满足巴克豪森准则 $|AF|\\geq 1$ 且相位为 $360°$。

RC桥式振荡器（文氏电桥）适用于低频，LC振荡器适用于高频，石英晶体振荡器频率稳定度可达 $10^{-6}$。""",
     "巴克豪森: $\\dot{A}\\dot{F}=1$, RC振荡: $f_0=\\frac{1}{2\\pi RC}$"),

    ("10. 直流稳压电源",
     """四部分：变压器降压、整流（桥式最常用）、滤波（并联大电容）、稳压（线性7805或开关稳压）。线性稳压纹波小但效率低，开关稳压效率85%~95%是现代主流。""",
     "桥式整流: $V_{dc}=\\frac{2V_m}{\\pi}\\approx 0.9V_{rms}$"),
]

DIGITAL_ELECTRONICS = [
    ("1. 数制与编码",
     """数字系统建立在二进制之上。常用八进制和十六进制作为简写。8421BCD码用4位二进制表示1位十进制；格雷码相邻编码只有一位不同，消除竞争冒险；ASCII用7位表示英文字符。""",
     "$(1101)_2 = 1\\times2^3+1\\times2^2+0\\times2^1+1\\times2^0 = (13)_{10}$"),

    ("2. 逻辑代数基础",
     """布尔代数三种基本运算：与(AND)、或(OR)、非(NOT)。**德摩根定律**"与的非等于非的或"在门电路转换中极常用。

化简方法：公式法和**卡诺图法**。将逻辑函数填入方格，圈出相邻的1，每圈必须是2的幂次个格子。无关项 $\\times$ 可灵活选用以获得更大圈。""",
     "$\\overline{A\\cdot B}=\\bar{A}+\\bar{B}$, $\\overline{A+B}=\\bar{A}\\cdot\\bar{B}$"),

    ("3. 门电路",
     """基本门：与门、或门、非门、与非门（通用门）、或非门、异或门。两大工艺：TTL（速度快功耗大）和CMOS（静态功耗极低，已成主流）。

关键参数：噪声容限（CMOS约40%VDD）、扇入扇出、传输延迟。三态输出(TSL)是总线结构的必要条件。""",
     "$Y=\\overline{A\\cdot B}$ (NAND), $Y=A\\oplus B=\\bar{A}B+A\\bar{B}$"),

    ("4. 组合逻辑电路",
     """输出只取决于当前输入，无记忆。设计流程：真值表→表达式→化简→电路。

常见模块：加法器（半加器/全加器/超前进位）、编码器（74HC148优先编码器）、译码器（74HC138）、数据选择器(MUX，可实现任何逻辑函数）。需注意**竞争冒险**现象。""",
     "全加器: $S=A\\oplus B\\oplus C_{in}$, $C_{out}=AB+BC_{in}+AC_{in}$"),

    ("5. 触发器",
     """触发器是时序逻辑基本单元——能存储一个比特。D触发器：$Q^{n+1}=D$，最常用的存储单元。JK触发器：克服SR的禁止态，J=K=1时翻转。

关键时序参数：建立时间 $t_{su}$、保持时间 $t_h$、传播延迟 $t_{pd}$。违反会导致**亚稳态**——输出在0和1之间振荡。""",
     "$D: Q^{n+1}=D$; $JK: Q^{n+1}=J\\bar{Q}^n+\\bar{K}Q^n$"),

    ("6. 时序逻辑电路",
     """输出取决于当前输入和历史状态。设计：状态图→状态表→状态化简→编码→驱动方程→电路。

计数器（同步/异步，加/减/可逆）、移位寄存器（串并转换）。Moore型输出只取决于状态，Mealy型还取决于输入。""",
     "Moore: 输出=$f$(状态); Mealy: 输出=$f$(状态,输入)"),

    ("7. 脉冲波形的产生与整形",
     """555定时器：单稳态（$t_w=1.1RC$）、无稳态（$f=\\frac{1.44}{(R_1+2R_2)C}$，方波发生器）、双稳态。施密特触发器具有迟滞特性，回差电压抑制噪声。""",
     "555无稳态: $f=\\frac{1.44}{(R_1+2R_2)C}$, 单稳态: $t_w=1.1RC$"),

    ("8. 半导体存储器与PLD",
     """RAM（SRAM快但大，DRAM密但需刷新）断电丢失；ROM/Flash断电保持。PLD从简单到复杂：PAL→GAL→CPLD→**FPGA**（当今最灵活的数字系统平台）。

使用FPGA需硬件描述语言：Verilog（语法类似C，工业界主流）或VHDL（强类型，军方常用）。""",
     "SRAM: 6管/位, DRAM: 1管+1电容/位, FPGA: CLB+互连+IO"),

    ("9. 数模与模数转换",
     """ADC将模拟信号转为数字量，DAC反之。R-2R梯形网络是主流DAC方案。ADC类型：Flash（最快）、SAR（最常用）、双积分（最精确）、$\\Sigma\\Delta$（最高分辨率24位）。

**奈奎斯特采样定理**要求 $f_s \\geq 2f_{max}$，实际取3~5倍。理想n位ADC信噪比 $SNR=6.02n+1.76$ dB。""",
     "$Q=\\frac{V_{ref}}{2^n}$, $f_s \\geq 2f_{max}$, $SNR = 6.02n+1.76$ dB"),
]

CONTROL_THEORY = [
    ("1. 自动控制的基本概念",
     """自动控制让系统在无人干预下按预期目标运行。空调恒温系统是典型**闭环控制**：测量→比较→调整。

开环控制简单但抗干扰差；闭环控制通过反馈自动补偿扰动。性能三要素：**稳定性**（最基本前提）、**准确性**（稳态误差小）、**快速性**（响应快），三者常相互矛盾需权衡。""",
     "闭环传递函数: C(s)/R(s) = G(s) / [1 + G(s)H(s)]"),

    ("2. 控制系统的数学模型",
     """传递函数 G(s) = C(s)/R(s) 在零初始条件下定义，完全由系统结构决定。典型环节：比例 K、积分 1/s、微分 s、惯性 1/(Ts+1)、振荡 ωₙ²/(s²+2ζωₙs+ωₙ²)。""",
     "惯性: K/(Ts+1)    振荡: ωₙ²/(s² + 2ζωₙs + ωₙ²)"),

    ("3. 框图化简与信号流图",
     """框图代数：串联 G₁G₂、并联 G₁+G₂、反馈 G/(1±GH)。化简规则包括移动求和点和分支点。

信号流图配合**梅森增益公式**可直接写出传递函数，无需逐步化简。""",
     "梅森公式: T = (1/Δ) · Σ PₖΔₖ"),

    ("4. 时域分析与性能指标",
     """二阶系统阶跃响应：上升时间 tᵣ、调节时间 tₛ（≈ 3.5/(ζωₙ) 或 4/(ζωₙ)）、超调量 σ% = e^(-ζπ/√(1-ζ²)) × 100%。阻尼比 ζ 和自然频率 ωₙ 完全决定响应形态。""",
     "超调量: σ% = e^(-ζπ/√(1-ζ²)) × 100%     调节时间: tₛ ≈ 4/(ζωₙ)"),

    ("5. 稳定性分析",
     """BIBO稳定要求所有极点在s左半平面。**劳斯-赫尔维茨判据**通过特征方程系数构造劳斯表，无需直接求根即可判断稳定性——第一列变号次数等于右半平面极点数。""",
     "特征方程: aₙsⁿ + aₙ₋₁sⁿ⁻¹ + ⋯ + a₁s + a₀ = 0"),

    ("6. 根轨迹法",
     """根轨迹：当开环增益 K 从0变化到无穷时，闭环极点在s平面上的运动轨迹。绘制规则：起点（K=0，开环极点）、终点（K→∞，开环零点或无穷远）、渐近线、分离点等。

根轨迹直接反映增益变化对系统稳定性、阻尼和响应速度的影响。""",
     "幅值条件: |G(s)H(s)| = 1/K     相角条件: ∠G(s)H(s) = (2k+1)×180°"),

    ("7. 频域分析",
     """频率响应：令 s=jω 得到 G(jω)，绘制**Bode图**（幅频+相频）。**增益裕度**和**相位裕度**衡量稳定程度。**Nyquist判据**：开环频率特性曲线包围(-1,j0)点的次数等于右半平面闭环极点数。""",
     "增益裕度: GM = -20lg|G(jωg)| dB     相位裕度: PM = 180° + ∠G(jωc)"),

    ("8. 系统校正",
     """**PID控制器**：P（减小偏差但有余差）、I（消除稳态误差但降低稳定性）、D（预测趋势提高快速性但放大噪声）。

Ziegler-Nichols经验整定法：先只用P控制逐步增大K直到等幅振荡，记录临界增益 Ku 和振荡周期 Tu，然后按公式设置PID参数。""",
     "PID: u(t) = Kp·e(t) + Ki·∫e(t)dt + Kd·de(t)/dt"),
]

RESOURCES = {
    "视频课程": [
        ("电路原理 — 清华大学 于歆杰", "清华大学电机系于歆杰教授主讲，B站播放量超千万", "https://www.bilibili.com/video/BV1ft411c7mE", "Bilibili · 227集"),
        ("电路分析基础 — 西安电子科技大学", "西电国家级精品课程，节点法、网孔法、戴维南定理等", "https://www.bilibili.com/video/BV1iW411d7xR", "Bilibili · 西电精品课"),
        ("高等数学 — 宋浩老师", "风趣幽默，从极限到微分方程，配合大量例题", "https://www.bilibili.com/video/BV1EW411u7th", "Bilibili · 全集精讲"),
        ("复变函数 — 西北工业大学", "复数运算、解析函数、留数定理、保角映射", "https://www.bilibili.com/video/BV1Yx411d7e1", "Bilibili · 西工大精品课"),
    ],
    "在线教材": [
        ("All About Circuits", "全英文免费电路教材，配交互实验", "https://www.allaboutcircuits.com/textbook/", "英文 · 免费"),
        ("可汗学院 — 电气工程", "从基础概念讲起，配练习题和进度追踪", "https://www.khanacademy.org/science/electrical-engineering", "英文 · 交互学习"),
        ("中国大学MOOC — 电路原理", "清华电路原理MOOC，可获电子证书", "https://www.icourse163.org/course/THU-1001891005", "中文 · 有证书"),
        ("电子发烧友", "国内最大电子工程师社区，技术文章、电路图库", "https://www.elecfans.com/", "中文 · 社区"),
    ],
}

# ════════════════════════════════════════════════════════════════════
#  试题数据
# ════════════════════════════════════════════════════════════════════

QUESTIONS = {
    "电路理论": [
        {"q": "基尔霍夫电流定律(KCL)的本质是什么？",
         "opts": ["能量守恒", "电荷守恒", "动量守恒", "功率守恒"],
         "ans": 1, "exp": "KCL的本质是电荷守恒：流入节点的电荷速率等于流出的电荷速率，电荷不会在节点处积累或消失。"},
        {"q": "两个电阻 R₁=10Ω 和 R₂=30Ω 并联，等效电阻是多少？",
         "opts": ["40Ω", "7.5Ω", "20Ω", "300Ω"],
         "ans": 1, "exp": "并联: R_eq = (R₁×R₂)/(R₁+R₂) = (10×30)/(10+30) = 300/40 = 7.5Ω。并联等效电阻一定小于最小的单个电阻。"},
        {"q": "正弦稳态分析中，电容的阻抗表达式是？",
         "opts": ["jωC", "1/(jωC)", "jωL", "R"],
         "ans": 1, "exp": "电容的伏安关系 i=C·dv/dt 在相量域变为 İ=jωC·V̇，因此阻抗 Z_C = V̇/İ = 1/(jωC) = -j/(ωC)。"},
        {"q": "RC电路的时间常数τ等于？",
         "opts": ["R/C", "RC", "1/(RC)", "R²C"],
         "ans": 1, "exp": "RC电路时间常数 τ=RC，单位为秒。经过一个τ后电容电压充到约63.2%，经过5τ后认为过渡过程结束。"},
        {"q": "戴维南等效电路中，等效电阻Rth的求法是？",
         "opts": ["将所有电源短路后从端口看进去的电阻", "开路电压除以短路电流", "负载电阻的值", "电源内阻"],
         "ans": 1, "exp": "Rth = V_oc/I_sc，即开路电压除以短路电流。也可以将所有独立源置零（电压源短路、电流源开路）后从端口看进去的等效电阻。"},
        {"q": "理想变压器的电压比等于？",
         "opts": ["电流比", "匝数反比", "匝数比", "阻抗比"],
         "ans": 2, "exp": "理想变压器: V₁/V₂ = N₁/N₂（电压比等于匝数比），I₁/I₂ = N₂/N₁（电流比等于匝数反比）。"},
        {"q": "三相电路中，Y接时线电压与相电压的关系是？",
         "opts": ["V_L = V_P", "V_L = √3·V_P", "V_L = 3·V_P", "V_L = V_P/√3"],
         "ans": 1, "exp": "Y接(星形连接)时线电压等于相电压的√3倍: V_L = √3·V_P。例如民用电220V相电压对应380V线电压。"},
        {"q": "串联RLC电路发生谐振时，电路呈什么性质？",
         "opts": ["感性", "容性", "纯阻性", "不确定"],
         "ans": 2, "exp": "串联谐振时感抗等于容抗(jωL = 1/(jωC))，两者相互抵消，总阻抗等于纯电阻R，电路呈纯阻性。"},
    ],
    "工程数学": [
        {"q": "欧拉公式 e^(jθ) 等于？",
         "opts": ["cosθ + sinθ", "cosθ + j·sinθ", "sinθ + j·cosθ", "j·(cosθ + sinθ)"],
         "ans": 1, "exp": "欧拉公式: e^(jθ) = cosθ + j·sinθ，被誉为最美的数学公式，将指数函数与三角函数统一。"},
        {"q": "复数 z = 3 + 4j 的模 |z| 等于？",
         "opts": ["7", "12", "5", "25"],
         "ans": 2, "exp": "|z| = √(a²+b²) = √(3²+4²) = √(9+16) = √25 = 5。这是经典的3-4-5勾股数。"},
        {"q": "一阶微分方程的通解由哪两部分组成？",
         "opts": ["齐次解和特解", "零输入响应和零状态响应", "暂态响应和稳态响应", "以上都对"],
         "ans": 3, "exp": "一阶微分方程通解 = 齐次解(自由响应) + 特解(强制响应)。零输入/零状态、暂态/稳态是不同的分解方式，三者本质相通。"},
        {"q": "德摩根定律 A·B 的非 等于？",
         "opts": ["A非 + B非", "A非 · B非", "A + B", "A · B非"],
         "ans": 0, "exp": "德摩根定律: (A·B)' = A' + B'，即'与的非等于非的或'。同理 (A+B)' = A'·B'。这是逻辑代数中最常用的定律。"},
        {"q": "拉普拉斯变换中，f(t)=e^(-at) 的变换结果是？",
         "opts": ["1/(s+a)", "1/(s-a)", "a/(s+a)", "s/(s+a)"],
         "ans": 0, "exp": "L{e^(-at)} = 1/(s+a)，收敛域 Re(s)>-a。这是拉普拉斯变换最基本的变换对之一。"},
        {"q": "矩阵 A 满足什么条件时逆矩阵存在？",
         "opts": ["A是方阵", "A的行列式不为零", "A的元素全为正", "A是对称矩阵"],
         "ans": 1, "exp": "逆矩阵 A⁻¹ 存在的充要条件是 |A|≠0（行列式不为零），即A是非奇异矩阵。仅仅A是方阵不够。"},
    ],
    "模拟电子技术": [
        {"q": "硅二极管的正向导通压降约为？",
         "opts": ["0.1V", "0.3V", "0.7V", "1.2V"],
         "ans": 2, "exp": "硅二极管正向导通压降约0.7V，锗管约0.3V。这是半导体器件的基本参数，在电路分析中常用恒压降模型。"},
        {"q": "BJT工作在放大区的条件是？",
         "opts": ["发射结正偏、集电结正偏", "发射结反偏、集电结反偏", "发射结正偏、集电结反偏", "两个结都零偏"],
         "ans": 2, "exp": "放大区: 发射结正偏(保证载流子注入)、集电结反偏(保证载流子被收集)。此时 I_C = β·I_B。"},
        {"q": "负反馈对放大器带宽的影响是？",
         "opts": ["减小带宽", "增大带宽", "不影响带宽", "带宽先增后减"],
         "ans": 1, "exp": "负反馈展宽带宽: BW_f = BW·(1+AF)。增益降低多少倍，带宽就增大多少倍，增益带宽积保持不变。"},
        {"q": "理想运放的'虚短'指的是？",
         "opts": ["输入电流为零", "输出电压为零", "两输入端电压相等", "开环增益为零"],
         "ans": 2, "exp": "虚短: v+ = v-，两输入端电压相等。这是因为理想运放开环增益无穷大，而输出电压有限，所以输入差模电压必须趋近于零。"},
        {"q": "B类功放的最大理论效率是？",
         "opts": ["25%", "50%", "78.5%", "100%"],
         "ans": 2, "exp": "B类推挽功放最大效率 η_max = π/4 ≈ 78.5%。A类最高25%(电阻负载)，D类可达90%以上。"},
        {"q": "文氏电桥振荡器的振荡频率公式是？",
         "opts": ["f₀ = 1/(2πRC)", "f₀ = 1/(2π√LC)", "f₀ = RC/(2π)", "f₀ = 2πRC"],
         "ans": 0, "exp": "RC桥式(文氏电桥)振荡器: f₀ = 1/(2πRC)，适用于低频(Hz~kHz)。LC振荡器: f₀ = 1/(2π√LC)，适用于高频。"},
    ],
    "数字电子技术": [
        {"q": "二进制数 1101 转换为十进制是？",
         "opts": ["11", "12", "13", "14"],
         "ans": 2, "exp": "1101₂ = 1×8 + 1×4 + 0×2 + 1×1 = 13₁₀。从右到左每位的权值是 2⁰, 2¹, 2², 2³。"},
        {"q": "与非门(NAND)为什么被称为'通用门'？",
         "opts": ["因为它最快", "因为仅用与非门就能实现所有逻辑功能", "因为它的功耗最低", "因为它是CMOS工艺"],
         "ans": 1, "exp": "与非门和或非门都是'完备集'——仅用一种门就能搭建出与、或、非等所有逻辑功能，因此被称为通用门。"},
        {"q": "D触发器的特征方程是？",
         "opts": ["Q(n+1) = D", "Q(n+1) = J·Q'+K'·Q", "Q(n+1) = T⊕Q", "Q(n+1) = S+R'·Q"],
         "ans": 0, "exp": "D触发器在时钟有效沿将输入D锁存到输出: Q(n+1) = D。它是最简单也是最常用的触发器，是寄存器的基本单元。"},
        {"q": "卡诺图化简中，圈的大小必须是？",
         "opts": ["任意数量", "2的幂次个格子(1,2,4,8...)", "偶数个格子", "至少4个格子"],
         "ans": 1, "exp": "卡诺图中每圈必须包含 2ⁿ 个格子(1,2,4,8,16...)，对应消去n个变量。圈越大，消去的变量越多，表达式越简。"},
        {"q": "逐次逼近型(SAR)ADC的特点是？",
         "opts": ["速度最快但面积大", "速度和精度均衡，最常用", "精度最高但速度最慢", "分辨率最高"],
         "ans": 1, "exp": "SAR ADC用二分法逐位确定，n位需要n个时钟周期。速度和精度均衡，是应用最广的ADC类型(8~18位，几十kSPS~几MSPS)。"},
        {"q": "8421BCD码中，十进制数9的编码是？",
         "opts": ["1001", "1010", "1100", "1000"],
         "ans": 0, "exp": "8421BCD码用4位二进制表示1位十进制。9 = 1001₂(8+0+0+1)。有效范围0000~1001，1010~1111无效。"},
    ],
    "自动控制原理": [
        {"q": "闭环控制系统相比开环系统的主要优势是？",
         "opts": ["结构简单", "成本低", "能自动补偿扰动", "不需要传感器"],
         "ans": 2, "exp": "闭环控制通过反馈自动检测偏差并修正，能补偿扰动和参数变化。代价是结构复杂、成本较高，但性能远优于开环。"},
        {"q": "传递函数 G(s) 定义的前提条件是？",
         "opts": ["系统必须是线性的", "初始条件为零", "输入是阶跃信号", "系统是时不变的"],
         "ans": 1, "exp": "传递函数定义为零初始条件下，输出的拉普拉斯变换与输入的拉普拉斯变换之比。线性和时不变是隐含前提，但定义的关键约束是零初始条件。"},
        {"q": "二阶系统阻尼比 ζ = 0.5 时，系统响应属于？",
         "opts": ["过阻尼", "欠阻尼", "临界阻尼", "无阻尼"],
         "ans": 1, "exp": "ζ < 1 为欠阻尼(振荡衰减)，ζ > 1 为过阻尼(缓慢无振荡)，ζ = 1 为临界阻尼。ζ = 0.5 < 1，属于欠阻尼。"},
        {"q": "劳斯判据中，劳斯表第一列变号次数等于？",
         "opts": ["系统的阶数", "右半平面极点数", "左半平面极点数", "虚轴上的极点数"],
         "ans": 1, "exp": "劳斯-赫尔维茨判据: 特征方程在右半平面的根(不稳定极点)个数等于劳斯表第一列变号次数。第一列不变号则系统稳定。"},
        {"q": "根轨迹的起点(K=0)是？",
         "opts": ["开环零点", "开环极点", "闭环零点", "闭环极点"],
         "ans": 1, "exp": "根轨迹起于开环极点(K=0)，终于开环零点或无穷远(K→∞)。绘制根轨迹可以直观看出增益K变化对闭环极点位置的影响。"},
        {"q": "PID控制器中，I(积分)环节的主要作用是？",
         "opts": ["提高响应速度", "减小超调量", "消除稳态误差", "抑制高频噪声"],
         "ans": 2, "exp": "积分环节对偏差进行累积，只要偏差存在就会持续调整，最终消除稳态误差。但积分会降低系统稳定性，可能引起振荡。"},
        {"q": "Bode图中，增益裕度(GM)的定义是？",
         "opts": ["相位为-180°时增益的倒数", "增益为0dB时相位与-180°的差", "截止频率处的增益", "直流增益"],
         "ans": 0, "exp": "增益裕度: 当相位等于-180°时，增益距0dB的余量。GM = -20lg|G(jωg)| dB，ωg是相位穿越频率。GM越大越稳定。"},
        {"q": "Ziegler-Nichols整定法中，首先需要找到？",
         "opts": ["系统的传递函数", "临界增益Ku和振荡周期Tu", "所有极点的位置", "Bode图"],
         "ans": 1, "exp": "Z-N法: 先只用P控制，逐步增大K直到系统等幅振荡，记录此时的临界增益Ku和振荡周期Tu，再按经验公式计算PID参数。"},
    ],
}

# ════════════════════════════════════════════════════════════════════
#  顶部导航 Tab
# ════════════════════════════════════════════════════════════════════

main_tabs = st.tabs(["课程知识", "资源链接", "仿真实验室", "试题练习"])

# ── 课程知识 ──
with main_tabs[0]:
    sub_tabs = st.tabs(["电路理论", "工程数学", "模拟电子技术", "数字电子技术", "自动控制原理"])
    with sub_tabs[0]:
        knowledge_section("电路理论", CIRCUIT_THEORY)
    with sub_tabs[1]:
        knowledge_section("工程数学", ENGINEERING_MATH)
    with sub_tabs[2]:
        knowledge_section("模拟电子技术", ANALOG_ELECTRONICS)
    with sub_tabs[3]:
        knowledge_section("数字电子技术", DIGITAL_ELECTRONICS)
    with sub_tabs[4]:
        knowledge_section("自动控制原理", CONTROL_THEORY)

# ── 资源链接 ──
with main_tabs[1]:
    for group, cards in RESOURCES.items():
        st.markdown(f"**{group}**")
        cols = st.columns(2)
        for i, (title, desc, url, tag) in enumerate(cards):
            with cols[i % 2]:
                st.link_button(f"**{title}**", url, help=desc, use_container_width=True)
                st.caption(f"{desc} / {tag}")

# ── 仿真实验室 ──
with main_tabs[2]:
    sim_sub = st.tabs(["CircuitJS 电路模拟器", "GeoGebra 复数可视化"])
    with sim_sub[0]:
        st.info("可点击 文件 - 打开示例 浏览预置电路，或自行搭建电路进行仿真。")
        st.components.v1.iframe(
            "https://lushprojects.com/circuitjs/circuitjs.html?lang=zh",
            height=550, scrolling=True,
        )
    with sim_sub[1]:
        st.info("拖动复平面上的点，观察复数乘法的几何意义——模相乘、角度相加。")
        st.components.v1.iframe(
            "https://www.geogebra.org/classic/tz5x6vga?embed",
            height=550, scrolling=True,
        )

# ── 试题练习 ──
with main_tabs[3]:
    # 初始化 session state
    if 'quiz_subject' not in st.session_state:
        st.session_state.quiz_subject = None
    if 'quiz_idx' not in st.session_state:
        st.session_state.quiz_idx = 0
    if 'quiz_score' not in st.session_state:
        st.session_state.quiz_score = 0
    if 'quiz_total' not in st.session_state:
        st.session_state.quiz_total = 0
    if 'quiz_answered' not in st.session_state:
        st.session_state.quiz_answered = False
    if 'quiz_history' not in st.session_state:
        st.session_state.quiz_history = []

    # 选择科目
    if st.session_state.quiz_subject is None:
        st.markdown("**选择科目开始练习**")
        cols = st.columns(len(QUESTIONS))
        for i, (subj, qs) in enumerate(QUESTIONS.items()):
            with cols[i]:
                if st.button(f"**{subj}**\n\n{len(qs)} 题", key=f"sub_{i}", use_container_width=True):
                    st.session_state.quiz_subject = subj
                    st.session_state.quiz_idx = 0
                    st.session_state.quiz_score = 0
                    st.session_state.quiz_total = len(qs)
                    st.session_state.quiz_answered = False
                    st.session_state.quiz_history = []
                    st.rerun()
    else:
        subj = st.session_state.quiz_subject
        questions = QUESTIONS[subj]
        idx = st.session_state.quiz_idx

        # 顶部进度栏
        progress = (idx) / len(questions) if len(questions) > 0 else 0
        st.progress(progress, text=f"{subj} · 第 {idx+1}/{len(questions)} 题 · 得分 {st.session_state.quiz_score}/{st.session_state.quiz_total}")

        if idx < len(questions):
            q = questions[idx]
            st.markdown(f"**{idx+1}. {q['q']}**")

            # 显示选项
            selected = st.radio("选择答案", q["opts"], key=f"q_{idx}", index=None)

            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("提交", key=f"submit_{idx}", disabled=(selected is None), use_container_width=True):
                    st.session_state.quiz_answered = True
                    chosen = q["opts"].index(selected)
                    correct = chosen == q["ans"]
                    if correct:
                        st.session_state.quiz_score += 1
                    st.session_state.quiz_history.append({
                        "q": q["q"], "chosen": chosen, "correct": correct,
                        "correct_ans": q["ans"], "exp": q["exp"]
                    })
                    st.rerun()

            # 显示结果
            if st.session_state.quiz_answered:
                last = st.session_state.quiz_history[-1]
                if last["correct"]:
                    st.success("正确!")
                else:
                    st.error(f"错误! 正确答案: {q['opts'][last['correct_ans']]}")
                st.info(f"**解析:** {last['exp']}")

                if st.button("下一题", key=f"next_{idx}", use_container_width=True):
                    st.session_state.quiz_idx += 1
                    st.session_state.quiz_answered = False
                    st.rerun()
        else:
            # 答题结束
            score = st.session_state.quiz_score
            total = st.session_state.quiz_total
            pct = score / total * 100 if total > 0 else 0

            st.markdown(f"### 练习完成!")
            st.markdown(f"**{subj}** · 得分 **{score}/{total}** ({pct:.0f}%)")

            if pct >= 80:
                st.balloons()
                st.success("优秀! 掌握得很好!")
            elif pct >= 60:
                st.info("不错，继续加油!")
            else:
                st.warning("建议回顾知识点后再试一次。")

            # 答题详情
            with st.expander("查看答题详情", expanded=False):
                for i, h in enumerate(st.session_state.quiz_history):
                    icon = "✓" if h["correct"] else "✗"
                    color = "green" if h["correct"] else "red"
                    st.markdown(f"**{i+1}.** :{color}[{icon}] {h['q']}")
                    if not h["correct"]:
                        st.caption(f"你选: {q['opts'][h['chosen']]} → 正确: {q['opts'][h['correct_ans']]}")
                    st.caption(f"解析: {h['exp']}")

            c1, c2 = st.columns(2)
            with c1:
                if st.button("重新挑战", use_container_width=True):
                    st.session_state.quiz_idx = 0
                    st.session_state.quiz_score = 0
                    st.session_state.quiz_answered = False
                    st.session_state.quiz_history = []
                    st.rerun()
            with c2:
                if st.button("换个科目", use_container_width=True):
                    st.session_state.quiz_subject = None
                    st.session_state.quiz_idx = 0
                    st.session_state.quiz_score = 0
                    st.session_state.quiz_answered = False
                    st.session_state.quiz_history = []
                    st.rerun()

# ── 页脚 ──
st.markdown('<div class="footer-line">EE-Learning &middot; 仅供个人学习使用</div>', unsafe_allow_html=True)
