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
import atexit
import datetime
import inspect
import logging
import os
import signal
import sys
import threading
from uuid import uuid4
from bstack_utils.percy_sdk import PercySDK
import tempfile
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1llll111l1_opy_, bstack1l1l1l111l_opy_, update, bstack1ll1llll11_opy_,
                                       bstack111ll11ll_opy_, bstack1l11111l1_opy_, bstack1ll1l11lll_opy_, bstack111lll1l1_opy_,
                                       bstack1ll11111l_opy_, bstack1l11lll11_opy_, bstack1l1lll1111_opy_, bstack1111lll11_opy_,
                                       bstack1l11l111l_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1llll1lll_opy_)
from browserstack_sdk.bstack1l1l11l1l_opy_ import bstack1l1lllll_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack1ll1l1l1_opy_
from bstack_utils.capture import bstack11lll1ll11_opy_
from bstack_utils.config import Config
from bstack_utils.constants import bstack11ll1l1ll_opy_, bstack1l11l1lll1_opy_, bstack11111lll_opy_, \
    bstack1llll1ll11_opy_
from bstack_utils.helper import bstack1ll1l11ll_opy_, bstack1ll111l11l_opy_, bstack111lll1lll_opy_, bstack11l1111l1_opy_, \
    bstack11l111lll1_opy_, \
    bstack11l1111l1l_opy_, bstack1l1lll111l_opy_, bstack1l11111ll_opy_, bstack11l1l11l1l_opy_, bstack1ll1l11l1_opy_, Notset, \
    bstack1ll11111_opy_, bstack11l11l1lll_opy_, bstack11l11l11ll_opy_, Result, bstack11l11l11l1_opy_, bstack111lll1l11_opy_, bstack1l111ll1ll_opy_, \
    bstack1lll111ll1_opy_, bstack111l1llll_opy_, bstack1ll1ll11_opy_, bstack11l1111ll1_opy_
from bstack_utils.bstack111ll1l11l_opy_ import bstack111ll1l111_opy_
from bstack_utils.messages import bstack1lllllllll_opy_, bstack1l1l11ll11_opy_, bstack1l1l11111l_opy_, bstack1ll1l111l_opy_, bstack1l111l1l_opy_, \
    bstack1l11l1ll1_opy_, bstack11l1l1l11_opy_, bstack1111l1111_opy_, bstack1l1l11lll_opy_, bstack1ll1l111_opy_, \
    bstack1ll1ll1l11_opy_, bstack1lll1l1111_opy_
from bstack_utils.proxy import bstack1lll11l1ll_opy_, bstack1ll1lll1ll_opy_
from bstack_utils.bstack1lll111l_opy_ import bstack1lllllllll1_opy_, bstack1lllllll111_opy_, bstack1llllll1lll_opy_, bstack1llllll1l1l_opy_, \
    bstack111111111l_opy_, bstack1111111111_opy_, bstack1llllllll1l_opy_, bstack1llllllll1_opy_, bstack11111111l1_opy_
from bstack_utils.bstack1lll1llll_opy_ import bstack1ll11l1ll_opy_
from bstack_utils.bstack111lllll1_opy_ import bstack1l1llllll1_opy_, bstack1llll1l11_opy_, bstack1l1ll1lll1_opy_, \
    bstack1ll1l1111_opy_, bstack11l1ll111_opy_
