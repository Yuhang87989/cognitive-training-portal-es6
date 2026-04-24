import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 修复登录页面 - 确保底部导航在登录页不显示
# 添加CSS来控制登录页面底部导航隐藏
old_css = '.bottom-nav{display:fixed;bottom:0;left:50%;transform:translateX(-50%);width:480px;max-width:100vw;background:white;border-top:1px solid #f0f0f0;display:flex;padding:8px 0;z-index:50}'
new_css = '.bottom-nav{display:fixed;bottom:0;left:50%;transform:translateX(-50%);width:480px;max-width:100vw;background:white;border-top:1px solid #f0f0f0;display:flex;padding:8px 0;z-index:50}#page-login .bottom-nav,#page-login~.bottom-nav{display:none!important}'
content = content.replace(old_css, new_css)

# 2. 修复登录页面 - 改进用户选择逻辑
# 移除 login-form-section 的隐藏属性，让它默认可见
old_login_form = '<div id="login-form-section" style="display:none;">'
new_login_form = '<div id="login-form-section">'
content = content.replace(old_login_form, new_login_form)

# 3. 添加清除所有数据按钮到登录页面
old_login_btn = '<button class="login-btn login-btn-outline" onclick="showCreateUserModal()" style="margin-top:16px;">➕ 创建新账号</button>'
new_login_btn = '''<button class="login-btn login-btn-outline" onclick="showCreateUserModal()" style="margin-top:12px;">➕ 创建新账号</button>
            <button class="login-btn login-btn-secondary" onclick="confirmClearAllData()" style="margin-top:8px;font-size:12px;">🗑️ 清除所有数据</button>'''
content = content.replace(old_login_btn, new_login_btn)

# 4. 添加 confirmClearAllData 函数
old_clear_func = 'function clearAllData() {'
new_clear_func = '''function confirmClearAllData() {
    if(confirm('确定要清除所有数据吗？这将删除所有用户和学习记录！')) {
        clearAllData();
    }
}
function clearAllData() {'''
content = content.replace(old_clear_func, new_clear_func)

# 5. 修复 quickLogin 函数 - 显示难度选择
old_quick_login = '''function quickLogin(userId) {
    const data = loadData();
    const user = data.users.find(u => u.id === userId);
    if (!user) return;
    data.currentUser = userId;
    saveData(data);
    document.getElementById('selected-user-display').innerHTML = `<span>${user.name.charAt(0)}</span> ${user.name}`;
    document.getElementById('login-form-section').style.display = 'block';
    document.getElementById('login-difficulty').value = user.difficulty;
    document.querySelector('.user-select-btn').dataset.userId = userId;
    document.getElementById('user-select-dropdown').classList.remove('show');
}'''

new_quick_login = '''function quickLogin(userId) {
    const data = loadData();
    const user = data.users.find(u => u.id === userId);
    if (!user) return;
    data.currentUser = userId;
    saveData(data);
    document.getElementById('selected-user-display').innerHTML = `<span>${user.name.charAt(0)}</span> ${user.name}`;
    document.getElementById('login-form-section').style.display = 'block';
    document.getElementById('login-difficulty').value = user.difficulty || 1;
    document.querySelector('.user-select-btn').dataset.userId = userId;
    document.getElementById('user-select-dropdown').classList.remove('show');
}'''

content = content.replace(old_quick_login, new_quick_login)

# 6. 修复 renderUserList 函数 - 确保始终显示难度选择
old_render_user = '''function renderUserList() {
    const data = loadData();
    const container = document.getElementById('user-list-container');
    if (!container) return;
    const colors = ['linear-gradient(135deg,#667eea,#764ba2)', 'linear-gradient(135deg,#FF9A63,#E87A4E)', 'linear-gradient(135deg,#43E97B,#38F9D7)'];
    container.innerHTML = data.users.length === 0 
        ? `<div style="padding:12px;text-align:center;color:var(--text-light);">暂无用户，请创建新账号</div>`
        : data.users.map((u, i) => `
            <div class="user-select-item" onclick="quickLogin('${u.id}')">
                <div class="item-avatar" style="background:${colors[i%3]};color:white;">${u.name.charAt(0)}</div>
                <div class="item-info">
                    <div class="item-name">${u.name}</div>
                    <div class="item-grade">${gradeNames[u.grade]} · Lv.${u.difficulty}</div>
                </div>
            </div>
        `).join('');
}'''

