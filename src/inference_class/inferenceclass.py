from langchain_community.llms import LlamaCpp
import sys
from huggingface_hub import InferenceClient
from openai import OpenAI
from openai.types.chat import ChatCompletion

providers = {
	"llamacpp": "LLamaCPPInferenceClient",
	"huggingface": "HuggingFaceInferenceClient",
	"openai": "OpenAiInferenceClient"
}

default_provider = list(providers.keys())[0]
class InferenceClass():
	def __new__(cls, provider: str, *args, **kwargs):
		print(f"Using provider: {provider}")
		if provider in providers:
			return getattr(sys.modules[__name__],providers[provider])(*args, **kwargs)
		else:
			raise Exception(f"Provider {provider} not supported. Supported providers are: {list(providers.keys())}")

class GeneralInferenceClass():
	def __init__(self, model: str, max_tokens: int, temperature: float, top_p: float):
		self.model = model
		self.max_tokens = max_tokens
		self.temperature = temperature
		self.top_p = top_p
	def invoke(self, prompt: list[str]) -> tuple[str, dict]:
		pass
	def free_model(self):
		pass

n_gpu_layers = -1  # The number of layers to put on the GPU. The rest will be on the CPU. If you don't know how many layers there are, you can use -1 to move all to GPU.
n_batch = 512  # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.
n_ctx=16384,

class LLamaCPPInferenceClient(GeneralInferenceClass):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.llm = LlamaCpp(
			model_path=self.model,
			# model_path="/home/thanh/vllm/GNU_COMBA/src/codellama-7b.Q4_K_M.gguf",
			# model_path="/home/thanh/Downloads/ggml-model-q4_0.gguf",
			n_gpu_layers=n_gpu_layers,
			n_batch=n_batch,
			max_tokens=self.max_tokens,
			n_ctx=n_ctx,
			# callback_manager=callback_manager,
			# verbose=True,  # Verbose is required to pass to the callback manager
			temperature=self.temperature,
			verbose=False
		)
	def invoke(self, prompt: list[str]):

		response : str = self.llm.invoke('\n'.join(prompt))
		return (response, {})
	def free_model(self):
		self.llm.client.close()


class HuggingFaceInferenceClient(GeneralInferenceClass):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		print(f"Loading model from HuggingFace: {self.model}")
		self.llm = InferenceClient(
			model=self.model,
			base_url="https://ivamvf7duqa3vwwl.us-east-1.aws.endpoints.huggingface.cloud"
		)
	def invoke(self, prompt: list[str]):
		# response : str = self.llm.invoke(prompt)
		messages = [{"role": "user", "content": message} for message in prompt]
		response = self.llm.chat_completion(messages=messages, max_tokens=self.max_tokens, temperature=self.temperature)

		return (response.choices[0].message, 
		  {"completion_tokens": response.usage.completion_tokens,
		 	"prompt_tokens": response.usage.prompt_tokens,
		   "total_tokens": response.usage.total_tokens})

class OpenAiInferenceClient(GeneralInferenceClass):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		print(f"Loading model from HuggingFace: {self.model}")
		self.llm = OpenAI(
			base_url = "https://a3tj6snd966fb5rq.us-east-1.aws.endpoints.huggingface.cloud/v1/",
			api_key = "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",
			
		)
	def invoke(self, prompt: list[str]):
		# response : str = self.llm.invoke(prompt)
		messages = [{"role": "user", "content": message} for message in prompt]
		# print(messages)
		# exit(123)
		response = self.llm.chat.completions.create(
			model=self.model,
			messages=messages,
			max_tokens=self.max_tokens, 
			temperature=self.temperature,
			top_p=self.top_p,
			
		)
		# response = self.llm.chat_completion(messages=[{"role": "user", "content": prompt}], max_tokens=self.max_tokens, temperature=self.temperature)

		return (response.choices[0].message.content, 
		  {"completion_tokens": response.usage.completion_tokens,
		 	"prompt_tokens": response.usage.prompt_tokens,
		   "total_tokens": response.usage.total_tokens})