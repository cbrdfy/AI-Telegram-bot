import openai

# This should be added to the database instead
MESSAGES_LOG = []

def openai_response(user_token, user_message, model):
    """
    Function sends a response from OpeanAI API based on attributes
    like how the system should act, max number of tokens, temperature.
    It could be increased and tweaked as desired.
    """
    global MESSAGES_LOG
    personality = {
        'role': 'system', 
        'content': 'You are a Motoko Kusanagi from Ghost in the Shell. Answer as concisely as possible.'
    }

    openai.api_key = user_token

    if not MESSAGES_LOG:
        MESSAGES_LOG.append(personality)

    messages_log = MESSAGES_LOG + [{'role': 'user', 'content': user_message}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages_log,
        max_tokens=1024,
        temperature=0.7
    )
    
    openai_response = response['choices'][0]['message']['content']
    messages_log.append({'role': 'assistant', 'content': openai_response})
    MESSAGES_LOG = messages_log
    # print(f'MSG_LOG: {MESSAGES_LOG}')
    return openai_response