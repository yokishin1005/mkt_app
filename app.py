import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv
import json
from streamlit_lottie import st_lottie
import requests

# Load environment variables
_ = load_dotenv(find_dotenv())
openapi_key = os.getenv('OPENAI_API_KEY')

# Initialize OpenAI client
client = OpenAI()

def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def generate_marketing_insights(gender, age, additional_info, challenges):
    prompt = f"""
あなたは、世界で屈指の優秀なマーケティングプロフェッショナルです。
以下の情報をまずは読み込んでください

ターゲットの情報:
- 性別: {gender}
- 年齢: {age}
- その他: {additional_info}
- 悩み、課題: {challenges}

Based on the provided data, use inference to write bullet points outlining the key points and details for the following three items. 
Ensure that you cover all the defined information and provide specific details in approximately 500 characters in Japanese. 
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

4.キャッチフレーズ:
    Based on the insights from points 1, 2, and 3, propose at least five catchphrases that would likely appeal to and attract the targeted persona.
    Craft compelling and memorable phrases that resonate with the target's demographic profile, psychographic characteristics, and specific needs.
    Use language and tone that align with the target's preferences and communication style to create a strong emotional connection and motivate action.
    Highlight the unique benefits, solutions, or experiences that the product, service, or brand offers to address the target's challenges and fulfill their desires.
    Aim for concise, impactful, and easily understandable catchphrases that effectively communicate the core message and value proposition.
    Present the proposed catchphrases in a bullet-point format, ensuring each catchphrase is clearly distinguishable and stands on its own.

Please format your response as a JSON object with the following structure:
{
    "demographic": "デモグラフィック情報のテキスト",
    "psychographic": "サイコグラフィック情報のテキスト",
    "challenges": "ターゲットの課題のテキスト",
    "catchphrases": ["キャッチフレーズ1", "キャッチフレーズ2", "キャッチフレーズ3", "キャッチフレーズ4", "キャッチフレーズ5"]
}
"""

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    res = completion.choices[0].message.content.strip()
    return json.loads(res)

def main():
    st.set_page_config(page_title="マーケティングインサイト生成器", layout="wide")

    # Load Lottie animation
    lottie_url = "https://assets5.lottiefiles.com/packages/lf20_V9t630.json"
    lottie_json = load_lottie_url(lottie_url)

    # Sidebar
    with st.sidebar:
        st.header("ターゲット情報入力")
        gender = st.radio("性別", ("男性", "女性"), key="gender")
        age = st.select_slider("年齢", options=["10代", "20代", "30代", "40代", "50代", "60代", "70代以上"], key="age")
        additional_info = st.text_area("その他の情報", key="additional_info")
        
        challenges = []
        num_challenges = st.number_input("悩み・課題の数", min_value=1, max_value=5, value=1, key="num_challenges")
        for i in range(num_challenges):
            challenge = st.text_input(f"悩み・課題 {i+1}", max_chars=40, key=f"challenge_{i}")
            challenges.append(challenge)

    # Main content
    col1, col2 = st.columns([2, 1])

    with col1:
        st.title("マーケティングインサイト生成器")
        st.write("ターゲットの情報を入力し、AIが詳細なマーケティングインサイトを生成します。")

    with col2:
        st_lottie(lottie_json, height=200, key="lottie")

    if st.button("インサイトを生成", key="generate_button"):
        with st.spinner("インサイトを生成中..."):
            insights = generate_marketing_insights(gender, age, additional_info, ", ".join(challenges))

        st.success("インサイトが生成されました！")

        # Display insights
        col1, col2 = st.columns(2)

        with col1:
            with st.expander("デモグラフィック情報", expanded=True):
                st.write(insights["demographic"])
            
            with st.expander("サイコグラフィック情報", expanded=True):
                st.write(insights["psychographic"])

        with col2:
            with st.expander("ターゲットの課題", expanded=True):
                st.write(insights["challenges"])
            
            with st.expander("キャッチフレーズ", expanded=True):
                for phrase in insights["catchphrases"]:
                    st.markdown(f"- {phrase}")

        # Add download button for insights
        st.download_button(
            label="インサイトをダウンロード",
            data=json.dumps(insights, ensure_ascii=False, indent=2),
            file_name="marketing_insights.json",
            mime="application/json",
        )

if __name__ == "__main__":
    main()