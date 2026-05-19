// ============================================================
// 版本: V231 - ES6 Module
// 学生成长日记模块
// ============================================================

const NOTEPAD_STORAGE_KEY = 'notepad_content';
const NOTEPAD_NOTES_KEY = 'student_diary_notes';
const DIARY_STATS_KEY = 'diary_statistics';

// 心情选项
const MOOD_OPTIONS = [
    { emoji: '😊', name: '开心', color: '#FFD93D' },
    { emoji: '😐', name: '一般', color: '#CCCCCC' },
    { emoji: '😢', name: '难过', color: '#6B9BFF' },
    { emoji: '😤', name: '生气', color: '#FF6B6B' },
    { emoji: '🤔', name: '思考', color: '#9B59B6' },
    { emoji: '💪', name: '加油', color: '#4CAF50' }
];

// 日记模板
const DIARY_TEMPLATES = [
    {
        name: '今日学习收获',
        content: '📚 今天我学到了：\n\n1. \n2. \n3. \n\n💡 最大的收获是：'
    },
    {
        name: '每日反思日记',
        content: '🔍 今日反思：\n\n✅ 做得好的地方：\n\n❌ 需要改进的地方：\n\n🎯 明天的目标：'
    },
    {
        name: '成长记录',
        content: '🌱 我的成长记录：\n\n📖 学习了什么新知识：\n\n🏆 取得了什么小成就：\n\n💪 克服了什么困难：\n\n✨ 下一步计划：'
    },
    {
        name: '自由书写',
        content: ''
    }
];

// 分类标签
const CATEGORY_TAGS = ['学习', '生活', '心情', '目标', '其他'];

// 加载笔记列表
function loadNotes() {
    const notes = localStorage.getItem(NOTEPAD_NOTES_KEY);
    return notes ? JSON.parse(notes) : [];
}

// 保存笔记列表
function saveNotes(notes) {
    localStorage.setItem(NOTEPAD_NOTES_KEY, JSON.stringify(notes));
}

// 加载统计数据
function loadStats() {
    const stats = localStorage.getItem(DIARY_STATS_KEY);
    return stats ? JSON.parse(stats) : {
        totalEntries: 0,
        streak: 0,
        lastEntryDate: null,
        totalWords: 0
    };
}

// 保存统计数据
function saveStats(stats) {
    localStorage.setItem(DIARY_STATS_KEY, JSON.stringify(stats));
}

// 更新统计数据
function updateStats(newEntry) {
    const stats = loadStats();
    const today = new Date().toDateString();
    
    stats.totalEntries++;
    stats.totalWords += newEntry.content.length;
    
    // 更新连续打卡
    if (stats.lastEntryDate) {
        const lastDate = new Date(stats.lastEntryDate);
        const daysDiff = Math.floor((new Date(today) - lastDate) / (1000 * 60 * 60 * 24));
        if (daysDiff === 1) {
            stats.streak++;
        } else if (daysDiff > 1) {
            stats.streak = 1;
        }
        // 同一天不更新streak
    } else {
        stats.streak = 1;
    }
    
    stats.lastEntryDate = today;
    saveStats(stats);
    return stats;
}

