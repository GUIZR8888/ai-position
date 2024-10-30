import streamlit as st
from zhipuai import ZhipuAI

# 初始化ZhipuAI模型
model = ZhipuAI(api_key='3a5ab4fe724fe28e879e67ff38cabcf2.4KRNENWgpA9hOYnL')

# 如果session_state中没有cache，则初始化一个空列表
if "cache" not in st.session_state:
    st.session_state.cache = []

# 获取用户输入
desc = st.chat_input("请输入图片的描述")

# 如果有描述信息
if desc:
    # 将用户输入的内容以用户角色输出到界面上，并添加到缓存
    with st.chat_message("user"):
        st.write(desc)
    st.session_state.cache.append({"role": "user", "content": desc})

    # 调用智谱AI的文生图大模型生成图片
    try:
        response = model.images.generations(
            model="cogview-3-plus",  # 填写需要调用的模型编码
            prompt=desc,
        )

        # 将响应数据添加到缓存
        st.session_state.cache.append({
            "role": "assistant",
            "image_url": response.data[0].url if response and response.data else None
        })
    except Exception as e:
        st.error(f"图片生成失败: {str(e)}")
        st.session_state.cache.append({
            "role": "assistant",
            "error": str(e)
        })

# 显示聊天记录中的所有消息
for message in st.session_state.cache:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.write(message["content"])
        elif message["role"] == "assistant":
            if "image_url" in message and message["image_url"]:
                st.image(message["image_url"], width=300)
            elif "error" in message:
                st.error(message["error"])