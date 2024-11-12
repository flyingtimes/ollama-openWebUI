import sys
import json
import re

def parse_chat_content(text):
    # 使用正则表达式匹配 <|im_start|>role\ncontent<|im_end|> 格式
    pattern = r'<\|im_start\|>(.*?)\n(.*?)<\|im_end\|>'
    matches = re.findall(pattern, text, re.DOTALL)
    
    # 转换成新的消息格式
    messages = []
    for role, content in matches:
        # 去除内容中的多余换行符
        content = content.strip()
        messages.append({
            "role": role,
            "content": content
        })
    
    return {"messages": messages}

def convert_file(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f_in, \
             open(output_file, 'w', encoding='utf-8') as f_out:
            
            # 逐行处理输入文件
            for line in f_in:
                # 解析输入的JSON
                input_data = json.loads(line.strip())
                text = input_data['text']
                
                # 转换格式
                output_data = parse_chat_content(text)
                
                # 写入输出文件
                f_out.write(json.dumps(output_data, ensure_ascii=False) + '\n')
                
        print(f"转换完成！输出文件已保存为：{output_file}")
        
    except FileNotFoundError:
        print(f"错误：找不到输入文件 {input_file}")
    except json.JSONDecodeError:
        print("错误：输入文件格式不正确")
    except Exception as e:
        print(f"发生错误：{str(e)}")

def main():
    if len(sys.argv) != 3:
        print("使用方法：python convert_chat_format.py 输入文件名 输出文件名")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    convert_file(input_file, output_file)

if __name__ == "__main__":
    main() 