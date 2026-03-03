# 🧪 Smart Equation Analyzer (Ultimate Edition)

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![SymPy](https://img.shields.io/badge/SymPy-Symbolic_Math-green?style=flat)

**Smart Equation Analyzer**는 복잡한 수치 해석과 상징적 수학 연산을 웹 대시보드에서 직관적으로 수행할 수 있는 통합 도구입니다. 다항식부터 초월방정식, 라플라스 변환, 미분방정식까지 공학 및 데이터 분석에 필요한 핵심 기능을 제공합니다.



---

## 🚀 주요 기능 (Key Features)

### 1. 대수/연립/초월방정식 풀이
* **모든 실근 추적**: 단순한 해뿐만 아니라 `10*sin(x) - x = 0`과 같이 해가 여러 개인 초월방정식의 모든 실근을 구간 스캔 방식으로 찾아냅니다.
* **연립 초월방정식**: `sin(x)-y=0, x-y=5`와 같이 기호적으로 풀기 어려운 식을 수치 해석 기법으로 해결합니다.

### 2. 공학 수학 도구 (Engineering Math)
* **라플라스 변환**: 시간 영역($t$)과 주파수 영역($s$) 사이의 변환 및 역변환을 지원합니다.
* **미분방정식(ODE)**: 일반해를 구하고 LaTeX 형식으로 깔끔하게 출력합니다.
* **미적분 계산**: 함수의 미분 및 적분 결과를 즉시 확인합니다.

### 3. 인터랙티브 시각화 및 리포트
* **Plotly 기반 그래프**: 확대/축소가 가능한 다크 테마 기반의 인터랙티브 그래프를 제공합니다.
* **PDF 리포트 저장**: 분석 결과와 그래프를 포함한 PDF 문서를 즉시 생성할 수 있습니다. (※ 미적분 모드 제외)

---

## 🛠️ 설치 및 실행 방법 (Installation)

### 필수 라이브러리 설치
본 프로젝트는 Python 3.8 이상 환경에서 최적화되어 있습니다. 아래 명령어로 필요한 패키지를 설치하세요.

```bash
pip install streamlit sympy numpy plotly fpdf kaleido
```

실행 방법
저장소를 클론하거나 코드를 내려받습니다.

터미널에서 다음 명령어를 입력합니다:

Bash
streamlit run app.py
또는 동봉된 run_analyzer.bat 파일을 더블 클릭하여 실행할 수 있습니다.

📂 프로젝트 구조 (Project Structure)
app.py: 메인 애플리케이션 소스 코드

run_analyzer.bat: 윈도우용 원클릭 실행 배치 파일

requirements.txt: 의존성 라이브러리 목록

.gitignore: 불필요한 임시 파일 업로드 방지 설정
