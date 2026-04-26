import os

html_content = '''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no">
<title>认知训练门户</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
:root{--blue:#1A6BFF;--bg:#F5F6FA;--white:#FFFFFF;--text-dark:#333;--text-gray:#666;--text-light:#999;--orange:#FF9A5C;--cyan:#00D4AA;--purple:#8B5CF6;--green:#43E97B}
body{font-family:-apple-system,BlinkMacSystemFont,'PingFang SC',sans-serif;background:var(--bg);max-width:480px;margin:0 auto;min-height:100vh;padding-bottom:80px}
.header{background:linear-gradient(135deg,#1A6BFF,#4F8EFF);color:white;padding:14px;border-radius:0 0 24px 24px;box-shadow:0 4px 20px rgba(26,107,255,0.3)}
.header-top{display:flex;justify-content:space-between;align-items:center}
.app-logo{width:40px;height:40px;background:linear-gradient(135deg,#1A6BFF,#00D4AA);border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:22px}
.user-avatar{width:34px;height:34px;background:linear-gradient(135deg,#FFD4B8,#FFB6C1);border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:bold;color:#fff;cursor:pointer;position:relative}
.stats-bar{margin:12px 16px;display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
.stat-item{background:rgba(255,255,255,0.2);border-radius:10px;padding:8px;text-align:center}
.stat-value{font-size:15px;font-weight:bold}
.stat-label{font-size:9px;opacity:0.9}
.modules{padding:8px 12px;display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
.module{background:white;border-radius:12px;padding:10px 4px;text-align:center;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,0.06);transition:all 0.2s;position:relative;overflow:hidden}
.module::before{content:'';position:absolute;top:0;left:0;right:0;height:3px}
.module:nth-child(1)::before{background:linear-gradient(90deg,#667eea,#764ba2)}
.module:nth-child(2)::before{background:linear-gradient(90deg,#FF9A5C,#FFB87C)}
.module:nth-child(3)::before{background:linear-gradient(90deg,#00D4AA,#5EEAD4)}
.module:nth-child(4)::before{background:linear-gradient(90deg,#8B5CF6,#A78BFA)}
.module:nth-child(5)::before{background:linear-gradient(90deg,#F472B6,#F9A8D4)}
.module:nth-child(6)::before{background:linear-gradient(90deg,#FBBF24,#FCD34D)}
.module:nth-child(7)::before{background:linear-gradient(90deg,#6366F1,#818CF8)}
.module:nth-child(8)::before{background:linear-gradient(90deg,#10B981,#34D399)}
.module:nth-child(9)::before{background:linear-gradient(90deg,#EC4899,#F472B6)}
.module:nth-child(10)::before{background:linear-gradient(90deg,#14B8A6,#2DD4BF)}
.module:nth-child(11)::before{background:linear-gradient(90deg,#64748B,#94A3B8)}
.module:nth-child(12)::before{background:linear-gradient(90deg,#1A6BFF,#4F8EFF)}
.module:active{transform:scale(0.95)}
.module-icon{font-size:20px;margin-bottom:4px}
.module-name{font-size:10px;font-weight:600;color:#333;line-height:1.2}
.module-desc{font-size:8px;color:#999;margin-top:2px}
.page{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:var(--bg);z-index:100;flex-direction:column;overflow-y:auto}
.page.active{display:flex}
.page-header{background:white;padding:10px 14px;display:flex;align-items:center;border-bottom:1px solid #eee;box-shadow:0 2px 8px rgba(0,0,0,0.05);position:sticky;top:0;z-index:10}
.page-back{font-size:18px;cursor:pointer;padding:6px;color:var(--blue);min-width:36px}
.page-title{flex:1;font-size:15px;font-weight:bold;text-align:center}
.page-content{flex:1;overflow-y:auto;padding:10px}
.card{background:white;border-radius:14px;padding:14px;margin-bottom:10px;box-shadow:0 2px 10px rgba(0,0,0,0.04)}
.card-title{font-size:13px;font-weight:bold;margin-bottom:10px;display:flex;align-items:center;gap:6px}
.card-title::before{content:'';width:3px;height:14px;background:linear-gradient(180deg,var(--blue),var(--cyan));border-radius:2px}
.btn{background:linear-gradient(135deg,var(--blue),#4F8EFF);color:white;border:none;padding:10px 16px;border-radius:10px;cursor:pointer;font-size:13px;box-shadow:0 3px 10px rgba(26,107,255,0.3)}
.btn:active{transform:translateY(1px)}
.btn-secondary{background:#f0f0f0;color:#333;box-shadow:none}
.btn-small{padding:6px 12px;font-size:11px;width:auto}
.item{background:#f8f9fa;border-radius:10px;padding:10px;margin-bottom:8px;cursor:pointer}
.item-title{font-size:13px;font-weight:bold}
.item-desc{font-size:11px;color:#666;margin-top:2px}
.badge{display:inline-block;background:linear-gradient(135deg,var(--blue),var(--cyan));color:white;font-size:9px;padding:2px 6px;border-radius:8px;margin-left:6px}
.progress-bar{height:6px;background:#e0e0e0;border-radius:3px;margin-top:6px}
.progress-fill{height:100%;background:linear-gradient(90deg,var(--blue),var(--cyan));border-radius:3px;transition:width 0.3s}
.modal{position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.5);display:none;align-items:center;justify-content:center;z-index:2000;padding:16px}
.modal.show{display:flex}
.modal-content{background:white;border-radius:18px;padding:20px;width:100%;max-width:380px;max-height:85vh;overflow-y:auto}
.modal-title{font-size:16px;font-weight:bold;text-align:center;margin-bottom:14px}
.chat-container{flex:1;display:flex;flex-direction:column;background:#f8f9fa}
.chat-messages{flex:1;overflow-y:auto;padding:10px;max-height:400px}
.chat-msg{display:flex;gap:8px;margin-bottom:10px}
.chat-msg.user{flex-direction:row-reverse}
.chat-avatar{width:34px;height:34px;border-radius:50%;background:linear-gradient(135deg,#667eea,#764ba2);display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0}
.chat-msg.user .chat-avatar{background:linear-gradient(135deg,var(--orange),#FFB87C)}
.chat-bubble{max-width:75%;padding:8px 12px;border-radius:14px;background:white;font-size:13px;line-height:1.5}
.chat-msg.user .chat-bubble{background:linear-gradient(135deg,var(--blue),#4F8EFF);color:white}
.chat-input-area{padding:10px;background:white;border-top:1px solid #eee;display:flex;gap:6px;align-items:center}
.chat-input{flex:1;padding:8px 12px;border:1px solid #ddd;border-radius:18px;font-size:13px}
.chat-send{padding:8px 14px;background:linear-gradient(135deg,var(--blue),#4F8EFF);border:none;border-radius:18px;color:white;font-size:13px;cursor:pointer}
.bottom-nav{position:fixed;bottom:0;left:0;right:0;max-width:480px;margin:0 auto;background:white;border-radius:18px 18px 0 0;box-shadow:0 -4px 20px rgba(0,0,0,0.1);display:flex;padding:6px 0;z-index:50}
.nav-item{flex:1;display:flex;flex-direction:column;align-items:center;padding:6px;cursor:pointer}
.nav-icon{font-size:18px;margin-bottom:2px}
.nav-text{font-size:9px;color:#999}
.nav-item.active .nav-text{color:var(--blue);font-weight:600}
.toast{position:fixed;bottom:90px;left:50%;transform:translateX(-50%);background:rgba(0,0,0,0.8);color:white;padding:10px 20px;border-radius:18px;font-size:13px;z-index:9999;animation:fadeIn 0.3s}
@keyframes fadeIn{from{opacity:0;transform:translateX(-50%) translateY(15px)}to{opacity:1;transform:translateX(-50%) translateY(0)}}
.loading-dots{display:inline-flex;gap:3px}
.loading-dots span{width:6px;height:6px;background:var(--blue);border-radius:50%;animation:dot 1.4s infinite}
.loading-dots span:nth-child(1){animation-delay:-0.32s}
.loading-dots span:nth-child(2){animation-delay:-0.16s}
@keyframes dot{0%,80%,100%{transform:scale(0)}50%{transform:scale(1)}}
.thinking-options{display:grid;grid-template-columns:repeat(2,1fr);gap:6px}
.thinking-option{padding:8px;background:#f5f5f5;border-radius:8px;font-size:12px;text-align:center;cursor:pointer;border:2px solid transparent;transition:all 0.2s}
.thinking-option.selected{border-color:var(--blue);background:rgba(26,107,255,0.1)}
.thinking-option.correct{border-color:#43E97B;background:rgba(67,233,123,0.15)}
.thinking-option.wrong{border-color:#FF6B6B;background:rgba(255,107,107,0.15)}
.teacher-list{display:flex;gap:8px;padding:6px;overflow-x:auto}
.teacher-item{display:flex;flex-direction:column;align-items:center;padding:8px;border-radius:10px;cursor:pointer;background:white;border:2px solid transparent;flex-shrink:0;min-width:60px}
.teacher-item.active{border-color:var(--blue);background:rgba(26,107,255,0.1)}
.teacher-avatar{width:40px;height:40px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:20px}
.teacher-name{font-size:10px;font-weight:600;margin-top:2px}
.teacher-subject{font-size:8px;color:#999}
.calendar-grid{display:grid;grid-template-columns:repeat(7,1fr);gap:3px;margin-top:10px}
.calendar-day{aspect-ratio:1;display:flex;align-items:center;justify-content:center;border-radius:50%;font-size:10px;cursor:pointer}
.calendar-day.checked{background:linear-gradient(135deg,var(--blue),var(--cyan));color:white}
.calendar-day.today{background:rgba(255,154,92,0.2);color:var(--orange);font-weight:bold}
.calendar-day.disabled{color:#ccc;cursor:not-allowed}
.plan-task{display:flex;align-items:center;gap:10px;padding:10px;background:#f5f5f5;border-radius:10px;margin-bottom:6px;cursor:pointer}
.task-checkbox{width:20px;height:20px;border-radius:50%;border:2px solid var(--blue);display:flex;align-items:center;justify-content:center;flex-shrink:0}
.task-checkbox.checked{background:linear-gradient(135deg,var(--blue),var(--cyan));color:white;border-color:transparent}
.task-text{flex:1;font-size:12px}
.task-time{font-size:9px;color:#999}
.game-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:8px}
.game-btn{background:white;border-radius:14px;padding:12px;text-align:center;cursor:pointer;box-shadow:0 2px 10px rgba(0,0,0,0.06)}
.game-icon{font-size:28px;margin-bottom:4px}
.game-name{font-size:11px;font-weight:bold;color:#333}
.media-list{display:flex;flex-direction:column;gap:6px}
.media-item{display:flex;align-items:center;gap:10px;padding:10px;background:#f8f9fa;border-radius:10px;cursor:pointer}
.media-item.playing{background:linear-gradient(135deg,rgba(26,107,255,0.1),rgba(0,212,170,0.1));border:1px solid var(--blue)}
.media-thumb{width:40px;height:40px;background:linear-gradient(135deg,var(--blue),var(--cyan));border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:16px;color:white;flex-shrink:0}
.media-title{font-size:12px;font-weight:600}
.media-duration{font-size:10px;color:#999}
.player-container{background:white;border-radius:14px;padding:14px;margin-bottom:10px}
.player-progress{height:5px;background:#e0e0e0;border-radius:2.5px;margin:10px 0;cursor:pointer}
.player-progress-fill{height:100%;background:linear-gradient(90deg,var(--blue),var(--cyan));border-radius:2.5px;transition:width 0.1s}
.player-controls{display:flex;align-items:center;justify-content:center;gap:14px}
.player-btn{width:38px;height:38px;border-radius:50%;border:none;background:linear-gradient(135deg,var(--blue),#4F8EFF);color:white;display:flex;align-items:center;justify-content:center;font-size:14px;cursor:pointer}
.settings-item{display:flex;align-items:center;gap:10px;padding:10px;background:#f8f9fa;border-radius:10px;margin-bottom:6px;cursor:pointer}
.settings-icon{width:34px;height:34px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:14px}
.settings-title{font-size:12px;font-weight:600}
.settings-desc{font-size:9px;color:#999}
.radar-container{position:relative;width:260px;height:260px;margin:10px auto}
.dropdown{display:none;position:absolute;top:100%;right:0;background:white;border-radius:10px;box-shadow:0 4px 20px rgba(0,0,0,0.15);width:180px;z-index:1000;margin-top:6px}
.dropdown.show{display:block}
.dropdown-item{padding:12px 14px;display:flex;align-items:center;gap:8px;cursor:pointer;border-bottom:1px solid #f0f0f0;font-size:13px;color:#333}
.dropdown-item:last-child{border-bottom:none}
.dropdown-item.danger{color:#ff6b6b}
.dropdown-item:active{background:#f5f5f5}
.coin-card{display:flex;align-items:center;gap:8px;padding:10px;background:#f8f9fa;border-radius:10px;margin-bottom:6px;cursor:pointer;border:2px solid transparent}
.coin-card.selected{border-color:var(--blue);background:rgba(26,107,255,0.05)}
.coin-icon{font-size:18px}
.coin-amount{font-size:13px;font-weight:bold;color:var(--blue)}
.coin-price{font-size:11px;color:#999;margin-left:auto}
.flashcard{width:100%;max-width:280px;height:160px;margin:10px auto;perspective:1000px;cursor:pointer}
.flashcard-inner{width:100%;height:100%;position:relative;transform-style:preserve-3d;transition:transform 0.6s}
.flashcard.flipped .flashcard-inner{transform:rotateY(180deg)}
.flashcard-front,.flashcard-back{position:absolute;width:100%;height:100%;backface-visibility:hidden;display:flex;align-items:center;justify-content:center;border-radius:14px;padding:16px;text-align:center;font-size:13px;font-weight:600;box-shadow:0 4px 15px rgba(0,0,0,0.1)}
.flashcard-front{background:linear-gradient(135deg,var(--blue),#4F8EFF);color:white}
.flashcard-back{background:white;color:#333;transform:rotateY(180deg);border:2px solid var(--blue)}
.timer-display{font-size:42px;font-weight:bold;color:var(--blue);text-align:center;font-family:monospace}
.checkin-btn{width:70px;height:70px;border-radius:50%;background:linear-gradient(135deg,var(--blue),var(--cyan));color:white;border:none;font-size:13px;font-weight:bold;cursor:pointer;box-shadow:0 4px 15px rgba(26,107,255,0.4)}
.checkin-btn.checked{background:#ccc;box-shadow:none;cursor:not-allowed}
.growth-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}
.growth-item{background:white;border-radius:14px;padding:16px;text-align:center;cursor:pointer;box-shadow:0 2px 10px rgba(0,0,0,0.06)}
.growth-icon{font-size:32px;margin-bottom:6px}
.growth-name{font-size:12px;font-weight:600;color:#333}
.growth-desc{font-size:10px;color:#999;margin-top:2px}
.practice-card{background:white;border-radius:12px;padding:14px;margin-bottom:10px}
.practice-question{font-size:13px;margin-bottom:10px;line-height:1.5}
.practice-result{padding:8px;border-radius:6px;margin-top:6px;font-size:12px}
.practice-result.correct{background:#e8f5e9;color:#2e7d32}
.practice-result.wrong{background:#ffebee;color:#c62828}
.topic-card{background:white;border-radius:12px;padding:12px;margin-bottom:8px;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,0.05)}
.topic-header{padding:12px;color:white;border-radius:8px 8px 0 0}
.topic-title{font-size:13px;font-weight:600}
.thinking-type-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.thinking-type-item{background:white;border-radius:12px;padding:10px;text-align:center;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,0.05)}
.thinking-type-icon{font-size:22px;margin-bottom:4px}
.thinking-type-name{font-size:10px;font-weight:600}
.upload-area{border:2px dashed #ddd;border-radius:10px;padding:16px;text-align:center;cursor:pointer}
.upload-icon{font-size:28px;color:#999;margin-bottom:6px}
.upload-text{font-size:11px;color:#666}
.upload-preview{width:100%;height:160px;background:#f0f0f0;border-radius:8px;margin:0 auto 10px;display:flex;align-items:center;justify-content:center;overflow:hidden}
.upload-preview img{max-width:100%;max-height:100%;object-fit:contain}
.real-game-container{width:100%;max-width:300px;margin:0 auto}
.game-board-real{background:#000;border-radius:8px;position:relative;overflow:hidden}
.game-score-display{text-align:center;font-size:16px;font-weight:bold;color:var(--blue);padding:8px}
.card-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;max-width:280px;margin:0 auto}
.memory-card{aspect-ratio:1;background:linear-gradient(135deg,var(--blue),var(--cyan));border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:28px;cursor:pointer;transition:transform 0.3s}
.memory-card.flipped{background:white;transform:rotateY(180deg)}
.memory-card.matched{background:#43E97B;opacity:0.6}
.hammer-area{position:relative;width:100%;height:220px;background:linear-gradient(180deg,#87CEEB 0%,#98D8AA 100%);border-radius:10px;overflow:hidden}
.mole{width:44px;height:44px;background:#8B4513;border-radius:50%;position:absolute;bottom:0;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:22px;transition:transform 0.15s}
.mole.hit{transform:scale(0.8) translateY(10px)}
.connect-grid{display:grid;grid-template-columns:repeat(6,1fr);gap:4px;padding:10px}
.connect-item{aspect-ratio:1;background:white;border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:20px;cursor:pointer;border:2px solid #eee;transition:all 0.2s}
.connect-item.selected{border-color:var(--blue);background:rgba(26,107,255,0.1)}
.connect-item.matched{background:#43E97B;animation:matchPop 0.3s}
.eliminate-grid{display:grid;grid-template-columns:repeat(6,1fr);gap:4px;padding:10px}
.eliminate-item{aspect-ratio:1;background:white;border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:22px;cursor:pointer;border:2px solid #eee;transition:all 0.2s}
.eliminate-item.selected{border-color:var(--blue);transform:scale(1.1)}
.eliminate-item.matched{background:#43E97B;animation:matchPop 0.3s}
@keyframes matchPop{0%{transform:scale(1)}50%{transform:scale(1.3)}100%{transform:scale(0)}}
.controls-row{display:flex;gap:8px;justify-content:center;margin-top:10px}
.game-dpad{display:grid;grid-template-columns:repeat(3,50px);grid-template-rows:repeat(3,50px);gap:4px;margin:0 auto}
.dpad-btn{background:white;border:none;border-radius:8px;font-size:20px;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 6px rgba(0,0,0,0.2)}
.game-fullscreen{position:fixed;top:0;left:0;right:0;bottom:0;background:#1a1a2e;z-index:1000;display:flex;flex-direction:column}
.game-full-header{height:50px;background:linear-gradient(135deg,var(--blue),#4F8EFF);display:flex;align-items:center;padding:0 10px;color:white}
.game-full-area{flex:1;display:flex;align-items:center;justify-content:center;overflow:hidden}
.game-full-controls{height:90px;background:rgba(0,0,0,0.3);display:flex;align-items:center;justify-content:center;gap:10px;padding:10px}
.schulte-grid{display:grid;gap:4px;max-width:280px;margin:0 auto}
.schulte-cell{aspect-ratio:1;background:white;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:bold;color:#333;cursor:pointer}
.video-player-container{width:100%;background:#000;border-radius:10px;overflow:hidden;margin-bottom:10px}
.video-player{width:100%;display:block}
.video-controls{background:rgba(0,0,0,0.8);padding:10px}
.video-progress{width:100%;height:4px;background:#555;border-radius:2px;cursor:pointer;margin-bottom:8px}
.video-progress-fill{height:100%;background:var(--blue);border-radius:2px}
.video-control-btns{display:flex;align-items:center;justify-content:space-between}
.video-time{font-size:11px;color:#fff}
.pagination{display:flex;align-items:center;justify-content:center;gap:8px;margin-top:12px}
.pagination-btn{background:var(--blue);color:white;border:none;padding:6px 14px;border-radius:16px;font-size:12px;cursor:pointer}
.pagination-btn:disabled{background:#ccc;cursor:not-allowed}
.page-info{font-size:12px;color:#666}
.speed-control{display:flex;gap:4px;margin-left:auto}
.speed-btn{padding:4px 8px;background:rgba(255,255,255,0.2);border:none;border-radius:4px;color:white;font-size:11px;cursor:pointer}
.speed-btn.active{background:var(--blue)}
.week-progress{display:flex;gap:4px;margin-top:8px}
.week-dot{width:8px;height:8px;border-radius:50%;background:#ddd}
.week-dot.active{background:var(--blue)}
.week-dot.completed{background:var(--green)}
</style>
</head>
<body>
'''

