#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V128播客播放器改造脚本
将SoundHelix占位URL替换为动态获取coze签名URL
"""

import re
import os

# 读取index.html
with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# 新的podcastCourses数组，使用coze分享URL
new_podcast_courses = '''var podcastCourses = [
    {id:'podcast1',title:'告别背书苦海！3个记忆妙招助你逆袭',teacher:'学习方法专家',duration:'6:14',durationSec:374,category:'学霸方法',gradient:'linear-gradient(135deg,#667eea,#764ba2)',icon:'🧠',shareUrl:'https://www.coze.cn/s/3rTjJ7Xbdc0/',views:25000},
    {id:'podcast2',title:'青少年高效笔记法，学习效率翻倍',teacher:'学习方法专家',duration:'5:48',durationSec:348,category:'学霸方法',gradient:'linear-gradient(135deg,#FF9A63,#E87A4E)',icon:'📝',shareUrl:'https://www.coze.cn/s/HAjMzHnxwvY/',views:18000},
    {id:'podcast3',title:'3招让24小时变48小时',teacher:'时间管理导师',duration:'7:22',durationSec:442,category:'学霸方法',gradient:'linear-gradient(135deg,#43E97B,#38F9D7)',icon:'⏰',shareUrl:'https://www.coze.cn/s/uPgU_c9cAIY/',views:22000},
    {id:'podcast4',title:'告别无效复习！3个高效策略学起来',teacher:'心理学专家',duration:'5:55',durationSec:355,category:'学霸方法',gradient:'linear-gradient(135deg,#4facfe,#00f2fe)',icon:'🎯',shareUrl:'https://www.coze.cn/s/-FFxXRTedN0/',views:19500},
    {id:'podcast5',title:'3招提升专注力，学习不走神',teacher:'特级教师',duration:'8:30',durationSec:510,category:'学霸方法',gradient:'linear-gradient(135deg,#fa709a,#fee140)',icon:'💡',shareUrl:'https://www.coze.cn/s/ymrXMhQcvNY/',views:28000},
    {id:'podcast6',title:'解锁语文思维，成绩飞升秘籍',teacher:'数学特级教师',duration:'9:15',durationSec:555,category:'数学',gradient:'linear-gradient(135deg,#667eea,#764ba2)',icon:'📐',shareUrl:'https://www.coze.cn/s/-w-VgFqqOrY/',views:15600},
    {id:'podcast7',title:'青少年英语思维训练秘籍大公开',teacher:'英语教学专家',duration:'10:20',durationSec:620,category:'英语',gradient:'linear-gradient(135deg,#FF9A63,#E87A4E)',icon:'📖',shareUrl:'https://www.coze.cn/s/FxptvND8qlo/',views:21000},
    {id:'podcast8',title:'考试总失常？三大秘籍助你超常发挥',teacher:'物理特级教师',duration:'8:45',durationSec:525,category:'物理',gradient:'linear-gradient(135deg,#4facfe,#00f2fe)',icon:'⚡',shareUrl:'https://www.coze.cn/s/mLuQHON0Zzk/',views:12800},
    {id:'podcast9',title:'学霸私藏！高效解题策略大公开',teacher:'化学教学专家',duration:'7:55',durationSec:475,category:'化学',gradient:'linear-gradient(135deg,#43E97B,#38F9D7)',icon:'🧪',shareUrl:'https://www.coze.cn/s/UUMhRMn7SDg/',views:9800},
    {id:'podcast10',title:'背了知识点还不会做题？学霸秘籍来了',teacher:'语文特级教师',duration:'6:30',durationSec:390,category:'语文',gradient:'linear-gradient(135deg,#667eea,#764ba2)',icon:'📜',shareUrl:'https://www.coze.cn/s/t6s2x0F0XAs/',views:14200},
    {id:'podcast11',title:'数学不难！五大思维轻松学',teacher:'语文教学专家',duration:'7:10',durationSec:430,category:'语文',gradient:'linear-gradient(135deg,#FF9A63,#E87A4E)',icon:'✍️',shareUrl:'https://www.coze.cn/s/YiJe4WN8ErI/',views:11500},
    {id:'podcast12',title:'数学难题克星：抽象思维与逻辑推理',teacher:'学习方法专家',duration:'5:40',durationSec:340,category:'学霸方法',gradient:'linear-gradient(135deg,#fa709a,#fee140)',icon:'🧠',shareUrl:'https://www.coze.cn/s/TcqwrK5jqWM/',views:32000},
    {id:'podcast13',title:'青少年数学思维：数形结合专项',teacher:'时间管理导师',duration:'4:50',durationSec:290,category:'学霸方法',gradient:'linear-gradient(135deg,#4facfe,#00f2fe)',icon:'🍅',shareUrl:null,views:24500},
    {id:'podcast14',title:'生活中的数学建模：从选套餐到做决策',teacher:'心理学专家',duration:'6:15',durationSec:375,category:'学霸方法',gradient:'linear-gradient(135deg,#43E97B,#38F9D7)',icon:'🧮',shareUrl:'https://www.coze.cn/s/9cS58bZwn1g/',views:19800},
    {id:'podcast15',title:'数学解题新思路：逆向思维超实用',teacher:'学习方法专家',duration:'5:25',durationSec:325,category:'学霸方法',gradient:'linear-gradient(135deg,#667eea,#764ba2)',icon:'🎨',shareUrl:'https://www.coze.cn/s/0QgmPaZ9sUI/',views:17600},
    {id:'podcast16',title:'物理学的两把解题钥匙',teacher:'学习方法专家',duration:'4:35',durationSec:275,category:'学霸方法',gradient:'linear-gradient(135deg,#FF9A63,#E87A4E)',icon:'📋',shareUrl:'https://www.coze.cn/s/qAgLfdh6aPE/',views:15900},
    {id:'podcast17',title:'揭秘物理学家的模型思维',teacher:'语文教学专家',duration:'5:05',durationSec:305,category:'学霸方法',gradient:'linear-gradient(135deg,#4facfe,#00f2fe)',icon:'📖',shareUrl:'https://www.coze.cn/s/9zZnticB374/',views:13400},
    {id:'podcast18',title:'Week1复盘&Week2记忆训练计划',teacher:'心理学专家',duration:'6:45',durationSec:405,category:'学霸方法',gradient:'linear-gradient(135deg,#fa709a,#fee140)',icon:'🚀',shareUrl:null,views:21800},
    {id:'podcast19',title:'青小年训练周报：数学物理思维入门',teacher:'心理辅导师',duration:'5:50',durationSec:350,category:'学霸方法',gradient:'linear-gradient(135deg,#43E97B,#38F9D7)',icon:'😌',shareUrl:'https://www.coze.cn/s/SjBR-HOwR98/',views:18700},
    {id:'podcast20',title:'青小年训练周报：Week3思维整合入门',teacher:'学习方法专家',duration:'4:20',durationSec:260,category:'学霸方法',gradient:'linear-gradient(135deg,#667eea,#764ba2)',icon:'📒',shareUrl:'https://www.coze.cn/s/ATJKT6u6G7E/',views:14200},
    {id:'podcast21',title:'青小年训练周报四周完结篇',teacher:'时间管理导师',duration:'7:30',durationSec:450,category:'学霸方法',gradient:'linear-gradient(135deg,#FF9A63,#E87A4E)',icon:'📅',shareUrl:'https://www.coze.cn/s/Illp6Wnea3A/',views:16500}
]'''

# 查找并替换podcastCourses数组
old_pattern = r"var podcastCourses = \[.*?\]"
if re.search(old_pattern, content, re.DOTALL):
    content = re.sub(old_pattern, new_podcast_courses, content, count=1, flags=re.DOTALL)
    print("✓ podcastCourses数组已更新")
else:
    print("✗ 未找到podcastCourses数组")

# 添加动态获取签名URL的函数
get_audio_url_function = '''
// ====== 播客签名URL获取与缓存 ======
var podcastUrlCache = {
    cache: {},
    cacheExpiry: {},
    CACHE_DURATION: 12 * 60 * 60 * 1000 // 12小时缓存
    
};

// 动态获取播客签名URL
async function getPodcastAudioUrl(shareUrl, courseId) {
    if (!shareUrl) return null;
    
    // 检查缓存
    var now = Date.now();
    if (podcastUrlCache.cache[courseId] && 
        podcastUrlCache.cacheExpiry[courseId] && 
        now < podcastUrlCache.cacheExpiry[courseId]) {
        console.log('使用缓存的签名URL:', courseId);
        return podcastUrlCache.cache[courseId];
    }
    
    try {
        console.log('正在获取签名URL:', shareUrl);
        
        // 1. fetch分享URL，跟随302获取.podcast JSON
        var resp = await fetch(shareUrl, {redirect: 'follow', credentials: 'include'});
        if (!resp.ok && resp.status !== 302) {
            throw new Error('分享URL请求失败: ' + resp.status);
        }
        
        var podcastData = await resp.json();
        var audioUri = podcastData.audio_uri;
        
        if (!audioUri) {
            throw new Error('分享页面未返回audio_uri');
        }
        
        console.log('获取到audio_uri:', audioUri);
        
        // 2. 调用coze内部API获取签名URL
        var signResp = await fetch('https://www.coze.cn/api/coze_space/get_url', {
            method: 'POST',
            credentials: 'include',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({uri: audioUri})
        });
        
        var signData = await signResp.json();
        
        if (signData.code === 0 && signData.data && signData.data.url) {
            var signedUrl = signData.data.url;
            console.log('获取到签名URL:', signedUrl);
            
            // 缓存结果
            podcastUrlCache.cache[courseId] = signedUrl;
            podcastUrlCache.cacheExpiry[courseId] = now + podcastUrlCache.CACHE_DURATION;
            
            return signedUrl;
        }
        
        console.warn('get_url API返回异常:', signData);
        throw new Error('get_url failed: ' + (signData.msg || 'unknown'));
        
    } catch(e) {
        console.error('获取播客音频URL失败:', e);
        return null;
    }
}

// 清除指定播客的缓存
function clearPodcastCache(courseId) {
    if (courseId) {
        delete podcastUrlCache.cache[courseId];
        delete podcastUrlCache.cacheExpiry[courseId];
        console.log('已清除缓存:', courseId);
    } else {
        podcastUrlCache.cache = {};
        podcastUrlCache.cacheExpiry = {};
        console.log('已清除所有播客缓存');
    }
}

'''

# 在playPodcastCourse函数之前插入新函数
# 找到 "// 播放器状态" 或 "var audioCtx" 的位置
insert_marker = "// 播放器状态"
if insert_marker in content:
    content = content.replace(insert_marker, get_audio_url_function + "\n" + insert_marker)
    print("✓ 签名URL获取函数已添加")
else:
    print("✗ 未找到插入位置")
    # 尝试其他位置
    insert_marker2 = "var audioCtx = {"
    if insert_marker2 in content:
        content = content.replace(insert_marker2, get_audio_url_function + "\nvar audioCtx = {")
        print("✓ 签名URL获取函数已添加(备用位置)")

# 替换playPodcastCourse函数
new_play_podcast_course = '''function playPodcastCourse(courseId) {
    // 确保获取真正的 audio 元素
    var audioEl = document.getElementById('hidden-audio');
    if (!audioEl) {
        console.error('播客播放器初始化失败：找不到 hidden-audio 元素');
        showToast('播放器初始化失败，请刷新页面');
        return;
    }
    var course = null;
    for (var i = 0; i < podcastCourses.length; i++) { if (podcastCourses[i].id === courseId) { course = podcastCourses[i]; break; } }
    if (!course) return;
    
    audioCtx.currentTrack = course;
    audioCtx.currentIndex = -1;
    for (var i = 0; i < podcastCourses.length; i++) { if (podcastCourses[i].id === courseId) { audioCtx.currentIndex = i; break; } }
    
    var titleEl = document.getElementById('ap-title');
    var coverEl = document.getElementById('ap-cover');
    var courseTitleEl = document.getElementById('ap-course-title');
    var teacherEl = document.getElementById('ap-teacher');
    var categoryEl = document.getElementById('ap-category');
    
    if (titleEl) titleEl.textContent = course.title;
    if (coverEl) { coverEl.innerHTML = course.icon; coverEl.style.background = course.gradient; }
    if (courseTitleEl) courseTitleEl.textContent = course.title;
    if (teacherEl) teacherEl.textContent = course.teacher;
    if (categoryEl) categoryEl.textContent = course.category;
    
    // 更新音频封面区域
    var audioCoverEl = document.getElementById('audio-cover-bg');
    if (audioCoverEl) { audioCoverEl.innerHTML = course.icon; audioCoverEl.style.background = course.gradient; }
    
    // 如果没有shareUrl，显示提示
    if (!course.shareUrl) {
        showToast('该播客暂不可用');
        return;
    }
    
    // 显示加载状态
    showToast('正在获取音频...');
    
    // 动态获取签名URL
    getPodcastAudioUrl(course.shareUrl, courseId).then(function(audioUrl) {
        if (audioUrl) {
            console.log('设置音频源:', audioUrl);
            audioEl.src = audioUrl;
            
            // 恢复播放进度
            if (savedPositions[courseId]) {
                audioEl.currentTime = savedPositions[courseId];
            }
            audioEl.playbackRate = audioCtx.playbackSpeed;
            audioEl.volume = audioCtx.volume;
            
            audioEl.play().then(function() {
                console.log('音频播放成功');
                audioCtx.isPlaying = true;
                updatePlayButtons();
            }).catch(function(e) {
                console.error('音频播放失败:', e);
                if (e.name === 'NotAllowedError') {
                    showToast('请手动点击播放按钮');
                } else {
                    showToast('播放失败，请检查网络');
                }
            });
            
            showMiniPlayer(course);
            var playerEl = document.getElementById('audio-player-fullscreen');
            var coverPlayingEl = document.getElementById('ap-cover');
            if (playerEl) playerEl.classList.add('show');
            if (coverPlayingEl) coverPlayingEl.classList.add('playing');
            updatePodcastListState(courseId);
            showToast('正在播放: ' + course.title);
        } else {
            console.warn('获取音频URL失败，尝试打开分享页面');
            // 获取失败时，打开分享页面作为fallback
            showToast('正在跳转播放页面...');
            window.open(course.shareUrl, '_blank');
        }
    });
}'''

# 替换原来的playPodcastCourse函数
# 找到原函数的开头和结尾
old_func_pattern = r'function playPodcastCourse\(courseId\) \{[\s\S]*?audioEl\.play\(\)\.then\(function\(\) \{[\s\S]*?showToast\(\'正在播放: \' \+ course\.title\'\);'
if re.search(old_func_pattern, content):
    content = re.sub(old_func_pattern, new_play_podcast_course, content, count=1)
    print("✓ playPodcastCourse函数已更新")
else:
    print("✗ 未找到playPodcastCourse函数进行替换")

# 更新版本号到V128
content = content.replace("'V120'", "'V128'")
content = content.replace(">V120</", ">V128</")
content = content.replace("V120 →", "V128 →")
content = content.replace("版本 V120", "版本 V128")
print("✓ 版本号已更新到V128")

# 保存修改后的文件
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n=== 改造完成 ===")
print("已完成的修改:")
print("1. podcastCourses数组使用coze分享URL（shareUrl字段）")
print("2. 添加了getPodcastAudioUrl函数动态获取签名URL")
print("3. 添加了podcastUrlCache缓存机制")
print("4. 修改了playPodcastCourse函数使用新的动态获取逻辑")
print("5. podcast13和podcast18标记为暂不可用")
print("6. 版本号更新为V128")
