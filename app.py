import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go
from fpdf import FPDF
import datetime
import os

# 1. 페이지 설정 및 다크 테마 커스텀
st.set_page_config(page_title="Smart Equation Analyzer", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #FF4B4B; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧪 Smart Equation Analyzer: Final Master")
st.markdown("수식 분석, 라플라스 변환, 미분방정식 풀이 및 그래프 포함 PDF 리포트 생성")

# 2. 사이드바 메뉴
menu = st.sidebar.selectbox("분석 모드 선택", 
    ["대수/연립/초월방정식", "라플라스 변환", "미분방정식(ODE)", "미적분 계산"])

# 기본 심볼 정의
x, y, t, s = sp.symbols('x y t s')

# --- 핵심 유틸리티 함수 ---

def create_pdf_report(mode_name, input_data, result_data, fig=None):
    """결과 수식과 그래프 이미지를 포함한 PDF 리포트 생성 (영문 베이스로 인코딩 오류 방지)"""
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 10, txt="Smart Equation Analyzer Report", ln=True, align='C')
    pdf.ln(10)
    
    # Info Section
    pdf.set_font("Arial", size=10)
    pdf.cell(190, 7, txt=f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.cell(190, 7, txt=f"Analysis Mode: {mode_name}", ln=True)
    pdf.ln(5)
    
    # 1. Results Section
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(190, 10, txt="1. Calculation Results", ln=True)
    pdf.set_font("Arial", size=10)
    # 특수 문자 정제 (인코딩 에러 방지)
    result_str = str(result_data).replace('π', 'pi').replace('∫', 'int')
    pdf.multi_cell(0, 7, txt=f"Input: {input_data}\nResult: {result_str}")
    pdf.ln(10)
    
    # 2. Graph Section
    if fig:
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(190, 10, txt="2. Visual Analysis (Graph)", ln=True)
        img_filename = "temp_plot_for_pdf.png"
        try:
            fig.write_image(img_filename, engine="kaleido", width=800, height=500, scale=2)
            pdf.image(img_filename, x=10, y=None, w=180)
            if os.path.exists(img_filename):
                os.remove(img_filename)
        except Exception as e:
            pdf.cell(190, 10, txt=f"(Graph could not be rendered: {str(e)})", ln=True)

    return pdf.output(dest='S')

def find_numerical_roots(expr, var, start=-20, end=20, steps=600):
    """수치 해석을 통한 모든 실근 탐색"""
    try:
        f_num = sp.lambdify(var, expr, 'numpy')
        pts = np.linspace(start, end, steps)
        roots = []
        for i in range(len(pts)-1):
            if f_num(pts[i]) * f_num(pts[i+1]) <= 0:
                try:
                    root = sp.nsolve(expr, var, (pts[i] + pts[i+1])/2)
                    if not any(abs(root - r) < 1e-5 for r in roots):
                        roots.append(root)
                except: continue
        return sorted(roots)
    except:
        return sp.solve(expr, var)

def generate_plot(exprs, labels, sols=None):
    """Plotly 인터랙티브 그래프 생성"""
    fig = go.Figure()
    xv = np.linspace(-15, 15, 1000)
    for expr, label in zip(exprs, labels):
        try:
            curr_expr = expr.subs({t: x, s: x})
            y_sols = sp.solve(curr_expr, y)
            if not y_sols:
                f_n = sp.lambdify(x, curr_expr, 'numpy')
                yv = f_n(xv)
                if isinstance(yv, (int, float)): yv = np.full_like(xv, yv)
                fig.add_trace(go.Scatter(x=xv, y=yv, name=label))
            else:
                for s_val in y_sols:
                    f_n = sp.lambdify(x, s_val, 'numpy')
                    yv = f_n(xv)
                    fig.add_trace(go.Scatter(x=xv, y=yv, name=f"Line: {label}"))
        except: continue

    if sols:
        if isinstance(sols, list) and len(sols) > 0 and isinstance(sols[0], dict):
            for s_dict in sols:
                px, py = float(s_dict[x].evalf()), float(s_dict[y].evalf())
                fig.add_trace(go.Scatter(x=[px], y=[py], mode='markers', name="Solution", marker=dict(size=12, color='red')))
        else:
            for s_val in sols:
                try:
                    px = float(s_val.evalf())
                    fig.add_trace(go.Scatter(x=[px], y=[0], mode='markers', name="Root", marker=dict(size=10, color='#FF4B4B', symbol='x')))
                except: pass

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#262730", template="plotly_dark",
        xaxis=dict(zeroline=True, zerolinecolor='white', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='white')),
        yaxis=dict(zeroline=True, zerolinecolor='white', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='white'))
    )
    return fig

