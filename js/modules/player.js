// 版本: V144 - 视频播放器优化版本

// ========== 视频播放器全局状态 ==========
window.videoCtx = {
    isPlaying: false,
    playbackSpeed: 1,
    volume: 0.8,
    lastVolume: 0.8,
    currentVideo: null,
    isInitialized: false
};

function playPodcast(title, id) { if (id) { for (var i = 0; i < podcastCourses.length; i++) { if (podcastCourses[i].id === id) { playPodcastCourse(id); return; } } } for (var i = 0; i < podcastCourses.length; i++) { if (podcastCourses[i].title === title) { playPodcastCourse(podcastCourses[i].id); return; } } showToast('播放: ' + title); }

function playVideo(title, url) {
    document.getElementById('vp-title').textContent = title;
    document.getElementById('video-player-modal').classList.add('show');
    vpVideo = document.getElementById('vp-video');
    vpVideo.src = url;
    vpVideo.onloadedmetadata = () => { document.getElementById('vp-time').textContent = '0:00 / ' + formatTime(vpVideo.duration); };
    vpVideo.ontimeupdate = () => {
        if (vpVideo.duration) {
            document.getElementById('vp-progress-bar').style.width = (vpVideo.currentTime/vpVideo.duration*100) + '%';
            document.getElementById('vp-time').textContent = formatTime(vpVideo.currentTime) + ' / ' + formatTime(vpVideo.duration);
        }
    };
    vpVideo.onplay = () => { vpPlaying = true; document.getElementById('vp-play-btn').textContent = '⏸'; };
    vpVideo.onpause = () => { vpPlaying = false; document.getElementById('vp-play-btn').textContent = '▶'; };
    vpVideo.play();
}

