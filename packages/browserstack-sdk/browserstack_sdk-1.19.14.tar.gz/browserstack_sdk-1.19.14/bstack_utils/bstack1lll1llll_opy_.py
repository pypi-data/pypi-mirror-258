# coding: UTF-8
import sys
bstack11l1111_opy_ = sys.version_info [0] == 2
bstack11l1l_opy_ = 2048
bstack1l1l1ll_opy_ = 7
def bstack11111_opy_ (bstack111ll11_opy_):
    global bstack1ll1l1l_opy_
    bstack1l111l1_opy_ = ord (bstack111ll11_opy_ [-1])
    bstack111l111_opy_ = bstack111ll11_opy_ [:-1]
    bstack11111ll_opy_ = bstack1l111l1_opy_ % len (bstack111l111_opy_)
    bstack1ll11l1_opy_ = bstack111l111_opy_ [:bstack11111ll_opy_] + bstack111l111_opy_ [bstack11111ll_opy_:]
    if bstack11l1111_opy_:
        bstack1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l_opy_ - (bstack1ll1ll_opy_ + bstack1l111l1_opy_) % bstack1l1l1ll_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1ll11l1_opy_)])
    else:
        bstack1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l_opy_ - (bstack1ll1ll_opy_ + bstack1l111l1_opy_) % bstack1l1l1ll_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1ll11l1_opy_)])
    return eval (bstack1ll11_opy_)
class bstack1ll11l1ll_opy_:
    def __init__(self, handler):
        self._1lllll1l111_opy_ = None
        self.handler = handler
        self._1lllll11lll_opy_ = self.bstack1lllll11ll1_opy_()
        self.patch()
    def patch(self):
        self._1lllll1l111_opy_ = self._1lllll11lll_opy_.execute
        self._1lllll11lll_opy_.execute = self.bstack1lllll11l1l_opy_()
    def bstack1lllll11l1l_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack11111_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࠦᑪ"), driver_command, None, this, args)
            response = self._1lllll1l111_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack11111_opy_ (u"ࠧࡧࡦࡵࡧࡵࠦᑫ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1lllll11lll_opy_.execute = self._1lllll1l111_opy_
    @staticmethod
    def bstack1lllll11ll1_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver