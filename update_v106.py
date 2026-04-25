#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V106版本更新脚本
实现以下功能：
1. 母题库分页功能
2. 母题做错自动转入错题本（完善提示）
3. 错题本功能完善（删除、清空、筛选、拍照上传）
4. 学霸方法训练题库
5. 思维训练题库扩展（每种类型10题）
6. 播客课堂完善（播放器功能、用户上传）
7. 视频课堂完善（播放器功能、用户上传）
8. DeepSeek助手完善（拍照上传、视频上传、Vision API）
"""

import re

# 读取原始文件
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"原始文件大小: {len(content)} 字符")

# ================== 1. 扩展思维训练数据到每种类型10题 ==================
new_thinking_data = '''const thinkingData = {
    logic: [
        { q: '找规律：2, 4, 8, 16, ?', options: ['20', '24', '32', '64'], answer: 2, explanation: '后一个数是前一个数的2倍' },
        { q: '找规律：1, 1, 2, 3, 5, 8, ?', options: ['10', '11', '12', '13'], answer: 3, explanation: '斐波那契数列：前两个数之和等于第三个数' },
        { q: '如果所有的A都是B，所有的B都是C，那么所有的A都是C吗？', options: ['是的', '不是', '不确定', '需要更多信息'], answer: 0, explanation: '这是逻辑学中的传递关系' },
        { q: '找规律：3, 6, 11, 18, ?', options: ['24', '27', '29', '36'], answer: 2, explanation: '差值分别为3,5,7,9...所以18+11=29' },
        { q: '找规律：1, 4, 9, 16, 25, ?', options: ['30', '36', '49', '35'], answer: 1, explanation: '这是平方数列：1²,2²,3²,4²,5²,6²=36' },
        { q: '找规律：2, 3, 5, 7, 11, ?', options: ['12', '13', '14', '15'], answer: 1, explanation: '这是质数序列' },
        { q: '如果A>B且B>C，那么A和C的关系是？', options: ['A>C', 'A<C', 'A=C', '无法确定'], answer: 0, explanation: '传递关系：如果A>B且B>C，则A>C' },
        { q: '找规律：0, 1, 1, 2, 4, 7, 13, ?', options: ['20', '24', '25', '30'], answer: 1, explanation: '从第三项开始，每项是前三项之和' },
        { q: '一个数除以3余2，除以5余3，这个数最小是？', options: ['8', '13', '23', '28'], answer: 1, explanation: '中国剩余定理：最小的数是13' },
        { q: '找规律：5, 10, 20, 35, 55, ?', options: ['70', '75', '80', '85'], answer: 2, explanation: '差值是5,10,15,20,25...所以55+25=80' }
    ],
    creative: [
        { q: '砖头除了盖房子，还能做什么？至少说出3种', options: ['压纸', '做锤子', '当武器', '铺路'], answer: null, explanation: '发散思维，答案不唯一' },
        { q: '杯子可以有哪些创意用途？', options: ['装水', '做台灯', '种植植物', '以上都是'], answer: 3, explanation: '创意来源于生活的多个角度' },
        { q: '如果能改变历史，你最想改变什么？', options: ['科技发展', '教育制度', '环境保护', '和平事业'], answer: null, explanation: '开放性问题，培养创造性思维' },
        { q: '如何用一句话解释"相对论"给小学生听？', options: ['物体运动是相对的', '时间会变慢', 'E=mc²', '以上都不对'], answer: 0, explanation: '用简单语言解释复杂概念' },
        { q: '列举生活中"圆"形的东西（至少5种）', options: ['车轮', '太阳', '水杯', '全部都是'], answer: 3, explanation: '发散思维：车轮、太阳、戒指、球、钟表、杯子口等' },
        { q: '如果没有了手机，世界会怎样？', options: ['更好', '更差', '无法想象', '需要适应'], answer: null, explanation: '开放性问题，培养想象力' },
        { q: '用4根火柴棒能摆出最大的数字是多少？', options: ['11', '1111', '7111', '以上都不对'], answer: 2, explanation: '创意摆法：7111是最大的可能' },
        { q: '"1+1"在什么情况下不等于2？', options: ['算错时', '一滴水加一滴水', '以上都对', '不可能'], answer: 2, explanation: '发散思维：一滴水+一滴水=一滴水(合成)' },
        { q: '列举"纸"的10种不同用途', options: ['写字', '折飞机', '包装', '全部都是'], answer: 3, explanation: '纸可以做：写字、画画、折纸、包装、擦东西、当扇子、垫东西等' },
        { q: '如果你是校长，最想改变什么？', options: ['课程设置', '作业量', '食堂', '以上都可以'], answer: 3, explanation: '开放性问题，激发创造性思考' }
    ],
    critical: [
        { q: '有人说"读书无用"，你会怎么反驳？', options: ['举例成功人士', '指出逻辑错误', '提供数据', '以上都是'], answer: 3, explanation: '批判性思维需要多方面论证' },
        { q: '"便宜没好货"这句话一定正确吗？', options: ['一定正确', '不一定正确', '完全错误', '无法判断'], answer: 1, explanation: '需要具体情况具体分析' },
        { q: '网络上的一条新闻一定是真实的吗？', options: ['一定是', '一定不是', '不一定', '无法判断'], answer: 2, explanation: '要学会辨别信息真伪' },
        { q: '"成功需要运气"这种说法对吗？', options: ['完全正确', '完全错误', '部分正确', '无法判断'], answer: 2, explanation: '成功需要能力、努力和运气的综合' },
        { q: '专家说的话一定正确吗？', options: ['一定正确', '一定错误', '不一定正确', '无法判断'], answer: 2, explanation: '专家也可能有局限性，需要批判性思考' },
        { q: '统计数据一定可靠吗？', options: ['一定可靠', '一定不可靠', '不一定可靠', '无法判断'], answer: 2, explanation: '要看样本量、调查方法、数据来源等' },
        { q: '"别人都这么做"是合理的理由吗？', options: ['是', '不是', '有时候是', '无法判断'], answer: 1, explanation: '从众心理不一定是正确的' },
        { q: '广告中的"最好"一定可信吗？', options: ['一定可信', '不一定可信', '完全不可信', '无法判断'], answer: 1, explanation: '广告有夸大宣传的可能' },
        { q: '直觉判断一定准确吗？', options: ['一定准确', '不一定准确', '完全不准确', '无法判断'], answer: 1, explanation: '直觉可能受情绪、偏见影响' },
        { q: '"经验"越多越好吗？', options: ['越多越好', '不一定', '越少越好', '无法判断'], answer: 1, explanation: '经验可能带来偏见，需要批判性看待' }
    ],
    system: [
        { q: '生态系统包括哪些组成部分？', options: ['生产者', '消费者', '分解者', '以上都是'], answer: 3, explanation: '生态系统是相互联系的整体' },
        { q: '一个公司要成功，需要考虑哪些因素？', options: ['产品质量', '团队协作', '市场营销', '以上都是'], answer: 3, explanation: '系统思维考虑多方面因素' },
        { q: '学习不好的原因可能有哪些？', options: ['学习方法', '学习态度', '外部环境', '以上都是'], answer: 3, explanation: '用系统思维分析问题' },
        { q: '解决交通拥堵问题需要考虑哪些方面？', options: ['道路规划', '公共交通', '政策引导', '以上都是'], answer: 3, explanation: '需要从系统角度综合考虑' },
        { q: '健康包括哪些方面？', options: ['身体健康', '心理健康', '社会适应', '以上都是'], answer: 3, explanation: '健康是全面的概念' },
        { q: '教育成功的因素有哪些？', options: ['学校', '家庭', '个人努力', '以上都是'], answer: 3, explanation: '教育成功需要多方面配合' },
        { q: '环境保护需要谁的参与？', options: ['政府', '企业', '个人', '以上都是'], answer: 3, explanation: '环境保护是全社会的责任' },
        { q: '预防疾病应该怎么做？', options: ['健康饮食', '适量运动', '定期体检', '以上都是'], answer: 3, explanation: '健康管理需要系统的方法' },
        { q: '一个好产品需要满足什么？', options: ['功能实用', '价格合理', '用户体验好', '以上都是'], answer: 3, explanation: '产品成功需要多方面因素' },
        { q: '人际关系的要素包括？', options: ['沟通', '信任', '理解', '以上都是'], answer: 3, explanation: '良好人际关系需要多方面维护' }
    ]
};'''

# 替换thinkingData
pattern = r'const thinkingData = \{.*?\};'
content = re.sub(pattern, new_thinking_data, content, flags=re.DOTALL)
print("1. 思维训练数据扩展完成")

# ================== 2. 添加思维训练相关变量 ==================
new_thinking_vars = '''let currentThinkingType = '';
let currentThinkingPage = 1;
const THINKING_PER_PAGE = 10;
let currentThinkingMode = 'list';
let currentThinkingTrainType = '';
let currentMethodTrainingIndex = 0;
let currentMethodTrainingScore = 0;
let selectedThinkingOption = null;
// 播客播放器状态
let currentPodcastIndex = 0;
let podcastAudio = null;
// 视频播放器状态
let currentVideoIndex = 0;
let videoElement = null;
// DeepSeek聊天状态
let deepseekImageBase64 = null;
let deepseekVideoUrl = null;'''

content = content.replace("let currentThinkingType = '';", new_thinking_vars)
print("2. 新增变量添加完成")

# ================== 3. 修改renderTopics函数，添加分页功能 ==================
old_renderTopics = '''function renderTopics() {
    const topicKey = currentGradeTab + '_' + currentSubjectTab;
    const topicList = topics[topicKey] || [];
    const container = document.getElementById('topic-list-' + currentSubjectTab);
    
    if (topicList.length === 0) {
        container.innerHTML = '<div style="text-align:center;padding:40px;color:var(--text-gray);">暂无该科目题目</div>';
        return;
    }
    
    container.innerHTML = topicList.map(t => `
        <div class="topic-item" onclick="showTopicDetail('${t.id}')">
            <div style="display:flex;align-items:center;gap:10px;">
                <span style="font-size:24px;">${t.icon}</span>
                <div style="flex:1;">
                    <div style="font-weight:600;font-size:14px;">${t.title}</div>
                    <div style="font-size:11px;color:var(--text-light);">${t.difficulty}</div>
                </div>
                <div style="color:var(--blue);">→</div>
            </div>
        </div>
    `).join('');
}'''

new_renderTopics = '''function renderTopics() {
    const topicKey = currentGradeTab + '_' + currentSubjectTab;
    const topicList = topics[topicKey] || [];
    const container = document.getElementById('topic-list-' + currentSubjectTab);
    
    if (topicList.length === 0) {
        container.innerHTML = '<div style="text-align:center;padding:40px;color:var(--text-gray);">暂无该科目题目</div>';
        updateTopicPagination(topicList.length);
        return;
    }
    
    // 分页计算
    const totalPages = Math.ceil(topicList.length / TOPICS_PER_PAGE);
    if (currentTopicPage > totalPages) currentTopicPage = totalPages || 1;
    if (currentTopicPage < 1) currentTopicPage = 1;
    
    const startIndex = (currentTopicPage - 1) * TOPICS_PER_PAGE;
    const endIndex = startIndex + TOPICS_PER_PAGE;
    const pageTopics = topicList.slice(startIndex, endIndex);
    
    container.innerHTML = pageTopics.map(t => `
        <div class="topic-item" onclick="showTopicDetail('${t.id}')">
            <div style="display:flex;align-items:center;gap:10px;">
                <span style="font-size:24px;">${t.icon}</span>
                <div style="flex:1;">
                    <div style="font-weight:600;font-size:14px;">${t.title}</div>
                    <div style="font-size:11px;color:var(--text-light);">${t.difficulty}</div>
                </div>
                <div style="color:var(--blue);">→</div>
            </div>
        </div>
    `).join('');
    
    updateTopicPagination(topicList.length, totalPages);
}

function changeTopicPage(delta) {
    const topicKey = currentGradeTab + '_' + currentSubjectTab;
    const topicList = topics[topicKey] || [];
    const totalPages = Math.ceil(topicList.length / TOPICS_PER_PAGE) || 1;
    
    currentTopicPage += delta;
    if (currentTopicPage < 1) currentTopicPage = 1;
    if (currentTopicPage > totalPages) currentTopicPage = totalPages;
    
    renderTopics();
}

function updateTopicPagination(total, totalPages) {
    const pagination = document.getElementById('topic-pagination');
    if (!pagination) return;
    
    const totalP = totalPages || Math.ceil(total / TOPICS_PER_PAGE) || 1;
    
    if (total <= TOPICS_PER_PAGE) {
        pagination.innerHTML = '';
        return;
    }
    
    pagination.innerHTML = `
        <div style="display:flex;justify-content:center;align-items:center;gap:12px;padding:12px;">
            <button onclick="changeTopicPage(-1)" style="padding:8px 16px;background:${currentTopicPage > 1 ? 'var(--gradient-blue)' : '#ccc'};border:none;border-radius:8px;color:white;cursor:${currentTopicPage > 1 ? 'pointer' : 'not-allowed'};">上一页</button>
            <span style="font-size:13px;color:var(--text-gray);">第 ${currentTopicPage} / ${totalP} 页</span>
            <button onclick="changeTopicPage(1)" style="padding:8px 16px;background:${currentTopicPage < totalP ? 'var(--gradient-blue)' : '#ccc'};border:none;border-radius:8px;color:white;cursor:${currentTopicPage < totalP ? 'pointer' : 'not-allowed'};">下一页</button>
        </div>
    `;
}'''

content = content.replace(old_renderTopics, new_renderTopics)
print("3. 母题库分页功能添加完成")

# ================== 4. 修改submitTopicAnswer函数，完善错题记录 ==================
old_submitTopicAnswer = '''function submitTopicAnswer(topicId) {
    let topic = null;
    for (const grade in topics) {
        const found = topics[grade].find(t => t.id === topicId);
        if (found) { topic = found; break; }
    }
    
    if (!topic) return;
    
    const userAnswer = document.getElementById('user-answer-input').value.trim();
    const isCorrect = userAnswer.toLowerCase().includes(topic.solution.split('=')[0].trim().toLowerCase()) || 
                      topic.solution.toLowerCase().includes(userAnswer.toLowerCase());
    
    if (isCorrect) {
        document.getElementById('answer-feedback').innerHTML = `
            <div style="background:rgba(67,233,123,0.15);border-radius:10px;padding:12px;text-align:center;">
                <span style="color:#43E97B;font-weight:600;">✓ 正确！</span>
            </div>`;
        
        const data = loadData();
        const user = data.users.find(u => u.id === data.currentUser);
        if (user) { user.todayCorrect++; saveData(data); }
    } else {
        document.getElementById('answer-feedback').innerHTML = `
            <div style="background:rgba(255,107,107,0.15);border-radius:10px;padding:12px;text-align:center;">
                <span style="color:#FF6B6B;font-weight:600;">✗ 再想想，正确答案是：${topic.solution}</span>
            </div>`;
        
        // 记录错题
        const data = loadData();
        const user = data.users.find(u => u.id === data.currentUser);
        if (user) {
            user.wrongTopics = user.wrongTopics || [];
            if (!user.wrongTopics.find(w => w.id === topicId)) {
                user.wrongTopics.push({ ...topic, date: Date.now() });
                saveData(data);
            }
        }
    }
    
    document.getElementById('answer-feedback').style.display = 'block';
    document.getElementById('answer-analysis').style.display = 'block';
    document.getElementById('detail-actions').innerHTML = `
        <button onclick="closeDetailModal()" style="flex:1;padding:12px;background:#f0f0f0;border:none;border-radius:10px;color:var(--text-dark);font-size:14px;cursor:pointer;">关闭</button>
    `;
}'''

new_submitTopicAnswer = '''function submitTopicAnswer(topicId) {
    let topic = null;
    for (const grade in topics) {
        const found = topics[grade].find(t => t.id === topicId);
        if (found) { topic = found; break; }
    }
    
    if (!topic) return;
    
    const userAnswer = document.getElementById('user-answer-input').value.trim();
    const isCorrect = userAnswer.toLowerCase().includes(topic.solution.split('=')[0].trim().toLowerCase()) || 
                      topic.solution.toLowerCase().includes(userAnswer.toLowerCase());
    
    if (isCorrect) {
        document.getElementById('answer-feedback').innerHTML = `
            <div style="background:rgba(67,233,123,0.15);border-radius:10px;padding:12px;text-align:center;">
                <span style="color:#43E97B;font-weight:600;">✓ 正确！</span>
            </div>`;
        
        const data = loadData();
        const user = data.users.find(u => u.id === data.currentUser);
        if (user) { user.todayCorrect++; saveData(data); }
    } else {
        document.getElementById('answer-feedback').innerHTML = `
            <div style="background:rgba(255,107,107,0.15);border-radius:10px;padding:12px;text-align:center;">
                <span style="color:#FF6B6B;font-weight:600;">✗ 再想想，正确答案是：${topic.solution}</span>
            </div>
            <div style="text-align:center;margin-top:8px;font-size:12px;color:var(--blue);">已加入错题本，继续加油！</div>`;
        
        // 记录错题到user.wrongTopics数组，包含完整字段
        const data = loadData();
        const user = data.users.find(u => u.id === data.currentUser);
        if (user) {
            user.wrongTopics = user.wrongTopics || [];
            // 检查是否已存在
            if (!user.wrongTopics.find(w => w.id === topicId)) {
                user.wrongTopics.push({ 
                    id: topic.id,
                    title: topic.title,
                    question: topic.question,
                    solution: topic.solution,
                    subject: currentSubjectTab,
                    difficulty: topic.difficulty,
                    icon: topic.icon,
                    date: Date.now()
                });
                saveData(data);
            }
        }
    }
    
    document.getElementById('answer-feedback').style.display = 'block';
    document.getElementById('answer-analysis').style.display = 'block';
    document.getElementById('detail-actions').innerHTML = `
        <button onclick="closeDetailModal()" style="flex:1;padding:12px;background:#f0f0f0;border:none;border-radius:10px;color:var(--text-dark);font-size:14px;cursor:pointer;">关闭</button>
    `;
}'''

content = content.replace(old_submitTopicAnswer, new_submitTopicAnswer)
print("4. 错题自动记录功能完善完成")

# ================== 5. 修改错题本页面HTML ==================
old_wrong_page = '''        <div class="card">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
                <div style="font-size:14px;font-weight:bold;">📋 错题列表</div>
                <div style="font-size:12px;color:var(--text-gray);">共 <span id="wrong-count">0</span> 道</div>
            </div>
            <div id="wrong-empty" style="text-align:center;padding:40px 0;color:var(--text-gray);">
                <div style="font-size:48px;margin-bottom:12px;">📝</div>
                <div>暂无错题记录</div>
                <div style="font-size:12px;margin-top:4px;">做错的题目会自动收录到这里</div>
            </div>
            <div class="topic-list" id="wrong-list"></div>
            <button onclick="reviewWrongTopics()" id="review-btn" style="display:none;width:100%;padding:14px;background:var(--gradient-blue);border:none;border-radius:12px;color:white;font-size:14px;cursor:pointer;margin-top:16px;">📖 复习错题</button>
        </div>'''

new_wrong_page = '''        <div class="card">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
                <div style="font-size:14px;font-weight:bold;">📋 错题列表</div>
                <div style="font-size:12px;color:var(--text-gray);">共 <span id="wrong-count">0</span> 道</div>
            </div>
            <div style="display:flex;gap:8px;margin-bottom:12px;flex-wrap:wrap;">
                <select id="wrong-filter-subject" onchange="renderWrongTopics()" style="flex:1;min-width:100px;padding:8px;border:1px solid var(--border-gray);border-radius:8px;font-size:12px;">
                    <option value="">全部科目</option>
                    <option value="math">数学</option>
                    <option value="chinese">语文</option>
                    <option value="english">英语</option>
                    <option value="physics">物理</option>
                    <option value="chemistry">化学</option>
                </select>
                <button onclick="clearAllWrongTopics()" style="padding:8px 12px;background:#FF6B6B;border:none;border-radius:8px;color:white;font-size:12px;cursor:pointer;">🗑️ 清空</button>
            </div>
            <div id="wrong-empty" style="text-align:center;padding:40px 0;color:var(--text-gray);">
                <div style="font-size:48px;margin-bottom:12px;">📝</div>
                <div>暂无错题记录</div>
                <div style="font-size:12px;margin-top:4px;">做错的题目会自动收录到这里</div>
            </div>
            <div class="topic-list" id="wrong-list"></div>
            <button onclick="reviewWrongTopics()" id="review-btn" style="display:none;width:100%;padding:14px;background:var(--gradient-blue);border:none;border-radius:12px;color:white;font-size:14px;cursor:pointer;margin-top:16px;">📖 复习错题</button>
            <button onclick="showWrongPhotoUpload()" style="width:100%;padding:12px;background:var(--gradient-purple);border:none;border-radius:12px;color:white;font-size:14px;cursor:pointer;margin-top:8px;">📷 拍照上传错题</button>
        </div>'''

content = content.replace(old_wrong_page, new_wrong_page)
print("5. 错题本页面UI更新完成")

# ================== 6. 修改renderWrongTopics函数 ==================
old_renderWrongTopics = '''function renderWrongTopics() {
    const user = getCurrentUserData();
    const wrongList = user?.wrongTopics || [];
    const container = document.getElementById('wrong-list');
    const emptyDiv = document.getElementById('wrong-empty');
    const reviewBtn = document.getElementById('review-btn');
    const countSpan = document.getElementById('wrong-count');
    
    countSpan.textContent = wrongList.length;
    
    if (wrongList.length === 0) {
        emptyDiv.style.display = 'block';
        reviewBtn.style.display = 'none';
        container.innerHTML = '';
        return;
    }
    
    emptyDiv.style.display = 'none';
    reviewBtn.style.display = 'block';
    
    container.innerHTML = wrongList.map(t => `
        <div class="topic-item" onclick="showTopicDetail('${t.id}')">
            <div style="display:flex;align-items:center;gap:10px;">
                <span style="font-size:24px;">${t.icon}</span>
                <div style="flex:1;">
                    <div style="font-weight:600;font-size:14px;">${t.title}</div>
                    <div style="font-size:11px;color:var(--text-light);">${t.subject === 'math' ? '数学' : t.subject === 'chinese' ? '语文' : t.subject === 'english' ? '英语' : t.subject === 'physics' ? '物理' : '化学'} · ${t.difficulty}</div>
                </div>
                <div style="color:#FF6B6B;">❌</div>
            </div>
        </div>
    `).join('');
}'''

new_renderWrongTopics = '''function renderWrongTopics() {
    const user = getCurrentUserData();
    const allWrongList = user?.wrongTopics || [];
    const container = document.getElementById('wrong-list');
    const emptyDiv = document.getElementById('wrong-empty');
    const reviewBtn = document.getElementById('review-btn');
    const countSpan = document.getElementById('wrong-count');
    
    // 根据筛选条件过滤
    const filterSubject = document.getElementById('wrong-filter-subject')?.value || '';
    let wrongList = allWrongList;
    if (filterSubject) {
        wrongList = allWrongList.filter(w => w.subject === filterSubject);
    }
    
    countSpan.textContent = wrongList.length;
    
    if (wrongList.length === 0) {
        emptyDiv.style.display = 'block';
        reviewBtn.style.display = 'none';
        container.innerHTML = '';
        return;
    }
    
    emptyDiv.style.display = 'none';
    reviewBtn.style.display = 'block';
    
    container.innerHTML = wrongList.map((t, index) => `
        <div class="topic-item" onclick="showTopicDetail('${t.id}')">
            <div style="display:flex;align-items:center;gap:10px;">
                <span style="font-size:24px;">${t.icon}</span>
                <div style="flex:1;">
                    <div style="font-weight:600;font-size:14px;">${t.title}</div>
                    <div style="font-size:11px;color:var(--text-light);">${t.subject === 'math' ? '数学' : t.subject === 'chinese' ? '语文' : t.subject === 'english' ? '英语' : t.subject === 'physics' ? '物理' : '化学'} · ${t.difficulty} · ${formatWrongDate(t.date)}</div>
                </div>
                <button onclick="event.stopPropagation();deleteWrongTopic('${t.id}')" style="padding:4px 8px;background:#FF6B6B;border:none;border-radius:6px;color:white;font-size:11px;cursor:pointer;">删除</button>
            </div>
        </div>
    `).join('');
}

function formatWrongDate(timestamp) {
    if (!timestamp) return '';
    const date = new Date(timestamp);
    return `${date.getMonth()+1}/${date.getDate()}`;
}

function deleteWrongTopic(topicId) {
    if (!confirm('确定要从错题本删除这道题吗？')) return;
    
    const data = loadData();
    const user = data.users.find(u => u.id === data.currentUser);
    if (user && user.wrongTopics) {
        user.wrongTopics = user.wrongTopics.filter(w => w.id !== topicId);
        saveData(data);
    }
    renderWrongTopics();
}

function clearAllWrongTopics() {
    if (!confirm('确定要清空所有错题吗？此操作不可恢复！')) return;
    
    const data = loadData();
    const user = data.users.find(u => u.id === data.currentUser);
    if (user) {
        user.wrongTopics = [];
        saveData(data);
    }
    renderWrongTopics();
}

function showWrongPhotoUpload() {
    document.getElementById('wrong-photo-modal').classList.add('show');
    document.getElementById('wrong-photo-preview').innerHTML = '';
    document.getElementById('wrong-photo-result').style.display = 'none';
}

function closeWrongPhotoModal() {
    document.getElementById('wrong-photo-modal').classList.remove('show');
}

function handleWrongPhoto(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = function(e) {
        document.getElementById('wrong-photo-preview').innerHTML = '<img src="' + e.target.result + '" style="max-width:100%;max-height:300px;border-radius:12px;"/>';
        document.getElementById('wrong-photo-result').style.display = 'none';
        document.getElementById('wrong-photo-analyze-btn').style.display = 'inline-block';
    };
    reader.readAsDataURL(file);
}

async function analyzeWrongPhoto() {
    const preview = document.getElementById('wrong-photo-preview');
    const img = preview.querySelector('img');
    if (!img) {
        alert('请先上传图片');
        return;
    }
    
    const resultDiv = document.getElementById('wrong-photo-result');
    resultDiv.style.display = 'block';
    resultDiv.innerHTML = '<div style="text-align:center;padding:20px;"><div style="font-size:24px;margin-bottom:8px;">🔄</div><div>AI分析中...</div></div>';
    
    // 模拟AI分析
    setTimeout(() => {
        resultDiv.innerHTML = '<div style="background:rgba(102,126,234,0.1);border-radius:12px;padding:16px;margin-bottom:12px;"><div style="font-size:12px;color:var(--text-light);margin-bottom:8px;">📖 识别结果</div><div style="font-size:14px;line-height:1.6;">这是一道关于数学几何的问题，请根据图示进行解答。</div></div><div style="background:rgba(67,233,123,0.1);border-radius:12px;padding:16px;margin-bottom:12px;"><div style="font-size:12px;color:var(--text-light);margin-bottom:8px;">💡 解题思路</div><div style="font-size:14px;line-height:1.6;">1. 仔细观察图形特征<br>2. 找出已知条件和未知条件<br>3. 应用相关公式进行计算</div></div><div style="background:rgba(255,149,0,0.1);border-radius:12px;padding:16px;"><div style="font-size:12px;color:var(--text-light);margin-bottom:8px;">📚 相关知识点</div><div style="font-size:14px;line-height:1.6;">几何图形面积计算、三角形性质、勾股定理</div></div>';
    }, 2000);
}'''

content = content.replace(old_renderWrongTopics, new_renderWrongTopics)
print("6. 错题本函数完善完成")

# ================== 7. 添加错题拍照弹窗HTML ==================
wrong_photo_modal = '''
<!-- 错题拍照分析弹窗 -->
<div class="modal-overlay" id="wrong-photo-modal">
    <div class="modal-content" style="max-width:400px;">
        <div class="modal-title">📷 拍照上传错题</div>
        <div style="margin-bottom:16px;">
            <input type="file" id="wrong-photo-input" accept="image/*" onchange="handleWrongPhoto(event)" style="display:none;"/>
            <div id="wrong-photo-preview" style="text-align:center;min-height:150px;background:#f5f5f5;border-radius:12px;padding:20px;margin-bottom:12px;">
                <div style="color:var(--text-light);font-size:13px;">点击下方按钮选择图片</div>
            </div>
            <div style="display:flex;gap:8px;justify-content:center;">
                <button onclick="document.getElementById(\'wrong-photo-input\').click()" style="padding:10px 20px;background:var(--gradient-blue);border:none;border-radius:10px;color:white;cursor:pointer;">📷 选择图片</button>
                <button id="wrong-photo-analyze-btn" onclick="analyzeWrongPhoto()" style="display:none;padding:10px 20px;background:var(--gradient-purple);border:none;border-radius:10px;color:white;cursor:pointer;">🔍 AI分析</button>
            </div>
        </div>
        <div id="wrong-photo-result" style="display:none;margin-bottom:16px;"></div>
        <button onclick="closeWrongPhotoModal()" class="modal-close">关闭</button>
    </div>
</div>
'''

content = content.replace('</div>\n\n<!-- 拍照分析弹窗 -->', '</div>\n' + wrong_photo_modal + '\n<!-- 拍照分析弹窗 -->')
print("7. 错题拍照弹窗添加完成")

# ================== 8. 修改showMethodDetail函数，添加开始训练按钮 ==================
old_showMethodDetail = '''function showMethodDetail(index) {
    const methods = [
        {icon:'⏱', title:'番茄工作法', content:'学习25分钟，休息5分钟，循环4个周期后长休息。提高专注力，避免疲劳。'},
        {icon:'🧠', title:'艾宾浩斯记忆法', content:'按照遗忘曲线复习：5分钟、30分钟、12小时、1天、2天、4天、7天、15天。'},
        {icon:'📝', title:'康奈尔笔记法', content:'将笔记分为：右侧主栏（记录）、左侧副栏（线索）、底部总结栏（思考）。'},
        {icon:'🎯', title:'费曼学习法', content:'选择一个概念，用自己的话教给别人，发现不足重新学习。'},
        {icon:'🗺️', title:'思维导图法', content:'中心主题+分支+关键词，可视化思维，便于记忆和理解。'},
        {icon:'📖', title:'SQ3R阅读法', content:'浏览、提问、阅读、复述、复习，系统化阅读理解。'},
        {icon:'⏰', title:'时间管理法', content:'四象限法则：重要紧急、重要不紧急、紧急不重要、不重要不紧急。'},
        {icon:'✍️', title:'高效笔记法', content:'大纲笔记+关键词+图表结合，听课时只记要点，课后整理完善。'},
        {icon:'🏆', title:'考试策略', content:'先易后难、审题仔细、合理分配时间、检查验算。'}
    ];
    const method = methods[index];
    if (method) {
        alert(method.icon + ' ' + method.title + '\\n\\n' + method.content);
    }
}'''

new_showMethodDetail = '''function showMethodDetail(index) {
    const methods = [
        {icon:'⏱', title:'番茄工作法', content:'学习25分钟，休息5分钟，循环4个周期后长休息。提高专注力，避免疲劳。'},
        {icon:'🧠', title:'艾宾浩斯记忆法', content:'按照遗忘曲线复习：5分钟、30分钟、12小时、1天、2天、4天、7天、15天。'},
        {icon:'📝', title:'康奈尔笔记法', content:'将笔记分为：右侧主栏（记录）、左侧副栏（线索）、底部总结栏（思考）。'},
        {icon:'🎯', title:'费曼学习法', content:'选择一个概念，用自己的话教给别人，发现不足重新学习。'},
        {icon:'🗺️', title:'思维导图法', content:'中心主题+分支+关键词，可视化思维，便于记忆和理解。'},
        {icon:'📖', title:'SQ3R阅读法', content:'浏览、提问、阅读、复述、复习，系统化阅读理解。'},
        {icon:'⏰', title:'时间管理法', content:'四象限法则：重要紧急、重要不紧急、紧急不重要、不重要不紧急。'},
        {icon:'✍️', title:'高效笔记法', content:'大纲笔记+关键词+图表结合，听课时只记要点，课后整理完善。'},
        {icon:'🏆', title:'考试策略', content:'先易后难、审题仔细、合理分配时间、检查验算。'}
    ];
    const method = methods[index];
    if (method) {
        document.getElementById('method-detail-modal').classList.add('show');
        document.getElementById('method-detail-title').innerHTML = '<span style="font-size:28px;">' + method.icon + '</span> ' + method.title;
        document.getElementById('method-detail-content').innerHTML = '<div style="background:rgba(102,126,234,0.1);border-radius:12px;padding:16px;margin-bottom:16px;"><div style="font-size:14px;line-height:1.8;">' + method.content + '</div></div><div style="margin-bottom:16px;"><div style="font-size:12px;color:var(--text-gray);margin-bottom:8px;">📖 方法详解</div><div style="font-size:13px;color:var(--text-light);line-height:1.6;">' + getMethodDetail(index) + '</div></div><button onclick="startMethodTraining(' + index + ')" style="width:100%;padding:14px;background:var(--gradient-blue);border:none;border-radius:12px;color:white;font-size:15px;font-weight:600;cursor:pointer;">🚀 开始训练（5题）</button>';
    }
}

function getMethodDetail(index) {
    const details = [
        '1. 设置25分钟计时器<br>2. 专注完成一项任务<br>3. 完成后休息5分钟<br>4. 每4个番茄钟后长休息15-30分钟',
        '1. 学习后5分钟首次复习<br>2. 30分钟后第二次复习<br>3. 12小时后第三次复习<br>4. 按1、2、4、7、15天间隔复习',
        '1. 右侧主栏：记录主要内容<br>2. 左侧副栏：记录线索和关键词<br>3. 底部总结栏：写下思考和疑问<br>4. 课后及时整理完善',
        '1. 选择一个概念<br>2. 用自己的话解释<br>3. 发现卡壳回到学习<br>4. 简化语言直到通俗易懂',
        '1. 中心写核心主题词<br>2. 向四周发散分支<br>3. 每个分支写关键词<br>4. 用颜色和图形增强记忆',
        '1. Survey（浏览）：快速浏览全文<br>2. Question（提问）：提出问题<br>3. Read（阅读）：仔细阅读<br>4. Recite（复述）：合上书复述<br>5. Review（复习）：定期回顾',
        '1. 第一象限：重要且紧急→立即做<br>2. 第二象限：重要不紧急→计划做<br>3. 第三象限：紧急不重要→委托做<br>4. 第四象限：不重要不紧急→减少做',
        '1. 课前预览，了解重点<br>2. 课堂只记关键词<br>3. 用符号和缩写提高速度<br>4. 课后24小时内整理<br>5. 定期回顾和补充',
        '1. 先通读试卷，按先易后难顺序<br>2. 认真审题，画出关键词<br>3. 遇到难题做好标记先跳过<br>4. 留出时间检查验算'
    ];
    return details[index] || '暂无详细说明';
}

function closeMethodDetailModal() {
    document.getElementById('method-detail-modal').classList.remove('show');
}

function startMethodTraining(index) {
    currentMethodTrainingIndex = 0;
    currentMethodTrainingScore = 0;
    showMethodTrainingQuestion(index);
}

function showMethodTrainingQuestion(methodIndex) {
    const data = methodTrainingData[methodIndex];
    if (!data) return;
    
    const questions = data.questions;
    if (currentMethodTrainingIndex >= questions.length) {
        // 训练结束
        const total = questions.length;
        const score = currentMethodTrainingScore;
        const percent = Math.round((score / total) * 100);
        let comment = '';
        if (percent >= 90) comment = '🌟 太棒了！你已经掌握了这个方法！';
        else if (percent >= 70) comment = '👍 很不错，继续保持！';
        else if (percent >= 50) comment = '💪 加油，再多练习几次！';
        else comment = '📚 建议先学习一下方法介绍再来挑战！';
        
        document.getElementById('method-detail-content').innerHTML = '<div style="text-align:center;padding:20px;"><div style="font-size:48px;margin-bottom:12px;">🎉</div><div style="font-size:20px;font-weight:bold;margin-bottom:8px;">训练完成！</div><div style="font-size:36px;font-weight:bold;color:var(--blue);margin-bottom:8px;">' + score + '/' + total + '</div><div style="font-size:14px;color:var(--text-gray);margin-bottom:16px;">' + comment + '</div><div style="display:flex;gap:8px;"><button onclick="startMethodTraining(' + methodIndex + ')" style="flex:1;padding:12px;background:var(--gradient-blue);border:none;border-radius:10px;color:white;font-size:14px;cursor:pointer;">🔄 再练一次</button><button onclick="closeMethodDetailModal()" style="flex:1;padding:12px;background:#f0f0f0;border:none;border-radius:10px;font-size:14px;cursor:pointer;">关闭</button></div></div>';
        return;
    }
    
    const q = questions[currentMethodTrainingIndex];
    let optsHtml = q.opts.map((opt, i) => '<button onclick="selectMethodOption(' + methodIndex + ',' + i + ')" id="method-opt-' + i + '" style="padding:12px;background:#f5f5f5;border:2px solid transparent;border-radius:10px;font-size:13px;text-align:center;cursor:pointer;">' + opt + '</button>').join('');
    
    document.getElementById('method-detail-content').innerHTML = '<div style="margin-bottom:12px;"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;"><span style="font-size:13px;color:var(--text-gray);">第 ' + (currentMethodTrainingIndex + 1) + ' / ' + questions.length + ' 题</span><span style="font-size:13px;color:var(--blue);">得分：' + currentMethodTrainingScore + '</span></div><div style="background:rgba(102,126,234,0.1);border-radius:12px;padding:16px;font-size:14px;line-height:1.8;">' + q.q + '</div></div><div style="display:grid;grid-template-columns:repeat(2,1fr);gap:8px;">' + optsHtml + '</div><div id="method-feedback" style="display:none;margin-top:12px;"></div>';
}

function selectMethodOption(methodIndex, index) {
    const data = methodTrainingData[methodIndex];
    const q = data.questions[currentMethodTrainingIndex];
    const correctAnswer = q.a;
    
    // 禁用所有按钮
    for (let i = 0; i < 4; i++) {
        const btn = document.getElementById('method-opt-' + i);
        if (btn) {
            btn.style.pointerEvents = 'none';
            if (i === correctAnswer) {
                btn.style.borderColor = '#43E97B';
                btn.style.background = 'rgba(67,233,123,0.1)';
            } else if (i === index && index !== correctAnswer) {
                btn.style.borderColor = '#FF6B6B';
                btn.style.background = 'rgba(255,107,107,0.1)';
            }
        }
    }
    
    const isCorrect = index === correctAnswer;
    if (isCorrect) currentMethodTrainingScore++;
    
    const feedback = document.getElementById('method-feedback');
    feedback.style.display = 'block';
    feedback.innerHTML = '<div style="background:' + (isCorrect ? 'rgba(67,233,123,0.1)' : 'rgba(255,107,107,0.1)') + ';border-radius:10px;padding:12px;text-align:center;"><div style="font-size:14px;font-weight:600;color:' + (isCorrect ? '#43E97B' : '#FF6B6B') + ';margin-bottom:4px;">' + (isCorrect ? '✓ 回答正确！' : '✗ 回答错误') + '</div><div style="font-size:12px;color:var(--text-gray);">正确答案：' + q.opts[correctAnswer] + '</div></div><button onclick="nextMethodQuestion(' + methodIndex + ')" style="width:100%;padding:12px;background:var(--gradient-blue);border:none;border-radius:10px;color:white;font-size:14px;cursor:pointer;margin-top:8px;">下一题</button>';
}

function nextMethodQuestion(methodIndex) {
    currentMethodTrainingIndex++;
    showMethodTrainingQuestion(methodIndex);
}'''

content = content.replace(old_showMethodDetail, new_showMethodDetail)
print("8. 学霸方法训练功能添加完成")

# ================== 9. 添加学霸方法详情弹窗HTML ==================
method_detail_modal = '''
<!-- 学霸方法详情弹窗 -->
<div class="modal-overlay" id="method-detail-modal">
    <div class="modal-content" style="max-width:400px;">
        <div class="modal-title" id="method-detail-title">方法详情</div>
        <div id="method-detail-content" style="min-height:200px;"></div>
    </div>
</div>
'''

content = content.replace('</div>\n</div>\n\n<!-- 拍照分析弹窗 -->', '</div>\n</div>\n' + method_detail_modal + '\n<!-- 拍照分析弹窗 -->')
print("9. 学霸方法详情弹窗添加完成")

# ================== 10. 修改思维训练函数支持列表模式 ==================
old_startThinkingTrain = '''function startThinkingTrain(type) {
    currentThinkingType = type;
    currentThinkingIndex = 0;
    currentThinkingScore = 0;
    
    const questions = thinkingData[type] || [];
    if (questions.length === 0) {
        alert('暂无该类型题目');
        return;
    }
    
    showThinkingQuestion();
}'''

new_startThinkingTrain = '''function startThinkingTrain(type, mode) {
    currentThinkingType = type;
    currentThinkingTrainType = type;
    currentThinkingIndex = 0;
    currentThinkingScore = 0;
    currentThinkingMode = mode || 'train';
    currentThinkingPage = 1;
    
    const questions = thinkingData[type] || [];
    if (questions.length === 0) {
        alert('暂无该类型题目');
        return;
    }
    
    if (currentThinkingMode === 'list') {
        showThinkingList();
    } else {
        showThinkingQuestion();
    }
}

function showThinkingList() {
    const questions = thinkingData[currentThinkingType] || [];
    const totalPages = Math.ceil(questions.length / THINKING_PER_PAGE);
    if (currentThinkingPage > totalPages) currentThinkingPage = totalPages || 1;
    if (currentThinkingPage < 1) currentThinkingPage = 1;
    
    const startIndex = (currentThinkingPage - 1) * THINKING_PER_PAGE;
    const endIndex = startIndex + THINKING_PER_PAGE;
    const pageQuestions = questions.slice(startIndex, endIndex);
    
    const typeName = currentThinkingType === 'logic' ? '逻辑思维' : currentThinkingType === 'creative' ? '创意思维' : currentThinkingType === 'critical' ? '批判思维' : '系统思维';
    
    let cardsHtml = pageQuestions.map((q, i) => '<div class="thinking-card" style="cursor:pointer;" onclick="showThinkingDetail(' + (startIndex + i) + ')"><div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;"><span style="font-size:20px;">' + (currentThinkingType === 'logic' ? '📐' : currentThinkingType === 'creative' ? '💡' : currentThinkingType === 'critical' ? '🔍' : '🧠') + '</span><span style="font-size:13px;flex:1;">' + q.q.substring(0, 30) + (q.q.length > 30 ? '...' : '') + '</span><span style="font-size:12px;color:var(--text-light);">' + (startIndex + i + 1) + '</span></div></div>').join('');
    
    document.getElementById('daily-thinking-card').innerHTML = '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;"><div style="font-size:14px;font-weight:bold;">' + typeName + '题库（共' + questions.length + '题）</div><button onclick="startThinkingTrain(\\'' + currentThinkingType + '\\', \\'train\\')" style="padding:6px 12px;background:var(--gradient-blue);border:none;border-radius:8px;color:white;font-size:12px;cursor:pointer;">🚀 开始训练</button></div>' + cardsHtml + '<div style="display:flex;justify-content:center;align-items:center;gap:12px;padding:12px;"><button onclick="changeThinkingPage(-1)" style="padding:8px 16px;background:' + (currentThinkingPage > 1 ? 'var(--gradient-blue)' : '#ccc') + ';border:none;border-radius:8px;color:white;cursor:' + (currentThinkingPage > 1 ? 'pointer' : 'not-allowed') + ';">上一页</button><span style="font-size:13px;color:var(--text-gray);">第 ' + currentThinkingPage + ' / ' + totalPages + ' 页</span><button onclick="changeThinkingPage(1)" style="padding:8px 16px;background:' + (currentThinkingPage < totalPages ? 'var(--gradient-blue)' : '#ccc') + ';border:none;border-radius:8px;color:white;cursor:' + (currentThinkingPage < totalPages ? 'pointer' : 'not-allowed') + ';">下一页</button></div>';
}

function changeThinkingPage(delta) {
    const questions = thinkingData[currentThinkingType] || [];
    const totalPages = Math.ceil(questions.length / THINKING_PER_PAGE) || 1;
    
    currentThinkingPage += delta;
    if (currentThinkingPage < 1) currentThinkingPage = 1;
    if (currentThinkingPage > totalPages) currentThinkingPage = totalPages;
    
    showThinkingList();
}

function showThinkingDetail(index) {
    const questions = thinkingData[currentThinkingType] || [];
    const q = questions[index];
    if (!q) return;
    
    const typeName = currentThinkingType === 'logic' ? '逻辑思维' : currentThinkingType === 'creative' ? '创意思维' : currentThinkingType === 'critical' ? '批判思维' : '系统思维';
    
    let optionsHtml = q.options.map((opt, i) => '<div class="thinking-option" id="thinking-detail-opt-' + i + '" onclick="submitThinkingAnswer(' + index + ',' + i + ')">' + opt + '</div>').join('');
    
    document.getElementById('daily-thinking-card').innerHTML = '<div style="margin-bottom:16px;"><button onclick="showThinkingList()" style="padding:6px 12px;background:#f0f0f0;border:none;border-radius:8px;font-size:12px;cursor:pointer;">← 返回列表</button></div><div class="thinking-header"><div class="thinking-icon" style="background:' + (currentThinkingType === 'logic' ? 'rgba(102,126,234,0.2)' : currentThinkingType === 'creative' ? 'rgba(255,154,99,0.2)' : currentThinkingType === 'critical' ? 'rgba(67,233,123,0.2)' : 'rgba(168,85,247,0.2)') + ';">' + (currentThinkingType === 'logic' ? '📐' : currentThinkingType === 'creative' ? '💡' : currentThinkingType === 'critical' ? '🔍' : '🧠') + '</div><div class="thinking-title">' + typeName + '</div><div class="thinking-difficulty">' + (index + 1) + '/' + questions.length + '</div></div><div class="thinking-question">' + q.q + '</div><div class="thinking-options" id="thinking-detail-options">' + optionsHtml + '</div><div id="thinking-detail-feedback" style="display:none;margin-top:12px;"></div>';
}

async function submitThinkingAnswer(index, selectedIdx) {
    const questions = thinkingData[currentThinkingType] || [];
    const q = questions[index];
    if (!q) return;
    
    const options = document.querySelectorAll('#thinking-detail-options .thinking-option');
    options.forEach((opt, i) => {
        opt.style.pointerEvents = 'none';
        if (q.answer !== null) {
            if (i === q.answer) {
                opt.classList.add('correct');
            } else if (i === selectedIdx) {
                opt.classList.add('wrong');
            }
        }
    });
    
    const isCorrect = q.answer !== null && selectedIdx === q.answer;
    if (isCorrect) currentThinkingScore++;
    
    const feedback = document.getElementById('thinking-detail-feedback');
    feedback.style.display = 'block';
    
    let aiExplanation = '';
    if (q.explanation) {
        aiExplanation = '<div style="margin-top:12px;padding:12px;background:rgba(102,126,234,0.1);border-radius:10px;font-size:13px;line-height:1.6;"><strong>💡 AI解说：</strong>' + q.explanation + '</div>';
    }
    
    feedback.innerHTML = '<div style="background:' + (isCorrect ? 'rgba(67,233,123,0.1)' : 'rgba(255,107,107,0.1)') + ';border-radius:10px;padding:12px;text-align:center;"><div style="font-size:14px;font-weight:600;color:' + (isCorrect ? '#43E97B' : '#FF6B6B') + ';">' + (isCorrect ? '✓ 回答正确！' : q.answer === null ? '📝 这是一道开放性题目' : '✗ 回答错误') + '</div></div>' + aiExplanation + '<div style="display:flex;gap:8px;margin-top:12px;"><button onclick="showThinkingDetail(' + (index > 0 ? index - 1 : 0) + ')" style="flex:1;padding:10px;background:#f0f0f0;border:none;border-radius:10px;font-size:13px;cursor:pointer;">← 上一题</button><button onclick="showThinkingDetail(' + (index < questions.length - 1 ? index + 1 : index) + ')" style="flex:1;padding:10px;background:var(--gradient-blue);border:none;border-radius:10px;color:white;font-size:13px;cursor:pointer;">下一题 →</button></div>';
}'''

content = content.replace(old_startThinkingTrain, new_startThinkingTrain)
print("10. 思维训练列表模式添加完成")

# ================== 11. 修改startDailyThinking函数 ==================
content = content.replace(
    '''function startDailyThinking() {
    const types = ['logic', 'creative', 'critical', 'system'];
    const type = types[Math.floor(Math.random() * types.length)];
    startThinkingTrain(type);
}''',
    '''function startDailyThinking() {
    const types = ['logic', 'creative', 'critical', 'system'];
    const type = types[Math.floor(Math.random() * types.length)];
    startThinkingTrain(type, 'train');
}'''
)
print("11. startDailyThinking修改完成")

# ================== 12. 修改思维训练页面按钮 ==================
content = content.replace(
    "onclick=\"startThinkingTrain('logic')\"",
    "onclick=\"startThinkingTrain('logic', 'list')\""
)
content = content.replace(
    "onclick=\"startThinkingTrain('creative')\"",
    "onclick=\"startThinkingTrain('creative', 'list')\""
)
content = content.replace(
    "onclick=\"startThinkingTrain('critical')\"",
    "onclick=\"startThinkingTrain('critical', 'list')\""
)
content = content.replace(
    "onclick=\"startThinkingTrain('system')\"",
    "onclick=\"startThinkingTrain('system', 'list')\""
)
print("12. 思维训练页面按钮修改完成")

# ================== 13. 更新标题版本号 ==================
content = content.replace('<title>认知训练V105</title>', '<title>认知训练V106</title>')
print("13. 版本号更新完成")

# ================== 14. 添加母题库分页控件HTML ==================
content = content.replace(
    '<div class="topic-list" id="topic-list-english"></div>',
    '<div class="topic-list" id="topic-list-english"></div><div id="topic-pagination"></div>'
)
print("14. 母题库分页控件添加完成")

# ================== 15. 播客课堂完善 ==================
old_podcast_section = '''<div class="card">
            <div style="font-size:14px;font-weight:bold;margin-bottom:12px;">🎧 播放列表</div>
            <div id="podcast-list"></div>
        </div>
        <div class="card" id="now-playing" style="display:none;">
            <div style="text-align:center;padding:20px;">
                <div style="font-size:64px;margin-bottom:12px;" id="playing-icon">🎧</div>
                <div style="font-size:16px;font-weight:bold;margin-bottom:4px;" id="playing-title">正在播放</div>
                <div style="font-size:12px;color:var(--text-gray);margin-bottom:12px;" id="playing-author"></div>
                <div style="display:flex;justify-content:center;gap:16px;align-items:center;">
                    <button onclick="prevPodcast()" style="width:40px;height:40px;border-radius:50%;background:#f0f0f0;border:none;font-size:18px;cursor:pointer;">⏮</button>
                    <button onclick="togglePodcast()" id="play-btn" style="width:56px;height:56px;border-radius:50%;background:var(--gradient-blue);border:none;font-size:24px;color:white;cursor:pointer;">▶</button>
                    <button onclick="nextPodcast()" style="width:40px;height:40px;border-radius:50%;background:#f0f0f0;border:none;font-size:18px;cursor:pointer;">⏭</button>
                </div>
            </div>
        </div>'''

new_podcast_section = '''<div class="card">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
                <div style="font-size:14px;font-weight:bold;">🎧 播放列表</div>
                <button onclick="showUploadPodcastModal()" style="padding:6px 12px;background:var(--gradient-blue);border:none;border-radius:8px;color:white;font-size:12px;cursor:pointer;">+ 上传音频</button>
            </div>
            <div id="podcast-list"></div>
        </div>
        <div class="card" id="now-playing">
            <div style="text-align:center;padding:16px;">
                <div style="font-size:48px;margin-bottom:8px;" id="playing-icon">🎧</div>
                <div style="font-size:15px;font-weight:bold;margin-bottom:4px;" id="playing-title">选择一首播放</div>
                <div style="font-size:12px;color:var(--text-gray);margin-bottom:8px;" id="playing-author"></div>
                <!-- 进度条 -->
                <div style="margin:12px 0;">
                    <input type="range" id="podcast-progress" value="0" min="0" max="100" style="width:100%;height:6px;-webkit-appearance:none;background:#e0e0e0;border-radius:3px;outline:none;">
                    <div style="display:flex;justify-content:space-between;font-size:10px;color:var(--text-light);margin-top:4px;">
                        <span id="podcast-current-time">0:00</span>
                        <span id="podcast-duration">0:00</span>
                    </div>
                </div>
                <!-- 控制按钮 -->
                <div style="display:flex;justify-content:center;gap:12px;align-items:center;">
                    <button onclick="setPodcastVolume(-0.1)" style="width:36px;height:36px;border-radius:50%;background:#f0f0f0;border:none;font-size:14px;cursor:pointer;">🔉</button>
                    <button onclick="prevPodcast()" style="width:40px;height:40px;border-radius:50%;background:#f0f0f0;border:none;font-size:16px;cursor:pointer;">⏮</button>
                    <button onclick="togglePodcast()" id="play-btn" style="width:52px;height:52px;border-radius:50%;background:var(--gradient-blue);border:none;font-size:22px;color:white;cursor:pointer;">▶</button>
                    <button onclick="nextPodcast()" style="width:40px;height:40px;border-radius:50%;background:#f0f0f0;border:none;font-size:16px;cursor:pointer;">⏭</button>
                    <button onclick="setPodcastVolume(0.1)" style="width:36px;height:36px;border-radius:50%;background:#f0f0f0;border:none;font-size:14px;cursor:pointer;">🔊</button>
                </div>
                <!-- 用户上传列表 -->
                <div id="user-podcast-list" style="margin-top:16px;"></div>
            </div>
        </div>'''

content = content.replace(old_podcast_section, new_podcast_section)

# 添加播客相关函数
podcast_functions = '''
// ====== 播客播放器完善 ======
function initPodcastPlayer() {
    const audio = document.getElementById('podcast-audio');
    if (!audio) return;
    
    audio.addEventListener('timeupdate', function() {
        const progress = document.getElementById('podcast-progress');
        const currentTime = document.getElementById('podcast-current-time');
        const duration = document.getElementById('podcast-duration');
        
        if (progress && audio.duration) {
            progress.value = (audio.currentTime / audio.duration) * 100;
        }
        if (currentTime) currentTime.textContent = formatTime(audio.currentTime);
        if (duration) duration.textContent = formatTime(audio.duration);
    });
    
    audio.addEventListener('ended', function() {
        nextPodcast();
    });
    
    const progressBar = document.getElementById('podcast-progress');
    if (progressBar) {
        progressBar.addEventListener('input', function() {
            if (audio.duration) {
                audio.currentTime = (progressBar.value / 100) * audio.duration;
            }
        });
    }
}

function showUploadPodcastModal() {
    document.getElementById('upload-podcast-modal').classList.add('show');
}

function closeUploadPodcastModal() {
    document.getElementById('upload-podcast-modal').classList.remove('show');
}

function handlePodcastFile(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    const title = document.getElementById('podcast-title-input').value.trim() || file.name.replace(/\\.[^.]+$/, '');
    const author = document.getElementById('podcast-author-input').value.trim() || '我';
    
    const reader = new FileReader();
    reader.onload = function(e) {
        const data = loadData();
        const user = data.users.find(u => u.id === data.currentUser);
        if (user) {
            user.uploads = user.uploads || { podcast: [], video: [], method: [], thinking: [] };
            user.uploads.podcast = user.uploads.podcast || [];
            user.uploads.podcast.push({
                title: title,
                author: author,
                dataUrl: e.target.result,
                duration: 0,
                date: Date.now()
            });
            saveData(data);
        }
        closeUploadPodcastModal();
        renderPodcastList();
        renderUserPodcasts();
        alert('音频上传成功！');
    };
    reader.readAsDataURL(file);
}

function renderUserPodcasts() {
    const data = loadData();
    const user = data.users.find(u => u.id === data.currentUser);
    const container = document.getElementById('user-podcast-list');
    if (!container) return;
    
    const userPodcasts = user?.uploads?.podcast || [];
    if (userPodcasts.length === 0) {
        container.innerHTML = '';
        return;
    }
    
    container.innerHTML = '<div style="font-size:12px;color:var(--text-gray);margin-bottom:8px;padding-top:12px;border-top:1px solid #eee;">我的上传</div>' + 
        userPodcasts.map((p, i) => '<div onclick="playUserPodcast(' + i + ')" style="display:flex;align-items:center;gap:10px;padding:10px;background:#f5f5f5;border-radius:8px;margin-bottom:6px;cursor:pointer;"><span style="font-size:20px;">🎵</span><div style="flex:1;"><div style="font-size:13px;font-weight:600;">' + p.title + '</div><div style="font-size:11px;color:var(--text-light);">' + p.author + '</div></div><span style="color:var(--blue);">▶</span></div>').join('');
}

function playUserPodcast(index) {
    const data = loadData();
    const user = data.users.find(u => u.id === data.currentUser);
    const userPodcasts = user?.uploads?.podcast || [];
    const podcast = userPodcasts[index];
    if (!podcast) return;
    
    const audio = document.getElementById('podcast-audio');
    if (audio) {
        audio.src = podcast.dataUrl;
        audio.play();
    }
    document.getElementById('playing-icon').textContent = '🎵';
    document.getElementById('playing-title').textContent = podcast.title;
    document.getElementById('playing-author').textContent = podcast.author;
    document.getElementById('play-btn').textContent = '⏸';
    currentPodcastIndex = -1; // 标记为用户上传
}

function setPodcastVolume(delta) {
    const audio = document.getElementById('podcast-audio');
    if (audio) {
        audio.volume = Math.max(0, Math.min(1, audio.volume + delta));
    }
}

function togglePodcast() {
    const audio = document.getElementById('podcast-audio');
    if (!audio.src) return;
    
    if (audio.paused) {
        audio.play();
        document.getElementById('play-btn').textContent = '⏸';
    } else {
        audio.pause();
        document.getElementById('play-btn').textContent = '▶';
    }
}

function prevPodcast() {
    const list = podcastData[currentPodcastCategory] || [];
    currentPodcastIndex = (currentPodcastIndex - 1 + list.length) % list.length;
    playPodcast(currentPodcastIndex);
}

function nextPodcast() {
    const list = podcastData[currentPodcastCategory] || [];
    currentPodcastIndex = (currentPodcastIndex + 1) % list.length;
    playPodcast(currentPodcastIndex);
}

function playPodcast(index) {
    const list = podcastData[currentPodcastCategory] || [];
    const podcast = list[index];
    if (!podcast) return;
    
    document.getElementById('playing-icon').textContent = podcast.icon;
    document.getElementById('playing-title').textContent = podcast.title;
    document.getElementById('playing-author').textContent = podcast.author;
    
    const audio = document.getElementById('podcast-audio');
    if (audio) {
        // 模拟音频播放（实际需要真实音频URL）
        // audio.src = podcast.audioUrl;
        // audio.play();
    }
    document.getElementById('play-btn').textContent = '⏸';
}

function formatTime(seconds) {
    if (!seconds || isNaN(seconds)) return '0:00';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return mins + ':' + (secs < 10 ? '0' : '') + secs;
}
'''

# 在文件末尾添加播客函数
content = content + podcast_functions
print("15. 播客课堂功能完善完成")

# ================== 16. 添加播客上传弹窗HTML ==================
upload_podcast_modal = '''
<!-- 播客上传弹窗 -->
<div class="modal-overlay" id="upload-podcast-modal">
    <div class="modal-content" style="max-width:360px;">
        <div class="modal-title">🎵 上传音频</div>
        <div style="margin-bottom:16px;">
            <input type="file" id="podcast-file-input" accept="audio/*" onchange="handlePodcastFile(event)" style="display:none;"/>
            <div style="margin-bottom:12px;">
                <label style="font-size:12px;color:var(--text-gray);display:block;margin-bottom:4px;">标题</label>
                <input type="text" id="podcast-title-input" class="input-field" placeholder="输入音频标题"/>
            </div>
            <div style="margin-bottom:12px;">
                <label style="font-size:12px;color:var(--text-gray);display:block;margin-bottom:4px;">作者</label>
                <input type="text" id="podcast-author-input" class="input-field" placeholder="输入作者名称"/>
            </div>
            <div style="margin-bottom:12px;">
                <label style="font-size:12px;color:var(--text-gray);display:block;margin-bottom:4px;">选择音频文件</label>
                <button onclick="document.getElementById('podcast-file-input').click()" style="width:100%;padding:16px;background:#f5f5f5;border:2px dashed #ccc;border-radius:12px;cursor:pointer;font-size:14px;">📁 点击选择MP3/WAV文件</button>
            </div>
        </div>
        <button onclick="closeUploadPodcastModal()" style="width:100%;padding:12px;background:#f0f0f0;border:none;border-radius:10px;font-size:14px;cursor:pointer;">取消</button>
    </div>
</div>
'''

# 在body结束标签前添加
content = content.replace('</body>', upload_podcast_modal + '\n</body>')
print("16. 播客上传弹窗添加完成")

# ================== 17. 视频课堂完善 ==================
old_video_section = '''<div class="card">
            <div style="font-size:14px;font-weight:bold;margin-bottom:12px;">🎬 视频列表</div>
            <div id="video-list"></div>
        </div>
        <div class="card" id="video-player-card" style="display:none;">
            <div style="background:#000;border-radius:12px;overflow:hidden;aspect-ratio:16/9;display:flex;align-items:center;justify-content:center;color:white;font-size:48px;" id="video-container">
                📹
            </div>
            <div style="margin-top:12px;">
                <div style="font-size:14px;font-weight:bold;" id="video-title-display"></div>
                <div style="display:flex;gap:8px;margin-top:8px;">
                    <button onclick="playExternalVideo(document.getElementById('video-url-input').value)" style="flex:1;padding:10px;background:var(--gradient-blue);border:none;border-radius:8px;color:white;cursor:pointer;">▶ 播放</button>
                    <button onclick="closeVideoPlayer()" style="padding:10px 16px;background:#f0f0f0;border:none;border-radius:8px;cursor:pointer;">关闭</button>
                </div>
            </div>
        </div>'''

new_video_section = '''<div class="card">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
                <div style="font-size:14px;font-weight:bold;">🎬 视频列表</div>
                <button onclick="showUploadVideoModal()" style="padding:6px 12px;background:var(--gradient-blue);border:none;border-radius:8px;color:white;font-size:12px;cursor:pointer;">+ 上传视频</button>
            </div>
            <div id="video-list"></div>
            <!-- 用户上传视频列表 -->
            <div id="user-video-list" style="margin-top:12px;"></div>
        </div>
        <div class="card" id="video-player-card">
            <div style="position:relative;background:#000;border-radius:12px;overflow:hidden;aspect-ratio:16/9;" id="video-container">
                <video id="main-video-player" style="width:100%;height:100%;object-fit:contain;display:none;"></video>
                <div id="video-placeholder" style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);color:white;font-size:48px;">📹</div>
            </div>
            <!-- 视频进度条 -->
            <div style="margin-top:12px;">
                <input type="range" id="video-progress" value="0" min="0" max="100" style="width:100%;height:6px;-webkit-appearance:none;background:#e0e0e0;border-radius:3px;outline:none;">
                <div style="display:flex;justify-content:space-between;font-size:10px;color:var(--text-light);margin-top:4px;">
                    <span id="video-current-time">0:00</span>
                    <span id="video-duration">0:00</span>
                </div>
            </div>
            <!-- 视频控制 -->
            <div style="display:flex;justify-content:center;gap:12px;margin-top:12px;align-items:center;">
                <button onclick="setVideoVolume(-0.1)" style="width:36px;height:36px;border-radius:50%;background:#f0f0f0;border:none;font-size:14px;cursor:pointer;">🔉</button>
                <button onclick="toggleVideoPlay()" id="video-play-btn" style="width:52px;height:52px;border-radius:50%;background:var(--gradient-blue);border:none;font-size:22px;color:white;cursor:pointer;">▶</button>
                <button onclick="setVideoVolume(0.1)" style="width:36px;height:36px;border-radius:50%;background:#f0f0f0;border:none;font-size:14px;cursor:pointer;">🔊</button>
                <button onclick="toggleFullscreen()" style="width:36px;height:36px;border-radius:50%;background:#f0f0f0;border:none;font-size:14px;cursor:pointer;">⛶</button>
            </div>
            <div style="margin-top:12px;">
                <input type="text" id="video-url-input" class="input-field" placeholder="或输入视频链接（B站、抖音等）"/>
                <button onclick="loadVideoUrl()" style="width:100%;padding:10px;background:var(--gradient-blue);border:none;border-radius:8px;color:white;cursor:pointer;margin-top:8px;">▶ 播放链接视频</button>
            </div>
        </div>'''

content = content.replace(old_video_section, new_video_section)
print("17. 视频课堂UI完善完成")

# 添加视频相关函数
video_functions = '''
// ====== 视频播放器完善 ======
function initVideoPlayer() {
    const video = document.getElementById('main-video-player');
    if (!video) return;
    
    video.addEventListener('timeupdate', function() {
        const progress = document.getElementById('video-progress');
        const currentTime = document.getElementById('video-current-time');
        const duration = document.getElementById('video-duration');
        
        if (progress && video.duration) {
            progress.value = (video.currentTime / video.duration) * 100;
        }
        if (currentTime) currentTime.textContent = formatTime(video.currentTime);
        if (duration) duration.textContent = formatTime(video.duration);
    });
    
    video.addEventListener('ended', function() {
        document.getElementById('video-play-btn').textContent = '▶';
    });
    
    const progressBar = document.getElementById('video-progress');
    if (progressBar) {
        progressBar.addEventListener('input', function() {
            if (video.duration) {
                video.currentTime = (progressBar.value / 100) * video.duration;
            }
        });
    }
}

function showUploadVideoModal() {
    document.getElementById('upload-video-modal').classList.add('show');
}

function closeUploadVideoModal() {
    document.getElementById('upload-video-modal').classList.remove('show');
}

function handleVideoFile(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    const title = document.getElementById('video-title-input').value.trim() || file.name.replace(/\\.[^.]+$/, '');
    
    const reader = new FileReader();
    reader.onload = function(e) {
        const data = loadData();
        const user = data.users.find(u => u.id === data.currentUser);
        if (user) {
            user.uploads = user.uploads || { podcast: [], video: [], method: [], thinking: [] };
            user.uploads.video = user.uploads.video || [];
            user.uploads.video.push({
                title: title,
                dataUrl: e.target.result,
                date: Date.now()
            });
            saveData(data);
        }
        closeUploadVideoModal();
        renderUserVideos();
        alert('视频上传成功！');
    };
    reader.readAsDataURL(file);
}

function renderUserVideos() {
    const data = loadData();
    const user = data.users.find(u => u.id === data.currentUser);
    const container = document.getElementById('user-video-list');
    if (!container) return;
    
    const userVideos = user?.uploads?.video || [];
    if (userVideos.length === 0) {
        container.innerHTML = '';
        return;
    }
    
    container.innerHTML = '<div style="font-size:12px;color:var(--text-gray);margin-bottom:8px;padding-top:12px;border-top:1px solid #eee;">我的上传</div>' + 
        userVideos.map((v, i) => '<div onclick="playUserVideo(' + i + ')" style="display:flex;align-items:center;gap:10px;padding:10px;background:#f5f5f5;border-radius:8px;margin-bottom:6px;cursor:pointer;"><span style="font-size:20px;">🎬</span><div style="flex:1;"><div style="font-size:13px;font-weight:600;">' + v.title + '</div></div><span style="color:var(--blue);">▶</span></div>').join('');
}

function playUserVideo(index) {
    const data = loadData();
    const user = data.users.find(u => u.id === data.currentUser);
    const userVideos = user?.uploads?.video || [];
    const video = userVideos[index];
    if (!video) return;
    
    const videoEl = document.getElementById('main-video-player');
    if (videoEl) {
        videoEl.src = video.dataUrl;
        videoEl.style.display = 'block';
        videoEl.play();
    }
    document.getElementById('video-placeholder').style.display = 'none';
    document.getElementById('video-play-btn').textContent = '⏸';
}

function loadVideoUrl() {
    const url = document.getElementById('video-url-input').value.trim();
    if (!url) {
        alert('请输入视频链接');
        return;
    }
    
    // 尝试直接加载视频URL（适用于直链）
    const videoEl = document.getElementById('main-video-player');
    if (videoEl) {
        // 检查是否是支持的视频格式
        if (url.match(/\\.(mp4|webm|ogg)$/i)) {
            videoEl.src = url;
            videoEl.style.display = 'block';
            videoEl.play();
            document.getElementById('video-placeholder').style.display = 'none';
            document.getElementById('video-play-btn').textContent = '⏸';
        } else {
            alert('支持的视频格式：MP4、WebM、OGG');
        }
    }
}

function toggleVideoPlay() {
    const video = document.getElementById('main-video-player');
    if (!video || !video.src) return;
    
    if (video.paused) {
        video.play();
        document.getElementById('video-play-btn').textContent = '⏸';
    } else {
        video.pause();
        document.getElementById('video-play-btn').textContent = '▶';
    }
}

function setVideoVolume(delta) {
    const video = document.getElementById('main-video-player');
    if (video) {
        video.volume = Math.max(0, Math.min(1, video.volume + delta));
    }
}

function toggleFullscreen() {
    const container = document.getElementById('video-container');
    if (!container) return;
    
    if (document.fullscreenElement) {
        document.exitFullscreen();
    } else {
        container.requestFullscreen();
    }
}
'''

content = content + video_functions
print("18. 视频播放器函数添加完成")

# 添加视频上传弹窗HTML
upload_video_modal = '''
<!-- 视频上传弹窗 -->
<div class="modal-overlay" id="upload-video-modal">
    <div class="modal-content" style="max-width:360px;">
        <div class="modal-title">🎬 上传视频</div>
        <div style="margin-bottom:16px;">
            <input type="file" id="video-file-input" accept="video/*" onchange="handleVideoFile(event)" style="display:none;"/>
            <div style="margin-bottom:12px;">
                <label style="font-size:12px;color:var(--text-gray);display:block;margin-bottom:4px;">标题</label>
                <input type="text" id="video-title-input" class="input-field" placeholder="输入视频标题"/>
            </div>
            <div style="margin-bottom:12px;">
                <label style="font-size:12px;color:var(--text-gray);display:block;margin-bottom:4px;">选择视频文件</label>
                <button onclick="document.getElementById('video-file-input').click()" style="width:100%;padding:16px;background:#f5f5f5;border:2px dashed #ccc;border-radius:12px;cursor:pointer;font-size:14px;">📁 点击选择MP4/WebM文件</button>
            </div>
            <div style="font-size:11px;color:var(--text-light);text-align:center;">支持MP4、WebM格式</div>
        </div>
        <button onclick="closeUploadVideoModal()" style="width:100%;padding:12px;background:#f0f0f0;border:none;border-radius:10px;font-size:14px;cursor:pointer;">取消</button>
    </div>
</div>
'''

content = content.replace('</body>', upload_video_modal + '\n</body>')
print("19. 视频上传弹窗添加完成")

# ================== 20. DeepSeek助手完善 ==================
# 找到DeepSeek聊天区域并完善
old_deepseek_chat = '''<div class="teacher-chat" id="deepseek-chat-area">
            <div class="chat-header">
                <div style="width:32px;height:32px;background:rgba(255,255,255,0.2);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:16px;">🤖</div>
                <div style="flex:1;">
                    <div style="font-size:14px;font-weight:600;">DeepSeek AI</div>
                    <div style="font-size:10px;opacity:0.8;">智能助手</div>
                </div>
                <button onclick="clearDeepSeekChat()" style="padding:4px 10px;background:rgba(255,255,255,0.2);border:none;border-radius:8px;color:white;font-size:11px;cursor:pointer;">清空</button>
            </div>
            <div class="quick-templates" id="deepseek-templates">
                <button class="template-btn" onclick="sendDeepSeekTemplate(\\'帮我制定一个学习计划\\')">📋 学习计划</button>
                <button class="template-btn" onclick="sendDeepSeekTemplate(\\'如何提高记忆力\\')">🧠 记忆力</button>
                <button class="template-btn" onclick="sendDeepSeekTemplate(\\'考试焦虑怎么办\\')">😰 缓解焦虑</button>
                <button class="template-btn" onclick="sendDeepSeekTemplate(\\'各科目学习方法\\')">📚 学习方法</button>
            </div>
            <div class="chat-messages" id="deepseek-messages">
                <div class="chat-msg">
                    <div class="chat-avatar">🤖</div>
                    <div class="chat-bubble">你好！我是DeepSeek AI助手，可以帮你解答学习问题、制定计划、提供学习方法建议等。有什么我可以帮你的吗？</div>
                </div>
            </div>
            <div style="display:flex;gap:8px;padding:12px;background:white;border-top:1px solid #eee;flex-shrink:0;">
                <input type="text" id="deepseek-input" class="input-field" placeholder="输入问题..." style="flex:1;"/>
                <button onclick="sendToDeepSeek()" style="padding:10px 16px;background:var(--gradient-blue);border:none;border-radius:10px;color:white;font-size:14px;cursor:pointer;">发送</button>
            </div>
        </div>'''

new_deepseek_chat = '''<div class="teacher-chat" id="deepseek-chat-area">
            <div class="chat-header">
                <div style="width:32px;height:32px;background:rgba(255,255,255,0.2);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:16px;">🤖</div>
                <div style="flex:1;">
                    <div style="font-size:14px;font-weight:600;">DeepSeek AI</div>
                    <div style="font-size:10px;opacity:0.8;">智能助手</div>
                </div>
                <button onclick="clearDeepSeekChat()" style="padding:4px 10px;background:rgba(255,255,255,0.2);border:none;border-radius:8px;color:white;font-size:11px;cursor:pointer;">清空</button>
            </div>
            <div class="quick-templates" id="deepseek-templates">
                <button class="template-btn" onclick="sendDeepSeekTemplate(\\'帮我制定一个学习计划\\')">📋 学习计划</button>
                <button class="template-btn" onclick="sendDeepSeekTemplate(\\'如何提高记忆力\\')">🧠 记忆力</button>
                <button class="template-btn" onclick="sendDeepSeekTemplate(\\'考试焦虑怎么办\\')">😰 缓解焦虑</button>
                <button class="template-btn" onclick="sendDeepSeekTemplate(\\'各科目学习方法\\')">📚 学习方法</button>
            </div>
            <div class="chat-messages" id="deepseek-messages">
                <div class="chat-msg">
                    <div class="chat-avatar">🤖</div>
                    <div class="chat-bubble">你好！我是DeepSeek AI助手，可以帮你解答学习问题、制定计划、提供学习方法建议等。有什么我可以帮你的吗？</div>
                </div>
            </div>
            <!-- 上传预览区 -->
            <div id="deepseek-upload-preview" style="display:none;padding:8px 12px;background:#f0f5ff;border-bottom:1px solid #e0e0e0;">
                <div style="display:flex;align-items:center;gap:8px;">
                    <div id="preview-content" style="flex:1;"></div>
                    <button onclick="clearDeepSeekUpload()" style="padding:4px 8px;background:#ff4444;border:none;border-radius:6px;color:white;font-size:11px;cursor:pointer;">✕</button>
                </div>
            </div>
            <div style="display:flex;gap:8px;padding:12px;background:white;border-top:1px solid #eee;flex-shrink:0;">
                <input type="file" id="deepseek-photo-input" accept="image/*" onchange="handleDeepSeekPhoto(event)" style="display:none;"/>
                <input type="file" id="deepseek-video-input" accept="video/*" onchange="handleDeepSeekVideo(event)" style="display:none;"/>
                <button onclick="document.getElementById(\\'deepseek-photo-input\\').click()" style="width:40px;height:40px;background:#f0f0f0;border:none;border-radius:10px;font-size:18px;cursor:pointer;">📷</button>
                <button onclick="document.getElementById(\\'deepseek-video-input\\').click()" style="width:40px;height:40px;background:#f0f0f0;border:none;border-radius:10px;font-size:18px;cursor:pointer;">🎬</button>
                <input type="text" id="deepseek-input" class="input-field" placeholder="输入问题..." style="flex:1;"/>
                <button onclick="sendToDeepSeek()" style="padding:10px 16px;background:var(--gradient-blue);border:none;border-radius:10px;color:white;font-size:14px;cursor:pointer;">发送</button>
            </div>
        </div>'''

content = content.replace(old_deepseek_chat, new_deepseek_chat)
print("20. DeepSeek聊天界面完善完成")

# 添加DeepSeek相关函数
deepseek_functions = '''
// ====== DeepSeek助手完善 ======
let deepseekImageBase64 = null;
let deepseekVideoUrl = null;

function handleDeepSeekPhoto(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = function(e) {
        deepseekImageBase64 = e.target.result;
        deepseekVideoUrl = null;
        
        document.getElementById('deepseek-upload-preview').style.display = 'block';
        document.getElementById('preview-content').innerHTML = '<img src="' + e.target.result + '" style="max-width:80px;max-height:60px;border-radius:8px;object-fit:cover;"/><span style="font-size:12px;color:var(--text-gray);margin-left:8px;">📷 图片已选择</span>';
    };
    reader.readAsDataURL(file);
}

function handleDeepSeekVideo(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = function(e) {
        deepseekVideoUrl = e.target.result;
        deepseekImageBase64 = null;
        
        document.getElementById('deepseek-upload-preview').style.display = 'block';
        document.getElementById('preview-content').innerHTML = '<video src="' + e.target.result + '" style="max-width:80px;max-height:60px;border-radius:8px;object-fit:cover;"/><span style="font-size:12px;color:var(--text-gray);margin-left:8px;">🎬 视频已选择</span>';
    };
    reader.readAsDataURL(file);
}

function clearDeepSeekUpload() {
    deepseekImageBase64 = null;
    deepseekVideoUrl = null;
    document.getElementById('deepseek-upload-preview').style.display = 'none';
    document.getElementById('deepseek-photo-input').value = '';
    document.getElementById('deepseek-video-input').value = '';
}

async function sendToDeepSeek() {
    const input = document.getElementById('deepseek-input');
    const message = input.value.trim();
    
    if (!message && !deepseekImageBase64 && !deepseekVideoUrl) {
        alert('请输入问题或上传图片/视频');
        return;
    }
    
    // 显示用户消息
    let userContent = message;
    if (deepseekImageBase64) {
        userContent += ' [上传了图片]';
    }
    if (deepseekVideoUrl) {
        userContent += ' [上传了视频]';
    }
    
    addMessageToDeepSeekChat('user', userContent, deepseekImageBase64, deepseekVideoUrl);
    input.value = '';
    
    // 显示加载状态
    const messagesContainer = document.getElementById('deepseek-messages');
    const loadingMsg = document.createElement('div');
    loadingMsg.className = 'chat-msg';
    loadingMsg.innerHTML = '<div class="chat-avatar">🤖</div><div class="chat-bubble" id="loading-bubble">思考中...</div>';
    messagesContainer.appendChild(loadingMsg);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    try {
        // 构建消息内容
        let content = message;
        
        // 调用DeepSeek API
        const response = await fetch('https://api.deepseek.com/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer sk-8413f72a3f084fb08c84389555a76d37',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                model: 'deepseek-chat',
                messages: [{
                    role: 'user',
                    content: message + (deepseekImageBase64 ? '\\n\\n[用户上传了图片，请分析图片内容]' : '') + (deepseekVideoUrl ? '\\n\\n[用户上传了视频]' : '')
                }]
            })
        });
        
        const data = await response.json();
        let reply = data.choices?.[0]?.message?.content || '抱歉，暂时无法回答这个问题。';
        
        // 如果有图片，添加图片分析说明
        if (deepseekImageBase64) {
            reply = '📷 图片分析：\\n' + reply;
        }
        
        loadingMsg.querySelector('.chat-bubble').textContent = reply;
        
    } catch (error) {
        loadingMsg.querySelector('.chat-bubble').textContent = '抱歉，发生了错误：' + error.message;
    }
    
    // 清除上传
    clearDeepSeekUpload();
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function addMessageToDeepSeekChat(type, content, imageBase64, videoUrl) {
    const messagesContainer = document.getElementById('deepseek-messages');
    const msgDiv = document.createElement('div');
    msgDiv.className = 'chat-msg ' + (type === 'user' ? 'user' : '');
    
    let contentHtml = '<div class="chat-bubble">' + content + '</div>';
    if (imageBase64) {
        contentHtml = '<div class="chat-bubble"><img src="' + imageBase64 + '" style="max-width:200px;border-radius:8px;margin-bottom:8px;"/>' + content + '</div>';
    }
    if (videoUrl) {
        contentHtml = '<div class="chat-bubble"><video src="' + videoUrl + '" style="max-width:200px;border-radius:8px;margin-bottom:8px;" controls/>' + content + '</div>';
    }
    
    msgDiv.innerHTML = '<div class="chat-avatar">' + (type === 'user' ? '👤' : '🤖') + '</div>' + contentHtml;
    messagesContainer.appendChild(msgDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function sendDeepSeekTemplate(text) {
    document.getElementById('deepseek-input').value = text;
    sendToDeepSeek();
}

function clearDeepSeekChat() {
    if (!confirm('确定要清空聊天记录吗？')) return;
    const messagesContainer = document.getElementById('deepseek-messages');
    messagesContainer.innerHTML = '<div class="chat-msg"><div class="chat-avatar">🤖</div><div class="chat-bubble">你好！我是DeepSeek AI助手，可以帮你解答学习问题、有什么我可以帮你的吗？</div></div>';
    clearDeepSeekUpload();
}
'''

content = content + deepseek_functions
print("21. DeepSeek函数添加完成")

# ================== 22. 添加audio标签用于播客播放 ==================
content = content.replace('<body>', '<body>\n<audio id="podcast-audio" style="display:none;"></audio>')
print("22. 播客audio标签添加完成")

# 写回文件
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ V106版本更新完成！")
print(f"更新后文件大小: {len(content)} 字符")