function playPodcastCourse(courseId) {
    var audioEl = document.getElementById('hidden-audio');
    if (!audioEl) {
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
    var courseTeacherEl = document.getElementById('ap-course-teacher');
    if (titleEl) titleEl.textContent = '音频课程';
    if (coverEl) { coverEl.innerHTML = course.icon; coverEl.style.background = course.gradient; }
    if (courseTitleEl) courseTitleEl.textContent = course.title;
    if (courseTeacherEl) courseTeacherEl.textContent = course.teacher + ' · ' + course.category;
    
    if (!course.shareUrl) {
        showToast('该播客暂不可用');
        return;
    }
    
    // 显示播放器UI
    showMiniPlayer(course);
    var playerEl = document.getElementById('audio-player-fullscreen');
    var coverPlayingEl = document.getElementById('ap-cover');
    if (playerEl) playerEl.classList.add('show');
    if (coverPlayingEl) coverPlayingEl.classList.add('playing');
    updatePodcastListState(courseId);
    
    // 尝试获取播客数据（包含字幕文本）
    showToast('正在加载播客...');
    fetch(course.shareUrl, {redirect: 'follow'}).then(function(resp) {
        if (!resp.ok) throw new Error('fetch failed');
        return resp.json();
    }).then(function(podcastData) {
        // 保存字幕数据供TTS使用
        if (podcastData.captions) {
            window._currentPodcastCaptions = podcastData.captions;
        }
        // 保存audio_uri
        var audioUri = podcastData.audio_uri;
        if (audioUri) {
            window._currentAudioUri = audioUri;
        }
        
        // 尝试获取签名音频URL
        return tryGetSignedAudioUrl(audioUri, courseId, audioEl);
    }).then(function(signedUrl) {
        if (signedUrl) {
            // 有签名URL，直接播放原声
            audioEl.src = signedUrl;
            if (savedPositions[courseId]) audioEl.currentTime = savedPositions[courseId];
            audioEl.playbackRate = audioCtx.playbackSpeed;
            audioEl.volume = audioCtx.volume;
            audioEl.play().then(function() {
                audioCtx.isPlaying = true;
                updatePlayButtons();
                showToast('正在播放: ' + course.title);
            }).catch(function(e) {
                showToast('播放失败，尝试语音朗读模式');
                startPodcastTTS();
            });
        } else {
            // 没有签名URL，使用TTS朗读模式
            showToast('使用语音朗读模式播放');
            startPodcastTTS();
        }
    }).catch(function(e) {
        console.error('播客加载失败:', e);
        showToast('加载失败，尝试语音朗读');
        startPodcastTTS();
    });
}

function playVideoCourse(courseId) {
    var course = null;
    for (var i = 0; i < videoCourses.length; i++) { if (videoCourses[i].id === courseId) { course = videoCourses[i]; break; } }
    if (!course) return;
    videoCtx.currentVideo = course;
    var titleEl = document.getElementById('evp-title');
    if (titleEl) titleEl.textContent = course.title;
    evpVideo.src = course.url;
    evpVideo.playbackRate = videoCtx.playbackSpeed;
    evpVideo.volume = videoCtx.volume;
    var playerEl = document.getElementById('enhanced-video-player');
    var bigPlayEl = document.getElementById('evp-big-play');
    if (playerEl) playerEl.style.display = 'flex';
    if (bigPlayEl) bigPlayEl.style.display = 'none';
    updateVideoListState(courseId);
    evpVideo.play().then(function() { videoCtx.isPlaying = true; showToast('正在播放: ' + course.title); }).catch(function(e) { videoCtx.isPlaying = false; });
}

function playLocalAudio(audioId) {
    const user = getCurrentUserData();
    const audio = user?.localAudios?.find(a => a.id === audioId);
    if (!audio) return;

    // 播放音频
    const tempAudio = new Audio(audio.url);
    tempAudio.play();
    showToast('正在播放: ' + audio.title);
}

// ============================================================
// V152: 视频压缩功能
// 使用 Canvas + MediaRecorder API 进行浏览器端压缩
// ============================================================

// 视频压缩参数
var VIDEO_COMPRESS_CONFIG = {
    maxWidth: 854,       // 最大宽度 480p
    maxHeight: 480,      // 最大高度
    videoBitrate: 1000000, // 1Mbps
    audioBitrate: 128000,  // 128kbps
    fps: 30,             // 帧率
    skipSize: 5 * 1024 * 1024 // 5MB以下跳过压缩
};

// 视频压缩函数
// 参数: file - 原始文件, onProgress - 进度回调 (0-100), onComplete - 完成回调 (compressedBlob or null), onError - 错误回调
function compressVideo(file, onProgress, onComplete, onError) {
    // 检查文件大小，小文件跳过压缩
    if (file.size < VIDEO_COMPRESS_CONFIG.skipSize) {
        console.log('[VideoCompress] 文件太小，跳过压缩:', (file.size / 1024 / 1024).toFixed(2), 'MB');
        onComplete(null); // 返回null表示不压缩
        return;
    }
    
    // 检查浏览器支持
    if (!window.MediaRecorder || !window.MediaSource) {
        console.warn('[VideoCompress] 浏览器不支持视频压缩');
        onComplete(null);
        return;
    }
    
    // 显示进度UI
    var progressEl = document.getElementById('video-compress-progress');
    if (progressEl) {
        progressEl.style.display = 'block';
        progressEl.querySelector('.progress-fill').style.width = '0%';
        progressEl.querySelector('.progress-text').textContent = '准备压缩...';
    }
    
    // 创建视频元素用于读取原视频
    var video = document.createElement('video');
    video.setAttribute('playsinline', '');
    video.setAttribute('webkit-playsinline', '');
    video.muted = true; // 静音以允许播放跨域视频
    
    var tempUrl = URL.createObjectURL(file);
    video.src = tempUrl;
    
    video.onloadedmetadata = function() {
        var duration = video.duration;
        var originalWidth = video.videoWidth;
        var originalHeight = video.videoHeight;
        
        console.log('[VideoCompress] 原视频:', originalWidth, 'x', originalHeight, '时长:', duration, '秒');
        
        // 计算缩放后的尺寸
        var scale = 1;
        if (originalWidth > VIDEO_COMPRESS_CONFIG.maxWidth || originalHeight > VIDEO_COMPRESS_CONFIG.maxHeight) {
            var scaleW = VIDEO_COMPRESS_CONFIG.maxWidth / originalWidth;
            var scaleH = VIDEO_COMPRESS_CONFIG.maxHeight / originalHeight;
            scale = Math.min(scaleW, scaleH);
        }
        
        var targetWidth = Math.floor(originalWidth * scale);
        var targetHeight = Math.floor(originalHeight * scale);
        
        // 确保尺寸是偶数（编码要求）
        targetWidth = targetWidth - (targetWidth % 2);
        targetHeight = targetHeight - (targetHeight % 2);
        
        console.log('[VideoCompress] 目标尺寸:', targetWidth, 'x', targetHeight);
        
        // 更新进度
        if (onProgress) onProgress(10);
        if (progressEl) {
            progressEl.querySelector('.progress-text').textContent = '开始压缩...';
        }
        
        // 创建Canvas
        var canvas = document.createElement('canvas');
        canvas.width = targetWidth;
        canvas.height = targetHeight;
        var ctx = canvas.getContext('2d');
        
        // 确定输出格式（优先webm，备用mp4）
        var mimeType = 'video/webm;codecs=vp9';
        if (!MediaRecorder.isTypeSupported(mimeType)) {
            mimeType = 'video/webm;codecs=vp8';
        }
        if (!MediaRecorder.isTypeSupported(mimeType)) {
            mimeType = 'video/webm';
        }
        if (!MediaRecorder.isTypeSupported(mimeType)) {
            mimeType = 'video/mp4';
        }
        
        console.log('[VideoCompress] 使用格式:', mimeType);
        
        // 创建MediaStream
        var stream = canvas.captureStream(VIDEO_COMPRESS_CONFIG.fps);
        
        // 添加音频轨道（如果有的话）
        if (file.type.indexOf('audio') === -1) {
            // 尝试从视频中获取音频
            try {
                var audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                var source = audioCtx.createMediaElementSource(video);
                var destination = audioCtx.createMediaStreamDestination();
                source.connect(destination);
                source.connect(audioCtx.destination);
                
                var audioTrack = destination.stream.getAudioTracks()[0];
                if (audioTrack) {
                    stream.addTrack(audioTrack);
                }
            } catch(e) {
                console.warn('[VideoCompress] 无法提取音频:', e);
            }
        }
        
        // 创建MediaRecorder
        var mediaRecorder;
        try {
            var options = {
                mimeType: mimeType,
                videoBitsPerSecond: VIDEO_COMPRESS_CONFIG.videoBitrate,
                audioBitsPerSecond: VIDEO_COMPRESS_CONFIG.audioBitrate
            };
            mediaRecorder = new MediaRecorder(stream, options);
        } catch(e) {
            console.error('[VideoCompress] MediaRecorder创建失败:', e);
            URL.revokeObjectURL(tempUrl);
            if (onError) onError(e);
            return;
        }
        
        var chunks = [];
        mediaRecorder.ondataavailable = function(e) {
            if (e.data && e.data.size > 0) {
                chunks.push(e.data);
            }
        };
        
        mediaRecorder.onstop = function() {
            var blob = new Blob(chunks, { type: mimeType });
            console.log('[VideoCompress] 压缩完成:', (blob.size / 1024 / 1024).toFixed(2), 'MB', 
                        '压缩率:', (blob.size / file.size * 100).toFixed(1) + '%');
            
            // 清理
            URL.revokeObjectURL(tempUrl);
            try { video.pause(); video.src = ''; } catch(e) {}
            try { stream.getTracks().forEach(function(t) { t.stop(); }); } catch(e) {}
            
            // 隐藏进度UI
            if (progressEl) {
                progressEl.style.display = 'none';
            }
            
            // 只有压缩后更小才使用压缩版本
            if (blob.size < file.size * 0.9) {
                if (onProgress) onProgress(100);
                if (onComplete) onComplete(blob);
            } else {
                console.log('[VideoCompress] 压缩效果不明显，使用原文件');
                if (onComplete) onComplete(null);
            }
        };
        
        mediaRecorder.onerror = function(e) {
            console.error('[VideoCompress] 录制错误:', e);
            URL.revokeObjectURL(tempUrl);
            if (progressEl) {
                progressEl.style.display = 'none';
            }
            if (onError) onError(e);
        };
        
        // 开始录制
        mediaRecorder.start(100); // 每100ms收集一次数据
        
        // 播放视频并绘制到Canvas
        video.currentTime = 0;
        video.play();
        
        var startTime = Date.now();
        var estimatedDuration = duration * 1000;
        
        var drawFrame = function() {
            if (!video.paused && !video.ended && video.currentTime < duration) {
                try {
                    ctx.drawImage(video, 0, 0, targetWidth, targetHeight);
                } catch(e) {}
                
                // 更新进度
                var elapsed = Date.now() - startTime;
                var progress = Math.min(90, Math.floor((elapsed / estimatedDuration) * 80) + 10);
                if (onProgress) onProgress(progress);
                if (progressEl) {
                    progressEl.querySelector('.progress-fill').style.width = progress + '%';
                    progressEl.querySelector('.progress-text').textContent = '压缩中 ' + progress + '%';
                }
                
                requestAnimationFrame(drawFrame);
            } else {
                // 录制完成
                setTimeout(function() {
                    try { mediaRecorder.stop(); } catch(e) {}
                }, 500);
            }
        };
        
        video.onseeked = function() {
            drawFrame();
        };
        
        // 超时保护（30秒）
        setTimeout(function() {
            if (mediaRecorder && mediaRecorder.state === 'recording') {
                console.warn('[VideoCompress] 压缩超时');
                try { mediaRecorder.stop(); } catch(e) {}
                URL.revokeObjectURL(tempUrl);
                if (progressEl) {
                    progressEl.style.display = 'none';
                }
                if (onComplete) onComplete(null);
            }
        }, 30000);
    };
    
    video.onerror = function(e) {
        console.error('[VideoCompress] 视频读取失败:', e);
        URL.revokeObjectURL(tempUrl);
        if (progressEl) {
            progressEl.style.display = 'none';
        }
        if (onError) onError(e);
        if (onComplete) onComplete(null);
    };
}

// 将压缩进度UI添加到页面
function insertVideoCompressProgressUI() {
    if (document.getElementById('video-compress-progress')) return;
    
    var container = document.createElement('div');
    container.id = 'video-compress-progress';
    container.style.cssText = 'display:none;position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);' +
        'background:rgba(0,0,0,0.85);padding:24px;border-radius:16px;z-index:999999;' +
        'min-width:280px;text-align:center;color:white;box-shadow:0 4px 20px rgba(0,0,0,0.3);';
    container.innerHTML = 
        '<div style="font-size:16px;font-weight:600;margin-bottom:16px;">📹 视频压缩中</div>' +
        '<div style="background:#333;border-radius:8px;height:12px;overflow:hidden;margin-bottom:12px;">' +
        '<div class="progress-fill" style="height:100%;background:linear-gradient(90deg,#43E97B,#38F9D7);' +
        'width:0%;transition:width 0.3s;"></div></div>' +
        '<div class="progress-text" style="font-size:13px;color:#ccc;">准备中...</div>' +
        '<div style="font-size:11px;color:#888;margin-top:8px;">请稍候，大视频需要处理时间</div>';
    
    document.body.appendChild(container);
}

// 页面加载时插入进度UI
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', insertVideoCompressProgressUI);
} else {
    insertVideoCompressProgressUI();
}

// Window exports for video compression
window.compressVideo = compressVideo;
window.VIDEO_COMPRESS_CONFIG = VIDEO_COMPRESS_CONFIG;

function playLocalVideo(videoId) {
    var user = getCurrentUserData();
    var video = user && user.localVideos ? user.localVideos.find(function(v) { return v.id === videoId; }) : null;
    if (!video) {
        showToast('视频信息不存在');
        return;
    }
    
    // 显示加载提示
    showToast('正在加载视频...');
    
    // 尝试从IndexedDB读取视频文件
    getVideoFile(videoId).then(function(blob) {
        if (blob) {
            // 生成临时 URL 播放
            var videoUrl = URL.createObjectURL(blob);
            openEnhancedVideoPlayer(video.title, videoUrl, videoId);
        } else {
            // 视频文件已丢失，尝试内存备用方案
            tryPlayFromMemoryFallback(videoId, video);
        }
    }).catch(function(e) {
        console.error('IndexedDB读取失败，尝试备用方案:', e);
        tryPlayFromMemoryFallback(videoId, video);
    });
}

