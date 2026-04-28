#!/usr/bin/env python3
"""合并所有模块到单文件index.html"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# JS文件加载顺序
JS_FILES = [
    'js/config.js',
    'js/ctm.js',
    'js/storage.js',
    'js/audio.js',
    'js/utils.js',
    'js/user.js',
    'js/data/week-plans.js',
    'js/data/topics.js',
    'js/data/podcasts.js',
    'js/data/videos.js',
    'js/data/games-config.js',
    'js/modules/ai.js',
    'js/modules/practice.js',
    'js/modules/map.js',
    'js/modules/plan.js',
    'js/modules/topics.js',
    'js/modules/method.js',
    'js/modules/thinking.js',
    'js/modules/podcast.js',
    'js/modules/video.js',
    'js/modules/player.js',
    'js/modules/games.js',
    'js/modules/deepseek.js',
    'js/modules/wrongbook.js',
    'js/modules/pomodoro.js',
    'js/modules/ui.js',
]

# 模块名称映射
MODULE_NAMES = {
    'js/config.js': 'Config - 全局配置',
    'js/ctm.js': 'CTM - 点击追踪',
    'js/storage.js': 'Storage - 数据存储',
    'js/audio.js': 'Audio - 音频管理',
    'js/utils.js': 'Utils - 工具函数',
    'js/user.js': 'User - 用户管理',
    'js/data/week-plans.js': 'WeekPlans - 周计划数据',
    'js/data/topics.js': 'Topics - 训练主题数据',
    'js/data/podcasts.js': 'Podcasts - 播客数据',
    'js/data/videos.js': 'Videos - 视频数据',
    'js/data/games-config.js': 'GamesConfig - 游戏配置',
    'js/modules/ai.js': 'AI - 智能问答',
    'js/modules/practice.js': 'Practice - 练习模块',
    'js/modules/map.js': 'Map - 地图模块',
    'js/modules/plan.js': 'Plan - 训练计划',
    'js/modules/topics.js': 'TopicsModule - 主题模块',
    'js/modules/method.js': 'Method - 学法指导',
    'js/modules/thinking.js': 'Thinking - 思维训练',
    'js/modules/podcast.js': 'Podcast - 播客模块',
    'js/modules/video.js': 'Video - 视频模块',
    'js/modules/player.js': 'Player - 播放器',
    'js/modules/games.js': 'Games - 游戏模块',
    'js/modules/deepseek.js': 'DeepSeek - AI对话',
    'js/modules/wrongbook.js': 'Wrongbook - 错题本',
    'js/modules/pomodoro.js': 'Pomodoro - 番茄钟',
    'js/modules/ui.js': 'UI - 用户界面',
}

def read_file(path):
    """读取文件内容"""
    full_path = os.path.join(BASE_DIR, path)
    with open(full_path, 'r', encoding='utf-8') as f:
        return f.read()

def get_module_comment(path):
    """获取模块注释头"""
    name = MODULE_NAMES.get(path, os.path.basename(path))
    return f"// {'='*60}\n// {name}\n// {'='*60}\n\n"

def main():
    # 读取CSS
    css_content = read_file('css/style.css')
    
    # 读取HTML模板
    html_path = os.path.join(BASE_DIR, 'index.html')
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 提取HTML头部和尾部
    head_end = html_content.find('</head>')
    body_end = html_content.find('</body>')
    
    html_head = html_content[:head_end]
    html_tail = html_content[body_end:]  # includes </body> and </html>
    
    # 修改图标路径为GitHub Pages绝对URL
    html_head = html_head.replace(
        'href="favicon.ico"',
        'href="https://yuhang87989.github.io/cognitive-training-portal/favicon.ico"'
    )
    html_head = html_head.replace(
        'href="icon-192.png"',
        'href="https://yuhang87989.github.io/cognitive-training-portal/icon-192.png"'
    )
    
    # 构建CSS标签
    css_style = f'<style>\n{css_content}\n</style>'
    
    # 移除旧的外链CSS引用
    html_head = html_head.replace('<link rel="stylesheet" href="css/style.css"/>', '')
    
    # 提取initApp脚本
    init_app_start = html_content.find('<script>\n// ====== 初始化脚本 ======')
    init_app_end = html_content.find('</script>', init_app_start) + len('</script>')
    init_app_script = html_content[init_app_start:init_app_end]
    
    # 移除旧的外链JS标签和initApp脚本
    script_pattern = r'<script src="[^"]+"></script>'
    html_head = html_head.split('<script>')[0] + html_head.split('<script>')[-1]
    
    # 重新构建HTML头部（去掉所有script标签和样式）
    lines = html_content.split('\n')
    new_lines = []
    in_script_block = False
    skip_to_end = False
    
    for i, line in enumerate(lines):
        if '<script src=' in line:
            continue  # 跳过外链script标签
        if line.strip() == '<script>' and i > 600:  # initApp脚本开始
            break  # 停止收集，跳过后面的内容
        new_lines.append(line)
    
    html_head = '\n'.join(new_lines)
    
    # 找到</body>的位置
    body_end_pos = html_head.rfind('</body>')
    html_head = html_head[:body_end_pos]
    
    # 构建合并后的JS内容
    js_parts = []
    for js_file in JS_FILES:
        try:
            content = read_file(js_file)
            js_parts.append(get_module_comment(js_file))
            js_parts.append(content)
            js_parts.append('\n\n')
            print(f"✓ {js_file}")
        except Exception as e:
            print(f"✗ {js_file}: {e}")
    
    # 添加initApp脚本
    js_parts.append('\n// ============================================================\n// Init - 应用初始化\n// ============================================================\n\n')
    js_parts.append(init_app_script)
    
    combined_js = ''.join(js_parts)
    
    # 构建完整JS标签
    js_script = f'<script>\n{combined_js}\n</script>'
    
    # 组装最终HTML
    final_html = html_head + '\n' + css_style + '\n' + js_script + '\n</body>\n</html>\n'
    
    # 写入文件
    output_path = os.path.join(BASE_DIR, 'index.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"\n✓ 合并完成！文件大小: {len(final_html):,} bytes")
    print(f"✓ 输出路径: {output_path}")

if __name__ == '__main__':
    main()
