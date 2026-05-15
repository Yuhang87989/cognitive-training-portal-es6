// ============================================================
// ES6 Module 入口文件 - V229
// 认知训练门户ES6改造第三阶段：真正的动态懒加载
// ============================================================

import './config.js';
import './ctm.js';
import './db.js';
import './storage.js';
import './utils.js';
import './user.js';
import './audio.js';
import './modules/ui.js';

// 数据模块 - 这些是配置数据，需要预先加载
import './data/topics.js';
import './data/week-plans.js';
import './data/podcasts.js';
import './data/videos.js';
import './data/games-config.js';

console.log('[ES6 Module] 核心模块 + 数据模块加载完成！');

// ============================================================
// 模块懒加载映射配置
// ============================================================
window.MODULE_LAZY_LOAD_MAP = {
    // 业务模块 - 点击时动态加载
    'practice':   { path: './modules/practice.js',   render: 'renderPractice' },
    'plan':       { path: './modules/plan.js',       render: 'renderPlan' },
    'games':      { path: './modules/games.js',      render: 'renderGames' },
    'deepseek':   { path: './modules/deepseek.js',   render: 'renderDeepseek' },
    'wrongbook':  { path: './modules/wrongbook.js',  render: 'renderWrongbook' },
    'podcast':    { path: './modules/podcast.js',    render: 'renderPodcast' },
    'video':      { path: './modules/video.js',      render: 'renderVideo' },
    'thinking':   { path: './modules/thinking.js',   render: 'renderThinking' },
    'topics':     { path: './modules/topics.js',     render: 'renderTopics' },
    'method':     { path: './modules/method.js',     render: 'renderMethod' },
    'pomodoro':   { path: './modules/pomodoro.js',   render: 'renderPomodoro' },
    'calculator': { path: './modules/calculator.js', render: 'renderCalculator' },
    'notepad':    { path: './modules/notepad.js',    render: 'renderNotepad' },
    'map':        { path: './modules/map.js',        render: 'renderMap' },
    'selfdrive':  { path: './modules/self-drive.js', render: 'renderSelfDrive' },
    'weekly':     { path: './modules/stats.js',      render: 'renderWeeklyReview' },
    'progress':   { path: './modules/stats.js',      render: 'renderProgressChart' },
    'my':         { path: './modules/my-page.js',    render: 'renderMyPage' },
    'usage-stats':{ path: './modules/my-page.js',    render: 'renderUsageStats' },
    'backup':     { path: './modules/local-db.js',   render: 'renderBackupManager' },
    
    // player.js 由其他模块依赖，不单独懒加载
};

// 已加载的模块缓存
window.LOADED_MODULES = new Set();

// 正在加载中的模块Promise缓存（防止重复加载）
window.LOADING_MODULES = new Map();

// ============================================================
// 懒加载核心函数
// ============================================================

/**
 * 动态加载模块
 * @param {string} moduleKey - 模块键名
 * @returns {Promise} 加载完成的Promise
 */
window.lazyLoadModule = async function(moduleKey) {
    const moduleConfig = MODULE_LAZY_LOAD_MAP[moduleKey];
    
    if (!moduleConfig) {
        console.warn(`[LazyLoad] 未找到模块配置: ${moduleKey}`);
        return null;
    }
    
    // 如果模块已加载，直接返回
    if (LOADED_MODULES.has(moduleConfig.path)) {
        console.log(`[LazyLoad] 模块已缓存: ${moduleKey}`);
        return window[moduleConfig.render];
    }
    
    // 如果模块正在加载中，等待Promise完成
    if (LOADING_MODULES.has(moduleConfig.path)) {
        console.log(`[LazyLoad] 模块正在加载中，等待: ${moduleKey}`);
        return LOADING_MODULES.get(moduleConfig.path);
    }
    
    console.log(`[LazyLoad] 开始动态加载: ${moduleKey}`);
    
    // 创建加载Promise并缓存
    const loadPromise = (async () => {
        try {
            // 动态import加载模块
            await import(moduleConfig.path);
            LOADED_MODULES.add(moduleConfig.path);
            console.log(`[LazyLoad] 模块加载完成: ${moduleKey}`);
            return window[moduleConfig.render];
        } catch (error) {
            console.error(`[LazyLoad] 模块加载失败: ${moduleKey}`, error);
            throw error;
        } finally {
            LOADING_MODULES.delete(moduleConfig.path);
        }
    })();
    
    LOADING_MODULES.set(moduleConfig.path, loadPromise);
    return loadPromise;
};

/**
 * 显示模块加载状态
 * @param {HTMLElement} container - 容器元素
 * @param {string} moduleName - 模块名称
 */
window.showModuleLoading = function(container, moduleName) {
    container.innerHTML = `
        <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:60vh;gap:20px;">
            <div style="width:50px;height:50px;border:4px solid #f3f3f3;border-top:4px solid #667eea;border-radius:50%;animation:spin 1s linear infinite;"></div>
            <div style="color:#666;font-size:16px;">正在加载 ${moduleName}...</div>
            <div style="color:#999;font-size:13px;">首次加载可能需要几秒钟</div>
        </div>
        <style>
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    `;
};

// ============================================================
// 空闲时预加载优化 - requestIdleCallback
// ============================================================

// 常用模块预加载列表（按使用频率排序）
const PRELOAD_PRIORITY = [
    'practice',     // AI精准练 - 最常用
    'games',        // 训练游戏 - 常用
    'deepseek',     // AI对话 - 常用
    'wrongbook',    // 错题本 - 常用
    'podcast',      // 播客课堂
    'video',        // 视频课堂
    'thinking',     // 思维训练
    'topics',       // 母题训练
    'method',       // 学习方法
    'pomodoro',     // 番茄钟
    'map',          // 认知地图
    'my',           // 我的页面
];

let preloadIndex = 0;

/**
 * 空闲时预加载模块
 */
function preloadModulesOnIdle() {
    if (typeof requestIdleCallback === 'undefined') {
        // 不支持requestIdleCallback时，使用setTimeout延迟
        setTimeout(preloadNextModule, 3000);
        return;
    }
    
    requestIdleCallback((deadline) => {
        while (deadline.timeRemaining() > 50 && preloadIndex < PRELOAD_PRIORITY.length) {
            const moduleKey = PRELOAD_PRIORITY[preloadIndex];
            // 静默预加载，不等待结果
            lazyLoadModule(moduleKey).catch(() => {});
            preloadIndex++;
        }
        
        // 如果还有模块需要预加载，继续调度
        if (preloadIndex < PRELOAD_PRIORITY.length) {
            setTimeout(preloadModulesOnIdle, 1000);
        }
    }, { timeout: 2000 });
}

// 页面加载完成3秒后开始预加载
window.addEventListener('load', () => {
    setTimeout(preloadModulesOnIdle, 3000);
    console.log('[LazyLoad] 3秒后将在空闲时预加载常用模块');
});

// 标记ES6模块已加载
window.ES6_MODULES_LOADED = true;

// 触发核心模块加载完成事件
if (window.dispatchEvent) {
    window.dispatchEvent(new CustomEvent('es6ModulesLoaded'));
}

console.log('[ES6 Module V229] 动态懒加载系统初始化完成！');
