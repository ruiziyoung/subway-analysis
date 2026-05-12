import streamlit as st
import sqlite3
import pandas as pd
import os

# --------------------------------------------------
# [설정] 페이지 기본 설정
# --------------------------------------------------
st.set_page_config(
    page_title="지하철 환승역 분석 대시보드",
    page_icon="🚇",
    layout="wide"
)

# --------------------------------------------------
# [함수] 데이터베이스 연결 및 데이터 불러오기
# --------------------------------------------------
def get_data_from_db(query):
    db_path = '지하철역.db'
    
    # DB 파일 존재 여부 확인 (에러 처리)
    if not os.path.exists(db_path):
        st.error(f"❌ 데이터베이스 파일 '{db_path}'를 찾을 수 없습니다. 파일 위치를 확인해주세요.")
        return None
    
    try:
        # SQLite 연결
        conn = sqlite3.connect(db_path)
        # SQL 쿼리 실행 후 결과를 데이터프레임으로 변환
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"⚠️ 쿼리 실행 중 오류가 발생했습니다: {e}")
        return None

# --------------------------------------------------
# [헤더] 메인 타이틀 및 설명
# --------------------------------------------------
st.title("🚇 지하철 환승역 데이터 분석 대시보드")
st.markdown("### 지하철 환승 데이터와 시간대별 혼잡도를 기반으로 주요 환승역 특징을 분석한 대시보드입니다.")
st.divider()

# --------------------------------------------------
# [차트 1] 환승역별 총환승인원 TOP 6
# --------------------------------------------------
st.header("📊 어떤 환승역이 가장 환승인원이 많을까?")

sql_1 = """
SELECT 환승역명, 
       SUM(총환승인원) AS 총환승인원
FROM 환승인원
GROUP BY 환승역명
ORDER BY 총환승인원 DESC
LIMIT 6;
"""

df1 = get_data_from_db(sql_1)

if df1 is not None:
    # 화면 분할 (차트와 정보를 좌우로 배치)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📍 환승역별 총환승인원 TOP 6")
        # 차트를 그리기 위해 '환승역명'을 인덱스로 설정
        chart_df1 = df1.set_index('환승역명')
        st.bar_chart(chart_df1, color="#1f77b4") # 깔끔한 파란색
        st.dataframe(df1, use_container_width=True) # 데이터 표 함께 출력

    with col2:
        st.markdown("##### 💻 사용된 SQL문")
        st.code(sql_1, language="sql")
        
        st.markdown("##### 💡 데이터 인사이트")
        st.success("""
        - **환승 규모 확인**: 총환승인원이 가장 많은 환승역 순위를 보여줍니다.
        - **정보 설계의 중요성**: 환승인원이 많은 만큼 환승 방향, 출구 위치, 환승 통로 등을 한눈에 이해할 수 있는 직관적인 표지판 배치가 매우 중요합니다.
        - **동선 개선**: 이용객의 병목 현상을 줄이기 위한 동선 개선 및 에스컬레이터 점검이 우선적으로 이루어져야 할 역들입니다.
        """)

st.divider() # 구분선

# --------------------------------------------------
# [차트 2] 평일 오전 8시 혼잡도 분석
# --------------------------------------------------
st.header("💼 총환승인원이 많은 환승역이 직장인 때문일까?")

sql_2 = """
SELECT 환승역명, 
       혼잡도
FROM 혼잡도
WHERE 요일구분 = '평일'
AND 시간 = 8
ORDER BY 혼잡도 DESC
LIMIT 6;
"""

df2 = get_data_from_db(sql_2)

if df2 is not None:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📍 평일 오전 8시 환승역별 혼잡도 TOP 6")
        chart_df2 = df2.set_index('환승역명')
        st.bar_chart(chart_df2, color="#ff7f0e") # 활기찬 주황색
        st.dataframe(df2, use_container_width=True)

    with col2:
        st.markdown("##### 💻 사용된 SQL문")
        st.code(sql_2, language="sql")
        
        st.markdown("##### 💡 데이터 인사이트")
        st.info("""
        - **출근길 혼잡 분석**: 평일 오전 8시, 실제 직장인들의 이동이 집중되는 역들을 확인할 수 있습니다.
        - **데이터 비교**: 단순히 총환승객이 많은 역과, 출근 시간에 집중적으로 혼잡한 역은 다를 수 있습니다.
        - **비즈니스 기회**: 혼잡도가 높은 역 근처에는 출근길 직장인들이 빠르게 아침 식사를 해결할 수 있는 카페, 샌드위치 가게, 테이크아웃 전문점 입점에 유리한 상권입니다.
        """)

st.divider()

# --------------------------------------------------
# [차트 3] 토요일 오후 14시 혼잡도 분석
# --------------------------------------------------
st.header("🎈 총환승인원이 많은 환승역은 놀러 오는 사람들이 많아서일까?")

sql_3 = """
SELECT 환승역명, 
       혼잡도
FROM 혼잡도
WHERE 요일구분 = '토요일'
AND 시간 = 14
ORDER BY 혼잡도 DESC
LIMIT 6;
"""

df3 = get_data_from_db(sql_3)

if df3 is not None:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📍 토요일 오후 14시 환승역별 혼잡도 TOP 6")
        chart_df3 = df3.set_index('환승역명')
        st.bar_chart(chart_df3, color="#2ca02c") # 산뜻한 녹색
        st.dataframe(df3, use_container_width=True)

    with col2:
        st.markdown("##### 💻 사용된 SQL문")
        st.code(sql_3, language="sql")
        
        st.markdown("##### 💡 데이터 인사이트")
        st.info("""
        - **여가 목적지 확인**: 토요일 오후 2시 혼잡도가 높은 곳은 대표적인 약속 장소나 문화 시설이 밀집된 지역일 가능성이 큽니다.
        - **유동인구 특징**: 평일 출근 시간대와 순위가 다르다면, 해당 역은 업무 지구보다는 여가/상업 지구의 특성을 가집니다.
        - **입점 전략**: 이러한 역 주변에는 트렌디한 팝업스토어, 의류 쇼핑몰, 디저트 카페 등 MZ세대나 가족 단위 방문객을 타겟으로 하는 업종이 유리합니다.
        """)

st.divider()
st.caption("© 2024 지하철 데이터 분석 대시보드 - Senior Data Developer")