// V152: 内存备用播放方案
// 如果IndexedDB读取失败，尝试使用上传时保存的内存引用
function tryPlayFromMemoryFallback(videoId, videoMeta) {
    console.log('[VideoPlay] 尝试备用播放方案:', videoId);
    
    // 检查是否有内存中的视频文件缓存
    if (window._uploadedVideos && window._uploadedVideos[videoId]) {
        var cachedFile = window._uploadedVideos[videoId];
        console.log('[VideoPlay] 找到内存缓存文件');
        
        var videoUrl = URL.createObjectURL(cachedFile);
        openEnhancedVideoPlayer(videoMeta.title, videoUrl, videoId);
        return;
    }
    
    // 检查是否可以从localStorage获取基本信息并提示用户
    if (videoMeta && videoMeta.title) {
        showToast('视频文件已丢失，请重新上传: ' + videoMeta.title);
    } else {
        showToast('视频文件已丢失，请重新上传');
    }
    
    // 标记需要重新上传
    if (videoMeta && videoMeta.id) {
        markVideoForReupload(videoMeta.id);
    }
}

// 标记视频需要重新上传
function markVideoForReupload(videoId) {
    try {
        var user = getCurrentUserData();
        if (user && user.localVideos) {
            for (var i = 0; i < user.localVideos.length; i++) {
                if (user.localVideos[i].id === videoId) {
                    user.localVideos[i].needsReupload = true;
                    syncUserData(user);
                    break;
                }
            }
        }
    } catch(e) {
        console.error('标记失败:', e);
    }
}

function playMediaCourse(courseId) {
    var course = null;
    for (var i = 0; i < allMediaCourses.length; i++) {
        if (allMediaCourses[i].id === courseId) {
            course = allMediaCourses[i];
            break;
        }
    }
    if (!course) return;
    
    mediaPlayer.currentMedia = course;
    mediaPlayer.currentIndex = -1;
    for (var i = 0; i < allMediaCourses.length; i++) {
        if (allMediaCourses[i].id === courseId) {
            mediaPlayer.currentIndex = i;
            break;
        }
    }
    
    mediaPlayer.isAudio = (course.type === 'audio');
    
    // 更新UI
    var typeLabel = document.getElementById('mp-type-label');
    var audioCover = document.getElementById('mp-audio-cover');
    var videoEl = document.getElementById('mp-video-element');
    var titleEl = document.getElementById('mp-title');
    var teacherEl = document.getElementById('mp-teacher');
    
    if (typeLabel) typeLabel.textContent = mediaPlayer.isAudio ? '🎧 音频课程' : '📺 视频课程';
    
    if (mediaPlayer.isAudio) {
        if (audioCover) { audioCover.style.display = 'flex'; audioCover.innerHTML = course.icon; audioCover.style.background = course.gradient; }
        if (videoEl) videoEl.style.display = 'none';
        var audioEl = document.getElementById('mp-audio-element');
        if (audioEl) { audioEl.src = course.url; audioEl.playbackRate = mediaPlayer.playbackSpeed; audioEl.volume = mediaPlayer.volume; audioEl.play().catch(function(e) {}); }
    } else {
        if (audioCover) audioCover.style.display = 'none';
        if (videoEl) { videoEl.style.display = 'block'; videoEl.src = course.url; videoEl.playbackRate = mediaPlayer.playbackSpeed; videoEl.volume = mediaPlayer.volume; videoEl.play().catch(function(e) {}); }
    }
    
    if (titleEl) titleEl.textContent = course.title;
    if (teacherEl) teacherEl.textContent = course.teacher + ' · ' + course.category;
    
    // 恢复播放进度
    var audioEl = document.getElementById('mp-audio-element');
    var videoEl = document.getElementById('mp-video-element');
    if (mediaPlayer.savedPositions[courseId]) {
        if (mediaPlayer.isAudio && audioEl) audioEl.currentTime = mediaPlayer.savedPositions[courseId];
        if (!mediaPlayer.isAudio && videoEl) videoEl.currentTime = mediaPlayer.savedPositions[courseId];
    }
    
    // 显示播放器
    var playerEl = document.getElementById('media-player');
    if (playerEl) playerEl.style.display = 'flex';
    
    // 更新列表状态
    updateMediaListState(courseId);
    
    showToast('正在播放: ' + course.title);
}

function playAudioPos(pos) {
    const freqs = [440, 554, 659];
    playAudioTone3(freqs[pos]);
    const isCorrect = pos === audioSequence[audioIndex];
    if (isCorrect) {
        const el = document.getElementById('audio-seq-' + audioIndex);
        if (el) { el.style.background = '#43E97B'; el.style.color = 'white'; }
        gameScore++;
        document.getElementById('game-score').textContent = gameScore;
        audioIndex++;
        SoundEffects.playCorrect();
        if (audioIndex >= audioSequence.length) setTimeout(() => { if (gameLevel < 5) { gameLevel++; updateGameLevelBadge(); } startAudioPosition(); }, 1000);
    } else {
        SoundEffects.playWrong();
        const el = document.getElementById('audio-seq-' + audioIndex);
        if (el) el.style.background = '#FF6B6B';
        audioIndex = 0;
        setTimeout(() => {
            for (let i = 0; i < audioSequence.length; i++) {
                const seqEl = document.getElementById('audio-seq-' + i);
                if (seqEl) { seqEl.style.background = '#f0f0f0'; seqEl.style.color = '#333'; }
            }
        }, 500);
    }
}

function playAudioTone3(freq) {
    SoundEffects.init();
    const osc = SoundEffects.audioContext.createOscillator();
    const gain = SoundEffects.audioContext.createGain();
    osc.connect(gain);
    gain.connect(SoundEffects.audioContext.destination);
    osc.frequency.value = freq;
    osc.type = 'sine';
    gain.gain.setValueAtTime(0.3, SoundEffects.audioContext.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, SoundEffects.audioContext.currentTime + 0.4);
    osc.start();
    osc.stop(SoundEffects.audioContext.currentTime + 0.4);
}

function initAudioPlayer() {
    currentAudio = document.getElementById('hidden-audio');
    if (!currentAudio) return;
    currentAudio.addEventListener('timeupdate', updateAudioProgress);
    currentAudio.addEventListener('loadedmetadata', onAudioLoaded);
    currentAudio.addEventListener('ended', onAudioEnded);
    currentAudio.addEventListener('play', function() { audioCtx.isPlaying = true; updatePlayButtons(); });
    currentAudio.addEventListener('pause', function() { audioCtx.isPlaying = false; updatePlayButtons(); });
    try { var saved = localStorage.getItem('podcastPositions'); if (saved) savedPositions = JSON.parse(saved); } catch(e) {}
}

function initUnifiedPlayer() {
    var audioEl = document.getElementById('mp-audio-element');
    var videoEl = document.getElementById('mp-video-element');
    if (!audioEl || !videoEl) return;
    
    audioEl.addEventListener('timeupdate', updateMediaProgress);
    audioEl.addEventListener('loadedmetadata', onMediaLoaded);
    audioEl.addEventListener('ended', playNextMedia);
    audioEl.addEventListener('play', function() { mediaPlayer.isPlaying = true; updateMediaPlayButtons(); });
    audioEl.addEventListener('pause', function() { mediaPlayer.isPlaying = false; updateMediaPlayButtons(); });
    
    videoEl.addEventListener('timeupdate', updateMediaProgress);
    videoEl.addEventListener('loadedmetadata', onMediaLoaded);
    videoEl.addEventListener('ended', playNextMedia);
    videoEl.addEventListener('play', function() { mediaPlayer.isPlaying = true; updateMediaPlayButtons(); });
    videoEl.addEventListener('pause', function() { mediaPlayer.isPlaying = false; updateMediaPlayButtons(); });
    
    try { 
        var saved = localStorage.getItem('mediaPositions'); 
        if (saved) mediaPlayer.savedPositions = JSON.parse(saved); 
        else mediaPlayer.savedPositions = {};
    } catch(e) { mediaPlayer.savedPositions = {}; }
    
    initMediaCourses();
}

