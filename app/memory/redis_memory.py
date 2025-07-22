from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import RedisChatMessageHistory


def get_memory(session_id:str):
    message_history = RedisChatMessageHistory(
        session_id=session_id,
        url="redis://localhost:6379"
    )
    memory = ConversationBufferMemory(
        chat_memory=message_history,
        return_messages=True,
        memory_key='chat_history'
    )
    return memory