# 项目目标
在192GB的macstudio上，完成全量72b级别模型的微调训练，并量化后部署到ollama
> mlx微调gguf-->合并gguf-->gguf导入ollama-->webUI运行示例

## 环境准备
### 一、部署 mlx
```
# mlx框架
pip install mlx
# 微调相关
pip install mlx_lm
```

### 二、部署 ollama+webui
> mac下的docker不支持调用GPU的能力，因此ollama使用原生mac版本的程序来跑，其他部分docker-compose-webuiONLY的方式跑起来

> windows/linux服务器带GPU的，用docker-compose-gpu方式跑起来

> 不具备GPU的服务器，使用docker-compose-cpu方式跑起来

部署示例：
```
docker compose -f xx.yaml up -d
```

### 三、准备模型文件和modelfile文件

```
# 从huggingface 拉取模型
ollama pull hf-mirror.com/Qwen/Qwen2.5-1.5B-Instruct-GGUF:q4_0
# 获取modelfile文件
ollama show --modelfile YOUR-MODEL-NAME > modelfile.txt
```



## 开始训练并部署到ollama
### 一、微调训练
```
# qwen1.5B
HF_ENDPOINT=https://hf-mirror.com mlx_lm.lora --model Qwen/Qwen2.5-1.5B-Instruct  --data data/ --train --iters 1000 --batch-size 32 --lora-layers 8 --adapter-path adapters/Qwen2.5-1.5B-FT-1109
# qwen72B
HF_ENDPOINT=https://hf-mirror.com mlx_lm.lora --model mlx-community/Qwen2.5-72B-Instruct  --data data/ --train --iters 3000 --batch-size 16 --lora-layers 8 --adapter-path adapters/Qwen2.5-72B-FT-1110
# nemotron
mlx_lm.lora --model mlx-community/nvidia_Llama-3.1-Nemotron-70B-Instruct-HF_4bit --data data/  --train --iters 3000 --batch-size 4 --lora-layers 12 --adapter adapter/nemotro
```

### 二、合并模型
```
# qwen
mlx_lm.fuse --model Qwen/Qwen2.5-1.5B-Instruct --adapter-path adapters/Qwen2.5-1.5B-FT-1109  --save-path gguf-models/qwen2-1.5b-FT-1109
# qwen72b
mlx_lm.fuse --model Qwen/Qwen2.5-72B-Instruct --adapter-path adapters/Qwen2.5-72B-FT-1110  --save-path gguf-models/qwen2-72b-FT-1110
# nemotron
mlx_lm.fuse --model mlx-community/nvidia_Llama-3.1-Nemotron-70B-Instruct-HF_4bit --adapter-path adapter/nemotron   --save-path gguf-models/nemotron-FT-1110
```
### 三、转换gguf
使用llama.cpp项目里面的程序
```
# 转换,qwen72b
python convert-hf-to-gguf.py ../ollama-openWebUI/gguf-models/qwen2-72b-FT-1110
# 量化(可选)
./quantize old-gguf-f16.gguf new-gguf-q4_0.gguf q4_0
```
### 四、将一个本地模型导入ollama
```
# 要先修改modelfile文件，将其与gguf文件绑定
ollama crate YOUR-MODEL-NAME -f /path/to/your/modelfile.txt
```

## 一键脚本
```
bash train-from-tensor-to-ollama-model.sh YOUR_TRAIN_NAME
```

## 文档的解析处理

#### 部署一个mark_server，用于接收用户文档，并解析成markdown
```
# dockerfile 文件参考 marker_docker.dockerfile
docker pull dockerpull.org/dibz15/marker_docker
```
调用方式
```
docker run -v .\documents\:/pdfs dockerpull.org/dibz15/marker_docker python convert_single.py /pdfs/1.pdf /pdfs/1.md --parallel_factor 2 --max_pages 10

```
#### 使用convert_pdfs.py批量处理pdf文件
```
# 基本用法
python convert_pdfs.py ./documents ./output

# 指定并行因子和最大页数
python convert_pdfs.py ./documents ./output --parallel_factor 4 --max_pages 20
```

> 使用cursor 完成convert_pdf的编写，并测试通过。
>> 写一个python程序，遍历输入文件夹中的所有子目录，对于其中的pdf文件做如下处理：调用marker_docker程序将pdf转换为md格式文件，并将所有输出文件保存到输出文件夹中 ***