// 游戏模块

let currentGame = null;
let gameScore = 0;

function startGame(gameType) {
    currentGame = gameType;
    gameScore = 0;
    
    const modal = document.getElementById('game-modal');
    if (modal) modal.classList.add('show');
    
    // 根据游戏类型初始化
    if (gameType === 'reaction') initReactionGame();
    else if (gameType === 'memory') initMemoryGame();
    else if (gameType === 'attention') initAttentionGame();
}

function closeGameModal() {
    const modal = document.getElementById('game-modal');
    if (modal) modal.classList.remove('show');
    currentGame = null;
}

function initReactionGame() {
    const area = document.getElementById('game-area');
    area.innerHTML = '<div style="text-align:center;padding:40px;"><p>点击出现的圆圈！</p></div>';
}

function initMemoryGame() {
    const area = document.getElementById('game-area');
    area.innerHTML = '<div style="text-align:center;padding:40px;"><p>记忆卡片位置！</p></div>';
}

function initAttentionGame() {
    const area = document.getElementById('game-area');
    area.innerHTML = '<div style="text-align:center;padding:40px;"><p>找出不同的图案！</p></div>';
}
