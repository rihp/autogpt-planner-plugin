import tokenizers
import re

# Global constants
tokenizer = tokenizers.ByteLevelBPETokenizer()

def process_response(response):
    """Processes the response by chunking it based on token limits.

    Args:
        response (str): The response to be processed.

    Returns:
        list: A list of response chunks.
    """
    MAX_TOKENS = 4096
    CONTEXT_MARKER = "<|context|>"
    tokens = tokenizer.encode(response)
    
    if len(tokens) > MAX_TOKENS:
        chunks = []
        current_chunk_tokens = []
        
        for token in tokens:
            if len(current_chunk_tokens) + 1 <= MAX_TOKENS:
                current_chunk_tokens.append(token)
            else:
                # Add contextual marker at the end of the chunk
                current_chunk_tokens.append(tokenizer.encode(CONTEXT_MARKER))
                chunks.append(tokenizer.decode(current_chunk_tokens))
                
                # Add contextual marker at the beginning of the next chunk
                current_chunk_tokens = [tokenizer.encode(CONTEXT_MARKER), token]
        
        if current_chunk_tokens:
            chunks.append(tokenizer.decode(current_chunk_tokens))
        
        return chunks
    else:
        return [response]
