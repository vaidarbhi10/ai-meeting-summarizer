from transformers import pipeline

generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-base"
)

def generate_mom(text):

    prompt = f"""
    Convert this meeting transcript into structured Minutes of Meeting.

    Give:
    1. Summary
    2. Key Discussion Points
    3. Action Items (clear bullet points)

    Transcript:
    {text}
    """

    result = generator(prompt, max_length=300, do_sample=False)[0]["generated_text"]

    # simple split (optional improvement later)
    action_items = []
    if "Action" in result:
        action_items = result.split("Action")[-1].split("\n")

    return result, action_items