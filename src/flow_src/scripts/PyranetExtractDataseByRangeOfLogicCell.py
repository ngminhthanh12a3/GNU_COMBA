from BaseProcess import BaseProcessClass

from datasets import load_dataset
from tqdm import tqdm
from transformers import AutoTokenizer
from dotenv import load_dotenv
import glob, numpy as np, os, sys
# from module_extraction import module_extraction
# from multiprocessing.managers import BaseManager
# from multiprocess import Pool

load_dotenv()



class PyranetExtractDataseByRangeOfLogicCell(BaseProcessClass):
	def run(self):
		print(self.trigger_path)
		sys.path.append(self.trigger_path)

		model_name = "unsloth/Qwen2.5-Coder-7B-Instruct"
		# model_name = "meta-llama/Llama-2-7b-hf"

		# model = AutoModelForCausalLM.from_pretrained(model_name,
		#                                             #  torch_dtype=torch.float16
		#                                              )
		tokenizer = AutoTokenizer.from_pretrained(model_name,
												# torch_dtype=torch.float16
												)
		
		dataset = load_dataset('bnadimi/PyraNet-Verilog', split = "train")

		all_num_cell_file = glob.glob(f"{self.trigger_path}/.cache_count_num_cell_2/*")

		all_cell_num_with_no_null = np.array([[None, None]] * len(dataset))
		all_cell_num_with_no_null

		def do_process(i):
			filename_path = all_num_cell_file[i]
			file_name = os.path.basename(filename_path)
			logic_index = int(file_name.replace(".txt", ""))
			# print(file_name)
			with open(filename_path, 'r') as file:
				file_list = file.read().split(",")
				return (logic_index, tuple(file_list))
			
		# num_core = int(os.cpu_count()/2)
		my_range = range(len(all_num_cell_file))
		# print(f"Using {num_core} cores for processing {len(all_num_cell_file)} files. ", __name__)

		pool = self.global_obj["pool"]

		# for i in tqdm(iterable=pool.imap_unordered(do_process, range(100000)), total=100000):
		# 	pass

		# with Pool(processes=num_core) as pool:
		
		for i in tqdm(iterable=pool.imap_unordered(do_process, my_range), total=len(my_range)):
			logic_index, file_list = i
			all_cell_num_with_no_null[logic_index][0] = int(file_list[0])
			all_cell_num_with_no_null[logic_index][1] = int(file_list[1]) if file_list[1] != 'None' else None
		
		all_cell_num_with_no_null = all_cell_num_with_no_null[:,1]
		all_cell_num_with_no_null = np.column_stack((all_cell_num_with_no_null, range(len(dataset))))
		all_cell_num_null_idx = np.where(all_cell_num_with_no_null[:, 0] != None)
		# dataset_filter = dataset.select(all_cell_num_null_idx[0])
		all_cell_num_with_no_null = all_cell_num_with_no_null[all_cell_num_null_idx].astype(np.uint64)
		all_cell_num_with_no_null = np.column_stack((all_cell_num_with_no_null.astype(object), [''] * len(all_cell_num_with_no_null)))
		max_cell = np.max(all_cell_num_with_no_null[:,0])
		max_cell_idxs = np.where(all_cell_num_with_no_null[:,0] == max_cell)[0]
		all_cell_num_with_no_null[max_cell_idxs]

		for i in range(len(all_cell_num_with_no_null)):
			int_x = all_cell_num_with_no_null[i][0]
			if int_x == 0:
				all_cell_num_with_no_null[i][2] = '0-0'
			else:
				start_i = 1
				stop_i = 41
				step_i = 5
				for ii in range(start_i,stop_i, step_i):
					cur_range = (ii, ii + step_i - 1)
					if cur_range[0] <= int_x <= cur_range[1]:
						all_cell_num_with_no_null[i][2] = f'{cur_range[0]}-{cur_range[1]}'
						break
		
		# all_cell_num_with_no_null = np.column_stack((all_cell_num_with_no_null, dataset_filter['token_length']))
		
		all_cell_num_with_no_null_0_100 = all_cell_num_with_no_null[:, 0:2]
		all_cell_num_with_no_null_0_100 = np.column_stack((all_cell_num_with_no_null_0_100, [None] * len(all_cell_num_with_no_null_0_100)))

		start_i = 1
		stop_i = 40
		step_i = 5
		for i in range(len(all_cell_num_with_no_null_0_100)):
			int_x = all_cell_num_with_no_null_0_100[i][0]
			if int_x == 0:
				all_cell_num_with_no_null_0_100[i][2] = '0-0'
				# pass
			else:
				for ii in range(start_i,stop_i, step_i):
					cur_range = (ii, ii + step_i - 1)
					if cur_range[0] <= int_x <= cur_range[1]:
						all_cell_num_with_no_null_0_100[i][2] = f'{cur_range[0]}-{cur_range[1]}'
						break
		
		filter_idxs = np.where(all_cell_num_with_no_null_0_100[:, 2] != None)[0]
		old_training_idxs = np.array([])
		# setdiff1d_of2 = np.setdiff1d(filter_idxs, old_training_idxs, assume_unique=True)
		# dataset_ranges = np.unique(all_cell_num_with_no_null_0_100[:, 2])
		segment_idxs = np.where(all_cell_num_with_no_null_0_100[:, 2] == '0-0')[0]
		segment_idxs_2 = np.where(all_cell_num_with_no_null_0_100[:, 2] == '1-5')[0]
		segment_idxs = np.concatenate((segment_idxs, segment_idxs_2))
		
		dataset = dataset.select(segment_idxs)
		self.global_obj["dataset"] = dataset
		print(dataset)

		np.save(f"{self.trigger_path}/TrainDataset/train_index2_{0}_{5}.npy", segment_idxs)
