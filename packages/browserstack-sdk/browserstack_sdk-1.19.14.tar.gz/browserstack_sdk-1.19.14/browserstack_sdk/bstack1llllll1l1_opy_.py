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
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1l11ll1l1_opy_ = {}
        bstack1l11l1ll1l_opy_ = os.environ.get(bstack11111_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪഔ"), bstack11111_opy_ (u"ࠪࠫക"))
        if not bstack1l11l1ll1l_opy_:
            return bstack1l11ll1l1_opy_
        try:
            bstack1l11l1ll11_opy_ = json.loads(bstack1l11l1ll1l_opy_)
            if bstack11111_opy_ (u"ࠦࡴࡹࠢഖ") in bstack1l11l1ll11_opy_:
                bstack1l11ll1l1_opy_[bstack11111_opy_ (u"ࠧࡵࡳࠣഗ")] = bstack1l11l1ll11_opy_[bstack11111_opy_ (u"ࠨ࡯ࡴࠤഘ")]
            if bstack11111_opy_ (u"ࠢࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠦങ") in bstack1l11l1ll11_opy_ or bstack11111_opy_ (u"ࠣࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠦച") in bstack1l11l1ll11_opy_:
                bstack1l11ll1l1_opy_[bstack11111_opy_ (u"ࠤࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠧഛ")] = bstack1l11l1ll11_opy_.get(bstack11111_opy_ (u"ࠥࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠢജ"), bstack1l11l1ll11_opy_.get(bstack11111_opy_ (u"ࠦࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠢഝ")))
            if bstack11111_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࠨഞ") in bstack1l11l1ll11_opy_ or bstack11111_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦട") in bstack1l11l1ll11_opy_:
                bstack1l11ll1l1_opy_[bstack11111_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠧഠ")] = bstack1l11l1ll11_opy_.get(bstack11111_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࠤഡ"), bstack1l11l1ll11_opy_.get(bstack11111_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢഢ")))
            if bstack11111_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧണ") in bstack1l11l1ll11_opy_ or bstack11111_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠧത") in bstack1l11l1ll11_opy_:
                bstack1l11ll1l1_opy_[bstack11111_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳࠨഥ")] = bstack1l11l1ll11_opy_.get(bstack11111_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣദ"), bstack1l11l1ll11_opy_.get(bstack11111_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠣധ")))
            if bstack11111_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࠣന") in bstack1l11l1ll11_opy_ or bstack11111_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪࠨഩ") in bstack1l11l1ll11_opy_:
                bstack1l11ll1l1_opy_[bstack11111_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠢപ")] = bstack1l11l1ll11_opy_.get(bstack11111_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࠦഫ"), bstack1l11l1ll11_opy_.get(bstack11111_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠤബ")))
            if bstack11111_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠣഭ") in bstack1l11l1ll11_opy_ or bstack11111_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨമ") in bstack1l11l1ll11_opy_:
                bstack1l11ll1l1_opy_[bstack11111_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢയ")] = bstack1l11l1ll11_opy_.get(bstack11111_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦര"), bstack1l11l1ll11_opy_.get(bstack11111_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤറ")))
            if bstack11111_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠢല") in bstack1l11l1ll11_opy_ or bstack11111_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢള") in bstack1l11l1ll11_opy_:
                bstack1l11ll1l1_opy_[bstack11111_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣഴ")] = bstack1l11l1ll11_opy_.get(bstack11111_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠥവ"), bstack1l11l1ll11_opy_.get(bstack11111_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥശ")))
            if bstack11111_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠦഷ") in bstack1l11l1ll11_opy_:
                bstack1l11ll1l1_opy_[bstack11111_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠧസ")] = bstack1l11l1ll11_opy_[bstack11111_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸࠨഹ")]
        except Exception as error:
            logger.error(bstack11111_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩࡧࡴࡢ࠼ࠣࠦഺ") +  str(error))
        return bstack1l11ll1l1_opy_