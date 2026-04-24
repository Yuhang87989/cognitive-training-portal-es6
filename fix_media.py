import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 修复播客课程数据 - 添加有效的音频URL
# soundhelix 的示例音频
soundhelix_base = 'https://www.soundhelix.com/examples/mp3'

old_podcast = '''// ====== 播客课程数据 ======
var podcastCourses = [
    {id:'audio1',title:'英语听力训练技巧',teacher:'王老师',duration:'12:30',category:'英语',gradient:'linear-gradient(135deg,#667eea,#764ba2)',icon:'🎧',views:2341},
    {id:'audio2',title:'费曼学习法详解',teacher:'李老师',duration:'8:45',category:'学习方法',gradient:'linear-gradient(135deg,#FF9A63,#E87A4E)',icon:'🧠',views:4521},
    {id:'audio3',title:'时间管理秘诀',teacher:'张老师',duration:'10:20',category:'学习方法',gradient:'linear-gradient(135deg,#43E97B,#38F9D7)',icon:'⏰',views:3892},
    {id:'audio4',title:'数学思维培养',teacher:'赵老师',duration:'15:00',category:'数学',gradient:'linear-gradient(135deg,#4facfe,#00f2fe)',icon:'📐',views:2156},
    {id:'audio5',title:'古诗词鉴赏技巧',teacher:'陈老师',duration:'11:30',category:'语文',gradient:'linear-gradient(135deg,#f6d365,#fda085)',icon:'📝',views:1876},
    {id:'audio6',title:'物理概念入门',teacher:'林老师',duration:'14:00',category:'物理',gradient:'linear-gradient(135deg,#fa709a,#fee140)',icon:'⚡',views:1567},
    {id:'audio7',title:'化学元素周期表',teacher:'周老师',duration:'13:45',category:'化学',gradient:'linear-gradient(135deg,#667eea,#764ba2)',icon:'🧪',views:1234},
    {id:'audio8',title:'番茄工作法实践',teacher:'刘老师',duration:'9:15',category:'学习方法',gradient:'linear-gradient(135deg,#FF6B6B,#FF4757)',icon:'🍅',views:3421},
    {id:'audio9',title:'艾宾浩斯记忆法',teacher:'孙老师',duration:'10:30',category:'学习方法',gradient:'linear-gradient(135deg,#43E97B,#38F9D7)',icon:'🔄',views:2890},
    {id:'audio10',title:'阅读理解技巧',teacher:'吴老师',duration:'12:00',category:'英语',gradient:'linear-gradient(135deg,#4facfe,#00f2fe)',icon:'📖',views:1678}
];'''

