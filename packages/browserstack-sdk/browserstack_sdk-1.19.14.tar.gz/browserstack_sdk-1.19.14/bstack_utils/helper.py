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
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
from urllib.parse import urlparse
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import bstack11l1l1l11l_opy_, bstack1ll1lll11_opy_, bstack1ll1ll11l_opy_, bstack1l1llllll_opy_
from bstack_utils.messages import bstack1lllllll1_opy_, bstack1l11l1ll1_opy_
from bstack_utils.proxy import bstack1lll1ll1l1_opy_, bstack1lll11l1ll_opy_
bstack11111111_opy_ = Config.bstack111l111l_opy_()
def bstack11ll1l1ll1_opy_(config):
    return config[bstack11111_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪᅺ")]
def bstack11ll111l11_opy_(config):
    return config[bstack11111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬᅻ")]
def bstack1l11llll1_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack11l111l1l1_opy_(obj):
    values = []
    bstack11l11ll1l1_opy_ = re.compile(bstack11111_opy_ (u"ࡵࠦࡣࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࡟ࡨ࠰ࠪࠢᅼ"), re.I)
    for key in obj.keys():
        if bstack11l11ll1l1_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11l11111l1_opy_(config):
    tags = []
    tags.extend(bstack11l111l1l1_opy_(os.environ))
    tags.extend(bstack11l111l1l1_opy_(config))
    return tags
def bstack11l1111l1l_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack111lll11l1_opy_(bstack111lll1l1l_opy_):
    if not bstack111lll1l1l_opy_:
        return bstack11111_opy_ (u"ࠫࠬᅽ")
    return bstack11111_opy_ (u"ࠧࢁࡽࠡࠪࡾࢁ࠮ࠨᅾ").format(bstack111lll1l1l_opy_.name, bstack111lll1l1l_opy_.email)
def bstack11l1lllll1_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack111lll1ll1_opy_ = repo.common_dir
        info = {
            bstack11111_opy_ (u"ࠨࡳࡩࡣࠥᅿ"): repo.head.commit.hexsha,
            bstack11111_opy_ (u"ࠢࡴࡪࡲࡶࡹࡥࡳࡩࡣࠥᆀ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack11111_opy_ (u"ࠣࡤࡵࡥࡳࡩࡨࠣᆁ"): repo.active_branch.name,
            bstack11111_opy_ (u"ࠤࡷࡥ࡬ࠨᆂ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack11111_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡷࡩࡷࠨᆃ"): bstack111lll11l1_opy_(repo.head.commit.committer),
            bstack11111_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡸࡪࡸ࡟ࡥࡣࡷࡩࠧᆄ"): repo.head.commit.committed_datetime.isoformat(),
            bstack11111_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࠧᆅ"): bstack111lll11l1_opy_(repo.head.commit.author),
            bstack11111_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࡥࡤࡢࡶࡨࠦᆆ"): repo.head.commit.authored_datetime.isoformat(),
            bstack11111_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠣᆇ"): repo.head.commit.message,
            bstack11111_opy_ (u"ࠣࡴࡲࡳࡹࠨᆈ"): repo.git.rev_parse(bstack11111_opy_ (u"ࠤ࠰࠱ࡸ࡮࡯ࡸ࠯ࡷࡳࡵࡲࡥࡷࡧ࡯ࠦᆉ")),
            bstack11111_opy_ (u"ࠥࡧࡴࡳ࡭ࡰࡰࡢ࡫࡮ࡺ࡟ࡥ࡫ࡵࠦᆊ"): bstack111lll1ll1_opy_,
            bstack11111_opy_ (u"ࠦࡼࡵࡲ࡬ࡶࡵࡩࡪࡥࡧࡪࡶࡢࡨ࡮ࡸࠢᆋ"): subprocess.check_output([bstack11111_opy_ (u"ࠧ࡭ࡩࡵࠤᆌ"), bstack11111_opy_ (u"ࠨࡲࡦࡸ࠰ࡴࡦࡸࡳࡦࠤᆍ"), bstack11111_opy_ (u"ࠢ࠮࠯ࡪ࡭ࡹ࠳ࡣࡰ࡯ࡰࡳࡳ࠳ࡤࡪࡴࠥᆎ")]).strip().decode(
                bstack11111_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧᆏ")),
            bstack11111_opy_ (u"ࠤ࡯ࡥࡸࡺ࡟ࡵࡣࡪࠦᆐ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack11111_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡶࡣࡸ࡯࡮ࡤࡧࡢࡰࡦࡹࡴࡠࡶࡤ࡫ࠧᆑ"): repo.git.rev_list(
                bstack11111_opy_ (u"ࠦࢀࢃ࠮࠯ࡽࢀࠦᆒ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11l11ll1ll_opy_ = []
        for remote in remotes:
            bstack111llll1ll_opy_ = {
                bstack11111_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᆓ"): remote.name,
                bstack11111_opy_ (u"ࠨࡵࡳ࡮ࠥᆔ"): remote.url,
            }
            bstack11l11ll1ll_opy_.append(bstack111llll1ll_opy_)
        return {
            bstack11111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᆕ"): bstack11111_opy_ (u"ࠣࡩ࡬ࡸࠧᆖ"),
            **info,
            bstack11111_opy_ (u"ࠤࡵࡩࡲࡵࡴࡦࡵࠥᆗ"): bstack11l11ll1ll_opy_
        }
    except Exception as err:
        print(bstack11111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡳࡵࡻ࡬ࡢࡶ࡬ࡲ࡬ࠦࡇࡪࡶࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨᆘ").format(err))
        return {}
def bstack11lll1lll_opy_():
    env = os.environ
    if (bstack11111_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤ࡛ࡒࡍࠤᆙ") in env and len(env[bstack11111_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡕࡓࡎࠥᆚ")]) > 0) or (
            bstack11111_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡉࡑࡐࡉࠧᆛ") in env and len(env[bstack11111_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡊࡒࡑࡊࠨᆜ")]) > 0):
        return {
            bstack11111_opy_ (u"ࠣࡰࡤࡱࡪࠨᆝ"): bstack11111_opy_ (u"ࠤࡍࡩࡳࡱࡩ࡯ࡵࠥᆞ"),
            bstack11111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᆟ"): env.get(bstack11111_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢᆠ")),
            bstack11111_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᆡ"): env.get(bstack11111_opy_ (u"ࠨࡊࡐࡄࡢࡒࡆࡓࡅࠣᆢ")),
            bstack11111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᆣ"): env.get(bstack11111_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᆤ"))
        }
    if env.get(bstack11111_opy_ (u"ࠤࡆࡍࠧᆥ")) == bstack11111_opy_ (u"ࠥࡸࡷࡻࡥࠣᆦ") and bstack1ll1ll11_opy_(env.get(bstack11111_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡇࡎࠨᆧ"))):
        return {
            bstack11111_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᆨ"): bstack11111_opy_ (u"ࠨࡃࡪࡴࡦࡰࡪࡉࡉࠣᆩ"),
            bstack11111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᆪ"): env.get(bstack11111_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦᆫ")),
            bstack11111_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᆬ"): env.get(bstack11111_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡢࡎࡔࡈࠢᆭ")),
            bstack11111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᆮ"): env.get(bstack11111_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࠣᆯ"))
        }
    if env.get(bstack11111_opy_ (u"ࠨࡃࡊࠤᆰ")) == bstack11111_opy_ (u"ࠢࡵࡴࡸࡩࠧᆱ") and bstack1ll1ll11_opy_(env.get(bstack11111_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࠣᆲ"))):
        return {
            bstack11111_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᆳ"): bstack11111_opy_ (u"ࠥࡘࡷࡧࡶࡪࡵࠣࡇࡎࠨᆴ"),
            bstack11111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᆵ"): env.get(bstack11111_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡈࡕࡊࡎࡇࡣ࡜ࡋࡂࡠࡗࡕࡐࠧᆶ")),
            bstack11111_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᆷ"): env.get(bstack11111_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᆸ")),
            bstack11111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᆹ"): env.get(bstack11111_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᆺ"))
        }
    if env.get(bstack11111_opy_ (u"ࠥࡇࡎࠨᆻ")) == bstack11111_opy_ (u"ࠦࡹࡸࡵࡦࠤᆼ") and env.get(bstack11111_opy_ (u"ࠧࡉࡉࡠࡐࡄࡑࡊࠨᆽ")) == bstack11111_opy_ (u"ࠨࡣࡰࡦࡨࡷ࡭࡯ࡰࠣᆾ"):
        return {
            bstack11111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᆿ"): bstack11111_opy_ (u"ࠣࡅࡲࡨࡪࡹࡨࡪࡲࠥᇀ"),
            bstack11111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᇁ"): None,
            bstack11111_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᇂ"): None,
            bstack11111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᇃ"): None
        }
    if env.get(bstack11111_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡄࡕࡅࡓࡉࡈࠣᇄ")) and env.get(bstack11111_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡆࡓࡒࡓࡉࡕࠤᇅ")):
        return {
            bstack11111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᇆ"): bstack11111_opy_ (u"ࠣࡄ࡬ࡸࡧࡻࡣ࡬ࡧࡷࠦᇇ"),
            bstack11111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᇈ"): env.get(bstack11111_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡇࡊࡖࡢࡌ࡙࡚ࡐࡠࡑࡕࡍࡌࡏࡎࠣᇉ")),
            bstack11111_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᇊ"): None,
            bstack11111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᇋ"): env.get(bstack11111_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᇌ"))
        }
    if env.get(bstack11111_opy_ (u"ࠢࡄࡋࠥᇍ")) == bstack11111_opy_ (u"ࠣࡶࡵࡹࡪࠨᇎ") and bstack1ll1ll11_opy_(env.get(bstack11111_opy_ (u"ࠤࡇࡖࡔࡔࡅࠣᇏ"))):
        return {
            bstack11111_opy_ (u"ࠥࡲࡦࡳࡥࠣᇐ"): bstack11111_opy_ (u"ࠦࡉࡸ࡯࡯ࡧࠥᇑ"),
            bstack11111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᇒ"): env.get(bstack11111_opy_ (u"ࠨࡄࡓࡑࡑࡉࡤࡈࡕࡊࡎࡇࡣࡑࡏࡎࡌࠤᇓ")),
            bstack11111_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᇔ"): None,
            bstack11111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᇕ"): env.get(bstack11111_opy_ (u"ࠤࡇࡖࡔࡔࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᇖ"))
        }
    if env.get(bstack11111_opy_ (u"ࠥࡇࡎࠨᇗ")) == bstack11111_opy_ (u"ࠦࡹࡸࡵࡦࠤᇘ") and bstack1ll1ll11_opy_(env.get(bstack11111_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࠣᇙ"))):
        return {
            bstack11111_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᇚ"): bstack11111_opy_ (u"ࠢࡔࡧࡰࡥࡵ࡮࡯ࡳࡧࠥᇛ"),
            bstack11111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᇜ"): env.get(bstack11111_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡕࡒࡈࡃࡑࡍ࡟ࡇࡔࡊࡑࡑࡣ࡚ࡘࡌࠣᇝ")),
            bstack11111_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᇞ"): env.get(bstack11111_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᇟ")),
            bstack11111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᇠ"): env.get(bstack11111_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡍࡓࡇࡥࡉࡅࠤᇡ"))
        }
    if env.get(bstack11111_opy_ (u"ࠢࡄࡋࠥᇢ")) == bstack11111_opy_ (u"ࠣࡶࡵࡹࡪࠨᇣ") and bstack1ll1ll11_opy_(env.get(bstack11111_opy_ (u"ࠤࡊࡍ࡙ࡒࡁࡃࡡࡆࡍࠧᇤ"))):
        return {
            bstack11111_opy_ (u"ࠥࡲࡦࡳࡥࠣᇥ"): bstack11111_opy_ (u"ࠦࡌ࡯ࡴࡍࡣࡥࠦᇦ"),
            bstack11111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᇧ"): env.get(bstack11111_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡕࡓࡎࠥᇨ")),
            bstack11111_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᇩ"): env.get(bstack11111_opy_ (u"ࠣࡅࡌࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᇪ")),
            bstack11111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᇫ"): env.get(bstack11111_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢࡍࡉࠨᇬ"))
        }
    if env.get(bstack11111_opy_ (u"ࠦࡈࡏࠢᇭ")) == bstack11111_opy_ (u"ࠧࡺࡲࡶࡧࠥᇮ") and bstack1ll1ll11_opy_(env.get(bstack11111_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࠤᇯ"))):
        return {
            bstack11111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᇰ"): bstack11111_opy_ (u"ࠣࡄࡸ࡭ࡱࡪ࡫ࡪࡶࡨࠦᇱ"),
            bstack11111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᇲ"): env.get(bstack11111_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᇳ")),
            bstack11111_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᇴ"): env.get(bstack11111_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡎࡄࡆࡊࡒࠢᇵ")) or env.get(bstack11111_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡓࡇࡍࡆࠤᇶ")),
            bstack11111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᇷ"): env.get(bstack11111_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᇸ"))
        }
    if bstack1ll1ll11_opy_(env.get(bstack11111_opy_ (u"ࠤࡗࡊࡤࡈࡕࡊࡎࡇࠦᇹ"))):
        return {
            bstack11111_opy_ (u"ࠥࡲࡦࡳࡥࠣᇺ"): bstack11111_opy_ (u"࡛ࠦ࡯ࡳࡶࡣ࡯ࠤࡘࡺࡵࡥ࡫ࡲࠤ࡙࡫ࡡ࡮ࠢࡖࡩࡷࡼࡩࡤࡧࡶࠦᇻ"),
            bstack11111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᇼ"): bstack11111_opy_ (u"ࠨࡻࡾࡽࢀࠦᇽ").format(env.get(bstack11111_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡋࡕࡕࡏࡆࡄࡘࡎࡕࡎࡔࡇࡕ࡚ࡊࡘࡕࡓࡋࠪᇾ")), env.get(bstack11111_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡖࡒࡐࡌࡈࡇ࡙ࡏࡄࠨᇿ"))),
            bstack11111_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦሀ"): env.get(bstack11111_opy_ (u"ࠥࡗ࡞࡙ࡔࡆࡏࡢࡈࡊࡌࡉࡏࡋࡗࡍࡔࡔࡉࡅࠤሁ")),
            bstack11111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥሂ"): env.get(bstack11111_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧሃ"))
        }
    if bstack1ll1ll11_opy_(env.get(bstack11111_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࠣሄ"))):
        return {
            bstack11111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧህ"): bstack11111_opy_ (u"ࠣࡃࡳࡴࡻ࡫ࡹࡰࡴࠥሆ"),
            bstack11111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧሇ"): bstack11111_opy_ (u"ࠥࡿࢂ࠵ࡰࡳࡱ࡭ࡩࡨࡺ࠯ࡼࡿ࠲ࡿࢂ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾࠤለ").format(env.get(bstack11111_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡕࡓࡎࠪሉ")), env.get(bstack11111_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡂࡅࡆࡓ࡚ࡔࡔࡠࡐࡄࡑࡊ࠭ሊ")), env.get(bstack11111_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡒࡕࡓࡏࡋࡃࡕࡡࡖࡐ࡚ࡍࠧላ")), env.get(bstack11111_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫሌ"))),
            bstack11111_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥል"): env.get(bstack11111_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨሎ")),
            bstack11111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤሏ"): env.get(bstack11111_opy_ (u"ࠦࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧሐ"))
        }
    if env.get(bstack11111_opy_ (u"ࠧࡇ࡚ࡖࡔࡈࡣࡍ࡚ࡔࡑࡡࡘࡗࡊࡘ࡟ࡂࡉࡈࡒ࡙ࠨሑ")) and env.get(bstack11111_opy_ (u"ࠨࡔࡇࡡࡅ࡙ࡎࡒࡄࠣሒ")):
        return {
            bstack11111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧሓ"): bstack11111_opy_ (u"ࠣࡃࡽࡹࡷ࡫ࠠࡄࡋࠥሔ"),
            bstack11111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧሕ"): bstack11111_opy_ (u"ࠥࡿࢂࢁࡽ࠰ࡡࡥࡹ࡮ࡲࡤ࠰ࡴࡨࡷࡺࡲࡴࡴࡁࡥࡹ࡮ࡲࡤࡊࡦࡀࡿࢂࠨሖ").format(env.get(bstack11111_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡈࡒ࡙ࡓࡊࡁࡕࡋࡒࡒࡘࡋࡒࡗࡇࡕ࡙ࡗࡏࠧሗ")), env.get(bstack11111_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡓࡖࡔࡐࡅࡄࡖࠪመ")), env.get(bstack11111_opy_ (u"࠭ࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉ࠭ሙ"))),
            bstack11111_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤሚ"): env.get(bstack11111_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣማ")),
            bstack11111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣሜ"): env.get(bstack11111_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠥም"))
        }
    if any([env.get(bstack11111_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤሞ")), env.get(bstack11111_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡔࡈࡗࡔࡒࡖࡆࡆࡢࡗࡔ࡛ࡒࡄࡇࡢ࡚ࡊࡘࡓࡊࡑࡑࠦሟ")), env.get(bstack11111_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡖࡓ࡚ࡘࡃࡆࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥሠ"))]):
        return {
            bstack11111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧሡ"): bstack11111_opy_ (u"ࠣࡃ࡚ࡗࠥࡉ࡯ࡥࡧࡅࡹ࡮ࡲࡤࠣሢ"),
            bstack11111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧሣ"): env.get(bstack11111_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡐࡖࡄࡏࡍࡈࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤሤ")),
            bstack11111_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨሥ"): env.get(bstack11111_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥሦ")),
            bstack11111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧሧ"): env.get(bstack11111_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧረ"))
        }
    if env.get(bstack11111_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡎࡶ࡯ࡥࡩࡷࠨሩ")):
        return {
            bstack11111_opy_ (u"ࠤࡱࡥࡲ࡫ࠢሪ"): bstack11111_opy_ (u"ࠥࡆࡦࡳࡢࡰࡱࠥራ"),
            bstack11111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢሬ"): env.get(bstack11111_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡖࡪࡹࡵ࡭ࡶࡶ࡙ࡷࡲࠢር")),
            bstack11111_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣሮ"): env.get(bstack11111_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡴࡪࡲࡶࡹࡐ࡯ࡣࡐࡤࡱࡪࠨሯ")),
            bstack11111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢሰ"): env.get(bstack11111_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡥࡹ࡮ࡲࡤࡏࡷࡰࡦࡪࡸࠢሱ"))
        }
    if env.get(bstack11111_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࠦሲ")) or env.get(bstack11111_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡓࡁࡊࡐࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤ࡙ࡔࡂࡔࡗࡉࡉࠨሳ")):
        return {
            bstack11111_opy_ (u"ࠧࡴࡡ࡮ࡧࠥሴ"): bstack11111_opy_ (u"ࠨࡗࡦࡴࡦ࡯ࡪࡸࠢስ"),
            bstack11111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥሶ"): env.get(bstack11111_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧሷ")),
            bstack11111_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦሸ"): bstack11111_opy_ (u"ࠥࡑࡦ࡯࡮ࠡࡒ࡬ࡴࡪࡲࡩ࡯ࡧࠥሹ") if env.get(bstack11111_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡓࡁࡊࡐࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤ࡙ࡔࡂࡔࡗࡉࡉࠨሺ")) else None,
            bstack11111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦሻ"): env.get(bstack11111_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡈࡋࡗࡣࡈࡕࡍࡎࡋࡗࠦሼ"))
        }
    if any([env.get(bstack11111_opy_ (u"ࠢࡈࡅࡓࡣࡕࡘࡏࡋࡇࡆࡘࠧሽ")), env.get(bstack11111_opy_ (u"ࠣࡉࡆࡐࡔ࡛ࡄࡠࡒࡕࡓࡏࡋࡃࡕࠤሾ")), env.get(bstack11111_opy_ (u"ࠤࡊࡓࡔࡍࡌࡆࡡࡆࡐࡔ࡛ࡄࡠࡒࡕࡓࡏࡋࡃࡕࠤሿ"))]):
        return {
            bstack11111_opy_ (u"ࠥࡲࡦࡳࡥࠣቀ"): bstack11111_opy_ (u"ࠦࡌࡵ࡯ࡨ࡮ࡨࠤࡈࡲ࡯ࡶࡦࠥቁ"),
            bstack11111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣቂ"): None,
            bstack11111_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣቃ"): env.get(bstack11111_opy_ (u"ࠢࡑࡔࡒࡎࡊࡉࡔࡠࡋࡇࠦቄ")),
            bstack11111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢቅ"): env.get(bstack11111_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡋࡇࠦቆ"))
        }
    if env.get(bstack11111_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࠨቇ")):
        return {
            bstack11111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤቈ"): bstack11111_opy_ (u"࡙ࠧࡨࡪࡲࡳࡥࡧࡲࡥࠣ቉"),
            bstack11111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤቊ"): env.get(bstack11111_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨቋ")),
            bstack11111_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥቌ"): bstack11111_opy_ (u"ࠤࡍࡳࡧࠦࠣࡼࡿࠥቍ").format(env.get(bstack11111_opy_ (u"ࠪࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡊࡐࡄࡢࡍࡉ࠭቎"))) if env.get(bstack11111_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡋࡑࡅࡣࡎࡊࠢ቏")) else None,
            bstack11111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦቐ"): env.get(bstack11111_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣቑ"))
        }
    if bstack1ll1ll11_opy_(env.get(bstack11111_opy_ (u"ࠢࡏࡇࡗࡐࡎࡌ࡙ࠣቒ"))):
        return {
            bstack11111_opy_ (u"ࠣࡰࡤࡱࡪࠨቓ"): bstack11111_opy_ (u"ࠤࡑࡩࡹࡲࡩࡧࡻࠥቔ"),
            bstack11111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨቕ"): env.get(bstack11111_opy_ (u"ࠦࡉࡋࡐࡍࡑ࡜ࡣ࡚ࡘࡌࠣቖ")),
            bstack11111_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ቗"): env.get(bstack11111_opy_ (u"ࠨࡓࡊࡖࡈࡣࡓࡇࡍࡆࠤቘ")),
            bstack11111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ቙"): env.get(bstack11111_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥቚ"))
        }
    if bstack1ll1ll11_opy_(env.get(bstack11111_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡࡄࡇ࡙ࡏࡏࡏࡕࠥቛ"))):
        return {
            bstack11111_opy_ (u"ࠥࡲࡦࡳࡥࠣቜ"): bstack11111_opy_ (u"ࠦࡌ࡯ࡴࡉࡷࡥࠤࡆࡩࡴࡪࡱࡱࡷࠧቝ"),
            bstack11111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ቞"): bstack11111_opy_ (u"ࠨࡻࡾ࠱ࡾࢁ࠴ࡧࡣࡵ࡫ࡲࡲࡸ࠵ࡲࡶࡰࡶ࠳ࢀࢃࠢ቟").format(env.get(bstack11111_opy_ (u"ࠧࡈࡋࡗࡌ࡚ࡈ࡟ࡔࡇࡕ࡚ࡊࡘ࡟ࡖࡔࡏࠫበ")), env.get(bstack11111_opy_ (u"ࠨࡉࡌࡘࡍ࡛ࡂࡠࡔࡈࡔࡔ࡙ࡉࡕࡑࡕ࡝ࠬቡ")), env.get(bstack11111_opy_ (u"ࠩࡊࡍ࡙ࡎࡕࡃࡡࡕ࡙ࡓࡥࡉࡅࠩቢ"))),
            bstack11111_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧባ"): env.get(bstack11111_opy_ (u"ࠦࡌࡏࡔࡉࡗࡅࡣ࡜ࡕࡒࡌࡈࡏࡓ࡜ࠨቤ")),
            bstack11111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦብ"): env.get(bstack11111_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡒࡖࡐࡢࡍࡉࠨቦ"))
        }
    if env.get(bstack11111_opy_ (u"ࠢࡄࡋࠥቧ")) == bstack11111_opy_ (u"ࠣࡶࡵࡹࡪࠨቨ") and env.get(bstack11111_opy_ (u"ࠤ࡙ࡉࡗࡉࡅࡍࠤቩ")) == bstack11111_opy_ (u"ࠥ࠵ࠧቪ"):
        return {
            bstack11111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤቫ"): bstack11111_opy_ (u"ࠧ࡜ࡥࡳࡥࡨࡰࠧቬ"),
            bstack11111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤቭ"): bstack11111_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࡼࡿࠥቮ").format(env.get(bstack11111_opy_ (u"ࠨࡘࡈࡖࡈࡋࡌࡠࡗࡕࡐࠬቯ"))),
            bstack11111_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦተ"): None,
            bstack11111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤቱ"): None,
        }
    if env.get(bstack11111_opy_ (u"࡙ࠦࡋࡁࡎࡅࡌࡘ࡞ࡥࡖࡆࡔࡖࡍࡔࡔࠢቲ")):
        return {
            bstack11111_opy_ (u"ࠧࡴࡡ࡮ࡧࠥታ"): bstack11111_opy_ (u"ࠨࡔࡦࡣࡰࡧ࡮ࡺࡹࠣቴ"),
            bstack11111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥት"): None,
            bstack11111_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥቶ"): env.get(bstack11111_opy_ (u"ࠤࡗࡉࡆࡓࡃࡊࡖ࡜ࡣࡕࡘࡏࡋࡇࡆࡘࡤࡔࡁࡎࡇࠥቷ")),
            bstack11111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤቸ"): env.get(bstack11111_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥቹ"))
        }
    if any([env.get(bstack11111_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࠣቺ")), env.get(bstack11111_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࡡࡘࡖࡑࠨቻ")), env.get(bstack11111_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠧቼ")), env.get(bstack11111_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࡣ࡙ࡋࡁࡎࠤች"))]):
        return {
            bstack11111_opy_ (u"ࠤࡱࡥࡲ࡫ࠢቾ"): bstack11111_opy_ (u"ࠥࡇࡴࡴࡣࡰࡷࡵࡷࡪࠨቿ"),
            bstack11111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢኀ"): None,
            bstack11111_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢኁ"): env.get(bstack11111_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢኂ")) or None,
            bstack11111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨኃ"): env.get(bstack11111_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥኄ"), 0)
        }
    if env.get(bstack11111_opy_ (u"ࠤࡊࡓࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢኅ")):
        return {
            bstack11111_opy_ (u"ࠥࡲࡦࡳࡥࠣኆ"): bstack11111_opy_ (u"ࠦࡌࡵࡃࡅࠤኇ"),
            bstack11111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣኈ"): None,
            bstack11111_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ኉"): env.get(bstack11111_opy_ (u"ࠢࡈࡑࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧኊ")),
            bstack11111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢኋ"): env.get(bstack11111_opy_ (u"ࠤࡊࡓࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡄࡑࡘࡒ࡙ࡋࡒࠣኌ"))
        }
    if env.get(bstack11111_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣኍ")):
        return {
            bstack11111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ኎"): bstack11111_opy_ (u"ࠧࡉ࡯ࡥࡧࡉࡶࡪࡹࡨࠣ኏"),
            bstack11111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤነ"): env.get(bstack11111_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨኑ")),
            bstack11111_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥኒ"): env.get(bstack11111_opy_ (u"ࠤࡆࡊࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡏࡃࡐࡉࠧና")),
            bstack11111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤኔ"): env.get(bstack11111_opy_ (u"ࠦࡈࡌ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤን"))
        }
    return {bstack11111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦኖ"): None}
def get_host_info():
    return {
        bstack11111_opy_ (u"ࠨࡨࡰࡵࡷࡲࡦࡳࡥࠣኗ"): platform.node(),
        bstack11111_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠤኘ"): platform.system(),
        bstack11111_opy_ (u"ࠣࡶࡼࡴࡪࠨኙ"): platform.machine(),
        bstack11111_opy_ (u"ࠤࡹࡩࡷࡹࡩࡰࡰࠥኚ"): platform.version(),
        bstack11111_opy_ (u"ࠥࡥࡷࡩࡨࠣኛ"): platform.architecture()[0]
    }
def bstack1ll111l11l_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack111llll1l1_opy_():
    if bstack11111111_opy_.get_property(bstack11111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬኜ")):
        return bstack11111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫኝ")
    return bstack11111_opy_ (u"࠭ࡵ࡯࡭ࡱࡳࡼࡴ࡟ࡨࡴ࡬ࡨࠬኞ")
def bstack11l1l11111_opy_(driver):
    info = {
        bstack11111_opy_ (u"ࠧࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ኟ"): driver.capabilities,
        bstack11111_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠬአ"): driver.session_id,
        bstack11111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪኡ"): driver.capabilities.get(bstack11111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨኢ"), None),
        bstack11111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ኣ"): driver.capabilities.get(bstack11111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ኤ"), None),
        bstack11111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠨእ"): driver.capabilities.get(bstack11111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭ኦ"), None),
    }
    if bstack111llll1l1_opy_() == bstack11111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧኧ"):
        info[bstack11111_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࠪከ")] = bstack11111_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩኩ") if bstack111l11111_opy_() else bstack11111_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ኪ")
    return info