// 格式化日期
function formatDate(timestamp) {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now - date;
    
    if (diff < 60000) return '刚刚';
    if (diff < 3600000) return Math.floor(diff / 60000) + '分钟前';
    if (diff < 86400000) return Math.floor(diff / 3600000) + '小时前';
    if (diff < 604800000) return Math.floor(diff / 86400000) + '天前';
    
    return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// HTML转义
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

let currentMood = null;
let currentTemplate = null;
let selectedCategory = '';

function renderNotepad(container) {
    const notes = loadNotes();
    const stats = loadStats();
    
    container.innerHTML = `
        <div style="max-width:600px;margin:0 auto;">
            <!-- 统计卡片 -->
            <div class="card" style="background:linear-gradient(135deg,#667eea,#764ba2);color:white;margin-bottom:16px;">
                <div style="text-align:center;">
                    <div style="font-size:36px;font-weight:bold;margin-bottom:4px;">🔥 ${stats.streak}</div>
                    <div style="font-size:14px;opacity:0.9;">连续记录天数</div>
                </div>
                <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:16px;text-align:center;">
                    <div>
                        <div style="font-size:20px;font-weight:bold;">📝 ${stats.totalEntries}</div>
                        <div style="font-size:12px;opacity:0.8;">日记总数</div>
                    </div>
                    <div>
                        <div style="font-size:20px;font-weight:bold;">✍️ ${stats.totalWords}</div>
                        <div style="font-size:12px;opacity:0.8;">总字数</div>
                    </div>
                    <div>
                        <div style="font-size:20px;font-weight:bold;">📅 ${new Date().toLocaleDateString('zh-CN',{month:'short',day:'numeric'})}</div>
                        <div style="font-size:12px;opacity:0.8;">今日</div>
                    </div>
                </div>
            </div>
            
            <!-- 写日记区域 -->
            <div class="card" style="margin-bottom:16px;">
                <h4 style="margin-bottom:12px;">✍️ 写日记</h4>
                
                <!-- 心情选择 -->
                <div style="margin-bottom:12px;">
                    <div style="font-size:13px;color:#666;margin-bottom:8px;">今日心情：</div>
                    <div style="display:flex;gap:8px;flex-wrap:wrap;">
                        ${MOOD_OPTIONS.map(mood => `
                            <button 
                                onclick="selectMood('${mood.emoji}')"
                                class="mood-btn"
                                id="mood-${mood.emoji}"
                                style="padding:8px 12px;border:2px solid ${currentMood === mood.emoji ? '#667eea' : '#e0e0e0'};border-radius:20px;background:${currentMood === mood.emoji ? '#e8f0ff' : 'white'};cursor:pointer;font-size:16px;"
                            >
                                ${mood.emoji} ${mood.name}
                            </button>
                        `).join('')}
                    </div>
                </div>
                
                <!-- 模板选择 -->
                <div style="margin-bottom:12px;">
                    <div style="font-size:13px;color:#666;margin-bottom:8px;">选择模板：</div>
                    <div style="display:flex;gap:8px;flex-wrap:wrap;">
                        ${DIARY_TEMPLATES.map((tpl, idx) => `
                            <button 
                                onclick="selectTemplate(${idx})"
                                class="template-btn"
                                id="tpl-${idx}"
                                style="padding:6px 12px;border:2px solid ${currentTemplate === idx ? '#667eea' : '#e0e0e0'};border-radius:8px;background:${currentTemplate === idx ? '#e8f0ff' : 'white'};cursor:pointer;font-size:12px;"
                            >
                                ${tpl.name}
                            </button>
                        `).join('')}
                    </div>
                </div>
                
                <!-- 分类标签 -->
                <div style="margin-bottom:12px;">
                    <div style="font-size:13px;color:#666;margin-bottom:8px;">分类标签：</div>
                    <div style="display:flex;gap:8px;flex-wrap:wrap;">
                        ${CATEGORY_TAGS.map((tag, idx) => `
                            <button 
                                onclick="selectCategory('${tag}')"
                                class="category-btn"
                                id="cat-${tag}"
                                style="padding:4px 10px;border:1px solid ${selectedCategory === tag ? '#667eea' : '#ddd'};border-radius:15px;background:${selectedCategory === tag ? '#667eea' : '#f5f5f5'};color:${selectedCategory === tag ? 'white' : '#666'};cursor:pointer;font-size:12px;"
                            >
                                #${tag}
                            </button>
                        `).join('')}
                    </div>
                </div>
                
                <input type="text" id="note-title" placeholder="标题（可选）" style="width:100%;padding:12px;margin-bottom:10px;border:1px solid #ddd;border-radius:8px;font-size:14px;box-sizing:border-box;">
                <textarea id="note-content" placeholder="写下今天的心情和收获..." style="width:100%;height:180px;padding:12px;border:1px solid #ddd;border-radius:8px;font-size:14px;resize:vertical;box-sizing:border-box;line-height:1.6;"></textarea>
                
                <div style="display:flex;justify-content:space-between;align-items:center;margin-top:10px;">
                    <span style="font-size:12px;color:#999;">字数：<span id="word-count">0</span></span>
                    <button onclick="saveNote()" style="padding:12px 24px;background:linear-gradient(135deg,#667eea,#764ba2);color:white;border:none;border-radius:8px;font-size:14px;font-weight:bold;cursor:pointer;">💾 保存日记</button>
                </div>
            </div>
            
            <!-- 日记列表 -->
            <div class="card">
                <h4 style="margin-bottom:12px;">📖 我的日记 (${notes.length})</h4>
                <div id="notes-list" style="max-height:400px;overflow-y:auto;">
                    ${notes.length === 0 ? 
                        '<div style="text-align:center;color:#999;padding:40px 20px;"><div style="font-size:48px;margin-bottom:12px;">📝</div><div>还没有日记，开始记录你的第一篇成长日记吧！</div></div>' : 
                        notes.map((note, index) => `
                            <div style="background:#f8f9fa;padding:14px;border-radius:12px;margin-bottom:12px;">
                                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;">
                                    <div style="flex:1;">
                                        <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
                                            ${note.mood ? `<span style="font-size:18px;">${note.mood}</span>` : ''}
                                            ${note.title ? `<span style="font-weight:bold;color:#333;">${escapeHtml(note.title)}</span>` : ''}
                                            ${note.category ? `<span style="font-size:11px;background:#e8f0ff;color:#667eea;padding:2px 8px;border-radius:10px;">#${note.category}</span>` : ''}
                                        </div>
                                        <div style="color:#666;font-size:13px;line-height:1.6;white-space:pre-wrap;word-break:break-word;">${escapeHtml(note.content.substring(0, 150))}${note.content.length > 150 ? '...' : ''}</div>
                                        <div style="display:flex;align-items:center;gap:12px;margin-top:8px;font-size:11px;color:#999;">
                                            <span>⏰ ${formatDate(note.timestamp)}</span>
                                            <span>✍️ ${note.content.length}字</span>
                                        </div>
                                    </div>
                                    <button onclick="deleteNote(${index})" style="margin-left:10px;padding:6px 10px;background:#ff6b6b;color:white;border:none;border-radius:6px;font-size:12px;cursor:pointer;">删除</button>
                                </div>
                            </div>
                        `).join('')
                    }
                </div>
            </div>
            
            <button onclick="closeFullscreenPage()" style="margin-top:16px;width:100%;padding:14px;background:#f5f5f5;color:#666;border:none;border-radius:10px;font-size:14px;cursor:pointer;">← 返回首页</button>
        </div>
    `;
    
    // 绑定字数统计
    const contentEl = document.getElementById('note-content');
    if (contentEl) {
        contentEl.addEventListener('input', function() {
            document.getElementById('word-count').textContent = this.value.length;
        });
    }
}

// 选择心情
function selectMood(mood) {
    if (currentMood === mood) {
        currentMood = null;
    } else {
        currentMood = mood;
    }
    
    // 更新UI
    MOOD_OPTIONS.forEach(m => {
        const btn = document.getElementById(`mood-${m.emoji}`);
        if (btn) {
            btn.style.borderColor = currentMood === m.emoji ? '#667eea' : '#e0e0e0';
            btn.style.background = currentMood === m.emoji ? '#e8f0ff' : 'white';
        }
    });
}

// 选择模板
function selectTemplate(idx) {
    const template = DIARY_TEMPLATES[idx];
    const contentEl = document.getElementById('note-content');
    
    if (currentTemplate === idx) {
        currentTemplate = null;
    } else {
        currentTemplate = idx;
        if (contentEl) {
            contentEl.value = template.content;
            contentEl.focus();
            document.getElementById('word-count').textContent = template.content.length;
        }
    }
    
    // 更新UI
    DIARY_TEMPLATES.forEach((_, i) => {
        const btn = document.getElementById(`tpl-${i}`);
        if (btn) {
            btn.style.borderColor = currentTemplate === i ? '#667eea' : '#e0e0e0';
            btn.style.background = currentTemplate === i ? '#e8f0ff' : 'white';
        }
    });
}

// 选择分类
function selectCategory(category) {
    if (selectedCategory === category) {
        selectedCategory = '';
    } else {
        selectedCategory = category;
    }
    
    // 更新UI
    CATEGORY_TAGS.forEach(tag => {
        const btn = document.getElementById(`cat-${tag}`);
        if (btn) {
            btn.style.borderColor = selectedCategory === tag ? '#667eea' : '#ddd';
            btn.style.background = selectedCategory === tag ? '#667eea' : '#f5f5f5';
            btn.style.color = selectedCategory === tag ? 'white' : '#666';
        }
    });
}

// 保存日记
function saveNote() {
    const titleEl = document.getElementById('note-title');
    const contentEl = document.getElementById('note-content');
    const title = titleEl.value.trim();
    const content = contentEl.value.trim();
    
    if (!content) {
        showToast('请输入日记内容');
        return;
    }
    
    const notes = loadNotes();
    const newNote = {
        title: title,
        content: content,
        mood: currentMood,
        category: selectedCategory,
        timestamp: Date.now()
    };
    
    notes.unshift(newNote);
    saveNotes(notes);
    
    // 更新统计
    updateStats(newNote);
    
    // 重置表单
    titleEl.value = '';
    contentEl.value = '';
    currentMood = null;
    currentTemplate = null;
    selectedCategory = '';
    document.getElementById('word-count').textContent = '0';
    
    showToast('日记已保存 🎉');
    
    // 重新渲染
    renderNotepad(document.getElementById('fullscreen-content'));
}

// 删除日记
function deleteNote(index) {
    if (!confirm('确定要删除这篇日记吗？')) return;
    
    const notes = loadNotes();
    notes.splice(index, 1);
    saveNotes(notes);
    
    showToast('日记已删除');
    renderNotepad(document.getElementById('fullscreen-content'));
}

// 挂载到window
window.renderNotepad = renderNotepad;
window.selectMood = selectMood;
window.selectTemplate = selectTemplate;
window.selectCategory = selectCategory;
window.saveNote = saveNote;
window.deleteNote = deleteNote;

// ES6导出
export {
    renderNotepad,
    loadNotes,
    saveNotes
};

console.log('[V231] 学生成长日记模块加载完成');
