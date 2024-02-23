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
import re
from bstack_utils.bstack111lllll1_opy_ import bstack1llllllllll_opy_
def bstack1llllll1ll1_opy_(fixture_name):
    if fixture_name.startswith(bstack11111_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᐷ")):
        return bstack11111_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫᐸ")
    elif fixture_name.startswith(bstack11111_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᐹ")):
        return bstack11111_opy_ (u"ࠬࡹࡥࡵࡷࡳ࠱ࡲࡵࡤࡶ࡮ࡨࠫᐺ")
    elif fixture_name.startswith(bstack11111_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᐻ")):
        return bstack11111_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫᐼ")
    elif fixture_name.startswith(bstack11111_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᐽ")):
        return bstack11111_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱ࡲࡵࡤࡶ࡮ࡨࠫᐾ")
def bstack1llllllll11_opy_(fixture_name):
    return bool(re.match(bstack11111_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟ࠩࡨࡸࡲࡨࡺࡩࡰࡰࡿࡱࡴࡪࡵ࡭ࡧࠬࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨᐿ"), fixture_name))
def bstack1llllll1l1l_opy_(fixture_name):
    return bool(re.match(bstack11111_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࡡ࠱࠮ࠬᑀ"), fixture_name))
def bstack111111111l_opy_(fixture_name):
    return bool(re.match(bstack11111_opy_ (u"ࠬࡤ࡟ࡹࡷࡱ࡭ࡹࡥࠨࡴࡧࡷࡹࡵࢂࡴࡦࡣࡵࡨࡴࡽ࡮ࠪࡡࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࡡ࠱࠮ࠬᑁ"), fixture_name))
def bstack1lllllll1ll_opy_(fixture_name):
    if fixture_name.startswith(bstack11111_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᑂ")):
        return bstack11111_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᑃ"), bstack11111_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭ᑄ")
    elif fixture_name.startswith(bstack11111_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᑅ")):
        return bstack11111_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡰࡳࡩࡻ࡬ࡦࠩᑆ"), bstack11111_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨᑇ")
    elif fixture_name.startswith(bstack11111_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᑈ")):
        return bstack11111_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪᑉ"), bstack11111_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫᑊ")
    elif fixture_name.startswith(bstack11111_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᑋ")):
        return bstack11111_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱ࡲࡵࡤࡶ࡮ࡨࠫᑌ"), bstack11111_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭ᑍ")
    return None, None
def bstack1lllllll111_opy_(hook_name):
    if hook_name in [bstack11111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪᑎ"), bstack11111_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧᑏ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1llllll1lll_opy_(hook_name):
    if hook_name in [bstack11111_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᑐ"), bstack11111_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ᑑ")]:
        return bstack11111_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭ᑒ")
    elif hook_name in [bstack11111_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨᑓ"), bstack11111_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨᑔ")]:
        return bstack11111_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨᑕ")
    elif hook_name in [bstack11111_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩᑖ"), bstack11111_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨᑗ")]:
        return bstack11111_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫᑘ")
    elif hook_name in [bstack11111_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪᑙ"), bstack11111_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪᑚ")]:
        return bstack11111_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭ᑛ")
    return hook_name
def bstack1111111111_opy_(node, scenario):
    if hasattr(node, bstack11111_opy_ (u"ࠫࡨࡧ࡬࡭ࡵࡳࡩࡨ࠭ᑜ")):
        parts = node.nodeid.rsplit(bstack11111_opy_ (u"ࠧࡡࠢᑝ"))
        params = parts[-1]
        return bstack11111_opy_ (u"ࠨࡻࡾࠢ࡞ࡿࢂࠨᑞ").format(scenario.name, params)
    return scenario.name
def bstack1lllllll1l1_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack11111_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩᑟ")):
            examples = list(node.callspec.params[bstack11111_opy_ (u"ࠨࡡࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡥࡹࡣࡰࡴࡱ࡫ࠧᑠ")].values())
        return examples
    except:
        return []
def bstack1llllllll1l_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack11111111l1_opy_(report):
    try:
        status = bstack11111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᑡ")
        if report.passed or (report.failed and hasattr(report, bstack11111_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧᑢ"))):
            status = bstack11111_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᑣ")
        elif report.skipped:
            status = bstack11111_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ᑤ")
        bstack1llllllllll_opy_(status)
    except:
        pass
def bstack1llllllll1_opy_(status):
    try:
        bstack1lllllll11l_opy_ = bstack11111_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᑥ")
        if status == bstack11111_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᑦ"):
            bstack1lllllll11l_opy_ = bstack11111_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᑧ")
        elif status == bstack11111_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᑨ"):
            bstack1lllllll11l_opy_ = bstack11111_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᑩ")
        bstack1llllllllll_opy_(bstack1lllllll11l_opy_)
    except:
        pass
def bstack1lllllllll1_opy_(item=None, report=None, summary=None, extra=None):
    return