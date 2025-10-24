#!/usr/bin/env python
import os, glob
SRCDIR = os.path.realpath(os.path.dirname(__file__))
prompt = ""

with open(SRCDIR + '/prompt.txt', 'r') as file:
	prompt = file.read()


VerilogEvalDatasetDir = os.path.realpath(SRCDIR + '/../ext/verilog-eval/dataset_code-complete-iccad2023')

VerilogEvalDatasetPromts = glob.glob(VerilogEvalDatasetDir + '/*prompt.txt')
VerilogEvalDatasetPromts.sort()

for datasetpromptdir in VerilogEvalDatasetPromts:

	datasetprompt = ""
	with open(datasetpromptdir, 'r') as file:
		datasetprompt = file.read()

	datasetPromtFilename = os.path.basename(datasetpromptdir)
	# datasetPromtDirName = os.path.dirname(datasetpromptdir)
	datasetRefFileName = datasetPromtFilename.replace('prompt.txt', 'ref.sv')
	datasetRefDir = VerilogEvalDatasetDir + '/' + datasetRefFileName

	datasetRefPrompt = ""
	with open(datasetRefDir, 'r') as file:
		datasetRefPrompt = file.read()

	print(f"""{prompt}

{datasetprompt}

The reference code for the module is:

{datasetRefPrompt}""")
	
	break
	