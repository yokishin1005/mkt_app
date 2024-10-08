import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv
import json
import re
from streamlit_lottie import st_lottie
import requests
import plotly.graph_objects as go
from streamlit_echarts import st_echarts

# Load environment variables and initialize OpenAI client
_ = load_dotenv(find_dotenv())
openapi_key = os.getenv('OPENAI_API_KEY')
client = OpenAI()

def load_lottie_url(url: str):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

def generate_marketing_insights(persona, challenges):
    prompt = f"""
あなたは、世界で屈指の優秀なマーケティングプロフェッショナルです。
以下の情報をまずは読み込んでください

ターゲットの情報:
{persona}

悩み、課題:
{challenges}

Based on the provided data, use inference to write bullet points outlining the key points and details for the following items. 
Ensure that you cover all the defined information and provide specific details. 
For any information not provided, please infer it from the given information. We request that you make innovative, concrete, and deep insights that can be inferred from the user-entered information, giving the impression of profound understanding.

1. デモグラフィック情報:
   - Infer and describe the target's detailed demographic profile, including age, gender, location (country, region, city), education level, occupation, income level, marital status, family composition, race/ethnicity, and language.
   - Provide specific insights into how these demographic factors may influence the target's behavior, preferences, and needs.

2. サイコグラフィック情報:
   - Infer and outline the target's lifestyle, values, personality traits, attitudes, interests, hobbies, social and political beliefs, purchasing motives, brand preferences, media consumption habits, technology usage, decision-making process, influential groups or communities, role models or respected figures, and future goals and aspirations.
   - Explain how these psychographic characteristics may shape the target's perceptions, choices, and interactions with products, services, and brands.

3. ターゲットの課題:
   - Infer and identify the problems or challenges currently faced by the target, the desired solutions or benefits they seek, the specific features or characteristics they require in products or services, the expected price range, preferred purchase channels (online, brick-and-mortar), potential barriers to purchase, necessary support or service to enhance satisfaction, current level of knowledge about the product or service, usage of competitor products or services, the purpose or intended use of the product or service, factors influencing their decision-making (quality, price, brand, reputation), post-purchase expectations or concerns, feedback or evaluation of the product or service, and potential future needs that may arise.
   - Provide actionable insights into how these needs can be addressed and fulfilled through tailored marketing strategies and personalized offerings.

4. キャッチフレーズ:
    Based on the insights from points 1, 2, and 3, propose at least five catchphrases that would likely appeal to and attract the targeted persona.
    Craft compelling and memorable phrases that resonate with the target's demographic profile, psychographic characteristics, and specific needs.
    Use language and tone that align with the target's preferences and communication style to create a strong emotional connection and motivate action.
    Highlight the unique benefits, solutions, or experiences that the product, service, or brand offers to address the target's challenges and fulfill their desires.
    Aim for concise, impactful, and easily understandable catchphrases that effectively communicate the core message and value proposition.
    Present the proposed catchphrases in a bullet-point format, ensuring each catchphrase is clearly distinguishable and stands on its own.

5. ペルソナの特性スコア:
   以下の特性について、1から10の範囲でスコアを付けてください。
   - 収入レベル
   - 教育レベル
   - デジタル親和性
   - ブランド志向性
   - 価格感応度
   - 健康意識
   - 環境意識
   - 社会的影響力
   - 冒険心
   - 家族重視度

Please format your response as a JSON object with the following structure:
{{
    "demographic": [
        "ポイント1",
        "ポイント2",
        "ポイント3"
    ],
    "psychographic": [
        "ポイント1",
        "ポイント2",
        "ポイント3"
    ],
    "challenges": [
        "課題1",
        "課題2",
        "課題3"
    ],
    "catchphrases": [
        "キャッチフレーズ1",
        "キャッチフレーズ2",
        "キャッチフレーズ3",
        "キャッチフレーズ4",
        "キャッチフレーズ5"
    ],
    "persona_scores": {{
        "収入レベル": 7,
        "教育レベル": 8,
        "デジタル親和性": 9,
        "ブランド志向性": 6,
        "価格感応度": 5,
        "健康意識": 8,
        "環境意識": 7,
        "社会的影響力": 6,
        "冒険心": 7,
        "家族重視度": 8
    }}
}}
"""

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    res = completion.choices[0].message.content.strip()
    
    # Remove markdown code block syntax if present
    res = re.sub(r'^```json\s*|\s*```$', '', res, flags=re.MULTILINE)
    
    try:
        return json.loads(res)
    except json.JSONDecodeError:
        # JSONの解析に失敗した場合、エラーメッセージを含む辞書を返す
        return {
            "error": "APIからの応答をJSONとして解析できませんでした。",
            "raw_response": res
        }

