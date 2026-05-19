// 版本: V231 - ES6 Module
// 模拟考试模块 - 独立功能模块（增强版）

const examModule = {
    name: 'exam',
    icon: '📝',
    render: renderExam
};

// 注册到CTM模块系统
if (typeof CTM !== 'undefined' && CTM.registerModule) {
    CTM.registerModule('exam', examModule);
}

// 全局状态
let currentExam = {
    subject: 'math',
    grade: 7,
    difficulty: 'medium',
    questions: [],
    answers: {},
    startTime: null,
    timeLimit: 30 * 60, // 30分钟
    timer: null,
    mode: 'auto', // auto=系统出题, manual=上传试卷
    uploadedPaper: null // 上传的试卷图片
};

let examHistory = [];

// 考试配置
const examConfig = {
    subjects: {
        math: { name: '数学', icon: '📐' },
        chinese: { name: '语文', icon: '📖' },
        english: { name: '英语', icon: '🔤' },
        physics: { name: '物理', icon: '⚡' },
        chemistry: { name: '化学', icon: '🧪' }
    },
    grades: [5, 6, 7, 8, 9],
    difficulties: {
        easy: { name: '简单', questionCount: 10, time: 15 },
        medium: { name: '中等', questionCount: 15, time: 30 },
        hard: { name: '困难', questionCount: 20, time: 45 }
    }
};

// 仿真笔迹样式
const handwritingStyles = `
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&family=ZCOOL+KuaiLe&display=swap');
        
        .handwriting-mode {
            font-family: 'ZCOOL KuaiLe', cursive;
        }
        
        .handwriting-mode .card {
            background: linear-gradient(to bottom, #fffdf5 0%, #fff9e6 100%);
            border: 1px solid #e8dcc8;
            box-shadow: 2px 2px 8px rgba(139, 119, 101, 0.15);
        }
        
        .handwriting-mode .question-card {
            background: white;
            border: 1px solid #d4c4a8;
            position: relative;
        }
        
        .handwriting-mode .question-card::before {
            content: '';
            position: absolute;
            left: 60px;
            top: 0;
            bottom: 0;
            width: 2px;
            background: #ffcccc;
        }
        
        .handwriting-mode .option-btn {
            font-family: 'Ma Shan Zheng', cursive;
            font-size: 18px;
            border: 2px dashed #c4b59d;
            transition: all 0.3s;
        }
        
        .handwriting-mode .option-btn:hover {
            border-style: solid;
            transform: scale(1.02);
        }
        
        .handwriting-mode .option-btn.selected {
            background: #fff3e0;
            border-color: #ff9800;
            border-style: solid;
        }
        
        .handwriting-mode .question-number {
            font-family: 'Ma Shan Zheng', cursive;
            font-size: 28px;
            color: #8b7355;
        }
        
        .handwriting-mode .question-text {
            font-family: 'ZCOOL KuaiLe', cursive;
            font-size: 17px;
            line-height: 1.8;
            color: #2d1f1a;
        }
        
        .paper-upload-area {
            border: 3px dashed #ccc;
            border-radius: 16px;
            padding: 40px 20px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
            background: #fafafa;
        }
        
        .paper-upload-area:hover {
            border-color: #667eea;
            background: #f0f4ff;
        }
        
        .paper-preview {
            max-width: 100%;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        .answer-sheet-area {
            background: #fffdf5;
            border: 2px solid #e8dcc8;
            border-radius: 12px;
            padding: 20px;
            margin-top: 16px;
        }
        
        .answer-grid {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 10px;
        }
        
        .answer-cell {
            width: 50px;
            height: 50px;
            border: 2px solid #d4c4a8;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Ma Shan Zheng', cursive;
            font-size: 24px;
            cursor: pointer;
            transition: all 0.2s;
            background: white;
        }
        
        .answer-cell:hover {
            background: #fff3e0;
            border-color: #ff9800;
        }
        
        .answer-cell.filled {
            background: #e8f5e9;
            border-color: #4caf50;
            color: #2e7d32;
        }
        
        .mode-toggle {
            display: flex;
            background: #f5f5f5;
            border-radius: 12px;
            padding: 4px;
            margin-bottom: 20px;
        }
        
        .mode-toggle-btn {
            flex: 1;
            padding: 10px;
            border: none;
            border-radius: 10px;
            background: transparent;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.3s;
        }
        
        .mode-toggle-btn.active {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
        }
    </style>
`;

