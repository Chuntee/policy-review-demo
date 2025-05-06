import streamlit as st

# --- 知识库逻辑设定 ---
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

# --- 页面设置 ---
st.title("🧾 Insurance Policy Review Demo")
st.markdown("为保险代理人打造的智能整理工具 💼")

# --- 用户输入 ---
input_text = st.text_input("请输入客户保单资讯：", placeholder="如：客户有SPWM 500k + SMM_200")

if input_text:
    st.subheader("📋 Review 报告：")
    lines = input_text.upper().replace(",", "").split(" ")
    output = []

    for i, word in enumerate(lines):
        if word in PRODUCT_KNOWLEDGE:
            product = PRODUCT_KNOWLEDGE[word]
            label = word

            # 主计划处理
            if label.startswith("SP"):
                try:
                    bsa = float(lines[i+1].replace("K", "")) * 1000
                except:
                    bsa = 0
                life = bsa * product.get("base_life_multiplier", 1)
                accident = bsa * product.get("accident_multiplier", 0)
                pubtrans = bsa * product.get("public_transport_multiplier", 0)
                output.append(f"✅ 主计划：{product['name']}")
                output.append(f"- 人寿保障：RM{int(life):,}")
                if accident:
                    output.append(f"- 意外保障：RM{int(accident):,}")
                if pubtrans:
                    output.append(f"- 公共交通意外：RM{int(pubtrans):,}")

            # 医疗卡处理
            elif label.startswith("SMM"):
                output.append(f"✅ 医疗卡：{product['name']}")
                output.append(f"- Room & Board：{product['room_and_board']}")
                output.append(f"- Annual Limit：{product['annual_limit']}")
                output.append(f"- 特别功能：{'、'.join(product['features'])}")

    if output:
        st.markdown("\n".join(output))
    else:
        st.warning("⚠️ 无法识别输入内容，请确认格式或关键字。")