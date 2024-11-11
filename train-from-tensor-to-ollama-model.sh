#!/bin/bash
date
# trainning using data/ folder ,resume
#HF_ENDPOINT=https://hf-mirror.com mlx_lm.lora --model Qwen/Qwen2.5-72B-Instruct  --data data/ --train --iters 5000 --batch-size 4 --lora-layers 16  --adapter-path adapters/Qwen2-72B-$1 --resume-adapter-file adapters/Qwen2-72B-$1/0000400_adapters.safetensors

# trainning using data/ folder 
HF_ENDPOINT=https://hf-mirror.com mlx_lm.lora --model Qwen/Qwen2.5-72B-Instruct  --data data/ --train --iters 3000 --batch-size 4 --lora-layers 16  --adapter-path adapters/Qwen2-72B-$1 
date
# fuse model
mlx_lm.fuse --model Qwen/Qwen2.5-72B-Instruct --adapter-path adapters/Qwen2-72B-$1  --save-path gguf-models/Qwen2-72B-$1
date
# transfer to gguf
python convert-hf-to-gguf.py gguf-models/Qwen2-72B-$1 --outtype q8_0
date
# copy modelfile
cp qwen_modelfile.txt gguf-models/Qwen2-72B-$1
date
# create ollama model
cd gguf-models/Qwen2-72B-$1;ollama create qwen72b-$1 -f qwen_modelfile.txt
date
# remove middle files
rm -rf gguf-models/Qwen2-72B-$1
date