new_podcast = '''// ====== 播客课程数据 ======
var podcastCourses = [
    {id:'audio1',title:'英语听力训练技巧',teacher:'王老师',duration:'12:30',category:'英语',gradient:'linear-gradient(135deg,#667eea,#764ba2)',icon:'🎧',views:2341,url:'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3'},
    {id:'audio2',title:'费曼学习法详解',teacher:'李老师',duration:'8:45',category:'学习方法',gradient:'linear-gradient(135deg,#FF9A63,#E87A4E)',icon:'🧠',views:4521,url:'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3'},
    {id:'audio3',title:'时间管理秘诀',teacher:'张老师',duration:'10:20',category:'学习方法',gradient:'linear-gradient(135deg,#43E97B,#38F9D7)',icon:'⏰',views:3892,url:'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3'},
    {id:'audio4',title:'数学思维培养',teacher:'赵老师',duration:'15:00',category:'数学',gradient:'linear-gradient(135deg,#4facfe,#00f2fe)',icon:'📐',views:2156,url:'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3'},
    {id:'audio5',title:'古诗词鉴赏技巧',teacher:'陈老师',duration:'11:30',category:'语文',gradient:'linear-gradient(135deg,#f6d365,#fda085)',icon:'📝',views:1876,url:'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3'},
    {id:'audio6',title:'物理概念入门',teacher:'林老师',duration:'14:00',category:'物理',gradient:'linear-gradient(135deg,#fa709a,#fee140)',icon:'⚡',views:1567,url:'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-6.mp3'},
    {id:'audio7',title:'化学元素周期表',teacher:'周老师',duration:'13:45',category:'化学',gradient:'linear-gradient(135deg,#667eea,#764ba2)',icon:'🧪',views:1234,url:'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-7.mp3'},
    {id:'audio8',title:'番茄工作法实践',teacher:'刘老师',duration:'9:15',category:'学习方法',gradient:'linear-gradient(135deg,#FF6B6B,#FF4757)',icon:'🍅',views:3421,url:'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3'},
    {id:'audio9',title:'艾宾浩斯记忆法',teacher:'孙老师',duration:'10:30',category:'学习方法',gradient:'linear-gradient(135deg,#43E97B,#38F9D7)',icon:'🔄',views:2890,url:'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-9.mp3'},
    {id:'audio10',title:'阅读理解技巧',teacher:'吴老师',duration:'12:00',category:'英语',gradient:'linear-gradient(135deg,#4facfe,#00f2fe)',icon:'📖',views:1678,url:'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-10.mp3'},
    {id:'audio11',title:'写作能力提升',teacher:'周老师',duration:'11:15',category:'语文',gradient:'linear-gradient(135deg,#a8edea,#fed6e3)',icon:'✍️',views:1456,url:'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-11.mp3'},
    {id:'audio12',title:'光学原理讲解',teacher:'陈老师',duration:'13:20',category:'物理',gradient:'linear-gradient(135deg,#d299c2,#fef9d7)',icon:'💡',views:1234,url:'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-12.mp3'},
    {id:'audio13',title:'力学基础入门',teacher:'林老师',duration:'14:45',category:'物理',gradient:'linear-gradient(135deg,#89f7fe,#66a6ff)',icon:'⚙️',views:1567,url:'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-13.mp3'},
    {id:'audio14',title:'化学反应原理',teacher:'吴老师',duration:'12:30',category:'化学',gradient:'linear-gradient(135deg,#fddb92,#d1fdff)',icon:'🧬',views:1345,url:'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-14.mp3'},
    {id:'audio15',title:'思维导图绘制',teacher:'刘老师',duration:'10:00',category:'学习方法',gradient:'linear-gradient(135deg,#ffecd2,#fcb69f)',icon:'🗺️',views:2890,url:'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-15.mp3'},
    {id:'audio16',title:'完形填空技巧',teacher:'王老师',duration:'9:30',category:'英语',gradient:'linear-gradient(135deg,#a1c4fd,#c2e9fb)',icon:'📝',views:1876,url:'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-16.mp3'},
    {id:'audio17',title:'文言文学习方法',teacher:'李老师',duration:'11:45',category:'语文',gradient:'linear-gradient(135deg,#f093fb,#f5576c)',icon:'📜',views:1678,url:'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3'},
    {id:'audio18',title:'声学基础知识',teacher:'张老师',duration:'10:15',category:'物理',gradient:'linear-gradient(135deg,#4facfe,#00f2fe)',icon:'🔊',views:1456,url:'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3'},
    {id:'audio19',title:'酸碱盐专题',teacher:'赵老师',duration:'13:00',category:'化学',gradient:'linear-gradient(135deg,#43e97b,#38f9d7)',icon:'⚗️',views:1234,url:'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3'},
    {id:'audio20',title:'数学解题思路',teacher:'孙老师',duration:'12:45',category:'数学',gradient:'linear-gradient(135deg,#fa709a,#fee140)',icon:'🔢',views:2156,url:'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3'},
    {id:'audio21',title:'学霸时间表分享',teacher:'吴老师',duration:'8:30',category:'学习方法',gradient:'linear-gradient(135deg,#667eea,#764ba2)',icon:'📅',views:3421,url:'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3'}
];'''

content = content.replace(old_podcast, new_podcast)