function initEnhancedVideoPlayer() {
    // 避免重复初始化
    if (videoCtx.isInitialized) return;
    
    evpVideo = document.getElementById('evp-video');
    if (!evpVideo) return;
    
    // 使用命名函数引用，便于后续移除
    const boundPlayHandler = function() { videoCtx.isPlaying = true; updateEnhancedPlayButtons(); };
    const boundPauseHandler = function() { videoCtx.isPlaying = false; updateEnhancedPlayButtons(); };
    
    evpVideo.addEventListener('timeupdate', updateEnhancedVideoProgress);
    evpVideo.addEventListener('loadedmetadata', onEnhancedVideoLoaded);
    evpVideo.addEventListener('ended', onEnhancedVideoEnded);
    evpVideo.addEventListener('play', boundPlayHandler);
    evpVideo.addEventListener('pause', boundPauseHandler);
    evpVideo.addEventListener('error', onEnhancedVideoError);
    evpVideo.addEventListener('waiting', onEnhancedVideoWaiting);
    evpVideo.addEventListener('canplay', onEnhancedVideoCanPlay);
    
    // 标记为已初始化
    videoCtx.isInitialized = true;
}

function closeAudioPlayer() { 
    // 停止音频和TTS
    if (currentAudio) { currentAudio.pause(); audioCtx.isPlaying = false; }
    stopPodcastTTS();
    // 隐藏全屏播放器
    var playerEl = document.getElementById('audio-player-fullscreen'); 
    var coverEl = document.getElementById('ap-cover'); 
    if (playerEl) playerEl.classList.remove('show'); 
    if (coverEl) coverEl.classList.remove('playing');
    // 显示迷你播放器
    if (audioCtx.currentTrack) {
        var miniEl = document.getElementById('mini-player');
        if (miniEl) miniEl.classList.add('show');
    }
    updatePlayButtons();
}

function closeMediaPlayer() {
    var playerEl = document.getElementById('media-player');
    var audioEl = document.getElementById('mp-audio-element');
    var videoEl = document.getElementById('mp-video-element');
    if (playerEl) playerEl.style.display = 'none';
    if (audioEl) { audioEl.pause(); audioEl.currentTime = 0; }
    if (videoEl) { videoEl.pause(); videoEl.currentTime = 0; }
    mediaPlayer.isPlaying = false;
    document.querySelectorAll('.media-item').forEach(function(item) { item.classList.remove('playing'); });
}

function closeMiniPlayer() { 
    // 完全停止音频和TTS
    if (currentAudio) { currentAudio.pause(); currentAudio.currentTime = 0; currentAudio.src = ''; } 
    stopPodcastTTS();
    audioCtx.isPlaying = false; 
    audioCtx.currentTrack = null;
    window._currentPodcastCaptions = null;
    window._currentAudioUri = null;
    // 隐藏迷你播放器和全屏播放器
    var miniEl = document.getElementById('mini-player'); 
    var playerEl = document.getElementById('audio-player-fullscreen'); 
    if (miniEl) miniEl.classList.remove('show'); 
    if (playerEl) playerEl.classList.remove('show');
    // 清除播放状态
    document.querySelectorAll('.podcast-item-enhanced').forEach(function(item) { item.classList.remove('playing'); });
    updatePlayButtons();
}

function closeEnhancedVideoPlayer() { 
    if (evpVideo) { evpVideo.pause(); evpVideo.src = ''; } 
    videoCtx.isPlaying = false; 
    videoCtx.currentVideo = null;
    var playerEl = document.getElementById('enhanced-video-player'); 
    if (playerEl) playerEl.style.display = 'none';
    // 退出全屏模式
    if (document.fullscreenElement) { document.exitFullscreen().catch(function() {}); }
}

function toggleAudioPlay() {
    // 如果正在TTS朗读，控制TTS
    if (window._currentPodcastCaptions && !currentAudio.src) {
window.closeEnhancedVideoPlayer = closeEnhancedVideoPlayer;
window.closeVideoPlayer = closeVideoPlayer;
window.seekEnhancedVideo = seekEnhancedVideo;
window.seekEnhancedVideoBackward = seekEnhancedVideoBackward;
window.seekEnhancedVideoForward = seekEnhancedVideoForward;
window.seekVideo = seekVideo;
window.toggleEnhancedFullscreen = toggleEnhancedFullscreen;
window.toggleEnhancedMute = toggleEnhancedMute;
window.toggleEnhancedSpeedDropdown = toggleEnhancedSpeedDropdown;
window.toggleEnhancedVideoPlay = toggleEnhancedVideoPlay;
window.togglePictureInPicture = togglePictureInPicture;
window.toggleVolume = toggleVolume;
window.toggleVpPlay = toggleVpPlay;
window.onEnhancedVideoError = onEnhancedVideoError;
window.onEnhancedVideoWaiting = onEnhancedVideoWaiting;
window.onEnhancedVideoCanPlay = onEnhancedVideoCanPlay;
window.initEnhancedVideoPlayer = initEnhancedVideoPlayer;
        if (audioCtx.isPlaying) { stopPodcastTTS(); }
        else { audioCtx.isPlaying = true; updatePlayButtons(); speakNextCaption(); }
        return;
    }
    if (!currentAudio) return;
    if (audioCtx.isPlaying) currentAudio.pause(); else currentAudio.play();
}

function toggleMediaPlay() {
    var mediaEl = getCurrentMediaElement();
    if (!mediaEl) return;
    if (mediaPlayer.isPlaying) mediaEl.pause();
    else mediaEl.play();
}

function toggleEnhancedVideoPlay() {
    if (!evpVideo) return;
    if (videoCtx.isPlaying) { evpVideo.pause(); var bigPlayEl = document.getElementById('evp-big-play'); if (bigPlayEl) bigPlayEl.style.display = 'flex'; }
    else { evpVideo.play(); var bigPlayEl = document.getElementById('evp-big-play'); if (bigPlayEl) bigPlayEl.style.display = 'none'; }
}

function togglePlayPause() {
    const audio = document.getElementById('hidden-audio');
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

function seekAudio(e) {
    if (!currentAudio) return;
    const bar = e.currentTarget;
    const rect = bar.getBoundingClientRect();
    const percent = (e.clientX - rect.left) / rect.width;
    currentAudio.currentTime = Math.floor(percent * currentAudio.duration);
    updateAudioProgress();
}

function seekVideo(e) { if (!vpVideo || !vpVideo.duration) return; const rect = e.target.getBoundingClientRect(); vpVideo.currentTime = ((e.clientX-rect.left)/rect.width)*vpVideo.duration; }

function seekMediaPlayer(e) {
    var mediaEl = getCurrentMediaElement();
    if (!mediaEl || !mediaEl.duration) return;
    var bar = document.getElementById('mp-progress-bar');
    if (!bar) return;
    var rect = bar.getBoundingClientRect();
    var percent = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
    mediaEl.currentTime = percent * mediaEl.duration;
}

function seekEnhancedVideo(e) { if (!evpVideo || !evpVideo.duration) return; var bar = document.getElementById('evp-progress'); if (!bar) return; var rect = bar.getBoundingClientRect(); var percent = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width)); evpVideo.currentTime = percent * evpVideo.duration; }

function seekEnhancedVideoBackward() { seekEnhancedVideoBy(-10); }

function seekEnhancedVideoForward() { seekEnhancedVideoBy(10); }

function seekEnhancedVideoBy(seconds) { if (!evpVideo) return; evpVideo.currentTime = Math.max(0, Math.min(evpVideo.duration, evpVideo.currentTime + seconds)); }

function seekAudioPlayer(e) {
    if (!currentAudio || !currentAudio.duration) return;
    var bar = document.getElementById('ap-progress-bar');
    if (!bar) return;
    var rect = bar.getBoundingClientRect();
    var percent = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
    currentAudio.currentTime = percent * currentAudio.duration;
}

function setVolume(value) { audioCtx.volume = value / 100; if (currentAudio) currentAudio.volume = audioCtx.volume; updateVolumeIcon(value); }

function toggleVolume() { if (!evpVideo) return; evpVideo.muted = !evpVideo.muted; var btn = document.getElementById('vp-volume-btn'); if (btn) btn.textContent = evpVideo.muted ? '🔇' : '🔊'; }

