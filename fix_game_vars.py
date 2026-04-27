#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复游戏代码中的变量名问题"""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 修复贪吃蛇中的速度变量名
content = content.replace('setInterval(update,速度)', 'setInterval(update,speed)')
content = content.replace('snakeGame = setInterval(update,速度)', 'snakeGame = setInterval(update,speed)')
content = content.replace('tetrisGame = setInterval(tick,速度)', 'tetrisGame = setInterval(tick,speed)')

# 修复地鼠游戏中 showMole 函数里的速度变量
content = content.replace('setTimeout(()=>{\n                        if(whackMoles[idx]===1) {\n                            whackMoles[idx] = 0;\n                            el.style.bottom = \'-50px\';\n                        }\n                    },速度);', '''setTimeout(()=>{
                        if(whackMoles[idx]===1) {
                            whackMoles[idx] = 0;
                            el.style.bottom = '-50px';
                        }
                    },moleSpeed);''')

# 更通用的替换
content = content.replace(',速度);', ',moleSpeed);')
content = content.replace('},速度);', '},moleSpeed);')

# 检查并添加 moleSpeed 变量
old_showMole = 'const speed = Math.max(300,800-gameLevel*50);'
if 'const speed = Math.max(300,800-gameLevel*50);' in content:
    content = content.replace('const speed = Math.max(300,800-gameLevel*50);', 'const moleSpeed = Math.max(300,800-gameLevel*50);')
    print("✓ 修复 moleSpeed 变量")

# 修复俄罗斯方块的tick函数中的lockPiece调用
old_tick = '''function tick() {
        if(gameOver) return;
        if(!canMove(current.shape,x,y+1)) {
            lockPiece();
        } else {
            y++;
        }
        drawBoard();
        drawCurrent();
    }'''
    
new_tick = '''function tick() {
        if(gameOver) return;
        if(!canMove(current.shape,x,y+1)) {
            lockPiece();
        } else {
            y++;
        }
        drawBoard();
        drawCurrent();
    }'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ 变量名修复完成")
