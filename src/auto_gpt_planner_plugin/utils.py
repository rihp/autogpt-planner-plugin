import tokenizers

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
    CONTEXT_MARKER = ""
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

def process_input_messages(messages):
    """Processes the input messages by chunking them based on token limits.

    Args:
        messages (list): The list of messages to be processed.

    Returns:
        list: A list of message chunks.
    """
    MAX_TOKENS = 4096
    CONTEXT_MARKER = ""
    message_chunks = []

    for message in messages:
        tokens = tokenizer.encode(message)

        if len(tokens) > MAX_TOKENS:
            current_chunk_tokens = []

            for token in tokens:
                if len(current_chunk_tokens) + 1 <= MAX_TOKENS:
                    current_chunk_tokens.append(token)
                else:
                    # Add contextual marker at the end of the chunk
                    current_chunk_tokens.append(tokenizer.encode(CONTEXT_MARKER))
                    message_chunks.append(tokenizer.decode(current_chunk_tokens))

                    # Add contextual marker at the beginning of the next chunk
                    current_chunk_tokens = [tokenizer.encode(CONTEXT_MARKER), token]

            if current_chunk_tokens:
                message_chunks.append(tokenizer.decode(current_chunk_tokens))
        else:
            message_chunks.append(message)

    return message_chunks