function setEnhancedVolume(value) { videoCtx.volume = value / 100; if (evpVideo) evpVideo.volume = videoCtx.volume; updateEnhancedVolumeIcon(value); }

function toggleMute() {
    if (audioCtx.volume > 0) { audioCtx.lastVolume = audioCtx.volume; setVolume(0); var sliderEl = document.getElementById('ap-volume-slider'); if (sliderEl) sliderEl.value = 0; }
    else { setVolume((audioCtx.lastVolume || 0.8) * 100); var sliderEl = document.getElementById('ap-volume-slider'); if (sliderEl) sliderEl.value = (audioCtx.lastVolume || 0.8) * 100; }
}

function toggleEnhancedMute() {
    if (videoCtx.volume > 0) { videoCtx.lastVolume = videoCtx.volume; setEnhancedVolume(0); var sliderEl = document.getElementById('evp-volume-slider'); if (sliderEl) sliderEl.value = 0; }
    else { setEnhancedVolume((videoCtx.lastVolume || 0.8) * 100); var sliderEl = document.getElementById('evp-volume-slider'); if (sliderEl) sliderEl.value = (videoCtx.lastVolume || 0.8) * 100; }
}

function toggleMediaMute() {
    var audioEl = document.getElementById('mp-audio-element');
    var videoEl = document.getElementById('mp-video-element');
    if (mediaPlayer.volume > 0) {
        mediaPlayer.lastVolume = mediaPlayer.volume;
        mediaPlayer.volume = 0;
    } else {
        mediaPlayer.volume = mediaPlayer.lastVolume || 0.8;
    }
    if (audioEl) audioEl.volume = mediaPlayer.volume;
    if (videoEl) videoEl.volume = mediaPlayer.volume;
    updateVolumeIcon();
}

function setPlaybackSpeed(speed) {
    audioCtx.playbackSpeed = speed;
    if (currentAudio) currentAudio.playbackRate = speed;
    var speedBtnEl = document.getElementById('ap-speed-btn');
    var dropdownEl = document.getElementById('ap-speed-dropdown');
    if (speedBtnEl) speedBtnEl.textContent = speed + 'x';
    if (dropdownEl) dropdownEl.classList.remove('show');
    document.querySelectorAll('.ap-speed-option').forEach(function(opt) { opt.classList.toggle('active', opt.textContent.trim() === speed + 'x'); });
}

function setEnhancedPlaybackSpeed(speed) { videoCtx.playbackSpeed = speed; if (evpVideo) evpVideo.playbackRate = speed; var speedBtnEl = document.getElementById('evp-speed-btn'); if (speedBtnEl) speedBtnEl.textContent = speed + 'x'; }

function cyclePlaybackSpeed() {
    var speeds = [0.5, 0.75, 1, 1.25, 1.5, 2];
    var currentIndex = speeds.indexOf(mediaPlayer.playbackSpeed);
    if (currentIndex < 0) currentIndex = 2;
    currentIndex = (currentIndex + 1) % speeds.length;
    mediaPlayer.playbackSpeed = speeds[currentIndex];
    
    var audioEl = document.getElementById('mp-audio-element');
    var videoEl = document.getElementById('mp-video-element');
    if (audioEl) audioEl.playbackRate = mediaPlayer.playbackSpeed;
    if (videoEl) videoEl.playbackRate = mediaPlayer.playbackSpeed;
    
    var speedBtnEl = document.getElementById('mp-speed-btn');
    if (speedBtnEl) speedBtnEl.textContent = mediaPlayer.playbackSpeed + 'x';
}

function toggleSpeedDropdown() { var dropdownEl = document.getElementById('ap-speed-dropdown'); if (dropdownEl) dropdownEl.classList.toggle('show'); }

function toggleEnhancedSpeedDropdown() { var speeds = [0.5, 1, 1.25, 1.5, 2]; var currentIndex = speeds.indexOf(videoCtx.playbackSpeed); var nextIndex = (currentIndex + 1) % speeds.length; setEnhancedPlaybackSpeed(speeds[nextIndex]); }

function showMiniPlayer(course) { var thumbEl = document.getElementById('mini-player-thumb'); var titleEl = document.getElementById('mini-player-title'); var teacherEl = document.getElementById('mini-player-teacher'); var playerEl = document.getElementById('mini-player'); if (thumbEl) { thumbEl.innerHTML = course.icon; thumbEl.style.background = course.gradient; } if (titleEl) titleEl.textContent = course.title; if (teacherEl) teacherEl.textContent = course.teacher; if (playerEl) playerEl.classList.add('show'); }

function showVideoPlayer(title, url, videoId) {
    openEnhancedVideoPlayer(title, url, videoId);
}

function openEnhancedVideoPlayer(title, url, videoId) {
    const playerEl = document.getElementById('enhanced-video-player');
    const videoEl = document.getElementById('evp-video');
    const titleEl = document.getElementById('evp-title');
    const bigPlayEl = document.getElementById('evp-big-play');
    const loadingEl = document.getElementById('evp-loading');
    
    if (playerEl && videoEl && titleEl) {
        titleEl.textContent = title;
        
        // 显示加载状态
        if (loadingEl) loadingEl.style.display = 'flex';
        if (bigPlayEl) bigPlayEl.style.display = 'none';
        
        // 记录视频ID
        if (videoId) {
            videoEl.dataset.videoId = videoId;
        }
        
        // 先移除旧的事件监听器（避免重复）
        const onVideoLoadedForResume = function() {
            // 恢复上次观看位置
            if (videoId) {
                const record = getVideoWatchRecord(videoId);
                if (record && record.progress < 90) {
                    const savedTime = (record.progress / 100) * videoEl.duration;
                    if (savedTime > 0 && !isNaN(savedTime)) {
                        videoEl.currentTime = savedTime;
                        showToast('已恢复到上次观看位置');
                    }
                }
            }
            // 移除这个一次性监听器
            videoEl.removeEventListener('loadedmetadata', onVideoLoadedForResume);
        };
        
        // 只在需要时添加一次性恢复监听器
        if (videoId) {
            videoEl.addEventListener('loadedmetadata', onVideoLoadedForResume);
        }
        
        // 检查URL是否有效
        if (!url || url === '' || url.indexOf('undefined') !== -1 || url.indexOf('null') !== -1) {
            showToast('视频地址无效');
            if (loadingEl) loadingEl.style.display = 'none';
            if (bigPlayEl) bigPlayEl.style.display = 'flex';
            return;
        }
        
        // 设置视频兼容性属性
        videoEl.preload = 'metadata';
        videoEl.setAttribute('playsinline', '');
        videoEl.setAttribute('webkit-playsinline', '');
        videoEl.setAttribute('x5-video-player-type', 'h5');
        videoEl.setAttribute('x5-video-player-fullscreen', 'true');
        
        // 使用source标签方式设置视频源，浏览器可以按顺序尝试
        // 先清除旧的source标签
        while (videoEl.firstChild) {
            videoEl.removeChild(videoEl.firstChild);
        }
        
        // 创建source元素
        var sourceEl = document.createElement('source');
        sourceEl.src = url;
        sourceEl.type = 'video/mp4';
        videoEl.appendChild(sourceEl);
        
        // 同时设置src属性作为后备
        videoEl.src = url;
        
        // 重置错误状态和重试计数
        videoEl.dataset.videoRetryCount = '0';
        
        videoEl.playbackRate = videoCtx.playbackSpeed;
        videoEl.volume = videoCtx.volume;
        
        playerEl.style.display = 'flex';
        
        // 确保视频元素引用是最新的
        evpVideo = videoEl;
        
        // 尝试播放，处理自动播放限制（移动端）
        const attemptPlay = function() {
            videoEl.play().then(function() {
                videoCtx.isPlaying = true;
                if (bigPlayEl) bigPlayEl.style.display = 'none';
                showToast('正在播放: ' + title);
            }).catch(function(e) {
                // 自动播放被阻止（常见于移动端），显示大播放按钮等待用户点击
                videoCtx.isPlaying = false;
                if (bigPlayEl) bigPlayEl.style.display = 'flex';
                console.log('自动播放被阻止，等待用户交互:', e.message);
            });
        };
        
        // 延迟执行播放尝试，确保 loadedmetadata 已触发
        setTimeout(attemptPlay, 100);
    }
}

