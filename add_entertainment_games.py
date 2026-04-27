#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为认知训练门户V126添加8个娱乐游戏
"""
import re

# 读取文件
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"文件大小: {len(content)} 字节, 行数: {content.count(chr(10))}")

# 1. 修改存储键版本号
content = content.replace("cognitive_training_v126", "cognitive_training_v127")
print("✓ 更新存储键为 V127")

# 2. 修改renderGames函数 - 添加娱乐游戏分组
# 找到renderGames函数中的games数组结束和统计部分，在统计前插入娱乐游戏
old_render_games = '''        </div>
        
        <div class="card" style="margin-top:12px;">
            <h4 style="margin-bottom:12px;">📊 游戏统计</h4>'''

new_render_games = '''        </div>
        
        <div class="card" style="margin-top:12px;">
            <h3 style="margin-bottom:12px;">🎮 娱乐游戏</h3>
            <p style="color:#666;font-size:13px;margin-bottom:16px;">轻松一刻，享受游戏乐趣！</p>
            
            <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:12px;">
                <div onclick="startGame('snake')" style="background:linear-gradient(135deg,#43A047,#66BB6A);color:white;padding:16px;border-radius:16px;cursor:pointer;position:relative;overflow:hidden;">
                    <div style="font-size:28px;margin-bottom:8px;">🐍</div>
                    <div style="font-size:14px;font-weight:600;">贪吃蛇</div>
                    <div style="font-size:11px;opacity:0.9;margin-top:4px;">经典益智</div>
                    ${gameScores['snake'] ? `<div style="position:absolute;top:8px;right:8px;background:rgba(255,255,255,0.3);padding:4px 8px;border-radius:12px;font-size:11px;">🏆 ${gameScores['snake']}</div>` : ''}
                </div>
                <div onclick="startGame('tetris')" style="background:linear-gradient(135deg,#E53935,#EF5350);color:white;padding:16px;border-radius:16px;cursor:pointer;position:relative;overflow:hidden;">
                    <div style="font-size:28px;margin-bottom:8px;">🧱</div>
                    <div style="font-size:14px;font-weight:600;">俄罗斯方块</div>
                    <div style="font-size:11px;opacity:0.9;margin-top:4px;">经典益智</div>
                    ${gameScores['tetris'] ? `<div style="position:absolute;top:8px;right:8px;background:rgba(255,255,255,0.3);padding:4px 8px;border-radius:12px;font-size:11px;">🏆 ${gameScores['tetris']}</div>` : ''}
                </div>
                <div onclick="startGame('flipcard')" style="background:linear-gradient(135deg,#1E88E5,#42A5F5);color:white;padding:16px;border-radius:16px;cursor:pointer;position:relative;overflow:hidden;">
                    <div style="font-size:28px;margin-bottom:8px;">🃏</div>
                    <div style="font-size:14px;font-weight:600;">记忆翻牌</div>
                    <div style="font-size:11px;opacity:0.9;margin-top:4px;">记忆力挑战</div>
                    ${gameScores['flipcard'] ? `<div style="position:absolute;top:8px;right:8px;background:rgba(255,255,255,0.3);padding:4px 8px;border-radius:12px;font-size:11px;">🏆 ${gameScores['flipcard']}</div>` : ''}
                </div>
                <div onclick="startGame('slide')" style="background:linear-gradient(135deg,#FB8C00,#FFA726);color:white;padding:16px;border-radius:16px;cursor:pointer;position:relative;overflow:hidden;">
                    <div style="font-size:28px;margin-bottom:8px;">🔢</div>
                    <div style="font-size:14px;font-weight:600;">数字华容道</div>
                    <div style="font-size:11px;opacity:0.9;margin-top:4px;">益智解谜</div>
                    ${gameScores['slide'] ? `<div style="position:absolute;top:8px;right:8px;background:rgba(255,255,255,0.3);padding:4px 8px;border-radius:12px;font-size:11px;">🏆 ${gameScores['slide']}</div>` : ''}
                </div>
                <div onclick="startGame('g2048')" style="background:linear-gradient(135deg,#EDC22E,#F0D060);color:white;padding:16px;border-radius:16px;cursor:pointer;position:relative;overflow:hidden;">
                    <div style="font-size:28px;margin-bottom:8px;">🎮</div>
                    <div style="font-size:14px;font-weight:600;">2048</div>
                    <div style="font-size:11px;opacity:0.9;margin-top:4px;">数字合并</div>
                    ${gameScores['g2048'] ? `<div style="position:absolute;top:8px;right:8px;background:rgba(255,255,255,0.3);padding:4px 8px;border-radius:12px;font-size:11px;">🏆 ${gameScores['g2048']}</div>` : ''}
                </div>
                <div onclick="startGame('whack')" style="background:linear-gradient(135deg,#8E24AA,#AB47BC);color:white;padding:16px;border-radius:16px;cursor:pointer;position:relative;overflow:hidden;">
                    <div style="font-size:28px;margin-bottom:8px;">🔨</div>
                    <div style="font-size:14px;font-weight:600;">打地鼠</div>
                    <div style="font-size:11px;opacity:0.9;margin-top:4px;">反应速度</div>
                    ${gameScores['whack'] ? `<div style="position:absolute;top:8px;right:8px;background:rgba(255,255,255,0.3);padding:4px 8px;border-radius:12px;font-size:11px;">🏆 ${gameScores['whack']}</div>` : ''}
                </div>
                <div onclick="startGame('linkup')" style="background:linear-gradient(135deg,#00897B,#26A69A);color:white;padding:16px;border-radius:16px;cursor:pointer;position:relative;overflow:hidden;">
                    <div style="font-size:28px;margin-bottom:8px;">🔗</div>
                    <div style="font-size:14px;font-weight:600;">连连看</div>
                    <div style="font-size:11px;opacity:0.9;margin-top:4px;">图案配对</div>
                    ${gameScores['linkup'] ? `<div style="position:absolute;top:8px;right:8px;background:rgba(255,255,255,0.3);padding:4px 8px;border-radius:12px;font-size:11px;">🏆 ${gameScores['linkup']}</div>` : ''}
                </div>
                <div onclick="startGame('eliminate')" style="background:linear-gradient(135deg,#F4511E,#FF7043);color:white;padding:16px;border-radius:16px;cursor:pointer;position:relative;overflow:hidden;">
                    <div style="font-size:28px;margin-bottom:8px;">💎</div>
                    <div style="font-size:14px;font-weight:600;">消消乐</div>
                    <div style="font-size:11px;opacity:0.9;margin-top:4px;">宝石消除</div>
                    ${gameScores['eliminate'] ? `<div style="position:absolute;top:8px;right:8px;background:rgba(255,255,255,0.3);padding:4px 8px;border-radius:12px;font-size:11px;">🏆 ${gameScores['eliminate']}</div>` : ''}
                </div>
            </div>
        </div>
        
        <div class="card" style="margin-top:12px;">
            <h4 style="margin-bottom:12px;">📊 游戏统计</h4>'''

if old_render_games in content:
    content = content.replace(old_render_games, new_render_games)
    print("✓ 添加娱乐游戏分组到renderGames")
else:
    print("✗ 未找到renderGames的插入位置")

# 3. 修改gameConfig - 添加8个娱乐游戏配置
old_gameConfig_end = '''    attention: {name:'🎯 注意力追踪',color:'#FF9A9E',gradient:'linear-gradient(135deg,#ff9a9e,#fecfef)'}
};'''

new_gameConfig_end = '''    attention: {name:'🎯 注意力追踪',color:'#FF9A9E',gradient:'linear-gradient(135deg,#ff9a9e,#fecfef)'},
    // 娱乐游戏配置
    snake: {name:'🐍 贪吃蛇',color:'#43A047',gradient:'linear-gradient(135deg,#43A047,#66BB6A)'},
    tetris: {name:'🧱 俄罗斯方块',color:'#E53935',gradient:'linear-gradient(135deg,#E53935,#EF5350)'},
    flipcard: {name:'🃏 记忆翻牌',color:'#1E88E5',gradient:'linear-gradient(135deg,#1E88E5,#42A5F5)'},
    slide: {name:'🔢 数字华容道',color:'#FB8C00',gradient:'linear-gradient(135deg,#FB8C00,#FFA726)'},
    g2048: {name:'🎮 2048',color:'#EDC22E',gradient:'linear-gradient(135deg,#EDC22E,#F0D060)'},
    whack: {name:'🔨 打地鼠',color:'#8E24AA',gradient:'linear-gradient(135deg,#8E24AA,#AB47BC)'},
    linkup: {name:'🔗 连连看',color:'#00897B',gradient:'linear-gradient(135deg,#00897B,#26A69A)'},
    eliminate: {name:'💎 消消乐',color:'#F4511E',gradient:'linear-gradient(135deg,#F4511E,#FF7043)'}
};'''

if old_gameConfig_end in content:
    content = content.replace(old_gameConfig_end, new_gameConfig_end)
    print("✓ 添加娱乐游戏到gameConfig")
else:
    print("✗ 未找到gameConfig的结束位置")

# 4. 修改startGame的switch - 添加8个case
old_switch_end = '''            case 'attention': startAttentionTrack(); break;
        }
    }, 100);
}'''

new_switch_end = '''            case 'attention': startAttentionTrack(); break;
            case 'snake': startSnake(); break;
            case 'tetris': startTetris(); break;
            case 'flipcard': startFlipCard(); break;
            case 'slide': startSlide(); break;
            case 'g2048': start2048(); break;
            case 'whack': startWhack(); break;
            case 'linkup': startLinkUp(); break;
            case 'eliminate': startEliminate(); break;
        }
    }, 100);
}'''

if old_switch_end in content:
    content = content.replace(old_switch_end, new_switch_end)
    print("✓ 添加娱乐游戏case到startGame")
else:
    print("✗ 未找到startGame的switch结束位置")

# 5. 添加8个娱乐游戏实现代码
entertainment_games_code = '''

// ==================== 娱乐游戏实现 ====================

// ----- 贪吃蛇游戏 -----
let snakeGame = null;
function startSnake() {
    document.getElementById('game-title').textContent = '🐍 贪吃蛇';
    const board = document.getElementById('game-board');
    board.style.display = 'block';
    board.innerHTML = '<div id="snake-container" style="display:flex;justify-content:center;align-items:center;height:100%;"><canvas id="snake-canvas" style="border:3px solid #43A047;border-radius:8px;"></canvas></div>';
    
    const canvas = document.getElementById('snake-canvas');
    const ctx = canvas.getContext('2d');
    const size = 300;
    canvas.width = size;
    canvas.height = size;
    
    const gridSize = 15;
    const gridCount = size / gridSize;
    
    let snake = [{x:5,y:5}];
    let direction = {x:1,y:0};
    let nextDirection = {x:1,y:0};
    let food = {x:10,y:10};
    let score = 0;
    let gameOver = false;
    let speed = 150;
    
    function placeFood() {
        do {
            food = {x:Math.floor(Math.random()*gridCount),y:Math.floor(Math.random()*gridCount)};
        } while (snake.some(s=>s.x===food.x&&s.y===food.y));
    }
    
    function draw() {
        ctx.fillStyle = '#f5f5f5';
        ctx.fillRect(0,0,size,size);
        
        // 网格线
        ctx.strokeStyle = '#ddd';
        for(let i=0;i<=gridCount;i++) {
            ctx.beginPath();
            ctx.moveTo(i*gridSize,0);
            ctx.lineTo(i*gridSize,size);
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(0,i*gridSize);
            ctx.lineTo(size,i*gridSize);
            ctx.stroke();
        }
        
        // 食物
        ctx.fillStyle = '#FF6B6B';
        ctx.beginPath();
        ctx.arc(food.x*gridSize+gridSize/2,food.y*gridSize+gridSize/2,gridSize/2-2,0,Math.PI*2);
        ctx.fill();
        
        // 蛇
        snake.forEach((seg,i) => {
            ctx.fillStyle = i===0 ? '#43A047' : '#66BB6A';
            ctx.fillRect(seg.x*gridSize+1,seg.y*gridSize+1,gridSize-2,gridSize-2);
        });
    }
    
    function update() {
        if(gameOver) return;
        direction = nextDirection;
        const head = {x:snake[0].x+direction.x,y:snake[0].y+direction.y};
        
        if(head.x<0||head.x>=gridCount||head.y<0||head.y>=gridCount||snake.some(s=>s.x===head.x&&s.y===head.y)) {
            gameOver = true;
            clearInterval(snakeGame);
            gameScore = score;
            document.getElementById('game-score').textContent = score;
            endGame();
            return;
        }
        
        snake.unshift(head);
        if(head.x===food.x&&head.y===food.y) {
            score++;
            gameScore = score;
            document.getElementById('game-score').textContent = score;
            SoundEffects.playCorrect();
            placeFood();
            if(score%5===0) {
                gameLevel++;
                updateGameLevelBadge();
                speed = Math.max(50,speed-10);
                clearInterval(snakeGame);
                snakeGame = setInterval(update,速度);
            }
        } else {
            snake.pop();
        }
        draw();
    }
    
    placeFood();
    draw();
    
    if(snakeGame) clearInterval(snakeGame);
    snakeGame = setInterval(update,速度);
    
    // 触屏控制
    let touchStartX = 0, touchStartY = 0;
    canvas.addEventListener('touchstart',e=>{
        touchStartX = e.touches[0].clientX;
        touchStartY = e.touches[0].clientY;
    });
    canvas.addEventListener('touchend',e=>{
        const dx = e.changedTouches[0].clientX - touchStartX;
        const dy = e.changedTouches[0].clientY - touchStartY;
        if(Math.abs(dx)>Math.abs(dy)) {
            if(dx>20&&direction.x!==-1) nextDirection={x:1,y:0};
            else if(dx<-20&&direction.x!==1) nextDirection={x:-1,y:0};
        } else {
            if(dy>20&&direction.y!==-1) nextDirection={x:0,y:1};
            else if(dy<-20&&direction.y!==1) nextDirection={x:0,y:-1};
        }
    });
    
    // 键盘控制
    document.addEventListener('keydown',e=>{
        if(e.key==='ArrowUp'&&direction.y!==1) nextDirection={x:0,y:-1};
        else if(e.key==='ArrowDown'&&direction.y!==-1) nextDirection={x:0,y:1};
        else if(e.key==='ArrowLeft'&&direction.x!==1) nextDirection={x:-1,y:0};
        else if(e.key==='ArrowRight'&&direction.x!==-1) nextDirection={x:1,y:0};
    });
    
    score = 0;
}

// ----- 俄罗斯方块 -----
let tetrisGame = null;
function startTetris() {
    document.getElementById('game-title').textContent = '🧱 俄罗斯方块';
    const board = document.getElementById('game-board');
    board.style.display = 'block';
    board.innerHTML = '<div id="tetris-container" style="display:flex;justify-content:center;align-items:center;height:100%;gap:20px;"><canvas id="tetris-canvas" style="border:3px solid #E53935;border-radius:8px;"></canvas><div id="tetris-next" style="padding:10px;background:#fff;border-radius:8px;"><div style="font-size:12px;color:#666;margin-bottom:8px;">下一个</div><canvas id="tetris-next-canvas" width="80" height="80"></canvas></div></div>';
    
    const canvas = document.getElementById('tetris-canvas');
    const ctx = canvas.getContext('2d');
    const nextCanvas = document.getElementById('tetris-next-canvas');
    const nextCtx = nextCanvas.getContext('2d');
    
    const cols = 10, rows = 16, cellSize = 20;
    canvas.width = cols * cellSize;
    canvas.height = rows * cellSize;
    
    const pieces = [
        {shape:[[1,1,1,1]],color:'#3498db'},
        {shape:[[1,1],[1,1]],color:'#f1c40f'},
        {shape:[[0,1,0],[1,1,1]],color:'#9b59b6'},
        {shape:[[1,0,0],[1,1,1]],color:'#e67e22'},
        {shape:[[0,0,1],[1,1,1]],color:'#1abc9c'},
        {shape:[[1,1,0],[0,1,1]],color:'#e74c3c'},
        {shape:[[0,1,1],[1,1,0]],color:'#2ecc71'}
    ];
    
    let board2d = Array.from({length:rows},()=>Array(cols).fill(0));
    let current = null, nextPiece = null;
    let x = 0, y = 0;
    let score = 0, lines = 0;
    let gameOver = false;
    let speed = 500;
    let lastDrop = Date.now();
    
    function randomPiece() {
        const p = pieces[Math.floor(Math.random()*pieces.length)];
        return {shape:p.shape.map(row=>[...row]),color:p.color};
    }
    
    function drawCell(c, ctx2, x2, y2, color, size2=cellSize) {
        ctx2.fillStyle = color;
        ctx2.fillRect(x2*size2+1,y2*size2+1,size2-2,size2-2);
        ctx2.fillStyle = 'rgba(255,255,255,0.3)';
        ctx2.fillRect(x2*size2+2,y2*size2+2,size2-6,3);
    }
    
    function drawBoard() {
        ctx.fillStyle = '#f5f5f5';
        ctx.fillRect(0,0,canvas.width,canvas.height);
        for(let r=0;r<rows;r++) for(let c=0;c<cols;c++) {
            if(board2d[r][c]) drawCell(null,ctx,c,r,board2d[r][c]);
        }
        ctx.strokeStyle = '#ddd';
        for(let i=0;i<=cols;i++) {ctx.beginPath();ctx.moveTo(i*cellSize,0);ctx.lineTo(i*cellSize,canvas.height);ctx.stroke();}
        for(let i=0;i<=rows;i++) {ctx.beginPath();ctx.moveTo(0,i*cellSize);ctx.lineTo(canvas.width,i*cellSize);ctx.stroke();}
    }
    
    function drawCurrent() {
        if(!current) return;
        current.shape.forEach((row,ri) => row.forEach((cell,ci) => {
            if(cell) drawCell(null,ctx,x+ci,y+ri,current.color);
        }));
    }
    
    function drawNext() {
        nextCtx.fillStyle = '#fff';
        nextCtx.fillRect(0,0,80,80);
        if(!nextPiece) return;
        const sz = 18;
        nextPiece.shape.forEach((row,ri) => row.forEach((cell,ci) => {
            if(cell) {
                nextCtx.fillStyle = nextPiece.color;
                nextCtx.fillRect(ci*sz+2,ri*sz+2,sz-4,sz-4);
            }
        }));
    }
    
    function canMove(shape, nx, ny) {
        for(let r=0;r<shape.length;r++) for(let c=0;c<shape[r].length;c++) {
            if(shape[r][c]) {
                if(nx+c<0||nx+c>=cols||ny+r>=rows) return false;
                if(ny+r>=0&&board2d[ny+r][nx+c]) return false;
            }
        }
        return true;
    }
    
    function lockPiece() {
        current.shape.forEach((row,ri) => row.forEach((cell,ci) => {
            if(cell) board2d[y+ri][x+ci] = current.color;
        }));
        
        let cleared = 0;
        for(let r=rows-1;r>=0;r--) {
            if(board2d[r].every(c=>c)) {
                board2d.splice(r,1);
                board2d.unshift(Array(cols).fill(0));
                cleared++;
                r++;
            }
        }
        
        if(cleared>0) {
            lines += cleared;
            score += cleared * 100 * cleared;
            gameScore = score;
            document.getElementById('game-score').textContent = score;
            if(lines%10===0) {
                gameLevel++;
                updateGameLevelBadge();
                speed = Math.max(100,speed-30);
            }
        }
        
        current = nextPiece;
        nextPiece = randomPiece();
        x = Math.floor(cols/2) - Math.floor(current.shape[0].length/2);
        y = 0;
        drawNext();
        
        if(!canMove(current.shape,x,y)) {
            gameOver = true;
            clearInterval(tetrisGame);
            endGame();
        }
    }
    
    function rotate(shape) {
        const rows2 = shape.length, cols2 = shape[0].length;
        const rotated = Array.from({length:cols2},()=>Array(rows2).fill(0));
        for(let r=0;r<rows2;r++) for(let c=0;c<cols2;c++) rotated[c][rows2-1-r] = shape[r][c];
        return rotated;
    }
    
    function tick() {
        if(gameOver) return;
        if(!canMove(current.shape,x,y+1)) {
            lockPiece();
        } else {
            y++;
        }
        drawBoard();
        drawCurrent();
    }
    
    current = randomPiece();
    nextPiece = randomPiece();
    x = Math.floor(cols/2) - Math.floor(current.shape[0].length/2);
    y = 0;
    drawNext();
    
    if(tetrisGame) clearInterval(tetrisGame);
    tetrisGame = setInterval(tick,速度);
    
    let touchStartX = 0, touchStartY = 0;
    board.addEventListener('touchstart',e=>{
        touchStartX = e.touches[0].clientX;
        touchStartY = e.touches[0].clientY;
    });
    board.addEventListener('touchend',e=>{
        const dx = e.changedTouches[0].clientX - touchStartX;
        const dy = e.changedTouches[0].clientY - touchStartY;
        if(Math.abs(dx)>30||Math.abs(dy)>30) {
            if(dy<-30) { // 上滑旋转
                const rotated = rotate(current.shape);
                if(canMove(rotated,x,y)) current.shape = rotated;
            } else if(dy>30) { // 下滑加速
                while(canMove(current.shape,x,y+1)) y++;
            } else if(dx>30) {
                if(canMove(current.shape,x+1,y)) x++;
            } else if(dx<-30) {
                if(canMove(current.shape,x-1,y)) x--;
            }
        }
    });
    
    document.addEventListener('keydown',e=>{
        if(e.key==='ArrowLeft'&&canMove(current.shape,x-1,y)) x--;
        else if(e.key==='ArrowRight'&&canMove(current.shape,x+1,y)) x++;
        else if(e.key==='ArrowDown'&&canMove(current.shape,x,y+1)) y++;
        else if(e.key==='ArrowUp') {
            const rotated = rotate(current.shape);
            if(canMove(rotated,x,y)) current.shape = rotated;
        }
    });
    
    score = 0; lines = 0;
}

// ----- 记忆翻牌游戏 -----
let flipCards = [], flipped = [], matched = 0, flips = 0;
function startFlipCard() {
    document.getElementById('game-title').textContent = '🃏 记忆翻牌';
    const board = document.getElementById('game-board');
    board.style.display = 'block';
    board.innerHTML = '<div id="flip-container" style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;padding:10px;max-width:320px;margin:0 auto;"></div>';
    
    const icons = ['🍎','🍌','🍇','🍓','🌟','🌙','🔥','💎'];
    flipCards = [...icons,...icons].sort(()=>Math.random()-0.5);
    flipped = []; matched = 0; flips = 0;
    
    const container = document.getElementById('flip-container');
    flipCards.forEach((icon,i) => {
        const card = document.createElement('div');
        card.id = 'flip-'+i;
        card.style.cssText = 'width:70px;height:70px;background:linear-gradient(135deg,#1E88E5,#42A5F5);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:32px;cursor:pointer;transition:transform 0.3s;transform-style:preserve-3d;';
        card.innerHTML = '<span style="opacity:0.3;">❓</span>';
        card.onclick = () => flipCard(i, card);
        container.appendChild(card);
    });
    
    gameScore = 0;
    document.getElementById('game-score').textContent = '0';
}

function flipCard(idx, el) {
    if(flipped.length>=2||flipped.includes(idx)||matched>=8) return;
    el.style.transform = 'rotateY(180deg)';
    el.innerHTML = '<span>'+flipCards[idx]+'</span>';
    flipped.push(idx);
    
    if(flipped.length===2) {
        flips++;
        gameScore = flips;
        document.getElementById('game-score').textContent = flips;
        
        if(flipCards[flipped[0]]===flipCards[flipped[1]]) {
            matched++;
            SoundEffects.playCorrect();
            if(matched===8) {
                setTimeout(()=>{
                    gameLevel++;
                    updateGameLevelBadge();
                    startFlipCard();
                },1000);
            }
            flipped = [];
        } else {
            SoundEffects.playWrong();
            setTimeout(()=>{
                const c1 = document.getElementById('flip-'+flipped[0]);
                const c2 = document.getElementById('flip-'+flipped[1]);
                if(c1) {c1.style.transform='';c1.innerHTML='<span style="opacity:0.3;">❓</span>';}
                if(c2) {c2.style.transform='';c2.innerHTML='<span style="opacity:0.3;">❓</span>';}
                flipped = [];
            },800);
        }
    }
}

// ----- 数字华容道 -----
let slideBoard = [], slideSize = 4, slideEmpty = {x:3,y:3}, slideMoves = 0;
function startSlide() {
    document.getElementById('game-title').textContent = '🔢 数字华容道';
    const board = document.getElementById('game-board');
    board.style.display = 'block';
    board.innerHTML = '<div id="slide-container" style="display:grid;grid-template-columns:repeat(4,1fr);gap:6px;padding:10px;max-width:300px;margin:0 auto;"></div><div style="text-align:center;margin-top:16px;"><button onclick="shuffleSlide()" style="padding:10px 24px;background:#FB8C00;color:white;border:none;border-radius:8px;cursor:pointer;">重新开始</button></div>';
    
    slideBoard = [];
    for(let i=1;i<16;i++) slideBoard.push(i);
    slideBoard.push(0);
    slideEmpty = {x:3,y:3};
    slideMoves = 0;
    shuffleSlide();
    
    gameScore = 0;
    document.getElementById('game-score').textContent = '0';
}

function shuffleSlide() {
    for(let i=0;i<100;i++) {
        const dirs = [];
        if(slideEmpty.x>0) dirs.push({x:-1,y:0});
        if(slideEmpty.x<3) dirs.push({x:1,y:0});
        if(slideEmpty.y>0) dirs.push({x:0,y:-1});
        if(slideEmpty.y<3) dirs.push({x:0,y:1});
        const d = dirs[Math.floor(Math.random()*dirs.length)];
        const nx = slideEmpty.x + d.x;
        const ny = slideEmpty.y + d.y;
        const idx = ny*4+nx;
        const emptyIdx = slideEmpty.y*4+slideEmpty.x;
        [slideBoard[idx],slideBoard[emptyIdx]] = [slideBoard[emptyIdx],slideBoard[idx]];
        slideEmpty = {x:nx,y:ny};
    }
    renderSlide();
}

function renderSlide() {
    const container = document.getElementById('slide-container');
    if(!container) return;
    container.innerHTML = '';
    slideBoard.forEach((num,i) => {
        const x = i%4, y = Math.floor(i/4);
        const cell = document.createElement('div');
        if(num===0) {
            cell.style.cssText = 'width:65px;height:65px;background:#ddd;border-radius:8px;';
        } else {
            cell.style.cssText = 'width:65px;height:65px;background:linear-gradient(135deg,#FB8C00,#FFA726);border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:24px;font-weight:bold;color:white;cursor:pointer;';
            cell.textContent = num;
            cell.onclick = () => moveSlide(x,y);
        }
        container.appendChild(cell);
    });
}

function moveSlide(x,y) {
    if((Math.abs(x-slideEmpty.x)===1&&y===slideEmpty.y)||(Math.abs(y-slideEmpty.y)===1&&x===slideEmpty.x)) {
        const idx = y*4+x;
        const emptyIdx = slideEmpty.y*4+slideEmpty.x;
        [slideBoard[idx],slideBoard[emptyIdx]] = [slideBoard[emptyIdx],slideBoard[idx]];
        slideEmpty = {x,y};
        slideMoves++;
        gameScore = slideMoves;
        document.getElementById('game-score').textContent = slideMoves;
        renderSlide();
        
        if(isSolved()) {
            SoundEffects.playComplete();
            gameLevel++;
            updateGameLevelBadge();
            setTimeout(()=>startSlide(),1000);
        }
    }
}

function isSolved() {
    for(let i=0;i<15;i++) if(slideBoard[i]!==i+1) return false;
    return slideBoard[15]===0;
}

// ----- 2048游戏 -----
let g2048Board = [], g2048Score = 0;
function start2048() {
    document.getElementById('game-title').textContent = '🎮 2048';
    const board = document.getElementById('game-board');
    board.style.display = 'block';
    board.innerHTML = '<div id="g2048-container" style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;padding:10px;max-width:320px;margin:0 auto;background:#bbada0;border-radius:12px;"></div><div style="text-align:center;margin-top:12px;"><button onclick="reset2048()" style="padding:10px 20px;background:#8f7a66;color:white;border:none;border-radius:8px;cursor:pointer;">重新开始</button></div>';
    
    g2048Board = Array(16).fill(0);
    g2048Score = 0;
    add2048Tile();
    add2048Tile();
    render2048();
    
    document.getElementById('game-score').textContent = '0';
}

function add2048Tile() {
    const empty = [];
    g2048Board.forEach((v,i)=>{if(v===0)empty.push(i);});
    if(empty.length) g2048Board[empty[Math.floor(Math.random()*empty.length)]] = Math.random()<0.9?2:4;
}

function render2048() {
    const container = document.getElementById('g2048-container');
    if(!container) return;
    container.innerHTML = '';
    const colors = {0:'#cdc1b4',2:'#eee4da',4:'#ede0c8',8:'#f2b179',16:'#f59563',32:'#f67c5f',64:'#f65e3b',128:'#edcf72',256:'#edcc61',512:'#edc850',1024:'#edc53f',2048:'#edc22e'};
    g2048Board.forEach((v,i)=>{
        const cell = document.createElement('div');
        cell.style.cssText = `width:70px;height:70px;background:${colors[v]||'#3c3a32'};border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:${v>=1000?20:24}px;font-weight:bold;color:${v<=4?'#776e65':'#fff'};`;
        if(v) cell.textContent = v;
        container.appendChild(cell);
    });
}

function move2048(dir) {
    const old = [...g2048Board];
    const rotate = (b,times) => {let r=[...b];for(let t=0;t<times;t++){const n=Array(16).fill(0);for(let i=0;i<16;i++)n[(3-i%4)*4+i%4]=b[i];r=n;}return r;};
    let b = rotate(g2048Board,dir);
    
    for(let r=0;r<4;r++) {
        let row = b.slice(r*4,r*4+4).filter(v=>v);
        for(let i=0;i<row.length-1;i++) if(row[i]===row[i+1]){row[i]*=2;g2048Score+=row[i];row.splice(i+1,1);}
        while(row.length<4) row.push(0);
        for(let c=0;c<4;c++) b[r*4+c]=row[c];
    }
    
    g2048Board = rotate(b,(4-dir)%4);
    gameScore = g2048Score;
    document.getElementById('game-score').textContent = g2048Score;
    
    if(JSON.stringify(old)!==JSON.stringify(g2048Board)) {
        add2048Tile();
        render2048();
        
        if(g2048Board.includes(2048)) {
            SoundEffects.playComplete();
            setTimeout(()=>{gameLevel++;updateGameLevelBadge();reset2048();},500);
        } else if(g2048Board.every(v=>v!==0)&&!canMove2048()) {
            endGame();
        }
    }
}

function canMove2048() {
    for(let i=0;i<16;i++) {
        if(g2048Board[i]===0) return true;
        if(i%4!==3&&g2048Board[i]===g2048Board[i+1]) return true;
        if(i<12&&g2048Board[i]===g2048Board[i+4]) return true;
    }
    return false;
}

function reset2048() { start2048(); }

// ----- 打地鼠游戏 -----
let whackMoles = [], whackTimer = null, whackTimeLeft = 30, whackActive = 0;
function startWhack() {
    document.getElementById('game-title').textContent = '🔨 打地鼠';
    const board = document.getElementById('game-board');
    board.style.display = 'block';
    board.innerHTML = '<div style="text-align:center;margin-bottom:16px;"><span id="whack-timer" style="font-size:24px;font-weight:bold;color:#8E24AA;">30</span>秒</div><div id="whack-container" style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;padding:20px;max-width:320px;margin:0 auto;"></div>';
    
    whackMoles = Array(9).fill(0);
    whackTimeLeft = 30;
    whackActive = 0;
    
    const container = document.getElementById('whack-container');
    for(let i=0;i<9;i++) {
        const hole = document.createElement('div');
        hole.style.cssText = 'width:80px;height:80px;background:#8B4513;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;position:relative;overflow:hidden;';
        hole.innerHTML = '<div id="whack-'+i+'" style="position:absolute;bottom:-50px;width:50px;height:50px;background:#D2691E;border-radius:50%;transition:bottom 0.15s;font-size:32px;text-align:center;line-height:50px;">🐹</div>';
        hole.onclick = () => whackMole(i);
        container.appendChild(hole);
    }
    
    gameScore = 0;
    document.getElementById('game-score').textContent = '0';
    
    if(whackTimer) clearInterval(whackTimer);
    whackTimer = setInterval(()=>{
        whackTimeLeft--;
        document.getElementById('whack-timer').textContent = whackTimeLeft;
        
        if(whackTimeLeft<=0) {
            clearInterval(whackTimer);
            endGame();
        } else {
            showMole();
        }
    },1000);
}

function showMole() {
    // 隐藏所有
    whackMoles.forEach((_,i)=>{
        const el = document.getElementById('whack-'+i);
        if(el) el.style.bottom = '-50px';
    });
    whackMoles = whackMoles.map(()=>0);
    
    // 显示新的
    const speed = Math.max(300,800-gameLevel*50);
    const count = Math.min(3,1+Math.floor(gameLevel/2));
    for(let i=0;i<count;i++) {
        setTimeout(()=>{
            const idx = Math.floor(Math.random()*9);
            const el = document.getElementById('whack-'+idx);
            if(el && whackMoles[idx]===0) {
                whackMoles[idx] = 1;
                el.style.bottom = '15px';
                setTimeout(()=>{
                    if(whackMoles[idx]===1) {
                        whackMoles[idx] = 0;
                        el.style.bottom = '-50px';
                    }
                },速度);
            }
        },i*200);
    }
}

function whackMole(idx) {
    if(whackMoles[idx]===1) {
        whackMoles[idx] = 0;
        const el = document.getElementById('whack-'+idx);
        if(el) el.style.bottom = '-50px';
        gameScore++;
        document.getElementById('game-score').textContent = gameScore;
        SoundEffects.playCorrect();
    }
}

// ----- 连连看游戏 -----
let linkIcons = [], linkSelected = [], linkPairs = 0, linkBoard = [];
function startLinkUp() {
    document.getElementById('game-title').textContent = '🔗 连连看';
    const board = document.getElementById('game-board');
    board.style.display = 'block';
    board.innerHTML = '<div id="link-container" style="display:grid;grid-template-columns:repeat(6,1fr);gap:4px;padding:10px;max-width:340px;margin:0 auto;"></div>';
    
    const emojis = ['🍎','🍊','🍋','🍇','🍓','🍒','🥝','🌟','❤️','🔵','💜','💚'];
    linkIcons = emojis.slice(0,18);
    linkBoard = [...linkIcons,...linkIcons].sort(()=>Math.random()-0.5);
    linkSelected = [];
    linkPairs = 0;
    
    const container = document.getElementById('link-container');
    linkBoard.forEach((icon,i)=>{
        const cell = document.createElement('div');
        cell.id = 'link-'+i;
        cell.style.cssText = 'width:50px;height:50px;background:#00897B;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:26px;cursor:pointer;';
        cell.textContent = icon;
        cell.onclick = () => clickLink(i);
        container.appendChild(cell);
    });
    
    gameScore = 0;
    document.getElementById('game-score').textContent = '0';
}

function clickLink(idx) {
    const el = document.getElementById('link-'+idx);
    if(!el||el.style.background==='#ccc'||linkSelected.length>=2) return;
    
    linkSelected.push(idx);
    el.style.transform = 'scale(1.1)';
    
    if(linkSelected.length===2) {
        gameScore++;
        document.getElementById('game-score').textContent = gameScore;
        
        const [i1,i2] = linkSelected;
        if(linkBoard[i1]===linkBoard[i2]&&canConnect(i1,i2)) {
            SoundEffects.playCorrect();
            setTimeout(()=>{
                document.getElementById('link-'+i1).style.background = '#ccc';
                document.getElementById('link-'+i2).style.background = '#ccc';
                document.getElementById('link-'+i1).style.pointerEvents = 'none';
                document.getElementById('link-'+i2).style.pointerEvents = 'none';
                linkPairs++;
                linkSelected = [];
                
                if(linkPairs===18) {
                    gameLevel++;
                    updateGameLevelBadge();
                    startLinkUp();
                }
            },200);
        } else {
            SoundEffects.playWrong();
            setTimeout(()=>{
                linkSelected.forEach(i=>{
                    const e = document.getElementById('link-'+i);
                    if(e) e.style.transform = '';
                });
                linkSelected = [];
            },500);
        }
    }
}

function canConnect(a,b) {
    const r1=Math.floor(a/6),c1=a%6,r2=Math.floor(b/6),c2=b%6;
    // 直线连接
    if(r1===r2) {
        for(let c=Math.min(c1,c2)+1;c<Math.max(c1,c2);c++) if(linkBoard[r1*6+c]!=='') return false;
        return true;
    }
    if(c1===c2) {
        for(let r=Math.min(r1,r2)+1;r<Math.max(r1,r2);r++) if(linkBoard[r*6+c1]!=='') return false;
        return true;
    }
    // 一个拐角
    if(linkBoard[r1*6+c2]==='') return true;
    if(linkBoard[r2*6+c1]==='') return true;
    // 两个拐角
    for(let r=0;r<6;r++) {
        if(linkBoard[r*6+c1]===''&&linkBoard[r*6+c2]==='') {
            let clear=true;
            for(let c=Math.min(c1,c2)+1;c<Math.max(c1,c2);c++) if(linkBoard[r*6+c]!=='') clear=false;
            if(clear) return true;
        }
    }
    for(let c=0;c<6;c++) {
        if(linkBoard[r1*6+c]===''&&linkBoard[r2*6+c]==='') {
            let clear=true;
            for(let r=Math.min(r1,r2)+1;r<Math.max(r1,r2);r++) if(linkBoard[r*6+c]!=='') clear=false;
            if(clear) return true;
        }
    }
    return false;
}

// ----- 消消乐游戏 -----
let elimBoard = [], elimScore = 0, elimTime = 60, elimTimer = null, elimSelected = null;
const elimColors = ['#e74c3c','#3498db','#2ecc71','#f1c40f','#9b59b6','#1abc9c'];
function startEliminate() {
    document.getElementById('game-title').textContent = '💎 消消乐';
    const board = document.getElementById('game-board');
    board.style.display = 'block';
    board.innerHTML = '<div style="text-align:center;margin-bottom:12px;"><span id="elim-timer" style="font-size:24px;font-weight:bold;color:#F4511E;">60</span>秒 | <span id="elim-score" style="font-size:20px;font-weight:bold;">0</span>分</div><div id="elim-container" style="display:grid;grid-template-columns:repeat(6,1fr);gap:4px;padding:10px;max-width:340px;margin:0 auto;"></div>';
    
    elimScore = 0;
    elimTime = 60;
    elimSelected = null;
    elimBoard = [];
    
    for(let i=0;i<36;i++) elimBoard.push(Math.floor(Math.random()*6));
    renderElim();
    
    document.getElementById('game-score').textContent = '0';
    
    if(elimTimer) clearInterval(elimTimer);
    elimTimer = setInterval(()=>{
        elimTime--;
        document.getElementById('elim-timer').textContent = elimTime;
        if(elimTime<=0) {
            clearInterval(elimTimer);
            endGame();
        }
    },1000);
}

function renderElim() {
    const container = document.getElementById('elim-container');
    if(!container) return;
    container.innerHTML = '';
    elimBoard.forEach((c,i)=>{
        const cell = document.createElement('div');
        cell.style.cssText = `width:50px;height:50px;background:${elimColors[c]};border-radius:8px;cursor:pointer;transition:transform 0.2s;`;
        cell.id = 'elim-'+i;
        cell.onclick = () => clickElim(i);
        container.appendChild(cell);
    });
}

function clickElim(idx) {
    const el = document.getElementById('elim-'+idx);
    if(!el||elimBoard[idx]<0) return;
    
    if(elimSelected===null) {
        elimSelected = idx;
        el.style.transform = 'scale(1.1)';
    } else {
        const [r1,c1] = [Math.floor(elimSelected/6),elimSelected%6];
        const [r2,c2] = [Math.floor(idx/6),idx%6];
        
        if((Math.abs(r1-r2)===1&&c1===c2)||(Math.abs(c1-c2)===1&&r1===r2)) {
            // 交换
            [elimBoard[elimSelected],elimBoard[idx]] = [elimBoard[idx],elimBoard[elimSelected]];
            const matches = findMatches();
            
            if(matches.length>0) {
                SoundEffects.playCorrect();
                processMatches(matches);
            } else {
                // 换回来
                [elimBoard[elimSelected],elimBoard[idx]] = [elimBoard[idx],elimBoard[elimSelected]];
                SoundEffects.playWrong();
            }
        }
        
        document.getElementById('elim-'+elimSelected).style.transform = '';
        elimSelected = null;
        renderElim();
    }
}

function findMatches() {
    const matches = new Set();
    // 横向
    for(let r=0;r<6;r++) {
        for(let c=0;c<4;c++) {
            const v = elimBoard[r*6+c];
            if(v>=0&&v===elimBoard[r*6+c+1]&&v===elimBoard[r*6+c+2]) {
                matches.add(r*6+c);matches.add(r*6+c+1);matches.add(r*6+c+2);
            }
        }
    }
    // 纵向
    for(let c=0;c<6;c++) {
        for(let r=0;r<4;r++) {
            const v = elimBoard[r*6+c];
            if(v>=0&&v===elimBoard[(r+1)*6+c]&&v===elimBoard[(r+2)*6+c]) {
                matches.add(r*6+c);matches.add((r+1)*6+c);matches.add((r+2)*6+c);
            }
        }
    }
    return [...matches];
}

function processMatches(matches) {
    elimScore += matches.length * 10;
    gameScore = elimScore;
    document.getElementById('game-score').textContent = elimScore;
    document.getElementById('elim-score').textContent = elimScore;
    
    matches.forEach(i => elimBoard[i] = -1);
    
    // 下落
    for(let c=0;c<6;c++) {
        let col = [];
        for(let r=5;r>=0;r--) if(elimBoard[r*6+c]>=0) col.push(elimBoard[r*6+c]);
        while(col.length<6) col.push(Math.floor(Math.random()*6));
        for(let r=5;r>=0;r--) elimBoard[r*6+c] = col[5-r];
    }
    
    setTimeout(()=>{
        const more = findMatches();
        if(more.length>0) processMatches(more);
        else renderElim();
    },300);
}

'''

# 找到endGame函数结束的位置，在resetGame之前插入游戏代码
old_endgame_area = '''function resetGame() { startGame(gameType); }'''

if old_endgame_area in content:
    content = content.replace(old_endgame_area, old_endgame_area + entertainment_games_code)
    print("✓ 添加8个娱乐游戏实现代码")
else:
    print("✗ 未找到endGame后的插入位置")

# 保存修改后的文件
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n修改完成！文件大小: {len(content)} 字节")
print(f"新增约 {len(entertainment_games_code)} 字符的娱乐游戏代码")