// 渲染主界面
function renderExam(container) {
    container.innerHTML = handwritingStyles + `
        <div class="card">
            <h3 style="margin-bottom:16px;">📝 模拟考试</h3>
            <p style="color:#666;font-size:13px;margin-bottom:20px;">全真模拟，实战演练，检验学习成果</p>
            
            <!-- 考试模式切换 -->
            <div class="mode-toggle">
                <button class="mode-toggle-btn ${currentExam.mode === 'auto' ? 'active' : ''}" onclick="setExamMode('auto')">
                    🤖 系统出题
                </button>
                <button class="mode-toggle-btn ${currentExam.mode === 'manual' ? 'active' : ''}" onclick="setExamMode('manual')">
                    📄 上传试卷
                </button>
            </div>
            
            <div id="auto-mode-config" style="${currentExam.mode === 'manual' ? 'display:none' : ''}">
                <div style="margin-bottom:20px;">
                    <label style="display:block;margin-bottom:8px;font-weight:600;">选择科目</label>
                    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;">
                        ${Object.entries(examConfig.subjects).map(([key, val]) => `
                            <button 
                                onclick="selectExamSubject('${key}', this)"
                                class="subject-btn ${key === currentExam.subject ? 'active' : ''}"
                                style="padding:12px;border:2px solid ${key === currentExam.subject ? '#3377FF' : '#e0e0e0'};border-radius:10px;background:${key === currentExam.subject ? '#e8f0ff' : 'white'};cursor:pointer;font-weight:600;"
                            >
                                ${val.icon} ${val.name}
                            </button>
                        `).join('')}
                    </div>
                </div>
                
                <div style="margin-bottom:20px;">
                    <label style="display:block;margin-bottom:8px;font-weight:600;">选择年级</label>
                    <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:8px;">
                        ${examConfig.grades.map(grade => `
                            <button 
                                onclick="selectExamGrade(${grade}, this)"
                                class="grade-btn ${grade === currentExam.grade ? 'active' : ''}"
                                style="padding:10px;border:2px solid ${grade === currentExam.grade ? '#3377FF' : '#e0e0e0'};border-radius:10px;background:${grade === currentExam.grade ? '#e8f0ff' : 'white'};cursor:pointer;font-weight:600;"
                            >
                                ${grade}年级
                            </button>
                        `).join('')}
                    </div>
                </div>
                
                <div style="margin-bottom:20px;">
                    <label style="display:block;margin-bottom:8px;font-weight:600;">选择难度</label>
                    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;">
                        ${Object.entries(examConfig.difficulties).map(([key, val]) => `
                            <button 
                                onclick="selectExamDifficulty('${key}', this)"
                                class="diff-btn ${key === currentExam.difficulty ? 'active' : ''}"
                                style="padding:12px;border:2px solid ${key === currentExam.difficulty ? '#3377FF' : '#e0e0e0'};border-radius:10px;background:${key === currentExam.difficulty ? '#e8f0ff' : 'white'};cursor:pointer;font-weight:600;"
                            >
                                ${val.name}<br>
                                <span style="font-size:11px;color:#666;">${val.questionCount}题 / ${val.time}分钟</span>
                            </button>
                        `).join('')}
                    </div>
                </div>
                
                <!-- 仿真笔迹开关 -->
                <div style="margin-bottom:20px;padding:12px;background:#f5f7ff;border-radius:10px;display:flex;align-items:center;justify-content:space-between;">
                    <div>
                        <div style="font-weight:600;">✍️ 仿真笔迹模式</div>
                        <div style="font-size:12px;color:#666;">使用手写字体，模拟真实考试答题体验</div>
                    </div>
                    <label style="position:relative;display:inline-block;width:50px;height:26px;">
                        <input type="checkbox" id="handwriting-toggle" style="opacity:0;width:0;height:0;" onchange="toggleHandwriting()">
                        <span style="position:absolute;cursor:pointer;top:0;left:0;right:0;bottom:0;background-color:#ccc;border-radius:26px;transition:.4s;">
                            <span style="position:absolute;content:'';height:20px;width:20px;left:3px;bottom:3px;background-color:white;border-radius:50%;transition:.4s;"></span>
                        </span>
                    </label>
                </div>
            </div>
            
            <div id="manual-mode-config" style="${currentExam.mode === 'auto' ? 'display:none' : ''}">
                <div style="margin-bottom:20px;">
                    <label style="display:block;margin-bottom:8px;font-weight:600;">📄 上传试卷</label>
                    <div class="paper-upload-area" onclick="document.getElementById('paper-upload').click()" id="paper-upload-area">
                        <div style="font-size:48px;margin-bottom:12px;">📷</div>
                        <div style="font-weight:600;margin-bottom:8px;">点击上传试卷照片</div>
                        <div style="font-size:13px;color:#666;">支持拍照或从相册选择</div>
                    </div>
                    <input type="file" id="paper-upload" accept="image/*" style="display:none;" onchange="handlePaperUpload(this)">
                    
                    <div id="paper-preview-container" style="display:none;margin-top:16px;">
                        <img id="paper-preview" class="paper-preview" />
                        <div style="display:flex;gap:10px;margin-top:12px;">
                            <button onclick="clearUploadedPaper()" style="flex:1;padding:10px;background:#f5f5f5;color:#666;border:none;border-radius:8px;cursor:pointer;">重新上传</button>
                        </div>
                    </div>
                </div>
                
                <div style="margin-bottom:20px;">
                    <label style="display:block;margin-bottom:8px;font-weight:600;">⏱️ 考试时长</label>
                    <select id="manual-time-select" style="width:100%;padding:12px;border:1px solid #ddd;border-radius:8px;font-size:14px;">
                        <option value="30">30分钟</option>
                        <option value="45">45分钟</option>
                        <option value="60">60分钟</option>
                        <option value="90">90分钟</option>
                        <option value="120">120分钟</option>
                    </select>
                </div>
                
                <div style="margin-bottom:20px;">
                    <label style="display:block;margin-bottom:8px;font-weight:600;">📝 题目数量</label>
                    <select id="manual-question-count" style="width:100%;padding:12px;border:1px solid #ddd;border-radius:8px;font-size:14px;">
                        <option value="10">10题</option>
                        <option value="15">15题</option>
                        <option value="20">20题</option>
                        <option value="25">25题</option>
                        <option value="30">30题</option>
                        <option value="50">50题</option>
                    </select>
                </div>
            </div>
            
            <button 
                onclick="startNewExam()"
                style="width:100%;padding:16px;background:linear-gradient(135deg,#FF6B6B,#FF9A63);color:white;border:none;border-radius:12px;font-size:16px;font-weight:600;cursor:pointer;margin-bottom:16px;"
            >
                🚀 开始考试
            </button>
            
            <div class="card" style="background:#f5f7ff;">
                <h4 style="margin-bottom:12px;">📊 历史记录</h4>
                <div id="exam-history-list">
                    ${renderExamHistory()}
                </div>
            </div>
        </div>
    `;
    
    // 从本地存储加载历史记录
    loadExamHistory();
}

