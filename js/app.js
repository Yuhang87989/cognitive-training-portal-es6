// 应用入口 - 初始化所有模块
console.log('认知训练门户 V2.1 启动');

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        // 初始化播客
        if (typeof renderPodcastList === 'function') {
            renderPodcastList();
        }
        // 初始化母题
        if (typeof renderTopics === 'function') {
            renderTopics();
        }
        // 检查登录状态
        checkLoginStatus();
    }, 300);
});

function checkLoginStatus() {
    const data = localStorage.getItem('cognitive_training_v33');
    if (!data) {
        // 显示登录
        const overlay = document.getElementById('home-login-overlay');
        if (overlay) overlay.style.display = 'flex';
    } else {
        // 已登录，更新UI
        try {
            const parsed = JSON.parse(data);
            if (parsed.currentUser && updateUI) {
                updateUI();
            }
        } catch(e) {}
    }
}
