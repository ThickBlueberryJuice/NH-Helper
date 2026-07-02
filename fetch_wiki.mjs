import { chromium } from "playwright-extra";
import StealthPlugin from "puppeteer-extra-plugin-stealth";

chromium.use(StealthPlugin());

(async () => {
    console.log("Launching stealth browser...");
    const browser = await chromium.launch({
        headless: true,
        args: ["--no-sandbox", "--disable-setuid-sandbox"]
    });

    const context = await browser.newContext({
        locale: "zh-CN",
        viewport: { width: 1920, height: 1080 }
    });

    const page = await context.newPage();
    const url = process.argv[2] || "https://gtnh.huijiwiki.com/wiki/%E9%A6%96%E9%A1%B5";
    console.log(`Navigating to: ${url}`);
    
    try {
        await page.goto(url, { waitUntil: "domcontentloaded", timeout: 30000 });
        console.log("Waiting 15s for Cloudflare...");
        await page.waitForTimeout(15000);
        
        const title = await page.title();
        console.log(`\n=== PAGE TITLE: ${title} ===\n`);

        const content = await page.evaluate(() => {
            const el = document.querySelector(".mw-parser-output") ||
                       document.querySelector("#mw-content-text") ||
                       document.querySelector("main") ||
                       document.body;
            return el ? el.innerText : "No content found";
        });

        console.log(content.substring(0, 8000));
    } catch (e) {
        console.log("Error during navigation:", e.message);
        try {
            const title = await page.title();
            console.log(`Current page title: ${title}`);
            const bodyText = await page.evaluate(() => document.body.innerText.substring(0, 2000));
            console.log("Body:", bodyText);
        } catch (e2) {}
    }

    console.log("\n=== END ===");
    await browser.close();
})().catch(e => {
    console.error("Fatal error:", e.message);
    process.exit(1);
});
