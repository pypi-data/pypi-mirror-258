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
import datetime
import json
import logging
import os
import threading
from bstack_utils.helper import bstack11l1lllll1_opy_, bstack11lll1lll_opy_, get_host_info, bstack11ll1l1ll1_opy_, bstack11ll111l11_opy_, bstack11l11111l1_opy_, \
    bstack11l1l11111_opy_, bstack111llll1l1_opy_, bstack1lll11l11l_opy_, bstack111lllll1l_opy_, bstack1ll1ll11_opy_, bstack1l111ll1ll_opy_
from bstack_utils.bstack1lllll1llll_opy_ import bstack1lllll1l1ll_opy_
from bstack_utils.bstack1l1111111l_opy_ import bstack1l11l11lll_opy_
import bstack_utils.bstack1l1111ll1_opy_ as bstack1ll1l11ll1_opy_
from bstack_utils.constants import bstack11l1l1l1ll_opy_
bstack1lll1llll1l_opy_ = [
    bstack11111_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬᓞ"), bstack11111_opy_ (u"ࠩࡆࡆ࡙࡙ࡥࡴࡵ࡬ࡳࡳࡉࡲࡦࡣࡷࡩࡩ࠭ᓟ"), bstack11111_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᓠ"), bstack11111_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬᓡ"),
    bstack11111_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᓢ"), bstack11111_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᓣ"), bstack11111_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᓤ")
]
bstack1llll111l11_opy_ = bstack11111_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡦࡳࡱࡲࡥࡤࡶࡲࡶ࠲ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨᓥ")
logger = logging.getLogger(__name__)
class bstack11ll1l1l1_opy_:
    bstack1lllll1llll_opy_ = None
    bs_config = None
    @classmethod
    @bstack1l111ll1ll_opy_(class_method=True)
    def launch(cls, bs_config, bstack1llll11111l_opy_):
        cls.bs_config = bs_config
        cls.bstack1llll11l1ll_opy_()
        bstack11l1llllll_opy_ = bstack11ll1l1ll1_opy_(bs_config)
        bstack11ll1ll111_opy_ = bstack11ll111l11_opy_(bs_config)
        bstack1lll11l1l1_opy_ = False
        bstack1ll11l111l_opy_ = False
        if bstack11111_opy_ (u"ࠩࡤࡴࡵ࠭ᓦ") in bs_config:
            bstack1lll11l1l1_opy_ = True
        else:
            bstack1ll11l111l_opy_ = True
        bstack1lllll11ll_opy_ = {
            bstack11111_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᓧ"): cls.bstack1llll1111l_opy_(),
            bstack11111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᓨ"): bstack1ll1l11ll1_opy_.bstack1lllll11l1_opy_(bs_config),
            bstack11111_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫᓩ"): bs_config.get(bstack11111_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬᓪ"), False),
            bstack11111_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩᓫ"): bstack1ll11l111l_opy_,
            bstack11111_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᓬ"): bstack1lll11l1l1_opy_
        }
        data = {
            bstack11111_opy_ (u"ࠩࡩࡳࡷࡳࡡࡵࠩᓭ"): bstack11111_opy_ (u"ࠪ࡮ࡸࡵ࡮ࠨᓮ"),
            bstack11111_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡤࡴࡡ࡮ࡧࠪᓯ"): bs_config.get(bstack11111_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪᓰ"), bstack11111_opy_ (u"࠭ࠧᓱ")),
            bstack11111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᓲ"): bs_config.get(bstack11111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫᓳ"), os.path.basename(os.path.abspath(os.getcwd()))),
            bstack11111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᓴ"): bs_config.get(bstack11111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᓵ")),
            bstack11111_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩᓶ"): bs_config.get(bstack11111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡈࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨᓷ"), bstack11111_opy_ (u"࠭ࠧᓸ")),
            bstack11111_opy_ (u"ࠧࡴࡶࡤࡶࡹࡥࡴࡪ࡯ࡨࠫᓹ"): datetime.datetime.now().isoformat(),
            bstack11111_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᓺ"): bstack11l11111l1_opy_(bs_config),
            bstack11111_opy_ (u"ࠩ࡫ࡳࡸࡺ࡟ࡪࡰࡩࡳࠬᓻ"): get_host_info(),
            bstack11111_opy_ (u"ࠪࡧ࡮ࡥࡩ࡯ࡨࡲࠫᓼ"): bstack11lll1lll_opy_(),
            bstack11111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢࡶࡺࡴ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᓽ"): os.environ.get(bstack11111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫᓾ")),
            bstack11111_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩࡥࡴࡦࡵࡷࡷࡤࡸࡥࡳࡷࡱࠫᓿ"): os.environ.get(bstack11111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࠬᔀ"), False),
            bstack11111_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࡡࡦࡳࡳࡺࡲࡰ࡮ࠪᔁ"): bstack11l1lllll1_opy_(),
            bstack11111_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧᔂ"): bstack1lllll11ll_opy_,
            bstack11111_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࡢࡺࡪࡸࡳࡪࡱࡱࠫᔃ"): {
                bstack11111_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡎࡢ࡯ࡨࠫᔄ"): bstack1llll11111l_opy_.get(bstack11111_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪ࠭ᔅ"), bstack11111_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭ᔆ")),
                bstack11111_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪᔇ"): bstack1llll11111l_opy_.get(bstack11111_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᔈ")),
                bstack11111_opy_ (u"ࠩࡶࡨࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᔉ"): bstack1llll11111l_opy_.get(bstack11111_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᔊ"))
            }
        }
        config = {
            bstack11111_opy_ (u"ࠫࡦࡻࡴࡩࠩᔋ"): (bstack11l1llllll_opy_, bstack11ll1ll111_opy_),
            bstack11111_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ᔌ"): cls.default_headers()
        }
        response = bstack1lll11l11l_opy_(bstack11111_opy_ (u"࠭ࡐࡐࡕࡗࠫᔍ"), cls.request_url(bstack11111_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡷ࡬ࡰࡩࡹࠧᔎ")), data, config)
        if response.status_code != 200:
            os.environ[bstack11111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ᔏ")] = bstack11111_opy_ (u"ࠩࡱࡹࡱࡲࠧᔐ")
            os.environ[bstack11111_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡃࡐࡏࡓࡐࡊ࡚ࡅࡅࠩᔑ")] = bstack11111_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪᔒ")
            os.environ[bstack11111_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭ᔓ")] = bstack11111_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᔔ")
            os.environ[bstack11111_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭ᔕ")] = bstack11111_opy_ (u"ࠣࡰࡸࡰࡱࠨᔖ")
            os.environ[bstack11111_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪᔗ")] = bstack11111_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᔘ")
            bstack1llll111111_opy_ = response.json()
            if bstack1llll111111_opy_ and bstack1llll111111_opy_[bstack11111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᔙ")]:
                error_message = bstack1llll111111_opy_[bstack11111_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᔚ")]
                if bstack1llll111111_opy_[bstack11111_opy_ (u"࠭ࡥࡳࡴࡲࡶ࡙ࡿࡰࡦࠩᔛ")] == bstack11111_opy_ (u"ࠧࡆࡔࡕࡓࡗࡥࡉࡏࡘࡄࡐࡎࡊ࡟ࡄࡔࡈࡈࡊࡔࡔࡊࡃࡏࡗࠬᔜ"):
                    logger.error(error_message)
                elif bstack1llll111111_opy_[bstack11111_opy_ (u"ࠨࡧࡵࡶࡴࡸࡔࡺࡲࡨࠫᔝ")] == bstack11111_opy_ (u"ࠩࡈࡖࡗࡕࡒࡠࡃࡆࡇࡊ࡙ࡓࡠࡆࡈࡒࡎࡋࡄࠨᔞ"):
                    logger.info(error_message)
                elif bstack1llll111111_opy_[bstack11111_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡖࡼࡴࡪ࠭ᔟ")] == bstack11111_opy_ (u"ࠫࡊࡘࡒࡐࡔࡢࡗࡉࡑ࡟ࡅࡇࡓࡖࡊࡉࡁࡕࡇࡇࠫᔠ"):
                    logger.error(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack11111_opy_ (u"ࠧࡊࡡࡵࡣࠣࡹࡵࡲ࡯ࡢࡦࠣࡸࡴࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯࡚ࠥࡥࡴࡶࠣࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠣࡪࡦ࡯࡬ࡦࡦࠣࡨࡺ࡫ࠠࡵࡱࠣࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠢᔡ"))
            return [None, None, None]
        bstack1llll111111_opy_ = response.json()
        os.environ[bstack11111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᔢ")] = bstack1llll111111_opy_[bstack11111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩᔣ")]
        if cls.bstack1llll1111l_opy_() is True and bstack1llll11111l_opy_.get(bstack11111_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡺࡹࡥࡥࠩᔤ")) in bstack11l1l1l1ll_opy_:
            logger.debug(bstack11111_opy_ (u"ࠩࡗࡩࡸࡺࠠࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠠࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠦ࠭ᔥ"))
            os.environ[bstack11111_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡃࡐࡏࡓࡐࡊ࡚ࡅࡅࠩᔦ")] = bstack11111_opy_ (u"ࠫࡹࡸࡵࡦࠩᔧ")
            if bstack1llll111111_opy_.get(bstack11111_opy_ (u"ࠬࡰࡷࡵࠩᔨ")):
                os.environ[bstack11111_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧᔩ")] = bstack1llll111111_opy_[bstack11111_opy_ (u"ࠧ࡫ࡹࡷࠫᔪ")]
                os.environ[bstack11111_opy_ (u"ࠨࡅࡕࡉࡉࡋࡎࡕࡋࡄࡐࡘࡥࡆࡐࡔࡢࡇࡗࡇࡓࡉࡡࡕࡉࡕࡕࡒࡕࡋࡑࡋࠬᔫ")] = json.dumps({
                    bstack11111_opy_ (u"ࠩࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫᔬ"): bstack11l1llllll_opy_,
                    bstack11111_opy_ (u"ࠪࡴࡦࡹࡳࡸࡱࡵࡨࠬᔭ"): bstack11ll1ll111_opy_
                })
            if bstack1llll111111_opy_.get(bstack11111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ᔮ")):
                os.environ[bstack11111_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫᔯ")] = bstack1llll111111_opy_[bstack11111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨᔰ")]
            if bstack1llll111111_opy_.get(bstack11111_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫᔱ")):
                os.environ[bstack11111_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩᔲ")] = str(bstack1llll111111_opy_[bstack11111_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭ᔳ")])
        return [bstack1llll111111_opy_[bstack11111_opy_ (u"ࠪ࡮ࡼࡺࠧᔴ")], bstack1llll111111_opy_[bstack11111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ᔵ")], bstack1llll111111_opy_[bstack11111_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩᔶ")]]
    @classmethod
    @bstack1l111ll1ll_opy_(class_method=True)
    def stop(cls):
        if not cls.on():
            return
        if os.environ[bstack11111_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧᔷ")] == bstack11111_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧᔸ") or os.environ[bstack11111_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧᔹ")] == bstack11111_opy_ (u"ࠤࡱࡹࡱࡲࠢᔺ"):
            print(bstack11111_opy_ (u"ࠪࡉ࡝ࡉࡅࡑࡖࡌࡓࡓࠦࡉࡏࠢࡶࡸࡴࡶࡂࡶ࡫࡯ࡨ࡚ࡶࡳࡵࡴࡨࡥࡲࠦࡒࡆࡓࡘࡉࡘ࡚ࠠࡕࡑࠣࡘࡊ࡙ࡔࠡࡑࡅࡗࡊࡘࡖࡂࡄࡌࡐࡎ࡚࡙ࠡ࠼ࠣࡑ࡮ࡹࡳࡪࡰࡪࠤࡦࡻࡴࡩࡧࡱࡸ࡮ࡩࡡࡵ࡫ࡲࡲࠥࡺ࡯࡬ࡧࡱࠫᔻ"))
            return {
                bstack11111_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᔼ"): bstack11111_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᔽ"),
                bstack11111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᔾ"): bstack11111_opy_ (u"ࠧࡕࡱ࡮ࡩࡳ࠵ࡢࡶ࡫࡯ࡨࡎࡊࠠࡪࡵࠣࡹࡳࡪࡥࡧ࡫ࡱࡩࡩ࠲ࠠࡣࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡ࡯࡬࡫࡭ࡺࠠࡩࡣࡹࡩࠥ࡬ࡡࡪ࡮ࡨࡨࠬᔿ")
            }
        else:
            cls.bstack1lllll1llll_opy_.shutdown()
            data = {
                bstack11111_opy_ (u"ࠨࡵࡷࡳࡵࡥࡴࡪ࡯ࡨࠫᕀ"): datetime.datetime.now().isoformat()
            }
            config = {
                bstack11111_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪᕁ"): cls.default_headers()
            }
            bstack111llll111_opy_ = bstack11111_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂ࠵ࡳࡵࡱࡳࠫᕂ").format(os.environ[bstack11111_opy_ (u"ࠦࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠥᕃ")])
            bstack1llll1111l1_opy_ = cls.request_url(bstack111llll111_opy_)
            response = bstack1lll11l11l_opy_(bstack11111_opy_ (u"ࠬࡖࡕࡕࠩᕄ"), bstack1llll1111l1_opy_, data, config)
            if not response.ok:
                raise Exception(bstack11111_opy_ (u"ࠨࡓࡵࡱࡳࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡴ࡯ࡵࠢࡲ࡯ࠧᕅ"))
    @classmethod
    def bstack1l11111lll_opy_(cls):
        if cls.bstack1lllll1llll_opy_ is None:
            return
        cls.bstack1lllll1llll_opy_.shutdown()
    @classmethod
    def bstack1lll11111_opy_(cls):
        if cls.on():
            print(
                bstack11111_opy_ (u"ࠧࡗ࡫ࡶ࡭ࡹࠦࡨࡵࡶࡳࡷ࠿࠵࠯ࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂࠦࡴࡰࠢࡹ࡭ࡪࡽࠠࡣࡷ࡬ࡰࡩࠦࡲࡦࡲࡲࡶࡹ࠲ࠠࡪࡰࡶ࡭࡬࡮ࡴࡴ࠮ࠣࡥࡳࡪࠠ࡮ࡣࡱࡽࠥࡳ࡯ࡳࡧࠣࡨࡪࡨࡵࡨࡩ࡬ࡲ࡬ࠦࡩ࡯ࡨࡲࡶࡲࡧࡴࡪࡱࡱࠤࡦࡲ࡬ࠡࡣࡷࠤࡴࡴࡥࠡࡲ࡯ࡥࡨ࡫ࠡ࡝ࡰࠪᕆ").format(os.environ[bstack11111_opy_ (u"ࠣࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠢᕇ")]))
    @classmethod
    def bstack1llll11l1ll_opy_(cls):
        if cls.bstack1lllll1llll_opy_ is not None:
            return
        cls.bstack1lllll1llll_opy_ = bstack1lllll1l1ll_opy_(cls.bstack1llll111ll1_opy_)
        cls.bstack1lllll1llll_opy_.start()
    @classmethod
    def bstack1l11l11111_opy_(cls, bstack11lllll11l_opy_, bstack1lll1llllll_opy_=bstack11111_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡥࡹࡩࡨࠨᕈ")):
        if not cls.on():
            return
        bstack1ll11lll_opy_ = bstack11lllll11l_opy_[bstack11111_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᕉ")]
        bstack1llll11l111_opy_ = {
            bstack11111_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᕊ"): bstack11111_opy_ (u"࡚ࠬࡥࡴࡶࡢࡗࡹࡧࡲࡵࡡࡘࡴࡱࡵࡡࡥࠩᕋ"),
            bstack11111_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᕌ"): bstack11111_opy_ (u"ࠧࡕࡧࡶࡸࡤࡋ࡮ࡥࡡࡘࡴࡱࡵࡡࡥࠩᕍ"),
            bstack11111_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩᕎ"): bstack11111_opy_ (u"ࠩࡗࡩࡸࡺ࡟ࡔ࡭࡬ࡴࡵ࡫ࡤࡠࡗࡳࡰࡴࡧࡤࠨᕏ"),
            bstack11111_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧᕐ"): bstack11111_opy_ (u"ࠫࡑࡵࡧࡠࡗࡳࡰࡴࡧࡤࠨᕑ"),
            bstack11111_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᕒ"): bstack11111_opy_ (u"࠭ࡈࡰࡱ࡮ࡣࡘࡺࡡࡳࡶࡢ࡙ࡵࡲ࡯ࡢࡦࠪᕓ"),
            bstack11111_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᕔ"): bstack11111_opy_ (u"ࠨࡊࡲࡳࡰࡥࡅ࡯ࡦࡢ࡙ࡵࡲ࡯ࡢࡦࠪᕕ"),
            bstack11111_opy_ (u"ࠩࡆࡆ࡙࡙ࡥࡴࡵ࡬ࡳࡳࡉࡲࡦࡣࡷࡩࡩ࠭ᕖ"): bstack11111_opy_ (u"ࠪࡇࡇ࡚࡟ࡖࡲ࡯ࡳࡦࡪࠧᕗ")
        }.get(bstack1ll11lll_opy_)
        if bstack1lll1llllll_opy_ == bstack11111_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪᕘ"):
            cls.bstack1llll11l1ll_opy_()
            cls.bstack1lllll1llll_opy_.add(bstack11lllll11l_opy_)
        elif bstack1lll1llllll_opy_ == bstack11111_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪᕙ"):
            cls.bstack1llll111ll1_opy_([bstack11lllll11l_opy_], bstack1lll1llllll_opy_)
    @classmethod
    @bstack1l111ll1ll_opy_(class_method=True)
    def bstack1llll111ll1_opy_(cls, bstack11lllll11l_opy_, bstack1lll1llllll_opy_=bstack11111_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬᕚ")):
        config = {
            bstack11111_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨᕛ"): cls.default_headers()
        }
        response = bstack1lll11l11l_opy_(bstack11111_opy_ (u"ࠨࡒࡒࡗ࡙࠭ᕜ"), cls.request_url(bstack1lll1llllll_opy_), bstack11lllll11l_opy_, config)
        bstack11ll111l1l_opy_ = response.json()
    @classmethod
    @bstack1l111ll1ll_opy_(class_method=True)
    def bstack1ll1l11l1l_opy_(cls, bstack1l1111l11l_opy_):
        bstack1lll1llll11_opy_ = []
        for log in bstack1l1111l11l_opy_:
            bstack1llll11ll1l_opy_ = {
                bstack11111_opy_ (u"ࠩ࡮࡭ࡳࡪࠧᕝ"): bstack11111_opy_ (u"ࠪࡘࡊ࡙ࡔࡠࡎࡒࡋࠬᕞ"),
                bstack11111_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᕟ"): log[bstack11111_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᕠ")],
                bstack11111_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᕡ"): log[bstack11111_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᕢ")],
                bstack11111_opy_ (u"ࠨࡪࡷࡸࡵࡥࡲࡦࡵࡳࡳࡳࡹࡥࠨᕣ"): {},
                bstack11111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᕤ"): log[bstack11111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᕥ")],
            }
            if bstack11111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᕦ") in log:
                bstack1llll11ll1l_opy_[bstack11111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᕧ")] = log[bstack11111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᕨ")]
            elif bstack11111_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᕩ") in log:
                bstack1llll11ll1l_opy_[bstack11111_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᕪ")] = log[bstack11111_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᕫ")]
            bstack1lll1llll11_opy_.append(bstack1llll11ll1l_opy_)
        cls.bstack1l11l11111_opy_({
            bstack11111_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᕬ"): bstack11111_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨᕭ"),
            bstack11111_opy_ (u"ࠬࡲ࡯ࡨࡵࠪᕮ"): bstack1lll1llll11_opy_
        })
    @classmethod
    @bstack1l111ll1ll_opy_(class_method=True)
    def bstack1llll11ll11_opy_(cls, steps):
        bstack1llll111lll_opy_ = []
        for step in steps:
            bstack1lll1lllll1_opy_ = {
                bstack11111_opy_ (u"࠭࡫ࡪࡰࡧࠫᕯ"): bstack11111_opy_ (u"ࠧࡕࡇࡖࡘࡤ࡙ࡔࡆࡒࠪᕰ"),
                bstack11111_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᕱ"): step[bstack11111_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᕲ")],
                bstack11111_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᕳ"): step[bstack11111_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᕴ")],
                bstack11111_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᕵ"): step[bstack11111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᕶ")],
                bstack11111_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩᕷ"): step[bstack11111_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪᕸ")]
            }
            if bstack11111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᕹ") in step:
                bstack1lll1lllll1_opy_[bstack11111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᕺ")] = step[bstack11111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᕻ")]
            elif bstack11111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᕼ") in step:
                bstack1lll1lllll1_opy_[bstack11111_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᕽ")] = step[bstack11111_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᕾ")]
            bstack1llll111lll_opy_.append(bstack1lll1lllll1_opy_)
        cls.bstack1l11l11111_opy_({
            bstack11111_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᕿ"): bstack11111_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ᖀ"),
            bstack11111_opy_ (u"ࠪࡰࡴ࡭ࡳࠨᖁ"): bstack1llll111lll_opy_
        })
    @classmethod
    @bstack1l111ll1ll_opy_(class_method=True)
    def bstack11l1llll_opy_(cls, screenshot):
        cls.bstack1l11l11111_opy_({
            bstack11111_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᖂ"): bstack11111_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩᖃ"),
            bstack11111_opy_ (u"࠭࡬ࡰࡩࡶࠫᖄ"): [{
                bstack11111_opy_ (u"ࠧ࡬࡫ࡱࡨࠬᖅ"): bstack11111_opy_ (u"ࠨࡖࡈࡗ࡙ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࠪᖆ"),
                bstack11111_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᖇ"): datetime.datetime.utcnow().isoformat() + bstack11111_opy_ (u"ࠪ࡞ࠬᖈ"),
                bstack11111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᖉ"): screenshot[bstack11111_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫᖊ")],
                bstack11111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᖋ"): screenshot[bstack11111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᖌ")]
            }]
        }, bstack1lll1llllll_opy_=bstack11111_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭ᖍ"))
    @classmethod
    @bstack1l111ll1ll_opy_(class_method=True)
    def bstack1ll11ll111_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1l11l11111_opy_({
            bstack11111_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ᖎ"): bstack11111_opy_ (u"ࠪࡇࡇ࡚ࡓࡦࡵࡶ࡭ࡴࡴࡃࡳࡧࡤࡸࡪࡪࠧᖏ"),
            bstack11111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭ᖐ"): {
                bstack11111_opy_ (u"ࠧࡻࡵࡪࡦࠥᖑ"): cls.current_test_uuid(),
                bstack11111_opy_ (u"ࠨࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠧᖒ"): cls.bstack1l1111llll_opy_(driver)
            }
        })
    @classmethod
    def on(cls):
        if os.environ.get(bstack11111_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡏ࡝ࡔࠨᖓ"), None) is None or os.environ[bstack11111_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡐࡗࡕࠩᖔ")] == bstack11111_opy_ (u"ࠤࡱࡹࡱࡲࠢᖕ"):
            return False
        return True
    @classmethod
    def bstack1llll1111l_opy_(cls):
        return bstack1ll1ll11_opy_(cls.bs_config.get(bstack11111_opy_ (u"ࠪࡸࡪࡹࡴࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧᖖ"), False))
    @staticmethod
    def request_url(url):
        return bstack11111_opy_ (u"ࠫࢀࢃ࠯ࡼࡿࠪᖗ").format(bstack1llll111l11_opy_, url)
    @staticmethod
    def default_headers():
        headers = {
            bstack11111_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫᖘ"): bstack11111_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩᖙ"),
            bstack11111_opy_ (u"࡙ࠧ࠯ࡅࡗ࡙ࡇࡃࡌ࠯ࡗࡉࡘ࡚ࡏࡑࡕࠪᖚ"): bstack11111_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᖛ")
        }
        if os.environ.get(bstack11111_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡊࡘࡖࠪᖜ"), None):
            headers[bstack11111_opy_ (u"ࠪࡅࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪᖝ")] = bstack11111_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࢀࢃࠧᖞ").format(os.environ[bstack11111_opy_ (u"ࠧࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙ࠨᖟ")])
        return headers
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack11111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪᖠ"), None)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack11111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᖡ"), None)
    @staticmethod
    def bstack1l111ll1l1_opy_():
        if getattr(threading.current_thread(), bstack11111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᖢ"), None):
            return {
                bstack11111_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᖣ"): bstack11111_opy_ (u"ࠪࡸࡪࡹࡴࠨᖤ"),
                bstack11111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᖥ"): getattr(threading.current_thread(), bstack11111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᖦ"), None)
            }
        if getattr(threading.current_thread(), bstack11111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᖧ"), None):
            return {
                bstack11111_opy_ (u"ࠧࡵࡻࡳࡩࠬᖨ"): bstack11111_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᖩ"),
                bstack11111_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᖪ"): getattr(threading.current_thread(), bstack11111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᖫ"), None)
            }
        return None
    @staticmethod
    def bstack1l1111llll_opy_(driver):
        return {
            bstack111llll1l1_opy_(): bstack11l1l11111_opy_(driver)
        }
    @staticmethod
    def bstack1lll1lll1ll_opy_(exception_info, report):
        return [{bstack11111_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᖬ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack11ll1lll11_opy_(typename):
        if bstack11111_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣᖭ") in typename:
            return bstack11111_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢᖮ")
        return bstack11111_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣᖯ")
    @staticmethod
    def bstack1llll111l1l_opy_(func):
        def wrap(*args, **kwargs):
            if bstack11ll1l1l1_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1l11111ll1_opy_(test, hook_name=None):
        bstack1llll11l1l1_opy_ = test.parent
        if hook_name in [bstack11111_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭ᖰ"), bstack11111_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪᖱ"), bstack11111_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩᖲ"), bstack11111_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭ᖳ")]:
            bstack1llll11l1l1_opy_ = test
        scope = []
        while bstack1llll11l1l1_opy_ is not None:
            scope.append(bstack1llll11l1l1_opy_.name)
            bstack1llll11l1l1_opy_ = bstack1llll11l1l1_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1llll1111ll_opy_(hook_type):
        if hook_type == bstack11111_opy_ (u"ࠧࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠥᖴ"):
            return bstack11111_opy_ (u"ࠨࡓࡦࡶࡸࡴࠥ࡮࡯ࡰ࡭ࠥᖵ")
        elif hook_type == bstack11111_opy_ (u"ࠢࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠦᖶ"):
            return bstack11111_opy_ (u"ࠣࡖࡨࡥࡷࡪ࡯ࡸࡰࠣ࡬ࡴࡵ࡫ࠣᖷ")
    @staticmethod
    def bstack1llll11l11l_opy_(bstack111l11ll_opy_):
        try:
            if not bstack11ll1l1l1_opy_.on():
                return bstack111l11ll_opy_
            if os.environ.get(bstack11111_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔࠢᖸ"), None) == bstack11111_opy_ (u"ࠥࡸࡷࡻࡥࠣᖹ"):
                tests = os.environ.get(bstack11111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࡡࡗࡉࡘ࡚ࡓࠣᖺ"), None)
                if tests is None or tests == bstack11111_opy_ (u"ࠧࡴࡵ࡭࡮ࠥᖻ"):
                    return bstack111l11ll_opy_
                bstack111l11ll_opy_ = tests.split(bstack11111_opy_ (u"࠭ࠬࠨᖼ"))
                return bstack111l11ll_opy_
        except Exception as exc:
            print(bstack11111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡲࡦࡴࡸࡲࠥ࡮ࡡ࡯ࡦ࡯ࡩࡷࡀࠠࠣᖽ"), str(exc))
        return bstack111l11ll_opy_
    @classmethod
    def bstack11llllllll_opy_(cls, event: str, bstack11lllll11l_opy_: bstack1l11l11lll_opy_):
        bstack11llll1l11_opy_ = {
            bstack11111_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᖾ"): event,
            bstack11lllll11l_opy_.bstack1l111l111l_opy_(): bstack11lllll11l_opy_.bstack1l11l111l1_opy_(event)
        }
        bstack11ll1l1l1_opy_.bstack1l11l11111_opy_(bstack11llll1l11_opy_)