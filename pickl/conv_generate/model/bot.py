import json
from typing import Any

import openai
from tenacity import retry, stop_after_attempt, wait_random_exponential


class Bot:
    """Bot model(ChatGPT) class"""

    def __init__(self, system_prompt: str, prompt: str) -> None:
        self.system_prompt = system_prompt
        self.prompt = prompt
        self.conv_history = self.reset_history()
        self.max_retry = 4

    def reset_history(self) -> list[dict[str, str]]:
        """Reset the query to the initial state."""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": self.prompt},
        ]
        self.conv_history = messages
        return messages

    @retry(wait=wait_random_exponential(min=15, max=30), stop=stop_after_attempt(4))
    def generate_response(self, model: str = "gpt-4", temperature: float = 1, return_json: bool = False) -> Any:
        """ChatGPT API request"""
        response = openai.ChatCompletion.create(
            model=model,
            messages=self.conv_history,
            temperature=temperature,
        )
        response = response["choices"][0]["message"]["content"]

        if return_json:
            # Will retry if response is not JSON parsable (@retry)
            response = json.loads(str(response))

        return response

    def add_bot_response(self, text: str | None = None) -> str:
        """Add response from the A model to the conversation history."""
        response: str = self.generate_response(return_json=False) if text is None else text
        self.conv_history.append({"role": "assistant", "content": response})
        return response

    def add_user_response(self, text: str) -> str:
        """Get response from the B model and add to the conversation history."""
        self.conv_history.append({"role": "user", "content": text})
        return text