def create_persona():
    st.subheader("ペルソナを作成")

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.select_slider("年齢", options=list(range(18, 81)), value=30)
        gender = st.radio("性別", ["男性", "女性", "その他"])
        marital_status = st.selectbox("婚姻状況", ["未婚", "既婚", "離婚", "その他"])
        children = st.number_input("子供の数", min_value=0, max_value=10, value=0)

    with col2:
        education = st.selectbox("最終学歴", ["高校卒", "専門学校卒", "大学卒", "大学院卒", "その他"])
        occupation = st.selectbox("職業", [
            "学生", "会社員", "公務員", "自営業", "フリーランス", "専業主婦/主夫",
            "パート/アルバイト", "無職", "その他"
        ])
        income = st.select_slider("年収（万円）", options=[0] + list(range(200, 2001, 100)), value=400)
        location = st.selectbox("居住地", ["大都市", "中規模都市", "小規模都市", "郊外", "農村部"])

    with col3:
        interests = st.multiselect("興味・関心", [
            "テクノロジー", "ファッション", "スポーツ", "旅行", "料理", "音楽", "映画", "読書",
            "アート", "健康", "環境", "投資", "ゲーム", "ペット", "その他"
        ])
        values = st.multiselect("重視する価値観", [
            "家族", "キャリア", "健康", "自己実現", "社会貢献", "冒険", "安定", "創造性",
            "独立性", "伝統", "その他"
        ])
        tech_savviness = st.slider("テクノロジーへの親和性", 1, 5, 3)

    persona = f"""
年齢: {age}歳
性別: {gender}
婚姻状況: {marital_status}
子供の数: {children}人
最終学歴: {education}
職業: {occupation}
年収: {income}万円
居住地: {location}
興味・関心: {', '.join(interests)}
重視する価値観: {', '.join(values)}
テクノロジーへの親和性: {tech_savviness}/5
"""

    return persona

def display_radar_chart(scores):
    options = {
        "title": {"text": "ペルソナの特性スコア"},
        "tooltip": {"trigger": "axis"},
        "legend": {"data": ["スコア"]},
        "radar": {
            "indicator": [{"name": k, "max": 10} for k in scores.keys()]
        },
        "series": [{
            "name": "ペルソナスコア",
            "type": "radar",
            "data": [{"value": list(scores.values()), "name": "スコア"}]
        }]
    }
    st_echarts(options=options, height="400px")

def main():
    st.set_page_config(page_title="ペルソナAIナビゲーター", layout="wide")

    # Custom CSS
    st.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
        font-weight: bold;
    }
    .medium-font {
        font-size:20px !important;
        font-weight: bold;
    }
    .small-font {
        font-size:14px !important;
    }
    .highlight {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Load Lottie animation
    lottie_url = "https://assets5.lottiefiles.com/packages/lf20_V9t630.json"
    lottie_json = load_lottie_url(lottie_url)

    # Main content
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<p class="big-font">✨ ペルソナAIナビゲーター ✨</p>', unsafe_allow_html=True)
        st.write("ペルソナを作成し、AIが詳細なマーケティングインサイトを生成します。")

    with col2:
        st_lottie(lottie_json, height=200, key="lottie")

    # Create persona
    persona = create_persona()

    # Challenges
    st.subheader("課題と悩み")
    challenges = st.multiselect(
        "主な課題や悩みを選択してください（複数選択可）",
        ["時間管理", "ストレス解消", "健康維持", "スキルアップ", "人間関係", "資産運用",
         "仕事と家庭の両立", "デジタル活用", "自己実現", "キャリアアップ", "環境への配慮",
         "ワークライフバランス", "育児", "介護", "老後の不安", "その他"],
        key="challenges"
    )
    
    if "その他" in challenges:
        other_challenge = st.text_input("その他の課題や悩みを具体的に入力してください", key="other_challenge")
        challenges = [c if c != "その他" else other_challenge for c in challenges]

    if st.button("インサイトを生成", key="generate_button"):
        with st.spinner("インサイトを生成中..."):
            insights = generate_marketing_insights(persona, ", ".join(challenges))

        if "error" in insights:
            st.error(f"エラーが発生しました: {insights['error']}")
            st.text("APIからの生の応答:")
            st.code(insights['raw_response'])
        else:
            st.success("インサイトが生成されました！")

            # Display insights
            col1, col2 = st.columns(2)

            with col1:
                st.markdown('<p class="medium-font">デモグラフィック情報</p>', unsafe_allow_html=True)
                for point in insights["demographic"]:
                    st.markdown(f'<p class="small-font">• {point}</p>', unsafe_allow_html=True)
                
                st.markdown('<p class="medium-font">サイコグラフィック情報</p>', unsafe_allow_html=True)
                for point in insights["psychographic"]:
                    st.markdown(f'<p class="small-font">• {point}</p>', unsafe_allow_html=True)

            with col2:
                st.markdown('<p class="medium-font">ターゲットの課題</p>', unsafe_allow_html=True)
                for challenge in insights["challenges"]:
                    st.markdown(f'<p class="small-font">• {challenge}</p>', unsafe_allow_html=True)
                
                st.markdown('<p class="medium-font">キャッチフレーズ</p>', unsafe_allow_html=True)
                for phrase in insights["catchphrases"]:
                    st.markdown(f'<p class="small-font highlight">"{phrase}"</p>', unsafe_allow_html=True)

            # Display radar chart
            st.markdown('<p class="medium-font">ペルソナの特性分析</p>', unsafe_allow_html=True)
            display_radar_chart(insights["persona_scores"])

            # Add download button for insights
            st.download_button(
                label="インサイトをダウンロード",
                data=json.dumps(insights, ensure_ascii=False, indent=2),
                file_name="marketing_insights.json",
                mime="application/json",
            )

if __name__ == "__main__":
    main()