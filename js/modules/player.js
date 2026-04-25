// 播放器模块

function playBilibiliVideo(bvid, title) {
    window.open('https://www.bilibili.com/video/' + bvid, '_blank');
}

function closeVideoPlayer() {
    const modal = document.getElementById('video-player-modal');
    const container = document.getElementById('video-container');
    if (container) {
        container.innerHTML = '<video id="main-video-player" controls style="width:100%;height:100%;"></video>';
    }
    modal.classList.remove('show');
}

function handlePodcastUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    const url = URL.createObjectURL(file);
    const title = file.name.replace(/\.[^/.]+$/, "");
    
    const data = loadData();
    const user = data.users.find(u => u.id === data.currentUser);
    if (user) {
        user.myPodcasts = user.myPodcasts || [];
        user.myPodcasts.push({ id: Date.now(), title, url, date: Date.now() });
        saveData(data);
        renderMyPodcasts();
    }
}

function renderMyPodcasts() {
    const data = loadData();
    const user = data.users.find(u => u.id === data.currentUser);
    const container = document.getElementById('my-podcast-list');
    if (!container) return;
    
    if (!user || !user.myPodcasts || !user.myPodcasts.length) {
        container.innerHTML = '<div style="text-align:center;padding:20px;color:#999;">点击右上角上传</div>';
        return;
    }
    
    let html = '';
    user.myPodcasts.forEach((p, i) => {
        html += '<div style="padding:12px;background:#f5f5f5;border-radius:12px;margin:8px 0;cursor:pointer;" onclick="playMyPodcast(' + i + ')">';
        html += '<div style="font-weight:600;">' + p.title + '</div></div>';
    });
    container.innerHTML = html;
}
