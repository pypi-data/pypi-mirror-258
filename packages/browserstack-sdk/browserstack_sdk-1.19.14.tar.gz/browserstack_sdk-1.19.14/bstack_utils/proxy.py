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
from urllib.parse import urlparse
from bstack_utils.messages import bstack111l1l11ll_opy_
def bstack1111111l11_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack111111l11l_opy_(bstack11111111ll_opy_, bstack1111111ll1_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack11111111ll_opy_):
        with open(bstack11111111ll_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1111111l11_opy_(bstack11111111ll_opy_):
        pac = get_pac(url=bstack11111111ll_opy_)
    else:
        raise Exception(bstack11111_opy_ (u"ࠧࡑࡣࡦࠤ࡫࡯࡬ࡦࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡪࡾࡩࡴࡶ࠽ࠤࢀࢃࠧᐒ").format(bstack11111111ll_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack11111_opy_ (u"ࠣ࠺࠱࠼࠳࠾࠮࠹ࠤᐓ"), 80))
        bstack111111l111_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack111111l111_opy_ = bstack11111_opy_ (u"ࠩ࠳࠲࠵࠴࠰࠯࠲ࠪᐔ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1111111ll1_opy_, bstack111111l111_opy_)
    return proxy_url
def bstack1lll111ll_opy_(config):
    return bstack11111_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ᐕ") in config or bstack11111_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨᐖ") in config
def bstack1lll11l1ll_opy_(config):
    if not bstack1lll111ll_opy_(config):
        return
    if config.get(bstack11111_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᐗ")):
        return config.get(bstack11111_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᐘ"))
    if config.get(bstack11111_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᐙ")):
        return config.get(bstack11111_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬᐚ"))
def bstack1lll1ll1l1_opy_(config, bstack1111111ll1_opy_):
    proxy = bstack1lll11l1ll_opy_(config)
    proxies = {}
    if config.get(bstack11111_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬᐛ")) or config.get(bstack11111_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧᐜ")):
        if proxy.endswith(bstack11111_opy_ (u"ࠫ࠳ࡶࡡࡤࠩᐝ")):
            proxies = bstack1ll1lll1ll_opy_(proxy, bstack1111111ll1_opy_)
        else:
            proxies = {
                bstack11111_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᐞ"): proxy
            }
    return proxies
def bstack1ll1lll1ll_opy_(bstack11111111ll_opy_, bstack1111111ll1_opy_):
    proxies = {}
    global bstack1111111l1l_opy_
    if bstack11111_opy_ (u"࠭ࡐࡂࡅࡢࡔࡗࡕࡘ࡚ࠩᐟ") in globals():
        return bstack1111111l1l_opy_
    try:
        proxy = bstack111111l11l_opy_(bstack11111111ll_opy_, bstack1111111ll1_opy_)
        if bstack11111_opy_ (u"ࠢࡅࡋࡕࡉࡈ࡚ࠢᐠ") in proxy:
            proxies = {}
        elif bstack11111_opy_ (u"ࠣࡊࡗࡘࡕࠨᐡ") in proxy or bstack11111_opy_ (u"ࠤࡋࡘ࡙ࡖࡓࠣᐢ") in proxy or bstack11111_opy_ (u"ࠥࡗࡔࡉࡋࡔࠤᐣ") in proxy:
            bstack1111111lll_opy_ = proxy.split(bstack11111_opy_ (u"ࠦࠥࠨᐤ"))
            if bstack11111_opy_ (u"ࠧࡀ࠯࠰ࠤᐥ") in bstack11111_opy_ (u"ࠨࠢᐦ").join(bstack1111111lll_opy_[1:]):
                proxies = {
                    bstack11111_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ᐧ"): bstack11111_opy_ (u"ࠣࠤᐨ").join(bstack1111111lll_opy_[1:])
                }
            else:
                proxies = {
                    bstack11111_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨᐩ"): str(bstack1111111lll_opy_[0]).lower() + bstack11111_opy_ (u"ࠥ࠾࠴࠵ࠢᐪ") + bstack11111_opy_ (u"ࠦࠧᐫ").join(bstack1111111lll_opy_[1:])
                }
        elif bstack11111_opy_ (u"ࠧࡖࡒࡐ࡚࡜ࠦᐬ") in proxy:
            bstack1111111lll_opy_ = proxy.split(bstack11111_opy_ (u"ࠨࠠࠣᐭ"))
            if bstack11111_opy_ (u"ࠢ࠻࠱࠲ࠦᐮ") in bstack11111_opy_ (u"ࠣࠤᐯ").join(bstack1111111lll_opy_[1:]):
                proxies = {
                    bstack11111_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨᐰ"): bstack11111_opy_ (u"ࠥࠦᐱ").join(bstack1111111lll_opy_[1:])
                }
            else:
                proxies = {
                    bstack11111_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪᐲ"): bstack11111_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨᐳ") + bstack11111_opy_ (u"ࠨࠢᐴ").join(bstack1111111lll_opy_[1:])
                }
        else:
            proxies = {
                bstack11111_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ᐵ"): proxy
            }
    except Exception as e:
        print(bstack11111_opy_ (u"ࠣࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠧᐶ"), bstack111l1l11ll_opy_.format(bstack11111111ll_opy_, str(e)))
    bstack1111111l1l_opy_ = proxies
    return proxies