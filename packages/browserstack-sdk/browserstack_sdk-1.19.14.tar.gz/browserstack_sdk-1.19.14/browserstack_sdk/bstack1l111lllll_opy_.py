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
import os
class RobotHandler():
    def __init__(self, args, logger, bstack11lll111l1_opy_, bstack11lll11l11_opy_):
        self.args = args
        self.logger = logger
        self.bstack11lll111l1_opy_ = bstack11lll111l1_opy_
        self.bstack11lll11l11_opy_ = bstack11lll11l11_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1l11111ll1_opy_(bstack11ll1ll1l1_opy_):
        bstack11ll1ll11l_opy_ = []
        if bstack11ll1ll1l1_opy_:
            tokens = str(os.path.basename(bstack11ll1ll1l1_opy_)).split(bstack11111_opy_ (u"ࠣࡡࠥฤ"))
            camelcase_name = bstack11111_opy_ (u"ࠤࠣࠦล").join(t.title() for t in tokens)
            suite_name, bstack11ll1ll1ll_opy_ = os.path.splitext(camelcase_name)
            bstack11ll1ll11l_opy_.append(suite_name)
        return bstack11ll1ll11l_opy_
    @staticmethod
    def bstack11ll1lll11_opy_(typename):
        if bstack11111_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨฦ") in typename:
            return bstack11111_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧว")
        return bstack11111_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨศ")