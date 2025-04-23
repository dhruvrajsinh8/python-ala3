import os
import openai

# Set your OpenAI API key as an environment variable before running the app
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_text(prompt, model="gpt-3.5-turbo", max_tokens=100):
    """
    Generate text from GPT based on the given prompt.
    """
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error generating text: {str(e)}"