// 切换考试模式
function setExamMode(mode) {
    currentExam.mode = mode;
    
    document.querySelectorAll('.mode-toggle-btn').forEach((btn, idx) => {
        btn.classList.toggle('active', (idx === 0 && mode === 'auto') || (idx === 1 && mode === 'manual'));
    });
    
    document.getElementById('auto-mode-config').style.display = mode === 'auto' ? 'block' : 'none';
    document.getElementById('manual-mode-config').style.display = mode === 'manual' ? 'block' : 'none';
}

// 处理试卷上传
function handlePaperUpload(input) {
    if (!input.files || !input.files[0]) return;
    
    const file = input.files[0];
    const reader = new FileReader();
    
    reader.onload = function(e) {
        currentExam.uploadedPaper = e.target.result;
        
        const preview = document.getElementById('paper-preview');
        const container = document.getElementById('paper-preview-container');
        const uploadArea = document.getElementById('paper-upload-area');
        
        preview.src = e.target.result;
        container.style.display = 'block';
        uploadArea.style.display = 'none';
        
        showToast('试卷上传成功！');
    };
    
    reader.readAsDataURL(file);
}

// 清除上传的试卷
function clearUploadedPaper() {
    currentExam.uploadedPaper = null;
    document.getElementById('paper-preview-container').style.display = 'none';
    document.getElementById('paper-upload-area').style.display = 'block';
    document.getElementById('paper-upload').value = '';
}

// 仿真笔迹开关
let handwritingEnabled = false;
function toggleHandwriting() {
    handwritingEnabled = document.getElementById('handwriting-toggle').checked;
    showToast(handwritingEnabled ? '已开启仿真笔迹模式 ✍️' : '已关闭仿真笔迹模式');
}

// 选择科目
function selectExamSubject(subject, btn) {
    currentExam.subject = subject;
    document.querySelectorAll('.subject-btn').forEach(b => {
        b.style.borderColor = '#e0e0e0';
        b.style.background = 'white';
    });
    btn.style.borderColor = '#3377FF';
    btn.style.background = '#e8f0ff';
}

