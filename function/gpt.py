import streamlit as st
import logging
from typing import Optional, List, Dict

import openai
from openai import OpenAI

APIKEY = st.secrets['API_KEY']
client = OpenAI(api_key=APIKEY, organization="org-k1IoKv4XS4Q9nVvPQsHhXzSp")
from dotenv import load_dotenv

load_dotenv()


class GPTInstance:
    def __init__(
        self,
        system_prompt: str = "You are a helpful assistant.",
        model="gpt-4-turbo-preview",
        keep_state: bool = True,
        temperature: float = 0,
        logger_name: str = __name__,
        functions: Optional[List] = None,
    ):
        self.model = model
        self.messages = [{"role": "system", "content": system_prompt}]
        self.keep_state = keep_state
        self.temperature = temperature
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)
        self.functions = functions

    def __call__(
        self, input: Optional[str] = None, role: str = "user", max_tokens=None, *args, **kwargs
    ) -> Dict:

        history = [*self.messages]

        if input:
            history.append({"role": role, "content": input})

        functions = kwargs.pop("functions", self.functions)

        if max_tokens:
            output = client.chat.completions.create(model=self.model, messages=history, functions=functions, max_tokens=max_tokens, *args, **kwargs)
        else:
            output = client.chat.completions.create(model=self.model, messages=history, functions=functions, *args, **kwargs)

        output = output.choices[0].message

        self.logger.info(output)

        if self.keep_state:
            self.messages.append(output)

        return output
