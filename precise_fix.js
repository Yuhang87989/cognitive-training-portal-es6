const fs = require('fs');

let content = fs.readFileSync('index.html', 'utf8');
let lines = content.split('\n');
let newLines = [];

console.log('开始精确修复...');

// 修复1: 删除第646-698行的重复 podcastList
console.log('\n1. 修复重复的 podcastList...');
let inDuplicatePodcast = false;
let podcastBrackets = 0;

for (let i = 0; i < lines.length; i++) {
    const lineNum = i + 1;
    const line = lines[i];
    
    // 找到第二个 podcastList 开始
    if (line.trim().startsWith('const podcastList = [') && lineNum > 620) {
        inDuplicatePodcast = true;
        podcastBrackets = 0;
        console.log(`   开始跳过第 ${lineNum} 行的重复 podcastList`);
        continue;
    }
    
    if (inDuplicatePodcast) {
        podcastBrackets += (line.match(/\[/g) || []).length;
        podcastBrackets -= (line.match(/\]/g) || []).length;
        
        if (podcastBrackets <= 0 && line.includes('];')) {
            inDuplicatePodcast = false;
            console.log(`   结束跳过第 ${lineNum} 行`);
            continue;
        }
    }
    
    newLines.push(line);
}

// 修复2: 删除第3038行的重复 methodTraining
console.log('\n2. 修复重复的 methodTraining...');
lines = newLines;
newLines = [];

for (let i = 0; i < lines.length; i++) {
    const lineNum = i + 1;
    const line = lines[i];
    
    // 跳过第二个 methodTraining 声明
    if (line.trim() === 'const methodTraining = methodTrainingQuestions;' && lineNum > 3020) {
        console.log(`   跳过第 ${lineNum} 行的重复 methodTraining`);
        continue;
    }
    
    newLines.push(line);
}

// 修复3: 修复 methodDetails 对象
console.log('\n3. 修复 methodDetails 对象...');
content = newLines.join('\n');
lines = content.split('\n');
newLines = [];

let methodDetailsStart = -1;
let methodDetailsEnd = -1;
let braceCount = 0;
let inMethodDetails = false;
let afterClosing = false;

for (let i = 0; i < lines.length; i++) {
    const lineNum = i + 1;
    const line = lines[i];
    
    if (line.includes('const methodDetails = {')) {
        methodDetailsStart = lineNum;
        inMethodDetails = true;
    }
    
    if (inMethodDetails) {
        braceCount += (line.match(/\{/g) || []).length;
        braceCount -= (line.match(/\}/g) || []).length;
        
        if (braceCount === 0 && line.includes('};')) {
            inMethodDetails = false;
            methodDetailsEnd = lineNum;
            afterClosing = true;
            newLines.push(line);
            continue;
        }
        
        // 如果在闭合后还有内容，检查是否需要添加 sq3r
        if (afterClosing && line.includes('sq3r:')) {
            // sq3r 已经在后面，不需要处理
            afterClosing = false;
        }
    }
    
    newLines.push(line);
}

// 检查 methodDetails 是否有 sq3r
content = newLines.join('\n');
if (!content.includes('sq3r:') || content.indexOf('sq3r:') > content.indexOf('function showMethodDetail')) {
    console.log('   需要添加 sq3r 到 methodDetails');
    // 找到 methodDetails 闭合大括号的位置
    lines = content.split('\n');
    newLines = [];
    
    for (let i = 0; i < lines.length; i++) {
        const lineNum = i + 1;
        const line = lines[i];
        newLines.push(line);
        
        // 在 methodDetails 的闭合大括号前添加 sq3r
        if (line.includes('testStrategy:') && line.includes('};')) {
            const sq3rLine = "    sq3r: {title:'📖 SQ3R阅读法',desc:'Survey泛读、Question提问、Read阅读、Recite复述、Review复习。',steps:['Survey（泛读）：快速浏览标题、目录、图表','Question（提问）：写下你想知道的问题','Read（阅读）：仔细阅读章节内容','Recite（复述）：合上书复述要点','Review（复习）：定期回顾已读内容'],tip:'💡 适合：教科书、论文、长篇文章的阅读。'}";
            newLines.push(sq3rLine);
            console.log(`   在第 ${lineNum} 行后添加了 sq3r`);
        }
    }
}

content = newLines.join('\n');
fs.writeFileSync('index.html', content);
console.log('\n✅ 精确修复完成');
