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
from browserstack_sdk.bstack1l1l11l1l_opy_ import bstack1l1lllll_opy_
from browserstack_sdk.bstack1l111lllll_opy_ import RobotHandler
def bstack11l1ll1l1_opy_(framework):
    if framework.lower() == bstack11111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᅶ"):
        return bstack1l1lllll_opy_.version()
    elif framework.lower() == bstack11111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫᅷ"):
        return RobotHandler.version()
    elif framework.lower() == bstack11111_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ᅸ"):
        import behave
        return behave.__version__
    else:
        return bstack11111_opy_ (u"ࠧࡶࡰ࡮ࡲࡴࡽ࡮ࠨᅹ")