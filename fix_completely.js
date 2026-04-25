const fs = require('fs');

let content = fs.readFileSync('index.html', 'utf8');
let lines = content.split('\n');
let newLines = [];
let skipUntil = -1;

console.log('开始修复...');

// 遍历每一行
for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const lineNum = i + 1;
    
    // 跳过第675-697行（重复的podcastList）
    if (lineNum >= 675 && lineNum <= 697) {
        if (lineNum === 675) console.log('跳过重复的 podcastList 开始');
        if (lineNum === 697) console.log('跳过重复的 podcastList 结束');
        continue;
    }
    
    // 跳过第3312行（重复的methodTraining）
    if (lineNum === 3312) {
        console.log('跳过重复的 methodTraining');
        continue;
    }
    
    newLines.push(line);
}

content = newLines.join('\n');
fs.writeFileSync('index.html', content);
console.log('✅ 修复完成');
