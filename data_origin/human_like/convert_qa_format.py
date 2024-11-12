import sys
import json
import random

def parse_qa_content(text):
    # 分割问答内容
    lines = text.strip().split('\n')
    question = None
    answer = None
    
    for line in lines:
        if line.startswith('问：'):
            question = line[2:].strip()
        elif line.startswith('答：'):
            answer = line[2:].strip()
    
    # 创建标准格式的消息
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": question
        },
        {
            "role": "assistant",
            "content": answer
        }
    ]
    
    return {"messages": messages}

def convert_file(input_file, output_train_file, output_valid_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f_in:
            # 读取整个文件内容
            content = f_in.read()
            # 按一个或多个空行分割成多组
            qa_groups = [group for group in content.split('\n\n') if group.strip()]
            
        # 随机打乱数据
        random.shuffle(qa_groups)
        
        # 计算训练集和验证集的分割点
        split_point = int(len(qa_groups) * 0.9)
        train_groups = qa_groups[:split_point]
        valid_groups = qa_groups[split_point:]
        
        # 写入训练集
        with open(output_train_file, 'w', encoding='utf-8') as f_train:
            for group in train_groups:
                output_data = parse_qa_content(group)
                f_train.write(json.dumps(output_data, ensure_ascii=False) + '\n')
                
        # 写入验证集
        with open(output_valid_file, 'w', encoding='utf-8') as f_valid:
            for group in valid_groups:
                output_data = parse_qa_content(group)
                f_valid.write(json.dumps(output_data, ensure_ascii=False) + '\n')
                
        print(f"转换完成！")
        print(f"训练集已保存为：{output_train_file}，共 {len(train_groups)} 条数据")
        print(f"验证集已保存为：{output_valid_file}，共 {len(valid_groups)} 条数据")
        
    except FileNotFoundError:
        print(f"错误：找不到输入文件 {input_file}")
    except Exception as e:
        print(f"发生错误：{str(e)}")

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