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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.helper import bstack11l1111111_opy_, bstack1lll11ll1l_opy_, bstack1ll1l11ll_opy_, bstack1l1l1l1l1l_opy_, \
    bstack11l11l1ll1_opy_
def bstack111ll1lll_opy_(bstack1lllll11l11_opy_):
    for driver in bstack1lllll11l11_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1ll1l1111_opy_(driver, status, reason=bstack11111_opy_ (u"࠭ࠧᑬ")):
    bstack11111111_opy_ = Config.bstack111l111l_opy_()
    if bstack11111111_opy_.bstack11lll1l1l1_opy_():
        return
    bstack11llll11_opy_ = bstack1l1llllll1_opy_(bstack11111_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪᑭ"), bstack11111_opy_ (u"ࠨࠩᑮ"), status, reason, bstack11111_opy_ (u"ࠩࠪᑯ"), bstack11111_opy_ (u"ࠪࠫᑰ"))
    driver.execute_script(bstack11llll11_opy_)
def bstack11l1ll111_opy_(page, status, reason=bstack11111_opy_ (u"ࠫࠬᑱ")):
    try:
        if page is None:
            return
        bstack11111111_opy_ = Config.bstack111l111l_opy_()
        if bstack11111111_opy_.bstack11lll1l1l1_opy_():
            return
        bstack11llll11_opy_ = bstack1l1llllll1_opy_(bstack11111_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨᑲ"), bstack11111_opy_ (u"࠭ࠧᑳ"), status, reason, bstack11111_opy_ (u"ࠧࠨᑴ"), bstack11111_opy_ (u"ࠨࠩᑵ"))
        page.evaluate(bstack11111_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥᑶ"), bstack11llll11_opy_)
    except Exception as e:
        print(bstack11111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡫ࡵࡲࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࢁࡽࠣᑷ"), e)
def bstack1l1llllll1_opy_(type, name, status, reason, bstack1l1ll11l11_opy_, bstack1l11ll1l_opy_):
    bstack111l111l1_opy_ = {
        bstack11111_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫᑸ"): type,
        bstack11111_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᑹ"): {}
    }
    if type == bstack11111_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨᑺ"):
        bstack111l111l1_opy_[bstack11111_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᑻ")][bstack11111_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᑼ")] = bstack1l1ll11l11_opy_
        bstack111l111l1_opy_[bstack11111_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᑽ")][bstack11111_opy_ (u"ࠪࡨࡦࡺࡡࠨᑾ")] = json.dumps(str(bstack1l11ll1l_opy_))
    if type == bstack11111_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᑿ"):
        bstack111l111l1_opy_[bstack11111_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᒀ")][bstack11111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᒁ")] = name
    if type == bstack11111_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪᒂ"):
        bstack111l111l1_opy_[bstack11111_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᒃ")][bstack11111_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᒄ")] = status
        if status == bstack11111_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᒅ") and str(reason) != bstack11111_opy_ (u"ࠦࠧᒆ"):
            bstack111l111l1_opy_[bstack11111_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᒇ")][bstack11111_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ᒈ")] = json.dumps(str(reason))
    bstack1ll1lll11l_opy_ = bstack11111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬᒉ").format(json.dumps(bstack111l111l1_opy_))
    return bstack1ll1lll11l_opy_
def bstack1llll1l11_opy_(url, config, logger, bstack11llll111_opy_=False):
    hostname = bstack1lll11ll1l_opy_(url)
    is_private = bstack1l1l1l1l1l_opy_(hostname)
    try:
        if is_private or bstack11llll111_opy_:
            file_path = bstack11l1111111_opy_(bstack11111_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᒊ"), bstack11111_opy_ (u"ࠩ࠱ࡦࡸࡺࡡࡤ࡭࠰ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨᒋ"), logger)
            if os.environ.get(bstack11111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨᒌ")) and eval(
                    os.environ.get(bstack11111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩᒍ"))):
                return
            if (bstack11111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩᒎ") in config and not config[bstack11111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪᒏ")]):
                os.environ[bstack11111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬᒐ")] = str(True)
                bstack1lllll1111l_opy_ = {bstack11111_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪᒑ"): hostname}
                bstack11l11l1ll1_opy_(bstack11111_opy_ (u"ࠩ࠱ࡦࡸࡺࡡࡤ࡭࠰ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨᒒ"), bstack11111_opy_ (u"ࠪࡲࡺࡪࡧࡦࡡ࡯ࡳࡨࡧ࡬ࠨᒓ"), bstack1lllll1111l_opy_, logger)
    except Exception as e:
        pass
def bstack1l1ll1lll1_opy_(caps, bstack1lllll111l1_opy_):
    if bstack11111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᒔ") in caps:
        caps[bstack11111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᒕ")][bstack11111_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬᒖ")] = True
        if bstack1lllll111l1_opy_:
            caps[bstack11111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᒗ")][bstack11111_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᒘ")] = bstack1lllll111l1_opy_
    else:
        caps[bstack11111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࠧᒙ")] = True
        if bstack1lllll111l1_opy_:
            caps[bstack11111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᒚ")] = bstack1lllll111l1_opy_
def bstack1llllllllll_opy_(bstack11llll111l_opy_):
    bstack1lllll111ll_opy_ = bstack1ll1l11ll_opy_(threading.current_thread(), bstack11111_opy_ (u"ࠫࡹ࡫ࡳࡵࡕࡷࡥࡹࡻࡳࠨᒛ"), bstack11111_opy_ (u"ࠬ࠭ᒜ"))
    if bstack1lllll111ll_opy_ == bstack11111_opy_ (u"࠭ࠧᒝ") or bstack1lllll111ll_opy_ == bstack11111_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨᒞ"):
        threading.current_thread().testStatus = bstack11llll111l_opy_
    else:
        if bstack11llll111l_opy_ == bstack11111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᒟ"):
            threading.current_thread().testStatus = bstack11llll111l_opy_