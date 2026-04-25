import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Global Pitch Assistant", page_icon="🌍", layout="wide")

with st.sidebar:
    st.header("⚙️ 使い方ガイド")
    st.write("1. 海外案件をコピペ")
    st.write("2. 案件の下にスキルと実績を日本語で記入してください")
    st.write("例：日本語がネイティブ")
    st.write("３. 「英語の提案文を作成」を押してください。")
    st.write("４. 結果が表示されます。")
    st.divider()
    st.info("💡 ヒント: 具体的な数値や、得意な分野（Web開発、デザインなど）を入れるとより強力な文章になります。")

st.title("🌍 Global Pitch Assistant")
st.markdown("#### 〜 あなたのスキルを世界へ。プロフェッショナルな英語提案文を10秒で作成 〜")
st.divider()

col1, col2 = st.columns(2)

# ========== 左側：入力エリア ==========
with col1:
    st.subheader("📝 入力エリア")
    user_input = st.text_area(
        "仕事内容、スキルまたは実績をコピペしてください",
        height=200, 
        placeholder="例：ネイティブの日本語話者です。語学力を活かし、機械翻訳のような直訳ではない、自然なニュアンスの英日翻訳を提供します。ビジネス文書やアプリのローカライズ（日本語化）が得意です。"
    )
    
    # 🌟 新機能：トーン選択ボタンを追加！ 🌟
    st.markdown("##### 🎯 提案文のトーンを選んでください")
    tone = st.radio(
        "トーンの選択",
        ["🧑‍💼 プロフェッショナル（丁寧）", "🤝 フレンドリー（親しみやすい）", "🔥 情熱的（熱意とやる気を伝える）"],
        label_visibility="collapsed" # 見た目をスッキリさせるための魔法
    )
    st.write("") # 少し隙間を空ける
    
    send = st.button("🚀 英語の提案文を作成", use_container_width=True)

# ========== 右側：結果表示エリア ==========
with col2:
    st.subheader("✨ 作成結果")
    
    if send:
        if user_input:
            with st.spinner("AIが最高のピッチを執筆中です...⏳"):
                try:
                    api_key = st.secrets["API_KEY"]
                    genai.configure(api_key=api_key)

                    # 🌟 超重要：プロンプト（指示書）を徹底的に鍛え上げる！ 🌟
                    my_system_prompt = f"""
                    あなたは海外案件の獲得をサポートする「プロの営業アシスタント」です。
                    ユーザーが入力した日本語のスキルや実績を元に、海外のクライアントの心を掴む英語の提案文（カバーレター）を作成してください。

                    【厳守するルール】
                    1. 文章のトーンは「{tone}」にしてください。
                    2. 最初に、クライアントの目を引く魅力的なメールの「件名（Subject）」を作成してください。
                    3. 本文の中で、ユーザーの強みを「3つの箇条書き（Bullet points）」で分かりやすく整理してアピールしてください。
                    4. 最後に、「ぜひ面談の機会をください」という前向きなCall to Action（行動喚起）を入れてください。
                    5. 英語の提案文が完成したら、改行して【日本語訳】という見出しをつけ、その下に正確な日本語の翻訳を必ず記載してください。
                    """

                    model = genai.GenerativeModel(
                        'gemini-2.5-flash',
                        system_instruction=my_system_prompt
                    )

                    response = model.generate_content(user_input)
                    gemini_answer = response.text
                    st.success("完成しました！内容をコピーして使ってください。")
                    st.info(gemini_answer)
                except Exception:
                    st.error("現在システムが混み合っています。1分ほど待ってからもう一度お試しください🙇‍♂️")
        else:
            st.warning("⚠️ スキルや実績を入力してください！")
    else:
        st.write("左側のボタンを押すと、ここに結果が表示されます。")