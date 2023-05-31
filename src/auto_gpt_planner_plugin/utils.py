import os
import openai
import backoff
from transformers import GPT2Tokenizer

# Global constants
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

completion_tokens = prompt_tokens = 0

# Set up OpenAI API key and base URL
api_key = os.getenv("OPENAI_API_KEY", "")
if api_key != "":
    openai.api_key = api_key
else:
    print("Warning: OPENAI_API_KEY is not set")

api_base = os.getenv("OPENAI_API_BASE", "")
if api_base != "":
    print("Warning: OPENAI_API_BASE is set to {}".format(api_base))
    openai.api_base = api_base

@backoff.on_exception(backoff.expo, openai.error.OpenAIError)
def completions_with_backoff(**kwargs):
    """
    Generate text using the OpenAI API with exponential backoff in case of errors.

    Args:
        **kwargs: A dictionary of keyword arguments to pass to the OpenAI API.

    Returns:
        A list of generated text.
    """
    return openai.ChatCompletion.create(**kwargs)

def process_response(response):
    """
    Process the response by chunking it based on token limits.

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
    """
    Process the input messages by chunking them based on token limits.

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

def gpt(messages, model="gpt-4", temperature=0.7, max_tokens=1000, n=1, stop=None) -> list:
    """
    Generate text using the OpenAI API.

    Args:
        messages (list): The list of messages to be processed.
        model (str): The model to use for generating text.
        temperature (float): The temperature to use for generating text.
        max_tokens (int): The maximum number of tokens to generate.
        n (int): The number of generations to perform.
        stop (str): A string that, if encountered, will cause the generation to stop.
        
        Returns:
        list: A list of generated texts.
    """
    prompts = process_input_messages(messages)
    completions = []

    for prompt in prompts:
        completion = completions_with_backoff(model=model, messages=[{"role": "system", "content": prompt}],
                                              temperature=temperature, max_tokens=max_tokens, n=n, stop=stop)
        completions.append(completion.choices[0].message.content)

    responses = []

    for completion in completions:
        chunks = process_response(completion)
        responses.extend(chunks)

    return responses
