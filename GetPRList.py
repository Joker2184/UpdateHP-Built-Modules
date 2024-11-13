import os
import requests
import re
import json
from typing import List

PAT_TOKEN = os.getenv('PAT_TOKEN')  # 获取 PAT Token

if not PAT_TOKEN:
    raise ValueError("PAT_TOKEN environment variable not set.")

headers = {
    'Authorization': f'Bearer {PAT_TOKEN}',  # 使用 Bearer Token 认证
    'Accept': 'application/vnd.github.v3+json'
}

def get_pull_requests() -> List[dict]:
    """获取GitHub的Pull Requests数据"""
    try:
        print("Sending request to GitHub API...")
        print(f"Request URL: {GITHUB_API_URL}")
        print(f"Headers: {HEADERS}")

        response = requests.get(GITHUB_API_URL, headers=HEADERS)
        
        # Debugging: Output response status code and response body
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        
        if response.status_code != 200:
            print(f"Failed to fetch data: {response.status_code}")
            print(f"Response body: {response.text}")  # Output response body for debugging
            response.raise_for_status()  # Raise HTTPError for bad responses

        return response.json()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        print(f"Response: {err.response.text}")
        raise
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

def clean_text(text: str) -> str:
    """清理文本中的\r\n以及其他换行符"""
    return re.sub(r'(\r\n|\n|\r)', '', text)

def generate_template(pr: dict) -> str:
    """根据Pull Request数据生成XML模板"""
    title = clean_text(pr.get('title', ''))
    body = clean_text(pr.get('body', ''))
    number = pr.get('number', '')
    
    # 填充XML模板
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
                Logo="M256 170.666667a85.333333 85.333333 0 1 0 0 170.666666 85.333333 85.333333 0 0 0 0-170.666666zM85.333333 256a170.666667 170.666667 0 1 1 213.333334 165.290667V896a42.666667 42.666667 0 0 1-85.333334 0V421.290667A170.666667 170.666667 0 0 1 85.333333 256z m426.666667 0a42.666667 42.666667 0 0 1 42.666667-42.666667H682.666667A128 128 0 0 1 810.666667 341.333333v261.376a170.666667 170.666667 0 1 1-85.333334 0V341.333333a42.666667 42.666667 0 0 0-42.666666-42.666666H554.666667A42.666667 42.666667 0 0 1 512 256z m256 426.666667a85.333333 85.333333 0 1 0 0 170.666666 85.333333 85.333333 0 0 0 0-170.666666z"/>
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
        <TextBlock FontSize="16"><Bold>你可以帮忙的PR</Bold></TextBlock>
        <StackPanel>
            <Grid>
                <Grid.RowDefinitions>
                    <RowDefinition Height="45" />
                </Grid.RowDefinitions>
                <local:MyListItem Title="本地化：语言、配置项、时间 #4145" Margin="-10,0,0,0" IsHitTestVisible="False" Info="你可以协助社区工作者一同完善PCL的国际化工作" Grid.Row="0" Grid.Column="1"/>
                <local:MyIconTextButton Grid.Column="1" HorizontalAlignment="Right" EventType="打开网页" LogoScale="1"
                    Text="加入翻译队伍" EventData="https://weblate.tangge233.cn/engage/PCL/" 
                    Logo="M640 416h256c35.36 0 64 28.48 64 64v416c0 35.36-28.48 64-64 64H480c-35.36 0-64-28.48-64-64V640h128c53.312 0 96-42.976 96-96V416zM64 128c0-35.36 28.48-64 64-64h416c35.36 0 64 28.48 64 64v416c0 35.36-28.48 64-64 64H128c-35.36 0-64-28.48-64-64V128z m128 276.256h46.72v-24.768h67.392V497.76h49.504V379.488h68.768v20.64h50.88V243.36H355.616v-34.368c0-10.08 1.376-18.784 4.16-26.112a10.56 10.56 0 0 0 1.344-4.16c0-0.896-3.2-1.792-9.6-2.72h-46.816v67.36H192v160.896z m46.72-122.368h67.392v60.48h-67.36V281.92z m185.664 60.48h-68.768V281.92h68.768v60.48z m203.84 488l19.264-53.632h100.384l19.264 53.632h54.976L732.736 576h-64.64L576 830.4h52.256z m33.024-96.256l37.12-108.608h1.376l34.368 108.608h-72.864zM896 320h-64a128 128 0 0 0-128-128v-64a192 192 0 0 1 192 192zM128 704h64a128 128 0 0 0 128 128v64a192 192 0 0 1-192-192z"/>
            </Grid>
        </StackPanel>
    </StackPanel>
</local:MyCard>
    """
    return xml_template

def save_to_json(content: dict, filename: str):
    """将生成的PR数据保存为JSON文件"""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(content, file, ensure_ascii=False, indent=4)
        print(f"PR 数据已保存到: {filename}")
    except Exception as e:
        print(f"保存文件时出错: {e}")

def save_to_xaml(content: str, filename: str):
    """将生成的模板保存为XAML文件"""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"文件已保存到: {filename}")
    except Exception as e:
        print(f"保存文件时出错: {e}")

def main():
    # 获取GitHub的PR数据
    try:
        prs = get_pull_requests()
        print("PR 数据获取成功")
    except Exception as e:
        print(f"获取 PR 数据失败: {e}")
        return

    # 如果存在数据库文件，读取数据库；否则创建新的数据库
    pr_database_path = "UpdateHP-Built-Modules/PRDatabase.json"
    if os.path.exists(pr_database_path):
        with open(pr_database_path, 'r', encoding='utf-8') as db_file:
            pr_database = json.load(db_file)
    else:
        # 如果没有数据库文件，先获取最新的10个PR，并生成数据库
        pr_database = prs[:10]  # 获取最新的10个PR
        save_to_json(pr_database, pr_database_path)

    # 保存新XAML文件
    new_prs = []
    for pr in prs:
        # 检查是否是新的PR（即是否不在数据库中）
        if not any(existing_pr['number'] == pr['number'] for existing_pr in pr_database):
            template = generate_template(pr)
            save_to_xaml(template, "UpdateHomepage-Build/libraries/Homepage/PRList.xaml")
            new_prs.append(pr)

    # 更新数据库（如果有新PR）
    if new_prs:
        pr_database.extend(new_prs)
        save_to_json(pr_database, pr_database_path)

if __name__ == "__main__":
    main()
