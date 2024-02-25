from anthropic_bedrock import AnthropicBedrock, HUMAN_PROMPT, AI_PROMPT
client = AnthropicBedrock(
    aws_access_key="AKIA47CRU3YWEUFX4BAK",
    aws_secret_key="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",
    aws_region="eu-central-1",
)
def get_response(prompt:str, tmp:float=0.8, prnt:bool=False,):
    r"""
- [Req] prompt: message to the bot. (Use of the HUMAN_PROMPT and AI_PROMPT is required)
    - Use: get_response(prompt=f"{HUMAN_PROMPT}[MESSAGE HERE]{AI_PROMPT}[OPTIONAL AI STARTING MESSAGE]", ..., ...)
- [Opt] tmp: The temperature, higher values indicates more creativity [from 0.0 to 1.0]
    - Use: get_response(..., tmp=[Put desired temperature here], ...)
- [Opt] prnt: if True, automatically print the AI message in stream and later return the AI message, else return the AI message when it's complete.
    - Use: get_response(..., ..., prnt=[True or False])
    """
    message = ""
    output = client.completions.create(
    model="anthropic.claude-v2:1",
    prompt=prompt,
    temperature=tmp,
    stream=True
)
    for event in output:
        message += event.completion
        if prnt:print(event.completion, end="")
    return message
get_response