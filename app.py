# 以下を「app.py」に書き込み
import streamlit as st
import openai
import langchain
import os

#langchain関連のモジュールを読み込み
from langchain.llms import OpenAI
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory

openai.api_key = st.secrets.OpenAIAPI.openai_api_key
os.environ["OPENAI_API_KEY"] = st.secrets.OpenAIAPI.openai_api_key

llm = OpenAI(model_name="text-davinci-003", temperature=0.2)
tool_names = ["llm-math"]
tools = load_tools(tool_names, llm=llm)

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
)

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)

system_prompt = """
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]
    bot_message = agent.run(st.session_state["user_input"])
    messages.append(bot_message)

    
#    if len(messages) > 0:
#        user_message = {"role": "user", "content": st.session_state["user_input"]}
#        messages.append(user_message)
#        bot_message = agent.run(st.session_state["user_input"])
#        messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("計算.bot")
st.write("計算問題を出してください。")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        st.write(message)
#        speaker = "🙂"
#        if message["role"]=="assistant":
#            speaker="🔮"
#
#        st.write(speaker + ": " + message["content"])
