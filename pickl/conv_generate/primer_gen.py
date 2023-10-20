from pathlib import Path

# pickl package for internal use
from pickl import PROMPT_DIR
from pickl.conv_generate.model import Bot


def generate_primers(
    system_prompt: str,
    user_prompt: str,
    topic_list: list[str],
) -> list[dict[str, list[dict[str, str]]]]:
    """Create conversation starters for each topic using ChatGPT."""
    # Iterate over topics
    primer_list = []

    for topic in topic_list:
        # Replace TOPIC with topic
        topic_prompt = user_prompt.replace("{{topic}}", topic)

        # Prepare ChatGPT payload
        chatgpt = Bot(system_prompt, topic_prompt)

        # Get ChatGPT Response, load as JSON, and append to primer_list
        response = chatgpt.generate_response(temperature=1, return_json=True)
        primer_list.append(response)

    return primer_list


if __name__ == "__main__":
    # --- Load Prompts ---
    sys_prompt = Path(PROMPT_DIR,  "primer_gen_system.txt").read_text()
    prompt = Path(PROMPT_DIR, "primer_gen.txt").read_text()

    # --- Generate Primers ---
    primers = generate_primers(
        system_prompt=sys_prompt,
        user_prompt=prompt,
        topic_list=["Gaming", "Weather", "(HUB)Event"],
    )
