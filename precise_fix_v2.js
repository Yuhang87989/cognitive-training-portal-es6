const fs = require('fs');

let content = fs.readFileSync('index.html', 'utf8');
let lines = content.split('\n');
let newLines = [];
let skipMode = null;
let skipStart = 0;
let skipEnd = 0;

console.log('开始修复...');

for (let i = 0; i < lines.length; i++) {
    const lineNum = i + 1;
    const line = lines[i];
    
    // 1. 跳过第646-668行（重复的 podcastList）
    if (lineNum >= 646 && lineNum <= 668) {
        if (lineNum === 646) console.log(`跳过重复 podcastList: 第${lineNum}-668行`);
        continue;
    }
    
    // 2. 跳过第3038行（重复的 methodTraining）
    if (lineNum === 3038) {
        console.log(`跳过重复 methodTraining: 第${lineNum}行`);
        continue;
    }
    
    // 3. 修复 methodDetails: 删除 2997-3003 行之间重复的属性（在闭合大括号后）
    if (lineNum >= 2997 && lineNum <= 3003 && line.includes(':')) {
        console.log(`跳过 methodDetails 重复属性: 第${lineNum}行`);
        continue;
    }
    
    // 4. 修复 methodDetails: 删除 3010-3016 行之间重复的属性
    if (lineNum >= 3010 && lineNum <= 3016 && line.includes(':')) {
        console.log(`跳过 methodDetails 重复属性: 第${lineNum}行`);
        continue;
    }
    
    newLines.push(line);
}

// 5. 修复 methodDetails: 确保 sq3r 在闭合大括号内
// 找到 methodDetails 闭合大括号，在其前添加 sq3r（如果没有的话）
let methodDetailsEndLine = -1;
let hasSq3r = false;

for (let i = 0; i < newLines.length; i++) {
    if (newLines[i].includes('testStrategy:') && newLines[i].includes('};')) {
        methodDetailsEndLine = i;
    }
    if (newLines[i].includes('sq3r:')) {
        hasSq3r = true;
    }
}

if (methodDetailsEndLine > 0 && !hasSq3r) {
    const sq3rLine = "    sq3r: {title:'📖 SQ3R阅读法',desc:'Survey泛读、Question提问、Read阅读、Recite复述、Review复习。',steps:['Survey（泛读）：快速浏览标题、目录、图表','Question（提问）：写下你想知道的问题','Read（阅读）：仔细阅读章节内容','Recite（复述）：合上书复述要点','Review（复习）：定期回顾已读内容'],tip:'💡 适合：教科书、论文、长篇文章的阅读。'}";
    newLines.splice(methodDetailsEndLine, 0, sq3rLine);
    console.log(`在第${methodDetailsEndLine+1}行后添加了 sq3r`);
}

// 删除闭合大括号后多余的空行和重复内容
let cleanLines = [];
let skipNextEmpty = false;

for (let i = 0; i < newLines.length; i++) {
    const line = newLines[i];
    const lineNum = i + 1;
    
    // 跳过闭合大括号后的空行（直到 sq3r 或函数定义）
    if (line.trim() === '' && i > methodDetailsEndLine && i < methodDetailsEndLine + 5) {
        if (newLines[i+1] && !newLines[i+1].includes('sq3r') && !newLines[i+1].includes('function')) {
            continue;
        }
    }
    
    cleanLines.push(line);
}

content = cleanLines.join('\n');
fs.writeFileSync('index.html', content);
console.log('✅ 修复完成');
