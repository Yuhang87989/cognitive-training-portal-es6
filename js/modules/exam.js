// 版本: V231 - ES6 Module
// 模拟考试模块 - 独立功能模块

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
    timer: null
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

// 渲染主界面
function renderExam(container) {
    container.innerHTML = `
        <div class="card">
            <h3 style="margin-bottom:16px;">📝 模拟考试</h3>
            <p style="color:#666;font-size:13px;margin-bottom:20px;">全真模拟，实战演练，检验学习成果</p>
            
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
    const config = examConfig.difficulties[currentExam.difficulty];
    const subjectInfo = examConfig.subjects[currentExam.subject];
    
    // 生成题目
    currentExam.questions = generateExamQuestions(currentExam.subject, currentExam.grade, config.questionCount);
    currentExam.answers = {};
    currentExam.timeLimit = config.time * 60;
    currentExam.startTime = Date.now();
    
    // 渲染考试界面
    renderExamInterface(subjectInfo, config);
    
    // 开始计时
    startExamTimer();
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
    const options = [correctAnswer];
    const distractors = generateDistractors(correctAnswer, subject);
    
    while (options.length < 4 && distractors.length > 0) {
        const idx = Math.floor(Math.random() * distractors.length);
        options.push(distractors.splice(idx, 1)[0]);
    }
    
    return shuffleArray(options);
}

// 生成干扰项
function generateDistractors(correctAnswer, subject) {
    const distractors = [];
    const num = parseFloat(correctAnswer);
    
    if (!isNaN(num)) {
        // 数字干扰项
        distractors.push(String(num + 1));
        distractors.push(String(num - 1));
        distractors.push(String(num * 2));
        distractors.push(String(Math.floor(num / 2)));
    } else {
        // 文字干扰项
        distractors.push(correctAnswer + '（错误）');
        distractors.push('其他' + correctAnswer);
        distractors.push('不正确答案');
    }
    
    return distractors.filter(d => d !== correctAnswer);
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
    
    container.innerHTML = `
        <div style="padding:16px;">
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
                    <div class="card" id="question-${index}" style="margin-bottom:16px;">
                        <div style="display:flex;gap:12px;">
                            <div style="background:#3377FF;color:white;width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:600;flex-shrink:0;">
                                ${index + 1}
                            </div>
                            <div style="flex:1;">
                                <div style="font-weight:600;margin-bottom:12px;line-height:1.5;">${q.question}</div>
                                <div style="display:flex;flex-direction:column;gap:8px;">
                                    ${q.options.map((opt, optIdx) => `
                                        <label 
                                            onclick="selectAnswer(${index}, '${optIdx}')"
                                            style="padding:10px 14px;background:#f8f9fa;border:2px solid #e0e0e0;border-radius:8px;cursor:pointer;transition:all 0.2s;"
                                            id="option-${index}-${optIdx}"
                                        >
                                            <span style="font-weight:600;margin-right:8px;">${String.fromCharCode(65 + optIdx)}.</span>
                                            ${opt}
                                        </label>
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
        score,
        total: currentExam.questions.length,
        correct: correctCount,
        timeUsed,
        results
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
    
    const subjectInfo = examConfig.subjects[record.subject];
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
            
            <h4 style="margin:20px 0 12px;">📋 题目解析</h4>
            <div style="max-height:calc(100vh - 350px);overflow-y:auto;padding-right:8px;">
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
                    onclick="startNewExam()"
                    style="flex:1;padding:14px;background:linear-gradient(135deg,#667eea,#764ba2);color:white;border:none;border-radius:12px;font-size:15px;font-weight:600;cursor:pointer;"
                >
                    🔄 再考一次
                </button>
                <button 
                    onclick="renderExam(document.getElementById('fullscreen-content'))"
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
        const subjectInfo = examConfig.subjects[record.subject];
        const percentage = Math.round((record.correct / record.total) * 100);
        return `
            <div style="display:flex;align-items:center;padding:12px;background:white;border-radius:10px;margin-bottom:8px;">
                <div style="font-size:24px;margin-right:12px;">${subjectInfo.icon}</div>
                <div style="flex:1;">
                    <div style="font-weight:600;font-size:14px;">${subjectInfo.name} - ${examConfig.difficulties[record.difficulty].name}</div>
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
window.selectExamSubject = selectExamSubject;
window.selectExamGrade = selectExamGrade;
window.selectExamDifficulty = selectExamDifficulty;
window.startNewExam = startNewExam;
window.selectAnswer = selectAnswer;
window.submitExam = submitExam;

// ES6导出
export {
    examModule,
    renderExam,
    startNewExam,
    submitExam
};

console.log('[V231] 模拟考试模块加载完成');