# --- 모드별 메인 로직 ---

if menu == "대수/연립/초월방정식":
    st.header("🔢 방정식 분석 (대수/초월/연립)")
    eqs_in = st.text_input("입력 (예: 10*sin(x)-x=0 또는 sin(x)-y=0, x-y=5)", "10*sin(x) - x = 0")
    if eqs_in:
        try:
            raw_eqs = [e.strip() for e in eqs_in.split(',')]
            plot_exprs = [sp.simplify(e.split('=')[0]) - sp.simplify(e.split('=')[1] if '=' in e else '0') for e in raw_eqs]
            with st.spinner('계산 중...'):
                if len(plot_exprs) == 1:
                    final_sols = find_numerical_roots(plot_exprs[0], x)
                else:
                    y_sub = sp.solve(sp.Eq(plot_exprs[1], 0), y)[0]
                    combined = plot_exprs[0].subs(y, y_sub)
                    x_roots = find_numerical_roots(combined, x)
                    final_sols = [{x: r, y: y_sub.subs(x, r)} for r in x_roots]
            st.subheader("📝 계산 결과")
            st.latex(sp.latex(final_sols))
            fig = generate_plot(plot_exprs, raw_eqs, final_sols)
            st.plotly_chart(fig, use_container_width=True)
            pdf_data = create_pdf_report("Equation Analysis", eqs_in, final_sols, fig=fig)
            st.download_button("📄 PDF 리포트 저장", pdf_data, "equation_report.pdf", "application/pdf")
        except Exception as e: st.error(f"오류: {e}")

elif menu == "라플라스 변환":
    st.header("🔄 라플라스 변환 (t ↔ s)")
    l_mode = st.radio("방향 선택", ["t -> s (Laplace)", "s -> t (Inverse)"])
    f_in = st.text_input("함수 입력", "exp(-t)*sin(t)")
    if f_in:
        try:
            expr = sp.simplify(f_in)
            res = sp.laplace_transform(expr, t, s)[0] if "t -> s" in l_mode else sp.inverse_laplace_transform(expr, s, t)
            st.subheader("📝 변환 결과")
            st.latex(sp.latex(res))
            pdf_data = create_pdf_report("Laplace Transform", f_in, res)
            st.download_button("📄 PDF 결과 저장", pdf_data, "laplace_report.pdf", "application/pdf")
        except Exception as e: st.error(f"오류: {e}")

elif menu == "미분방정식(ODE)":
    st.header("📉 미분방정식 풀이 (ODE)")
    f_func = sp.Function('f')(x)
    ode_in = st.text_input("입력 (예: f(x).diff(x, x) + f(x) = 0)", "f(x).diff(x) - f(x) = 0")
    if ode_in:
        try:
            l, r = ode_in.split('=') if '=' in ode_in else (ode_in, '0')
            sol = sp.dsolve(sp.Eq(sp.simplify(l), sp.simplify(r)), f_func)
            st.subheader("📝 일반해 (LaTeX)")
            st.latex(sp.latex(sol))
            pdf_data = create_pdf_report("ODE Analysis", ode_in, sol)
            st.download_button("📄 PDF 결과 저장", pdf_data, "ode_report.pdf", "application/pdf")
        except Exception as e: st.error(f"오류: {e}")

elif menu == "미적분 계산":
    st.header("📐 미분 및 적분")
    st.warning("⚠️ 미적분 모드는 특수 기호 호환 문제로 PDF 저장을 지원하지 않습니다. (화면 결과 확인 권장)")
    c_expr = st.text_input("수식", "x * sin(x)")
    c_mode = st.radio("작업", ["미분", "적분"])
    if c_expr:
        try:
            expr = sp.simplify(c_expr)
            res = sp.diff(expr, x) if c_mode == "미분" else sp.integrate(expr, x)
            st.subheader("📝 계산 결과")
            st.latex(sp.latex(res))
            fig = generate_plot([res], [f"{c_mode} 결과"])
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e: st.error(f"계산 중 오류: {e}")