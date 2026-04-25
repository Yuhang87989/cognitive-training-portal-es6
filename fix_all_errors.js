const fs = require('fs');

let content = fs.readFileSync('index.html', 'utf8');
let lines = content.split('\n');
let newLines = [];
let skipUntilLine = -1;

// 方法1: 查找并修复 methodDetails
let inMethodDetails = false;
let braceCount = 0;
let methodDetailsEnd = -1;
let methodDetailsHasSq3r = false;

for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const lineNum = i + 1;
    
    // 跳过 675-697 行（重复的 podcastList）
    if (lineNum >= 675 && lineNum <= 697) continue;
    
    // 跳过 3312 行（重复的 methodTraining）
    if (lineNum === 3312) continue;
    
    // 找到 methodDetails
    if (line.includes('const methodDetails = {')) {
        inMethodDetails = true;
    }
    
    if (inMethodDetails) {
        braceCount += (line.match(/\{/g) || []).length;
        braceCount -= (line.match(/\}/g) || []).length;
        
        // 检查是否已经包含 sq3r
        if (line.includes('sq3r:')) {
            methodDetailsHasSq3r = true;
        }
        
        // 找到闭合大括号
        if (braceCount === 0 && line.includes('};')) {
            inMethodDetails = false;
            methodDetailsEnd = lineNum;
            
            // 如果没有 sq3r，在闭合前添加
            if (!methodDetailsHasSq3r) {
                // 插入 sq3r
                newLines.push("    sq3r: {title:'📖 SQ3R阅读法',desc:'Survey泛读、Question提问、Read阅读、Recite复述、Review复习。',steps:['Survey（泛读）：快速浏览标题、目录、图表','Question（提问）：写下你想知道的问题','Read（阅读）：仔细阅读章节内容','Recite（复述）：合上书复述要点','Review（复习）：定期回顾已读内容'],tip:'💡 适合：教科书、论文、长篇文章的阅读。'}");
            }
        }
    }
    
    // 删除重复的 methodDetails 内容（在闭合大括号后但在下一个函数前的空行）
    if (lineNum > methodDetailsEnd && lineNum < methodDetailsEnd + 20) {
        // 删除 timeManagement, noteTaking, testStrategy 的重复定义
        if (line.includes('timeManagement:') || line.includes('noteTaking:') || line.includes('testStrategy:')) {
            if (lineNum > methodDetailsEnd) {
                continue; // 跳过重复行
            }
        }
        // 删除重复的闭合括号
        if (line.trim() === '}' && !line.includes(';')) {
            continue;
        }
    }
    
    newLines.push(line);
}

// 查找并修复 methodDetails - 重新检查
lines = newLines.join('\n').split('\n');
newLines = [];
inMethodDetails = false;
braceCount = 0;
let foundClosing = false;
let lineAfterClosing = false;

for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const lineNum = i + 1;
    
    if (line.includes('const methodDetails = {')) {
        inMethodDetails = true;
    }
    
    if (inMethodDetails) {
        braceCount += (line.match(/\{/g) || []).length;
        braceCount -= (line.match(/\}/g) || []).length;
        
        if (braceCount === 0 && line.includes('};')) {
            inMethodDetails = false;
            foundClosing = true;
        }
        
        // 如果闭合大括号后面还有属性定义（说明结构有问题）
        if (foundClosing && !lineAfterClosing) {
            if (line.includes(':') && !line.includes('function') && line.trim().length > 0) {
                lineAfterClosing = true;
                // 在闭合前插入这些属性
                if (!line.includes('sq3r:')) {
                    newLines.push("    sq3r: {title:'📖 SQ3R阅读法',desc:'Survey泛读、Question提问、Read阅读、Recite复述、Review复习。',steps:['Survey（泛读）：快速浏览标题、目录、图表','Question（提问）：写下你想知道的问题','Read（阅读）：仔细阅读章节内容','Recite（复述）：合上书复述要点','Review（复习）：定期回顾已读内容'],tip:'💡 适合：教科书、论文、长篇文章的阅读。'}");
                }
                newLines.push('};');
                continue;
            }
        }
    }
    
    newLines.push(line);
}

content = newLines.join('\n');
fs.writeFileSync('index.html', content);
console.log('✅ 修复完成');