function toggleMiniPlayer() { if (!currentAudio) return; if (audioCtx.isPlaying) currentAudio.pause(); else currentAudio.play(); }

function toggleEnhancedFullscreen() { var playerEl = document.getElementById('enhanced-video-player'); if (!playerEl) return; if (document.fullscreenElement) { document.exitFullscreen().catch(function(e) {}); } else { playerEl.requestFullscreen().catch(function(e) {}); } }

function togglePictureInPicture() { if (!evpVideo) return; if (document.pictureInPictureElement) { document.exitPictureInPicture().catch(function(e) {}); } else { evpVideo.requestPictureInPicture().catch(function(e) { showToast('画中画模式不支持'); }); } }

function updateMediaProgress() {
    var mediaEl = getCurrentMediaElement();
    if (!mediaEl || !mediaEl.duration) return;
    
    var progress = (mediaEl.currentTime / mediaEl.duration) * 100;
    var fillEl = document.getElementById('mp-progress-fill');
    var currentTimeEl = document.getElementById('mp-current-time');
    
    if (fillEl) fillEl.style.width = progress + '%';
    if (currentTimeEl) currentTimeEl.textContent = formatMediaTime(mediaEl.currentTime);
    
    // 保存进度
    if (mediaPlayer.currentMedia) {
        mediaPlayer.savedPositions[mediaPlayer.currentMedia.id] = mediaEl.currentTime;
        try { localStorage.setItem('mediaPositions', JSON.stringify(mediaPlayer.savedPositions)); } catch(e) {}
    }
}

function updateAudioProgress() {
    if (!currentAudio) return;
    const progress = (currentAudio.currentTime / currentAudio.duration) * 100;
    document.getElementById('audio-progress-bar').style.width = progress + '%';
    document.getElementById('audio-current-time').textContent = formatTime(currentAudio.currentTime);
    document.getElementById('audio-duration').textContent = formatTime(currentAudio.duration);
}

function updateEnhancedVideoProgress() { if (!evpVideo || !evpVideo.duration) return; var progress = (evpVideo.currentTime / evpVideo.duration) * 100; var barEl = document.getElementById('evp-progress-bar'); var timeEl = document.getElementById('evp-time'); if (barEl) barEl.style.width = progress + '%'; if (timeEl) timeEl.textContent = formatTimeFull(evpVideo.currentTime) + ' / ' + formatTimeFull(evpVideo.duration); }

function onAudioEnded() { playNextTrack(); }

function onAudioLoaded() { var totalEl = document.getElementById('ap-total-time'); if (totalEl) totalEl.textContent = formatTimeFull(currentAudio.duration); }

function onEnhancedVideoEnded() { videoCtx.isPlaying = false; var bigPlayEl = document.getElementById('evp-big-play'); if (bigPlayEl) bigPlayEl.style.display = 'flex'; updateEnhancedPlayButtons(); }

function onEnhancedVideoLoaded() { 
    var timeEl = document.getElementById('evp-time'); 
    var loadingEl = document.getElementById('evp-loading');
    if (timeEl) timeEl.textContent = '0:00 / ' + formatTimeFull(evpVideo.duration); 
    if (loadingEl) loadingEl.style.display = 'none';
}

// 视频错误处理
function onEnhancedVideoError(e) {
    videoCtx.isPlaying = false;
    var loadingEl = document.getElementById('evp-loading');
    var bigPlayEl = document.getElementById('evp-big-play');
    var playerEl = document.getElementById('enhanced-video-player');
    
    if (loadingEl) loadingEl.style.display = 'none';
    if (bigPlayEl) bigPlayEl.style.display = 'flex';
    
    // 获取视频元素
    var videoEl = document.getElementById('evp-video');
    
    // 检查播放器是否可见，如果不可见说明是自动加载失败，不显示toast
    var isPlayerVisible = false;
    if (playerEl && playerEl.style.display !== 'none') {
        isPlayerVisible = true;
    }
    
    // 如果播放器不可见，不显示任何错误提示（避免首页自动加载失败弹窗）
    if (!isPlayerVisible) {
        console.warn('视频加载失败但播放器不可见，已忽略');
        return;
    }
    
    // 获取重试次数
    var retryCount = 0;
    if (videoEl && videoEl.dataset) {
        retryCount = parseInt(videoEl.dataset.videoRetryCount) || 0;
    }
    
    // 检查是否是src为空的情况
    var isEmptySrc = false;
    if (videoEl && (!videoEl.src || videoEl.src === '' || videoEl.src.indexOf('undefined') !== -1 || videoEl.src.indexOf('null') !== -1)) {
        isEmptySrc = true;
    }
    
    // 判断是否是本地视频（blob URL）还是网络视频
    var isLocalVideo = false;
    if (videoEl && videoEl.src && videoEl.src.indexOf('blob:') === 0) {
        isLocalVideo = true;
    }
    
    var errorMsg = '视频加载失败';
    var errorCode = 0;
    if (videoEl && videoEl.error) {
        errorCode = videoEl.error.code;
    }
    
    // 判断是否应该重试（网络视频可以重试，blob本地视频不需要）
    if (retryCount === 0 && !isEmptySrc && errorCode === 4 && !isLocalVideo) {
        // error code 4 在移动端经常是网络/自动播放问题，不一定是格式不支持
        // 第一次失败时自动重试一次（仅针对网络视频）
        if (videoEl && videoEl.src && videoEl.src.indexOf('blob:') !== 0) {
            videoEl.dataset.videoRetryCount = '1';
            // 减少重试提示频率，只在重试时提示一次
            setTimeout(function() {
                var currentSrc = videoEl.src;
                videoEl.load(); // 重置错误状态
                // 重新设置src触发加载
                var tempSrc = currentSrc;
                videoEl.src = '';
                setTimeout(function() {
                    videoEl.src = tempSrc;
                    videoEl.load();
                }, 50);
            }, 1000);
            return; // 不显示错误提示，等待重试
        }
    }
    
    // 重试后仍然失败，显示更友好的错误提示
    if (isEmptySrc || (videoEl && (!videoEl.src || videoEl.src === ''))) {
        errorMsg = isLocalVideo ? '视频文件已丢失，请重新上传' : '视频加载失败，请检查网络';
    } else if (isLocalVideo) {
        // 本地视频的错误提示
        switch(errorCode) {
            case 1: errorMsg = '视频读取被中断'; break;
            case 2: errorMsg = '视频文件损坏，请重新上传'; break;
            case 3: errorMsg = '视频格式不支持'; break;
            case 4: errorMsg = '视频加载失败，请重新上传'; break;
            default: errorMsg = '视频加载失败，请重新上传'; break;
        }
    } else {
        // 网络视频的错误提示
        switch(errorCode) {
            case 1: errorMsg = '视频加载被中断'; break;
            case 2: errorMsg = '网络错误，请检查网络连接'; break;
            case 3: errorMsg = '视频解码失败，请稍后重试'; break;
            case 4: errorMsg = '视频加载失败，请检查网络或稍后重试'; break;
            default: errorMsg = '网络视频加载失败，请检查网络连接'; break;
        }
    }
    
    // 重置重试计数
    if (videoEl && videoEl.dataset) {
        videoEl.dataset.videoRetryCount = '0';
    }
    
    showToast(errorMsg);
    if (videoEl && videoEl.error) {
        console.error('视频加载错误:', videoEl.error);
    }
}

// 视频缓冲等待状态
function onEnhancedVideoWaiting() {
    var loadingEl = document.getElementById('evp-loading');
    if (loadingEl) loadingEl.style.display = 'flex';
}

// 视频可以播放状态
function onEnhancedVideoCanPlay() {
    var loadingEl = document.getElementById('evp-loading');
    if (loadingEl) loadingEl.style.display = 'none';
}

function onMediaLoaded() {
    var mediaEl = getCurrentMediaElement();
    var totalEl = document.getElementById('mp-total-time');
    if (totalEl && mediaEl) totalEl.textContent = formatMediaTime(mediaEl.duration);
}

function playNextMedia() {
    if (allMediaCourses.length === 0) return;
    mediaPlayer.currentIndex = (mediaPlayer.currentIndex + 1) % allMediaCourses.length;
    var course = allMediaCourses[mediaPlayer.currentIndex];
    if (course) playMediaCourse(course.id);
}

