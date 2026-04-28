#!/usr/bin/env python3
"""合并所有模块到单文件index.html - V140 单文件版"""
import os
import re

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
    # 从模块化版本开始
    source_path = os.path.join(BASE_DIR, 'index_modular_temp.html')
    with open(source_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 找到</head>位置
    head_end_pos = content.find('</head>') + len('</head>')
    
    # 2. 找到body开始和所有<script src>标签
    body_start = content.find('<body>')
    all_script_tags = list(re.finditer(r'<script src="[^"]+"></script>', content))
    
    # 3. 分类script标签
    head_scripts = []  # 在</head>之前的（保留PeerJS）
    body_scripts = []   # 在</head>之后的（要移除）
    
    for m in all_script_tags:
        if m.start() < head_end_pos:
            head_scripts.append(m)
        else:
            body_scripts.append(m)
    
    print(f"head中外链script: {len(head_scripts)}")
    print(f"body中外链script: {len(body_scripts)}")
    
    # 4. 构建HTML头部（保留PeerJS，移除CSS外链，更新图标路径）
    head_content = re.sub(r'<link\s+rel="stylesheet"\s+href="css/style\.css"\s*/?>', '', content[:head_end_pos])
    
    # 更新图标路径
    head_content = head_content.replace(
        'href="favicon.ico"',
        'href="https://yuhang87989.github.io/cognitive-training-portal/favicon.ico"'
    )
    head_content = head_content.replace(
        'href="icon-192.png"',
        'href="https://yuhang87989.github.io/cognitive-training-portal/icon-192.png"'
    )
    head_content = head_content.replace(
        'href="apple-touch-icon.png"',
        'href="https://yuhang87989.github.io/cognitive-training-portal/apple-touch-icon.png"'
    )
    
    # 5. 读取CSS内容并构建<style>标签
    css_content = read_file('css/style.css')
    css_style = f'\n<style>\n{css_content}\n</style>\n'
    
    # 6. 提取body内容
    # 从<body>到第一个body中外链<script>之前
    if body_scripts:
        body_end = body_scripts[0].start()
    else:
        body_end = content.find('<script>\n// ======', body_start)
    
    body_content = content[body_start:body_end]
    
    # 7. 提取initApp脚本（只提取一次）
    init_start = content.find('<script>\n// ====== 初始化脚本')
    init_end = content.find('</script>', init_start) + len('</script>')
    init_script = content[init_start:init_end]
    print(f"✓ 提取initApp脚本: 位置{init_start}-{init_end}")
    
    # 8. 构建合并后的JS内容（不含initApp，让它单独在最后）
    js_parts = []
    for js_file in JS_FILES:
        try:
            file_content = read_file(js_file)
            js_parts.append(get_module_comment(js_file))
            js_parts.append(file_content)
            js_parts.append('\n\n')
            print(f"✓ {js_file}")
        except Exception as e:
            print(f"✗ {js_file}: {e}")
    
    combined_js = ''.join(js_parts)
    
    # 构建模块JS标签
    js_modules_script = f'<script>\n{combined_js}\n</script>\n'
    
    # initApp单独一个标签
    js_init_script = f'<script>\n{init_script}\n</script>\n'
    
    # 9. 组装最终HTML
    final_html = head_content + css_style + body_content + js_modules_script + js_init_script + '\n</body>\n</html>\n'
    
    # 写入文件
    output_path = os.path.join(BASE_DIR, 'index.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    # 验证
    print(f"\n--- 验证 ---")
    if 'yuhang87989.github.io' in final_html:
        print("✓ 图标路径已更新为GitHub Pages URL")
    else:
        print("✗ 图标路径未更新")
    
    style_count = final_html.count('<style>')
    script_count = final_html.count('<script>')
    print(f"✓ <style>标签数量: {style_count} (应为2: 全局 + 内联)")
    print(f"✓ <script>标签数量: {script_count} (应为3: PeerJS + 模块 + initApp)")
    
    if 'href="css/style.css"' in final_html:
        print("✗ 仍有外链CSS引用")
    else:
        print("✓ 无外链CSS引用")

    if 'src="js/' in final_html:
        print("✗ 仍有外链JS引用")
    else:
        print("✓ 无外链JS引用")
    
    # 验证HTML结构
    if '</head>' in final_html:
        print("✓ </head>存在")
    if '</body>' in final_html:
        print("✓ </body>存在")
    if '</html>' in final_html:
        print("✓ </html>存在")
    
    # 验证所有模块
    print("\n--- 模块检查 ---")
    for name in MODULE_NAMES.values():
        if name in final_html:
            print(f"  ✓ {name}")
        else:
            print(f"  ✗ {name} 未找到")
    
    print(f"\n✓ 合并完成！文件大小: {len(final_html):,} bytes")
    
    # 清理临时文件
    os.remove(source_path)
    print(f"✓ 已清理临时文件")

if __name__ == '__main__':
    main()
