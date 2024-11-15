import sys
import os
from pathlib import Path
import random

def merge_files(input_filename, output_file, folder_lines_pairs):
    """
    从多个文件夹中合并同名文件的指定行数，并随机打乱顺序
    
    Args:
        input_filename: 要合并的文件名
        output_file: 输出文件路径
        folder_lines_pairs: 包含(文件夹路径, 提取行数)元组的列表
    """
    try:
        # 用于存储所有文件中读取的行
        all_lines = []
        
        # 遍历每个文件夹和对应的行数
        for folder, lines_count in folder_lines_pairs:
            # 构建完整的文件路径
            file_path = Path(folder) / input_filename
            
            # 检查文件是否存在
            if not file_path.exists():
                print(f"警告：文件 {file_path} 不存在，已跳过")
                continue
            
            # 读取指定行数的数据
            with open(file_path, 'r', encoding='utf-8') as in_f:
                lines = []
                # 逐行读取指定数量的数据
                for _ in range(lines_count):
                    line = in_f.readline()
                    if not line:  # 如果读到文件末尾则停止
                        break
                    lines.append(line)
                
                # 将当前文件读取的行添加到总行列表中
                all_lines.extend(lines)
                print(f"已从 {file_path} 提取 {len(lines)} 行数据")
        
        # 使用random.shuffle随机打乱所有行的顺序
        random.shuffle(all_lines)
        
        # 将打乱后的数据写入到输出文件
        with open(output_file, 'w', encoding='utf-8') as out_f:
            out_f.writelines(all_lines)
        
        print(f"合并完成！输出文件：{output_file}，共 {len(all_lines)} 行")
        
    except Exception as e:
        print(f"发生错误：{str(e)}")

def main():
    # 检查命令行参数数量是否足够
    if len(sys.argv) < 5:
        print("使用方法：python merge_files.py 输入文件名 输出文件名 文件夹1 行数1 [文件夹2 行数2 ...]")
        print("示例：python merge_files.py data.json output.txt folder1 100 folder2 200 folder3 150")
        sys.exit(1)
    
    # 获取输入和输出文件名
    input_filename = sys.argv[1]
    output_file = sys.argv[2]
    
    # 检查文件夹和行数参数是否成对出现
    if (len(sys.argv) - 3) % 2 != 0:
        print("错误：每个文件夹必须指定对应的行数")
        sys.exit(1)
    
    # 将文件夹和行数配对存储
    folder_lines_pairs = []
    # 从第3个参数开始，每次取2个参数（文件夹和行数）
    for i in range(3, len(sys.argv), 2):
        folder = sys.argv[i]
        # 尝试将行数转换为整数
        try:
            lines = int(sys.argv[i + 1])
        except ValueError:
            print(f"错误：行数必须是整数，得到的是 {sys.argv[i + 1]}")
            sys.exit(1)
        
        # 检查文件夹是否存在    
        if not os.path.isdir(folder):
            print(f"错误：文件夹 {folder} 不存在")
            sys.exit(1)
        
        # 将文件夹和行数作为元组添加到列表中    
        folder_lines_pairs.append((folder, lines))
    
    # 调用合并函数处理文件
    merge_files(input_filename, output_file, folder_lines_pairs)

# 程序入口点
if __name__ == "__main__":
    main() 