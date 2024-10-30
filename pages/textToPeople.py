#基于历史聊天记录的对话模型
#制作聊天界面
import streamlit as st
#langchain调用大模型，导入langchain的代码
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
#构建一个大模型
model = ChatOpenAI(
    temperature=0.8,#温度，创新型
    model="glm-4-plus",#大模型名称
    base_url="https://open.bigmodel.cn/api/paas/v4/",#大模型地址，接口文档第三方框架内
    api_key="3d463c10aee8e0a730fd293dfd118fac.b8fKeb7nUCpc9wxp"#账号信息 个人API
)
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(memory_key="history")
#memory=ConversationBufferMemory(memory_key="history")
prompt=PromptTemplate.from_template("你的名字叫ggBoy，你现在扮演一个生理性别为男，心理性别为女的角色，"
                                    "你的性格怪异，你现在要和你的朋友进行对话，你朋友说的话是{input},"
                                    "你需要对你朋友的话作出回应，而且只做回应，你和你朋友的历史对话为{history}")
chain=LLMChain(
    llm=model,
    prompt=prompt,
    memory=st.session_state.memory,
)
st.title("你有个朋友叫ggBoy")
if "cache" not in st.session_state:
    st.session_state.cache = []
else:
    for message in st.session_state.cache:
        with st.chat_message(message['role']):
            st.write(message["content"])
@st.cache_data
def invoke_model(problem, history):
    # 将历史记录和当前问题合并作为输入
    full_input = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history]) + f"\nuser: {problem}"
    return model.invoke(full_input)
#创建一个聊天输入框
problem = st.chat_input("变态的ggBoy正在等待你的回应")
#判断用来确定用户有没有输入问题 若输入
if problem:
    #1.将用户的问题输出界面，以用户角色
    with st.chat_message("user"):
        st.write(problem)
    st.session_state.cache.append({"role":"user","content":problem})

    #2.调用大模型回答问题
    result = chain.invoke({"input": problem})
    with st.chat_message("assistant"):
        st.write(result['text'])

    st.session_state.cache.append({"role": "assistant", "content": result})