def bstack111l11111_opy_():
    if bstack11111111_opy_.get_property(bstack11111_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫካ")):
        return True
    if bstack1ll1ll11_opy_(os.environ.get(bstack11111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧኬ"), None)):
        return True
    return False
def bstack1lll11l11l_opy_(bstack11l111l111_opy_, url, data, config):
    headers = config.get(bstack11111_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨክ"), None)
    proxies = bstack1lll1ll1l1_opy_(config, url)
    auth = config.get(bstack11111_opy_ (u"ࠨࡣࡸࡸ࡭࠭ኮ"), None)
    response = requests.request(
            bstack11l111l111_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1ll11l1l1l_opy_(bstack11l11l11l_opy_, size):
    bstack1ll1lll1_opy_ = []
    while len(bstack11l11l11l_opy_) > size:
        bstack1l11l11l1_opy_ = bstack11l11l11l_opy_[:size]
        bstack1ll1lll1_opy_.append(bstack1l11l11l1_opy_)
        bstack11l11l11l_opy_ = bstack11l11l11l_opy_[size:]
    bstack1ll1lll1_opy_.append(bstack11l11l11l_opy_)
    return bstack1ll1lll1_opy_
def bstack111lllll1l_opy_(message, bstack11l1l11l11_opy_=False):
    os.write(1, bytes(message, bstack11111_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨኯ")))
    os.write(1, bytes(bstack11111_opy_ (u"ࠪࡠࡳ࠭ኰ"), bstack11111_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪ኱")))
    if bstack11l1l11l11_opy_:
        with open(bstack11111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠲ࡵ࠱࠲ࡻ࠰ࠫኲ") + os.environ[bstack11111_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬኳ")] + bstack11111_opy_ (u"ࠧ࠯࡮ࡲ࡫ࠬኴ"), bstack11111_opy_ (u"ࠨࡣࠪኵ")) as f:
            f.write(message + bstack11111_opy_ (u"ࠩ࡟ࡲࠬ኶"))
def bstack111lll1lll_opy_():
    return os.environ[bstack11111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭኷")].lower() == bstack11111_opy_ (u"ࠫࡹࡸࡵࡦࠩኸ")
def bstack1ll1l1lll1_opy_(bstack111llll111_opy_):
    return bstack11111_opy_ (u"ࠬࢁࡽ࠰ࡽࢀࠫኹ").format(bstack11l1l1l11l_opy_, bstack111llll111_opy_)
def bstack11l1111l1_opy_():
    return datetime.datetime.utcnow().isoformat() + bstack11111_opy_ (u"࡚࠭ࠨኺ")
def bstack11l11l1lll_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack11111_opy_ (u"࡛ࠧࠩኻ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack11111_opy_ (u"ࠨ࡜ࠪኼ")))).total_seconds() * 1000
def bstack11l11l11l1_opy_(timestamp):
    return datetime.datetime.utcfromtimestamp(timestamp).isoformat() + bstack11111_opy_ (u"ࠩ࡝ࠫኽ")
def bstack11l11lll1l_opy_(bstack11l1l1111l_opy_):
    date_format = bstack11111_opy_ (u"ࠪࠩ࡞ࠫ࡭ࠦࡦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗ࠳ࠫࡦࠨኾ")
    bstack11l11l111l_opy_ = datetime.datetime.strptime(bstack11l1l1111l_opy_, date_format)
    return bstack11l11l111l_opy_.isoformat() + bstack11111_opy_ (u"ࠫ࡟࠭኿")
def bstack11l111lll1_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack11111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬዀ")
    else:
        return bstack11111_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭዁")
def bstack1ll1ll11_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack11111_opy_ (u"ࠧࡵࡴࡸࡩࠬዂ")
def bstack11l111llll_opy_(val):
    return val.__str__().lower() == bstack11111_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧዃ")
def bstack1l111ll1ll_opy_(bstack11l11lll11_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11l11lll11_opy_ as e:
                print(bstack11111_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡿࢂࠦ࠭࠿ࠢࡾࢁ࠿ࠦࡻࡾࠤዄ").format(func.__name__, bstack11l11lll11_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11l11111ll_opy_(bstack111lllll11_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack111lllll11_opy_(cls, *args, **kwargs)
            except bstack11l11lll11_opy_ as e:
                print(bstack11111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࢀࢃࠠ࠮ࡀࠣࡿࢂࡀࠠࡼࡿࠥዅ").format(bstack111lllll11_opy_.__name__, bstack11l11lll11_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11l11111ll_opy_
    else:
        return decorator
def bstack1l1111l1_opy_(bstack11lll111l1_opy_):
    if bstack11111_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ዆") in bstack11lll111l1_opy_ and bstack11l111llll_opy_(bstack11lll111l1_opy_[bstack11111_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ዇")]):
        return False
    if bstack11111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨወ") in bstack11lll111l1_opy_ and bstack11l111llll_opy_(bstack11lll111l1_opy_[bstack11111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩዉ")]):
        return False
    return True
def bstack1ll1l11l1_opy_():
    try:
        from pytest_bdd import reporting
        return True
    except Exception as e:
        return False
def bstack1l11111ll_opy_(hub_url):
    if bstack1l1lll111l_opy_() <= version.parse(bstack11111_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨዊ")):
        if hub_url != bstack11111_opy_ (u"ࠩࠪዋ"):
            return bstack11111_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦዌ") + hub_url + bstack11111_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣው")
        return bstack1ll1ll11l_opy_
    if hub_url != bstack11111_opy_ (u"ࠬ࠭ዎ"):
        return bstack11111_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࠣዏ") + hub_url + bstack11111_opy_ (u"ࠢ࠰ࡹࡧ࠳࡭ࡻࡢࠣዐ")
    return bstack1l1llllll_opy_
def bstack11l1l11l1l_opy_():
    return isinstance(os.getenv(bstack11111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑ࡛ࡗࡉࡘ࡚࡟ࡑࡎࡘࡋࡎࡔࠧዑ")), str)
def bstack1lll11ll1l_opy_(url):
    return urlparse(url).hostname
def bstack1l1l1l1l1l_opy_(hostname):
    for bstack11lll111l_opy_ in bstack1ll1lll11_opy_:
        regex = re.compile(bstack11lll111l_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11l1111111_opy_(bstack11l111ll11_opy_, file_name, logger):
    bstack111ll1ll1_opy_ = os.path.join(os.path.expanduser(bstack11111_opy_ (u"ࠩࢁࠫዒ")), bstack11l111ll11_opy_)
    try:
        if not os.path.exists(bstack111ll1ll1_opy_):
            os.makedirs(bstack111ll1ll1_opy_)
        file_path = os.path.join(os.path.expanduser(bstack11111_opy_ (u"ࠪࢂࠬዓ")), bstack11l111ll11_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack11111_opy_ (u"ࠫࡼ࠭ዔ")):
                pass
            with open(file_path, bstack11111_opy_ (u"ࠧࡽࠫࠣዕ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1lllllll1_opy_.format(str(e)))
def bstack11l11l1ll1_opy_(file_name, key, value, logger):
    file_path = bstack11l1111111_opy_(bstack11111_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ዖ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1l1lll1l1_opy_ = json.load(open(file_path, bstack11111_opy_ (u"ࠧࡳࡤࠪ዗")))
        else:
            bstack1l1lll1l1_opy_ = {}
        bstack1l1lll1l1_opy_[key] = value
        with open(file_path, bstack11111_opy_ (u"ࠣࡹ࠮ࠦዘ")) as outfile:
            json.dump(bstack1l1lll1l1_opy_, outfile)
def bstack1l1l1llll_opy_(file_name, logger):
    file_path = bstack11l1111111_opy_(bstack11111_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩዙ"), file_name, logger)
    bstack1l1lll1l1_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack11111_opy_ (u"ࠪࡶࠬዚ")) as bstack1l1l11l11_opy_:
            bstack1l1lll1l1_opy_ = json.load(bstack1l1l11l11_opy_)
    return bstack1l1lll1l1_opy_
def bstack1l1ll11lll_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack11111_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡤࡦ࡮ࡨࡸ࡮ࡴࡧࠡࡨ࡬ࡰࡪࡀࠠࠨዛ") + file_path + bstack11111_opy_ (u"ࠬࠦࠧዜ") + str(e))
def bstack1l1lll111l_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack11111_opy_ (u"ࠨ࠼ࡏࡑࡗࡗࡊ࡚࠾ࠣዝ")
def bstack1ll11111_opy_(config):
    if bstack11111_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ዞ") in config:
        del (config[bstack11111_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧዟ")])
        return False
    if bstack1l1lll111l_opy_() < version.parse(bstack11111_opy_ (u"ࠩ࠶࠲࠹࠴࠰ࠨዠ")):
        return False
    if bstack1l1lll111l_opy_() >= version.parse(bstack11111_opy_ (u"ࠪ࠸࠳࠷࠮࠶ࠩዡ")):
        return True
    if bstack11111_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫዢ") in config and config[bstack11111_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬዣ")] is False:
        return False
    else:
        return True
def bstack11l11111l_opy_(args_list, bstack11l11l1111_opy_):
    index = -1
    for value in bstack11l11l1111_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack11lllll1ll_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack11lllll1ll_opy_ = bstack11lllll1ll_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack11111_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ዤ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack11111_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧዥ"), exception=exception)
    def bstack11ll1lll11_opy_(self):
        if self.result != bstack11111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨዦ"):
            return None
        if bstack11111_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧዧ") in self.exception_type:
            return bstack11111_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦየ")
        return bstack11111_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧዩ")
    def bstack111llll11l_opy_(self):
        if self.result != bstack11111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬዪ"):
            return None
        if self.bstack11lllll1ll_opy_:
            return self.bstack11lllll1ll_opy_
        return bstack11l11l11ll_opy_(self.exception)
def bstack11l11l11ll_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack111lll1l11_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1ll1l11ll_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack111l11lll_opy_(config, logger):
    try:
        import playwright
        bstack11l11ll111_opy_ = playwright.__file__
        bstack11l11ll11l_opy_ = os.path.split(bstack11l11ll111_opy_)
        bstack11l11lllll_opy_ = bstack11l11ll11l_opy_[0] + bstack11111_opy_ (u"࠭࠯ࡥࡴ࡬ࡺࡪࡸ࠯ࡱࡣࡦ࡯ࡦ࡭ࡥ࠰࡮࡬ࡦ࠴ࡩ࡬ࡪ࠱ࡦࡰ࡮࠴ࡪࡴࠩያ")
        os.environ[bstack11111_opy_ (u"ࠧࡈࡎࡒࡆࡆࡒ࡟ࡂࡉࡈࡒ࡙ࡥࡈࡕࡖࡓࡣࡕࡘࡏ࡙࡛ࠪዬ")] = bstack1lll11l1ll_opy_(config)
        with open(bstack11l11lllll_opy_, bstack11111_opy_ (u"ࠨࡴࠪይ")) as f:
            bstack111111l1l_opy_ = f.read()
            bstack111lllllll_opy_ = bstack11111_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭࠯ࡤ࡫ࡪࡴࡴࠨዮ")
            bstack111lll11ll_opy_ = bstack111111l1l_opy_.find(bstack111lllllll_opy_)
            if bstack111lll11ll_opy_ == -1:
              process = subprocess.Popen(bstack11111_opy_ (u"ࠥࡲࡵࡳࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺࠢዯ"), shell=True, cwd=bstack11l11ll11l_opy_[0])
              process.wait()
              bstack11l11llll1_opy_ = bstack11111_opy_ (u"ࠫࠧࡻࡳࡦࠢࡶࡸࡷ࡯ࡣࡵࠤ࠾ࠫደ")
              bstack11l111l1ll_opy_ = bstack11111_opy_ (u"ࠧࠨࠢࠡ࡞ࠥࡹࡸ࡫ࠠࡴࡶࡵ࡭ࡨࡺ࡜ࠣ࠽ࠣࡧࡴࡴࡳࡵࠢࡾࠤࡧࡵ࡯ࡵࡵࡷࡶࡦࡶࠠࡾࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭࠭ࡧ࡭ࡱࡥࡥࡱ࠳ࡡࡨࡧࡱࡸࠬ࠯࠻ࠡ࡫ࡩࠤ࠭ࡶࡲࡰࡥࡨࡷࡸ࠴ࡥ࡯ࡸ࠱ࡋࡑࡕࡂࡂࡎࡢࡅࡌࡋࡎࡕࡡࡋࡘ࡙ࡖ࡟ࡑࡔࡒ࡜࡞࠯ࠠࡣࡱࡲࡸࡸࡺࡲࡢࡲࠫ࠭ࡀࠦࠢࠣࠤዱ")
              bstack111llllll1_opy_ = bstack111111l1l_opy_.replace(bstack11l11llll1_opy_, bstack11l111l1ll_opy_)
              with open(bstack11l11lllll_opy_, bstack11111_opy_ (u"࠭ࡷࠨዲ")) as f:
                f.write(bstack111llllll1_opy_)
    except Exception as e:
        logger.error(bstack1l11l1ll1_opy_.format(str(e)))
def bstack1l11l1111_opy_():
  try:
    bstack111lll111l_opy_ = os.path.join(tempfile.gettempdir(), bstack11111_opy_ (u"ࠧࡰࡲࡷ࡭ࡲࡧ࡬ࡠࡪࡸࡦࡤࡻࡲ࡭࠰࡭ࡷࡴࡴࠧዳ"))
    bstack11l1l111ll_opy_ = []
    if os.path.exists(bstack111lll111l_opy_):
      with open(bstack111lll111l_opy_) as f:
        bstack11l1l111ll_opy_ = json.load(f)
      os.remove(bstack111lll111l_opy_)
    return bstack11l1l111ll_opy_
  except:
    pass
  return []
def bstack1lll111ll1_opy_(bstack1llll1l1l1_opy_):
  try:
    bstack11l1l111ll_opy_ = []
    bstack111lll111l_opy_ = os.path.join(tempfile.gettempdir(), bstack11111_opy_ (u"ࠨࡱࡳࡸ࡮ࡳࡡ࡭ࡡ࡫ࡹࡧࡥࡵࡳ࡮࠱࡮ࡸࡵ࡮ࠨዴ"))
    if os.path.exists(bstack111lll111l_opy_):
      with open(bstack111lll111l_opy_) as f:
        bstack11l1l111ll_opy_ = json.load(f)
    bstack11l1l111ll_opy_.append(bstack1llll1l1l1_opy_)
    with open(bstack111lll111l_opy_, bstack11111_opy_ (u"ࠩࡺࠫድ")) as f:
        json.dump(bstack11l1l111ll_opy_, f)
  except:
    pass
def bstack111l1llll_opy_(logger, bstack11l1l111l1_opy_ = False):
  try:
    test_name = os.environ.get(bstack11111_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࡢࡘࡊ࡙ࡔࡠࡐࡄࡑࡊ࠭ዶ"), bstack11111_opy_ (u"ࠫࠬዷ"))
    if test_name == bstack11111_opy_ (u"ࠬ࠭ዸ"):
        test_name = threading.current_thread().__dict__.get(bstack11111_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡈࡤࡥࡡࡷࡩࡸࡺ࡟࡯ࡣࡰࡩࠬዹ"), bstack11111_opy_ (u"ࠧࠨዺ"))
    bstack11l11l1l11_opy_ = bstack11111_opy_ (u"ࠨ࠮ࠣࠫዻ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11l1l111l1_opy_:
        bstack11lll1ll_opy_ = os.environ.get(bstack11111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩዼ"), bstack11111_opy_ (u"ࠪ࠴ࠬዽ"))
        bstack1ll111ll1_opy_ = {bstack11111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩዾ"): test_name, bstack11111_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫዿ"): bstack11l11l1l11_opy_, bstack11111_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬጀ"): bstack11lll1ll_opy_}
        bstack11l111111l_opy_ = []
        bstack11l1111l11_opy_ = os.path.join(tempfile.gettempdir(), bstack11111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡱࡲࡳࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ጁ"))
        if os.path.exists(bstack11l1111l11_opy_):
            with open(bstack11l1111l11_opy_) as f:
                bstack11l111111l_opy_ = json.load(f)
        bstack11l111111l_opy_.append(bstack1ll111ll1_opy_)
        with open(bstack11l1111l11_opy_, bstack11111_opy_ (u"ࠨࡹࠪጂ")) as f:
            json.dump(bstack11l111111l_opy_, f)
    else:
        bstack1ll111ll1_opy_ = {bstack11111_opy_ (u"ࠩࡱࡥࡲ࡫ࠧጃ"): test_name, bstack11111_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩጄ"): bstack11l11l1l11_opy_, bstack11111_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪጅ"): str(multiprocessing.current_process().name)}
        if bstack11111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵࠩጆ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1ll111ll1_opy_)
  except Exception as e:
      logger.warn(bstack11111_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡲࡼࡸࡪࡹࡴࠡࡨࡸࡲࡳ࡫࡬ࠡࡦࡤࡸࡦࡀࠠࡼࡿࠥጇ").format(e))
def bstack11l11lll1_opy_(error_message, test_name, index, logger):
  try:
    bstack11l111ll1l_opy_ = []
    bstack1ll111ll1_opy_ = {bstack11111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬገ"): test_name, bstack11111_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧጉ"): error_message, bstack11111_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨጊ"): index}
    bstack11l1111lll_opy_ = os.path.join(tempfile.gettempdir(), bstack11111_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫጋ"))
    if os.path.exists(bstack11l1111lll_opy_):
        with open(bstack11l1111lll_opy_) as f:
            bstack11l111ll1l_opy_ = json.load(f)
    bstack11l111ll1l_opy_.append(bstack1ll111ll1_opy_)
    with open(bstack11l1111lll_opy_, bstack11111_opy_ (u"ࠫࡼ࠭ጌ")) as f:
        json.dump(bstack11l111ll1l_opy_, f)
  except Exception as e:
    logger.warn(bstack11111_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡳࡱࡥࡳࡹࠦࡦࡶࡰࡱࡩࡱࠦࡤࡢࡶࡤ࠾ࠥࢁࡽࠣግ").format(e))
def bstack1llll11ll_opy_(bstack1l1ll11111_opy_, name, logger):
  try:
    bstack1ll111ll1_opy_ = {bstack11111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫጎ"): name, bstack11111_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ጏ"): bstack1l1ll11111_opy_, bstack11111_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧጐ"): str(threading.current_thread()._name)}
    return bstack1ll111ll1_opy_
  except Exception as e:
    logger.warn(bstack11111_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡧ࡫ࡨࡢࡸࡨࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢ࠼ࠣࡿࢂࠨ጑").format(e))
  return
def bstack11l1111ll1_opy_():
    return platform.system() == bstack11111_opy_ (u"࡛ࠪ࡮ࡴࡤࡰࡹࡶࠫጒ")
def bstack111llllll_opy_(bstack11l11l1l1l_opy_, config, logger):
    bstack11l111l11l_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack11l11l1l1l_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack11111_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫࡯ࡸࡪࡸࠠࡤࡱࡱࡪ࡮࡭ࠠ࡬ࡧࡼࡷࠥࡨࡹࠡࡴࡨ࡫ࡪࡾࠠ࡮ࡣࡷࡧ࡭ࡀࠠࡼࡿࠥጓ").format(e))
    return bstack11l111l11l_opy_