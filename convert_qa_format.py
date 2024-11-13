import sys
import json
import random

def parse_conversation(text):
    # 分割对话内容
    lines = text.strip().split('\n')
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        }
    ]
    
    for line in lines:
        if not line.strip():  # 跳过空行
            continue
            
        # 分割说话者和内容
        if ':' in line:
            speaker, content = line.split(':', 1)
            speaker = speaker.strip()
            content = content.strip()
            
            # 将A说的话映射为assistant，B说的话映射为user
            role = "assistant" if speaker == "A" else "user"
            messages.append({
                "role": role,
                "content": content
            })
    
    return {"messages": messages}

def convert_file(input_file, output_train_file, output_valid_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f_in:
            # 读取整个文件内容
            content = f_in.read()
            # 按一个或多个空行分割成多组对话
            conversations = [conv for conv in content.split('\n\n') if conv.strip()]
            
        # 随机打乱数据
        random.shuffle(conversations)
        
        # 计算训练集和验证集的分割点
        split_point = int(len(conversations) * 0.9)
        train_convs = conversations[:split_point]
        valid_convs = conversations[split_point:]
        
        # 写入训练集
        with open(output_train_file, 'w', encoding='utf-8') as f_train:
            for conv in train_convs:
                output_data = parse_conversation(conv)
                f_train.write(json.dumps(output_data, ensure_ascii=False) + '\n')
                
        # 写入验证集
        with open(output_valid_file, 'w', encoding='utf-8') as f_valid:
            for conv in valid_convs:
                output_data = parse_conversation(conv)
                f_valid.write(json.dumps(output_data, ensure_ascii=False) + '\n')
                
        print(f"转换完成！")
        print(f"训练集已保存为：{output_train_file}，共 {len(train_convs)} 条对话")
        print(f"验证集已保存为：{output_valid_file}，共 {len(valid_convs)} 条对话")
        
    except FileNotFoundError:
        print(f"错误：找不到输入文件 {input_file}")
    except Exception as e:
        print(f"发生错误��{str(e)}")

def main():
    if len(sys.argv) != 4:
        print("使用方法：python convert_qa_format.py 输入文件名 训练集输出文件名 验证集输出文件名")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_train_file = sys.argv[2]
    output_valid_file = sys.argv[3]
    convert_file(input_file, output_train_file, output_valid_file)

if __name__ == "__main__":
    main() 