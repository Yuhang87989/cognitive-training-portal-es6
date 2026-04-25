// 应用入口 - 初始化所有模块

console.log('认知训练门户启动');

// 初始化播客列表
function initPodcast() {
    const list = podcastData[currentPodcastCategory];
    const container = document.getElementById('podcast-list');
    if (!container || !list) return;
    
    let html = '';
    list.forEach((p, i) => {
        html += '<div class="topic-item" onclick="playPodcast(' + i + ')">';
        html += '<span>' + p.icon + '</span>';
        html += '<div>' + p.title + '</div></div>';
    });
    container.innerHTML = html;
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        initPodcast();
        renderTopics();
    }, 200);
});
