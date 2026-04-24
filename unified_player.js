// ====== 统一媒体播放器核心代码 ======
var mediaPlayer = {
    isPlaying: false,
    currentMedia: null,
    currentIndex: -1,
    playbackSpeed: 1,
    volume: 0.8,
    lastVolume: 0.8,
    isAudio: true // true=音频模式, false=视频模式
};

// 合并音频和视频课程数据
var allMediaCourses = [];

// 初始化媒体课程列表
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

// 初始化统一播放器
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

// 播放媒体课程
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

// 格式化时间
function formatMediaTime(seconds) {
    if (isNaN(seconds) || seconds < 0) return '0:00';
    var mins = Math.floor(seconds / 60);
    var secs = Math.floor(seconds % 60);
    return mins + ':' + (secs < 10 ? '0' : '') + secs;
}

function onMediaLoaded() {
    var mediaEl = getCurrentMediaElement();
    var totalEl = document.getElementById('mp-total-time');
    if (totalEl && mediaEl) totalEl.textContent = formatMediaTime(mediaEl.duration);
}

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

function getCurrentMediaElement() {
    if (mediaPlayer.isAudio) return document.getElementById('mp-audio-element');
    return document.getElementById('mp-video-element');
}

function toggleMediaPlay() {
    var mediaEl = getCurrentMediaElement();
    if (!mediaEl) return;
    if (mediaPlayer.isPlaying) mediaEl.pause();
    else mediaEl.play();
}

function seekMediaPlayer(e) {
    var mediaEl = getCurrentMediaElement();
    if (!mediaEl || !mediaEl.duration) return;
    var bar = document.getElementById('mp-progress-bar');
    if (!bar) return;
    var rect = bar.getBoundingClientRect();
    var percent = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
    mediaEl.currentTime = percent * mediaEl.duration;
}

function playPrevMedia() {
    if (allMediaCourses.length === 0) return;
    mediaPlayer.currentIndex = (mediaPlayer.currentIndex - 1 + allMediaCourses.length) % allMediaCourses.length;
    var course = allMediaCourses[mediaPlayer.currentIndex];
    if (course) playMediaCourse(course.id);
}

function playNextMedia() {
    if (allMediaCourses.length === 0) return;
    mediaPlayer.currentIndex = (mediaPlayer.currentIndex + 1) % allMediaCourses.length;
    var course = allMediaCourses[mediaPlayer.currentIndex];
    if (course) playMediaCourse(course.id);
}

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

function updateVolumeIcon() {
    var icon = mediaPlayer.volume == 0 ? '🔇' : (mediaPlayer.volume < 50 ? '🔉' : '🔊');
    var btnEl = document.getElementById('mp-volume-btn');
    if (btnEl) btnEl.innerHTML = icon;
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

function updateMediaPlayButtons() {
    var icon = mediaPlayer.isPlaying ? '⏸' : '▶';
    var apPlayBtn = document.getElementById('mp-play-btn');
    if (apPlayBtn) apPlayBtn.innerHTML = icon;
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
