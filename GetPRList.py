import os
import requests
import re
import json
from typing import List

# GitHub API Token 和仓库信息
GITHUB_API_URL = "https://api.github.com/repos/Hex-Dragon/PCL2/pulls"
PAT_TOKEN = os.getenv("PAT_TOKEN")  # 从环境变量中获取 Token

if not PAT_TOKEN:
    raise ValueError("PAT_TOKEN 环境变量未设置。")

headers = {
    'Authorization': f'Bearer {PAT_TOKEN}',  # 使用 Bearer Token 认证
    'Accept': 'application/vnd.github.v3+json'
}

def ensure_directory_exists(file_path: str):
    """确保文件路径中的目录存在"""
    dir_path = os.path.dirname(file_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def get_pull_requests() -> List[dict]:
    """获取 GitHub 的 Pull Requests 数据"""
    try:
        print("发送请求到 GitHub API...")
        print(f"请求 URL: {GITHUB_API_URL}")
        response = requests.get(GITHUB_API_URL, headers=headers)
        print(f"响应状态码: {response.status_code}")

        if response.status_code != 200:
            print(f"请求失败，状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            response.raise_for_status()  # 如果响应失败，抛出异常

        return response.json()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP 错误: {err}")
        print(f"详细信息: {err.response.text}")
        raise
    except Exception as e:
        print(f"发生未知错误: {e}")
        raise

def clean_text(text: str) -> str:
    """清理文本中的换行符"""
    return re.sub(r'(\r\n|\n|\r)', '', text)

def generate_template(pr: dict) -> str:
    """根据 Pull Request 数据生成 XML 模板"""
    title = clean_text(pr.get('title', ''))
    body = clean_text(pr.get('body', ''))
    number = pr.get('number', '')

    # 填充 XML 模板
    xml_template = f"""
<local:MyCard Margin="0,0,0,15">
    <StackPanel Margin="20,14">
        <Grid>
            <Grid.ColumnDefinitions>
                <ColumnDefinition Width="3*"/>
                <ColumnDefinition Width="1*"/>
            </Grid.ColumnDefinitions>
            <StackPanel Grid.Column="0">
                <TextBlock FontSize="16"><Bold>社区快讯</Bold></TextBlock>
                <TextBlock FontSize="14">社区用户正在参与制作更多有趣的新功能</TextBlock>
                <TextBlock FontSize="14">他们正为 PCL 伟大的咕咕咕事业贡献自己的力量！</TextBlock>
            </StackPanel>
            <local:MyIconTextButton Grid.Column="1" HorizontalAlignment="Right" EventType="打开网页" LogoScale="1"
                Text="PRs" EventData="https://github.com/Hex-Dragon/PCL2/pulls" ToolTip="提交一个PCL Pull Requests 合并后可以获取活跃橙"
                Logo="M256 170.666667a85.333333 85.333333 0 1 0 0 170.666666 85.333333 85.333333 0 0 0 0-170.666666z"/>
        </Grid>
        <Line X1="0" X2="100" Stroke="{{DynamicResource ColorBrush6}}" StrokeThickness="1.5" Stretch="Fill" Margin="0,8"/>
        <TextBlock FontSize="16"><Bold>最新PR</Bold></TextBlock>
        <StackPanel>
            <Grid>
                <Grid.RowDefinitions>
                    <RowDefinition Height="45" />
                </Grid.RowDefinitions>
                <local:MyListItem Title="{title} #{number}" Margin="-10,0,0,0" IsHitTestVisible="False" Info="{body}" Grid.Row="0" Grid.Column="1"/>
            </Grid>
        </StackPanel>
    </StackPanel>
</local:MyCard>
    """
    return xml_template

def save_to_json(content: dict, filename: str):
    """将生成的 PR 数据保存为 JSON 文件"""
    try:
        ensure_directory_exists(filename)
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(content, file, ensure_ascii=False, indent=4)
        print(f"PR 数据已保存到: {filename}")
    except Exception as e:
        print(f"保存文件 {filename} 时出错: {e}")

def save_to_xaml(content: str, filename: str):
    """将生成的模板保存为 XAML 文件"""
    try:
        ensure_directory_exists(filename)
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"文件已保存到: {filename}")
    except Exception as e:
        print(f"保存文件 {filename} 时出错: {e}")

# 主逻辑
workspace = os.getenv("GITHUB_WORKSPACE")
if not workspace:
    raise ValueError("GITHUB_WORKSPACE 环境变量未设置。")

pr_data = get_pull_requests()
if not pr_data:
    print("未获取到任何 PR 数据，可能是当前没有打开的 Pull Requests。")
else:
    output_json = os.path.join(workspace, "UpdateHP-Built-Modules", "PRDatabase.json")
    output_xaml = os.path.join(workspace, "UpdateHP-Built-Modules", "libraries", "Homepage", "PRList.xaml")

    save_to_json(pr_data, output_json)
    save_to_xaml(generate_template(pr_data[0]), output_xaml)
