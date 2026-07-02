const { chromium } = require('playwright');

(async () => {
    console.log("Launching Chromium...");
    const browser = await chromium.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const context = await browser.newContext({
        userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        locale: 'zh-CN'
    });

    const page = await context.newPage();

    const url = process.argv[2] || 'https://gtnh.huijiwiki.com/wiki/%E9%A6%96%E9%A1%B5';
    console.log(`Navigating to: ${url}`);
    await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });

    // Extra wait for Cloudflare challenge
    await page.waitForTimeout(3000);

    const title = await page.title();
    console.log(`\n=== PAGE TITLE: ${title} ===\n`);

    // Get main content
    const content = await page.evaluate(() => {
        const el = document.querySelector('.mw-parser-output') ||
                   document.querySelector('#mw-content-text') ||
                   document.querySelector('main') ||
                   document.body;
        return el ? el.innerText : 'No content found';
    });

    console.log(content.substring(0, 8000));
    console.log('\n=== END ===');

    await browser.close();
})().catch(e => {
    console.error('Error:', e.message);
    process.exit(1);
});
