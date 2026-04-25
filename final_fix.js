const fs = require('fs');

let content = fs.readFileSync('index.html', 'utf8');

// 方法1: 直接用正则替换修复 methodDetails
// 找到 methodDetails 对象并替换

// 替换整个 methodDetails 对象
const correctMethodDetails = `const methodDetails = {
    feyman: {title:'🧠 费曼学习法',desc:'把学到的知识用自己的话讲给别人听，如果别人能听懂，说明你真正掌握了。',steps:['选择一个你想要理解的概念','想象你要把这个概念教给一个完全不懂的人','如果讲解过程中卡住了，就回顾原始材料','用自己的话重新组织，确保通俗易懂'],tip:'💡 最佳实践：每天用费曼学习法复习一个知识点，坚持21天形成习惯。'},
    pomodoro: {title:'⏰ 番茄工作法',desc:'25分钟专注学习，5分钟休息，循环进行，提高效率。',steps:['选择一个待完成的任务','设定25分钟倒计时（一个番茄钟）','专注工作，中途不做其他事','计时结束后休息5分钟','每4个番茄钟后休息15-30分钟'],tip:'💡 建议：使用手机闹钟或专门的番茄钟APP来计时。'},
    ebbinghaus: {title:'🔄 艾宾浩斯记忆法',desc:'学习后1天、3天、7天、14天、30天分别复习，加深长期记忆。',steps:['初次学习新知识','24小时后进行第一次复习','3天后再复习一次','7天后第三次复习','14天后第四次复习','30天后最后一次复习'],tip:'💡 关键：严格按照时间节点复习，不要偷懒！'},
    mindmap: {title:'🎨 思维导图法',desc:'用图形和关键词将知识点连接起来，形成系统化的知识结构。',steps:['在纸中央写下核心主题','从中心向外画出主分支','在每个主分支写上关键词','从关键词继续延伸子分支','用不同颜色区分不同主题','添加图标和符号增强记忆'],tip:'💡 工具推荐：可以使用XMind、幕布等软件制作数字思维导图。'},
    cornell: {title:'📝 康奈尔笔记法',desc:'将笔记分为要点、线索、总结三个区域，提高复习效率。',steps:['把笔记页面分为三部分','右侧大的区域记录主要内容','左侧区域记录提示词/关键词','底部区域写总结和问题','用笔记时遮住右侧，回忆内容','用总结区进行自测'],tip:'💡 最佳使用场景：课堂笔记、读书笔记、讲座记录。'},
    timeManagement: {title:'⏱️ 时间管理法',desc:'合理安排学习时间，提高学习效率。',steps:['列出所有待办事项','按重要性和紧急性分类','设定每个任务的完成时间','使用番茄工作法保持专注','定期回顾和调整计划'],tip:'💡 建议：每天晚上规划第二天的任务，早上执行最重要的任务。'},
    noteTaking: {title:'📒 高效笔记法',desc:'科学记笔记，让学习更高效。',steps:['使用简洁的语言和缩写','用颜色区分重点内容','建立层次分明的结构','课后及时整理和补充','定期回顾和更新笔记'],tip:'💡 工具推荐：印象笔记、有道云笔记、Notion等。'},
    testStrategy: {title:'📝 考试策略',desc:'科学应考，减少失误，提高成绩。',steps:['先浏览试卷，了解题量和难度','按先易后难的顺序答题','遇到难题先跳过，不要卡住','留出时间检查会的题','注意答题规范和卷面整洁'],tip:'💡 关键：保持平和心态，相信自己的第一判断。'},
    sq3r: {title:'📖 SQ3R阅读法',desc:'Survey泛读、Question提问、Read阅读、Recite复述、Review复习。',steps:['Survey（泛读）：快速浏览标题、目录、图表','Question（提问）：写下你想知道的问题','Read（阅读）：仔细阅读章节内容','Recite（复述）：合上书复述要点','Review（复习）：定期回顾已读内容'],tip:'💡 适合：教科书、论文、长篇文章的阅读。'}
};`;

// 使用正则表达式找到并替换 methodDetails
const pattern = /const methodDetails = \{[\s\S]*?\};/;
if (pattern.test(content)) {
    content = content.replace(pattern, correctMethodDetails);
    console.log('✅ 已修复 methodDetails');
} else {
    console.log('⚠️ 未找到 methodDetails');
}

// 修复2: 删除重复的 podcastList（从第二个开始）
const lines = content.split('\n');
let newLines = [];
let skipUntilPodcastEnd = false;
let podcastBracketCount = 0;

for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const lineNum = i + 1;
    
    // 找到第二个 podcastList 开始（跳过第一个）
    if (line.trim().startsWith('const podcastList = [') && lineNum > 600) {
        skipUntilPodcastEnd = true;
        podcastBracketCount = 0;
        console.log(`跳过第 ${lineNum} 行开始的重复 podcastList`);
        continue;
    }
    
    if (skipUntilPodcastEnd) {
        podcastBracketCount += (line.match(/\[/g) || []).length;
        podcastBracketCount -= (line.match(/\]/g) || []).length;
        
        if (podcastBracketCount <= 0 && (line.includes('];') || line.includes('];'))) {
            skipUntilPodcastEnd = false;
            console.log(`结束跳过 podcastList 在第 ${lineNum} 行`);
        }
        continue;
    }
    
    newLines.push(line);
}

content = newLines.join('\n');

// 修复3: 删除重复的 methodTraining
content = content.replace(
    /const methodTraining = methodTrainingQuestions;\s*\n\s*function getMethodTraining[\s\S]*?const methodTraining = methodTrainingQuestions;\s*\n/g,
    'const methodTraining = methodTrainingQuestions;\n\nfunction getMethodTraining'
);

fs.writeFileSync('index.html', content);
console.log('✅ 最终修复完成');
