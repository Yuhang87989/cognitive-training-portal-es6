#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接替换playPodcastCourse函数中的关键逻辑
"""

with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# 原来的关键代码
old_code = '''    // 使用本地 audioEl 而不是全局 currentAudio，确保正确播放
    audioEl.src = course.url || 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3';
    console.log('设置音频源:', audioEl.src);
    if (savedPositions[courseId]) audioEl.currentTime = savedPositions[courseId];
    audioEl.playbackRate = audioCtx.playbackSpeed;
    audioEl.volume = audioCtx.volume;
    
    // 播放音频并处理可能的错误
    audioEl.play().then(function() {
        console.log('音频播放成功');
        audioCtx.isPlaying = true;
        updatePlayButtons();
    }).catch(function(e) {
        console.error('音频播放失败:', e);
        // 自动播放被阻止时，提示用户
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
}'''

# 新的关键代码
new_code = '''    // 如果没有shareUrl，显示提示
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

if old_code in content:
    content = content.replace(old_code, new_code)
    print("✓ playPodcastCourse函数已更新")
else:
    print("✗ 未找到需要替换的代码块")
    # 检查是否已经替换过
    if 'getPodcastAudioUrl(course.shareUrl' in content:
        print("  函数可能已经被修改过")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
