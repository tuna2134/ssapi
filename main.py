from sanic import Sanic
from sanic.response import file, json
from playwright.async_api import async_playwright

app = Sanic("app")

@app.post("/api")
async def api(request):
    data = request.json
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto(data["url"])
        except:
            await browser.close()
            return json({"error": "please check url"})
        else:
            await page.screenshot(path="image.png")
            await browser.close()
            return await file("image.png")

app.run(host="0.0.0.0", port=8080)
