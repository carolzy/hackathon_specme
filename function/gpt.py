import os
import logging
from typing import Optional, List, Dict
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

# Initialize OpenAI client with API key and organization from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORGANIZATION")

class GPTInstance:
    def __init__(
        self,
        system_prompt: str = "You are a helpful assistant.",
        model: str = "gpt-4-turbo-preview",
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
        self, input: Optional[str] = None, role: str = "user", max_tokens: Optional[int] = None, *args, **kwargs
    ) -> Dict:
        history = self.messages[:]
        
        if input:
            history.append({"role": role, "content": input})
        
        functions = kwargs.pop("functions", self.functions)

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=history,
            functions=functions,
            max_tokens=max_tokens,
            *args,
            **kwargs
        )

        output = response.choices[0].message
        self.logger.info(output)
        
        if self.keep_state:
            self.messages.append(output)
        
        return output

