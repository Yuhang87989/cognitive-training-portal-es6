// 母题训练模块

let currentGradeTab = 'grade5';
let currentSubjectTab = 'math';
let currentTopicPage = 1;
const TOPICS_PER_PAGE = 10;

function switchGradeTab(grade, el) {
    currentGradeTab = grade;
    document.querySelectorAll('.grade-tab-btn').forEach(b => b.classList.remove('active'));
    if (el) el.classList.add('active');
    renderTopics();
}

function switchTopicTab(subject, el) {
    currentSubjectTab = subject;
    document.querySelectorAll('.tab-item').forEach(t => t.classList.remove('active'));
    if (el) el.classList.add('active');
    document.querySelectorAll('.topic-list').forEach(l => l.style.display = 'none');
    const list = document.getElementById('topic-list-' + subject);
    if (list) list.style.display = 'block';
    renderTopics();
}

function renderTopics() {
    const topicKey = currentGradeTab + '_' + currentSubjectTab;
    const topicList = topics[topicKey] || [];
    const container = document.getElementById('topic-list-' + currentSubjectTab);
    
    if (!container) return;
    
    if (!topicList.length) {
        container.innerHTML = '<div style="text-align:center;padding:40px;color:#999;">暂无题目</div>';
        return;
    }
    
    let html = '';
    topicList.forEach((t, i) => {
        html += '<div class="topic-item" onclick="showTopicDetail(' + i + ')">';
        html += '<span>' + t.icon + '</span>';
        html += '<div><div style="font-weight:600;">' + t.title + '</div>';
        html += '<div style="font-size:12px;color:#999;">' + t.difficulty + '</div></div></div>';
    });
    container.innerHTML = html;
}

function showTopicDetail(index) {
    const topicKey = currentGradeTab + '_' + currentSubjectTab;
    const topic = topics[topicKey][index];
    if (!topic) return;
    
    alert('题目：' + topic.question + '\n答案：' + topic.solution);
}
