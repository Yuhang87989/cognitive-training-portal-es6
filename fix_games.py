import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 修复游戏全屏显示 - 将游戏区域移到全屏容器中
# 找到游戏页面内容并修改 startGame 函数

old_start_game = '''function startGame(type) {
    gameType = type; gameScore = 0; gameLevel = 1;
    document.getElementById('game-area').style.display = 'block';
    document.getElementById('game-score').textContent = '0';
    switch(type) {
        case 'schulte': startSchulte(); break;
        case 'visual': startVisual(); break;
        case 'digit': startDigit(); break;
        case 'pattern': startPattern(); break;
        case 'tap': startTap(); break;
        case 'color': startColor(); break;
        case 'diff': startDiff(); break;
        case 'reason': startReason(); break;
    }
}'''

new_start_game = '''function startGame(type) {
    gameType = type; gameScore = 0; gameLevel = 1;
    // 显示全屏游戏区域
    const gameFullscreen = document.getElementById('game-fullscreen-container');
    if (gameFullscreen) {
        gameFullscreen.style.display = 'flex';
        document.getElementById('game-area').style.display = 'block';
    } else {
        document.getElementById('game-area').style.display = 'block';
    }
    document.getElementById('game-score').textContent = '0';
    switch(type) {
        case 'schulte': startSchulte(); break;
        case 'visual': startVisual(); break;
        case 'digit': startDigit(); break;
        case 'pattern': startPattern(); break;
        case 'tap': startTap(); break;
        case 'color': startColor(); break;
        case 'diff': startDiff(); break;
        case 'reason': startReason(); break;
    }
}'''

content = content.replace(old_start_game, new_start_game)

# 修复 closeGame 函数
old_close_game = '''function closeGame() { if (gameTimer) clearInterval(gameTimer); document.getElementById('game-area').style.display = 'none'; }'''

new_close_game = '''function closeGame() { 
    if (gameTimer) clearInterval(gameTimer); 
    document.getElementById('game-area').style.display = 'none';
    const gameFullscreen = document.getElementById('game-fullscreen-container');
    if (gameFullscreen) gameFullscreen.style.display = 'none';
}'''

content = content.replace(old_close_game, new_close_game)

# 修复 endGame 函数中的关闭按钮
old_end_game = '''function endGame() {
    if (gameTimer) clearInterval(gameTimer);
    const timeSpent = Math.round((Date.now()-gameStartTime)/1000);
    const board = document.getElementById('game-board');
    board.style.cssText = 'display:flex;align-items:center;justify-content:center;min-height:200px;';
    board.innerHTML = `<div style="text-align:center;"><div style="font-size:48px;margin-bottom:12px;">🎉</div><div style="font-size:20px;font-weight:bold;color:var(--blue);">游戏结束！</div><div style="font-size:36px;font-weight:bold;margin:16px 0;">得分：${gameScore}</div><div style="font-size:14px;color:var(--text-gray);">用时：${timeSpent}秒 · 到达关卡 ${gameLevel}</div></div>`;'''

new_end_game = '''function endGame() {
    if (gameTimer) clearInterval(gameTimer);
    const timeSpent = Math.round((Date.now()-gameStartTime)/1000);
    const board = document.getElementById('game-board');
    board.style.cssText = 'display:flex;align-items:center;justify-content:center;min-height:200px;';
    board.innerHTML = `<div style="text-align:center;"><div style="font-size:48px;margin-bottom:12px;">🎉</div><div style="font-size:20px;font-weight:bold;color:var(--blue);">游戏结束！</div><div style="font-size:36px;font-weight:bold;margin:16px 0;">得分：${gameScore}</div><div style="font-size:14px;color:var(--text-gray);">用时：${timeSpent}秒 · 到达关卡 ${gameLevel}</div><div style="margin-top:20px;display:flex;gap:12px;justify-content:center;"><button class="game-btn btn-blue" onclick="resetGame()">再来一次</button><button class="game-btn btn-orange" onclick="closeGame()">返回</button></div></div>`;'''

content = content.replace(old_end_game, new_end_game)

# 在游戏页面内容中添加游戏全屏容器
old_game_content_end = '''                <div class="game-card" onclick="startGame('reason')">
                    <div class="game-icon-area gradient-blue-solid">🧩</div>
                    <div class="game-name">图形推理</div>
                    <div class="game-desc">观察力训练</div>
                </div>
            </div>
            <div class="card" id="game-area" style="display:none;">'''

new_game_content_end = '''                <div class="game-card" onclick="startGame('reason')">
                    <div class="game-icon-area gradient-blue-solid">🧩</div>
                    <div class="game-name">图形推理</div>
                    <div class="game-desc">观察力训练</div>
                </div>
            </div>
        `
    },
    'game-play': {
        title: '🎮 游戏训练',
        content: `
            <div id="game-fullscreen-container" style="position:fixed;top:0;left:0;right:0;bottom:0;background:var(--bg-page);z-index:500;display:none;flex-direction:column;">
                <div style="display:flex;justify-content:space-between;align-items:center;padding:12px 16px;background:white;border-bottom:1px solid #eee;">
                    <button onclick="closeGame()" style="background:none;border:none;font-size:20px;cursor:pointer;">← 返回</button>
                    <div id="game-title" style="font-size:16px;font-weight:bold;">游戏</div>
                    <div id="game-score" style="font-size:18px;font-weight:bold;color:var(--blue);">0</div>
                </div>
                <div id="game-area" style="flex:1;display:none;padding:16px;overflow:auto;">
                    <div id="game-board" class="game-board size-3"></div>
                </div>
            </div>
            <div class="card" id="game-area" style="display:none;">'''

content = content.replace(old_game_content_end, new_game_content_end)

# 添加 game-play 页面到 pageContent
# 在 games 页面的 content 末尾添加进入游戏按钮

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("游戏修复完成!")
