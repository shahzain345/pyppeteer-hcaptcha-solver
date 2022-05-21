from pyppeteer import launch
from pyppeteer.page import Page
from pyppeteer.frame_manager import Frame
from .yolo import YOLO
from .exceptions import UnknownException, UnsolvableCaptcha
import asyncio, random, httpx

class PyppeteerHcaptchaSolver:
    """
    # PyppeteerHcaptchaSolver

    A hcaptcha solver for pyppeteer
    """

    def __init__(self, browser):
        self._browser = browser

    async def solve(self, page: Page):
        try:
            res = await self.__detect_captcha(page)
            if res:
                # Hcaptcha is visible now. we can now solve it.
                await page.click("iframe")
                frame = page.frames[1]
                await frame.waitForSelector(".prompt-text")
                elm = await frame.querySelector(".prompt-text")
                _challange_question = await frame.evaluate("""(elm) => elm.textContent""", elm)
                _label = await self.__get_label(_challange_question)
                return await self.__click_all_good_images(frame, page, _label)
            else:
                raise UnknownException("Unsolvable captcha")
        except Exception as e:
            raise Exception("Unsolvable captcha")
    async def __click_all_good_images(self, frame: Frame, page: Page, label: str) -> str:
        client = httpx.Client() # start a httpx client for best perf.
        model = YOLO(dir_model=None, onnx_prefix="yolov5n6")
        for i in range(9):
            await frame.waitForSelector(f'div.task-image:nth-child({i+1})')
            await frame.waitForSelector(f'div.task-image:nth-child({i+1}) > div:nth-child(2) > div:nth-child(1)', { "visible": True })
            await asyncio.sleep(random.uniform(0.1, 1))
            _elm_handle = await frame.querySelector(f"div.task-image:nth-child({i+1}) > div:nth-child(2) > div:nth-child(1)")
            style: str = await frame.evaluate("(elm) => elm.getAttribute('style')", _elm_handle)
            
            url = style.split('url("')[1].split('")')[0]
            if model.solution(img_stream=client.get(url).read(), label=label):
                await frame.click(f"div.task-image:nth-child({i+1})")
        await frame.click(".button-submit") # yay we successfully solved hcaptcha with pyppteer
        await asyncio.sleep(1)
        return await page.evaluate("hcaptcha.getResponse();")
    async def __detect_captcha(self, page: Page) -> bool:
        try:
            await page.waitForSelector("iframe")
            return True
        except Exception as e:
            return False

    async def __get_label(self, label: str) -> str:
        if "containing" in label:
            label = label.split("containing an ")[
                1] if "an" in label else label.split("containing a ")[1]
        label_aliases = {
            'airplane': 'aeroplane',
            'аirplane': 'aeroplane',
            'motorbus': 'bus',
            'mοtorbus': 'bus',
            'truck': 'truck',
            'truсk': 'truck',
            'motorcycle': 'motorbike',
            'boat': 'boat',
            'bicycle': 'bicycle',
            'train': 'train',
            'vertical river': 'vertical river',
            'airplane in the sky flying left': 'airplane in the sky flying left',
            'airplanes in the sky that are flying to the left': 'airplane in the sky flying left',
            'airplanes in the sky that are flying to the right': 'airplane in the sky flying right'
        }
        if label in label_aliases:
            return label_aliases[label]
        else:
            raise UnsolvableCaptcha("Unsolvable captcha")