with open('./cognitive-training-portal/full.html', 'w', encoding='utf-8') as f:
    f.write(html_content)
    f.write('''
<!-- 首页 -->
<div class="header">
<div class="header-top">
<div style="display:flex;align-items:center"><span style="font-size:20px">🧠</span><span style="font-size:15px;font-weight:bold;margin-left:5px">认知训练</span></div>
<div style="display:flex;align-items:center;gap:10px">
<div style="font-size:12px"><span style="opacity:0.8">积分:</span> <span id="header-points" style="font-weight:bold">0</span></div>
<div style="position:relative">
<div class="user-avatar" onclick="toggleMenu()">邱</div>
<div class="dropdown" id="menu">
<div class="dropdown-item" onclick="openPage('settings')"><span>👤</span><span>个人设置</span></div>
<div class="dropdown-item" onclick="openApiSettings()"><span>🔑</span><span>API设置</span></div>
<div class="dropdown-item" onclick="openRecharge()"><span>💰</span><span>充值金币</span></div>
<div class="dropdown-item danger" onclick="clearData()"><span>🗑️</span><span>清除数据</span></div>
</div>
</div>
</div>
</div>

<div class="stats-bar">
<div class="stat-item"><div class="stat-value" id="stat-questions" style="color:white">0</div><div class="stat-label" style="color:rgba(255,255,255,0.8)">提问</div></div>
<div class="stat-item"><div class="stat-value" id="stat-correct" style="color:white">0%</div><div class="stat-label" style="color:rgba(255,255,255,0.8)">正确率</div></div>
<div class="stat-item"><div class="stat-value" id="stat-minutes" style="color:white">0</div><div class="stat-label" style="color:rgba(255,255,255,0.8)">分钟</div></div>
<div class="stat-item"><div class="stat-value" id="stat-streak" style="color:white">0</div><div class="stat-label" style="color:rgba(255,255,255,0.8)">连续</div></div>
</div>

<div class="modules">
<div class="module" onclick="openPage('avatar')"><div class="module-icon">🎓</div><div class="module-name">AI数字分身</div><div class="module-desc">5导师对话</div></div>
<div class="module" onclick="openPage('practice')"><div class="module-icon">🎯</div><div class="module-name">AI精准练</div><div class="module-desc">薄弱点诊断</div></div>
<div class="module" onclick="openPage('map')"><div class="module-icon">🧠</div><div class="module-name">认知地图</div><div class="module-desc">六维雷达图</div></div>
<div class="module" onclick="openPage('plan')"><div class="module-icon">📅</div><div class="module-name">学习计划</div><div class="module-desc">Week1-6</div></div>
<div class="module" onclick="openPage('topics')"><div class="module-icon">📚</div><div class="module-name">母题训练</div><div class="module-desc">363道母题</div></div>
<div class="module" onclick="openPage('method')"><div class="module-icon">💡</div><div class="module-name">学霸方法</div><div class="module-desc">6大方法</div></div>
<div class="module" onclick="openPage('thinking')"><div class="module-icon">🧩</div><div class="module-name">思维训练</div><div class="module-desc">9种思维</div></div>
<div class="module" onclick="openPage('games')"><div class="module-icon">🎮</div><div class="module-name">训练游戏</div><div class="module-desc">16款游戏</div></div>
<div class="module" onclick="openPage('podcast')"><div class="module-icon">🎧</div><div class="module-name">播客课堂</div><div class="module-desc">21课程</div></div>
<div class="module" onclick="openPage('video')"><div class="module-icon">🎬</div><div class="module-name">视频课堂</div><div class="module-desc">多格式支持</div></div>
<div class="module" onclick="openPage('growth')"><div class="module-icon">🌱</div><div class="module-name">成长中心</div><div class="module-desc">打卡+专注</div></div>
<div class="module" onclick="openPage('deepseek')"><div class="module-icon">🤖</div><div class="module-name">DeepSeek助手</div><div class="module-desc">AI问答</div></div>
</div>

<div class="bottom-nav">
<div class="nav-item active" onclick="switchTab('home', this)"><div class="nav-icon">🏠</div><div class="nav-text">首页</div></div>
<div class="nav-item" onclick="switchTab('avatar', this)"><div class="nav-icon">👨‍🏫</div><div class="nav-text">老师</div></div>
<div class="nav-item" onclick="switchTab('games', this)"><div class="nav-icon">🎮</div><div class="nav-text">训练</div></div>
<div class="nav-item" onclick="switchTab('map', this)"><div class="nav-icon">🧠</div><div class="nav-text">认知</div></div>
<div class="nav-item" onclick="switchTab('growth', this)"><div class="nav-icon">🌱</div><div class="nav-text">成长</div></div>
</div>

<div id="page-avatar" class="page"><div class="page-header"><div class="page-back" onclick="closePage()">←</div><div class="page-title">🎓 AI数字分身</div></div><div class="page-content" id="content-avatar"></div></div>
<div id="page-practice" class="page"><div class="page-header"><div class="page-back" onclick="closePage()">←</div><div class="page-title">🎯 AI精准练</div></div><div class="page-content" id="content-practice"></div></div>
<div id="page-map" class="page"><div class="page-header"><div class="page-back" onclick="closePage()">←</div><div class="page-title">🧠 认知地图</div></div><div class="page-content" id="content-map"></div></div>
<div id="page-plan" class="page"><div class="page-header"><div class="page-back" onclick="closePage()">←</div><div class="page-title">📅 学习计划</div></div><div class="page-content" id="content-plan"></div></div>
<div id="page-topics" class="page"><div class="page-header"><div class="page-back" onclick="closePage()">←</div><div class="page-title">📚 母题训练</div></div><div class="page-content" id="content-topics"></div></div>
<div id="page-method" class="page"><div class="page-header"><div class="page-back" onclick="closePage()">←</div><div class="page-title">💡 学霸方法</div></div><div class="page-content" id="content-method"></div></div>
<div id="page-thinking" class="page"><div class="page-header"><div class="page-back" onclick="closePage()">←</div><div class="page-title">🧩 思维训练</div></div><div class="page-content" id="content-thinking"></div></div>
<div id="page-games" class="page"><div class="page-header"><div class="page-back" onclick="closePage()">←</div><div class="page-title">🎮 训练游戏</div></div><div class="page-content" id="content-games"></div></div>
<div id="page-podcast" class="page"><div class="page-header"><div class="page-back" onclick="closePage()">←</div><div class="page-title">🎧 播客课堂</div></div><div class="page-content" id="content-podcast"></div></div>
<div id="page-video" class="page"><div class="page-header"><div class="page-back" onclick="closePage()">←</div><div class="page-title">🎬 视频课堂</div></div><div class="page-content" id="content-video"></div></div>
<div id="page-growth" class="page"><div class="page-header"><div class="page-back" onclick="closePage()">←</div><div class="page-title">🌱 成长中心</div></div><div class="page-content" id="content-growth"></div></div>
<div id="page-settings" class="page"><div class="page-header"><div class="page-back" onclick="closePage()">←</div><div class="page-title">⚙️ 设置</div></div><div class="page-content" id="content-settings"></div></div>
<div id="page-deepseek" class="page"><div class="page-header"><div class="page-back" onclick="closePage()">←</div><div class="page-title">🤖 DeepSeek助手</div></div><div class="page-content" id="content-deepseek"></div></div>

<div id="page-game-full" class="page"><div class="game-fullscreen" id="game-fullscreen"></div></div>

<div class="modal" id="detail-modal"><div class="modal-content" id="detail-content"></div></div>

<audio id="audio-player" style="display:none"></audio>
''')

print("HTML structure written successfully")
