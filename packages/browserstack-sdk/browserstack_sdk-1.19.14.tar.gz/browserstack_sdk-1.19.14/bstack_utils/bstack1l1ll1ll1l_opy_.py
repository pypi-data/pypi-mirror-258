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
from collections import deque
from bstack_utils.constants import *
class bstack111lll11_opy_:
    def __init__(self):
        self._11111l1l11_opy_ = deque()
        self._111111ll11_opy_ = {}
        self._11111l11l1_opy_ = False
    def bstack11111l1111_opy_(self, test_name, bstack111111lll1_opy_):
        bstack111111l1l1_opy_ = self._111111ll11_opy_.get(test_name, {})
        return bstack111111l1l1_opy_.get(bstack111111lll1_opy_, 0)
    def bstack11111l11ll_opy_(self, test_name, bstack111111lll1_opy_):
        bstack111111llll_opy_ = self.bstack11111l1111_opy_(test_name, bstack111111lll1_opy_)
        self.bstack111111ll1l_opy_(test_name, bstack111111lll1_opy_)
        return bstack111111llll_opy_
    def bstack111111ll1l_opy_(self, test_name, bstack111111lll1_opy_):
        if test_name not in self._111111ll11_opy_:
            self._111111ll11_opy_[test_name] = {}
        bstack111111l1l1_opy_ = self._111111ll11_opy_[test_name]
        bstack111111llll_opy_ = bstack111111l1l1_opy_.get(bstack111111lll1_opy_, 0)
        bstack111111l1l1_opy_[bstack111111lll1_opy_] = bstack111111llll_opy_ + 1
    def bstack1lll1111l1_opy_(self, bstack11111l1lll_opy_, bstack111111l1ll_opy_):
        bstack11111l1ll1_opy_ = self.bstack11111l11ll_opy_(bstack11111l1lll_opy_, bstack111111l1ll_opy_)
        bstack11111l111l_opy_ = bstack11l1l1ll1l_opy_[bstack111111l1ll_opy_]
        bstack11111l1l1l_opy_ = bstack11111_opy_ (u"ࠨࡻࡾ࠯ࡾࢁ࠲ࢁࡽࠣᐑ").format(bstack11111l1lll_opy_, bstack11111l111l_opy_, bstack11111l1ll1_opy_)
        self._11111l1l11_opy_.append(bstack11111l1l1l_opy_)
    def bstack111111ll_opy_(self):
        return len(self._11111l1l11_opy_) == 0
    def bstack111ll111_opy_(self):
        bstack11111ll111_opy_ = self._11111l1l11_opy_.popleft()
        return bstack11111ll111_opy_
    def capturing(self):
        return self._11111l11l1_opy_
    def bstack1ll11ll11l_opy_(self):
        self._11111l11l1_opy_ = True
    def bstack1ll1lllll_opy_(self):
        self._11111l11l1_opy_ = False