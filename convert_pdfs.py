import os
import subprocess
from pathlib import Path
import argparse

def convert_pdf_to_md(input_path: Path, output_path: Path, parallel_factor: int = 2, max_pages: int = 10):
    """
    使用marker_docker将PDF文件转换为Markdown格式
    
    Args:
        input_path: PDF文件路径
        output_path: 输出的Markdown文件路径
        parallel_factor: 并行处理因子
        max_pages: 最大处理页数
    """
    # 确保输出目录存在
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 构建docker命令
    cmd = [
        "docker", "run",
        "-v", f"{input_path.parent}:/pdfs_in",  # 输入目录挂载
        "-v", f"{output_path.parent}:/pdfs_out", # 输出目录挂载
        "dockerpull.org/dibz15/marker_docker",
        "python", "convert_single.py",
        f"/pdfs_in/{input_path.name}",
        f"/pdfs_out/{output_path.name}",
        "--parallel_factor", str(parallel_factor),
        "--max_pages", str(max_pages)
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"成功转换: {input_path} -> {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"转换失败 {input_path}: {str(e)}")

def process_directory(input_dir: Path, output_dir: Path, parallel_factor: int = 2, max_pages: int = 10):
    """
    递归处理目录中的所有PDF文件
    
    Args:
        input_dir: 输入目录
        output_dir: 输出目录
        parallel_factor: 并行处理因子
        max_pages: 最大处理页数
    """
    # 遍历输入目录中的所有文件和子目录
    for item in input_dir.rglob("*.pdf"):
        # 计算相对路径，以保持目录结构
        rel_path = item.relative_to(input_dir)
        # 构建输出文件路径，将.pdf替换为.md
        output_path = output_dir / rel_path.with_suffix('.md')
        
        # 转换PDF文件
        convert_pdf_to_md(item, output_path, parallel_factor, max_pages)

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='将目录中的PDF文件批量转换为Markdown格式')
    parser.add_argument('input_dir', type=str, help='输入目录路径')
    parser.add_argument('output_dir', type=str, help='输出目录路径')
    parser.add_argument('--parallel_factor', type=int, default=2, help='并行处理因子')
    parser.add_argument('--max_pages', type=int, default=10, help='每个PDF处理的最大页数')
    
    args = parser.parse_args()
    
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
    process_directory(input_dir, output_dir, args.parallel_factor, args.max_pages)
    print("处理完成")

if __name__ == "__main__":
    main() 