function playPrevMedia() {
    if (allMediaCourses.length === 0) return;
    mediaPlayer.currentIndex = (mediaPlayer.currentIndex - 1 + allMediaCourses.length) % allMediaCourses.length;
    var course = allMediaCourses[mediaPlayer.currentIndex];
    if (course) playMediaCourse(course.id);
}

function playNextTrack() { if (podcastCourses.length === 0) return; audioCtx.currentIndex = (audioCtx.currentIndex + 1) % podcastCourses.length; var course = podcastCourses[audioCtx.currentIndex]; if (course) playPodcastCourse(course.id); }

function playPrevTrack() { if (podcastCourses.length === 0) return; audioCtx.currentIndex = (audioCtx.currentIndex - 1 + podcastCourses.length) % podcastCourses.length; var course = podcastCourses[audioCtx.currentIndex]; if (course) playPodcastCourse(course.id); }

function playVideoFromList(id) {
    var course = videoCourses.find(function(v) { return v.id === id; });
    if (course) {
        // 使用增强版视频播放器，传入videoId用于记录观看进度
        openEnhancedVideoPlayer(course.title, course.url, course.id);
    }
}

function handleAudioUpload(input) {
    const file = input.files[0];
    if (!file) return;

    // 检查文件类型
    if (!file.type.startsWith('audio/')) {
        showToast('请上传音频文件');
        return;
    }

    // 检查文件大小（限制50MB）
    if (file.size > 50 * 1024 * 1024) {
        showToast('音频文件不能超过50MB');
        return;
    }

    const user = getCurrentUserData();
    if (!user.localAudios) user.localAudios = [];

    // 创建音频URL
    const audioUrl = URL.createObjectURL(file);

    // 添加到用户数据
    const audioData = {
        id: 'local-audio-' + Date.now(),
        title: file.name.replace(/\.[^/.]+$/, ''),
        url: audioUrl,
        size: file.size,
        type: file.type,
        uploadTime: new Date().toLocaleString(),
        duration: '未知'
    };

    user.localAudios.push(audioData);
    syncUserData(user);

    // 获取音频时长
    const tempAudio = new Audio();
    tempAudio.src = audioUrl;
    tempAudio.onloadedmetadata = function() {
        const mins = Math.floor(tempAudio.duration / 60);
        const secs = Math.floor(tempAudio.duration % 60);
        audioData.duration = mins + ':' + (secs < 10 ? '0' : '') + secs;
        syncUserData(user);
        renderLocalAudioList();
    };

    showToast('音频上传成功！');
    renderLocalAudioList();
}

// V152: 处理视频上传（集成压缩功能）
function handleVideoUpload(input) {
    var file = input.files[0];
    if (!file) return;
    
    // 检查文件类型
    if (!file.type.startsWith('video/')) {
        showToast('请上传视频文件');
        return;
    }
    
    // 检查文件大小（限制100MB原始文件）
    if (file.size > 100 * 1024 * 1024) {
        showToast('视频文件不能超过100MB');
        return;
    }
    
    var user = getCurrentUserData();
    if (!user.localVideos) user.localVideos = [];
    
    // 生成视频ID
    var videoId = 'local-video-' + Date.now();
    
    // 添加到用户数据（只存元信息，不存url）
    var videoData = {
        id: videoId,
        title: file.name.replace(/\.[^/.]+$/, ''),
        size: file.size,
        type: file.type,
        uploadTime: new Date().toLocaleString(),
        duration: '未知',
        originalSize: file.size
    };
    
    user.localVideos.push(videoData);
    syncUserData(user);
    
    // 显示上传提示
    showToast('正在处理视频...');
    
    // 初始化内存缓存（用于备用播放）
    if (!window._uploadedVideos) {
        window._uploadedVideos = {};
    }
    
    // 获取视频时长（使用临时URL）
    var tempVideo = document.createElement('video');
    var tempUrl = URL.createObjectURL(file);
    tempVideo.src = tempUrl;
    
    tempVideo.onloadedmetadata = function() {
        var mins = Math.floor(tempVideo.duration / 60);
        var secs = Math.floor(tempVideo.duration % 60);
        videoData.duration = mins + ':' + (secs < 10 ? '0' : '') + secs;
        syncUserData(user);
        renderLocalVideoList();
        // 释放临时URL
        URL.revokeObjectURL(tempUrl);
    };
    
    tempVideo.onerror = function() {
        URL.revokeObjectURL(tempUrl);
    };
    
    // V152: 视频压缩处理
    compressVideo(file, function(progress) {
        // 进度回调 - 更新UI
        var progressText = document.getElementById('video-compress-progress-text');
        if (progressText) {
            progressText.textContent = '视频压缩中 ' + progress + '%';
        }
    }, function(compressedBlob) {
        // 完成回调
        var fileToSave = compressedBlob || file;
        var finalSize = fileToSave.size;
        
        // 更新元数据
        if (compressedBlob) {
            videoData.size = finalSize;
            videoData.compressed = true;
            videoData.originalSize = file.size;
            var savedSize = ((file.size - finalSize) / file.size * 100).toFixed(1);
            showToast('视频压缩完成！节省 ' + savedSize + '% 存储空间');
        } else {
            showToast('视频上传成功！');
        }
        
        syncUserData(user);
        
        // 保存到内存缓存（用于备用播放方案）
        window._uploadedVideos[videoId] = fileToSave;
        
        // 将视频文件存入 IndexedDB
        saveVideoFile(videoId, fileToSave).then(function() {
            console.log('[VideoUpload] 视频文件已持久化存储:', videoId, 
                        '大小:', (finalSize / 1024 / 1024).toFixed(2), 'MB');
            
            // 存储后清理内存缓存以释放内存
            if (window._uploadedVideos && window._uploadedVideos[videoId]) {
                // 保留一段时间后再清理
                setTimeout(function() {
                    if (window._uploadedVideos && window._uploadedVideos[videoId]) {
                        delete window._uploadedVideos[videoId];
                        console.log('[VideoUpload] 已清理内存缓存:', videoId);
                    }
                }, 60000); // 1分钟后清理
            }
        }).catch(function(e) {
            console.error('[VideoUpload] 视频持久化存储失败:', e);
            showToast('视频存储可能不稳定，请刷新重试');
        });
        
        renderLocalVideoList();
    }, function(error) {
        // 错误回调 - 保留原视频
        console.error('[VideoUpload] 压缩失败，使用原视频:', error);
        showToast('视频上传成功！');
        
        // 保存原文件
        window._uploadedVideos[videoId] = file;
        
        saveVideoFile(videoId, file).then(function() {
            console.log('[VideoUpload] 原视频已存储:', videoId);
        }).catch(function(e) {
            console.error('[VideoUpload] 存储失败:', e);
        });
        
        renderLocalVideoList();
    });
}

function deleteLocalAudio(audioId) {
    if (!confirm('确定要删除这个音频吗？')) return;

    const user = getCurrentUserData();
    if (!user.localAudios) return;

    user.localAudios = user.localAudios.filter(a => a.id !== audioId);
    syncUserData(user);
    renderLocalAudioList();
    showToast('音频已删除');
}

function deleteLocalVideo(videoId) {
    if (!confirm('确定删除这个视频吗？')) return;
    
    const user = getCurrentUserData();
    user.localVideos = user.localVideos.filter(v => v.id !== videoId);
    syncUserData(user);
    
    // 同时从 IndexedDB 删除视频文件
    deleteVideoFile(videoId).then(function() {
        console.log('视频已从存储中删除:', videoId);
    }).catch(function(e) {
        console.error('删除视频文件失败:', e);
    });
    
    renderLocalVideoList();
    showToast('视频已删除');
}

function initMediaCourses() {
    allMediaCourses = [];
    podcastCourses.forEach(function(course) {
        allMediaCourses.push({
            id: course.id,
            title: course.title,
            teacher: course.teacher,
            duration: course.duration,
            category: course.category,
            gradient: course.gradient,
            icon: course.icon,
            url: course.url,
            type: 'audio'
        });
    });
    videoCourses.forEach(function(course) {
        allMediaCourses.push({
            id: course.id,
            title: course.title,
            teacher: course.teacher,
            duration: course.duration,
            category: course.category,
            gradient: course.gradient,
            icon: course.icon,
            url: course.url,
            type: 'video'
        });
    });
}