# 修复视频课程数据 - 添加更多有效视频
old_video = '''var videoCourses = [
    {id:'video1',title:'高效学习技巧',teacher:'赵老师',duration:'5:30',durationSec:330,category:'学习方法',gradient:'linear-gradient(135deg,#667eea,#764ba2)',icon:'🎬',url:'https://www.w3schools.com/html/mov_bbb.mp4',views:12000},
    {id:'video2',title:'时间管理方法',teacher:'张老师',duration:'8:15',durationSec:495,category:'学习方法',gradient:'linear-gradient(135deg,#FF9A63,#E87A4E)',icon:'🎬',url:'https://www.w3schools.com/html/movie.mp4',views:8000},
    {id:'video3',title:'数学解题大招',teacher:'赵老师',duration:'12:00',durationSec:720,category:'数学',gradient:'linear-gradient(135deg,#43E97B,#38F9D7)',icon:'📐',url:'https://www.w3schools.com/html/mov_bbb.mp4',views:5600},
    {id:'video4',title:'英语口语训练',teacher:'王老师',duration:'15:45',durationSec:945,category:'英语',gradient:'linear-gradient(135deg,#4facfe,#00f2fe)',icon:'🗣️',url:'https://www.w3schools.com/html/movie.mp4',views:4300}
];'''

