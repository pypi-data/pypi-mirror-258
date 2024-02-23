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
import multiprocessing
import os
import json
from time import sleep
import bstack_utils.bstack1l1111ll1_opy_ as bstack1ll1l11ll1_opy_
from browserstack_sdk.bstack1l11ll1l1l_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1l111l1l_opy_
class bstack1l1lllll_opy_:
    def __init__(self, args, logger, bstack11lll111l1_opy_, bstack11lll11l11_opy_):
        self.args = args
        self.logger = logger
        self.bstack11lll111l1_opy_ = bstack11lll111l1_opy_
        self.bstack11lll11l11_opy_ = bstack11lll11l11_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack111l11ll_opy_ = []
        self.bstack11lll1l111_opy_ = None
        self.bstack1llll11111_opy_ = []
        self.bstack11lll1111l_opy_ = self.bstack1l11llllll_opy_()
        self.bstack11l11ll1_opy_ = -1
    def bstack11l11llll_opy_(self, bstack11lll11111_opy_):
        self.parse_args()
        self.bstack11lll1l11l_opy_()
        self.bstack11ll1lllll_opy_(bstack11lll11111_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    def bstack11lll11l1l_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack11l11ll1_opy_ = -1
        if bstack11111_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧง") in self.bstack11lll111l1_opy_:
            self.bstack11l11ll1_opy_ = int(self.bstack11lll111l1_opy_[bstack11111_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨจ")])
        try:
            bstack11ll1llll1_opy_ = [bstack11111_opy_ (u"ࠩ࠰࠱ࡩࡸࡩࡷࡧࡵࠫฉ"), bstack11111_opy_ (u"ࠪ࠱࠲ࡶ࡬ࡶࡩ࡬ࡲࡸ࠭ช"), bstack11111_opy_ (u"ࠫ࠲ࡶࠧซ")]
            if self.bstack11l11ll1_opy_ >= 0:
                bstack11ll1llll1_opy_.extend([bstack11111_opy_ (u"ࠬ࠳࠭࡯ࡷࡰࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭ฌ"), bstack11111_opy_ (u"࠭࠭࡯ࠩญ")])
            for arg in bstack11ll1llll1_opy_:
                self.bstack11lll11l1l_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack11lll1l11l_opy_(self):
        bstack11lll1l111_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack11lll1l111_opy_ = bstack11lll1l111_opy_
        return bstack11lll1l111_opy_
    def bstack1111l111l_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            import importlib
            bstack11lll111ll_opy_ = importlib.find_loader(bstack11111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩฎ"))
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1l111l1l_opy_)
    def bstack11ll1lllll_opy_(self, bstack11lll11111_opy_):
        bstack11111111_opy_ = Config.bstack111l111l_opy_()
        if bstack11lll11111_opy_:
            self.bstack11lll1l111_opy_.append(bstack11111_opy_ (u"ࠨ࠯࠰ࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬฏ"))
            self.bstack11lll1l111_opy_.append(bstack11111_opy_ (u"ࠩࡗࡶࡺ࡫ࠧฐ"))
        if bstack11111111_opy_.bstack11lll1l1l1_opy_():
            self.bstack11lll1l111_opy_.append(bstack11111_opy_ (u"ࠪ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩฑ"))
            self.bstack11lll1l111_opy_.append(bstack11111_opy_ (u"࡙ࠫࡸࡵࡦࠩฒ"))
        self.bstack11lll1l111_opy_.append(bstack11111_opy_ (u"ࠬ࠳ࡰࠨณ"))
        self.bstack11lll1l111_opy_.append(bstack11111_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡵࡲࡵࡨ࡫ࡱࠫด"))
        self.bstack11lll1l111_opy_.append(bstack11111_opy_ (u"ࠧ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠩต"))
        self.bstack11lll1l111_opy_.append(bstack11111_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨถ"))
        if self.bstack11l11ll1_opy_ > 1:
            self.bstack11lll1l111_opy_.append(bstack11111_opy_ (u"ࠩ࠰ࡲࠬท"))
            self.bstack11lll1l111_opy_.append(str(self.bstack11l11ll1_opy_))
    def bstack11lll1l1ll_opy_(self):
        bstack1llll11111_opy_ = []
        for spec in self.bstack111l11ll_opy_:
            bstack1l1l11l111_opy_ = [spec]
            bstack1l1l11l111_opy_ += self.bstack11lll1l111_opy_
            bstack1llll11111_opy_.append(bstack1l1l11l111_opy_)
        self.bstack1llll11111_opy_ = bstack1llll11111_opy_
        return bstack1llll11111_opy_
    def bstack1l11llllll_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack11lll1111l_opy_ = True
            return True
        except Exception as e:
            self.bstack11lll1111l_opy_ = False
        return self.bstack11lll1111l_opy_
    def bstack1llll11ll1_opy_(self, bstack11lll11lll_opy_, bstack11l11llll_opy_):
        bstack11l11llll_opy_[bstack11111_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪธ")] = self.bstack11lll111l1_opy_
        multiprocessing.set_start_method(bstack11111_opy_ (u"ࠫࡸࡶࡡࡸࡰࠪน"))
        if bstack11111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨบ") in self.bstack11lll111l1_opy_:
            bstack1ll111l11_opy_ = []
            manager = multiprocessing.Manager()
            bstack1l1l11lll1_opy_ = manager.list()
            for index, platform in enumerate(self.bstack11lll111l1_opy_[bstack11111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩป")]):
                bstack1ll111l11_opy_.append(multiprocessing.Process(name=str(index),
                                                           target=bstack11lll11lll_opy_,
                                                           args=(self.bstack11lll1l111_opy_, bstack11l11llll_opy_, bstack1l1l11lll1_opy_)))
            i = 0
            bstack11ll1lll1l_opy_ = len(self.bstack11lll111l1_opy_[bstack11111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪผ")])
            for t in bstack1ll111l11_opy_:
                os.environ[bstack11111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨฝ")] = str(i)
                os.environ[bstack11111_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪพ")] = json.dumps(self.bstack11lll111l1_opy_[bstack11111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ฟ")][i % bstack11ll1lll1l_opy_])
                i += 1
                t.start()
            for t in bstack1ll111l11_opy_:
                t.join()
            return list(bstack1l1l11lll1_opy_)
    @staticmethod
    def bstack1l1lll11l1_opy_(driver, bstack1l1l1l1l1_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack11111_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨภ"), None)
        if item and getattr(item, bstack11111_opy_ (u"ࠬࡥࡡ࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡦࡥࡸ࡫ࠧม"), None) and not getattr(item, bstack11111_opy_ (u"࠭࡟ࡢ࠳࠴ࡽࡤࡹࡴࡰࡲࡢࡨࡴࡴࡥࠨย"), False):
            logger.info(
                bstack11111_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡵ࡮ࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠥࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡩࡳࡷࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡪࡵࠣࡹࡳࡪࡥࡳࡹࡤࡽ࠳ࠨร"))
            bstack11lll11ll1_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1ll1l11ll1_opy_.bstack11llll1l1_opy_(driver, bstack11lll11ll1_opy_, item.name, item.module.__name__, item.path, bstack1l1l1l1l1_opy_)
            item._a11y_stop_done = True
            if wait:
                sleep(2)