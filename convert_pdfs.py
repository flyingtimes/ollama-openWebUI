import os
import subprocess
from pathlib import Path
import argparse
import sys
import fitz  # PyMuPDF

def check_pdf_validity(pdf_path: Path) -> bool:
    """
    检查PDF文件是否可以正常打开
    
    Args:
        pdf_path: PDF文件路径
    Returns:
        bool: PDF文件是否有效
    """
    try:
        doc = fitz.open(pdf_path)
        doc.close()
        return True
    except Exception as e:
        print(f"PDF文件检查失败 {pdf_path}: {str(e)}")
        return False

def convert_pdf_to_md(input_path: Path, output_path: Path, max_pages: int = 10, batch_multiplier: int = 4):
    """
    使用marker/convert_single.py将PDF文件转换为Markdown格式
    
    Args:
        input_path: PDF文件路径
        output_path: 输出的Markdown文件路径
        max_pages: 最大处理页数
        batch_multiplier: 批处理乘数，用于控制处理速度
    """
    # 检查PDF文件是否有效
    if not check_pdf_validity(input_path):
        print(f"跳过无效的PDF文件: {input_path}")
        return
    
    # 确保输出目录存在
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 获取marker目录的路径
    mark_dir = Path(__file__).parent / 'marker'
    convert_script = mark_dir / 'convert_single.py'
    
    if not convert_script.exists():
        print(f"错误：找不到转换脚本 {convert_script}")
        return
    
    # 构建命令，使用正确的参数
    cmd = [
        sys.executable,
        str(convert_script),
        str(input_path.absolute()),  # 使用绝对路径
        str(output_path.absolute()),  # 使用绝对路径
        "--max_pages", str(max_pages),
        "--langs", "chinese",
        "--batch_multiplier", str(batch_multiplier)
    ]
    
    try:
        print(f"开始转换: {input_path}")
        print(f"命令: {' '.join(cmd)}")
        
        # 设置环境变量
        env = os.environ.copy()
        env["PYTHONPATH"] = str(mark_dir.parent)  # 添加marker目录到Python路径
        
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
            env=env
        )
        
        if result.stdout:
            print("输出:", result.stdout)
        print(f"成功转换: {input_path} -> {output_path}")
        
    except subprocess.CalledProcessError as e:
        print(f"转换失败 {input_path}")
        print(f"错误输出: {e.stderr}")
        print(f"标准输出: {e.stdout}")
    except Exception as e:
        print(f"发生错误: {str(e)}")

def process_directory(input_dir: Path, output_dir: Path, max_pages: int = 10, batch_multiplier: int = 4):
    """
    递归处理目录中的所有PDF文件
    
    Args:
        input_dir: 输入目录
        output_dir: 输出目录
        max_pages: 最大处理页数
        batch_multiplier: 批处理乘数
    """
    # 遍历输入目录中的所有文件和子目录
    for item in input_dir.rglob("*.pdf"):
        try:
            # 计算相对路径，以保持目录结构
            rel_path = item.relative_to(input_dir)
            # 构建输出文件路径，将.pdf替换为.md
            output_path = output_dir / rel_path.with_suffix('.md')
            
            # 转换PDF文件
            convert_pdf_to_md(item, output_path, max_pages, batch_multiplier)
            
        except Exception as e:
            print(f"处理文件 {item} 时发生错误: {str(e)}")
            continue

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='将目录中的PDF文件批量转换为Markdown格式')
    parser.add_argument('input_dir', type=str, help='输入目录路径')
    parser.add_argument('output_dir', type=str, help='输出目录路径')
    parser.add_argument('--max_pages', type=int, default=10, help='每个PDF处理的最大页数')
    parser.add_argument('--batch_multiplier', type=int, default=4, 
                       help='批处理乘数，用于控制处理速度（更大的值处理更快但消耗更多内存）')
    
    args = parser.parse_args()
    
    try:
        # 转换路径字符串为Path对象
        input_dir = Path(args.input_dir).resolve()
        output_dir = Path(args.output_dir).resolve()
        
        # 确保输入目录存在
        if not input_dir.exists():
            print(f"错误：输入目录 {input_dir} 不存在")
            return
        
        # 创建输出目录
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 开始处理
        print(f"开始处理目录: {input_dir}")
        process_directory(input_dir, output_dir, args.max_pages, args.batch_multiplier)
        print("处理完成")
        
    except Exception as e:
        print(f"程序执行过程中发生错误: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 