# Conversation

Once interaction with the LLM begins, the API will need to be called in a loop while it builds up enough information through various function calls. This stops once a function returns with `"stop": True`.

`{#conversation}: s`
```python
messages = [
    {"role": "system", "content": preamble},
    {"role": "user", "content": prompt},
]

print("System:")
print(preamble)

print("User:")
print(prompt)

output = { "stop": False }
while not output["stop"]:
    <#send existing messages>
    <#execute function>
    <#print function call and output>
    <#add to messages>
```

All of the arguments have been assembled elsewhere to call the API. We're using `gpt-3.5-turbo` right now because it's much cheaper than `gpt-4`, although it might make more sense to use the latter once the code interacting with it is stable.

`{#send existing messages}: s`
```python
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=messages,
    functions=function_footprints,
)
```

`{#execute function}: s`
```python
# Going to look at actual output first
print(response)
function_call = response["choices"][0]["message"]["function_call"]
```

The rest of the macros I'm going to leave unwritten until I have a chance to examine an actual response.

`{#print function call and output}: s`
```python
# Going to look at actual output first
print(f"{function_call['name']}({function_call['arguments']})")
```

`{#add to messages}: s`
```python
output = {"stop": True}
```
