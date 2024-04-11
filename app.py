import streamlit as st
from openai import OpenAI
import os

from dotenv import load_dotenv, find_dotenv
_= load_dotenv(find_dotenv())
openapi_key = os.getenv('OPENAI_API_KEY')

import streamlit as st
from openai import OpenAI

def generate_marketing_insights(gender, age, additional_info, challenges):
    # プロンプト文の作成
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
"""

    # OpenAI APIを使用して回答を生成
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    res = completion.choices[0].message.content.strip()
    return res

# Streamlitアプリケーションの設定
st.set_page_config(page_title="コピーアプリ AiDist", layout="wide")

# タイトルの表示
st.title("AiDist")

# サイドバーの設定
st.sidebar.header("ターゲット情報入力")
gender = st.sidebar.radio("性別", ("男性", "女性"))
age = st.sidebar.radio("年齢", ("10代", "20代", "30代", "40代", "50代", "60代", "70代以上"))
additional_info = st.sidebar.text_input("その他の情報")

challenges = []
num_challenges = st.sidebar.number_input("悩み・課題の数", min_value=1, max_value=5, value=1)
for i in range(num_challenges):
    challenge = st.sidebar.text_input(f"悩み・課題 {i+1}", max_chars=40)
    challenges.append(challenge)

# インサイト生成ボタン
if st.button("インサイトを生成"):
    # マーケティングインサイトの生成
    insights = generate_marketing_insights(gender, age, additional_info, ", ".join(challenges))
    
    # 生成されたインサイトの表示
    st.subheader("マーケティングインサイト")
    st.write(insights)