// 选择年级
function selectExamGrade(grade, btn) {
    currentExam.grade = grade;
    document.querySelectorAll('.grade-btn').forEach(b => {
        b.style.borderColor = '#e0e0e0';
        b.style.background = 'white';
    });
    btn.style.borderColor = '#3377FF';
    btn.style.background = '#e8f0ff';
}

// 选择难度
function selectExamDifficulty(difficulty, btn) {
    currentExam.difficulty = difficulty;
    document.querySelectorAll('.diff-btn').forEach(b => {
        b.style.borderColor = '#e0e0e0';
        b.style.background = 'white';
    });
    btn.style.borderColor = '#3377FF';
    btn.style.background = '#e8f0ff';
}

// 开始新考试
function startNewExam() {
    if (currentExam.mode === 'manual') {
        // 上传试卷模式
        const timeSelect = document.getElementById('manual-time-select');
        const countSelect = document.getElementById('manual-question-count');
        const time = parseInt(timeSelect.value);
        const count = parseInt(countSelect.value);
        
        if (!currentExam.uploadedPaper) {
            showToast('请先上传试卷照片！');
            return;
        }
        
        // 生成答题卡题目（只有编号，没有题目内容）
        currentExam.questions = [];
        for (let i = 1; i <= count; i++) {
            currentExam.questions.push({
                id: i,
                question: `第 ${i} 题`,
                answer: 'A',
                explanation: '请自行对照答案',
                type: 'manual',
                options: ['A', 'B', 'C', 'D']
            });
        }
        currentExam.answers = {};
        currentExam.timeLimit = time * 60;
        currentExam.startTime = Date.now();
        
        // 渲染手动答题界面
        renderManualExamInterface(time, count);
        
    } else {
        // 系统出题模式
        const config = examConfig.difficulties[currentExam.difficulty];
        const subjectInfo = examConfig.subjects[currentExam.subject];
        
        // 生成题目
        currentExam.questions = generateExamQuestions(currentExam.subject, currentExam.grade, config.questionCount);
        currentExam.answers = {};
        currentExam.timeLimit = config.time * 60;
        currentExam.startTime = Date.now();
        
        // 渲染考试界面
        renderExamInterface(subjectInfo, config);
    }
    
    // 开始计时
    startExamTimer();
}

// 渲染手动答题界面（上传试卷）
function renderManualExamInterface(time, count) {
    const container = document.getElementById('fullscreen-content');
    if (!container) return;
    
    container.innerHTML = handwritingStyles + `
        <div class="${handwritingEnabled ? 'handwriting-mode' : ''}" style="padding:16px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
                <div>
                    <span style="font-size:20px;font-weight:600;">📄 自定义试卷</span>
                    <span style="margin-left:10px;font-size:13px;color:#666;">${count}题 / ${time}分钟</span>
                </div>
                <div id="exam-timer" style="font-size:24px;font-weight:bold;color:#FF6B6B;">
                    ${Math.floor(time/60).toString().padStart(2,'0')}:${(time%60).toString().padStart(2,'0')}
                </div>
            </div>
            
            <!-- 试卷图片 -->
            <div style="margin-bottom:16px;background:#f5f5f5;border-radius:12px;overflow:hidden;">
                <img src="${currentExam.uploadedPaper}" style="width:100%;display:block;" />
            </div>
            
            <!-- 答题卡 -->
            <div class="answer-sheet-area">
                <div style="text-align:center;margin-bottom:16px;font-weight:600;font-size:18px;">
                    ✍️ 答题卡
                </div>
                <div class="answer-grid" id="answer-grid">
                    ${currentExam.questions.map((q, idx) => `
                        <div 
                            class="answer-cell"
                            id="answer-cell-${idx}"
                            onclick="selectManualAnswer(${idx})"
                        >
                            ${idx + 1}
                        </div>
                    `).join('')}
                </div>
            </div>
            
            <!-- 选项选择器 -->
            <div id="option-selector" style="display:none;position:fixed;bottom:0;left:0;right:0;background:white;padding:20px;box-shadow:0 -4px 20px rgba(0,0,0,0.15);border-radius:20px 20px 0 0;z-index:1000;">
                <div style="text-align:center;margin-bottom:12px;font-weight:600;">选择答案</div>
                <div style="display:flex;gap:12px;justify-content:center;">
                    ${['A', 'B', 'C', 'D'].map(opt => `
                        <button 
                            onclick="setManualAnswer('${opt}')"
                            style="width:60px;height:60px;border:2px solid #ddd;border-radius:12px;font-size:24px;font-weight:bold;background:white;cursor:pointer;"
                        >
                            ${opt}
                        </button>
                    `).join('')}
                </div>
                <button onclick="closeOptionSelector()" style="margin-top:12px;width:100%;padding:12px;background:#f5f5f5;color:#666;border:none;border-radius:8px;cursor:pointer;">取消</button>
            </div>
            
            <div style="position:sticky;bottom:0;left:0;right:0;background:white;padding:16px 0;border-top:1px solid #eee;margin-top:16px;">
                <div style="display:flex;gap:12px;">
                    <button 
                        onclick="submitExam()"
                        style="flex:1;padding:14px;background:linear-gradient(135deg,#FF6B6B,#FF9A63);color:white;border:none;border-radius:12px;font-size:15px;font-weight:600;cursor:pointer;"
                    >
                        ✅ 交卷
                    </button>
                </div>
                <div style="text-align:center;margin-top:8px;font-size:12px;color:#999;">
                    已答：<span id="answered-count">0</span> / ${currentExam.questions.length}
                </div>
            </div>
        </div>
    `;
}

