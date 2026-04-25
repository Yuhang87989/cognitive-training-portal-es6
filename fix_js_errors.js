// V113 JavaScript语法错误修复脚本

const fs = require('fs');

// 读取文件
let content = fs.readFileSync('index.html', 'utf8');
let lines = content.split('\n');
let modified = false;

// 修复1: 删除第675行开始的重复 podcastList 定义
console.log('检查 podcastList 重复定义...');
let inDuplicatePodcastList = false;
let duplicateStartLine = -1;
let braceCount = 0;

for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    
    // 找到重复的 podcastList 开始 (第675行附近)
    if (line.trim().startsWith("const podcastList = [") && i > 650) {
        inDuplicatePodcastList = true;
        duplicateStartLine = i;
        console.log(`  发现重复 podcastList 开始于第 ${i+1} 行`);
        continue;
    }
    
    if (inDuplicatePodcastList) {
        braceCount += (line.match(/\[/g) || []).length;
        braceCount -= (line.match(/\]/g) || []).length;
        
        if (braceCount <= 0 && line.includes('];')) {
            // 删除这一行
            lines[i] = '';
            modified = true;
            console.log(`  删除第 ${i+1} 行的重复 podcastList 结束`);
            inDuplicatePodcastList = false;
            braceCount = 0;
        } else {
            lines[i] = '';
            modified = true;
        }
    }
}

// 修复2: 删除第3312行的重复 methodTraining 声明
console.log('检查 methodTraining 重复声明...');
for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (line.trim() === 'const methodTraining = methodTrainingQuestions;' && i > 3300) {
        lines[i] = '';
        modified = true;
        console.log(`  删除第 ${i+1} 行的重复 methodTraining 声明`);
    }
}

// 修复3: 修复 methodDetails 对象的重复属性
console.log('检查 methodDetails 对象重复属性...');
let methodDetailsStart = -1;
let methodDetailsEnd = -1;
let inMethodDetails = false;
let foundDuplicateSection = false;

for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    
    // 找到 methodDetails 开始
    if (line.includes('const methodDetails = {')) {
        methodDetailsStart = i;
        inMethodDetails = true;
        console.log(`  methodDetails 开始于第 ${i+1} 行`);
    }
    
    if (inMethodDetails) {
        // 找到第一个闭合大括号（排除timeManagement等内的）
        if (line.includes('sq3r:')) {
            methodDetailsEnd = i - 1;
            console.log(`  sq3r 定义异常，位置: 第 ${i+1} 行`);
        }
        
        // 删除重复的 timeManagement, noteTaking, testStrategy (在3253-3259行附近)
        if (i >= 3253 && i <= 3260 && line.includes('timeManagement:')) {
            // 检查是否是重复的
            if (!line.includes('feynman')) {
                lines[i] = '';
                modified = true;
                console.log(`  删除第 ${i+1} 行的重复 timeManagement`);
            }
        }
    }
}

if (modified) {
    content = lines.join('\n');
    fs.writeFileSync('index.html', content);
    console.log('\n✅ 文件已修改');
} else {
    console.log('\n⚠️ 未发现需要修复的问题');
}
