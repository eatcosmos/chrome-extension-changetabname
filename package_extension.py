import os
import zipfile
from datetime import datetime
import json
import shutil

def read_manifest():
    """读取 manifest.json 获取版本信息"""
    with open('manifest.json', 'r', encoding='utf-8') as f:
        manifest = json.load(f)
    return manifest.get('version', '1.0')

def create_package():
    """创建发布包"""
    # 确保 .gitignore 包含 dist 目录
    gitignore_path = '.gitignore'
    dist_ignore = 'dist/'
    
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if dist_ignore not in content:
            with open(gitignore_path, 'a', encoding='utf-8') as f:
                f.write(f'\n{dist_ignore}\n')
    else:
        with open(gitignore_path, 'w', encoding='utf-8') as f:
            f.write(f'{dist_ignore}\n')
    
    # 获取版本号
    version = read_manifest()
    
    # 创建发布目录
    dist_dir = 'dist'
    if not os.path.exists(dist_dir):
        os.makedirs(dist_dir)
    
    # 生成文件名（使用版本号和时间戳）
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    zip_filename = f'deepseek_title_changer_v{version}_{timestamp}.zip'
    zip_path = os.path.join(dist_dir, zip_filename)
    
    # 需要打包的文件列表
    files_to_package = [
        'manifest.json',
        'content.js',
        'background.js',
        'privacy_policy.md',
        'README.md'
    ]
    
    # 检查 icons 目录
    if not os.path.exists('icons'):
        print("警告: icons 目录不存在，正在创建图标...")
        try:
            import create_icons
            create_icons.main()
        except Exception as e:
            print(f"创建图标失败: {e}")
            return
    
    # 创建临时目录用于打包
    temp_dir = 'temp_package'
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    # 复制文件到临时目录
    print("正在复制文件...")
    for file in files_to_package:
        if os.path.exists(file):
            shutil.copy2(file, temp_dir)
        else:
            print(f"警告: 文件 {file} 不存在")
    
    # 复制 icons 目录
    if os.path.exists('icons'):
        shutil.copytree('icons', os.path.join(temp_dir, 'icons'))
    
    # 创建 ZIP 文件
    print(f"正在创建 ZIP 文件: {zip_filename}")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, temp_dir)
                zipf.write(file_path, arcname)
    
    # 清理临时目录
    shutil.rmtree(temp_dir)
    
    print(f"\n打包完成！")
    print(f"文件位置: {os.path.abspath(zip_path)}")
    print(f"文件大小: {os.path.getsize(zip_path) / 1024:.2f} KB")
    
    # 列出打包的文件
    print("\n包含的文件:")
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        for file in zipf.namelist():
            print(f"- {file}")

if __name__ == "__main__":
    create_package() 