let currentSelectingQuestion = -1;

function selectManualAnswer(idx) {
    currentSelectingQuestion = idx;
    document.getElementById('option-selector').style.display = 'block';
}

function setManualAnswer(option) {
    if (currentSelectingQuestion < 0) return;
    
    currentExam.answers[currentSelectingQuestion] = option;
    const cell = document.getElementById(`answer-cell-${currentSelectingQuestion}`);
    if (cell) {
        cell.textContent = option;
        cell.classList.add('filled');
    }
    
    closeOptionSelector();
    updateAnsweredCount();
}

function closeOptionSelector() {
    currentSelectingQuestion = -1;
    document.getElementById('option-selector').style.display = 'none';
}

// 生成考试题目
function generateExamQuestions(subject, grade, count) {
    // 使用母题库中的题目
    const topicKey = subject + grade;
    let questionPool = [];
    
    if (typeof topics !== 'undefined' && topics[topicKey]) {
        questionPool = [...topics[topicKey]];
    }
    
    // 如果题目不够，生成备用题目
    if (questionPool.length < count) {
        const backupQuestions = generateBackupQuestions(subject, grade, count - questionPool.length);
        questionPool = questionPool.concat(backupQuestions);
    }
    
    // 随机打乱并选取指定数量
    return shuffleArray(questionPool).slice(0, count).map((q, index) => ({
        id: index + 1,
        question: q.q,
        answer: q.a,
        explanation: q.e || '暂无解析',
        type: q.type || 'text',
        options: q.options || generateOptions(q.a, subject)
    }));
}

// 生成备用题目
function generateBackupQuestions(subject, grade, count) {
    const questions = [];
    const templates = {
        math: [
            { q: '计算：${a} + ${b} = ?', a: '${a+b}', e: '加法运算' },
            { q: '计算：${a} × ${b} = ?', a: '${a*b}', e: '乘法运算' },
            { q: '解方程：x + ${a} = ${b}', a: '${b-a}', e: '一元一次方程' },
            { q: '${a}的${b}%是多少？', a: '${a*b/100}', e: '百分比计算' }
        ],
        chinese: [
            { q: '"${word}"的拼音是？', a: 'pinyin', e: '拼音练习' },
            { q: '补充成语：${part1}____', a: '${part2}', e: '成语积累' },
            { q: '"${sentence}"使用了什么修辞手法？', a: '比喻', e: '修辞手法' }
        ],
        english: [
            { q: '"${word}"的中文意思是？', a: 'meaning', e: '词汇练习' },
            { q: '翻译：${english}', a: '${chinese}', e: '翻译练习' }
        ],
        physics: [
            { q: '速度公式是？', a: 'v=s/t', e: '基本公式' },
            { q: '密度公式是？', a: 'ρ=m/V', e: '基本公式' }
        ],
        chemistry: [
            { q: '水的化学式是？', a: 'H₂O', e: '化学式' },
            { q: '氧气的化学式是？', a: 'O₂', e: '化学式' }
        ]
    };
    
    const subjectTemplates = templates[subject] || templates.math;
    
    for (let i = 0; i < count; i++) {
        const template = subjectTemplates[i % subjectTemplates.length];
        const a = Math.floor(Math.random() * 50) + 10;
        const b = Math.floor(Math.random() * 20) + 5;
        
        questions.push({
            q: template.q.replace(/\$\{a\}/g, a).replace(/\$\{b\}/g, b),
            a: String(eval(template.a.replace(/\$\{a\}/g, a).replace(/\$\{b\}/g, b))),
            e: template.e
        });
    }
    
    return questions;
}

