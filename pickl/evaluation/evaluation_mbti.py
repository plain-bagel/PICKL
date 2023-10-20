import json
from pathlib import Path

from pickl import PROMPT_DIR, TOPIC_DIR
from pickl.conv_generate.model import Bot


# Type aliases
PreferencePair = dict[str, int]
MBTIType = dict[str, PreferencePair]


def evaluate_mbti(system_prompt: str, mbti_prompt: str, conv_group: list[str]) -> dict[str, str | MBTIType]:
    """Evaluate model MBTI based on groups of conversations"""

    # Add parameters into prompt
    mbti_prompt = mbti_prompt.replace("{{num_dialogue}}", str(len(conv_group)))
    # Insert conversation group into prompt
    conversation_string = ""
    for i, conv in enumerate(conv_group):
        conv_str = "\n".join(conv)
        conversation_string += f"conversation {i+1}:\n{conv_str}"
        conversation_string += "\n\n" if i != len(conv_group) - 1 else ""
    mbti_prompt = mbti_prompt.replace("{{conversations}}", conversation_string)

    # Query ChatGPT with conversation MBTI payload
    chatgpt = Bot(system_prompt, mbti_prompt)
    response: MBTIType = chatgpt.generate_response(temperature=0, return_json=True)

    # Calculate MBTI(Simple) - requires further processing for real use
    energy = "E" if response["b_energy"]["extroverted"] > response["b_energy"]["introverted"] else "I"
    information = "S" if response["b_information"]["sensitive"] > response["b_information"]["intuition"] else "N"
    conclusion = "T" if response["b_conclusion"]["thinking"] > response["b_conclusion"]["feeling"] else "F"
    approach = "J" if response["b_approach"]["judging"] > response["b_approach"]["perceiving"] else "P"

    return {"mbti": energy + information + conclusion + approach, "preferences": response}


if __name__ == "__main__":
    # Prepare Conversation group
    with Path(TOPIC_DIR, "sample_data.json").open() as f:
        data = json.load(f)

    conversation_group = data[0]["conversations"]
    num_dialogue = len(conversation_group)

    # Load Prompts
    sys_prompt = Path(PROMPT_DIR, "evaluation_system.txt").read_text()
    prompt = Path(PROMPT_DIR, "evaluation_mbti.txt").read_text()

    # Evaluate MBTI
    results = evaluate_mbti(sys_prompt, prompt, conversation_group)