new_video = '''var videoCourses = [
    {id:'video1',title:'高效学习技巧',teacher:'赵老师',duration:'5:30',durationSec:330,category:'学习方法',gradient:'linear-gradient(135deg,#667eea,#764ba2)',icon:'🎬',url:'https://www.w3schools.com/html/mov_bbb.mp4',views:12000},
    {id:'video2',title:'时间管理方法',teacher:'张老师',duration:'8:15',durationSec:495,category:'学习方法',gradient:'linear-gradient(135deg,#FF9A63,#E87A4E)',icon:'🎬',url:'https://www.w3schools.com/html/movie.mp4',views:8000},
    {id:'video3',title:'数学解题大招',teacher:'赵老师',duration:'12:00',durationSec:720,category:'数学',gradient:'linear-gradient(135deg,#43E97B,#38F9D7)',icon:'📐',url:'https://www.w3schools.com/html/mov_bbb.mp4',views:5600},
    {id:'video4',title:'英语口语训练',teacher:'王老师',duration:'15:45',durationSec:945,category:'英语',gradient:'linear-gradient(135deg,#4facfe,#00f2fe)',icon:'🗣️',url:'https://www.w3schools.com/html/movie.mp4',views:4300},
    {id:'video5',title:'勾股定理证明',teacher:'李老师',duration:'10:20',durationSec:620,category:'数学',gradient:'linear-gradient(135deg,#FF6B6B,#FF4757)',icon:'📐',url:'https://www.w3schools.com/html/mov_bbb.mp4',views:7800},
    {id:'video6',title:'一元二次方程',teacher:'孙老师',duration:'14:30',durationSec:870,category:'数学',gradient:'linear-gradient(135deg,#667eea,#764ba2)',icon:'🔢',url:'https://www.w3schools.com/html/movie.mp4',views:6500},
    {id:'video7',title:'力的合成与分解',teacher:'陈老师',duration:'13:15',durationSec:795,category:'物理',gradient:'linear-gradient(135deg,#4facfe,#00f2fe)',icon:'⚡',url:'https://www.w3schools.com/html/mov_bbb.mp4',views:5200},
    {id:'video8',title:'欧姆定律精讲',teacher:'林老师',duration:'12:00',durationSec:720,category:'物理',gradient:'linear-gradient(135deg,#FF9A63,#E87A4E)',icon:'💡',url:'https://www.w3schools.com/html/movie.mp4',views:4800},
    {id:'video9',title:'化学方程式配平',teacher:'周老师',duration:'11:30',durationSec:690,category:'化学',gradient:'linear-gradient(135deg,#43E97B,#38F9D7)',icon:'⚗️',url:'https://www.w3schools.com/html/mov_bbb.mp4',views:4100},
    {id:'video10',title:'质量守恒定律',teacher:'吴老师',duration:'10:45',durationSec:645,category:'化学',gradient:'linear-gradient(135deg,#f6d365,#fda085)',icon:'🧪',url:'https://www.w3schools.com/html/movie.mp4',views:3900},
    {id:'video11',title:'三角形全等证明',teacher:'刘老师',duration:'15:00',durationSec:900,category:'数学',gradient:'linear-gradient(135deg,#fa709a,#fee140)',icon:'📐',url:'https://www.w3schools.com/html/mov_bbb.mp4',views:5500},
    {id:'video12',title:'浮力计算方法',teacher:'张老师',duration:'13:45',durationSec:825,category:'物理',gradient:'linear-gradient(135deg,#667eea,#764ba2)',icon:'💧',url:'https://www.w3schools.com/html/movie.mp4',views:4700},
    {id:'video13',title:'溶液配制计算',teacher:'赵老师',duration:'12:30',durationSec:750,category:'化学',gradient:'linear-gradient(135deg,#FF6B6B,#FF4757)',icon:'🧬',url:'https://www.w3schools.com/html/mov_bbb.mp4',views:3600},
    {id:'video14',title:'函数图像变换',teacher:'王老师',duration:'14:15',durationSec:855,category:'数学',gradient:'linear-gradient(135deg,#4facfe,#00f2fe)',icon:'📈',url:'https://www.w3schools.com/html/movie.mp4',views:6200},
    {id:'video15',title:'机械效率计算',teacher:'李老师',duration:'11:00',durationSec:660,category:'物理',gradient:'linear-gradient(135deg,#43E97B,#38F9D7)',icon:'⚙️',url:'https://www.w3schools.com/html/mov_bbb.mp4',views:4300},
    {id:'video16',title:'酸碱盐反应规律',teacher:'陈老师',duration:'13:30',durationSec:810,category:'化学',gradient:'linear-gradient(135deg,#FF9A63,#E87A4E)',icon:'⚗️',url:'https://www.w3schools.com/html/movie.mp4',views:3800},
    {id:'video17',title:'圆与直线位置关系',teacher:'林老师',duration:'12:45',durationSec:765,category:'数学',gradient:'linear-gradient(135deg,#667eea,#764ba2)',icon:'⭕',url:'https://www.w3schools.com/html/mov_bbb.mp4',views:5100},
    {id:'video18',title:'电功率计算专题',teacher:'周老师',duration:'14:00',durationSec:840,category:'物理',gradient:'linear-gradient(135deg,#fa709a,#fee140)',icon:'⚡',url:'https://www.w3schools.com/html/movie.mp4',views:4600},
    {id:'video19',title:'金属活动性应用',teacher:'孙老师',duration:'11:15',durationSec:675,category:'化学',gradient:'linear-gradient(135deg,#4facfe,#00f2fe)',icon:'🔩',url:'https://www.w3schools.com/html/mov_bbb.mp4',views:3500},
    {id:'video20',title:'相似三角形判定',teacher:'吴老师',duration:'13:00',durationSec:780,category:'数学',gradient:'linear-gradient(135deg,#43E97B,#38F9D7)',icon:'📐',url:'https://www.w3schools.com/html/movie.mp4',views:4900},
    {id:'video21',title:'能量转化与守恒',teacher:'刘老师',duration:'12:15',durationSec:735,category:'物理',gradient:'linear-gradient(135deg,#FF6B6B,#FF4757)',icon:'🔋',url:'https://www.w3schools.com/html/mov_bbb.mp4',views:4200}
];'''

content = content.replace(old_video, new_video)

# 更新母题描述中的数量
content = content.replace('共10个音频课程', '共21个音频课程')
content = content.replace('精选21个视频课程 + 本地上传', '精选21个视频课程 + 本地上传')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("媒体数据修复完成!")
