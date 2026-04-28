const puppeteer = require('puppeteer');
(async () => {
    const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox','--disable-setuid-sandbox'] });
    const page = await browser.newPage();
    await page.setCacheEnabled(false);
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    await page.goto('https://yuhang87989.github.io/cognitive-training-portal/?_t=' + Date.now(), { waitUntil: 'domcontentloaded', timeout: 60000 });
    for (let i = 0; i < 30; i++) {
        await new Promise(r => setTimeout(r, 2000));
        if (await page.evaluate(() => typeof openFullscreenPage === 'function')) break;
    }
    await new Promise(r => setTimeout(r, 3000));
    
    // 12模块测试
    const modules = ['practice','map','plan','topics','method','thinking','podcast','video','games','deepseek','wrongbook','pomodoro'];
    let pass = 0;
    for (const mod of modules) {
        const r = await page.evaluate((m) => {
            try { openFullscreenPage(m); const c = document.getElementById('fullscreen-content'); return c && c.innerHTML.trim().length > 50; }
            catch(e) { return { err: e.message }; }
        }, mod);
        const ok = typeof r === 'object' && r.err ? false : r;
        if (ok) pass++;
        console.log((ok?'✅':'❌') + ' ' + mod + (typeof r === 'object' && r.err ? ' '+r.err : ''));
    }
    console.log(pass + '/12');
    
    // DeepSeek测试
    await page.evaluate(() => openFullscreenPage('deepseek'));
    const dsCheck = await page.evaluate(() => ({
        input: !!document.getElementById('deepseek-input'),
        send: typeof sendToDeepSeek === 'function',
        voice: typeof toggleDeepSeekVoice === 'function',
        image: typeof handleDeepSeekImage === 'function'
    }));
    console.log('DeepSeek:', JSON.stringify(dsCheck));
    
    // 游戏退出测试
    await page.evaluate(() => openFullscreenPage('games'));
    await page.evaluate(() => { const cards = document.querySelectorAll('[onclick*="startGame"]'); if(cards[0]) cards[0].click(); });
    await new Promise(r => setTimeout(r, 1000));
    const gameTest = await page.evaluate(() => {
        const gfc = document.getElementById('game-fullscreen-container');
        return { containerVisible: gfc ? getComputedStyle(gfc).display !== 'none' : false };
    });
    console.log('游戏:', JSON.stringify(gameTest));
    // 测试退出
    await page.evaluate(() => { if(typeof exitGame === 'function') exitGame(); });
    await new Promise(r => setTimeout(r, 500));
    const afterExit = await page.evaluate(() => {
        const gfc = document.getElementById('game-fullscreen-container');
        return { gameContainerHidden: gfc ? getComputedStyle(gfc).display === 'none' : true, fullscreenVisible: !!document.getElementById('fullscreen-container').classList.contains('active') };
    });
    console.log('退出后:', JSON.stringify(afterExit));
    
    // 学霸方法题库测试
    await page.evaluate(() => openFullscreenPage('method'));
    const methodTest = await page.evaluate(() => ({
        hasQuestions: typeof methodTrainingQuestions !== 'undefined',
        hasDetails: typeof methodDetails !== 'undefined',
        quizBtn: typeof startMethodQuiz === 'function'
    }));
    console.log('学霸方法:', JSON.stringify(methodTest));
    
    const uniqueErrors = [...new Set(errors)];
    if (uniqueErrors.length) console.log('\nJS错误(' + uniqueErrors.length + '):', uniqueErrors.slice(0,5).join(' | '));
    else console.log('\n无JS错误 ✅');
    await browser.close();
})();
