import pdb
from openai import OpenAI
import subprocess

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

def write_to_file(file_name, txt_content):
  fixed_file_name = validate_python_file_extension(file_name)
  fixed_prompt_content = clean_prompt_response(txt_content)
  file = open(fixed_file_name, "w")

  file.write(fixed_prompt_content)
  file.close()

def validate_python_file_extension(file_name):
  split_array_min_length = 2
  if len(file_name.split('.')) < split_array_min_length: 
    return file_name+".py"
  
  return file_name

#Remove headers and footers of gpt prompt in case code snippet returned
def clean_prompt_response(response_content):
  cleaned_response = '\n'.join(response_content.splitlines()[1:-1])
  
  return cleaned_response

#Exmple prompt: "Create a python program that checks if a number is prime. Do not write any explanations, just show me the code itself to put in a file. Also please include running unit tests with asserts that check the logic of the program. Make sure to also check interesting edge cases. There should be at least 10 different unit tests"
request_input = input("Enter GPT Prompt: \n")
gpt_response = openai_create_request(request_input)

generated_file_name = "generatedcode.py"
write_to_file(generated_file_name, gpt_response)

file_path = "./generatedcode.py"
subprocess.run(["python", file_path])
