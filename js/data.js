// 数据定义文件

// 母题数据
const topics = {
    grade5_math: [
        { id: 'g5m1', title: '小数加减法', difficulty: '基础', icon: '📊', question: '计算：3.25 + 1.78', solution: '5.03' },
        { id: 'g5m2', title: '小数乘法', difficulty: '基础', icon: '📈', question: '计算：0.5 × 0.4', solution: '0.20' },
        { id: 'g5m3', title: '三角形面积', difficulty: '进阶', icon: '🔺', question: '底6cm高4cm', solution: '12cm²' }
    ],
    grade5_chinese: [
        { id: 'g5c1', title: '古诗词默写', difficulty: '基础', icon: '📜', question: '静夜思', solution: '举头望明月' }
    ],
    grade5_english: [
        { id: 'g5e1', title: '基数词', difficulty: '基础', icon: '🔢', question: '15用英语怎么说', solution: 'fifteen' }
    ],
    grade7_math: [
        { id: 'g7m1', title: '有理数加法', difficulty: '基础', icon: '➕', question: '(-3) + (+7)', solution: '+4' }
    ],
    grade7_chinese: [
        { id: 'g7c1', title: '文言文实词', difficulty: '基础', icon: '📜', question: '学而时习之', solution: '按时学习' }
    ],
    grade7_english: [
        { id: 'g7e1', title: 'be动词', difficulty: '基础', icon: '📝', question: 'I ___ a student', solution: 'am' }
    ]
};

// 播客数据
const podcastData = {
    method: [
        { title: '高效学习秘诀', duration: 900, icon: '🎧', author: '学习方法专家' },
        { title: '记忆力提升', duration: 1200, icon: '🧠', author: '记忆训练师' }
    ],
    knowledge: [
        { title: '数学思维导图', duration: 1500, icon: '📐', author: '数学名师' }
    ]
};

// 老师数据
const teachers = {
    math: { name: '赵老师', icon: '📐', subject: '数学' },
    chinese: { name: '李老师', icon: '📝', subject: '语文' },
    english: { name: '王老师', icon: '📖', subject: '英语' }
};

// 状态变量
let currentPodcastCategory = 'method';
let currentAudioIndex = 0;
