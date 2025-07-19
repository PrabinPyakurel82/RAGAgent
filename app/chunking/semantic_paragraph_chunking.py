from langchain.text_splitter import CharacterTextSplitter

def semantic_paragraph_chunk(text):
    splitter = CharacterTextSplitter(
        separator="\n\n", 
        chunk_size=500,
        chunk_overlap=50,
    )
    return splitter.split_text(text)