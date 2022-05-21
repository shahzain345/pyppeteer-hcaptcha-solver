# Pyppeteer Hcaptcha

A fork of [Puppeteer Hcaptcha Solver](https://github.com/shahzain345/puppeteer-hcaptcha-solver) for python.

## Features
Asynchronous
Fast
Easy to use
Solves hcaptcha on any site

## Installation

```pip install pyppeteer-hcaptcha-solver```

## License:

MIT

## Basic Usage:

```py
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
    token = await solver.solve(page) # boom hcaptcha is solved!!!
    print(token)
asyncio.get_event_loop().run_until_complete(main())
```

## Pyppeteer Hcaptcha In Action

![]([https://hi.shahzain.me/r/pyppeteer-hcaptcha.gif](https://us-east-1.tixte.net/uploads/hi.shahzain.me/pyppeteer-hcaptcha.gif))