from bstack_utils.bstack1l1111111l_opy_ import bstack1l1111lll1_opy_
from bstack_utils.bstack1ll1llllll_opy_ import bstack11ll1l1l1_opy_
import bstack_utils.bstack1l1111ll1_opy_ as bstack1ll1l11ll1_opy_
from bstack_utils.bstack1ll11l111_opy_ import bstack1ll11l111_opy_
bstack1l1l1ll111_opy_ = None
bstack1ll11ll11_opy_ = None
bstack1lll1l11l1_opy_ = None
bstack1ll11ll1_opy_ = None
bstack1l1l111l1_opy_ = None
bstack1l1l1l1111_opy_ = None
bstack1l111111l_opy_ = None
bstack1llllll11_opy_ = None
bstack1l1ll1l111_opy_ = None
bstack1lll1l1lll_opy_ = None
bstack1lll1lll_opy_ = None
bstack1ll1lll111_opy_ = None
bstack1l1111l1l_opy_ = None
bstack1l1l1lll1l_opy_ = bstack11111_opy_ (u"ࠩࠪᖿ")
CONFIG = {}
bstack1111l1l11_opy_ = False
bstack1l1l11llll_opy_ = bstack11111_opy_ (u"ࠪࠫᗀ")
bstack1llll1ll_opy_ = bstack11111_opy_ (u"ࠫࠬᗁ")
bstack1l1lll11_opy_ = False
bstack1l1ll1llll_opy_ = []
bstack11l111l1_opy_ = bstack11ll1l1ll_opy_
bstack1lll1ll111l_opy_ = bstack11111_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᗂ")
bstack1lll1lll1l1_opy_ = False
bstack1lll11l1l_opy_ = {}
bstack11l1ll11l_opy_ = False
logger = bstack1ll1l1l1_opy_.get_logger(__name__, bstack11l111l1_opy_)
store = {
    bstack11111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᗃ"): []
}
bstack1lll1l111ll_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_11llll1111_opy_ = {}
current_test_uuid = None
def bstack11111ll11_opy_(page, bstack1l1llll1ll_opy_):
    try:
        page.evaluate(bstack11111_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣᗄ"),
                      bstack11111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠬᗅ") + json.dumps(
                          bstack1l1llll1ll_opy_) + bstack11111_opy_ (u"ࠤࢀࢁࠧᗆ"))
    except Exception as e:
        print(bstack11111_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࢁࡽࠣᗇ"), e)
def bstack1lll1ll1l_opy_(page, message, level):
    try:
        page.evaluate(bstack11111_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧᗈ"), bstack11111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪᗉ") + json.dumps(
            message) + bstack11111_opy_ (u"࠭ࠬࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠩᗊ") + json.dumps(level) + bstack11111_opy_ (u"ࠧࡾࡿࠪᗋ"))
    except Exception as e:
        print(bstack11111_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠡࡽࢀࠦᗌ"), e)
def pytest_configure(config):
    bstack11111111_opy_ = Config.bstack111l111l_opy_()
    config.args = bstack11ll1l1l1_opy_.bstack1llll11l11l_opy_(config.args)
    bstack11111111_opy_.bstack1lllllll1l_opy_(bstack1ll1ll11_opy_(config.getoption(bstack11111_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ᗍ"))))
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack1lll1l11l11_opy_ = item.config.getoption(bstack11111_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᗎ"))
    plugins = item.config.getoption(bstack11111_opy_ (u"ࠦࡵࡲࡵࡨ࡫ࡱࡷࠧᗏ"))
    report = outcome.get_result()
    bstack1lll1l11ll1_opy_(item, call, report)
    if bstack11111_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡴࡱࡻࡧࡪࡰࠥᗐ") not in plugins or bstack1ll1l11l1_opy_():
        return
    summary = []
    driver = getattr(item, bstack11111_opy_ (u"ࠨ࡟ࡥࡴ࡬ࡺࡪࡸࠢᗑ"), None)
    page = getattr(item, bstack11111_opy_ (u"ࠢࡠࡲࡤ࡫ࡪࠨᗒ"), None)
    try:
        if (driver == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack1lll1ll1ll1_opy_(item, report, summary, bstack1lll1l11l11_opy_)
    if (page is not None):
        bstack1lll1ll11l1_opy_(item, report, summary, bstack1lll1l11l11_opy_)
def bstack1lll1ll1ll1_opy_(item, report, summary, bstack1lll1l11l11_opy_):
    if report.when == bstack11111_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᗓ") and report.skipped:
        bstack11111111l1_opy_(report)
    if report.when in [bstack11111_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣᗔ"), bstack11111_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧᗕ")]:
        return
    if not bstack111lll1lll_opy_():
        return
    try:
        if (str(bstack1lll1l11l11_opy_).lower() != bstack11111_opy_ (u"ࠫࡹࡸࡵࡦࠩᗖ")):
            item._driver.execute_script(
                bstack11111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪᗗ") + json.dumps(
                    report.nodeid) + bstack11111_opy_ (u"࠭ࡽࡾࠩᗘ"))
        os.environ[bstack11111_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪᗙ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack11111_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧ࠽ࠤࢀ࠶ࡽࠣᗚ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11111_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦᗛ")))
    bstack1l11llll_opy_ = bstack11111_opy_ (u"ࠥࠦᗜ")
    bstack11111111l1_opy_(report)
    if not passed:
        try:
            bstack1l11llll_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack11111_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡲࡦࡣࡶࡳࡳࡀࠠࡼ࠲ࢀࠦᗝ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1l11llll_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack11111_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢᗞ")))
        bstack1l11llll_opy_ = bstack11111_opy_ (u"ࠨࠢᗟ")
        if not passed:
            try:
                bstack1l11llll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11111_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡵࡩࡦࡹ࡯࡯࠼ࠣࡿ࠵ࢃࠢᗠ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1l11llll_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack11111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡩࡧࡴࡢࠤ࠽ࠤࠬᗡ")
                    + json.dumps(bstack11111_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠣࠥᗢ"))
                    + bstack11111_opy_ (u"ࠥࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࠨᗣ")
                )
            else:
                item._driver.execute_script(
                    bstack11111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡦࡴࡵࡳࡷࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡦࡤࡸࡦࠨ࠺ࠡࠩᗤ")
                    + json.dumps(str(bstack1l11llll_opy_))
                    + bstack11111_opy_ (u"ࠧࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࠣᗥ")
                )
        except Exception as e:
            summary.append(bstack11111_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡦࡴ࡮ࡰࡶࡤࡸࡪࡀࠠࡼ࠲ࢀࠦᗦ").format(e))
def bstack1lll11lll11_opy_(test_name, error_message):
    try:
        bstack1lll1l1lll1_opy_ = []
        bstack11lll1ll_opy_ = os.environ.get(bstack11111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᗧ"), bstack11111_opy_ (u"ࠨ࠲ࠪᗨ"))
        bstack1ll111ll1_opy_ = {bstack11111_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᗩ"): test_name, bstack11111_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᗪ"): error_message, bstack11111_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪᗫ"): bstack11lll1ll_opy_}
        bstack1lll1l11111_opy_ = os.path.join(tempfile.gettempdir(), bstack11111_opy_ (u"ࠬࡶࡷࡠࡲࡼࡸࡪࡹࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪᗬ"))
        if os.path.exists(bstack1lll1l11111_opy_):
            with open(bstack1lll1l11111_opy_) as f:
                bstack1lll1l1lll1_opy_ = json.load(f)
        bstack1lll1l1lll1_opy_.append(bstack1ll111ll1_opy_)
        with open(bstack1lll1l11111_opy_, bstack11111_opy_ (u"࠭ࡷࠨᗭ")) as f:
            json.dump(bstack1lll1l1lll1_opy_, f)
    except Exception as e:
        logger.debug(bstack11111_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡩࡷࡹࡩࡴࡶ࡬ࡲ࡬ࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡴࡾࡺࡥࡴࡶࠣࡩࡷࡸ࡯ࡳࡵ࠽ࠤࠬᗮ") + str(e))
def bstack1lll1ll11l1_opy_(item, report, summary, bstack1lll1l11l11_opy_):
    if report.when in [bstack11111_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢᗯ"), bstack11111_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦᗰ")]:
        return
    if (str(bstack1lll1l11l11_opy_).lower() != bstack11111_opy_ (u"ࠪࡸࡷࡻࡥࠨᗱ")):
        bstack11111ll11_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11111_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨᗲ")))
    bstack1l11llll_opy_ = bstack11111_opy_ (u"ࠧࠨᗳ")
    bstack11111111l1_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1l11llll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11111_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥࠡࡴࡨࡥࡸࡵ࡮࠻ࠢࡾ࠴ࢂࠨᗴ").format(e)
                )
        try:
            if passed:
                bstack11l1ll111_opy_(getattr(item, bstack11111_opy_ (u"ࠧࡠࡲࡤ࡫ࡪ࠭ᗵ"), None), bstack11111_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣᗶ"))
            else:
                error_message = bstack11111_opy_ (u"ࠩࠪᗷ")
                if bstack1l11llll_opy_:
                    bstack1lll1ll1l_opy_(item._page, str(bstack1l11llll_opy_), bstack11111_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤᗸ"))
                    bstack11l1ll111_opy_(getattr(item, bstack11111_opy_ (u"ࠫࡤࡶࡡࡨࡧࠪᗹ"), None), bstack11111_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᗺ"), str(bstack1l11llll_opy_))
                    error_message = str(bstack1l11llll_opy_)
                else:
                    bstack11l1ll111_opy_(getattr(item, bstack11111_opy_ (u"࠭࡟ࡱࡣࡪࡩࠬᗻ"), None), bstack11111_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢᗼ"))
                bstack1lll11lll11_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack11111_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡵࡱࡦࡤࡸࡪࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࡽ࠳ࢁࠧᗽ").format(e))
try:
    from typing import Generator
    import pytest_playwright.pytest_playwright as p
    @pytest.fixture
    def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
        page = context.new_page()
        request.node._page = page
        yield page
except:
    pass
def pytest_addoption(parser):
    parser.addoption(bstack11111_opy_ (u"ࠤ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨᗾ"), default=bstack11111_opy_ (u"ࠥࡊࡦࡲࡳࡦࠤᗿ"), help=bstack11111_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡩࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠥᘀ"))
    parser.addoption(bstack11111_opy_ (u"ࠧ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦᘁ"), default=bstack11111_opy_ (u"ࠨࡆࡢ࡮ࡶࡩࠧᘂ"), help=bstack11111_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡪࡥࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠨᘃ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack11111_opy_ (u"ࠣ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠥᘄ"), action=bstack11111_opy_ (u"ࠤࡶࡸࡴࡸࡥࠣᘅ"), default=bstack11111_opy_ (u"ࠥࡧ࡭ࡸ࡯࡮ࡧࠥᘆ"),
                         help=bstack11111_opy_ (u"ࠦࡉࡸࡩࡷࡧࡵࠤࡹࡵࠠࡳࡷࡱࠤࡹ࡫ࡳࡵࡵࠥᘇ"))
def bstack1l111ll111_opy_(log):
    if not (log[bstack11111_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᘈ")] and log[bstack11111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᘉ")].strip()):
        return
    active = bstack1l111ll1l1_opy_()
    log = {
        bstack11111_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᘊ"): log[bstack11111_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᘋ")],
        bstack11111_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᘌ"): datetime.datetime.utcnow().isoformat() + bstack11111_opy_ (u"ࠪ࡞ࠬᘍ"),
        bstack11111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᘎ"): log[bstack11111_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᘏ")],
    }
    if active:
        if active[bstack11111_opy_ (u"࠭ࡴࡺࡲࡨࠫᘐ")] == bstack11111_opy_ (u"ࠧࡩࡱࡲ࡯ࠬᘑ"):
            log[bstack11111_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᘒ")] = active[bstack11111_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᘓ")]
        elif active[bstack11111_opy_ (u"ࠪࡸࡾࡶࡥࠨᘔ")] == bstack11111_opy_ (u"ࠫࡹ࡫ࡳࡵࠩᘕ"):
            log[bstack11111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᘖ")] = active[bstack11111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᘗ")]
    bstack11ll1l1l1_opy_.bstack1ll1l11l1l_opy_([log])
def bstack1l111ll1l1_opy_():
    if len(store[bstack11111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᘘ")]) > 0 and store[bstack11111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᘙ")][-1]:
        return {
            bstack11111_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᘚ"): bstack11111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨᘛ"),
            bstack11111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᘜ"): store[bstack11111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᘝ")][-1]
        }
    if store.get(bstack11111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪᘞ"), None):
        return {
            bstack11111_opy_ (u"ࠧࡵࡻࡳࡩࠬᘟ"): bstack11111_opy_ (u"ࠨࡶࡨࡷࡹ࠭ᘠ"),
            bstack11111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᘡ"): store[bstack11111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᘢ")]
        }
    return None
