import pdb
from openai import OpenAI
import subprocess
import random
import time
from colorama import init, Fore, Back, Style
from tqdm import tqdm

#Programs List Params
GUIDELINES_PROMPT = '''based on user input, Do not write any explanations, just show me the code itself to put in a file.
Also please include running unit tests with asserts that check the logic of the program. 
Make sure to also check interesting edge cases. There should be at least 10 different unit tests'''

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
  "A program that calculates how many saturdays i have been going through since an inputed year" #PROGRAM 5
]

#OpenAI Init
client = OpenAI()
client_messages = [{"role": "system", "content": "You are a helpful assistant."}]


def openai_request(prompt):
  latest_message = { "role": "user", "content": prompt }
  client_messages.append(latest_message)

  completion = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=client_messages
  )
  
  chat_response = completion.choices[0].message.content
  client_messages.append({"role": "assistant", "content": chat_response})
  
  return chat_response

def super_python_coder_gpt_response(request_input):
  if request_input != "":
    return openai_request(request_input + GUIDELINES_PROMPT)
  
  return openai_request(random.choice(PROGRAMS_LIST) + GUIDELINES_PROMPT)

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

#Remove headers and footers of gpt output in code snippet return
def clean_prompt_response(response_content):
  cleaned_response = '\n'.join(response_content.splitlines()[1:-1])
  
  return cleaned_response

def generate_process_file(gpt_response):
  generated_file_name = "generatedcode.py"
  write_to_file(generated_file_name, gpt_response)
  file_path = "./generatedcode.py"

  return file_path

def subprocess_run_logic(file_path, retries_num):
  if retries_num > 5: 
    print(Fore.RED + "Code generation FAILED" + Fore.RESET)
    return
  
  try:
    start_time =  time.time()
    subprocess.run(["python", file_path], check=True)
    end_time = time.time()
    elapsed_time=end_time - start_time
    if(elapsed_time): return round(elapsed_time, 4)
 
  except subprocess.SubprocessError as error_message:
    print(Fore.YELLOW + f"code generation unsuccessfull - trying again - ({retries_num})" + Fore.RESET)
    updated_response = openai_request(f"please fix the code based on the following error: {error_message} {GUIDELINES_PROMPT}")
    generate_process_file(updated_response)
    subprocess_run_logic(file_path, retries_num + 1)

def optimized_code_runner():
  updated_code = openai_request("great, now run the same unit tests but make the code more efficient")
  generate_process_file(updated_code)

  elapsed_time = subprocess_run_logic(file_path, retries_num=0)
  return elapsed_time

def elapsed_time_handler(before_elapsed_time, improved_elapsed_time):
    if(elapsed_time > improved_elapsed_time):
      print(f"Code running time optimized! It now runs in {improved_elapsed_time} milliseconds, while before it was {elapsed_time} milliseconds")

def lint_error_checker(file_path):
  result = subprocess.run(
            ["pylint", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
  if result.returncode == 0: return True
  else: return False

def lint_code_optimizer(file_path, retries_num):
  if not lint_error_checker(file_path): return Fore.GREEN + "Amazing. No lint errors/warnings" + Fore.RESET
  if retries_num > 3: return Fore.YELLOW + "There are still lint errors/warnings"

  updated_response = openai_request(f"please check the code for pylint errors, if it has lint errors, fix them. {GUIDELINES_PROMPT}")
  generate_process_file(updated_response)
  lint_code_optimizer(file_path, retries_num + 1)

#Exmple prompt: "Create a python program that checks if a number is prime."
code_generation_total_steps = 3
with tqdm(total=code_generation_total_steps, desc="Code Generation Progress", ncols=100, dynamic_ncols=True) as pbar:
  request_input = input(Fore.GREEN + "I’m Super Python Coder. Tell me, which program would you like me to code for you? If you don't have an idea,just press enter and I will choose a random program to code: \n" + Fore.RESET)
  pbar.update(1)
  pbar.set_description("Contacting Chat...")
  gpt_response = super_python_coder_gpt_response(request_input)
  pbar.update(1)
  pbar.set_description("Updating code locally...")
  file_path = generate_process_file(gpt_response)
  pbar.update(1)

print("\n\n Running Code:")
elapsed_time = subprocess_run_logic(file_path, retries_num=0)
if(elapsed_time):
  improved_elapsed_time = subprocess_run_logic(file_path, retries_num=0)
  elapsed_time_handler(elapsed_time, improved_elapsed_time)

  lint_status = lint_code_optimizer(file_path, retries_num=0)
  print(lint_status)
