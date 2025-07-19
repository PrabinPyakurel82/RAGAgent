import spacy

nlp = spacy.load('en_core_web_sm')

def semantic_sentence_chunk(text:str,max_chunk_size=500):
    document = nlp(text)
    sentences = [sentence.text.strip() for sentence in document.sents]

    chunks=[]
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence)  + 1 > max_chunk_size:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
        else:
            current_chunk += " " + sentence if current_chunk else sentence
    
    if current_chunk:
        chunks.append(current_chunk.strip())
        
    return chunks



