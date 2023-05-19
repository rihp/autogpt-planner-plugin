import tokenizers

# Global constants
tokenizer = tokenizers.ByteLevelBPETokenizer()

def process_response(response):
    """Processes the response by chunking it based on token limits."""
    MAX_TOKENS = 4096
    tokens = len(tokenizer.encode(response))
    if tokens > MAX_TOKENS:
        chunks = []
        words = response.split()
        current_chunk = ""
        for word in words:
            if len(tokenizer.encode(current_chunk + " " + word)) <= MAX_TOKENS:
                current_chunk += " " + word
            else:
                chunks.append(current_chunk.strip())
                current_chunk = word
        if current_chunk:
            chunks.append(current_chunk.strip())
        return chunks
    else:
        return [response]