bstack11llllll1l_opy_ = bstack11lll1ll11_opy_(bstack1l111ll111_opy_)
def pytest_runtest_call(item):
    try:
        global CONFIG
        global bstack1lll1lll1l1_opy_
        item._1lll11ll11l_opy_ = True
        bstack1lll1lll11_opy_ = bstack1ll1l11ll1_opy_.bstack1l11l11ll_opy_(CONFIG, bstack11l1111l1l_opy_(item.own_markers))
        item._a11y_test_case = bstack1lll1lll11_opy_
        if bstack1lll1lll1l1_opy_:
            driver = getattr(item, bstack11111_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬᘣ"), None)
            item._a11y_started = bstack1ll1l11ll1_opy_.bstack1ll1l11111_opy_(driver, bstack1lll1lll11_opy_)
        if not bstack11ll1l1l1_opy_.on() or bstack1lll1ll111l_opy_ != bstack11111_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᘤ"):
            return
        global current_test_uuid, bstack11llllll1l_opy_
        bstack11llllll1l_opy_.start()
        bstack11lllll111_opy_ = {
            bstack11111_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᘥ"): uuid4().__str__(),
            bstack11111_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᘦ"): datetime.datetime.utcnow().isoformat() + bstack11111_opy_ (u"ࠨ࡜ࠪᘧ")
        }
        current_test_uuid = bstack11lllll111_opy_[bstack11111_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᘨ")]
        store[bstack11111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᘩ")] = bstack11lllll111_opy_[bstack11111_opy_ (u"ࠫࡺࡻࡩࡥࠩᘪ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _11llll1111_opy_[item.nodeid] = {**_11llll1111_opy_[item.nodeid], **bstack11lllll111_opy_}
        bstack1lll1l1l111_opy_(item, _11llll1111_opy_[item.nodeid], bstack11111_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᘫ"))
    except Exception as err:
        print(bstack11111_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡸࡵ࡯ࡶࡨࡷࡹࡥࡣࡢ࡮࡯࠾ࠥࢁࡽࠨᘬ"), str(err))
def pytest_runtest_setup(item):
    global bstack1lll1l111ll_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack11l1l11l1l_opy_():
        atexit.register(bstack111ll1lll_opy_)
        if not bstack1lll1l111ll_opy_:
            try:
                bstack1lll1l1111l_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack11l1111ll1_opy_():
                    bstack1lll1l1111l_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1lll1l1111l_opy_:
                    signal.signal(s, bstack1lll11ll1ll_opy_)
                bstack1lll1l111ll_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack11111_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡵࡩ࡬࡯ࡳࡵࡧࡵࠤࡸ࡯ࡧ࡯ࡣ࡯ࠤ࡭ࡧ࡮ࡥ࡮ࡨࡶࡸࡀࠠࠣᘭ") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1lllllllll1_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack11111_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᘮ")
    try:
        if not bstack11ll1l1l1_opy_.on():
            return
        bstack11llllll1l_opy_.start()
        uuid = uuid4().__str__()
        bstack11lllll111_opy_ = {
            bstack11111_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᘯ"): uuid,
            bstack11111_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᘰ"): datetime.datetime.utcnow().isoformat() + bstack11111_opy_ (u"ࠫ࡟࠭ᘱ"),
            bstack11111_opy_ (u"ࠬࡺࡹࡱࡧࠪᘲ"): bstack11111_opy_ (u"࠭ࡨࡰࡱ࡮ࠫᘳ"),
            bstack11111_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪᘴ"): bstack11111_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭ᘵ"),
            bstack11111_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬᘶ"): bstack11111_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᘷ")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack11111_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨᘸ")] = item
        store[bstack11111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᘹ")] = [uuid]
        if not _11llll1111_opy_.get(item.nodeid, None):
            _11llll1111_opy_[item.nodeid] = {bstack11111_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᘺ"): [], bstack11111_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩᘻ"): []}
        _11llll1111_opy_[item.nodeid][bstack11111_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᘼ")].append(bstack11lllll111_opy_[bstack11111_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᘽ")])
        _11llll1111_opy_[item.nodeid + bstack11111_opy_ (u"ࠪ࠱ࡸ࡫ࡴࡶࡲࠪᘾ")] = bstack11lllll111_opy_
        bstack1lll11ll1l1_opy_(item, bstack11lllll111_opy_, bstack11111_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᘿ"))
    except Exception as err:
        print(bstack11111_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡷࡻ࡮ࡵࡧࡶࡸࡤࡹࡥࡵࡷࡳ࠾ࠥࢁࡽࠨᙀ"), str(err))
def pytest_runtest_teardown(item):
    try:
        global bstack1lll11l1l_opy_
        if CONFIG.get(bstack11111_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬᙁ"), False):
            if CONFIG.get(bstack11111_opy_ (u"ࠧࡱࡧࡵࡧࡾࡉࡡࡱࡶࡸࡶࡪࡓ࡯ࡥࡧࠪᙂ"), bstack11111_opy_ (u"ࠣࡣࡸࡸࡴࠨᙃ")) == bstack11111_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦᙄ"):
                bstack1lll11lllll_opy_ = bstack1ll1l11ll_opy_(threading.current_thread(), bstack11111_opy_ (u"ࠪࡴࡪࡸࡣࡺࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᙅ"), None)
                bstack1lll1l1ll1_opy_ = bstack1lll11lllll_opy_ + bstack11111_opy_ (u"ࠦ࠲ࡺࡥࡴࡶࡦࡥࡸ࡫ࠢᙆ")
                driver = getattr(item, bstack11111_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭ᙇ"), None)
                PercySDK.screenshot(driver, bstack1lll1l1ll1_opy_)
        if getattr(item, bstack11111_opy_ (u"࠭࡟ࡢ࠳࠴ࡽࡤࡹࡴࡢࡴࡷࡩࡩ࠭ᙈ"), False):
            bstack1l1lllll_opy_.bstack1l1lll11l1_opy_(getattr(item, bstack11111_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨᙉ"), None), bstack1lll11l1l_opy_, logger, item)
        if not bstack11ll1l1l1_opy_.on():
            return
        bstack11lllll111_opy_ = {
            bstack11111_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᙊ"): uuid4().__str__(),
            bstack11111_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᙋ"): datetime.datetime.utcnow().isoformat() + bstack11111_opy_ (u"ࠪ࡞ࠬᙌ"),
            bstack11111_opy_ (u"ࠫࡹࡿࡰࡦࠩᙍ"): bstack11111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᙎ"),
            bstack11111_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᙏ"): bstack11111_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫᙐ"),
            bstack11111_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫᙑ"): bstack11111_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫᙒ")
        }
        _11llll1111_opy_[item.nodeid + bstack11111_opy_ (u"ࠪ࠱ࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ᙓ")] = bstack11lllll111_opy_
        bstack1lll11ll1l1_opy_(item, bstack11lllll111_opy_, bstack11111_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᙔ"))
    except Exception as err:
        print(bstack11111_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡷࡻ࡮ࡵࡧࡶࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࠺ࠡࡽࢀࠫᙕ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack11ll1l1l1_opy_.on():
        yield
        return
    start_time = datetime.datetime.now()
    if bstack1llllll1l1l_opy_(fixturedef.argname):
        store[bstack11111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡪࡶࡨࡱࠬᙖ")] = request.node
    elif bstack111111111l_opy_(fixturedef.argname):
        store[bstack11111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡥ࡯ࡥࡸࡹ࡟ࡪࡶࡨࡱࠬᙗ")] = request.node
    outcome = yield
    try:
        fixture = {
            bstack11111_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᙘ"): fixturedef.argname,
            bstack11111_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᙙ"): bstack11l111lll1_opy_(outcome),
            bstack11111_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬᙚ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack11111_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨᙛ")]
        if not _11llll1111_opy_.get(current_test_item.nodeid, None):
            _11llll1111_opy_[current_test_item.nodeid] = {bstack11111_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧᙜ"): []}
        _11llll1111_opy_[current_test_item.nodeid][bstack11111_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨᙝ")].append(fixture)
    except Exception as err:
        logger.debug(bstack11111_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡴࡧࡷࡹࡵࡀࠠࡼࡿࠪᙞ"), str(err))
if bstack1ll1l11l1_opy_() and bstack11ll1l1l1_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _11llll1111_opy_[request.node.nodeid][bstack11111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᙟ")].bstack1lllll11111_opy_(id(step))
        except Exception as err:
            print(bstack11111_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲ࠽ࠤࢀࢃࠧᙠ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _11llll1111_opy_[request.node.nodeid][bstack11111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᙡ")].bstack1l11l11l1l_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack11111_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡴࡶࡨࡴࡤ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠨᙢ"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack1l1111111l_opy_: bstack1l1111lll1_opy_ = _11llll1111_opy_[request.node.nodeid][bstack11111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᙣ")]
            bstack1l1111111l_opy_.bstack1l11l11l1l_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack11111_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡶࡸࡪࡶ࡟ࡦࡴࡵࡳࡷࡀࠠࡼࡿࠪᙤ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1lll1ll111l_opy_
        try:
            if not bstack11ll1l1l1_opy_.on() or bstack1lll1ll111l_opy_ != bstack11111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫᙥ"):
                return
            global bstack11llllll1l_opy_
            bstack11llllll1l_opy_.start()
            if not _11llll1111_opy_.get(request.node.nodeid, None):
                _11llll1111_opy_[request.node.nodeid] = {}
            bstack1l1111111l_opy_ = bstack1l1111lll1_opy_.bstack1llll1l1l1l_opy_(
                scenario, feature, request.node,
                name=bstack1111111111_opy_(request.node, scenario),
                bstack1l111lll1l_opy_=bstack11l1111l1_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack11111_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴ࠮ࡥࡸࡧࡺࡳࡢࡦࡴࠪᙦ"),
                tags=bstack1llllllll1l_opy_(feature, scenario)
            )
            _11llll1111_opy_[request.node.nodeid][bstack11111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᙧ")] = bstack1l1111111l_opy_
            bstack1lll1ll1lll_opy_(bstack1l1111111l_opy_.uuid)
            bstack11ll1l1l1_opy_.bstack11llllllll_opy_(bstack11111_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᙨ"), bstack1l1111111l_opy_)
        except Exception as err:
            print(bstack11111_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰ࠼ࠣࡿࢂ࠭ᙩ"), str(err))
def bstack1lll1ll1l11_opy_(bstack1lll1l111l1_opy_):
    if bstack1lll1l111l1_opy_ in store[bstack11111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᙪ")]:
        store[bstack11111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᙫ")].remove(bstack1lll1l111l1_opy_)
def bstack1lll1ll1lll_opy_(bstack1lll1l1l1ll_opy_):
    store[bstack11111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᙬ")] = bstack1lll1l1l1ll_opy_
    threading.current_thread().current_test_uuid = bstack1lll1l1l1ll_opy_
@bstack11ll1l1l1_opy_.bstack1llll111l1l_opy_
def bstack1lll1l11ll1_opy_(item, call, report):
    global bstack1lll1ll111l_opy_
    bstack1ll11ll1ll_opy_ = bstack11l1111l1_opy_()
    if hasattr(report, bstack11111_opy_ (u"ࠨࡵࡷࡳࡵ࠭᙭")):
        bstack1ll11ll1ll_opy_ = bstack11l11l11l1_opy_(report.stop)
    if hasattr(report, bstack11111_opy_ (u"ࠩࡶࡸࡦࡸࡴࠨ᙮")):
        bstack1ll11ll1ll_opy_ = bstack11l11l11l1_opy_(report.start)
    try:
        if getattr(report, bstack11111_opy_ (u"ࠪࡻ࡭࡫࡮ࠨᙯ"), bstack11111_opy_ (u"ࠫࠬᙰ")) == bstack11111_opy_ (u"ࠬࡩࡡ࡭࡮ࠪᙱ"):
            bstack11llllll1l_opy_.reset()
        if getattr(report, bstack11111_opy_ (u"࠭ࡷࡩࡧࡱࠫᙲ"), bstack11111_opy_ (u"ࠧࠨᙳ")) == bstack11111_opy_ (u"ࠨࡥࡤࡰࡱ࠭ᙴ"):
            if bstack1lll1ll111l_opy_ == bstack11111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᙵ"):
                _11llll1111_opy_[item.nodeid][bstack11111_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᙶ")] = bstack1ll11ll1ll_opy_
                bstack1lll1l1l111_opy_(item, _11llll1111_opy_[item.nodeid], bstack11111_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᙷ"), report, call)
                store[bstack11111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᙸ")] = None
            elif bstack1lll1ll111l_opy_ == bstack11111_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥᙹ"):
                bstack1l1111111l_opy_ = _11llll1111_opy_[item.nodeid][bstack11111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᙺ")]
                bstack1l1111111l_opy_.set(hooks=_11llll1111_opy_[item.nodeid].get(bstack11111_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᙻ"), []))
                exception, bstack11lllll1ll_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack11lllll1ll_opy_ = [call.excinfo.exconly(), getattr(report, bstack11111_opy_ (u"ࠩ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠨᙼ"), bstack11111_opy_ (u"ࠪࠫᙽ"))]
                bstack1l1111111l_opy_.stop(time=bstack1ll11ll1ll_opy_, result=Result(result=getattr(report, bstack11111_opy_ (u"ࠫࡴࡻࡴࡤࡱࡰࡩࠬᙾ"), bstack11111_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᙿ")), exception=exception, bstack11lllll1ll_opy_=bstack11lllll1ll_opy_))
                bstack11ll1l1l1_opy_.bstack11llllllll_opy_(bstack11111_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ "), _11llll1111_opy_[item.nodeid][bstack11111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᚁ")])
        elif getattr(report, bstack11111_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭ᚂ"), bstack11111_opy_ (u"ࠩࠪᚃ")) in [bstack11111_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᚄ"), bstack11111_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ᚅ")]:
            bstack1l111l1l11_opy_ = item.nodeid + bstack11111_opy_ (u"ࠬ࠳ࠧᚆ") + getattr(report, bstack11111_opy_ (u"࠭ࡷࡩࡧࡱࠫᚇ"), bstack11111_opy_ (u"ࠧࠨᚈ"))
            if getattr(report, bstack11111_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᚉ"), False):
                hook_type = bstack11111_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧᚊ") if getattr(report, bstack11111_opy_ (u"ࠪࡻ࡭࡫࡮ࠨᚋ"), bstack11111_opy_ (u"ࠫࠬᚌ")) == bstack11111_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᚍ") else bstack11111_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪᚎ")
                _11llll1111_opy_[bstack1l111l1l11_opy_] = {
                    bstack11111_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᚏ"): uuid4().__str__(),
                    bstack11111_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᚐ"): bstack1ll11ll1ll_opy_,
                    bstack11111_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᚑ"): hook_type
                }
            _11llll1111_opy_[bstack1l111l1l11_opy_][bstack11111_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᚒ")] = bstack1ll11ll1ll_opy_
            bstack1lll1ll1l11_opy_(_11llll1111_opy_[bstack1l111l1l11_opy_][bstack11111_opy_ (u"ࠫࡺࡻࡩࡥࠩᚓ")])
            bstack1lll11ll1l1_opy_(item, _11llll1111_opy_[bstack1l111l1l11_opy_], bstack11111_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᚔ"), report, call)
            if getattr(report, bstack11111_opy_ (u"࠭ࡷࡩࡧࡱࠫᚕ"), bstack11111_opy_ (u"ࠧࠨᚖ")) == bstack11111_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᚗ"):
                if getattr(report, bstack11111_opy_ (u"ࠩࡲࡹࡹࡩ࡯࡮ࡧࠪᚘ"), bstack11111_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᚙ")) == bstack11111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᚚ"):
                    bstack11lllll111_opy_ = {
                        bstack11111_opy_ (u"ࠬࡻࡵࡪࡦࠪ᚛"): uuid4().__str__(),
                        bstack11111_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ᚜"): bstack11l1111l1_opy_(),
                        bstack11111_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ᚝"): bstack11l1111l1_opy_()
                    }
                    _11llll1111_opy_[item.nodeid] = {**_11llll1111_opy_[item.nodeid], **bstack11lllll111_opy_}
                    bstack1lll1l1l111_opy_(item, _11llll1111_opy_[item.nodeid], bstack11111_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ᚞"))
                    bstack1lll1l1l111_opy_(item, _11llll1111_opy_[item.nodeid], bstack11111_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ᚟"), report, call)
    except Exception as err:
        print(bstack11111_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡥࡳࡪ࡬ࡦࡡࡲ࠵࠶ࡿ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷ࠾ࠥࢁࡽࠨᚠ"), str(err))
def bstack1lll1l11lll_opy_(test, bstack11lllll111_opy_, result=None, call=None, bstack1ll11lll_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack1l1111111l_opy_ = {
        bstack11111_opy_ (u"ࠫࡺࡻࡩࡥࠩᚡ"): bstack11lllll111_opy_[bstack11111_opy_ (u"ࠬࡻࡵࡪࡦࠪᚢ")],
        bstack11111_opy_ (u"࠭ࡴࡺࡲࡨࠫᚣ"): bstack11111_opy_ (u"ࠧࡵࡧࡶࡸࠬᚤ"),
        bstack11111_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᚥ"): test.name,
        bstack11111_opy_ (u"ࠩࡥࡳࡩࡿࠧᚦ"): {
            bstack11111_opy_ (u"ࠪࡰࡦࡴࡧࠨᚧ"): bstack11111_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫᚨ"),
            bstack11111_opy_ (u"ࠬࡩ࡯ࡥࡧࠪᚩ"): inspect.getsource(test.obj)
        },
        bstack11111_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᚪ"): test.name,
        bstack11111_opy_ (u"ࠧࡴࡥࡲࡴࡪ࠭ᚫ"): test.name,
        bstack11111_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨᚬ"): bstack11ll1l1l1_opy_.bstack1l11111ll1_opy_(test),
        bstack11111_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬᚭ"): file_path,
        bstack11111_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࠬᚮ"): file_path,
        bstack11111_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᚯ"): bstack11111_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭ᚰ"),
        bstack11111_opy_ (u"࠭ࡶࡤࡡࡩ࡭ࡱ࡫ࡰࡢࡶ࡫ࠫᚱ"): file_path,
        bstack11111_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᚲ"): bstack11lllll111_opy_[bstack11111_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᚳ")],
        bstack11111_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᚴ"): bstack11111_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪᚵ"),
        bstack11111_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡖࡪࡸࡵ࡯ࡒࡤࡶࡦࡳࠧᚶ"): {
            bstack11111_opy_ (u"ࠬࡸࡥࡳࡷࡱࡣࡳࡧ࡭ࡦࠩᚷ"): test.nodeid
        },
        bstack11111_opy_ (u"࠭ࡴࡢࡩࡶࠫᚸ"): bstack11l1111l1l_opy_(test.own_markers)
    }
    if bstack1ll11lll_opy_ in [bstack11111_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨᚹ"), bstack11111_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᚺ")]:
        bstack1l1111111l_opy_[bstack11111_opy_ (u"ࠩࡰࡩࡹࡧࠧᚻ")] = {
            bstack11111_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬᚼ"): bstack11lllll111_opy_.get(bstack11111_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭ᚽ"), [])
        }
    if bstack1ll11lll_opy_ == bstack11111_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭ᚾ"):
        bstack1l1111111l_opy_[bstack11111_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᚿ")] = bstack11111_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨᛀ")
        bstack1l1111111l_opy_[bstack11111_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᛁ")] = bstack11lllll111_opy_[bstack11111_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᛂ")]
        bstack1l1111111l_opy_[bstack11111_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᛃ")] = bstack11lllll111_opy_[bstack11111_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᛄ")]
    if result:
        bstack1l1111111l_opy_[bstack11111_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᛅ")] = result.outcome
        bstack1l1111111l_opy_[bstack11111_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧᛆ")] = result.duration * 1000
        bstack1l1111111l_opy_[bstack11111_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᛇ")] = bstack11lllll111_opy_[bstack11111_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᛈ")]
        if result.failed:
            bstack1l1111111l_opy_[bstack11111_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨᛉ")] = bstack11ll1l1l1_opy_.bstack11ll1lll11_opy_(call.excinfo.typename)
            bstack1l1111111l_opy_[bstack11111_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᛊ")] = bstack11ll1l1l1_opy_.bstack1lll1lll1ll_opy_(call.excinfo, result)
        bstack1l1111111l_opy_[bstack11111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᛋ")] = bstack11lllll111_opy_[bstack11111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᛌ")]
    if outcome:
        bstack1l1111111l_opy_[bstack11111_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᛍ")] = bstack11l111lll1_opy_(outcome)
        bstack1l1111111l_opy_[bstack11111_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨᛎ")] = 0
        bstack1l1111111l_opy_[bstack11111_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᛏ")] = bstack11lllll111_opy_[bstack11111_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᛐ")]
        if bstack1l1111111l_opy_[bstack11111_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᛑ")] == bstack11111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᛒ"):
            bstack1l1111111l_opy_[bstack11111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫᛓ")] = bstack11111_opy_ (u"࠭ࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠧᛔ")  # bstack1lll11ll111_opy_
            bstack1l1111111l_opy_[bstack11111_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨᛕ")] = [{bstack11111_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᛖ"): [bstack11111_opy_ (u"ࠩࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷ࠭ᛗ")]}]
        bstack1l1111111l_opy_[bstack11111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᛘ")] = bstack11lllll111_opy_[bstack11111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᛙ")]
    return bstack1l1111111l_opy_
def bstack1lll1l1ll1l_opy_(test, bstack1l111l11l1_opy_, bstack1ll11lll_opy_, result, call, outcome, bstack1lll1l11l1l_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack1l111l11l1_opy_[bstack11111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨᛚ")]
    hook_name = bstack1l111l11l1_opy_[bstack11111_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩᛛ")]
    hook_data = {
        bstack11111_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᛜ"): bstack1l111l11l1_opy_[bstack11111_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᛝ")],
        bstack11111_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᛞ"): bstack11111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨᛟ"),
        bstack11111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᛠ"): bstack11111_opy_ (u"ࠬࢁࡽࠨᛡ").format(bstack1lllllll111_opy_(hook_name)),
        bstack11111_opy_ (u"࠭ࡢࡰࡦࡼࠫᛢ"): {
            bstack11111_opy_ (u"ࠧ࡭ࡣࡱ࡫ࠬᛣ"): bstack11111_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨᛤ"),
            bstack11111_opy_ (u"ࠩࡦࡳࡩ࡫ࠧᛥ"): None
        },
        bstack11111_opy_ (u"ࠪࡷࡨࡵࡰࡦࠩᛦ"): test.name,
        bstack11111_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫᛧ"): bstack11ll1l1l1_opy_.bstack1l11111ll1_opy_(test, hook_name),
        bstack11111_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨᛨ"): file_path,
        bstack11111_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨᛩ"): file_path,
        bstack11111_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᛪ"): bstack11111_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ᛫"),
        bstack11111_opy_ (u"ࠩࡹࡧࡤ࡬ࡩ࡭ࡧࡳࡥࡹ࡮ࠧ᛬"): file_path,
        bstack11111_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ᛭"): bstack1l111l11l1_opy_[bstack11111_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᛮ")],
        bstack11111_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᛯ"): bstack11111_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠳ࡣࡶࡥࡸࡱࡧ࡫ࡲࠨᛰ") if bstack1lll1ll111l_opy_ == bstack11111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫᛱ") else bstack11111_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨᛲ"),
        bstack11111_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᛳ"): hook_type
    }
    bstack1lll1ll1111_opy_ = bstack1l11l1l111_opy_(_11llll1111_opy_.get(test.nodeid, None))
    if bstack1lll1ll1111_opy_:
        hook_data[bstack11111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤ࡯ࡤࠨᛴ")] = bstack1lll1ll1111_opy_
    if result:
        hook_data[bstack11111_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᛵ")] = result.outcome
        hook_data[bstack11111_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭ᛶ")] = result.duration * 1000
        hook_data[bstack11111_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᛷ")] = bstack1l111l11l1_opy_[bstack11111_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᛸ")]
        if result.failed:
            hook_data[bstack11111_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧ᛹")] = bstack11ll1l1l1_opy_.bstack11ll1lll11_opy_(call.excinfo.typename)
            hook_data[bstack11111_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪ᛺")] = bstack11ll1l1l1_opy_.bstack1lll1lll1ll_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack11111_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ᛻")] = bstack11l111lll1_opy_(outcome)
        hook_data[bstack11111_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬ᛼")] = 100
        hook_data[bstack11111_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ᛽")] = bstack1l111l11l1_opy_[bstack11111_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ᛾")]
        if hook_data[bstack11111_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ᛿")] == bstack11111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᜀ"):
            hook_data[bstack11111_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨᜁ")] = bstack11111_opy_ (u"࡙ࠪࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠫᜂ")  # bstack1lll11ll111_opy_
            hook_data[bstack11111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᜃ")] = [{bstack11111_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᜄ"): [bstack11111_opy_ (u"࠭ࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠪᜅ")]}]
    if bstack1lll1l11l1l_opy_:
        hook_data[bstack11111_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᜆ")] = bstack1lll1l11l1l_opy_.result
        hook_data[bstack11111_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩᜇ")] = bstack11l11l1lll_opy_(bstack1l111l11l1_opy_[bstack11111_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᜈ")], bstack1l111l11l1_opy_[bstack11111_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᜉ")])
        hook_data[bstack11111_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᜊ")] = bstack1l111l11l1_opy_[bstack11111_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᜋ")]
        if hook_data[bstack11111_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᜌ")] == bstack11111_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᜍ"):
            hook_data[bstack11111_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧᜎ")] = bstack11ll1l1l1_opy_.bstack11ll1lll11_opy_(bstack1lll1l11l1l_opy_.exception_type)
            hook_data[bstack11111_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᜏ")] = [{bstack11111_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᜐ"): bstack11l11l11ll_opy_(bstack1lll1l11l1l_opy_.exception)}]
    return hook_data
def bstack1lll1l1l111_opy_(test, bstack11lllll111_opy_, bstack1ll11lll_opy_, result=None, call=None, outcome=None):
    bstack1l1111111l_opy_ = bstack1lll1l11lll_opy_(test, bstack11lllll111_opy_, result, call, bstack1ll11lll_opy_, outcome)
    driver = getattr(test, bstack11111_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬᜑ"), None)
    if bstack1ll11lll_opy_ == bstack11111_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᜒ") and driver:
        bstack1l1111111l_opy_[bstack11111_opy_ (u"࠭ࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠬᜓ")] = bstack11ll1l1l1_opy_.bstack1l1111llll_opy_(driver)
    if bstack1ll11lll_opy_ == bstack11111_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨ᜔"):
        bstack1ll11lll_opy_ = bstack11111_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦ᜕ࠪ")
    bstack11llll1l11_opy_ = {
        bstack11111_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭᜖"): bstack1ll11lll_opy_,
        bstack11111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬ᜗"): bstack1l1111111l_opy_
    }
    bstack11ll1l1l1_opy_.bstack1l11l11111_opy_(bstack11llll1l11_opy_)
def bstack1lll11ll1l1_opy_(test, bstack11lllll111_opy_, bstack1ll11lll_opy_, result=None, call=None, outcome=None, bstack1lll1l11l1l_opy_=None):
    hook_data = bstack1lll1l1ll1l_opy_(test, bstack11lllll111_opy_, bstack1ll11lll_opy_, result, call, outcome, bstack1lll1l11l1l_opy_)
    bstack11llll1l11_opy_ = {
        bstack11111_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ᜘"): bstack1ll11lll_opy_,
        bstack11111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴࠧ᜙"): hook_data
    }
    bstack11ll1l1l1_opy_.bstack1l11l11111_opy_(bstack11llll1l11_opy_)
def bstack1l11l1l111_opy_(bstack11lllll111_opy_):
    if not bstack11lllll111_opy_:
        return None
    if bstack11lllll111_opy_.get(bstack11111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ᜚"), None):
        return getattr(bstack11lllll111_opy_[bstack11111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ᜛")], bstack11111_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭᜜"), None)
    return bstack11lllll111_opy_.get(bstack11111_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ᜝"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack11ll1l1l1_opy_.on():
            return
        places = [bstack11111_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ᜞"), bstack11111_opy_ (u"ࠫࡨࡧ࡬࡭ࠩᜟ"), bstack11111_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧᜠ")]
        bstack1l1111l11l_opy_ = []
        for bstack1lll1l1llll_opy_ in places:
            records = caplog.get_records(bstack1lll1l1llll_opy_)
            bstack1lll1lll111_opy_ = bstack11111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᜡ") if bstack1lll1l1llll_opy_ == bstack11111_opy_ (u"ࠧࡤࡣ࡯ࡰࠬᜢ") else bstack11111_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᜣ")
            bstack1lll1lll11l_opy_ = request.node.nodeid + (bstack11111_opy_ (u"ࠩࠪᜤ") if bstack1lll1l1llll_opy_ == bstack11111_opy_ (u"ࠪࡧࡦࡲ࡬ࠨᜥ") else bstack11111_opy_ (u"ࠫ࠲࠭ᜦ") + bstack1lll1l1llll_opy_)
            bstack1lll1l1l1ll_opy_ = bstack1l11l1l111_opy_(_11llll1111_opy_.get(bstack1lll1lll11l_opy_, None))
            if not bstack1lll1l1l1ll_opy_:
                continue
            for record in records:
                if bstack111lll1l11_opy_(record.message):
                    continue
                bstack1l1111l11l_opy_.append({
                    bstack11111_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨᜧ"): datetime.datetime.utcfromtimestamp(record.created).isoformat() + bstack11111_opy_ (u"࡚࠭ࠨᜨ"),
                    bstack11111_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᜩ"): record.levelname,
                    bstack11111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᜪ"): record.message,
                    bstack1lll1lll111_opy_: bstack1lll1l1l1ll_opy_
                })
        if len(bstack1l1111l11l_opy_) > 0:
            bstack11ll1l1l1_opy_.bstack1ll1l11l1l_opy_(bstack1l1111l11l_opy_)
    except Exception as err:
        print(bstack11111_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡧࡴࡴࡤࡠࡨ࡬ࡼࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭ᜫ"), str(err))
def bstack111111l1_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack11l1ll11l_opy_
    bstack1ll1l111l1_opy_ = bstack1ll1l11ll_opy_(threading.current_thread(), bstack11111_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧᜬ"), None) and bstack1ll1l11ll_opy_(
            threading.current_thread(), bstack11111_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᜭ"), None)
    bstack1l1l1llll1_opy_ = getattr(driver, bstack11111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬᜮ"), None) != None and getattr(driver, bstack11111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭ᜯ"), None) == True
    if sequence == bstack11111_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧᜰ") and driver != None:
      if not bstack11l1ll11l_opy_ and bstack111lll1lll_opy_() and bstack11111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᜱ") in CONFIG and CONFIG[bstack11111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᜲ")] == True and bstack1ll11l111_opy_.bstack1l1l1l111_opy_(driver_command) and (bstack1l1l1llll1_opy_ or bstack1ll1l111l1_opy_) and not bstack1llll1lll_opy_(args):
        try:
          bstack11l1ll11l_opy_ = True
          logger.debug(bstack11111_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥ࡬࡯ࡳࠢࡾࢁࠬᜳ").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack11111_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡧࡵࡪࡴࡸ࡭ࠡࡵࡦࡥࡳࠦࡻࡾ᜴ࠩ").format(str(err)))
        bstack11l1ll11l_opy_ = False
    if sequence == bstack11111_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫ᜵"):
        if driver_command == bstack11111_opy_ (u"࠭ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠪ᜶"):
            bstack11ll1l1l1_opy_.bstack11l1llll_opy_({
                bstack11111_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭᜷"): response[bstack11111_opy_ (u"ࠨࡸࡤࡰࡺ࡫ࠧ᜸")],
                bstack11111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ᜹"): store[bstack11111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ᜺")]
            })
def bstack111ll1lll_opy_():
    global bstack1l1ll1llll_opy_
    bstack1ll1l1l1_opy_.bstack1l1l1ll11_opy_()
    logging.shutdown()
    bstack11ll1l1l1_opy_.bstack1l11111lll_opy_()
    for driver in bstack1l1ll1llll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1lll11ll1ll_opy_(*args):
    global bstack1l1ll1llll_opy_
    bstack11ll1l1l1_opy_.bstack1l11111lll_opy_()
    for driver in bstack1l1ll1llll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1llll1ll1_opy_(self, *args, **kwargs):
    bstack1ll1ll111_opy_ = bstack1l1l1ll111_opy_(self, *args, **kwargs)
    bstack11ll1l1l1_opy_.bstack1ll11ll111_opy_(self)
    return bstack1ll1ll111_opy_
def bstack1l1lllll1l_opy_(framework_name):
    global bstack1l1l1lll1l_opy_
    global bstack11l11l1ll_opy_
    bstack1l1l1lll1l_opy_ = framework_name
    logger.info(bstack1lll1l1111_opy_.format(bstack1l1l1lll1l_opy_.split(bstack11111_opy_ (u"ࠫ࠲࠭᜻"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack111lll1lll_opy_():
            Service.start = bstack1ll1l11lll_opy_
            Service.stop = bstack111lll1l1_opy_
            webdriver.Remote.__init__ = bstack1l11ll1ll_opy_
            webdriver.Remote.get = bstack1lllll1l1_opy_
            if not isinstance(os.getenv(bstack11111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡇࡒࡂࡎࡏࡉࡑ࠭᜼")), str):
                return
            WebDriver.close = bstack1ll11111l_opy_
            WebDriver.quit = bstack1l11ll1l11_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        if not bstack111lll1lll_opy_() and bstack11ll1l1l1_opy_.on():
            webdriver.Remote.__init__ = bstack1llll1ll1_opy_
        bstack11l11l1ll_opy_ = True
    except Exception as e:
        pass
    bstack1lllll111_opy_()
    if os.environ.get(bstack11111_opy_ (u"࠭ࡓࡆࡎࡈࡒࡎ࡛ࡍࡠࡑࡕࡣࡕࡒࡁ࡚࡙ࡕࡍࡌࡎࡔࡠࡋࡑࡗ࡙ࡇࡌࡍࡇࡇࠫ᜽")):
        bstack11l11l1ll_opy_ = eval(os.environ.get(bstack11111_opy_ (u"ࠧࡔࡇࡏࡉࡓࡏࡕࡎࡡࡒࡖࡤࡖࡌࡂ࡛࡚ࡖࡎࡍࡈࡕࡡࡌࡒࡘ࡚ࡁࡍࡎࡈࡈࠬ᜾")))
    if not bstack11l11l1ll_opy_:
        bstack1l1lll1111_opy_(bstack11111_opy_ (u"ࠣࡒࡤࡧࡰࡧࡧࡦࡵࠣࡲࡴࡺࠠࡪࡰࡶࡸࡦࡲ࡬ࡦࡦࠥ᜿"), bstack1ll1ll1l11_opy_)
    if bstack1l11lllll_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._get_proxy_url = bstack1lll11lll_opy_
        except Exception as e:
            logger.error(bstack1l11l1ll1_opy_.format(str(e)))
    if bstack11111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᝀ") in str(framework_name).lower():
        if not bstack111lll1lll_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack111ll11ll_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1l11111l1_opy_
            Config.getoption = bstack1ll111ll1l_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1llll11l1l_opy_
        except Exception as e:
            pass
def bstack1l11ll1l11_opy_(self):
    global bstack1l1l1lll1l_opy_
    global bstack1ll11l1ll1_opy_
    global bstack1ll11ll11_opy_
    try:
        if bstack11111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᝁ") in bstack1l1l1lll1l_opy_ and self.session_id != None and bstack1ll1l11ll_opy_(threading.current_thread(), bstack11111_opy_ (u"ࠫࡹ࡫ࡳࡵࡕࡷࡥࡹࡻࡳࠨᝂ"), bstack11111_opy_ (u"ࠬ࠭ᝃ")) != bstack11111_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᝄ"):
            bstack11l1111l_opy_ = bstack11111_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᝅ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᝆ")
            bstack111l1llll_opy_(logger, True)
            if self != None:
                bstack1ll1l1111_opy_(self, bstack11l1111l_opy_, bstack11111_opy_ (u"ࠩ࠯ࠤࠬᝇ").join(threading.current_thread().bstackTestErrorMessages))
        item = store.get(bstack11111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧᝈ"), None)
        if item is not None and bstack1lll1lll1l1_opy_:
            bstack1l1lllll_opy_.bstack1l1lll11l1_opy_(self, bstack1lll11l1l_opy_, logger, item)
        threading.current_thread().testStatus = bstack11111_opy_ (u"ࠫࠬᝉ")
    except Exception as e:
        logger.debug(bstack11111_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࠨᝊ") + str(e))
    bstack1ll11ll11_opy_(self)
    self.session_id = None
def bstack1l11ll1ll_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1ll11l1ll1_opy_
    global bstack111lll11l_opy_
    global bstack1l1lll11_opy_
    global bstack1l1l1lll1l_opy_
    global bstack1l1l1ll111_opy_
    global bstack1l1ll1llll_opy_
    global bstack1l1l11llll_opy_
    global bstack1llll1ll_opy_
    global bstack1lll1lll1l1_opy_
    global bstack1lll11l1l_opy_
    CONFIG[bstack11111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨᝋ")] = str(bstack1l1l1lll1l_opy_) + str(__version__)
    command_executor = bstack1l11111ll_opy_(bstack1l1l11llll_opy_)
    logger.debug(bstack1ll1l111l_opy_.format(command_executor))
    proxy = bstack1l11l111l_opy_(CONFIG, proxy)
    bstack11lll1ll_opy_ = 0
    try:
        if bstack1l1lll11_opy_ is True:
            bstack11lll1ll_opy_ = int(os.environ.get(bstack11111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᝌ")))
    except:
        bstack11lll1ll_opy_ = 0
    bstack1lll11ll_opy_ = bstack1llll111l1_opy_(CONFIG, bstack11lll1ll_opy_)
    logger.debug(bstack1111l1111_opy_.format(str(bstack1lll11ll_opy_)))
    bstack1lll11l1l_opy_ = CONFIG.get(bstack11111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᝍ"))[bstack11lll1ll_opy_]
    if bstack11111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᝎ") in CONFIG and CONFIG[bstack11111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧᝏ")]:
        bstack1l1ll1lll1_opy_(bstack1lll11ll_opy_, bstack1llll1ll_opy_)
    if desired_capabilities:
        bstack1lll1lll1l_opy_ = bstack1l1l1l111l_opy_(desired_capabilities)
        bstack1lll1lll1l_opy_[bstack11111_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫᝐ")] = bstack1ll11111_opy_(CONFIG)
        bstack1ll1l11l11_opy_ = bstack1llll111l1_opy_(bstack1lll1lll1l_opy_)
        if bstack1ll1l11l11_opy_:
            bstack1lll11ll_opy_ = update(bstack1ll1l11l11_opy_, bstack1lll11ll_opy_)
        desired_capabilities = None
    if options:
        bstack1l11lll11_opy_(options, bstack1lll11ll_opy_)
    if not options:
        options = bstack1ll1llll11_opy_(bstack1lll11ll_opy_)
    if bstack1ll1l11ll1_opy_.bstack1l1l1111l_opy_(CONFIG, bstack11lll1ll_opy_) and bstack1ll1l11ll1_opy_.bstack11lll1l1l_opy_(bstack1lll11ll_opy_, options):
        bstack1lll1lll1l1_opy_ = True
        bstack1ll1l11ll1_opy_.set_capabilities(bstack1lll11ll_opy_, CONFIG)
    if proxy and bstack1l1lll111l_opy_() >= version.parse(bstack11111_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬᝑ")):
        options.proxy(proxy)
    if options and bstack1l1lll111l_opy_() >= version.parse(bstack11111_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬᝒ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1l1lll111l_opy_() < version.parse(bstack11111_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ᝓ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1lll11ll_opy_)
    logger.info(bstack1l1l11111l_opy_)
    if bstack1l1lll111l_opy_() >= version.parse(bstack11111_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨ᝔")):
        bstack1l1l1ll111_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1l1lll111l_opy_() >= version.parse(bstack11111_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ᝕")):
        bstack1l1l1ll111_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1l1lll111l_opy_() >= version.parse(bstack11111_opy_ (u"ࠪ࠶࠳࠻࠳࠯࠲ࠪ᝖")):
        bstack1l1l1ll111_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack1l1l1ll111_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack1llll1l1l1_opy_ = bstack11111_opy_ (u"ࠫࠬ᝗")
        if bstack1l1lll111l_opy_() >= version.parse(bstack11111_opy_ (u"ࠬ࠺࠮࠱࠰࠳ࡦ࠶࠭᝘")):
            bstack1llll1l1l1_opy_ = self.caps.get(bstack11111_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨ᝙"))
        else:
            bstack1llll1l1l1_opy_ = self.capabilities.get(bstack11111_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢ᝚"))
        if bstack1llll1l1l1_opy_:
            bstack1lll111ll1_opy_(bstack1llll1l1l1_opy_)
            if bstack1l1lll111l_opy_() <= version.parse(bstack11111_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨ᝛")):
                self.command_executor._url = bstack11111_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ᝜") + bstack1l1l11llll_opy_ + bstack11111_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢ᝝")
            else:
                self.command_executor._url = bstack11111_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨ᝞") + bstack1llll1l1l1_opy_ + bstack11111_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨ᝟")
            logger.debug(bstack1l1l11ll11_opy_.format(bstack1llll1l1l1_opy_))
        else:
            logger.debug(bstack1lllllllll_opy_.format(bstack11111_opy_ (u"ࠨࡏࡱࡶ࡬ࡱࡦࡲࠠࡉࡷࡥࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢᝠ")))
    except Exception as e:
        logger.debug(bstack1lllllllll_opy_.format(e))
    bstack1ll11l1ll1_opy_ = self.session_id
    if bstack11111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᝡ") in bstack1l1l1lll1l_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack11111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬᝢ"), None)
        if item:
            bstack1lll1l1l11l_opy_ = getattr(item, bstack11111_opy_ (u"ࠩࡢࡸࡪࡹࡴࡠࡥࡤࡷࡪࡥࡳࡵࡣࡵࡸࡪࡪࠧᝣ"), False)
            if not getattr(item, bstack11111_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫᝤ"), None) and bstack1lll1l1l11l_opy_:
                setattr(store[bstack11111_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨᝥ")], bstack11111_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭ᝦ"), self)
        bstack11ll1l1l1_opy_.bstack1ll11ll111_opy_(self)
    bstack1l1ll1llll_opy_.append(self)
    if bstack11111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᝧ") in CONFIG and bstack11111_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᝨ") in CONFIG[bstack11111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᝩ")][bstack11lll1ll_opy_]:
        bstack111lll11l_opy_ = CONFIG[bstack11111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᝪ")][bstack11lll1ll_opy_][bstack11111_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᝫ")]
    logger.debug(bstack1ll1l111_opy_.format(bstack1ll11l1ll1_opy_))
def bstack1lllll1l1_opy_(self, url):
    global bstack1l1ll1l111_opy_
    global CONFIG
    try:
        bstack1llll1l11_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1l1l11lll_opy_.format(str(err)))
    try:
        bstack1l1ll1l111_opy_(self, url)
    except Exception as e:
        try:
            bstack11ll1111l_opy_ = str(e)
            if any(err_msg in bstack11ll1111l_opy_ for err_msg in bstack11111lll_opy_):
                bstack1llll1l11_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1l1l11lll_opy_.format(str(err)))
        raise e
def bstack1lll1111_opy_(item, when):
    global bstack1ll1lll111_opy_
    try:
        bstack1ll1lll111_opy_(item, when)
    except Exception as e:
        pass
def bstack1llll11l1l_opy_(item, call, rep):
    global bstack1l1111l1l_opy_
    global bstack1l1ll1llll_opy_
    name = bstack11111_opy_ (u"ࠫࠬᝬ")
    try:
        if rep.when == bstack11111_opy_ (u"ࠬࡩࡡ࡭࡮ࠪ᝭"):
            bstack1ll11l1ll1_opy_ = threading.current_thread().bstackSessionId
            bstack1lll1l11l11_opy_ = item.config.getoption(bstack11111_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᝮ"))
            try:
                if (str(bstack1lll1l11l11_opy_).lower() != bstack11111_opy_ (u"ࠧࡵࡴࡸࡩࠬᝯ")):
                    name = str(rep.nodeid)
                    bstack11llll11_opy_ = bstack1l1llllll1_opy_(bstack11111_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩᝰ"), name, bstack11111_opy_ (u"ࠩࠪ᝱"), bstack11111_opy_ (u"ࠪࠫᝲ"), bstack11111_opy_ (u"ࠫࠬᝳ"), bstack11111_opy_ (u"ࠬ࠭᝴"))
                    os.environ[bstack11111_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩ᝵")] = name
                    for driver in bstack1l1ll1llll_opy_:
                        if bstack1ll11l1ll1_opy_ == driver.session_id:
                            driver.execute_script(bstack11llll11_opy_)
            except Exception as e:
                logger.debug(bstack11111_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧ᝶").format(str(e)))
            try:
                bstack1llllllll1_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack11111_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ᝷"):
                    status = bstack11111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ᝸") if rep.outcome.lower() == bstack11111_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ᝹") else bstack11111_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ᝺")
                    reason = bstack11111_opy_ (u"ࠬ࠭᝻")
                    if status == bstack11111_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭᝼"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack11111_opy_ (u"ࠧࡪࡰࡩࡳࠬ᝽") if status == bstack11111_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ᝾") else bstack11111_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ᝿")
                    data = name + bstack11111_opy_ (u"ࠪࠤࡵࡧࡳࡴࡧࡧࠥࠬក") if status == bstack11111_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫខ") else name + bstack11111_opy_ (u"ࠬࠦࡦࡢ࡫࡯ࡩࡩࠧࠠࠨគ") + reason
                    bstack11lll1111_opy_ = bstack1l1llllll1_opy_(bstack11111_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨឃ"), bstack11111_opy_ (u"ࠧࠨង"), bstack11111_opy_ (u"ࠨࠩច"), bstack11111_opy_ (u"ࠩࠪឆ"), level, data)
                    for driver in bstack1l1ll1llll_opy_:
                        if bstack1ll11l1ll1_opy_ == driver.session_id:
                            driver.execute_script(bstack11lll1111_opy_)
            except Exception as e:
                logger.debug(bstack11111_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡤࡱࡱࡸࡪࡾࡴࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧជ").format(str(e)))
    except Exception as e:
        logger.debug(bstack11111_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡶࡤࡸࡪࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࢁࡽࠨឈ").format(str(e)))
    bstack1l1111l1l_opy_(item, call, rep)
notset = Notset()
def bstack1ll111ll1l_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1lll1lll_opy_
    if str(name).lower() == bstack11111_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࠬញ"):
        return bstack11111_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧដ")
    else:
        return bstack1lll1lll_opy_(self, name, default, skip)
def bstack1lll11lll_opy_(self):
    global CONFIG
    global bstack1l111111l_opy_
    try:
        proxy = bstack1lll11l1ll_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack11111_opy_ (u"ࠧ࠯ࡲࡤࡧࠬឋ")):
                proxies = bstack1ll1lll1ll_opy_(proxy, bstack1l11111ll_opy_())
                if len(proxies) > 0:
                    protocol, bstack1l111ll1l_opy_ = proxies.popitem()
                    if bstack11111_opy_ (u"ࠣ࠼࠲࠳ࠧឌ") in bstack1l111ll1l_opy_:
                        return bstack1l111ll1l_opy_
                    else:
                        return bstack11111_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥឍ") + bstack1l111ll1l_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack11111_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡰࡳࡱࡻࡽࠥࡻࡲ࡭ࠢ࠽ࠤࢀࢃࠢណ").format(str(e)))
    return bstack1l111111l_opy_(self)
def bstack1l11lllll_opy_():
    return (bstack11111_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧត") in CONFIG or bstack11111_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩថ") in CONFIG) and bstack1ll111l11l_opy_() and bstack1l1lll111l_opy_() >= version.parse(
        bstack1l11l1lll1_opy_)
def bstack1l1lll1ll_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack111lll11l_opy_
    global bstack1l1lll11_opy_
    global bstack1l1l1lll1l_opy_
    CONFIG[bstack11111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨទ")] = str(bstack1l1l1lll1l_opy_) + str(__version__)
    bstack11lll1ll_opy_ = 0
    try:
        if bstack1l1lll11_opy_ is True:
            bstack11lll1ll_opy_ = int(os.environ.get(bstack11111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧធ")))
    except:
        bstack11lll1ll_opy_ = 0
    CONFIG[bstack11111_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢន")] = True
    bstack1lll11ll_opy_ = bstack1llll111l1_opy_(CONFIG, bstack11lll1ll_opy_)
    logger.debug(bstack1111l1111_opy_.format(str(bstack1lll11ll_opy_)))
    if CONFIG.get(bstack11111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ប")):
        bstack1l1ll1lll1_opy_(bstack1lll11ll_opy_, bstack1llll1ll_opy_)
    if bstack11111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ផ") in CONFIG and bstack11111_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩព") in CONFIG[bstack11111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨភ")][bstack11lll1ll_opy_]:
        bstack111lll11l_opy_ = CONFIG[bstack11111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩម")][bstack11lll1ll_opy_][bstack11111_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬយ")]
    import urllib
    import json
    bstack11l1l11l_opy_ = bstack11111_opy_ (u"ࠨࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࠪរ") + urllib.parse.quote(json.dumps(bstack1lll11ll_opy_))
    browser = self.connect(bstack11l1l11l_opy_)
    return browser
def bstack1lllll111_opy_():
    global bstack11l11l1ll_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1l1lll1ll_opy_
        bstack11l11l1ll_opy_ = True
    except Exception as e:
        pass
def bstack1lll11llll1_opy_():
    global CONFIG
    global bstack1111l1l11_opy_
    global bstack1l1l11llll_opy_
    global bstack1llll1ll_opy_
    global bstack1l1lll11_opy_
    global bstack11l111l1_opy_
    CONFIG = json.loads(os.environ.get(bstack11111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࠨល")))
    bstack1111l1l11_opy_ = eval(os.environ.get(bstack11111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫវ")))
    bstack1l1l11llll_opy_ = os.environ.get(bstack11111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡌ࡚ࡈ࡟ࡖࡔࡏࠫឝ"))
    bstack1111lll11_opy_(CONFIG, bstack1111l1l11_opy_)
    bstack11l111l1_opy_ = bstack1ll1l1l1_opy_.bstack1l111llll_opy_(CONFIG, bstack11l111l1_opy_)
    global bstack1l1l1ll111_opy_
    global bstack1ll11ll11_opy_
    global bstack1lll1l11l1_opy_
    global bstack1ll11ll1_opy_
    global bstack1l1l111l1_opy_
    global bstack1l1l1l1111_opy_
    global bstack1llllll11_opy_
    global bstack1l1ll1l111_opy_
    global bstack1l111111l_opy_
    global bstack1lll1lll_opy_
    global bstack1ll1lll111_opy_
    global bstack1l1111l1l_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1l1l1ll111_opy_ = webdriver.Remote.__init__
        bstack1ll11ll11_opy_ = WebDriver.quit
        bstack1llllll11_opy_ = WebDriver.close
        bstack1l1ll1l111_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack11111_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨឞ") in CONFIG or bstack11111_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪស") in CONFIG) and bstack1ll111l11l_opy_():
        if bstack1l1lll111l_opy_() < version.parse(bstack1l11l1lll1_opy_):
            logger.error(bstack11l1l1l11_opy_.format(bstack1l1lll111l_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack1l111111l_opy_ = RemoteConnection._get_proxy_url
            except Exception as e:
                logger.error(bstack1l11l1ll1_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1lll1lll_opy_ = Config.getoption
        from _pytest import runner
        bstack1ll1lll111_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack1l111l1l_opy_)
    try:
        from pytest_bdd import reporting
        bstack1l1111l1l_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack11111_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨហ"))
    bstack1llll1ll_opy_ = CONFIG.get(bstack11111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬឡ"), {}).get(bstack11111_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫអ"))
    bstack1l1lll11_opy_ = True
    bstack1l1lllll1l_opy_(bstack1llll1ll11_opy_)
if (bstack11l1l11l1l_opy_()):
    bstack1lll11llll1_opy_()
@bstack1l111ll1ll_opy_(class_method=False)
def bstack1lll1ll11ll_opy_(hook_name, event, bstack1lll1ll1l1l_opy_=None):
    if hook_name not in [bstack11111_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫឣ"), bstack11111_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨឤ"), bstack11111_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫឥ"), bstack11111_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨឦ"), bstack11111_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬឧ"), bstack11111_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩឨ"), bstack11111_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨឩ"), bstack11111_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬឪ")]:
        return
    node = store[bstack11111_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨឫ")]
    if hook_name in [bstack11111_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫឬ"), bstack11111_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨឭ")]:
        node = store[bstack11111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠ࡯ࡲࡨࡺࡲࡥࡠ࡫ࡷࡩࡲ࠭ឮ")]
    elif hook_name in [bstack11111_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭ឯ"), bstack11111_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪឰ")]:
        node = store[bstack11111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡨࡲࡡࡴࡵࡢ࡭ࡹ࡫࡭ࠨឱ")]
    if event == bstack11111_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫឲ"):
        hook_type = bstack1llllll1lll_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack1l111l11l1_opy_ = {
            bstack11111_opy_ (u"ࠬࡻࡵࡪࡦࠪឳ"): uuid,
            bstack11111_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ឴"): bstack11l1111l1_opy_(),
            bstack11111_opy_ (u"ࠧࡵࡻࡳࡩࠬ឵"): bstack11111_opy_ (u"ࠨࡪࡲࡳࡰ࠭ា"),
            bstack11111_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬិ"): hook_type,
            bstack11111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭ី"): hook_name
        }
        store[bstack11111_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨឹ")].append(uuid)
        bstack1lll1l1l1l1_opy_ = node.nodeid
        if hook_type == bstack11111_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪឺ"):
            if not _11llll1111_opy_.get(bstack1lll1l1l1l1_opy_, None):
                _11llll1111_opy_[bstack1lll1l1l1l1_opy_] = {bstack11111_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬុ"): []}
            _11llll1111_opy_[bstack1lll1l1l1l1_opy_][bstack11111_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ូ")].append(bstack1l111l11l1_opy_[bstack11111_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ួ")])
        _11llll1111_opy_[bstack1lll1l1l1l1_opy_ + bstack11111_opy_ (u"ࠩ࠰ࠫើ") + hook_name] = bstack1l111l11l1_opy_
        bstack1lll11ll1l1_opy_(node, bstack1l111l11l1_opy_, bstack11111_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫឿ"))
    elif event == bstack11111_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪៀ"):
        bstack1l111l1l11_opy_ = node.nodeid + bstack11111_opy_ (u"ࠬ࠳ࠧេ") + hook_name
        _11llll1111_opy_[bstack1l111l1l11_opy_][bstack11111_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫែ")] = bstack11l1111l1_opy_()
        bstack1lll1ll1l11_opy_(_11llll1111_opy_[bstack1l111l1l11_opy_][bstack11111_opy_ (u"ࠧࡶࡷ࡬ࡨࠬៃ")])
        bstack1lll11ll1l1_opy_(node, _11llll1111_opy_[bstack1l111l1l11_opy_], bstack11111_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪោ"), bstack1lll1l11l1l_opy_=bstack1lll1ll1l1l_opy_)
def bstack1lll11lll1l_opy_():
    global bstack1lll1ll111l_opy_
    if bstack1ll1l11l1_opy_():
        bstack1lll1ll111l_opy_ = bstack11111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭ៅ")
    else:
        bstack1lll1ll111l_opy_ = bstack11111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪំ")
@bstack11ll1l1l1_opy_.bstack1llll111l1l_opy_
def bstack1lll1l1ll11_opy_():
    bstack1lll11lll1l_opy_()
    if bstack1ll111l11l_opy_():
        bstack1ll11l1ll_opy_(bstack111111l1_opy_)
    bstack111ll1l11l_opy_ = bstack111ll1l111_opy_(bstack1lll1ll11ll_opy_)
bstack1lll1l1ll11_opy_()