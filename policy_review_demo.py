import streamlit as st
import openai

# 🧠 初始化 GPT Key（从 Streamlit Secrets 读取）
openai.api_key = st.secrets["OPENAI_API_KEY"]

# 📚 产品规则库（可扩充）
PRODUCT_KNOWLEDGE = {
    "SPWM": {
        "name": "SmartProtect Wealth Max",
        "base_life_multiplier": 1,
        "accident_multiplier": 2,
        "public_transport_multiplier": 3
    },
    "SPY": {
        "name": "SmartProtect You",
        "base_life_multiplier": 1
    },
    "SMM_200": {
        "name": "Smart Medic Million (200)",
        "room_and_board": "RM200",
        "annual_limit": "RM3,000,000",
        "features": ["No lifetime limit", "Auto upgrade every 5 years"]
    }
}

# 🧠 GPT 分析自然语言，并提取产品结构
def extract_from_gpt(user_input):
    prompt = f"""
你是一个保险规划分析助手，请从以下内容中识别保单产品与保额，输出格式如下：
{{
  "products": [
    {{ "code": "SPWM", "sum_assured": 500000 }},
    {{ "code": "SMM_200" }}
  ]
}}

如果没有金额，就不需填写 sum_assured。现在开始：
内容：{user_input}
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    output = response.choices[0].message.content.strip()
    try:
        return eval(output)
    except:
        return {"products": []}

# --- 页面设定 ---
st.title("🧾 Policy Review Demo v3")
st.markdown("🎙️ 你可以讲，也可以写，用自然语言输入保单资讯👇")

# --- 语音按钮占位（暂未启用）
st.subheader("🎤（开发中）语音功能测试")
st.info("目前语音功能界面已设定，若需完整语音转文字功能，请部署至本地服务器或启用 WebRTC 支援。")

# --- 用户输入区（主功能）
input_text = st.text_input("✍️ 请输入客户保单资讯：", placeholder="如：客户有一份SPWM 500千，还有SMM200医疗卡")

if input_text:
    st.subheader("📋 Review 报告：")
    result = extract_from_gpt(input_text)
    products = result.get("products", [])
    output = []

    for prod in products:
        code = prod["code"]
        info = PRODUCT_KNOWLEDGE.get(code)
        if not info:
            continue
        output.append(f"✅ 计划：{info['name']}")
        if code.startswith("SP"):
            bsa = prod.get("sum_assured", 0)
            life = bsa * info.get("base_life_multiplier", 1)
            accident = bsa * info.get("accident_multiplier", 0)
            pubtrans = bsa * info.get("public_transport_multiplier", 0)
            output.append(f"- 人寿保障：RM{int(life):,}")
            if accident:
                output.append(f"- 意外保障：RM{int(accident):,}")
            if pubtrans:
                output.append(f"- 公共交通意外：RM{int(pubtrans):,}")
        elif code.startswith("SMM"):
            output.append(f"- Room & Board：{info['room_and_board']}")
            output.append(f"- Annual Limit：{info['annual_limit']}")
            output.append(f"- 特别功能：{'、'.join(info['features'])}")

    if output:
        st.markdown("\n".join(output))
    else:
        st.warning("⚠️ 没有识别到可用的产品或格式，请检查输入内容")
