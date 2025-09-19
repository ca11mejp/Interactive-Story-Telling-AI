import gpt_call
import os
import json
from openai import OpenAI

# 🔑 Make sure you set your API key before running:
# export OPENAI_API_KEY="your_api_key_here"
client = OpenAI()

story_state = {
    "title": "",
    "beats": [],
    "current_index": 0,
}

def generate_outline(story_idea):
    """Ask GPT to create a simple plot outline with beats"""
    prompt = f"""
    Create a simple 3-beat story outline for this idea: {story_idea}.
    Return as numbered list, each beat in one sentence.
    """
    resp = gpt_call.gptcall(prompt)
    text = resp.choices[0].message.content
    beats = [line.strip("123. ") for line in text.splitlines() if line.strip()]
    return beats

def expand_beat(beat):
    """Expand a beat into story text with 2 choices"""
    prompt = f"""
    Expand this story beat into 2 short paragraphs of narrative prose.
    Then suggest 2 possible choices the hero can make.
    Return JSON with keys: text, choices.
    Beat: {beat}
    """
    resp = gpt_call.gptcall(prompt)
    return resp.choices[0].message.content

def main():
    print("📖 Interactive Story Generator")
    idea = input("Enter your story idea: ")
    story_state["title"] = idea
    story_state["beats"] = generate_outline(idea)

    print("\nGenerated plot outline:")
    for i, beat in enumerate(story_state["beats"], 1):
        print(f"Beat {i}: {beat}")

    # Start with first beat
    while story_state["current_index"] < len(story_state["beats"]):
        beat = story_state["beats"][story_state["current_index"]]
        print(f"\n--- Expanding Beat {story_state['current_index']+1} ---")
        result_json = expand_beat(beat)

        result = json.loads(result_json)

        print("\n" + result["text"] + "\n")
        for i, choice in enumerate(result["choices"], 1):
            print(f"{i}. {choice}")

        choice = input("Pick a choice (1/2) or 'q' to quit: ")
        if choice.lower() == "q":
            break

        # Just move to next beat (real branching comes later)
        story_state["current_index"] += 1

    print("\n✅ The End of the Story!")

if __name__ == "__main__":
    main()

