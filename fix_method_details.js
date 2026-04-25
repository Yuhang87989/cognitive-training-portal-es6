const fs = require('fs');

let content = fs.readFileSync('index.html', 'utf8');
let lines = content.split('\n');
let newLines = [];

// 找到并修复 methodDetails
let inMethodDetails = false;
let braceCount = 0;
let foundClosingBrace = false;

for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const lineNum = i + 1;
    
    // 找到 methodDetails 开始
    if (line.includes('const methodDetails = {')) {
        inMethodDetails = true;
        console.log(`methodDetails 开始于第 ${lineNum} 行`);
    }
    
    if (inMethodDetails) {
        // 计数大括号
        braceCount += (line.match(/\{/g) || []).length;
        braceCount -= (line.match(/\}/g) || []).length;
        
        // 如果遇到闭合大括号
        if (braceCount === 0 && line.includes('};')) {
            foundClosingBrace = true;
            inMethodDetails = false;
            console.log(`methodDetails 闭合于第 ${lineNum} 行`);
        }
        
        // 如果在闭合后找到 sq3r，删除它
        if (foundClosingBrace && line.includes('sq3r:')) {
            console.log(`删除第 ${lineNum} 行的多余 sq3r`);
            continue;
        }
        
        // 删除多余的闭合大括号（如果有多行）
        if (foundClosingBrace && line.trim() === '}' && !line.includes(';')) {
            console.log(`删除第 ${lineNum} 行的多余闭合括号`);
            continue;
        }
    }
    
    newLines.push(line);
}

content = newLines.join('\n');
fs.writeFileSync('index.html', content);
console.log('✅ methodDetails 修复完成');
