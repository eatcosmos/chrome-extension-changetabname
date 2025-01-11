import os
import subprocess
import sys
from pathlib import Path
import requests
import json

def run_command(command):
    """运行命令并返回输出"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e.cmd}")
        print(f"错误信息: {e.stderr}")
        sys.exit(1)

def main():
    # 获取当前目录名
    current_dir = Path.cwd()
    repo_name = current_dir.name

    # 检查是否已经初始化了 Git
    if not os.path.exists('.git'):
        print("初始化 Git 仓库...")
        run_command('git init -b main')  # 使用 main 作为默认分支
    else:
        print("Git 仓库已存在")
        # 确保当前分支是 main
        try:
            current_branch = run_command('git rev-parse --abbrev-ref HEAD')
            if current_branch != 'main':
                run_command('git branch -m master main')  # 如果是 master，重命名为 main
        except:
            pass

    # 检查环境变量中是否存在 GitHub token
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("请设置 GITHUB_TOKEN 环境变量")
        print("你可以在 GitHub 的 Settings -> Developer settings -> Personal access tokens 中创建一个token")
        print("然后运行: ")
        print("Windows: [Environment]::SetEnvironmentVariable('GITHUB_TOKEN', '你的token', 'User')")
        print("Linux/Mac: export GITHUB_TOKEN=你的token")
        sys.exit(1)

    # 创建 GitHub 仓库
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {
        'name': repo_name,
        'private': False,
        'default_branch': 'main'  # 设置默认分支为 main
    }
    
    print(f"正在创建 GitHub 仓库: {repo_name}...")
    response = requests.post('https://api.github.com/user/repos', headers=headers, data=json.dumps(data))
    
    if response.status_code == 201:
        print("GitHub 仓库创建成功")
    elif response.status_code == 422:
        print("仓库可能已经存在，继续执行...")
    else:
        print(f"创建仓库失败: {response.status_code}")
        print(response.json())
        sys.exit(1)

    # 获取用户名
    user_response = requests.get('https://api.github.com/user', headers=headers)
    username = user_response.json()['login']

    # 添加远程仓库
    remote_url = f'https://github.com/{username}/{repo_name}.git'
    try:
        run_command('git remote remove origin')
    except:
        pass
    run_command(f'git remote add origin {remote_url}')

    # 添加所有文件并提交
    print("添加文件到暂存区...")
    run_command('git add .')
    
    # 检查是否有文件要提交
    status = run_command('git status --porcelain')
    if status:
        print("提交更改...")
        run_command('git commit -m "Initial commit"')
    else:
        print("没有需要提交的更改，尝试强制推送...")
        
    print("推送到 GitHub...")
    try:
        run_command('git push -u origin main')
    except:
        print("尝试强制推送...")
        run_command('git push -u origin main --force')
    
    print(f"\n完成！仓库已推送到: {remote_url}")

if __name__ == "__main__":
    main() 