// 生成选项
function generateOptions(correctAnswer, subject) {
    const distractors = [];
    const num = parseFloat(correctAnswer);
    
    if (!isNaN(num)) {
        // 数字干扰项
        distractors.push(String(num + 1));
        distractors.push(String(num - 1));
        distractors.push(String(num * 2));
    } else {
        // 文字干扰项
        distractors.push('其他选项');
        distractors.push('不正确答案');
        distractors.push('以上都不对');
    }
    
    const options = [correctAnswer, ...distractors.slice(0, 3)];
    return shuffleArray(options);
}

// 打乱数组
function shuffleArray(array) {
    const newArray = [...array];
    for (let i = newArray.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [newArray[i], newArray[j]] = [newArray[j], newArray[i]];
    }
    return newArray;
}

// 渲染考试界面
function renderExamInterface(subjectInfo, config) {
    const container = document.getElementById('fullscreen-content');
    if (!container) return;
    
    container.innerHTML = handwritingStyles + `
        <div class="${handwritingEnabled ? 'handwriting-mode' : ''}" style="padding:16px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
                <div>
                    <span style="font-size:20px;font-weight:600;">${subjectInfo.icon} ${subjectInfo.name}模拟考试</span>
                    <span style="margin-left:10px;font-size:13px;color:#666;">${config.questionCount}题</span>
                </div>
                <div id="exam-timer" style="font-size:24px;font-weight:bold;color:#FF6B6B;">
                    30:00
                </div>
            </div>
            
            <div id="exam-questions-container" style="max-height:calc(100vh - 250px);overflow-y:auto;padding-right:8px;">
                ${currentExam.questions.map((q, index) => `
                    <div class="card question-card" id="question-${index}" style="margin-bottom:16px;">
                        <div style="display:flex;gap:12px;">
                            <div class="question-number" style="background:#3377FF;color:white;width:40px;height:40px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:600;flex-shrink:0;">
                                ${index + 1}
                            </div>
                            <div style="flex:1;">
                                <div class="question-text" style="font-weight:600;margin-bottom:12px;line-height:1.6;">${q.question}</div>
                                <div style="display:flex;flex-direction:column;gap:8px;">
                                    ${q.options.map((opt, optIdx) => `
                                        <button 
                                            onclick="selectAnswer(${index}, ${optIdx})"
                                            class="option-btn"
                                            id="option-${index}-${optIdx}"
                                            style="padding:12px 16px;background:#f8f9fa;border:2px solid #e0e0e0;border-radius:10px;cursor:pointer;text-align:left;transition:all 0.2s;font-size:14px;"
                                        >
                                            <span style="font-weight:600;margin-right:8px;">${String.fromCharCode(65 + optIdx)}.</span>
                                            ${opt}
                                        </button>
                                    `).join('')}
                                </div>
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
            
            <div style="position:sticky;bottom:0;left:0;right:0;background:white;padding:16px 0;border-top:1px solid #eee;">
                <div style="display:flex;gap:12px;">
                    <button 
                        onclick="submitExam()"
                        style="flex:1;padding:14px;background:linear-gradient(135deg,#FF6B6B,#FF9A63);color:white;border:none;border-radius:12px;font-size:15px;font-weight:600;cursor:pointer;"
                    >
                        ✅ 交卷
                    </button>
                </div>
                <div style="text-align:center;margin-top:8px;font-size:12px;color:#999;">
                    已答：<span id="answered-count">0</span> / ${currentExam.questions.length}
                </div>
            </div>
        </div>
    `;
}

// 选择答案
function selectAnswer(questionIndex, optionIndex) {
    // 清除同题其他选项
    for (let i = 0; i < 4; i++) {
        const el = document.getElementById(`option-${questionIndex}-${i}`);
        if (el) {
            el.style.background = '#f8f9fa';
            el.style.borderColor = '#e0e0e0';
        }
    }
    
    // 选中当前选项
    const selectedEl = document.getElementById(`option-${questionIndex}-${optionIndex}`);
    if (selectedEl) {
        selectedEl.style.background = '#e8f0ff';
        selectedEl.style.borderColor = '#3377FF';
        selectedEl.classList.add('selected');
    }
    
    // 记录答案
    currentExam.answers[questionIndex] = currentExam.questions[questionIndex].options[optionIndex];
    
    // 更新已答计数
    updateAnsweredCount();
}

// 更新已答计数
function updateAnsweredCount() {
    const count = Object.keys(currentExam.answers).length;
    const el = document.getElementById('answered-count');
    if (el) el.textContent = count;
}

// 开始计时
function startExamTimer() {
    if (currentExam.timer) {
        clearInterval(currentExam.timer);
    }
    
    currentExam.timer = setInterval(() => {
        const elapsed = Math.floor((Date.now() - currentExam.startTime) / 1000);
        const remaining = currentExam.timeLimit - elapsed;
        
        if (remaining <= 0) {
            clearInterval(currentExam.timer);
            showToast('时间到！自动交卷');
            submitExam();
            return;
        }
        
        const minutes = Math.floor(remaining / 60);
        const seconds = remaining % 60;
        const timerEl = document.getElementById('exam-timer');
        if (timerEl) {
            timerEl.textContent = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
            if (remaining <= 300) { // 最后5分钟变红
                timerEl.style.color = '#FF0000';
                timerEl.style.animation = 'pulse 1s infinite';
            }
        }
    }, 1000);
}

// 交卷
function submitExam() {
    if (currentExam.timer) {
        clearInterval(currentExam.timer);
    }
    
    // 计算成绩
    let correctCount = 0;
    const results = currentExam.questions.map((q, index) => {
        const userAnswer = currentExam.answers[index] || '';
        const isCorrect = String(userAnswer).trim() === String(q.answer).trim();
        if (isCorrect) correctCount++;
        return {
            ...q,
            userAnswer,
            isCorrect
        };
    });
    
    const score = Math.round((correctCount / currentExam.questions.length) * 100);
    const timeUsed = Math.floor((Date.now() - currentExam.startTime) / 1000);
    
    // 保存记录
    const record = {
        id: Date.now(),
        date: new Date().toLocaleString(),
        subject: currentExam.subject,
        grade: currentExam.grade,
        difficulty: currentExam.difficulty,
        mode: currentExam.mode,
        score,
        total: currentExam.questions.length,
        correct: correctCount,
        timeUsed,
        results,
        hasPaper: !!currentExam.uploadedPaper
    };
    
    examHistory.unshift(record);
    saveExamHistory();
    
    // 显示结果
    renderExamResult(record);
}

// 渲染考试结果
function renderExamResult(record) {
    const container = document.getElementById('fullscreen-content');
    if (!container) return;
    
    const subjectInfo = examConfig.subjects[record.subject] || { name: '自定义', icon: '📄' };
    const percentage = Math.round((record.correct / record.total) * 100);
    const minutes = Math.floor(record.timeUsed / 60);
    const seconds = record.timeUsed % 60;
    
    // 根据分数显示不同颜色
    let scoreColor = '#43E97B';
    let scoreComment = '优秀！继续保持！';
    if (percentage < 60) {
        scoreColor = '#FF6B6B';
        scoreComment = '需要加油哦！';
    } else if (percentage < 80) {
        scoreColor = '#FFB800';
        scoreComment = '不错，还有提升空间！';
    }
    
    container.innerHTML = `
        <div style="padding:16px;">
            <div class="card" style="text-align:center;padding:30px 20px;background:linear-gradient(135deg,#667eea,#764ba2);color:white;">
                <div style="font-size:64px;font-weight:bold;margin-bottom:8px;">${percentage}</div>
                <div style="font-size:18px;opacity:0.9;">${scoreComment}</div>
                <div style="display:flex;justify-content:center;gap:30px;margin-top:20px;font-size:14px;opacity:0.9;">
                    <div>✅ 正确 ${record.correct}</div>
                    <div>❌ 错误 ${record.total - record.correct}</div>
                    <div>⏱️ 用时 ${minutes}:${String(seconds).padStart(2, '0')}</div>
                </div>
            </div>
            
            ${record.hasPaper ? `
                <div style="margin-top:16px;">
                    <div style="font-weight:600;margin-bottom:8px;">📄 你的试卷</div>
                    <img src="${currentExam.uploadedPaper}" style="width:100%;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,0.1);" />
                </div>
            ` : ''}
            
            <h4 style="margin:20px 0 12px;">📋 答题详情</h4>
            <div style="max-height:calc(100vh - 400px);overflow-y:auto;padding-right:8px;">
                ${record.results.map((r, index) => `
                    <div class="card" style="margin-bottom:12px;padding:14px;border-left:4px solid ${r.isCorrect ? '#43E97B' : '#FF6B6B'};">
                        <div style="display:flex;align-items:flex-start;gap:10px;">
                            <span style="font-size:18px;">${r.isCorrect ? '✅' : '❌'}</span>
                            <div style="flex:1;">
                                <div style="font-weight:600;margin-bottom:8px;">
                                    ${index + 1}. ${r.question}
                                </div>
                                <div style="font-size:13px;color:#666;margin-bottom:4px;">
                                    你的答案：<span style="color:${r.isCorrect ? '#43E97B' : '#FF6B6B'};font-weight:600;">${r.userAnswer || '未作答'}</span>
                                </div>
                                ${!r.isCorrect ? `
                                    <div style="font-size:13px;color:#666;margin-bottom:4px;">
                                        正确答案：<span style="color:#43E97B;font-weight:600;">${r.answer}</span>
                                    </div>
                                    <div style="font-size:12px;color:#999;background:#f5f7ff;padding:8px;border-radius:6px;">
                                        💡 ${r.explanation}
                                    </div>
                                ` : ''}
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
            
            <div style="display:flex;gap:12px;margin-top:16px;">
                <button 
                    onclick="renderExam(document.getElementById('fullscreen-content'))"
                    style="flex:1;padding:14px;background:linear-gradient(135deg,#667eea,#764ba2);color:white;border:none;border-radius:12px;font-size:15px;font-weight:600;cursor:pointer;"
                >
                    🔄 再来一次
                </button>
                <button 
                    onclick="closeFullscreenPage()"
                    style="flex:1;padding:14px;background:#f5f5f5;color:#666;border:none;border-radius:12px;font-size:15px;font-weight:600;cursor:pointer;"
                >
                    📝 返回首页
                </button>
            </div>
        </div>
    `;
}

// 渲染历史记录
function renderExamHistory() {
    if (examHistory.length === 0) {
        return '<div style="text-align:center;padding:20px;color:#999;">暂无考试记录</div>';
    }
    
    return examHistory.slice(0, 10).map(record => {
        const subjectInfo = examConfig.subjects[record.subject] || { name: '自定义', icon: '📄' };
        const percentage = Math.round((record.correct / record.total) * 100);
        return `
            <div style="display:flex;align-items:center;padding:12px;background:white;border-radius:10px;margin-bottom:8px;">
                <div style="font-size:24px;margin-right:12px;">${subjectInfo.icon}</div>
                <div style="flex:1;">
                    <div style="font-weight:600;font-size:14px;">${subjectInfo.name} ${record.mode === 'manual' ? '·上传试卷' : '·' + examConfig.difficulties[record.difficulty]?.name}</div>
                    <div style="font-size:12px;color:#999;">${record.date}</div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:20px;font-weight:bold;color:${percentage >= 80 ? '#43E97B' : percentage >= 60 ? '#FFB800' : '#FF6B6B'}">${percentage}分</div>
                    <div style="font-size:11px;color:#999;">${record.correct}/${record.total}题</div>
                </div>
            </div>
        `;
    }).join('');
}

// 保存历史记录到本地存储
function saveExamHistory() {
    try {
        localStorage.setItem('exam_history', JSON.stringify(examHistory.slice(0, 50))); // 最多保存50条
    } catch (e) {
        console.error('保存考试历史失败:', e);
    }
}

// 从本地存储加载历史记录
function loadExamHistory() {
    try {
        const saved = localStorage.getItem('exam_history');
        if (saved) {
            examHistory = JSON.parse(saved);
        }
    } catch (e) {
        console.error('加载考试历史失败:', e);
        examHistory = [];
    }
}

// 挂载到window
window.renderExam = renderExam;
window.setExamMode = setExamMode;
window.handlePaperUpload = handlePaperUpload;
window.clearUploadedPaper = clearUploadedPaper;
window.toggleHandwriting = toggleHandwriting;
window.selectExamSubject = selectExamSubject;
window.selectExamGrade = selectExamGrade;
window.selectExamDifficulty = selectExamDifficulty;
window.startNewExam = startNewExam;
window.selectAnswer = selectAnswer;
window.selectManualAnswer = selectManualAnswer;
window.setManualAnswer = setManualAnswer;
window.closeOptionSelector = closeOptionSelector;
window.submitExam = submitExam;

// ES6导出
export {
    examModule,
    renderExam,
    startNewExam,
    submitExam
};

console.log('[V231] 模拟考试模块（增强版）加载完成');
