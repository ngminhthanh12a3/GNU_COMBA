#!/usr/bin/env python

import atexit, json
import os, glob, sys
from langchain_community.llms import LlamaCpp
# from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate
from tqdm import tqdm
import argparse

#
workDir = os.getcwd()
srcDir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(f"{srcDir}/inference_class"))

from inferenceclass import InferenceClass

#-------------------------------------------------------------------------
# Command line processing
#-------------------------------------------------------------------------

class ArgumentParserWithCustomError(argparse.ArgumentParser):
  def error( self, msg = "" ):
    if ( msg ): print("\n ERROR: %s" % msg)
    print("")
    file = open( sys.argv[0] )
    for ( lineno, line ) in enumerate( file ):
      if ( line[0] != '#' ): sys.exit(msg != "")
      if ( (lineno == 2) or (lineno >= 4) ): print( line[1:].rstrip("\n") )

def parse_cmdline():
    p = ArgumentParserWithCustomError( add_help=False )

    p.add_argument( "-x", "--samples",    type=int,   default=1 )
    p.add_argument( "-h", "--help",        action="store_true" )
    p.add_argument( "-p", "--provider",       type=str,   default="llamacpp")
    p.add_argument( "-n", "--max-tokens",  type=int,   default=2048 )
    p.add_argument( "-t", "--temperature", type=float, default=0.85 )
    p.add_argument( "-m", "--model",       type=str,   default="gpt-3.5-turbo" )
    p.add_argument( "-P", "--top-p",       type=float, default=0.95 )
    # p.add_argument( "-v", "--verbose",     action="store_true" )
    # p.add_argument( "-l", "--list-models", action="store_true" )
    # p.add_argument( "-e", "--explain",     action="store_true" )
    # p.add_argument( "-x", "--examples",    type=int,   default=0 )
    # p.add_argument( "-r", "--rules",       action="store_true" )
    # p.add_argument(       "--output",      type=str,   default="-" )
    # p.add_argument(       "--base-url",    type=str,   default=None)
    # p.add_argument(       "--task",        type=str,   default="code-complete-iccad2023" )
    # p.add_argument( "prompt_filename" )

    opts = p.parse_args()
    if opts.help: p.error()
    return opts

examples_icl = [{
    "instruction": """Implement the Verilog module based on the following description. Assume that signals are positive clock/clk triggered unless otherwise stated.

The module should implement an incrementer which increments the input by
one and writes the result to the output. Assume all values are encoded as
two's complement binary numbers.
""",
    "module_def": """module TopModule
(
  input  logic [7:0] in_,
  output logic [7:0] out
);

""",
"response": """
<hdls>
<hdl>
<module_definition>
module TopModule
(
  input  logic [7:0] in_,
  output logic [7:0] out
);
</module_definition>
<module_code>
  // Combinational logic

  assign out = in_ + 1;

endmodule
</module_code>
</hdl>
</hdls>
"""
},
{"instruction": """Implement the Verilog module based on the following description. Assume that signals are positive clock/clk triggered unless otherwise stated.

The module should implement an 8-bit registered incrementer with an
active-high synchronous reset. The 8-bit input is first registered and
then incremented by one on the next cycle. The internal state should be
reset to zero when the reset input is one. Assume all values are encoded
as two's complement binary numbers. Assume all sequential logic is
triggered on the positive edge of the clock.
""",
    "module_def": """module TopModule
(
  input  logic       clk,
  input  logic       reset,
  input  logic [7:0] in_,
  output logic [7:0] out
);
""",
"response": """
<hdls>
<hdl>
<module_definition>
module TopModule
(
  input  logic       clk,
  input  logic       reset,
  input  logic [7:0] in_,
  output logic [7:0] out
);
</module_definition>
<module_code>
// Sequential logic

  logic [7:0] reg_out;

  always @( posedge clk ) begin
    if ( reset )
      reg_out <= 0;
    else
      reg_out <= in_;
  end

  // Combinational logic

  logic [7:0] temp_wire;

  always @(*) begin
    temp_wire = reg_out + 1;
  end

  // Structural connections

  assign out = temp_wire;

endmodule
</module_code>
</hdl>
</hdls>
"""
},
]

