const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

console.log('===== V75 添加页面调试面板 =====\n');

// 1. 在head结束前添加调试面板CSS和JS
const debugCode = `
<style>
#debug-panel {
    position: fixed;
    bottom: 80px;
    left: 10px;
    right: 10px;
    max-height: 150px;
    background: rgba(0,0,0,0.9);
    color: #0f0;
    font-size: 11px;
    padding: 10px;
    border-radius: 8px;
    overflow-y: auto;
    z-index: 99999;
    font-family: monospace;
}
#debug-panel .log { margin: 2px 0; }
#debug-panel .error { color: #f00; }
#debug-panel .success { color: #0f0; }
</style>
<script>
function debugLog(msg, type) {
    var panel = document.getElementById('debug-logs');
    if (!panel) return;
    var div = document.createElement('div');
    div.className = 'log ' + (type || '');
    div.textContent = '[' + new Date().toLocaleTimeString() + '] ' + msg;
    panel.appendChild(div);
    panel.scrollTop = panel.scrollHeight;
    console.log(msg);
}
window.onerror = function(msg, url, line) {
    debugLog('JS错误: ' + msg + ' (行' + line + ')', 'error');
    return false;
};
</script>
`;

html = html.replace('</head>', debugCode + '\n</head>');

// 2. 在body开始处添加调试面板HTML
const debugHTML = `
<div id="debug-panel" style="display:block;">
    <div style="color:#ff0;margin-bottom:5px;">[调试面板 V75 - 点击头像测试]</div>
    <div id="debug-logs"></div>
</div>
`;

html = html.replace('<body>', '<body>\n' + debugHTML);

// 3. 替换关键函数，添加调试日志
html = html.replace(
    /function toggleUserMenu\(\)[\s\S]*?\n\}/,
    `function toggleUserMenu() {
    debugLog('>>> toggleUserMenu被调用', 'success');
    var el = document.getElementById('user-dropdown');
    if (!el) {
        debugLog('错误: user-dropdown不存在', 'error');
        return;
    }
    el.classList.toggle('show');
    debugLog('下拉菜单: ' + (el.classList.contains('show') ? '已显示' : '已隐藏'), 'success');
}`
);

html = html.replace(
    /function closeUserMenu\(\)[\s\S]*?\n\}/,
    `function closeUserMenu() {
    debugLog('>>> closeUserMenu被调用');
    var el = document.getElementById('user-dropdown');
    if (el) el.classList.remove('show');
}`
);

html = html.replace(
    /function showUserSwitchModal\(\)[\s\S]*?\n\s*\}/,
    `function showUserSwitchModal() {
    debugLog('>>> showUserSwitchModal被调用', 'success');
    try {
        closeUserMenu();
        var data = loadData();
        debugLog('用户数量: ' + data.users.length);
        
        if (data.users.length === 0) {
            showToast('暂无用户，请先创建账号');
            debugLog('无用户', 'error');
            return;
        }
        
        if (data.users.length === 1) {
            showToast('只有一个用户：' + data.users[0].name);
            debugLog('只有一个用户，无需切换', 'error');
            return;
        }
        
        var container = document.getElementById('switch-user-list');
        if (!container) {
            debugLog('错误: switch-user-list不存在', 'error');
            showToast('页面元素缺失');
            return;
        }
        
        debugLog('找到容器，开始渲染用户列表');
        var colors = ['linear-gradient(135deg,#667eea,#764ba2)', 'linear-gradient(135deg,#FF9A63,#E87A4E)', 'linear-gradient(135deg,#43E97B,#38F9D7)'];
        var htmlContent = '';
        data.users.forEach(function(u, i) {
            htmlContent += '<div class="user-select-item" onclick="switchToUser(\\'' + u.id + '\\')" style="' + (u.id === data.currentUser ? 'background:#f0f7ff;' : '') + '">';
            htmlContent += '<div class="item-avatar" style="background:' + colors[i % 3] + ';color:white;">' + u.name.charAt(0) + '</div>';
            htmlContent += '<div class="item-info">';
            htmlContent += '<div class="item-name">' + u.name + (u.id === data.currentUser ? ' (当前)' : '') + '</div>';
            htmlContent += '<div class="item-grade">' + gradeNames[u.grade] + ' · Lv.' + u.difficulty + '</div>';
            htmlContent += '</div></div>';
        });
        container.innerHTML = htmlContent;
        debugLog('用户列表渲染完成');
        
        var modal = document.getElementById('user-switch-modal');
        modal.style.display = 'flex';
        modal.classList.add('show');
        debugLog('模态框已显示', 'success');
        showToast('请选择用户');
    } catch(err) {
        debugLog('错误: ' + err.message, 'error');
        showToast('错误: ' + err.message);
    }
}`
);

// 4. 添加点击事件日志（使用addEventListener方式）
html = html.replace(
    /<div class="user-avatar-circle" id="header-avatar" onclick="toggleUserMenu\(\)">/,
    '<div class="user-avatar-circle" id="header-avatar" onclick="debugLog(\'点击头像\',\'success\'); toggleUserMenu()">'
);

html = html.replace(
    /<div class="user-dropdown-item" onclick="showUserSwitchModal\(\)">/,
    '<div class="user-dropdown-item" onclick="debugLog(\'点击切换用户\',\'success\'); showUserSwitchModal()">'
);

fs.writeFileSync('index.html', html);
console.log('✓ V75调试版本创建完成');
