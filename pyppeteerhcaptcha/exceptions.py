class HcaptchaExceptions(Exception):
    """Base class for all non-exit hcaptcha exceptions"""
class UnsolvableCaptcha(HcaptchaExceptions):
    """The captcha is unsolvable"""
class UnknownException(HcaptchaExceptions):
    """A exception that is unknown. lol"""