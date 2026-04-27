#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为2048游戏添加触屏和键盘控制"""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 修复start2048函数 - 添加触屏和键盘控制
old_start2048 = '''    document.getElementById('game-score').textContent = '0';
}

function add2048Tile() {'''

new_start2048 = '''    document.getElementById('game-score').textContent = '0';
    
    // 触屏滑动控制
    let touchStartX = 0, touchStartY = 0;
    board.addEventListener('touchstart',e=>{
        touchStartX = e.touches[0].clientX;
        touchStartY = e.touches[0].clientY;
    });
    board.addEventListener('touchend',e=>{
        const dx = e.changedTouches[0].clientX - touchStartX;
        const dy = e.changedTouches[0].clientY - touchStartY;
        if(Math.abs(dx)>30||Math.abs(dy)>30) {
            if(Math.abs(dx)>Math.abs(dy)) {
                move2048(dx>0?2:4); // 右:2, 左:4
            } else {
                move2048(dy>0?1:3); // 下:1, 上:3
            }
        }
    });
    
    // 键盘控制
    document.addEventListener('keydown',e=>{
        if(e.key==='ArrowUp') move2048(3);
        else if(e.key==='ArrowDown') move2048(1);
        else if(e.key==='ArrowLeft') move2048(4);
        else if(e.key==='ArrowRight') move2048(2);
    });
}

function add2048Tile() {'''

if old_start2048 in content:
    content = content.replace(old_start2048, new_start2048)
    print("✓ 添加2048触屏和键盘控制")
else:
    print("✗ 未找到start2048的插入位置")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("完成")