function filterVideoCourse(category, btn) {
    document.querySelectorAll('.subject-tab-btn').forEach(function(b) { b.classList.remove('active'); });
    btn.classList.add('active');
    
    var videos = videoCourses.filter(function(v) { return category === 'all' || v.category === category; });
    var videoHtml = videos.map(function(v) {
        return '<div class="video-item" onclick="playVideoFromList(\'' + v.id + '\')">' +
               '<div class="video-thumb"><span class="play-icon">▶</span></div>' +
               '<div class="video-info"><div class="video-title">' + v.title + '</div>' +
               '<div class="video-meta">' + v.teacher + ' · ' + v.duration + '</div>' +
               '<div class="media-views">👁 ' + (v.views ? (v.views/1000).toFixed(1) + '万' : '0') + '</div></div></div>';
    }).join('');
    
    document.getElementById('video-list').innerHTML = videoHtml;
}

function updateMediaListState(courseId) {
    document.querySelectorAll('.media-item').forEach(function(item) {
        var id = item.getAttribute('data-id');
        if (id === courseId) {
            item.classList.add('playing');
            var indicator = item.querySelector('.media-playing-indicator');
            if (indicator) indicator.style.display = 'flex';
        } else {
            item.classList.remove('playing');
            var indicator = item.querySelector('.media-playing-indicator');
            if (indicator) indicator.style.display = 'none';
        }
    });
}

function updateVideoListState(courseId) { document.querySelectorAll('.video-item-enhanced').forEach(function(item) { var id = item.getAttribute('data-id'); item.classList.toggle('playing', id === courseId); }); }

function updatePodcastListState(courseId) { document.querySelectorAll('.podcast-item-enhanced').forEach(function(item) { var id = item.getAttribute('data-id'); if (id === courseId) { item.classList.add('playing'); var indicator = item.querySelector('.podcast-playing-indicator'); if (indicator) indicator.style.display = 'flex'; } else { item.classList.remove('playing'); var indicator = item.querySelector('.podcast-playing-indicator'); if (indicator) indicator.style.display = 'none'; } }); }

function updatePlayButtons() { var icon = audioCtx.isPlaying ? '⏸' : '▶'; var apPlayBtn = document.getElementById('ap-play-btn'); var miniBtn = document.getElementById('mini-player-btn'); if (apPlayBtn) apPlayBtn.innerHTML = icon; if (miniBtn) miniBtn.innerHTML = icon; }

function updateEnhancedPlayButtons() { var icon = videoCtx.isPlaying ? '⏸' : '▶'; var playBtnEl = document.getElementById('evp-play-btn'); var bigPlayEl = document.getElementById('evp-big-play'); if (playBtnEl) playBtnEl.innerHTML = icon; if (bigPlayEl) bigPlayEl.innerHTML = icon; }

function getCurrentMediaElement() {
    if (mediaPlayer.isAudio) return document.getElementById('mp-audio-element');
    return document.getElementById('mp-video-element');
}

function formatMediaTime(seconds) {
    if (isNaN(seconds) || seconds < 0) return '0:00';
    var mins = Math.floor(seconds / 60);
    var secs = Math.floor(seconds % 60);
    return mins + ':' + (secs < 10 ? '0' : '') + secs;
}

function startAudioPosition() {
    document.getElementById('game-title').textContent = '🎧 听音辨位';
    const board = document.getElementById('game-board');
    board.style.display = 'block';
    board.style.textAlign = 'center';
    const lengths = [3, 4, 5, 6, 7];
    const seqLength = lengths[Math.min(gameLevel - 1, 4)];
    audioSequence = [];
    for (let i = 0; i < seqLength; i++) audioSequence.push(Math.floor(Math.random() * 3));
    audioIndex = 0;
    board.innerHTML = '<div style="background:white;border-radius:16px;padding:24px;max-width:320px;"><div style="font-size:14px;color:#666;margin-bottom:16px;">仔细听，按顺序点击播放顺序：</div><div id="audio-sequence-display" style="display:flex;gap:8px;justify-content:center;margin-bottom:20px;">' + audioSequence.map((_, i) => '<div id="audio-seq-' + i + '" style="width:36px;height:36px;background:#f0f0f0;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:18px;">' + (i + 1) + '</div>').join('') + '</div><div style="display:flex;gap:12px;justify-content:center;margin-bottom:20px;"><button onclick="playAudioPos(0)" style="width:80px;height:80px;background:linear-gradient(135deg,#667eea,#764ba2);border:none;border-radius:16px;color:white;font-size:14px;cursor:pointer;">👈 左</button><button onclick="playAudioPos(1)" style="width:80px;height:80px;background:linear-gradient(135deg,#4ECDC4,#38F9D7);border:none;border-radius:16px;color:white;font-size:14px;cursor:pointer;">👆 中</button><button onclick="playAudioPos(2)" style="width:80px;height:80px;background:linear-gradient(135deg,#FF6B6B,#FF4757);border:none;border-radius:16px;color:white;font-size:14px;cursor:pointer;">👉 右</button></div><button onclick="startAudioSeq()" style="margin-top:16px;padding:12px 24px;background:#43E97B;color:white;border:none;border-radius:10px;font-size:14px;cursor:pointer;">开始播放序列</button></div>';
    gameScore = 0;
    document.getElementById('game-score').textContent = '0';
}

function toggleVpPlay() { if (!vpVideo) return; vpPlaying ? vpVideo.pause() : vpVideo.play(); }

function updateEnhancedVolumeIcon(value) { var icon = value == 0 ? '🔇' : (value < 50 ? '🔉' : '🔊'); var btnEl = document.getElementById('evp-volume-btn'); if (btnEl) btnEl.innerHTML = icon; }

function updateVolumeIcon() {
    var icon = mediaPlayer.volume == 0 ? '🔇' : (mediaPlayer.volume < 50 ? '🔉' : '🔊');
    var btnEl = document.getElementById('mp-volume-btn');
    if (btnEl) btnEl.innerHTML = icon;
}

function closeVideoPlayer() { if (vpVideo) { vpVideo.pause(); vpVideo.src = ''; } document.getElementById('video-player-modal').classList.remove('show'); }

function updateMediaPlayButtons() {
    var icon = mediaPlayer.isPlaying ? '⏸' : '▶';
    var apPlayBtn = document.getElementById('mp-play-btn');
    if (apPlayBtn) apPlayBtn.innerHTML = icon;
}


// ============================================================
// Games - 游戏模块
// ============================================================
window.playAudioPos = playAudioPos;
window.startAudioSeq = startAudioSeq;
// ========== 视频观看记录功能 ==========
function getVideoWatchRecord(videoId) {
    try {
        const user = getCurrentUserData();
        if (!user || !user.videoWatchRecords) return null;
        return user.videoWatchRecords[videoId] || null;
    } catch (e) {
        return null;
    }
}

function saveVideoWatchRecord(videoId, progress, duration) {
    try {
        const user = getCurrentUserData();
        if (!user) return;
        if (!user.videoWatchRecords) user.videoWatchRecords = {};
        user.videoWatchRecords[videoId] = {
            progress: Math.min(progress, 100),
            duration: duration,
            timestamp: Date.now()
        };
        saveCurrentUserData(user);
    } catch (e) {}
}

function updateVideoProgress() {
    try {
        const videoEl = document.getElementById('evp-video');
        if (!videoEl || !videoEl.dataset.videoId) return;
        const videoId = videoEl.dataset.videoId;
        const progress = videoEl.duration > 0 ? (videoEl.currentTime / videoEl.duration) * 100 : 0;
        saveVideoWatchRecord(videoId, progress, videoEl.duration);
    } catch (e) {}
}

// ========== 本地视频相关函数导出 ==========
window.playLocalVideo = playLocalVideo;
window.handleVideoUpload = handleVideoUpload;
window.deleteLocalVideo = deleteLocalVideo;
window.compressVideo = compressVideo;
window.tryPlayFromMemoryFallback = tryPlayFromMemoryFallback;
window.markVideoForReupload = markVideoForReupload;
window._uploadedVideos = window._uploadedVideos || {};
