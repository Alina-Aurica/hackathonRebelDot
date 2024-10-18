import openai


def translate_text(text, target_language):
    prompt = f"Translate the following text to {target_language}:\n\n{text}"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful translation assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    translated_text = response.choices[0].message['content'].strip()
    return translated_text

