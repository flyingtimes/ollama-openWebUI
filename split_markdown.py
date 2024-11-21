import re
from pathlib import Path
import argparse

def sanitize_filename(filename: str) -> str:
    """
    清理文件名，移除不合法的字符
    
    Args:
        filename: 原始文件名
    Returns:
        str: 清理后的文件名
    """
    # 替换不合法的文件名字符
    illegal_chars = r'[<>:"/\\|?*]'
    filename = re.sub(illegal_chars, '_', filename)
    # 移除开头和结尾的空格和点
    filename = filename.strip('. ')
    # 如果文件名为空，返回默认名称
    return filename if filename else 'unnamed_section'

def split_markdown_by_sections(input_file: Path, output_dir: Path):
    """
    按章节拆分Markdown文件
    
    Args:
        input_file: 输入的Markdown文件路径
        output_dir: 输出目录路径
    """
    # 确保输出目录存在
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 读取文件内容
    content = input_file.read_text(encoding='utf-8')
    
    # 使用正则表达式匹配标题
    # 匹配 # 到 ##### 级别的标题
    section_pattern = re.compile(r'^(#{1,5})\s+(.+)$', re.MULTILINE)
    
    # 找到所有标题及其位置
    sections = [(match.group(1), match.group(2), match.start()) 
               for match in section_pattern.finditer(content)]
    
    # 如果没有找到任何标题，将整个文件作为一个部分
    if not sections:
        output_file = output_dir / f"{input_file.stem}_full.md"
        output_file.write_text(content, encoding='utf-8')
        print(f"未找到章节标题，已将整个文件保存为: {output_file}")
        return
    
    # 处理每个章节
    for i, (level, title, start) in enumerate(sections):
        # 获取当前章节的内容（到下一个章节开始或文件结束）
        next_start = sections[i + 1][2] if i + 1 < len(sections) else len(content)
        section_content = content[start:next_start].strip()
        
        # 生成文件名
        # 使用标题级别数字和标题文本创建文件名
        level_num = len(level)  # 获取#的数量
        filename = f"{level_num}_{sanitize_filename(title)}.md"
        output_file = output_dir / filename
        
        # 写入文件
        output_file.write_text(section_content, encoding='utf-8')
        print(f"已保存章节: {filename}")

def main():
    parser = argparse.ArgumentParser(description='将Markdown文件按章节拆分为多个文件')
    parser.add_argument('input_file', type=str, help='输入的Markdown文件路径')
    parser.add_argument('output_dir', type=str, help='输出目录路径')
    
    args = parser.parse_args()
    
    try:
        input_file = Path(args.input_file).resolve()
        output_dir = Path(args.output_dir).resolve()
        
        # 检查输入文件是否存在
        if not input_file.exists():
            print(f"错误：输入文件 {input_file} 不存在")
            return
        
        # 检查输入文件是否是Markdown文件
        if input_file.suffix.lower() not in ['.md', '.markdown']:
            print(f"警告：输入文件 {input_file} 可能不是Markdown文件")
        
        # 开始处理
        print(f"开始处理文件: {input_file}")
        split_markdown_by_sections(input_file, output_dir)
        print("处理完成")
        
    except Exception as e:
        print(f"程序执行过程中发生错误: {str(e)}")
        raise

if __name__ == "__main__":
    main() 