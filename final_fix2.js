const fs = require('fs');

let content = fs.readFileSync('index.html', 'utf8');

// 方法: 直接删除重复的 methodDetails 内容

// 找到 methodDetails 的闭合大括号，然后删除其后的重复内容
const lines = content.split('\n');
let newLines = [];
let foundClosing = false;
let skipUntilFunction = false;

for (let i = 0; i < lines.length; i++) {
    const lineNum = i + 1;
    const line = lines[i];
    
    // 找到 methodDetails 的闭合大括号
    if (line.includes('testStrategy:') && line.includes('};')) {
        foundClosing = true;
        newLines.push(line); // 保留闭合大括号
        skipUntilFunction = true;
        console.log(`找到闭合大括号在第${lineNum}行`);
        continue;
    }
    
    // 跳过闭合大括号后的空行和重复内容
    if (skipUntilFunction) {
        // 如果遇到函数定义，停止跳过
        if (line.includes('function showMethodDetail')) {
            skipUntilFunction = false;
            foundClosing = false;
            newLines.push(line);
            console.log(`找到函数定义在第${lineNum}行`);
            continue;
        }
        // 跳过所有其他内容
        continue;
    }
    
    newLines.push(line);
}

content = newLines.join('\n');
fs.writeFileSync('index.html', content);
console.log('✅ 修复完成');
