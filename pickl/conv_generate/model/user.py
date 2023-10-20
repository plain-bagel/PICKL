import requests


class User:
    """User model(Examinee) class"""

    def __init__(self, url: str) -> None:
        self.url = url
        self.conv_history = self.reset_history()
        self.max_retry = 4

    def reset_history(self) -> list[dict[str, str]]:
        """Reset the query to the initial state."""
        self.conv_history = []
        return []

    def generate_response(self) -> dict[str, list[dict[str, str]]]:
        """Send generate response request to the test model"""
        count = 0
        while count < self.max_retry:
            # Send POST request to B model server
            response = requests.post(self.url, json={"messages": self.conv_history})
            # Check response status code
            if response.status_code == 200:
                data: dict[str, list[dict[str, str]]] = response.json()
                return data
            elif response.status_code == 400:
                break
            elif response.status_code == 500:
                raise Exception(f"Error: Server error. {response.text}")
            count += 1
        raise Exception("Error: Failed to get response from server.")

    def add_bot_response(self, text: str) -> str:
        """Add response from the A model to the conversation history."""
        self.conv_history.append({"speaker": "A", "message": text})
        return text

    def add_user_response(self, text: str | None = None) -> str:
        """Get response from the B model and add to the conversation history."""
        response = self.generate_response() if text is None else text
        chat: str = (
            str(" ".join(item["message"] for item in response.get("response", [])))
            if isinstance(response, dict)
            else str(response)
        )

        self.conv_history.append({"speaker": "B", "message": chat})
        return chat
