// UI核心模块

function showPage(pageId) {
    // 隐藏所有页面
    document.querySelectorAll('.page').forEach(p => {
        p.classList.remove('active');
        p.style.display = 'none';
    });
    
    // 显示目标页面
    const page = document.getElementById('page-' + pageId);
    if (page) {
        page.classList.add('active');
        page.style.display = 'block';
    }
    
    // 更新导航
    document.querySelectorAll('.nav-item').forEach((n, i) => {
        const map = {home:0, avatar:1, games:2, map:3, plan:4};
        n.classList.toggle('active', map[pageId] === i);
    });
}

function updateUI() {
    const user = getCurrentUserData();
    if (!user) return;
    
    document.getElementById('greeting-name').textContent = user.name;
}

function delayedInit() {
    const homePage = document.getElementById('page-home');
    const loginOverlay = document.getElementById('home-login-overlay');
    
    if (homePage) {
        homePage.style.display = 'block';
        homePage.classList.add('active');
    }
    
    const data = loadData();
    if (!data.currentUser || !data.users.length) {
        if (loginOverlay) loginOverlay.style.display = 'flex';
    } else {
        if (loginOverlay) loginOverlay.style.display = 'none';
        updateUI();
    }
}

function handleHomeLogin() {
    const name = document.getElementById('home-name').value.trim();
    const grade = document.getElementById('home-grade').value;
    const difficulty = document.getElementById('home-difficulty').value;
    
    if (!name) { alert('请输入名字'); return; }
    
    const data = loadData();
    const userId = 'user_' + Date.now();
    data.users.push({ id: userId, name, grade, difficulty, score: 0 });
    data.currentUser = userId;
    saveData(data);
    
    document.getElementById('home-login-overlay').style.display = 'none';
    updateUI();
}

document.addEventListener('DOMContentLoaded', () => setTimeout(delayedInit, 100));
