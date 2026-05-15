// ============================================================
// ES6 Module 入口文件 - V225
// 认知训练门户ES6改造第一阶段：核心模块改造
// ============================================================

import './config.js';
import './ctm.js';
import './db.js';
import './storage.js';
import './utils.js';
import './user.js';
import './modules/ui.js';

console.log('[ES6 Module] 核心模块加载完成！');

// 标记ES6模块已加载
window.ES6_MODULES_LOADED = true;

// 触发核心模块加载完成事件
if (window.dispatchEvent) {
    window.dispatchEvent(new CustomEvent('es6ModulesLoaded'));
}
