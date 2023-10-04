# LLM Revisions

Tome projects inherently provide much greater natural language context around the code that they construct, which could make revisions by LLMs really effective. OpenAI has an official Python package, which we will need to include in the project:

`{#dependencies}: s`
```
openai==0.28.0
```

In order to interact with the ChatGPT API, a little bit of logic is needed to send the prompt to the API:

`{#send prompt}: s`
```python
import os
import openai

openai.api_key = os.environ['TOME_OPENAI_API_KEY']

<Preamble.md#system>
<Revision.md#prompt>

messages = [
    {"role": "system", "content": system},
    {"role": "user", "content": prompt},
]

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages
)
```
