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
import sys
class bstack11lll1ll11_opy_:
    def __init__(self, handler):
        self._11l1ll1l11_opy_ = sys.stdout.write
        self._11l1ll1l1l_opy_ = sys.stderr.write
        self.handler = handler
        self._started = False
    def start(self):
        if self._started:
            return
        self._started = True
        sys.stdout.write = self.bstack11l1ll1ll1_opy_
        sys.stdout.error = self.bstack11l1ll11ll_opy_
    def bstack11l1ll1ll1_opy_(self, _str):
        self._11l1ll1l11_opy_(_str)
        if self.handler:
            self.handler({bstack11111_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪໝ"): bstack11111_opy_ (u"ࠬࡏࡎࡇࡑࠪໞ"), bstack11111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧໟ"): _str})
    def bstack11l1ll11ll_opy_(self, _str):
        self._11l1ll1l1l_opy_(_str)
        if self.handler:
            self.handler({bstack11111_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭໠"): bstack11111_opy_ (u"ࠨࡇࡕࡖࡔࡘࠧ໡"), bstack11111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ໢"): _str})
    def reset(self):
        if not self._started:
            return
        self._started = False
        sys.stdout.write = self._11l1ll1l11_opy_
        sys.stderr.write = self._11l1ll1l1l_opy_