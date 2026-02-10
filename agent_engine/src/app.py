import streamlit as st
from graph import graph

st.set_page_config(page_title="SecureOrder AI", page_icon="🛡️")
st.title("🛡️ SecureOrder AI: Enterprise Procurement")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Welcome to SecureOrder AI. How can I assist with your procurement today?"}]

# Display Chat
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# User Input
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    # Run the Graph
    inputs = {"messages": st.session_state.messages, "order_data": {}, "requires_approval": False}
    config = {"configurable": {"thread_id": "1"}}
    
    final_state = graph.invoke(inputs, config)
    answer = final_state["messages"][-1].content
    
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.chat_message("assistant").write(answer)