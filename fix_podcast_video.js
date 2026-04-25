// V82 播客视频修复脚本
const fs = require('fs');
const path = require('path');

const indexPath = path.join(__dirname, 'index.html');
let content = fs.readFileSync(indexPath, 'utf8');

// 新的播客数据 - 21个真实音频
const podcastData = `// 播客音频数据 - 21个真实音频
const podcastList = [
    {id:1,title:"青少年高效记忆法全攻略",url:"https://lf-coze-scdn.coze.cn/7626319930325139754-data_volume/generated/20260416/c8bb3b0e-ecba-4d86-a712-87f1f5f81681/audio_76c4432f-433a-4faa-94d5-8481cd7d858d.mp3",duration:"6:14",category:"学霸方法",icon:"🧠"},
    {id:2,title:"青少年高效笔记法大揭秘",url:"https://lf-coze-scdn.coze.cn/7626319930325139754-data_volume/generated/20260416/d4a7a670-15a0-4697-ba59-484ef9deb4ab/audio_46214d4b-5ac8-4ce2-adfc-8329a5842b81.mp3",duration:"8:10",category:"学霸方法",icon:"📒"},
    {id:3,title:"青少年高效时间管理秘籍",url:"https://lf-coze-scdn.coze.cn/7626319930325139754-data_volume/generated/20260416/a24b1313-f6be-4a47-9568-f2615b278a50/audio_6fdd7411-5a5c-4c29-8873-2876897b9d9f.mp3",duration:"7:52",category:"学霸方法",icon:"⏰"},
    {id:4,title:"青少年高效复习策略指南",url:"https://lf-coze-scdn.coze.cn/7626319930325139754-data_volume/generated/20260416/9f4430be-29cc-4025-8102-ac791cbff83c/audio_5ba0144b-1219-49ad-87d9-e9c1be72794e.mp3",duration:"7:30",category:"学霸方法",icon:"📖"},
    {id:5,title:"三招提升青少年专注力",url:"https://lf-coze-scdn.coze.cn/7626319930325139754-data_volume/generated/20260416/4d24d8a3-cce6-4066-b5c5-dfba8edb6fb2/audio_2c3d214a-66c3-4ed8-9375-b00e4d09e02e.mp3",duration:"10:54",category:"学霸方法",icon:"🎯"},
    {id:6,title:"青少年语文思维训练秘籍",url:"https://lf-coze-scdn.coze.cn/7626319930325139754-data_volume/generated/20260416/32fb5056-b96d-47eb-9cf6-1901e6286ac8/audio_a15c9809-e450-486e-b53c-f7be13ce0e45.mp3",duration:"9:30",category:"思维训练",icon:"📝"},
    {id:7,title:"青少年英语思维训练秘籍",url:"https://lf-coze-scdn.coze.cn/7626319930325139754-data_volume/generated/20260416/16b62bb3-1200-4c8c-b722-1f1974bd4ebe/audio_36379afa-9737-4b09-a5d5-2f44d9c6b888.mp3",duration:"10:08",category:"思维训练",icon:"📖"},
    {id:8,title:"青少年考试通关秘籍大公开",url:"https://lf-coze-scdn.coze.cn/7626319930325139754-data_volume/generated/20260416/fe4d1632-3670-4d3a-a32c-dfd4bd5866de/audio_478bad14-6b2c-49d5-9fad-77a937ee43e3.mp3",duration:"10:51",category:"学霸方法",icon:"🏆"},
    {id:9,title:"学霸私藏！高效解题策略大揭秘",url:"https://lf-coze-scdn.coze.cn/7626319930325139754-data_volume/generated/20260409/d48b8313-dd9b-4330-b92e-b07d158bc4c2/audio_1bd17a89-5fed-4ef2-878b-ad6280ef84ed.mp3",duration:"13:12",category:"学霸方法",icon:"💡"},
    {id:10,title:"学霸秘籍：深度理解知识建构法",url:"https://lf-coze-scdn.coze.cn/7626319930325139754-data_volume/generated/20260409/2bfc0231-a369-45f2-ab6e-82bbce1ec732/audio_080df6bb-7e56-4dee-adbe-358183a8e22a.mp3",duration:"9:42",category:"学霸方法",icon:"🏗️"},
    {id:11,title:"揭秘数学五大思维，解题变简单！",url:"https://lf-coze-scdn.coze.cn/7626319930325139754-data_volume/generated/20260412/c9b9a765-eecc-43a7-8d58-ee7aaf18b3f2/audio_0aab9a93-da9a-4fbf-9d68-943db9addf6c.mp3",duration:"3:36",category:"数学思维",icon:"🔢"},
    {id:12,title:"青少年数学思维：抽象与推理",url:"https://lf-coze-scdn.coze.cn/7626319930325139754-data_volume/generated/20260409/176a52a0-26d9-4360-ade1-a65be62256a1/audio_f4839c95-9f04-41ab-8f91-4eb776be47a0.mp3",duration:"7:56",category:"数学思维",icon:"📐"},
    {id:13,title:"青少年数学思维：数形结合专项",url:"https://lf-coze-scdn.coze.cn/7626319930325139754-data_volume/generated/20260409/6e9cadec-b1df-4c1c-81a8-ddbe79205d56/audio_e26d1ba7-c4f6-447d-9325-a9771ad48689.mp3",duration:"8:58",category:"数学思维",icon:"📊"},
    {id:14,title:"青少年数学建模思维入门指南",url:"https://lf-coze-scdn.coze.cn/7626319930325139754-data_volume/generated/20260409/becbe2ea-03d6-4b2d-b756-4377de6fb189/audio_ec4848f7-a93a-4a02-b5f8-70d40b44b0f6.mp3",duration:"8:29",category:"数学思维",icon:"🏛️"},
    {id:15,title:"青少年数学逆向思维专项课",url:"https://lf-coze-scdn.coze.cn/7626319930325139754-data_volume/generated/20260409/2f5d873e-3dcd-4d75-9526-0091cca45cb0/audio_8d19c35a-5db4-4a45-b4d2-f471f4119ad8.mp3",duration:"9:04",category:"数学思维",icon:"🔄"},
    {id:16,title:"青少年物理思维：因果与守恒",url:"https://lf-coze-scdn.coze.cn/7626319930325139754-data_volume/generated/20260409/881db938-d0ee-4c66-8eda-556966dd144d/audio_7f34f8f9-25c6-4eb3-882e-7f288b16681b.mp3",duration:"8:05",category:"物理思维",icon:"⚡"},
    {id:17,title:"青少年物理模型思维入门指南",url:"https://lf-coze-scdn.coze.cn/7626319930325139754-data_volume/generated/20260409/8d712c8a-9d3e-4ca7-8805-943c91e57466/audio_8bb3eb9c-52ac-4e08-bc5d-96e18019b12f.mp3",duration:"6:25",category:"物理思维",icon:"🔧"},
    {id:18,title:"Week1复盘&Week2记忆训练计划",url:"https://lf-coze-scdn.coze.cn/7626319930325139754-data_volume/generated/20260416/af4d7586-2308-4aa1-915f-f7a41a84ae25/audio_03b8b756-15cd-4097-aae7-9b264b2aece5.mp3",duration:"1:55",category:"周度复盘",icon:"📅"},
    {id:19,title:"Week2复盘&Week3训练大揭秘",url:"https://lf-coze-scdn.coze.cn/7626319930325139754-data_volume/generated/20260416/98dbf101-0eac-4d49-9f94-8748babaa1ee/audio_2aaa7b2e-2547-40a8-9d79-218e0bd15a0c.mp3",duration:"1:55",category:"周度复盘",icon:"📅"},
    {id:20,title:"Week3复盘&Week4冲刺计划",url:"https://lf-coze-scdn.coze.cn/7626319930325139754-data_volume/generated/20260416/24f977cd-3d2a-440a-97dc-f249d265c829/audio_2f252ee4-bf23-4536-a65b-cad08438f4ec.mp3",duration:"2:10",category:"周度复盘",icon:"📅"},
    {id:21,title:"四周训练完结！青小年蜕变复盘",url:"https://lf-coze-scdn.coze.cn/7626319930325139754-data_volume/generated/20260416/64b06198-e977-4638-a9d3-f46478ca4702/audio_fe4b8c27-7280-471e-9014-b64ab0b8ed4b.mp3",duration:"2:24",category:"周度复盘",icon:"🎉"}
];

// 播放播客音频
function playPodcastAudio(id) {
    const podcast = podcastList.find(p => p.id === id);
    if (!podcast) return;
    
    const audio = document.getElementById('main-audio');
    if (!audio) return;
    
    audio.src = podcast.url;
    audio.play().catch(e => {
        showToast('播放失败，请检查网络连接');
    });
    
    showMiniPlayer(podcast.title, podcast.duration);
    currentPodcastId = id;
    
    audio.onended = function() {
        const nextId = id + 1;
        if (nextId <= podcastList.length) {
            playPodcastAudio(nextId);
        }
    };
}

// 迷你播放器显示
let currentPodcastId = null;
function showMiniPlayer(title, duration) {
    let miniPlayer = document.getElementById('mini-player');
    if (!miniPlayer) {
        miniPlayer = document.createElement('div');
        miniPlayer.id = 'mini-player';
        miniPlayer.className = 'mini-player';
        document.body.appendChild(miniPlayer);
    }
    
    miniPlayer.innerHTML = \`
        <div style="width:40px;height:40px;background:linear-gradient(135deg,#667eea,#764ba2);border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:20px;">🎧</div>
        <div style="flex:1;min-width:0;">
            <div style="font-size:13px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">\${title}</div>
            <div style="font-size:11px;color:#999;">🎧 播客 · \${duration}</div>
        </div>
        <button onclick="togglePlayPause()" id="mp-play-btn" style="width:36px;height:36px;border-radius:50%;background:var(--blue);border:none;color:white;font-size:14px;cursor:pointer;">▶</button>
        <button onclick="closeMiniPlayer()" style="width:28px;height:28px;border-radius:50%;background:#f0f0f0;border:none;font-size:12px;cursor:pointer;">✕</button>
    \`;
    
    miniPlayer.style.display = 'flex';
}

function closeMiniPlayer() {
    const miniPlayer = document.getElementById('mini-player');
    if (miniPlayer) miniPlayer.style.display = 'none';
    const audio = document.getElementById('main-audio');
    if (audio) audio.pause();
}

function togglePlayPause() {
    const audio = document.getElementById('main-audio');
    const btn = document.getElementById('mp-play-btn');
    if (audio && btn) {
        if (audio.paused) {
            audio.play();
            btn.textContent = '⏸';
        } else {
            audio.pause();
            btn.textContent = '▶';
        }
    }
}

// 渲染播客列表
function renderPodcast(container) {
    container.innerHTML = \`
        <div class="card">
            <h3 style="margin-bottom:16px;">🎧 播客课堂 <span style="font-size:12px;color:#999;">共\${podcastList.length}个音频</span></h3>
            <div class="subject-tab">
                <button class="subject-tab-btn active" onclick="filterPodcast('all', this)">全部</button>
                <button class="subject-tab-btn" onclick="filterPodcast('学霸方法', this)">学霸方法</button>
                <button class="subject-tab-btn" onclick="filterPodcast('思维训练', this)">思维训练</button>
                <button class="subject-tab-btn" onclick="filterPodcast('数学思维', this)">数学思维</button>
                <button class="subject-tab-btn" onclick="filterPodcast('物理思维', this)">物理思维</button>
                <button class="subject-tab-btn" onclick="filterPodcast('周度复盘', this)">周度复盘</button>
            </div>
        </div>
        <div id="podcast-list">
            \${podcastList.map(p => \`
            <div class="podcast-item" onclick="playPodcastAudio(\${p.id})">
                <div class="podcast-thumb" style="background:linear-gradient(135deg,#667eea,#764ba2);">\${p.icon}</div>
                <div class="podcast-info">
                    <div class="podcast-title">\${p.title}</div>
                    <div class="podcast-meta">AI导师 · \${p.duration} · <span class="media-badge">\${p.category}</span></div>
                </div>
            </div>
            \`).join('')}
        </div>
    \`;
}

// 筛选播客
function filterPodcast(category, btn) {
    document.querySelectorAll('.subject-tab-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    
    const filtered = category === 'all' ? podcastList : podcastList.filter(p => p.category === category);
    const list = document.getElementById('podcast-list');
    if (list) {
        list.innerHTML = filtered.map(p => \`
        <div class="podcast-item" onclick="playPodcastAudio(\${p.id})">
            <div class="podcast-thumb" style="background:linear-gradient(135deg,#667eea,#764ba2);">\${p.icon}</div>
            <div class="podcast-info">
                <div class="podcast-title">\${p.title}</div>
                <div class="podcast-meta">AI导师 · \${p.duration} · <span class="media-badge">\${p.category}</span></div>
            </div>
        </div>
        \`).join('');
    }
}

// 视频课程数据
const videoList = [
    {id:1,title:"专注力训练",url:"https://yuhang87989.github.io/cognitive-training-portal/videos/专注力训练.mp4",duration:"5:23",category:"学霸方法"},
    {id:2,title:"学霸深度理解法_第1集",url:"https://yuhang87989.github.io/cognitive-training-portal/videos/学霸深度理解法_第1集.mp4",duration:"6:18",category:"学霸方法"},
    {id:3,title:"数学抽象推理",url:"https://yuhang87989.github.io/cognitive-training-portal/videos/数学抽象推理.mp4",duration:"5:06",category:"数学思维"},
    {id:4,title:"物理因果守恒_第1集",url:"https://yuhang87989.github.io/cognitive-training-portal/videos/物理因果守恒_第1集.mp4",duration:"5:41",category:"物理思维"},
    {id:5,title:"逆向思维训练_第1集",url:"https://yuhang87989.github.io/cognitive-training-portal/videos/逆向思维训练_第1集.mp4",duration:"3:27",category:"思维训练"}
];

// 渲染视频列表
function renderVideo(container) {
    container.innerHTML = \`
        <div class="card">
            <h3 style="margin-bottom:16px;">📺 视频课堂 <span style="font-size:12px;color:#999;">共\${videoList.length}个视频</span></h3>
            <div class="subject-tab">
                <button class="subject-tab-btn active" onclick="filterVideo('all', this)">全部</button>
                <button class="subject-tab-btn" onclick="filterVideo('学霸方法', this)">学习方法</button>
                <button class="subject-tab-btn" onclick="filterVideo('数学思维', this)">数学</button>
                <button class="subject-tab-btn" onclick="filterVideo('思维训练', this)">思维</button>
                <button class="subject-tab-btn" onclick="filterVideo('物理思维', this)">物理</button>
            </div>
        </div>
        <div id="video-list">
            \${videoList.map(v => \`
            <div class="video-item" onclick="playVideoFromList(\${v.id})">
                <div class="video-thumb"><span class="play-icon">▶</span></div>
                <div class="video-info">
                    <div class="video-title">\${v.title}</div>
                    <div class="video-meta">\${v.duration} · <span class="media-badge video">\${v.category}</span></div>
                </div>
            </div>
            \`).join('')}
        </div>
    \`;
}

// 筛选视频
function filterVideo(category, btn) {
    document.querySelectorAll('.subject-tab-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    
    const filtered = category === 'all' ? videoList : videoList.filter(v => v.category === category);
    const list = document.getElementById('video-list');
    if (list) {
        list.innerHTML = filtered.map(v => \`
        <div class="video-item" onclick="playVideoFromList(\${v.id})">
            <div class="video-thumb"><span class="play-icon">▶</span></div>
            <div class="video-info">
                <div class="video-title">\${v.title}</div>
                <div class="video-meta">\${v.duration} · <span class="media-badge video">\${v.category}</span></div>
            </div>
        </div>
        \`).join('');
    }
}

// 播放视频
function playVideoFromList(id) {
    const video = videoList.find(v => v.id === id);
    if (video) {
        openVideoPlayer(video.url, video.title);
    }
}
`;

