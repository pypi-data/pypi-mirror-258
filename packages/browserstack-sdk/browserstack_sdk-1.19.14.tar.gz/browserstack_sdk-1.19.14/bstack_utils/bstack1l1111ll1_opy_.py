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
import requests
import logging
from urllib.parse import urlparse
from datetime import datetime
from bstack_utils.constants import bstack11ll11l11l_opy_ as bstack11ll1111ll_opy_
from bstack_utils.bstack1ll11l111_opy_ import bstack1ll11l111_opy_
from bstack_utils.helper import bstack11l1111l1_opy_, bstack1l1111l1_opy_, bstack11ll1l1ll1_opy_, bstack11ll111l11_opy_, bstack11lll1lll_opy_, get_host_info, bstack11l1lllll1_opy_, bstack1lll11l11l_opy_, bstack1l111ll1ll_opy_
from browserstack_sdk._version import __version__
logger = logging.getLogger(__name__)
@bstack1l111ll1ll_opy_(class_method=False)
def _11ll111111_opy_(driver, bstack1l1l1l1l1_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack11111_opy_ (u"࠭࡯ࡴࡡࡱࡥࡲ࡫ࠧษ"): caps.get(bstack11111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭ส"), None),
        bstack11111_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬห"): bstack1l1l1l1l1_opy_.get(bstack11111_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬฬ"), None),
        bstack11111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡳࡧ࡭ࡦࠩอ"): caps.get(bstack11111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩฮ"), None),
        bstack11111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧฯ"): caps.get(bstack11111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧะ"), None)
    }
  except Exception as error:
    logger.debug(bstack11111_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡦࡶࡦ࡬࡮ࡴࡧࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡨࡪࡺࡡࡪ࡮ࡶࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲࠡ࠼ࠣࠫั") + str(error))
  return response
def bstack1lllll11l1_opy_(config):
  return config.get(bstack11111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨา"), False) or any([p.get(bstack11111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩำ"), False) == True for p in config.get(bstack11111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ิ"), [])])
def bstack1l1l1111l_opy_(config, bstack11lll1ll_opy_):
  try:
    if not bstack1l1111l1_opy_(config):
      return False
    bstack11ll1l1l1l_opy_ = config.get(bstack11111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫี"), False)
    bstack11ll11l1ll_opy_ = config[bstack11111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨึ")][bstack11lll1ll_opy_].get(bstack11111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ื"), None)
    if bstack11ll11l1ll_opy_ != None:
      bstack11ll1l1l1l_opy_ = bstack11ll11l1ll_opy_
    bstack11ll111ll1_opy_ = os.getenv(bstack11111_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘุࠬ")) is not None and len(os.getenv(bstack11111_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍู࡛࡙࠭"))) > 0 and os.getenv(bstack11111_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜ฺ࡚ࠧ")) != bstack11111_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ฻")
    return bstack11ll1l1l1l_opy_ and bstack11ll111ll1_opy_
  except Exception as error:
    logger.debug(bstack11111_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡺࡪࡸࡩࡧࡻ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡪࡹࡳࡪࡱࡱࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲࠡ࠼ࠣࠫ฼") + str(error))
  return False
def bstack1l11l11ll_opy_(bstack11ll11lll1_opy_, test_tags):
  bstack11ll11lll1_opy_ = os.getenv(bstack11111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭฽"))
  if bstack11ll11lll1_opy_ is None:
    return True
  bstack11ll11lll1_opy_ = json.loads(bstack11ll11lll1_opy_)
  try:
    include_tags = bstack11ll11lll1_opy_[bstack11111_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫ฾")] if bstack11111_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬ฿") in bstack11ll11lll1_opy_ and isinstance(bstack11ll11lll1_opy_[bstack11111_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭เ")], list) else []
    exclude_tags = bstack11ll11lll1_opy_[bstack11111_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧแ")] if bstack11111_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨโ") in bstack11ll11lll1_opy_ and isinstance(bstack11ll11lll1_opy_[bstack11111_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩใ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack11111_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡺࡦࡲࡩࡥࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡪࡴࡸࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡥࡤࡲࡳ࡯࡮ࡨ࠰ࠣࡉࡷࡸ࡯ࡳࠢ࠽ࠤࠧไ") + str(error))
  return False
def bstack1llllllll_opy_(config, bstack11ll1l11ll_opy_, bstack11ll11l1l1_opy_, bstack11ll1111l1_opy_):
  bstack11l1llllll_opy_ = bstack11ll1l1ll1_opy_(config)
  bstack11ll1ll111_opy_ = bstack11ll111l11_opy_(config)
  if bstack11l1llllll_opy_ is None or bstack11ll1ll111_opy_ is None:
    logger.error(bstack11111_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡴࡸࡲࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࡍࡪࡵࡶ࡭ࡳ࡭ࠠࡢࡷࡷ࡬ࡪࡴࡴࡪࡥࡤࡸ࡮ࡵ࡮ࠡࡶࡲ࡯ࡪࡴࠧๅ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack11111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨๆ"), bstack11111_opy_ (u"ࠨࡽࢀࠫ็")))
    data = {
        bstack11111_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫่ࠧ"): config[bstack11111_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ้")],
        bstack11111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫๊ࠧ"): config.get(bstack11111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ๋"), os.path.basename(os.getcwd())),
        bstack11111_opy_ (u"࠭ࡳࡵࡣࡵࡸ࡙࡯࡭ࡦࠩ์"): bstack11l1111l1_opy_(),
        bstack11111_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬํ"): config.get(bstack11111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫ๎"), bstack11111_opy_ (u"ࠩࠪ๏")),
        bstack11111_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ๐"): {
            bstack11111_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡎࡢ࡯ࡨࠫ๑"): bstack11ll1l11ll_opy_,
            bstack11111_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ๒"): bstack11ll11l1l1_opy_,
            bstack11111_opy_ (u"࠭ࡳࡥ࡭࡙ࡩࡷࡹࡩࡰࡰࠪ๓"): __version__,
            bstack11111_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࠩ๔"): bstack11111_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ๕"),
            bstack11111_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ๖"): bstack11111_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࠬ๗"),
            bstack11111_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫ๘"): bstack11ll1111l1_opy_
        },
        bstack11111_opy_ (u"ࠬࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠧ๙"): settings,
        bstack11111_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࡃࡰࡰࡷࡶࡴࡲࠧ๚"): bstack11l1lllll1_opy_(),
        bstack11111_opy_ (u"ࠧࡤ࡫ࡌࡲ࡫ࡵࠧ๛"): bstack11lll1lll_opy_(),
        bstack11111_opy_ (u"ࠨࡪࡲࡷࡹࡏ࡮ࡧࡱࠪ๜"): get_host_info(),
        bstack11111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ๝"): bstack1l1111l1_opy_(config)
    }
    headers = {
        bstack11111_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩ๞"): bstack11111_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ๟"),
    }
    config = {
        bstack11111_opy_ (u"ࠬࡧࡵࡵࡪࠪ๠"): (bstack11l1llllll_opy_, bstack11ll1ll111_opy_),
        bstack11111_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧ๡"): headers
    }
    response = bstack1lll11l11l_opy_(bstack11111_opy_ (u"ࠧࡑࡑࡖࡘࠬ๢"), bstack11ll1111ll_opy_ + bstack11111_opy_ (u"ࠨ࠱ࡹ࠶࠴ࡺࡥࡴࡶࡢࡶࡺࡴࡳࠨ๣"), data, config)
    bstack11ll111l1l_opy_ = response.json()
    if bstack11ll111l1l_opy_[bstack11111_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪ๤")]:
      parsed = json.loads(os.getenv(bstack11111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ๥"), bstack11111_opy_ (u"ࠫࢀࢃࠧ๦")))
      parsed[bstack11111_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭๧")] = bstack11ll111l1l_opy_[bstack11111_opy_ (u"࠭ࡤࡢࡶࡤࠫ๨")][bstack11111_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ๩")]
      os.environ[bstack11111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩ๪")] = json.dumps(parsed)
      bstack1ll11l111_opy_.bstack11ll1l111l_opy_(bstack11ll111l1l_opy_[bstack11111_opy_ (u"ࠩࡧࡥࡹࡧࠧ๫")][bstack11111_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫ๬")])
      bstack1ll11l111_opy_.bstack11ll11ll1l_opy_(bstack11ll111l1l_opy_[bstack11111_opy_ (u"ࠫࡩࡧࡴࡢࠩ๭")][bstack11111_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧ๮")])
      bstack1ll11l111_opy_.store()
      return bstack11ll111l1l_opy_[bstack11111_opy_ (u"࠭ࡤࡢࡶࡤࠫ๯")][bstack11111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡔࡰ࡭ࡨࡲࠬ๰")], bstack11ll111l1l_opy_[bstack11111_opy_ (u"ࠨࡦࡤࡸࡦ࠭๱")][bstack11111_opy_ (u"ࠩ࡬ࡨࠬ๲")]
    else:
      logger.error(bstack11111_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠼ࠣࠫ๳") + bstack11ll111l1l_opy_[bstack11111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ๴")])
      if bstack11ll111l1l_opy_[bstack11111_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭๵")] == bstack11111_opy_ (u"࠭ࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡱࡣࡶࡷࡪࡪ࠮ࠨ๶"):
        for bstack11ll11111l_opy_ in bstack11ll111l1l_opy_[bstack11111_opy_ (u"ࠧࡦࡴࡵࡳࡷࡹࠧ๷")]:
          logger.error(bstack11ll11111l_opy_[bstack11111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ๸")])
      return None, None
  except Exception as error:
    logger.error(bstack11111_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡷࡻ࡮ࠡࡨࡲࡶࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠻ࠢࠥ๹") +  str(error))
    return None, None
def bstack1lll111111_opy_():
  if os.getenv(bstack11111_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ๺")) is None:
    return {
        bstack11111_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ๻"): bstack11111_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ๼"),
        bstack11111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ๽"): bstack11111_opy_ (u"ࠧࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡪࡤࡨࠥ࡬ࡡࡪ࡮ࡨࡨ࠳࠭๾")
    }
  data = {bstack11111_opy_ (u"ࠨࡧࡱࡨ࡙࡯࡭ࡦࠩ๿"): bstack11l1111l1_opy_()}
  headers = {
      bstack11111_opy_ (u"ࠩࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩ຀"): bstack11111_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࠫກ") + os.getenv(bstack11111_opy_ (u"ࠦࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠤຂ")),
      bstack11111_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫ຃"): bstack11111_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩຄ")
  }
  response = bstack1lll11l11l_opy_(bstack11111_opy_ (u"ࠧࡑࡗࡗࠫ຅"), bstack11ll1111ll_opy_ + bstack11111_opy_ (u"ࠨ࠱ࡷࡩࡸࡺ࡟ࡳࡷࡱࡷ࠴ࡹࡴࡰࡲࠪຆ"), data, { bstack11111_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪງ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack11111_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡔࡦࡵࡷࠤࡗࡻ࡮ࠡ࡯ࡤࡶࡰ࡫ࡤࠡࡣࡶࠤࡨࡵ࡭ࡱ࡮ࡨࡸࡪࡪࠠࡢࡶࠣࠦຈ") + datetime.utcnow().isoformat() + bstack11111_opy_ (u"ࠫ࡟࠭ຉ"))
      return {bstack11111_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬຊ"): bstack11111_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧ຋"), bstack11111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨຌ"): bstack11111_opy_ (u"ࠨࠩຍ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack11111_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡯࡯࡯ࠢࡲࡪࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡖࡨࡷࡹࠦࡒࡶࡰ࠽ࠤࠧຎ") + str(error))
    return {
        bstack11111_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪຏ"): bstack11111_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪຐ"),
        bstack11111_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ຑ"): str(error)
    }
def bstack11lll1l1l_opy_(caps, options):
  try:
    bstack11ll11l111_opy_ = caps.get(bstack11111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧຒ"), {}).get(bstack11111_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫຓ"), caps.get(bstack11111_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨດ"), bstack11111_opy_ (u"ࠩࠪຕ")))
    if bstack11ll11l111_opy_:
      logger.warn(bstack11111_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡈࡪࡹ࡫ࡵࡱࡳࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢຖ"))
      return False
    browser = caps.get(bstack11111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩທ"), bstack11111_opy_ (u"ࠬ࠭ຘ")).lower()
    if browser != bstack11111_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ນ"):
      logger.warn(bstack11111_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡄࡪࡵࡳࡲ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴ࠰ࠥບ"))
      return False
    browser_version = caps.get(bstack11111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩປ"), caps.get(bstack11111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫຜ")))
    if browser_version and browser_version != bstack11111_opy_ (u"ࠪࡰࡦࡺࡥࡴࡶࠪຝ") and int(browser_version.split(bstack11111_opy_ (u"ࠫ࠳࠭ພ"))[0]) <= 94:
      logger.warn(bstack11111_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡉࡨࡳࡱࡰࡩࠥࡨࡲࡰࡹࡶࡩࡷࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡨࡴࡨࡥࡹ࡫ࡲࠡࡶ࡫ࡥࡳࠦ࠹࠵࠰ࠥຟ"))
      return False
    if not options is None:
      bstack11ll11llll_opy_ = options.to_capabilities().get(bstack11111_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫຠ"), {})
      if bstack11111_opy_ (u"ࠧ࠮࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶࠫມ") in bstack11ll11llll_opy_.get(bstack11111_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ຢ"), []):
        logger.warn(bstack11111_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡳࡵࡴࠡࡴࡸࡲࠥࡵ࡮ࠡ࡮ࡨ࡫ࡦࡩࡹࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠢࡖࡻ࡮ࡺࡣࡩࠢࡷࡳࠥࡴࡥࡸࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦࠢࡲࡶࠥࡧࡶࡰ࡫ࡧࠤࡺࡹࡩ࡯ࡩࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠦຣ"))
        return False
    return True
  except Exception as error:
    logger.debug(bstack11111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡹࡥࡱ࡯ࡤࡢࡶࡨࠤࡦ࠷࠱ࡺࠢࡶࡹࡵࡶ࡯ࡳࡶࠣ࠾ࠧ຤") + str(error))
    return False
def set_capabilities(caps, config):
  try:
    bstack11l1llll1l_opy_ = config.get(bstack11111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫລ"), {})
    bstack11l1llll1l_opy_[bstack11111_opy_ (u"ࠬࡧࡵࡵࡪࡗࡳࡰ࡫࡮ࠨ຦")] = os.getenv(bstack11111_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫວ"))
    bstack11ll11ll11_opy_ = json.loads(os.getenv(bstack11111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨຨ"), bstack11111_opy_ (u"ࠨࡽࢀࠫຩ"))).get(bstack11111_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪສ"))
    caps[bstack11111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪຫ")] = True
    if bstack11111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬຬ") in caps:
      caps[bstack11111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ອ")][bstack11111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ຮ")] = bstack11l1llll1l_opy_
      caps[bstack11111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨຯ")][bstack11111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨະ")][bstack11111_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪັ")] = bstack11ll11ll11_opy_
    else:
      caps[bstack11111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩາ")] = bstack11l1llll1l_opy_
      caps[bstack11111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪຳ")][bstack11111_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ິ")] = bstack11ll11ll11_opy_
  except Exception as error:
    logger.debug(bstack11111_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷ࠳ࠦࡅࡳࡴࡲࡶ࠿ࠦࠢີ") +  str(error))
def bstack1ll1l11111_opy_(driver, bstack11ll1l1111_opy_):
  try:
    setattr(driver, bstack11111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧຶ"), True)
    session = driver.session_id
    if session:
      bstack11ll1l11l1_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11ll1l11l1_opy_ = False
      bstack11ll1l11l1_opy_ = url.scheme in [bstack11111_opy_ (u"ࠣࡪࡷࡸࡵࠨື"), bstack11111_opy_ (u"ࠤ࡫ࡸࡹࡶࡳຸࠣ")]
      if bstack11ll1l11l1_opy_:
        if bstack11ll1l1111_opy_:
          logger.info(bstack11111_opy_ (u"ࠥࡗࡪࡺࡵࡱࠢࡩࡳࡷࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡩࡣࡶࠤࡸࡺࡡࡳࡶࡨࡨ࠳ࠦࡁࡶࡶࡲࡱࡦࡺࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡨࡥࡨ࡫ࡱࠤࡲࡵ࡭ࡦࡰࡷࡥࡷ࡯࡬ࡺ࠰ູࠥ"))
      return bstack11ll1l1111_opy_
  except Exception as e:
    logger.error(bstack11111_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡧࡦࡴࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩ࠿຺ࠦࠢ") + str(e))
    return False
def bstack11llll1l1_opy_(driver, class_name, name, module_name, path, bstack1l1l1l1l1_opy_):
  try:
    bstack11lll11ll1_opy_ = [class_name] if not class_name is None else []
    bstack11ll1l1lll_opy_ = {
        bstack11111_opy_ (u"ࠧࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠥົ"): True,
        bstack11111_opy_ (u"ࠨࡴࡦࡵࡷࡈࡪࡺࡡࡪ࡮ࡶࠦຼ"): {
            bstack11111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧຽ"): name,
            bstack11111_opy_ (u"ࠣࡶࡨࡷࡹࡘࡵ࡯ࡋࡧࠦ຾"): os.environ.get(bstack11111_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡘࡊ࡙ࡔࡠࡔࡘࡒࡤࡏࡄࠨ຿")),
            bstack11111_opy_ (u"ࠥࡪ࡮ࡲࡥࡑࡣࡷ࡬ࠧເ"): str(path),
            bstack11111_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࡏ࡭ࡸࡺࠢແ"): [module_name, *bstack11lll11ll1_opy_, name],
        },
        bstack11111_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࠢໂ"): _11ll111111_opy_(driver, bstack1l1l1l1l1_opy_)
    }
    logger.debug(bstack11111_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡵࡤࡺ࡮ࡴࡧࠡࡴࡨࡷࡺࡲࡴࡴࠩໃ"))
    logger.debug(driver.execute_async_script(bstack1ll11l111_opy_.perform_scan, {bstack11111_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪࠢໄ"): name}))
    logger.debug(driver.execute_async_script(bstack1ll11l111_opy_.bstack11ll111lll_opy_, bstack11ll1l1lll_opy_))
    logger.info(bstack11111_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠦ໅"))
  except Exception as bstack11ll1l1l11_opy_:
    logger.error(bstack11111_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡧࡴࡻ࡬ࡥࠢࡱࡳࡹࠦࡢࡦࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦ࠼ࠣࠦໆ") + str(path) + bstack11111_opy_ (u"ࠥࠤࡊࡸࡲࡰࡴࠣ࠾ࠧ໇") + str(bstack11ll1l1l11_opy_))