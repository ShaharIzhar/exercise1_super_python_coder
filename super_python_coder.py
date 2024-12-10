import pdb
from openai import OpenAI
import subprocess
import random

#ProgramS List Params
PROGRAMS_LIST=[
  '''Given two strings str1 and str2, prints all interleavings of the given
  two strings. You may assume that all characters in both strings are
  different.Input: str1 = "AB", str2 = "CD"
  Output:
  ABCD
  ACBD
  ACDB
  CABD
  CADB
  CDAB
  Input: str1 = "AB", str2 = "C"
  Output:
  ABC
  ACB
  CAB "''', #PROGRAM 1
  "A program that checks if a number is a palindrome", #PROGRAM 2
  "A program that finds the kth smallest element in a given binary search tree." #PROGRAM 3
  "A program that writes the sum of isopsephy of a given sentence", #PROGRAM 4 - Geometria (hebrew)
  "A program that is a Soduko Validator - make user enter a 9x9 Sudoku grid row by row (use 0 for empty cells)" #PROGRAM 5
]

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

def super_python_coder_gpt_response(request_input):
  guidelines_prompt = '''based on user input, Do not write any explanations, just show me the code itself to put in a file.
  Also please include running unit tests with asserts that check the logic of the program. 
  Make sure to also check interesting edge cases. There should be at least 10 different unit tests, do not run the tests, run the main logic only'''
  if request_input != "":
    return openai_create_request(request_input + guidelines_prompt)
  
  return openai_create_request(random.choice(PROGRAMS_LIST) + guidelines_prompt)

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

#Remove headers and footers of gpt prompt in code snippet return
def clean_prompt_response(response_content):
  cleaned_response = '\n'.join(response_content.splitlines()[1:-1])
  
  return cleaned_response

def generate_process_file(gpt_response):
  generated_file_name = "generatedcode.py"
  write_to_file(generated_file_name, gpt_response)
  file_path = "./generatedcode.py"

  return file_path

#Exmple prompt: "Create a python program that checks if a number is prime."
request_input = input("I’m Super Python Coder. Tell me, which program would you like me to code for you? If you don't have an idea,just press enter and I will choose a random program to code: \n")
gpt_response = super_python_coder_gpt_response(request_input)
file_path = generate_process_file(gpt_response)
subprocess.run(["python", file_path])