// 替换旧的renderPodcast和renderVideo函数
// 找到const OLD_KEYS之前的部分，插入新代码
const oldKeysIndex = content.indexOf("const OLD_KEYS = ['cognitive_training_v43'");
if (oldKeysIndex !== -1) {
    content = content.substring(0, oldKeysIndex) + podcastData + "\n" + content.substring(oldKeysIndex);
    console.log("已添加播客和视频数据");
} else {
    console.log("未找到插入位置");
}

// 删除旧的renderPodcast和renderVideo函数（如果有重复的话）
// 由于我们是在OLD_KEYS之前添加的，旧函数应该还在后面
// 让我们删除它们

// 查找并删除旧的renderPodcast函数
const oldRenderPodcastMatch = content.match(/function renderPodcast\(container\) \{[\s\S]*?\n\}\n\nfunction filterPodcast/);
if (oldRenderPodcastMatch) {
    content = content.replace(oldRenderPodcastMatch[0], '');
    console.log("已删除旧的renderPodcast函数");
}

// 查找并删除旧的renderVideo函数
const oldRenderVideoMatch = content.match(/function renderVideo\(container\) \{[\s\S]*?\n\}\n\nfunction filterVideo/);
if (oldRenderVideoMatch) {
    content = content.replace(oldRenderVideoMatch[0], '');
    console.log("已删除旧的renderVideo函数");
}

// 删除旧的filterPodcast和filterVideo函数
content = content.replace(/function filterPodcast\(category, btn\) \{[\s\S]*?\n\}\n\n/, '\n');
content = content.replace(/function filterVideo\(category, btn\) \{[\s\S]*?\n\}\n\n/, '\n');

// 保存文件
fs.writeFileSync(indexPath, content, 'utf8');
console.log("文件已更新");