template = """Below is an instruction that describes a Verilog module, paired with a module definition that provides further context for input and output ports. Write a response that only completes the code of Verilog module, inside XML tags and without other descriptions.

### Instruction:
{instruction}

Place the completion of the Verilog module in an XML tag <hdls></hdls>.
Inside the XML tag, all partial modules constructing the Verilog module, are placed inside a child XML tag <hdl></hdl>.
In each partial tag, the tag <module_definition></module_definition> is used to place the module definition of that module and
the tag <module_code></module_code> is used to place the module code of that module.

### Module Definition:
{module_def}

### Response:
{response}
"""

prompt = PromptTemplate.from_template(template)


problemDir = f"{srcDir}/../ext/verilog-eval/dataset_code-complete-iccad2023"

problemPromptsPath = glob.glob(f"{problemDir}/Prob*_prompt.txt")


def main():
    
    opts = parse_cmdline()
    
    num_samples = opts.samples

    max_tokens = opts.max_tokens
    temperature = opts.temperature
    provider = opts.provider
    # Make sure the model path is correct for your system!
    model = opts.model
    top_p = opts.top_p
    
    global inference_client
    inference_client = InferenceClass(
        # model="/home/thanh/vllm/GNU_COMBA/src/codellama-7b.Q4_K_M.gguf",
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        provider=provider,
        top_p=top_p
    )
    @atexit.register
    def free_model():
        inference_client.free_model()
    
    global pbar
    pbar = tqdm(total=len(problemPromptsPath) * num_samples)
    problemPromptsPath.sort()
    for problemPromptPath in problemPromptsPath:
        problemPrompt = ""
        with open(problemPromptPath, 'r') as file:
            problemPrompt = file.read()
        # print(problemPrompt)
        problemModuleDefStart = problemPrompt.rfind("module TopModule")
        problemModuleDef = problemPrompt[problemModuleDefStart:]
        problemModuleDescription = problemPrompt[:problemModuleDefStart]
        
        # resp = llm_chain.invoke({"instruction": problemModuleDescription, "module_def": problemModuleDef})
        problemPromptFileName = os.path.basename(problemPromptPath)
        problemPromptFileNameNoSuffix = problemPromptFileName[:problemPromptFileName.rfind("_prompt.txt")]
        
        if not os.path.exists(problemPromptFileNameNoSuffix):
            os.makedirs(problemPromptFileNameNoSuffix)
        
        inputprompt: list[str] = []
        for example in examples_icl:
            inputprompt += [template.format(**example)]
            
        inputprompt += [template.format(instruction=problemModuleDescription, module_def=problemModuleDef, response="")]
        with open(f"{problemPromptFileNameNoSuffix}/{problemPromptFileNameNoSuffix}_customprompt.txt", 'w+') as file:
            print('\n'.join(inputprompt), file=file)
        # print(inputprompt)
        # break
        for i in range(1,num_samples + 1):
            
            resp, resp_statistic = inference_client.invoke(inputprompt)
            
            with open(f"{problemPromptFileNameNoSuffix}/{problemPromptFileNameNoSuffix}_sample{i:02d}_response_all.txt", 'w+') as file:
                print(resp, file=file)
            
            with open(f"{problemPromptFileNameNoSuffix}/{problemPromptFileNameNoSuffix}_sample{i:02d}_statistic.json", 'w+') as file:
                json.dump(resp_statistic, file)

            module_code_tags = ["<module_code>", "</module_code>"]
            codeStart = resp.find(module_code_tags[0])
            codeEnd = resp.find(module_code_tags[1])
            if codeStart > -1 and codeEnd > -1 and codeStart < codeEnd:
                resp = resp[len(module_code_tags[0]) + codeStart:codeEnd]
            else:
                resp = ""
                
            with open(f"{problemPromptFileNameNoSuffix}/{problemPromptFileNameNoSuffix}_sample{i:02d}_response.txt", 'w+') as file:
                print(resp, file=file)
            
            pbar.update(1)
        # print(problemPromptFileNameNoSuffix)
        # with open
        # print("### Resp:\n", resp)
        # continue
        # break

def EndProcesdures():
    inference_client.free_model()
    pbar.close()

if __name__ == "__main__":
    try:
        main()
        EndProcesdures()
    except KeyboardInterrupt:
        EndProcesdures()

