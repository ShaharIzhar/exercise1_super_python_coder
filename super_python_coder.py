from openai import OpenAI

#OpenAI Init
client = OpenAI()

def openai_create_request(prompt):
  completion = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
          {"role": "system", "content": "You are a helpful assistant."},
          {
              "role": "user",
              "content": prompt
          }
      ]
  )
  
  return completion.choices[0].message.content

request_input = "Create a python program that checks if a number is prime. Do not write any explanations, just show me the code itself."
print(openai_create_request(request_input))
