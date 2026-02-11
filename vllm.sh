# conda create -n vllm python=3.10 -y
# conda activate vllm
# pip install --upgrade uv --cache-dir pip_cache/
# uv pip install vllm --torch-backend=cu124 --cache-dir pip_cache/

# nohup vllm serve nvmthanhhcmus/LORAV-DeepSeek-Coder --config vllm.yaml > vllm.out &

vllm serve nvmthanhhcmus/LORAV-DeepSeek-Coder --config vllm.yaml