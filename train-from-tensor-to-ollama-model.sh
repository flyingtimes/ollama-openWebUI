#!/bin/bash

# trainning using data/ folder 
HF_ENDPOINT=https://hf-mirror.com mlx_lm.lora --model Qwen/Qwen2.5-72B-Instruct  --data data/ --train --iters 3000 --batch-size 4 --lora-layers 16 --adapter-path adapters/Qwen2.5-72B-$1

# fuse model
mlx_lm.fuse --model Qwen/Qwen2.5-72B-Instruct --adapter-path adapters/Qwen2.5-72B-FT-$1  --save-path gguf-models/Qwen2.5-72B-$1

# transfer to gguf
python convert-hf-to-gguf.py gguf-models/Qwen2.5-72B-$1 --outtype q8_0

# copy modelfile
cp qwen_modelfile.txt gguf-models/Qwen2.5-72B-$1

# create ollama model
cd gguf-models/Qwen2.5-72B-$1;ollama create qwen72b-$1 -f qwen_modelfile.txt

# remove middle files
rm -rf adapters/Qwen2.5-72B-$1
rm -rf gguf-models/Qwen2.5-72B-$1