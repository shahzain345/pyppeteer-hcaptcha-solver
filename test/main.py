from pyppeteer import launch
from pyppeteerhcaptcha import PyppeteerHcaptchaSolver
import asyncio
async def main():
    browser = await launch({ "headless": False })
    solver = PyppeteerHcaptchaSolver(browser)
    page = await browser.newPage()
    await page.goto("https://accounts.hcaptcha.com/demo?sitekey=4c672d35-0701-42b2-88c3-78380b0db560")
    await page.waitForSelector("iframe")
    await asyncio.sleep(2)
    token = await solver.solve(page)
    print(token)
    input("Exit(PRESS ENTER)")
asyncio.get_event_loop().run_until_complete(main())