new_render_user = '''function renderUserList() {
    const data = loadData();
    const container = document.getElementById('user-list-container');
    if (!container) return;
    const colors = ['linear-gradient(135deg,#667eea,#764ba2)', 'linear-gradient(135deg,#FF9A63,#E87A4E)', 'linear-gradient(135deg,#43E97B,#38F9D7)'];
    container.innerHTML = data.users.length === 0 
        ? `<div style="padding:12px;text-align:center;color:var(--text-light);">暂无用户，请创建新账号</div>`
        : data.users.map((u, i) => `
            <div class="user-select-item ${u.id === data.currentUser ? 'active' : ''}" onclick="quickLogin('${u.id}')">
                <div class="item-avatar" style="background:${colors[i%3]};color:white;">${u.name.charAt(0)}</div>
                <div class="item-info">
                    <div class="item-name">${u.name} ${u.id === data.currentUser ? '(当前)' : ''}</div>
                    <div class="item-grade">${gradeNames[u.grade] || '初一'} · Lv.${u.difficulty || 1}</div>
                </div>
            </div>
        `).join('');
    // 自动显示难度选择区域
    document.getElementById('login-form-section').style.display = 'block';
}'''

content = content.replace(old_render_user, new_render_user)

# 7. 添加底部导航隐藏逻辑到 showPage 函数
old_show_page = '''function showPage(pageId) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    const target = document.getElementById('page-' + pageId);
    if (target) target.classList.add('active');
}'''

new_show_page = '''function showPage(pageId) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    const target = document.getElementById('page-' + pageId);
    if (target) target.classList.add('active');
    // 登录页面隐藏底部导航
    const bottomNav = document.querySelector('.bottom-nav');
    if (bottomNav) {
        bottomNav.style.display = pageId === 'login' ? 'none' : 'flex';
    }
}'''

content = content.replace(old_show_page, new_show_page)

# 8. 修复 initLoginPage - 确保始终显示难度选择
old_init_login = '''function initLoginPage() {
    const data = loadData();
    renderUserList();
    if (data.users.length > 0) { document.getElementById('login-form-section').style.display = 'none'; }
    else { showCreateUserModal(); }
}'''

new_init_login = '''function initLoginPage() {
    const data = loadData();
    renderUserList();
    if (data.users.length === 0) { showCreateUserModal(); }
}'''

content = content.replace(old_init_login, new_init_login)

# 9. 修复 handleLogin - 确保用户数据正确保存
old_handle_login = '''function handleLogin() {
    const data = loadData();
    const btn = document.querySelector('.user-select-btn');
    const userId = btn.dataset.userId;
    const difficulty = parseInt(document.getElementById('login-difficulty').value);
    if (userId) {
        const user = data.users.find(u => u.id === userId);
        if (user) { user.difficulty = difficulty; user.lastLogin = Date.now(); data.currentUser = userId; saveData(data); }
    }
    updateUI(); syncTodayStats(); showPage('home');
}'''

new_handle_login = '''function handleLogin() {
    const data = loadData();
    const btn = document.querySelector('.user-select-btn');
    const userId = btn.dataset.userId;
    const difficulty = parseInt(document.getElementById('login-difficulty').value);
    if (userId) {
        const user = data.users.find(u => u.id === userId);
        if (user) { 
            user.difficulty = difficulty; 
            user.lastLogin = Date.now(); 
            data.currentUser = userId; 
            saveData(data); 
        }
    } else {
        showToast('请先选择学习者');
        return;
    }
    updateUI(); syncTodayStats(); showPage('home');
}'''

content = content.replace(old_handle_login, new_handle_login)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("修复完成!")
