from openai import OpenAI
import datasets, os, time
from tqdm import tqdm

client = OpenAI(api_key="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")

yes_messages = []
for i in range(0, 4, 2):
	with open(f"s{i+1}.txt", 'r') as file:
		yes_messages.append({'role': 'user', "content": file.read()})
		yes_messages.append({'role': 'assistant', "content": "Yes"})

# print(yes_messages)

dataset_no_logic = datasets.load_dataset('json', data_files="Pyranet_no_logic.jsonl", split = "train")

with open("last_i.txt", "r+") as file:
	file_read = file.read()
	if len(file_read):
		last_i = int(file_read)
	else:
		last_i = 0
	
	print("Run from i = ", last_i)
	time.sleep(5)

total_usage = 0
for i in tqdm(range(last_i, len(dataset_no_logic))):
	cur_code = dataset_no_logic['code'][i]

	completion = client.chat.completions.create(
	model="gpt-4o-mini",
	messages=[
		{"role": "developer", "content": "You are a helpful assistant to detect useless Verilog code."
		"These Verilog codes only contain definition keywords, such as module, input, inout, output, and endmodule."
		"And These Verilog codes don't contain keywords for logic operations such as assign, always, etc."
		"In constrast, a useful Verilog code is a code containing logic operation keywords, such as always, always_comb, always_ff, always_latch, or assign"
		"If you consider a Verilog code is useless, only answer \"Yes\", otherwise, \"No\". Don't explain anything."},
	] + yes_messages + [{"role": "user", "content": cur_code}]
	)
	res_message = completion.choices[0].message

	total_usage += completion.usage.total_tokens
	with open("usage.txt", 'w+') as file:
		file.write(str(completion.usage.total_tokens) + "\n" + str(total_usage))
	# print("Res: ", res_message)
	if "Yes" in res_message.content:
		# open(f"found/{i}", 'r+').close()
		os.system(f"touch found/{i}")
	with open("last_i.txt", "w") as file:
		file.write(str(i))


# print(completion.choices[0].message)