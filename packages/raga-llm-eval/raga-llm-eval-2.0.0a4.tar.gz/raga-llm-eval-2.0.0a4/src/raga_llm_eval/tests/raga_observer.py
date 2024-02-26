import time
from functools import wraps

from openai import OpenAI

client = OpenAI()


class raga_observer(object):

    def __init__(self, function):
        self.count = 0
        self.timetaken = list()
        self.tokensused = list()
        self.wrapper = dict()
        self.function = function

    def __call__(self, *args, **kwargs):
        self.count += 1
        response = self.function(self.wrapper, *args, **kwargs)
        self.timetaken.append(self.wrapper["timetaken"])
        self.tokensused.append(self.wrapper["response"].usage.total_tokens)
        print(self.timetaken)
        return response


"""
def raga_observer(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        response = function(wrapper, *args, **kwargs)
        print(wrapper.response.usage.total_tokens)
        print(wrapper.timetaken)
        return response
    return wrapper
"""


@raga_observer
def call_openai_service(w, prompt):
    """
    Calls open ai service to get the response for the given prompt.

    Args:
        prompt(str): the prompt given to the model

    Returns:
        dict: A dictionary containing the prompt, response, total_tokens and timetaken for the openai response
    """
    messages = [{"role": "user", "content": prompt}]
    t1 = time.time()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,
        max_tokens=1000,
        top_p=0.5,
        n=1,
        frequency_penalty=0.1,
        presence_penalty=0.1,
    )
    timetaken = time.time() - t1
    w.response = response
    w.timetaken = timetaken
    contents = []
    for choice in response.choices:
        # Check if the response is valid
        if choice.finish_reason not in ["stop", "length"]:
            raise ValueError(f"OpenAI Finish Reason Error: {choice.finish_reason}")
        contents.append(choice.message.content)
    return_response = {
        "prompt": prompt,
        "timetaken": w.timetaken,
        "response": contents[0],
        "tokens_used": response.usage.total_tokens,
    }
    return return_response
