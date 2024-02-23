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
import os
import signal
import sys
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
import multiprocessing
import traceback
import copy
import tempfile
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from bstack_utils.constants import *
from bstack_utils.percy import *
from browserstack_sdk.bstack1llllll1l1_opy_ import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack1l1ll1ll1l_opy_ import bstack111lll11_opy_
import time
import requests
def bstack1l1llll11l_opy_():
  global CONFIG
  headers = {
        bstack11111_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack11111_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack1lll1ll1l1_opy_(CONFIG, bstack1ll11l11l1_opy_)
  try:
    response = requests.get(bstack1ll11l11l1_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack111lll1ll_opy_ = response.json()[bstack11111_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack11ll11ll_opy_.format(response.json()))
      return bstack111lll1ll_opy_
    else:
      logger.debug(bstack11ll1l11l_opy_.format(bstack11111_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack11ll1l11l_opy_.format(e))
def bstack1l1lll1l_opy_(hub_url):
  global CONFIG
  url = bstack11111_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack11111_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack11111_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack11111_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack1lll1ll1l1_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack111llll1l_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1l1l1lll11_opy_.format(hub_url, e))
def bstack11l1l1l1l_opy_():
  try:
    global bstack1l1l11llll_opy_
    bstack111lll1ll_opy_ = bstack1l1llll11l_opy_()
    bstack1ll111lll1_opy_ = []
    results = []
    for bstack1l1l11ll1l_opy_ in bstack111lll1ll_opy_:
      bstack1ll111lll1_opy_.append(bstack1l11l1l1l_opy_(target=bstack1l1lll1l_opy_,args=(bstack1l1l11ll1l_opy_,)))
    for t in bstack1ll111lll1_opy_:
      t.start()
    for t in bstack1ll111lll1_opy_:
      results.append(t.join())
    bstack1ll1l1ll1_opy_ = {}
    for item in results:
      hub_url = item[bstack11111_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬࡾ")]
      latency = item[bstack11111_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭ࡿ")]
      bstack1ll1l1ll1_opy_[hub_url] = latency
    bstack11l1ll1l_opy_ = min(bstack1ll1l1ll1_opy_, key= lambda x: bstack1ll1l1ll1_opy_[x])
    bstack1l1l11llll_opy_ = bstack11l1ll1l_opy_
    logger.debug(bstack111ll1ll_opy_.format(bstack11l1ll1l_opy_))
  except Exception as e:
    logger.debug(bstack11ll1lll_opy_.format(e))
from bstack_utils.messages import *
from bstack_utils import bstack1ll1l1l1_opy_
from bstack_utils.config import Config
from bstack_utils.helper import bstack111llllll_opy_, bstack1lll11l11l_opy_, bstack1ll1l1lll1_opy_, bstack1ll1l11ll_opy_, bstack1l1111l1_opy_, \
  Notset, bstack1ll11111_opy_, \
  bstack1l1l1llll_opy_, bstack1l1ll11lll_opy_, bstack11l11111l_opy_, bstack11lll1lll_opy_, bstack1ll1l11l1_opy_, bstack1ll111l11l_opy_, \
  bstack1l11llll1_opy_, \
  bstack111l11lll_opy_, bstack1l11l1111_opy_, bstack1lll111ll1_opy_, bstack1llll11ll_opy_, \
  bstack111l1llll_opy_, bstack11l11lll1_opy_, bstack1ll1ll11_opy_
from bstack_utils.bstack11l1l11ll_opy_ import bstack11l1ll1l1_opy_
from bstack_utils.bstack1lll1llll_opy_ import bstack1ll11l1ll_opy_
from bstack_utils.bstack111lllll1_opy_ import bstack1ll1l1111_opy_, bstack11l1ll111_opy_
from bstack_utils.bstack1ll1llllll_opy_ import bstack11ll1l1l1_opy_
from bstack_utils.bstack1ll11l111_opy_ import bstack1ll11l111_opy_
from bstack_utils.proxy import bstack1ll1lll1ll_opy_, bstack1lll1ll1l1_opy_, bstack1lll11l1ll_opy_, bstack1lll111ll_opy_
import bstack_utils.bstack1l1111ll1_opy_ as bstack1ll1l11ll1_opy_
from browserstack_sdk.bstack1l1l11l1l_opy_ import *
from browserstack_sdk.bstack1l11ll1l1l_opy_ import *
from bstack_utils.bstack1lll111l_opy_ import bstack1llllllll1_opy_
bstack111111lll_opy_ = bstack11111_opy_ (u"࠭ࠠࠡ࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳࠦࠠࡪࡨࠫࡴࡦ࡭ࡥࠡ࠿ࡀࡁࠥࡼ࡯ࡪࡦࠣ࠴࠮ࠦࡻ࡝ࡰࠣࠤࠥࡺࡲࡺࡽ࡟ࡲࠥࡩ࡯࡯ࡵࡷࠤ࡫ࡹࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࡠࠬ࡬ࡳ࡝ࠩࠬ࠿ࡡࡴࠠࠡࠢࠣࠤ࡫ࡹ࠮ࡢࡲࡳࡩࡳࡪࡆࡪ࡮ࡨࡗࡾࡴࡣࠩࡤࡶࡸࡦࡩ࡫ࡠࡲࡤࡸ࡭࠲ࠠࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡲࡢ࡭ࡳࡪࡥࡹࠫࠣ࠯ࠥࠨ࠺ࠣࠢ࠮ࠤࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࠫࡥࡼࡧࡩࡵࠢࡱࡩࡼࡖࡡࡨࡧ࠵࠲ࡪࡼࡡ࡭ࡷࡤࡸࡪ࠮ࠢࠩࠫࠣࡁࡃࠦࡻࡾࠤ࠯ࠤࡡ࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡧࡦࡶࡖࡩࡸࡹࡩࡰࡰࡇࡩࡹࡧࡩ࡭ࡵࠥࢁࡡ࠭ࠩࠪࠫ࡞ࠦ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠢ࡞ࠫࠣ࠯ࠥࠨࠬ࡝࡞ࡱࠦ࠮ࡢ࡮ࠡࠢࠣࠤࢂࡩࡡࡵࡥ࡫ࠬࡪࡾࠩࡼ࡞ࡱࠤࠥࠦࠠࡾ࡞ࡱࠤࠥࢃ࡜࡯ࠢࠣ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴࠭ࢀ")
bstack11111llll_opy_ = bstack11111_opy_ (u"ࠧ࡝ࡰ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠹࡝࡝ࡰࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠳ࡠࡠࡳࡩ࡯࡯ࡵࡷࠤࡵࡥࡩ࡯ࡦࡨࡼࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠳࡟࡟ࡲࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡸࡲࡩࡤࡧࠫ࠴࠱ࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠴ࠫ࡟ࡲࡨࡵ࡮ࡴࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫ࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤࠬ࠿ࡡࡴࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴࡬ࡢࡷࡱࡧ࡭ࠦ࠽ࠡࡣࡶࡽࡳࡩࠠࠩ࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁ࡜࡯࡮ࡨࡸࠥࡩࡡࡱࡵ࠾ࡠࡳࡺࡲࡺࠢࡾࡠࡳࡩࡡࡱࡵࠣࡁࠥࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠩ࡝ࡰࠣࠤࢂࠦࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࠢࡾࡠࡳࠦࠠࠡࠢࢀࡠࡳࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺࠨࡼ࡞ࡱࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥࡦࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠥࡽࡨࡲࡨࡵࡤࡦࡗࡕࡍࡈࡵ࡭ࡱࡱࡱࡩࡳࡺࠨࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡥࡤࡴࡸ࠯ࠩࡾࡢ࠯ࡠࡳࠦࠠࠡࠢ࠱࠲࠳ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷࡡࡴࠠࠡࡿࠬࡠࡳࢃ࡜࡯࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳ࠭ࢁ")
from ._version import __version__
bstack1l1l111l1l_opy_ = None
CONFIG = {}
bstack1l1ll111ll_opy_ = {}
bstack11l1lll1_opy_ = {}
bstack1ll11l1ll1_opy_ = None
bstack1lll1ll111_opy_ = None
bstack111lll11l_opy_ = None
bstack11l1ll1ll_opy_ = -1
bstack1ll111l1l_opy_ = 0
bstack11l111l1_opy_ = bstack11ll1l1ll_opy_
bstack111111111_opy_ = 1
bstack1l1lll11_opy_ = False
bstack1lll1l1l_opy_ = False
bstack1l1l1lll1l_opy_ = bstack11111_opy_ (u"ࠨࠩࢂ")
bstack1llll1ll_opy_ = bstack11111_opy_ (u"ࠩࠪࢃ")
bstack1111l1l11_opy_ = False
bstack1111111ll_opy_ = True
bstack111ll1l11_opy_ = bstack11111_opy_ (u"ࠪࠫࢄ")
bstack1l1ll1llll_opy_ = []
bstack1l1l11llll_opy_ = bstack11111_opy_ (u"ࠫࠬࢅ")
bstack11l11l1ll_opy_ = False
bstack1lll11111l_opy_ = None
bstack1llll1llll_opy_ = None
bstack1lll1lll1_opy_ = None
bstack1l1l1lll_opy_ = -1
bstack1llll11l_opy_ = os.path.join(os.path.expanduser(bstack11111_opy_ (u"ࠬࢄࠧࢆ")), bstack11111_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ࢇ"), bstack11111_opy_ (u"ࠧ࠯ࡴࡲࡦࡴࡺ࠭ࡳࡧࡳࡳࡷࡺ࠭ࡩࡧ࡯ࡴࡪࡸ࠮࡫ࡵࡲࡲࠬ࢈"))
bstack1ll1ll1l1_opy_ = 0
bstack1ll1l1l1ll_opy_ = []
bstack1l1111111_opy_ = []
bstack1lll111l1_opy_ = []
bstack1l1ll1lll_opy_ = []
bstack11l1ll11_opy_ = bstack11111_opy_ (u"ࠨࠩࢉ")
bstack111ll1l1l_opy_ = bstack11111_opy_ (u"ࠩࠪࢊ")
bstack1ll1lll1l_opy_ = False
bstack1llll1111_opy_ = False
bstack1lll11l1l_opy_ = {}
bstack1l1l1ll111_opy_ = None
bstack1ll11ll11_opy_ = None
bstack1l11l1llll_opy_ = None
bstack1l1l1ll1ll_opy_ = None
bstack1l11lllll1_opy_ = None
bstack1llll111ll_opy_ = None
bstack1lll1l11l1_opy_ = None
bstack1ll11ll1_opy_ = None
bstack1l1ll11ll_opy_ = None
bstack1l1l111l1_opy_ = None
bstack1l1l1l1111_opy_ = None
bstack1l111111l_opy_ = None
bstack1llllll11_opy_ = None
bstack1l1ll1l111_opy_ = None
bstack1lll1l1lll_opy_ = None
bstack1lll1lll_opy_ = None
bstack1ll1lll111_opy_ = None
bstack1llll1lll1_opy_ = None
bstack1l1111l1l_opy_ = None
bstack11l1llll1_opy_ = None
bstack11111l1l1_opy_ = None
bstack11l1ll11l_opy_ = False
bstack1l1l1l1ll_opy_ = bstack11111_opy_ (u"ࠥࠦࢋ")
logger = bstack1ll1l1l1_opy_.get_logger(__name__, bstack11l111l1_opy_)
bstack11111111_opy_ = Config.bstack111l111l_opy_()
percy = bstack11l11111_opy_()
bstack11llll1ll_opy_ = bstack111lll11_opy_()
def bstack11ll11111_opy_():
  global CONFIG
  global bstack1ll1lll1l_opy_
  global bstack11111111_opy_
  bstack1l1ll111l1_opy_ = bstack1ll111l111_opy_(CONFIG)
  if (bstack11111_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ࢌ") in bstack1l1ll111l1_opy_ and str(bstack1l1ll111l1_opy_[bstack11111_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧࢍ")]).lower() == bstack11111_opy_ (u"࠭ࡴࡳࡷࡨࠫࢎ")):
    bstack1ll1lll1l_opy_ = True
  bstack11111111_opy_.bstack1lllllll1l_opy_(bstack1l1ll111l1_opy_.get(bstack11111_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫ࢏"), False))
def bstack1l1ll1ll1_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1l1lll111l_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack11ll111l_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack11111_opy_ (u"ࠣ࠯࠰ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡥࡲࡲ࡫࡯ࡧࡧ࡫࡯ࡩࠧ࢐") == args[i].lower() or bstack11111_opy_ (u"ࠤ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡴࡦࡪࡩࠥ࢑") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack111ll1l11_opy_
      bstack111ll1l11_opy_ += bstack11111_opy_ (u"ࠪ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡇࡴࡴࡦࡪࡩࡉ࡭ࡱ࡫ࠠࠨ࢒") + path
      return path
  return None
bstack1llll1ll1l_opy_ = re.compile(bstack11111_opy_ (u"ࡶࠧ࠴ࠪࡀ࡞ࠧࡿ࠭࠴ࠪࡀࠫࢀ࠲࠯ࡅࠢ࢓"))
def bstack1lll1l11ll_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1llll1ll1l_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack11111_opy_ (u"ࠧࠪࡻࠣ࢔") + group + bstack11111_opy_ (u"ࠨࡽࠣ࢕"), os.environ.get(group))
  return value
def bstack1l1l1l11l1_opy_():
  bstack1ll1l1lll_opy_ = bstack11ll111l_opy_()
  if bstack1ll1l1lll_opy_ and os.path.exists(os.path.abspath(bstack1ll1l1lll_opy_)):
    fileName = bstack1ll1l1lll_opy_
  if bstack11111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫ࢖") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack11111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉࠬࢗ")])) and not bstack11111_opy_ (u"ࠩࡩ࡭ࡱ࡫ࡎࡢ࡯ࡨࠫ࢘") in locals():
    fileName = os.environ[bstack11111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࡡࡉࡍࡑࡋ࢙ࠧ")]
  if bstack11111_opy_ (u"ࠫ࡫࡯࡬ࡦࡐࡤࡱࡪ࢚࠭") in locals():
    bstack11l11l_opy_ = os.path.abspath(fileName)
  else:
    bstack11l11l_opy_ = bstack11111_opy_ (u"࢛ࠬ࠭")
  bstack1l1l1l11ll_opy_ = os.getcwd()
  bstack1ll11lll1l_opy_ = bstack11111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩ࢜")
  bstack11111ll1_opy_ = bstack11111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹࡢ࡯࡯ࠫ࢝")
  while (not os.path.exists(bstack11l11l_opy_)) and bstack1l1l1l11ll_opy_ != bstack11111_opy_ (u"ࠣࠤ࢞"):
    bstack11l11l_opy_ = os.path.join(bstack1l1l1l11ll_opy_, bstack1ll11lll1l_opy_)
    if not os.path.exists(bstack11l11l_opy_):
      bstack11l11l_opy_ = os.path.join(bstack1l1l1l11ll_opy_, bstack11111ll1_opy_)
    if bstack1l1l1l11ll_opy_ != os.path.dirname(bstack1l1l1l11ll_opy_):
      bstack1l1l1l11ll_opy_ = os.path.dirname(bstack1l1l1l11ll_opy_)
    else:
      bstack1l1l1l11ll_opy_ = bstack11111_opy_ (u"ࠤࠥ࢟")
  if not os.path.exists(bstack11l11l_opy_):
    bstack1ll1ll1lll_opy_(
      bstack1ll1l1ll_opy_.format(os.getcwd()))
  try:
    with open(bstack11l11l_opy_, bstack11111_opy_ (u"ࠪࡶࠬࢠ")) as stream:
      yaml.add_implicit_resolver(bstack11111_opy_ (u"ࠦࠦࡶࡡࡵࡪࡨࡼࠧࢡ"), bstack1llll1ll1l_opy_)
      yaml.add_constructor(bstack11111_opy_ (u"ࠧࠧࡰࡢࡶ࡫ࡩࡽࠨࢢ"), bstack1lll1l11ll_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack11l11l_opy_, bstack11111_opy_ (u"࠭ࡲࠨࢣ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack1ll1ll1lll_opy_(bstack111l1111l_opy_.format(str(exc)))
def bstack1l1ll1ll11_opy_(config):
  bstack1ll1llll_opy_ = bstack1l111111_opy_(config)
  for option in list(bstack1ll1llll_opy_):
    if option.lower() in bstack1lll1l111_opy_ and option != bstack1lll1l111_opy_[option.lower()]:
      bstack1ll1llll_opy_[bstack1lll1l111_opy_[option.lower()]] = bstack1ll1llll_opy_[option]
      del bstack1ll1llll_opy_[option]
  return config
def bstack1ll1111l1l_opy_():
  global bstack11l1lll1_opy_
  for key, bstack11l111111_opy_ in bstack11ll1ll11_opy_.items():
    if isinstance(bstack11l111111_opy_, list):
      for var in bstack11l111111_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack11l1lll1_opy_[key] = os.environ[var]
          break
    elif bstack11l111111_opy_ in os.environ and os.environ[bstack11l111111_opy_] and str(os.environ[bstack11l111111_opy_]).strip():
      bstack11l1lll1_opy_[key] = os.environ[bstack11l111111_opy_]
  if bstack11111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩࢤ") in os.environ:
    bstack11l1lll1_opy_[bstack11111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢥ")] = {}
    bstack11l1lll1_opy_[bstack11111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢦ")][bstack11111_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࢧ")] = os.environ[bstack11111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ࢨ")]
def bstack1ll11l1l_opy_():
  global bstack1l1ll111ll_opy_
  global bstack111ll1l11_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack11111_opy_ (u"ࠬ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࢩ").lower() == val.lower():
      bstack1l1ll111ll_opy_[bstack11111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢪ")] = {}
      bstack1l1ll111ll_opy_[bstack11111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࢫ")][bstack11111_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࢬ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack1lllll1lll_opy_ in bstack1l1l1l11l_opy_.items():
    if isinstance(bstack1lllll1lll_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack1lllll1lll_opy_:
          if idx < len(sys.argv) and bstack11111_opy_ (u"ࠩ࠰࠱ࠬࢭ") + var.lower() == val.lower() and not key in bstack1l1ll111ll_opy_:
            bstack1l1ll111ll_opy_[key] = sys.argv[idx + 1]
            bstack111ll1l11_opy_ += bstack11111_opy_ (u"ࠪࠤ࠲࠳ࠧࢮ") + var + bstack11111_opy_ (u"ࠫࠥ࠭ࢯ") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack11111_opy_ (u"ࠬ࠳࠭ࠨࢰ") + bstack1lllll1lll_opy_.lower() == val.lower() and not key in bstack1l1ll111ll_opy_:
          bstack1l1ll111ll_opy_[key] = sys.argv[idx + 1]
          bstack111ll1l11_opy_ += bstack11111_opy_ (u"࠭ࠠ࠮࠯ࠪࢱ") + bstack1lllll1lll_opy_ + bstack11111_opy_ (u"ࠧࠡࠩࢲ") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack1l1l1l111l_opy_(config):
  bstack11lll11ll_opy_ = config.keys()
  for bstack1ll11l11ll_opy_, bstack1l11l1l11_opy_ in bstack11lll1ll1_opy_.items():
    if bstack1l11l1l11_opy_ in bstack11lll11ll_opy_:
      config[bstack1ll11l11ll_opy_] = config[bstack1l11l1l11_opy_]
      del config[bstack1l11l1l11_opy_]
  for bstack1ll11l11ll_opy_, bstack1l11l1l11_opy_ in bstack11ll11l1_opy_.items():
    if isinstance(bstack1l11l1l11_opy_, list):
      for bstack1ll11lll11_opy_ in bstack1l11l1l11_opy_:
        if bstack1ll11lll11_opy_ in bstack11lll11ll_opy_:
          config[bstack1ll11l11ll_opy_] = config[bstack1ll11lll11_opy_]
          del config[bstack1ll11lll11_opy_]
          break
    elif bstack1l11l1l11_opy_ in bstack11lll11ll_opy_:
      config[bstack1ll11l11ll_opy_] = config[bstack1l11l1l11_opy_]
      del config[bstack1l11l1l11_opy_]
  for bstack1ll11lll11_opy_ in list(config):
    for bstack1lll11llll_opy_ in bstack1lll1l11l_opy_:
      if bstack1ll11lll11_opy_.lower() == bstack1lll11llll_opy_.lower() and bstack1ll11lll11_opy_ != bstack1lll11llll_opy_:
        config[bstack1lll11llll_opy_] = config[bstack1ll11lll11_opy_]
        del config[bstack1ll11lll11_opy_]
  bstack1l1ll1l1l_opy_ = []
  if bstack11111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫࢳ") in config:
    bstack1l1ll1l1l_opy_ = config[bstack11111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࢴ")]
  for platform in bstack1l1ll1l1l_opy_:
    for bstack1ll11lll11_opy_ in list(platform):
      for bstack1lll11llll_opy_ in bstack1lll1l11l_opy_:
        if bstack1ll11lll11_opy_.lower() == bstack1lll11llll_opy_.lower() and bstack1ll11lll11_opy_ != bstack1lll11llll_opy_:
          platform[bstack1lll11llll_opy_] = platform[bstack1ll11lll11_opy_]
          del platform[bstack1ll11lll11_opy_]
  for bstack1ll11l11ll_opy_, bstack1l11l1l11_opy_ in bstack11ll11l1_opy_.items():
    for platform in bstack1l1ll1l1l_opy_:
      if isinstance(bstack1l11l1l11_opy_, list):
        for bstack1ll11lll11_opy_ in bstack1l11l1l11_opy_:
          if bstack1ll11lll11_opy_ in platform:
            platform[bstack1ll11l11ll_opy_] = platform[bstack1ll11lll11_opy_]
            del platform[bstack1ll11lll11_opy_]
            break
      elif bstack1l11l1l11_opy_ in platform:
        platform[bstack1ll11l11ll_opy_] = platform[bstack1l11l1l11_opy_]
        del platform[bstack1l11l1l11_opy_]
  for bstack11l1l1lll_opy_ in bstack1111l111_opy_:
    if bstack11l1l1lll_opy_ in config:
      if not bstack1111l111_opy_[bstack11l1l1lll_opy_] in config:
        config[bstack1111l111_opy_[bstack11l1l1lll_opy_]] = {}
      config[bstack1111l111_opy_[bstack11l1l1lll_opy_]].update(config[bstack11l1l1lll_opy_])
      del config[bstack11l1l1lll_opy_]
  for platform in bstack1l1ll1l1l_opy_:
    for bstack11l1l1lll_opy_ in bstack1111l111_opy_:
      if bstack11l1l1lll_opy_ in list(platform):
        if not bstack1111l111_opy_[bstack11l1l1lll_opy_] in platform:
          platform[bstack1111l111_opy_[bstack11l1l1lll_opy_]] = {}
        platform[bstack1111l111_opy_[bstack11l1l1lll_opy_]].update(platform[bstack11l1l1lll_opy_])
        del platform[bstack11l1l1lll_opy_]
  config = bstack1l1ll1ll11_opy_(config)
  return config
def bstack1lll1l1ll_opy_(config):
  global bstack1llll1ll_opy_
  if bstack11111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧࢵ") in config and str(config[bstack11111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨࢶ")]).lower() != bstack11111_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫࢷ"):
    if not bstack11111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢸ") in config:
      config[bstack11111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࢹ")] = {}
    if not bstack11111_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࢺ") in config[bstack11111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢻ")]:
      bstack11l1111l1_opy_ = datetime.datetime.now()
      bstack1ll11l11_opy_ = bstack11l1111l1_opy_.strftime(bstack11111_opy_ (u"ࠪࠩࡩࡥࠥࡣࡡࠨࡌࠪࡓࠧࢼ"))
      hostname = socket.gethostname()
      bstack1llll1l1_opy_ = bstack11111_opy_ (u"ࠫࠬࢽ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack11111_opy_ (u"ࠬࢁࡽࡠࡽࢀࡣࢀࢃࠧࢾ").format(bstack1ll11l11_opy_, hostname, bstack1llll1l1_opy_)
      config[bstack11111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢿ")][bstack11111_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣀ")] = identifier
    bstack1llll1ll_opy_ = config[bstack11111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࣁ")][bstack11111_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣂ")]
  return config
def bstack1l1l111ll_opy_():
  bstack1111ll1l1_opy_ =  bstack11lll1lll_opy_()[bstack11111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠩࣃ")]
  return bstack1111ll1l1_opy_ if bstack1111ll1l1_opy_ else -1
def bstack1l11ll11_opy_(bstack1111ll1l1_opy_):
  global CONFIG
  if not bstack11111_opy_ (u"ࠫࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭ࣄ") in CONFIG[bstack11111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣅ")]:
    return
  CONFIG[bstack11111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣆ")] = CONFIG[bstack11111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣇ")].replace(
    bstack11111_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪࣈ"),
    str(bstack1111ll1l1_opy_)
  )
def bstack1111llll_opy_():
  global CONFIG
  if not bstack11111_opy_ (u"ࠩࠧࡿࡉࡇࡔࡆࡡࡗࡍࡒࡋࡽࠨࣉ") in CONFIG[bstack11111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ࣊")]:
    return
  bstack11l1111l1_opy_ = datetime.datetime.now()
  bstack1ll11l11_opy_ = bstack11l1111l1_opy_.strftime(bstack11111_opy_ (u"ࠫࠪࡪ࠭ࠦࡤ࠰ࠩࡍࡀࠥࡎࠩ࣋"))
  CONFIG[bstack11111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ࣌")] = CONFIG[bstack11111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ࣍")].replace(
    bstack11111_opy_ (u"ࠧࠥࡽࡇࡅ࡙ࡋ࡟ࡕࡋࡐࡉࢂ࠭࣎"),
    bstack1ll11l11_opy_
  )
def bstack1lllll1l1l_opy_():
  global CONFIG
  if bstack11111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴ࣏ࠪ") in CONFIG and not bool(CONFIG[bstack11111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ࣐ࠫ")]):
    del CONFIG[bstack11111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶ࣑ࠬ")]
    return
  if not bstack11111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࣒࠭") in CONFIG:
    CONFIG[bstack11111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ࣓ࠧ")] = bstack11111_opy_ (u"࠭ࠣࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩࣔ")
  if bstack11111_opy_ (u"ࠧࠥࡽࡇࡅ࡙ࡋ࡟ࡕࡋࡐࡉࢂ࠭ࣕ") in CONFIG[bstack11111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣖ")]:
    bstack1111llll_opy_()
    os.environ[bstack11111_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡆࡓࡒࡈࡉࡏࡇࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭ࣗ")] = CONFIG[bstack11111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣘ")]
  if not bstack11111_opy_ (u"ࠫࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭ࣙ") in CONFIG[bstack11111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣚ")]:
    return
  bstack1111ll1l1_opy_ = bstack11111_opy_ (u"࠭ࠧࣛ")
  bstack11ll11l1l_opy_ = bstack1l1l111ll_opy_()
  if bstack11ll11l1l_opy_ != -1:
    bstack1111ll1l1_opy_ = bstack11111_opy_ (u"ࠧࡄࡋࠣࠫࣜ") + str(bstack11ll11l1l_opy_)
  if bstack1111ll1l1_opy_ == bstack11111_opy_ (u"ࠨࠩࣝ"):
    bstack111l1l1l1_opy_ = bstack1ll111l1_opy_(CONFIG[bstack11111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬࣞ")])
    if bstack111l1l1l1_opy_ != -1:
      bstack1111ll1l1_opy_ = str(bstack111l1l1l1_opy_)
  if bstack1111ll1l1_opy_:
    bstack1l11ll11_opy_(bstack1111ll1l1_opy_)
    os.environ[bstack11111_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧࣟ")] = CONFIG[bstack11111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࣠")]
def bstack111lll1l_opy_(bstack1l111l1l1_opy_, bstack1l11ll111l_opy_, path):
  bstack1l1l1lll1_opy_ = {
    bstack11111_opy_ (u"ࠬ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ࣡"): bstack1l11ll111l_opy_
  }
  if os.path.exists(path):
    bstack1l1lll1l1_opy_ = json.load(open(path, bstack11111_opy_ (u"࠭ࡲࡣࠩ࣢")))
  else:
    bstack1l1lll1l1_opy_ = {}
  bstack1l1lll1l1_opy_[bstack1l111l1l1_opy_] = bstack1l1l1lll1_opy_
  with open(path, bstack11111_opy_ (u"ࠢࡸࣣ࠭ࠥ")) as outfile:
    json.dump(bstack1l1lll1l1_opy_, outfile)
def bstack1ll111l1_opy_(bstack1l111l1l1_opy_):
  bstack1l111l1l1_opy_ = str(bstack1l111l1l1_opy_)
  bstack111ll1ll1_opy_ = os.path.join(os.path.expanduser(bstack11111_opy_ (u"ࠨࢀࠪࣤ")), bstack11111_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩࣥ"))
  try:
    if not os.path.exists(bstack111ll1ll1_opy_):
      os.makedirs(bstack111ll1ll1_opy_)
    file_path = os.path.join(os.path.expanduser(bstack11111_opy_ (u"ࠪࢂࣦࠬ")), bstack11111_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫࣧ"), bstack11111_opy_ (u"ࠬ࠴ࡢࡶ࡫࡯ࡨ࠲ࡴࡡ࡮ࡧ࠰ࡧࡦࡩࡨࡦ࠰࡭ࡷࡴࡴࠧࣨ"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack11111_opy_ (u"࠭ࡷࠨࣩ")):
        pass
      with open(file_path, bstack11111_opy_ (u"ࠢࡸ࠭ࠥ࣪")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack11111_opy_ (u"ࠨࡴࠪ࣫")) as bstack1l1l11l11_opy_:
      bstack11111l111_opy_ = json.load(bstack1l1l11l11_opy_)
    if bstack1l111l1l1_opy_ in bstack11111l111_opy_:
      bstack1ll1ll11ll_opy_ = bstack11111l111_opy_[bstack1l111l1l1_opy_][bstack11111_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࣬")]
      bstack111lll111_opy_ = int(bstack1ll1ll11ll_opy_) + 1
      bstack111lll1l_opy_(bstack1l111l1l1_opy_, bstack111lll111_opy_, file_path)
      return bstack111lll111_opy_
    else:
      bstack111lll1l_opy_(bstack1l111l1l1_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1lllllll1_opy_.format(str(e)))
    return -1
def bstack1111l11l_opy_(config):
  if not config[bstack11111_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩ࣭ࠬ")] or not config[bstack11111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿ࣮ࠧ")]:
    return True
  else:
    return False
def bstack11l11l111_opy_(config, index=0):
  global bstack1111l1l11_opy_
  bstack1ll111lll_opy_ = {}
  caps = bstack1l11l1lll_opy_ + bstack111ll1l1_opy_
  if bstack1111l1l11_opy_:
    caps += bstack1l1l1l1lll_opy_
  for key in config:
    if key in caps + [bstack11111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ࣯")]:
      continue
    bstack1ll111lll_opy_[key] = config[key]
  if bstack11111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࣰࠩ") in config:
    for bstack1l1111l11_opy_ in config[bstack11111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࣱࠪ")][index]:
      if bstack1l1111l11_opy_ in caps + [bstack11111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࣲ࠭"), bstack11111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪࣳ")]:
        continue
      bstack1ll111lll_opy_[bstack1l1111l11_opy_] = config[bstack11111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣴ")][index][bstack1l1111l11_opy_]
  bstack1ll111lll_opy_[bstack11111_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ࣵ")] = socket.gethostname()
  if bstack11111_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳࣶ࠭") in bstack1ll111lll_opy_:
    del (bstack1ll111lll_opy_[bstack11111_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧࣷ")])
  return bstack1ll111lll_opy_
def bstack1lll11ll1_opy_(config):
  global bstack1111l1l11_opy_
  bstack1l1ll1l1_opy_ = {}
  caps = bstack111ll1l1_opy_
  if bstack1111l1l11_opy_:
    caps += bstack1l1l1l1lll_opy_
  for key in caps:
    if key in config:
      bstack1l1ll1l1_opy_[key] = config[key]
  return bstack1l1ll1l1_opy_
def bstack1111l1ll1_opy_(bstack1ll111lll_opy_, bstack1l1ll1l1_opy_):
  bstack1ll1l11l_opy_ = {}
  for key in bstack1ll111lll_opy_.keys():
    if key in bstack11lll1ll1_opy_:
      bstack1ll1l11l_opy_[bstack11lll1ll1_opy_[key]] = bstack1ll111lll_opy_[key]
    else:
      bstack1ll1l11l_opy_[key] = bstack1ll111lll_opy_[key]
  for key in bstack1l1ll1l1_opy_:
    if key in bstack11lll1ll1_opy_:
      bstack1ll1l11l_opy_[bstack11lll1ll1_opy_[key]] = bstack1l1ll1l1_opy_[key]
    else:
      bstack1ll1l11l_opy_[key] = bstack1l1ll1l1_opy_[key]
  return bstack1ll1l11l_opy_
def bstack1llll111l1_opy_(config, index=0):
  global bstack1111l1l11_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack1llll1l11l_opy_ = bstack111llllll_opy_(bstack1ll111ll11_opy_, config, logger)
  bstack1l1ll1l1_opy_ = bstack1lll11ll1_opy_(config)
  bstack1lll1ll1_opy_ = bstack111ll1l1_opy_
  bstack1lll1ll1_opy_ += bstack111ll1111_opy_
  bstack1l1ll1l1_opy_ = update(bstack1l1ll1l1_opy_, bstack1llll1l11l_opy_)
  if bstack1111l1l11_opy_:
    bstack1lll1ll1_opy_ += bstack1l1l1l1lll_opy_
  if bstack11111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪࣸ") in config:
    if bstack11111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࣹ࠭") in config[bstack11111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࣺࠬ")][index]:
      caps[bstack11111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨࣻ")] = config[bstack11111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࣼ")][index][bstack11111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪࣽ")]
    if bstack11111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧࣾ") in config[bstack11111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪࣿ")][index]:
      caps[bstack11111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩऀ")] = str(config[bstack11111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬँ")][index][bstack11111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫं")])
    bstack11l1l1ll1_opy_ = bstack111llllll_opy_(bstack1ll111ll11_opy_, config[bstack11111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧः")][index], logger)
    bstack1lll1ll1_opy_ += list(bstack11l1l1ll1_opy_.keys())
    for bstack1l1l11l1ll_opy_ in bstack1lll1ll1_opy_:
      if bstack1l1l11l1ll_opy_ in config[bstack11111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨऄ")][index]:
        if bstack1l1l11l1ll_opy_ == bstack11111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨअ"):
          try:
            bstack11l1l1ll1_opy_[bstack1l1l11l1ll_opy_] = str(config[bstack11111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪआ")][index][bstack1l1l11l1ll_opy_] * 1.0)
          except:
            bstack11l1l1ll1_opy_[bstack1l1l11l1ll_opy_] = str(config[bstack11111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫइ")][index][bstack1l1l11l1ll_opy_])
        else:
          bstack11l1l1ll1_opy_[bstack1l1l11l1ll_opy_] = config[bstack11111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬई")][index][bstack1l1l11l1ll_opy_]
        del (config[bstack11111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭उ")][index][bstack1l1l11l1ll_opy_])
    bstack1l1ll1l1_opy_ = update(bstack1l1ll1l1_opy_, bstack11l1l1ll1_opy_)
  bstack1ll111lll_opy_ = bstack11l11l111_opy_(config, index)
  for bstack1ll11lll11_opy_ in bstack111ll1l1_opy_ + [bstack11111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩऊ"), bstack11111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ऋ")] + list(bstack1llll1l11l_opy_.keys()):
    if bstack1ll11lll11_opy_ in bstack1ll111lll_opy_:
      bstack1l1ll1l1_opy_[bstack1ll11lll11_opy_] = bstack1ll111lll_opy_[bstack1ll11lll11_opy_]
      del (bstack1ll111lll_opy_[bstack1ll11lll11_opy_])
  if bstack1ll11111_opy_(config):
    bstack1ll111lll_opy_[bstack11111_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ऌ")] = True
    caps.update(bstack1l1ll1l1_opy_)
    caps[bstack11111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨऍ")] = bstack1ll111lll_opy_
  else:
    bstack1ll111lll_opy_[bstack11111_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨऎ")] = False
    caps.update(bstack1111l1ll1_opy_(bstack1ll111lll_opy_, bstack1l1ll1l1_opy_))
    if bstack11111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧए") in caps:
      caps[bstack11111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫऐ")] = caps[bstack11111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩऑ")]
      del (caps[bstack11111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪऒ")])
    if bstack11111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧओ") in caps:
      caps[bstack11111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩऔ")] = caps[bstack11111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩक")]
      del (caps[bstack11111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪख")])
  return caps
def bstack1l11111ll_opy_():
  global bstack1l1l11llll_opy_
  if bstack1l1lll111l_opy_() <= version.parse(bstack11111_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪग")):
    if bstack1l1l11llll_opy_ != bstack11111_opy_ (u"ࠫࠬघ"):
      return bstack11111_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨङ") + bstack1l1l11llll_opy_ + bstack11111_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠥच")
    return bstack1ll1ll11l_opy_
  if bstack1l1l11llll_opy_ != bstack11111_opy_ (u"ࠧࠨछ"):
    return bstack11111_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥज") + bstack1l1l11llll_opy_ + bstack11111_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥझ")
  return bstack1l1llllll_opy_
def bstack1l1ll111_opy_(options):
  return hasattr(options, bstack11111_opy_ (u"ࠪࡷࡪࡺ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶࡼࠫञ"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack11l111l1l_opy_(options, bstack1l1lll1ll1_opy_):
  for bstack1l11lll111_opy_ in bstack1l1lll1ll1_opy_:
    if bstack1l11lll111_opy_ in [bstack11111_opy_ (u"ࠫࡦࡸࡧࡴࠩट"), bstack11111_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩठ")]:
      continue
    if bstack1l11lll111_opy_ in options._experimental_options:
      options._experimental_options[bstack1l11lll111_opy_] = update(options._experimental_options[bstack1l11lll111_opy_],
                                                         bstack1l1lll1ll1_opy_[bstack1l11lll111_opy_])
    else:
      options.add_experimental_option(bstack1l11lll111_opy_, bstack1l1lll1ll1_opy_[bstack1l11lll111_opy_])
  if bstack11111_opy_ (u"࠭ࡡࡳࡩࡶࠫड") in bstack1l1lll1ll1_opy_:
    for arg in bstack1l1lll1ll1_opy_[bstack11111_opy_ (u"ࠧࡢࡴࡪࡷࠬढ")]:
      options.add_argument(arg)
    del (bstack1l1lll1ll1_opy_[bstack11111_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ण")])
  if bstack11111_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭त") in bstack1l1lll1ll1_opy_:
    for ext in bstack1l1lll1ll1_opy_[bstack11111_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧथ")]:
      options.add_extension(ext)
    del (bstack1l1lll1ll1_opy_[bstack11111_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨद")])
def bstack11l11ll11_opy_(options, bstack1ll1l1ll1l_opy_):
  if bstack11111_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫध") in bstack1ll1l1ll1l_opy_:
    for bstack111111l11_opy_ in bstack1ll1l1ll1l_opy_[bstack11111_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬन")]:
      if bstack111111l11_opy_ in options._preferences:
        options._preferences[bstack111111l11_opy_] = update(options._preferences[bstack111111l11_opy_], bstack1ll1l1ll1l_opy_[bstack11111_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ऩ")][bstack111111l11_opy_])
      else:
        options.set_preference(bstack111111l11_opy_, bstack1ll1l1ll1l_opy_[bstack11111_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧप")][bstack111111l11_opy_])
  if bstack11111_opy_ (u"ࠩࡤࡶ࡬ࡹࠧफ") in bstack1ll1l1ll1l_opy_:
    for arg in bstack1ll1l1ll1l_opy_[bstack11111_opy_ (u"ࠪࡥࡷ࡭ࡳࠨब")]:
      options.add_argument(arg)
def bstack11l111l11_opy_(options, bstack1lllll1ll_opy_):
  if bstack11111_opy_ (u"ࠫࡼ࡫ࡢࡷ࡫ࡨࡻࠬभ") in bstack1lllll1ll_opy_:
    options.use_webview(bool(bstack1lllll1ll_opy_[bstack11111_opy_ (u"ࠬࡽࡥࡣࡸ࡬ࡩࡼ࠭म")]))
  bstack11l111l1l_opy_(options, bstack1lllll1ll_opy_)
def bstack11l11l1l_opy_(options, bstack1llll1l111_opy_):
  for bstack1llll11l11_opy_ in bstack1llll1l111_opy_:
    if bstack1llll11l11_opy_ in [bstack11111_opy_ (u"࠭ࡴࡦࡥ࡫ࡲࡴࡲ࡯ࡨࡻࡓࡶࡪࡼࡩࡦࡹࠪय"), bstack11111_opy_ (u"ࠧࡢࡴࡪࡷࠬर")]:
      continue
    options.set_capability(bstack1llll11l11_opy_, bstack1llll1l111_opy_[bstack1llll11l11_opy_])
  if bstack11111_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ऱ") in bstack1llll1l111_opy_:
    for arg in bstack1llll1l111_opy_[bstack11111_opy_ (u"ࠩࡤࡶ࡬ࡹࠧल")]:
      options.add_argument(arg)
  if bstack11111_opy_ (u"ࠪࡸࡪࡩࡨ࡯ࡱ࡯ࡳ࡬ࡿࡐࡳࡧࡹ࡭ࡪࡽࠧळ") in bstack1llll1l111_opy_:
    options.bstack11ll1llll_opy_(bool(bstack1llll1l111_opy_[bstack11111_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨऴ")]))
def bstack1111lllll_opy_(options, bstack1lllll1111_opy_):
  for bstack1l11l11l_opy_ in bstack1lllll1111_opy_:
    if bstack1l11l11l_opy_ in [bstack11111_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩव"), bstack11111_opy_ (u"࠭ࡡࡳࡩࡶࠫश")]:
      continue
    options._options[bstack1l11l11l_opy_] = bstack1lllll1111_opy_[bstack1l11l11l_opy_]
  if bstack11111_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫष") in bstack1lllll1111_opy_:
    for bstack1l1l111l11_opy_ in bstack1lllll1111_opy_[bstack11111_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬस")]:
      options.bstack1l11l1l1_opy_(
        bstack1l1l111l11_opy_, bstack1lllll1111_opy_[bstack11111_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ह")][bstack1l1l111l11_opy_])
  if bstack11111_opy_ (u"ࠪࡥࡷ࡭ࡳࠨऺ") in bstack1lllll1111_opy_:
    for arg in bstack1lllll1111_opy_[bstack11111_opy_ (u"ࠫࡦࡸࡧࡴࠩऻ")]:
      options.add_argument(arg)
def bstack1ll111ll_opy_(options, caps):
  if not hasattr(options, bstack11111_opy_ (u"ࠬࡑࡅ़࡚ࠩ")):
    return
  if options.KEY == bstack11111_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫऽ") and options.KEY in caps:
    bstack11l111l1l_opy_(options, caps[bstack11111_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬा")])
  elif options.KEY == bstack11111_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ि") and options.KEY in caps:
    bstack11l11ll11_opy_(options, caps[bstack11111_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧी")])
  elif options.KEY == bstack11111_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫु") and options.KEY in caps:
    bstack11l11l1l_opy_(options, caps[bstack11111_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬू")])
  elif options.KEY == bstack11111_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ृ") and options.KEY in caps:
    bstack11l111l11_opy_(options, caps[bstack11111_opy_ (u"࠭࡭ࡴ࠼ࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧॄ")])
  elif options.KEY == bstack11111_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ॅ") and options.KEY in caps:
    bstack1111lllll_opy_(options, caps[bstack11111_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧॆ")])
def bstack1ll1llll11_opy_(caps):
  global bstack1111l1l11_opy_
  if isinstance(os.environ.get(bstack11111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪे")), str):
    bstack1111l1l11_opy_ = eval(os.getenv(bstack11111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫै")))
  if bstack1111l1l11_opy_:
    if bstack1l1ll1ll1_opy_() < version.parse(bstack11111_opy_ (u"ࠫ࠷࠴࠳࠯࠲ࠪॉ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack11111_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬॊ")
    if bstack11111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫो") in caps:
      browser = caps[bstack11111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬौ")]
    elif bstack11111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳ्ࠩ") in caps:
      browser = caps[bstack11111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪॎ")]
    browser = str(browser).lower()
    if browser == bstack11111_opy_ (u"ࠪ࡭ࡵ࡮࡯࡯ࡧࠪॏ") or browser == bstack11111_opy_ (u"ࠫ࡮ࡶࡡࡥࠩॐ"):
      browser = bstack11111_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࠬ॑")
    if browser == bstack11111_opy_ (u"࠭ࡳࡢ࡯ࡶࡹࡳ࡭॒ࠧ"):
      browser = bstack11111_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ॓")
    if browser not in [bstack11111_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨ॔"), bstack11111_opy_ (u"ࠩࡨࡨ࡬࡫ࠧॕ"), bstack11111_opy_ (u"ࠪ࡭ࡪ࠭ॖ"), bstack11111_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫॗ"), bstack11111_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽ࠭क़")]:
      return None
    try:
      package = bstack11111_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠯ࡹࡨࡦࡩࡸࡩࡷࡧࡵ࠲ࢀࢃ࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨख़").format(browser)
      name = bstack11111_opy_ (u"ࠧࡐࡲࡷ࡭ࡴࡴࡳࠨग़")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1l1ll111_opy_(options):
        return None
      for bstack1ll11lll11_opy_ in caps.keys():
        options.set_capability(bstack1ll11lll11_opy_, caps[bstack1ll11lll11_opy_])
      bstack1ll111ll_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1l11lll11_opy_(options, bstack1lll11ll_opy_):
  if not bstack1l1ll111_opy_(options):
    return
  for bstack1ll11lll11_opy_ in bstack1lll11ll_opy_.keys():
    if bstack1ll11lll11_opy_ in bstack111ll1111_opy_:
      continue
    if bstack1ll11lll11_opy_ in options._caps and type(options._caps[bstack1ll11lll11_opy_]) in [dict, list]:
      options._caps[bstack1ll11lll11_opy_] = update(options._caps[bstack1ll11lll11_opy_], bstack1lll11ll_opy_[bstack1ll11lll11_opy_])
    else:
      options.set_capability(bstack1ll11lll11_opy_, bstack1lll11ll_opy_[bstack1ll11lll11_opy_])
  bstack1ll111ll_opy_(options, bstack1lll11ll_opy_)
  if bstack11111_opy_ (u"ࠨ࡯ࡲࡾ࠿ࡪࡥࡣࡷࡪ࡫ࡪࡸࡁࡥࡦࡵࡩࡸࡹࠧज़") in options._caps:
    if options._caps[bstack11111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧड़")] and options._caps[bstack11111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨढ़")].lower() != bstack11111_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬफ़"):
      del options._caps[bstack11111_opy_ (u"ࠬࡳ࡯ࡻ࠼ࡧࡩࡧࡻࡧࡨࡧࡵࡅࡩࡪࡲࡦࡵࡶࠫय़")]
def bstack1111ll11_opy_(proxy_config):
  if bstack11111_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪॠ") in proxy_config:
    proxy_config[bstack11111_opy_ (u"ࠧࡴࡵ࡯ࡔࡷࡵࡸࡺࠩॡ")] = proxy_config[bstack11111_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬॢ")]
    del (proxy_config[bstack11111_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ॣ")])
  if bstack11111_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭।") in proxy_config and proxy_config[bstack11111_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧ॥")].lower() != bstack11111_opy_ (u"ࠬࡪࡩࡳࡧࡦࡸࠬ०"):
    proxy_config[bstack11111_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡙ࡿࡰࡦࠩ१")] = bstack11111_opy_ (u"ࠧ࡮ࡣࡱࡹࡦࡲࠧ२")
  if bstack11111_opy_ (u"ࠨࡲࡵࡳࡽࡿࡁࡶࡶࡲࡧࡴࡴࡦࡪࡩࡘࡶࡱ࠭३") in proxy_config:
    proxy_config[bstack11111_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬ४")] = bstack11111_opy_ (u"ࠪࡴࡦࡩࠧ५")
  return proxy_config
def bstack1l11l111l_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack11111_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪ६") in config:
    return proxy
  config[bstack11111_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ७")] = bstack1111ll11_opy_(config[bstack11111_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬ८")])
  if proxy == None:
    proxy = Proxy(config[bstack11111_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭९")])
  return proxy
def bstack1lll11lll_opy_(self):
  global CONFIG
  global bstack1l111111l_opy_
  try:
    proxy = bstack1lll11l1ll_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack11111_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭॰")):
        proxies = bstack1ll1lll1ll_opy_(proxy, bstack1l11111ll_opy_())
        if len(proxies) > 0:
          protocol, bstack1l111ll1l_opy_ = proxies.popitem()
          if bstack11111_opy_ (u"ࠤ࠽࠳࠴ࠨॱ") in bstack1l111ll1l_opy_:
            return bstack1l111ll1l_opy_
          else:
            return bstack11111_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦॲ") + bstack1l111ll1l_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack11111_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡱࡴࡲࡼࡾࠦࡵࡳ࡮ࠣ࠾ࠥࢁࡽࠣॳ").format(str(e)))
  return bstack1l111111l_opy_(self)
def bstack1l11lllll_opy_():
  global CONFIG
  return bstack1lll111ll_opy_(CONFIG) and bstack1ll111l11l_opy_() and bstack1l1lll111l_opy_() >= version.parse(bstack1l11l1lll1_opy_)
def bstack1llllll111_opy_():
  global CONFIG
  return (bstack11111_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨॴ") in CONFIG or bstack11111_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪॵ") in CONFIG) and bstack1l11llll1_opy_()
def bstack1l111111_opy_(config):
  bstack1ll1llll_opy_ = {}
  if bstack11111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫॶ") in config:
    bstack1ll1llll_opy_ = config[bstack11111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬॷ")]
  if bstack11111_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨॸ") in config:
    bstack1ll1llll_opy_ = config[bstack11111_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩॹ")]
  proxy = bstack1lll11l1ll_opy_(config)
  if proxy:
    if proxy.endswith(bstack11111_opy_ (u"ࠫ࠳ࡶࡡࡤࠩॺ")) and os.path.isfile(proxy):
      bstack1ll1llll_opy_[bstack11111_opy_ (u"ࠬ࠳ࡰࡢࡥ࠰ࡪ࡮ࡲࡥࠨॻ")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack11111_opy_ (u"࠭࠮ࡱࡣࡦࠫॼ")):
        proxies = bstack1lll1ll1l1_opy_(config, bstack1l11111ll_opy_())
        if len(proxies) > 0:
          protocol, bstack1l111ll1l_opy_ = proxies.popitem()
          if bstack11111_opy_ (u"ࠢ࠻࠱࠲ࠦॽ") in bstack1l111ll1l_opy_:
            parsed_url = urlparse(bstack1l111ll1l_opy_)
          else:
            parsed_url = urlparse(protocol + bstack11111_opy_ (u"ࠣ࠼࠲࠳ࠧॾ") + bstack1l111ll1l_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1ll1llll_opy_[bstack11111_opy_ (u"ࠩࡳࡶࡴࡾࡹࡉࡱࡶࡸࠬॿ")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1ll1llll_opy_[bstack11111_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡲࡶࡹ࠭ঀ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1ll1llll_opy_[bstack11111_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡘࡷࡪࡸࠧঁ")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1ll1llll_opy_[bstack11111_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡦࡹࡳࠨং")] = str(parsed_url.password)
  return bstack1ll1llll_opy_
def bstack1ll111l111_opy_(config):
  if bstack11111_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫঃ") in config:
    return config[bstack11111_opy_ (u"ࠧࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠬ঄")]
  return {}
def bstack1l1ll1lll1_opy_(caps):
  global bstack1llll1ll_opy_
  if bstack11111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩঅ") in caps:
    caps[bstack11111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪআ")][bstack11111_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࠩই")] = True
    if bstack1llll1ll_opy_:
      caps[bstack11111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬঈ")][bstack11111_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧউ")] = bstack1llll1ll_opy_
  else:
    caps[bstack11111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࠫঊ")] = True
    if bstack1llll1ll_opy_:
      caps[bstack11111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨঋ")] = bstack1llll1ll_opy_
def bstack1l1l1l1ll1_opy_():
  global CONFIG
  if bstack11111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬঌ") in CONFIG and bstack1ll1ll11_opy_(CONFIG[bstack11111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭঍")]):
    bstack1ll1llll_opy_ = bstack1l111111_opy_(CONFIG)
    bstack1l1l1lllll_opy_(CONFIG[bstack11111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭঎")], bstack1ll1llll_opy_)
def bstack1l1l1lllll_opy_(key, bstack1ll1llll_opy_):
  global bstack1l1l111l1l_opy_
  logger.info(bstack11ll1ll1l_opy_)
  try:
    bstack1l1l111l1l_opy_ = Local()
    bstack111l1ll1l_opy_ = {bstack11111_opy_ (u"ࠫࡰ࡫ࡹࠨএ"): key}
    bstack111l1ll1l_opy_.update(bstack1ll1llll_opy_)
    logger.debug(bstack1l1l1111l1_opy_.format(str(bstack111l1ll1l_opy_)))
    bstack1l1l111l1l_opy_.start(**bstack111l1ll1l_opy_)
    if bstack1l1l111l1l_opy_.isRunning():
      logger.info(bstack1l1ll1l11_opy_)
  except Exception as e:
    bstack1ll1ll1lll_opy_(bstack1l1l11ll1_opy_.format(str(e)))
def bstack1l11l1ll_opy_():
  global bstack1l1l111l1l_opy_
  if bstack1l1l111l1l_opy_.isRunning():
    logger.info(bstack11llllll_opy_)
    bstack1l1l111l1l_opy_.stop()
  bstack1l1l111l1l_opy_ = None
def bstack1l11ll1111_opy_(bstack111l1l1l_opy_=[]):
  global CONFIG
  bstack1l1l111lll_opy_ = []
  bstack11lllll1_opy_ = [bstack11111_opy_ (u"ࠬࡵࡳࠨঐ"), bstack11111_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩ঑"), bstack11111_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫ঒"), bstack11111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪও"), bstack11111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧঔ"), bstack11111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫক")]
  try:
    for err in bstack111l1l1l_opy_:
      bstack1l11llll1l_opy_ = {}
      for k in bstack11lllll1_opy_:
        val = CONFIG[bstack11111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧখ")][int(err[bstack11111_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫগ")])].get(k)
        if val:
          bstack1l11llll1l_opy_[k] = val
      if(err[bstack11111_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬঘ")] != bstack11111_opy_ (u"ࠧࠨঙ")):
        bstack1l11llll1l_opy_[bstack11111_opy_ (u"ࠨࡶࡨࡷࡹࡹࠧচ")] = {
          err[bstack11111_opy_ (u"ࠩࡱࡥࡲ࡫ࠧছ")]: err[bstack11111_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩজ")]
        }
        bstack1l1l111lll_opy_.append(bstack1l11llll1l_opy_)
  except Exception as e:
    logger.debug(bstack11111_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡰࡴࡰࡥࡹࡺࡩ࡯ࡩࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥ࡫ࡶࡦࡰࡷ࠾ࠥ࠭ঝ") + str(e))
  finally:
    return bstack1l1l111lll_opy_
def bstack1l111ll11_opy_(file_name):
  bstack1ll1l1llll_opy_ = []
  try:
    bstack1llllll11l_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1llllll11l_opy_):
      with open(bstack1llllll11l_opy_) as f:
        bstack1l1lll1l1l_opy_ = json.load(f)
        bstack1ll1l1llll_opy_ = bstack1l1lll1l1l_opy_
      os.remove(bstack1llllll11l_opy_)
    return bstack1ll1l1llll_opy_
  except Exception as e:
    logger.debug(bstack11111_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧ࡫ࡱࡨ࡮ࡴࡧࠡࡧࡵࡶࡴࡸࠠ࡭࡫ࡶࡸ࠿ࠦࠧঞ") + str(e))
def bstack111ll1lll_opy_():
  global bstack1l1l1l1ll_opy_
  global bstack1l1ll1llll_opy_
  global bstack1ll1l1l1ll_opy_
  global bstack1l1111111_opy_
  global bstack1lll111l1_opy_
  global bstack111ll1l1l_opy_
  global CONFIG
  percy.shutdown()
  bstack1l1lll11l_opy_ = os.environ.get(bstack11111_opy_ (u"࠭ࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࡡࡘࡗࡊࡊࠧট"))
  if bstack1l1lll11l_opy_ in [bstack11111_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ঠ"), bstack11111_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧড")]:
    bstack1l11llll11_opy_()
  if bstack1l1l1l1ll_opy_:
    logger.warning(bstack1l111lll1_opy_.format(str(bstack1l1l1l1ll_opy_)))
  else:
    try:
      bstack1l1lll1l1_opy_ = bstack1l1l1llll_opy_(bstack11111_opy_ (u"ࠩ࠱ࡦࡸࡺࡡࡤ࡭࠰ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨঢ"), logger)
      if bstack1l1lll1l1_opy_.get(bstack11111_opy_ (u"ࠪࡲࡺࡪࡧࡦࡡ࡯ࡳࡨࡧ࡬ࠨণ")) and bstack1l1lll1l1_opy_.get(bstack11111_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩত")).get(bstack11111_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧথ")):
        logger.warning(bstack1l111lll1_opy_.format(str(bstack1l1lll1l1_opy_[bstack11111_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫদ")][bstack11111_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩধ")])))
    except Exception as e:
      logger.error(e)
  logger.info(bstack111l11l1l_opy_)
  global bstack1l1l111l1l_opy_
  if bstack1l1l111l1l_opy_:
    bstack1l11l1ll_opy_()
  try:
    for driver in bstack1l1ll1llll_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1l1l11ll_opy_)
  if bstack111ll1l1l_opy_ == bstack11111_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧন"):
    bstack1lll111l1_opy_ = bstack1l111ll11_opy_(bstack11111_opy_ (u"ࠩࡵࡳࡧࡵࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪ঩"))
  if bstack111ll1l1l_opy_ == bstack11111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪপ") and len(bstack1l1111111_opy_) == 0:
    bstack1l1111111_opy_ = bstack1l111ll11_opy_(bstack11111_opy_ (u"ࠫࡵࡽ࡟ࡱࡻࡷࡩࡸࡺ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩফ"))
    if len(bstack1l1111111_opy_) == 0:
      bstack1l1111111_opy_ = bstack1l111ll11_opy_(bstack11111_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡶࡰࡱࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫব"))
  bstack1ll1l1l111_opy_ = bstack11111_opy_ (u"࠭ࠧভ")
  if len(bstack1ll1l1l1ll_opy_) > 0:
    bstack1ll1l1l111_opy_ = bstack1l11ll1111_opy_(bstack1ll1l1l1ll_opy_)
  elif len(bstack1l1111111_opy_) > 0:
    bstack1ll1l1l111_opy_ = bstack1l11ll1111_opy_(bstack1l1111111_opy_)
  elif len(bstack1lll111l1_opy_) > 0:
    bstack1ll1l1l111_opy_ = bstack1l11ll1111_opy_(bstack1lll111l1_opy_)
  elif len(bstack1l1ll1lll_opy_) > 0:
    bstack1ll1l1l111_opy_ = bstack1l11ll1111_opy_(bstack1l1ll1lll_opy_)
  if bool(bstack1ll1l1l111_opy_):
    bstack1llll1l1l_opy_(bstack1ll1l1l111_opy_)
  else:
    bstack1llll1l1l_opy_()
  bstack1l1ll11lll_opy_(bstack1ll1ll111l_opy_, logger)
  bstack1ll1l1l1_opy_.bstack1ll1l11l1l_opy_(CONFIG)
def bstack11111111l_opy_(self, *args):
  logger.error(bstack1ll11111l1_opy_)
  bstack111ll1lll_opy_()
  sys.exit(1)
def bstack1ll1ll1lll_opy_(err):
  logger.critical(bstack1l1l111111_opy_.format(str(err)))
  bstack1llll1l1l_opy_(bstack1l1l111111_opy_.format(str(err)), True)
  atexit.unregister(bstack111ll1lll_opy_)
  bstack1l11llll11_opy_()
  sys.exit(1)
def bstack1l1lll1111_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1llll1l1l_opy_(message, True)
  atexit.unregister(bstack111ll1lll_opy_)
  bstack1l11llll11_opy_()
  sys.exit(1)
def bstack11111ll1l_opy_():
  global CONFIG
  global bstack1l1ll111ll_opy_
  global bstack11l1lll1_opy_
  global bstack1111111ll_opy_
  CONFIG = bstack1l1l1l11l1_opy_()
  load_dotenv(CONFIG.get(bstack11111_opy_ (u"ࠧࡦࡰࡹࡊ࡮ࡲࡥࠨম")))
  bstack1ll1111l1l_opy_()
  bstack1ll11l1l_opy_()
  CONFIG = bstack1l1l1l111l_opy_(CONFIG)
  update(CONFIG, bstack11l1lll1_opy_)
  update(CONFIG, bstack1l1ll111ll_opy_)
  CONFIG = bstack1lll1l1ll_opy_(CONFIG)
  bstack1111111ll_opy_ = bstack1l1111l1_opy_(CONFIG)
  bstack11111111_opy_.bstack1l1l1111_opy_(bstack11111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩয"), bstack1111111ll_opy_)
  if (bstack11111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬর") in CONFIG and bstack11111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭঱") in bstack1l1ll111ll_opy_) or (
          bstack11111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧল") in CONFIG and bstack11111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ঳") not in bstack11l1lll1_opy_):
    if os.getenv(bstack11111_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪ঴")):
      CONFIG[bstack11111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ঵")] = os.getenv(bstack11111_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬশ"))
    else:
      bstack1lllll1l1l_opy_()
  elif (bstack11111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬষ") not in CONFIG and bstack11111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬস") in CONFIG) or (
          bstack11111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧহ") in bstack11l1lll1_opy_ and bstack11111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ঺") not in bstack1l1ll111ll_opy_):
    del (CONFIG[bstack11111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ঻")])
  if bstack1111l11l_opy_(CONFIG):
    bstack1ll1ll1lll_opy_(bstack1ll1l1111l_opy_)
  bstack1llll11l1_opy_()
  bstack1ll1111111_opy_()
  if bstack1111l1l11_opy_:
    CONFIG[bstack11111_opy_ (u"ࠧࡢࡲࡳ়ࠫ")] = bstack1111l1l1l_opy_(CONFIG)
    logger.info(bstack1l1ll1l1ll_opy_.format(CONFIG[bstack11111_opy_ (u"ࠨࡣࡳࡴࠬঽ")]))
  if not bstack1111111ll_opy_:
    CONFIG[bstack11111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬা")] = [{}]
def bstack1111lll11_opy_(config, bstack111l11111_opy_):
  global CONFIG
  global bstack1111l1l11_opy_
  CONFIG = config
  bstack1111l1l11_opy_ = bstack111l11111_opy_
def bstack1ll1111111_opy_():
  global CONFIG
  global bstack1111l1l11_opy_
  if bstack11111_opy_ (u"ࠪࡥࡵࡶࠧি") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1l1lll1111_opy_(e, bstack1lll1ll1ll_opy_)
    bstack1111l1l11_opy_ = True
    bstack11111111_opy_.bstack1l1l1111_opy_(bstack11111_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪী"), True)
def bstack1111l1l1l_opy_(config):
  bstack11l1lll1l_opy_ = bstack11111_opy_ (u"ࠬ࠭ু")
  app = config[bstack11111_opy_ (u"࠭ࡡࡱࡲࠪূ")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1lll1111l_opy_:
      if os.path.exists(app):
        bstack11l1lll1l_opy_ = bstack1ll1lllll1_opy_(config, app)
      elif bstack1ll1111ll_opy_(app):
        bstack11l1lll1l_opy_ = app
      else:
        bstack1ll1ll1lll_opy_(bstack1l11lll1_opy_.format(app))
    else:
      if bstack1ll1111ll_opy_(app):
        bstack11l1lll1l_opy_ = app
      elif os.path.exists(app):
        bstack11l1lll1l_opy_ = bstack1ll1lllll1_opy_(app)
      else:
        bstack1ll1ll1lll_opy_(bstack11111l11_opy_)
  else:
    if len(app) > 2:
      bstack1ll1ll1lll_opy_(bstack111111ll1_opy_)
    elif len(app) == 2:
      if bstack11111_opy_ (u"ࠧࡱࡣࡷ࡬ࠬৃ") in app and bstack11111_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠫৄ") in app:
        if os.path.exists(app[bstack11111_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ৅")]):
          bstack11l1lll1l_opy_ = bstack1ll1lllll1_opy_(config, app[bstack11111_opy_ (u"ࠪࡴࡦࡺࡨࠨ৆")], app[bstack11111_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣ࡮ࡪࠧে")])
        else:
          bstack1ll1ll1lll_opy_(bstack1l11lll1_opy_.format(app))
      else:
        bstack1ll1ll1lll_opy_(bstack111111ll1_opy_)
    else:
      for key in app:
        if key in bstack1l1ll11l1_opy_:
          if key == bstack11111_opy_ (u"ࠬࡶࡡࡵࡪࠪৈ"):
            if os.path.exists(app[key]):
              bstack11l1lll1l_opy_ = bstack1ll1lllll1_opy_(config, app[key])
            else:
              bstack1ll1ll1lll_opy_(bstack1l11lll1_opy_.format(app))
          else:
            bstack11l1lll1l_opy_ = app[key]
        else:
          bstack1ll1ll1lll_opy_(bstack1l1lll111_opy_)
  return bstack11l1lll1l_opy_
def bstack1ll1111ll_opy_(bstack11l1lll1l_opy_):
  import re
  bstack1l11lll1l_opy_ = re.compile(bstack11111_opy_ (u"ࡸࠢ࡟࡝ࡤ࠱ࡿࡇ࡛࠭࠲࠰࠽ࡡࡥ࠮࡝࠯ࡠ࠮ࠩࠨ৉"))
  bstack11l11l1l1_opy_ = re.compile(bstack11111_opy_ (u"ࡲࠣࡠ࡞ࡥ࠲ࢀࡁ࠮࡜࠳࠱࠾ࡢ࡟࠯࡞࠰ࡡ࠯࠵࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬࠧࠦ৊"))
  if bstack11111_opy_ (u"ࠨࡤࡶ࠾࠴࠵ࠧো") in bstack11l1lll1l_opy_ or re.fullmatch(bstack1l11lll1l_opy_, bstack11l1lll1l_opy_) or re.fullmatch(bstack11l11l1l1_opy_, bstack11l1lll1l_opy_):
    return True
  else:
    return False
def bstack1ll1lllll1_opy_(config, path, bstack11lll1l1_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack11111_opy_ (u"ࠩࡵࡦࠬৌ")).read()).hexdigest()
  bstack1ll1111l_opy_ = bstack111l1l111_opy_(md5_hash)
  bstack11l1lll1l_opy_ = None
  if bstack1ll1111l_opy_:
    logger.info(bstack1ll1111l1_opy_.format(bstack1ll1111l_opy_, md5_hash))
    return bstack1ll1111l_opy_
  bstack1ll1111l11_opy_ = MultipartEncoder(
    fields={
      bstack11111_opy_ (u"ࠪࡪ࡮ࡲࡥࠨ্"): (os.path.basename(path), open(os.path.abspath(path), bstack11111_opy_ (u"ࠫࡷࡨࠧৎ")), bstack11111_opy_ (u"ࠬࡺࡥࡹࡶ࠲ࡴࡱࡧࡩ࡯ࠩ৏")),
      bstack11111_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡥࡩࡥࠩ৐"): bstack11lll1l1_opy_
    }
  )
  response = requests.post(bstack1llll11lll_opy_, data=bstack1ll1111l11_opy_,
                           headers={bstack11111_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭৑"): bstack1ll1111l11_opy_.content_type},
                           auth=(config[bstack11111_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ৒")], config[bstack11111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ৓")]))
  try:
    res = json.loads(response.text)
    bstack11l1lll1l_opy_ = res[bstack11111_opy_ (u"ࠪࡥࡵࡶ࡟ࡶࡴ࡯ࠫ৔")]
    logger.info(bstack11l1lll11_opy_.format(bstack11l1lll1l_opy_))
    bstack1111ll1l_opy_(md5_hash, bstack11l1lll1l_opy_)
  except ValueError as err:
    bstack1ll1ll1lll_opy_(bstack1lll1l1l1_opy_.format(str(err)))
  return bstack11l1lll1l_opy_
def bstack1llll11l1_opy_():
  global CONFIG
  global bstack111111111_opy_
  bstack1l11ll1l1_opy_ = 0
  bstack1111llll1_opy_ = 1
  if bstack11111_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ৕") in CONFIG:
    bstack1111llll1_opy_ = CONFIG[bstack11111_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ৖")]
  if bstack11111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩৗ") in CONFIG:
    bstack1l11ll1l1_opy_ = len(CONFIG[bstack11111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ৘")])
  bstack111111111_opy_ = int(bstack1111llll1_opy_) * int(bstack1l11ll1l1_opy_)
def bstack111l1l111_opy_(md5_hash):
  bstack11ll111ll_opy_ = os.path.join(os.path.expanduser(bstack11111_opy_ (u"ࠨࢀࠪ৙")), bstack11111_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ৚"), bstack11111_opy_ (u"ࠪࡥࡵࡶࡕࡱ࡮ࡲࡥࡩࡓࡄ࠶ࡊࡤࡷ࡭࠴ࡪࡴࡱࡱࠫ৛"))
  if os.path.exists(bstack11ll111ll_opy_):
    bstack1l1ll11l_opy_ = json.load(open(bstack11ll111ll_opy_, bstack11111_opy_ (u"ࠫࡷࡨࠧড়")))
    if md5_hash in bstack1l1ll11l_opy_:
      bstack1ll1l1l11l_opy_ = bstack1l1ll11l_opy_[md5_hash]
      bstack1ll11ll1ll_opy_ = datetime.datetime.now()
      bstack1l111l111_opy_ = datetime.datetime.strptime(bstack1ll1l1l11l_opy_[bstack11111_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨঢ়")], bstack11111_opy_ (u"࠭ࠥࡥ࠱ࠨࡱ࠴࡙ࠫࠡࠧࡋ࠾ࠪࡓ࠺ࠦࡕࠪ৞"))
      if (bstack1ll11ll1ll_opy_ - bstack1l111l111_opy_).days > 30:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1ll1l1l11l_opy_[bstack11111_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬয়")]):
        return None
      return bstack1ll1l1l11l_opy_[bstack11111_opy_ (u"ࠨ࡫ࡧࠫৠ")]
  else:
    return None
def bstack1111ll1l_opy_(md5_hash, bstack11l1lll1l_opy_):
  bstack111ll1ll1_opy_ = os.path.join(os.path.expanduser(bstack11111_opy_ (u"ࠩࢁࠫৡ")), bstack11111_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪৢ"))
  if not os.path.exists(bstack111ll1ll1_opy_):
    os.makedirs(bstack111ll1ll1_opy_)
  bstack11ll111ll_opy_ = os.path.join(os.path.expanduser(bstack11111_opy_ (u"ࠫࢃ࠭ৣ")), bstack11111_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ৤"), bstack11111_opy_ (u"࠭ࡡࡱࡲࡘࡴࡱࡵࡡࡥࡏࡇ࠹ࡍࡧࡳࡩ࠰࡭ࡷࡴࡴࠧ৥"))
  bstack1l1l1l11_opy_ = {
    bstack11111_opy_ (u"ࠧࡪࡦࠪ০"): bstack11l1lll1l_opy_,
    bstack11111_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ১"): datetime.datetime.strftime(datetime.datetime.now(), bstack11111_opy_ (u"ࠩࠨࡨ࠴ࠫ࡭࠰ࠧ࡜ࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭২")),
    bstack11111_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ৩"): str(__version__)
  }
  if os.path.exists(bstack11ll111ll_opy_):
    bstack1l1ll11l_opy_ = json.load(open(bstack11ll111ll_opy_, bstack11111_opy_ (u"ࠫࡷࡨࠧ৪")))
  else:
    bstack1l1ll11l_opy_ = {}
  bstack1l1ll11l_opy_[md5_hash] = bstack1l1l1l11_opy_
  with open(bstack11ll111ll_opy_, bstack11111_opy_ (u"ࠧࡽࠫࠣ৫")) as outfile:
    json.dump(bstack1l1ll11l_opy_, outfile)
def bstack1ll1l11lll_opy_(self):
  return
def bstack111lll1l1_opy_(self):
  return
def bstack1ll11111l_opy_(self):
  global bstack1llllll11_opy_
  bstack1llllll11_opy_(self)
def bstack1lllll11l_opy_():
  global bstack1lll1lll1_opy_
  bstack1lll1lll1_opy_ = True
def bstack1l11ll1l11_opy_(self):
  global bstack1l1l1lll1l_opy_
  global bstack1ll11l1ll1_opy_
  global bstack1ll11ll11_opy_
  try:
    if bstack11111_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭৬") in bstack1l1l1lll1l_opy_ and self.session_id != None and bstack1ll1l11ll_opy_(threading.current_thread(), bstack11111_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫ৭"), bstack11111_opy_ (u"ࠨࠩ৮")) != bstack11111_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ৯"):
      bstack11l1111l_opy_ = bstack11111_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪৰ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫৱ")
      if bstack11l1111l_opy_ == bstack11111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ৲"):
        bstack111l1llll_opy_(logger)
      if self != None:
        bstack1ll1l1111_opy_(self, bstack11l1111l_opy_, bstack11111_opy_ (u"࠭ࠬࠡࠩ৳").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack11111_opy_ (u"ࠧࠨ৴")
    if bstack11111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ৵") in bstack1l1l1lll1l_opy_ and getattr(threading.current_thread(), bstack11111_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ৶"), None):
      bstack1l1lllll_opy_.bstack1l1lll11l1_opy_(self, bstack1lll11l1l_opy_, logger, wait=True)
  except Exception as e:
    logger.debug(bstack11111_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࠦ৷") + str(e))
  bstack1ll11ll11_opy_(self)
  self.session_id = None
def bstack1llll1ll1_opy_(self, command_executor=bstack11111_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳࠶࠸࠷࠯࠲࠱࠴࠳࠷࠺࠵࠶࠷࠸ࠧ৸"), *args, **kwargs):
  bstack1ll1ll111_opy_ = bstack1l1l1ll111_opy_(self, command_executor, *args, **kwargs)
  try:
    logger.debug(bstack11111_opy_ (u"ࠬࡉ࡯࡮࡯ࡤࡲࡩࠦࡅࡹࡧࡦࡹࡹࡵࡲࠡࡹ࡫ࡩࡳࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢ࡬ࡷࠥ࡬ࡡ࡭ࡵࡨࠤ࠲ࠦࡻࡾࠩ৹").format(str(command_executor)))
    logger.debug(bstack11111_opy_ (u"࠭ࡈࡶࡤ࡙ࠣࡗࡒࠠࡪࡵࠣ࠱ࠥࢁࡽࠨ৺").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack11111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪ৻") in command_executor._url:
      bstack11111111_opy_.bstack1l1l1111_opy_(bstack11111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩৼ"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack11111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬ৽") in command_executor):
    bstack11111111_opy_.bstack1l1l1111_opy_(bstack11111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫ৾"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack11ll1l1l1_opy_.bstack1ll11ll111_opy_(self)
  return bstack1ll1ll111_opy_
def bstack1llll1lll_opy_(args):
  return bstack11111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠬ৿") in str(args)
def bstack111ll111l_opy_(self, driver_command, *args, **kwargs):
  global bstack11l1llll1_opy_
  global bstack11l1ll11l_opy_
  bstack1ll1l111l1_opy_ = bstack1ll1l11ll_opy_(threading.current_thread(), bstack11111_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ਀"), None) and bstack1ll1l11ll_opy_(
          threading.current_thread(), bstack11111_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬਁ"), None)
  bstack1l1l1llll1_opy_ = getattr(self, bstack11111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧਂ"), None) != None and getattr(self, bstack11111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨਃ"), None) == True
  if not bstack11l1ll11l_opy_ and bstack1111111ll_opy_ and bstack11111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ਄") in CONFIG and CONFIG[bstack11111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪਅ")] == True and bstack1ll11l111_opy_.bstack1l1l1l111_opy_(driver_command) and (bstack1l1l1llll1_opy_ or bstack1ll1l111l1_opy_) and not bstack1llll1lll_opy_(args):
    try:
      bstack11l1ll11l_opy_ = True
      logger.debug(bstack11111_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡦࡰࡴࠣࡿࢂ࠭ਆ").format(driver_command))
      logger.debug(perform_scan(self, driver_command=driver_command))
    except Exception as err:
      logger.debug(bstack11111_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡨࡶ࡫ࡵࡲ࡮ࠢࡶࡧࡦࡴࠠࡼࡿࠪਇ").format(str(err)))
    bstack11l1ll11l_opy_ = False
  response = bstack11l1llll1_opy_(self, driver_command, *args, **kwargs)
  if bstack11111_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬਈ") in str(bstack1l1l1lll1l_opy_).lower() and bstack11ll1l1l1_opy_.on():
    try:
      if driver_command == bstack11111_opy_ (u"ࠧࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫਉ"):
        bstack11ll1l1l1_opy_.bstack11l1llll_opy_({
            bstack11111_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ࠧਊ"): response[bstack11111_opy_ (u"ࠩࡹࡥࡱࡻࡥࠨ਋")],
            bstack11111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ਌"): bstack11ll1l1l1_opy_.current_test_uuid() if bstack11ll1l1l1_opy_.current_test_uuid() else bstack11ll1l1l1_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
def bstack1l11ll1ll_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack1ll11l1ll1_opy_
  global bstack11l1ll1ll_opy_
  global bstack111lll11l_opy_
  global bstack1l1lll11_opy_
  global bstack1lll1l1l_opy_
  global bstack1l1l1lll1l_opy_
  global bstack1l1l1ll111_opy_
  global bstack1l1ll1llll_opy_
  global bstack1l1l1lll_opy_
  global bstack1lll11l1l_opy_
  CONFIG[bstack11111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭਍")] = str(bstack1l1l1lll1l_opy_) + str(__version__)
  command_executor = bstack1l11111ll_opy_()
  logger.debug(bstack1ll1l111l_opy_.format(command_executor))
  proxy = bstack1l11l111l_opy_(CONFIG, proxy)
  bstack11lll1ll_opy_ = 0 if bstack11l1ll1ll_opy_ < 0 else bstack11l1ll1ll_opy_
  try:
    if bstack1l1lll11_opy_ is True:
      bstack11lll1ll_opy_ = int(multiprocessing.current_process().name)
    elif bstack1lll1l1l_opy_ is True:
      bstack11lll1ll_opy_ = int(threading.current_thread().name)
  except:
    bstack11lll1ll_opy_ = 0
  bstack1lll11ll_opy_ = bstack1llll111l1_opy_(CONFIG, bstack11lll1ll_opy_)
  logger.debug(bstack1111l1111_opy_.format(str(bstack1lll11ll_opy_)))
  if bstack11111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ਎") in CONFIG and bstack1ll1ll11_opy_(CONFIG[bstack11111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪਏ")]):
    bstack1l1ll1lll1_opy_(bstack1lll11ll_opy_)
  if desired_capabilities:
    bstack1lll1lll1l_opy_ = bstack1l1l1l111l_opy_(desired_capabilities)
    bstack1lll1lll1l_opy_[bstack11111_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧਐ")] = bstack1ll11111_opy_(CONFIG)
    bstack1ll1l11l11_opy_ = bstack1llll111l1_opy_(bstack1lll1lll1l_opy_)
    if bstack1ll1l11l11_opy_:
      bstack1lll11ll_opy_ = update(bstack1ll1l11l11_opy_, bstack1lll11ll_opy_)
    desired_capabilities = None
  if options:
    bstack1l11lll11_opy_(options, bstack1lll11ll_opy_)
  if not options:
    options = bstack1ll1llll11_opy_(bstack1lll11ll_opy_)
  bstack1lll11l1l_opy_ = CONFIG.get(bstack11111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ਑"))[bstack11lll1ll_opy_]
  if bstack1ll1l11ll1_opy_.bstack1l1l1111l_opy_(CONFIG, bstack11lll1ll_opy_) and bstack1ll1l11ll1_opy_.bstack11lll1l1l_opy_(bstack1lll11ll_opy_, options):
    threading.current_thread().a11yPlatform = True
    bstack1ll1l11ll1_opy_.set_capabilities(bstack1lll11ll_opy_, CONFIG)
  if proxy and bstack1l1lll111l_opy_() >= version.parse(bstack11111_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩ਒")):
    options.proxy(proxy)
  if options and bstack1l1lll111l_opy_() >= version.parse(bstack11111_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩਓ")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1l1lll111l_opy_() < version.parse(bstack11111_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪਔ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1lll11ll_opy_)
  logger.info(bstack1l1l11111l_opy_)
  if bstack1l1lll111l_opy_() >= version.parse(bstack11111_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬਕ")):
    bstack1l1l1ll111_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1l1lll111l_opy_() >= version.parse(bstack11111_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬਖ")):
    bstack1l1l1ll111_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1l1lll111l_opy_() >= version.parse(bstack11111_opy_ (u"ࠧ࠳࠰࠸࠷࠳࠶ࠧਗ")):
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
    bstack1llll1l1l1_opy_ = bstack11111_opy_ (u"ࠨࠩਘ")
    if bstack1l1lll111l_opy_() >= version.parse(bstack11111_opy_ (u"ࠩ࠷࠲࠵࠴࠰ࡣ࠳ࠪਙ")):
      bstack1llll1l1l1_opy_ = self.caps.get(bstack11111_opy_ (u"ࠥࡳࡵࡺࡩ࡮ࡣ࡯ࡌࡺࡨࡕࡳ࡮ࠥਚ"))
    else:
      bstack1llll1l1l1_opy_ = self.capabilities.get(bstack11111_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦਛ"))
    if bstack1llll1l1l1_opy_:
      bstack1lll111ll1_opy_(bstack1llll1l1l1_opy_)
      if bstack1l1lll111l_opy_() <= version.parse(bstack11111_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬਜ")):
        self.command_executor._url = bstack11111_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢਝ") + bstack1l1l11llll_opy_ + bstack11111_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦਞ")
      else:
        self.command_executor._url = bstack11111_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥਟ") + bstack1llll1l1l1_opy_ + bstack11111_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥਠ")
      logger.debug(bstack1l1l11ll11_opy_.format(bstack1llll1l1l1_opy_))
    else:
      logger.debug(bstack1lllllllll_opy_.format(bstack11111_opy_ (u"ࠥࡓࡵࡺࡩ࡮ࡣ࡯ࠤࡍࡻࡢࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧࠦਡ")))
  except Exception as e:
    logger.debug(bstack1lllllllll_opy_.format(e))
  if bstack11111_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪਢ") in bstack1l1l1lll1l_opy_:
    bstack11l11ll1l_opy_(bstack11l1ll1ll_opy_, bstack1l1l1lll_opy_)
  bstack1ll11l1ll1_opy_ = self.session_id
  if bstack11111_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬਣ") in bstack1l1l1lll1l_opy_ or bstack11111_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ਤ") in bstack1l1l1lll1l_opy_ or bstack11111_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ਥ") in bstack1l1l1lll1l_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
    bstack11ll1l1l1_opy_.bstack1ll11ll111_opy_(self)
  bstack1l1ll1llll_opy_.append(self)
  if bstack11111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫਦ") in CONFIG and bstack11111_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧਧ") in CONFIG[bstack11111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ਨ")][bstack11lll1ll_opy_]:
    bstack111lll11l_opy_ = CONFIG[bstack11111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ਩")][bstack11lll1ll_opy_][bstack11111_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪਪ")]
  logger.debug(bstack1ll1l111_opy_.format(bstack1ll11l1ll1_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack1l1l1ll1l_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack11l11l1ll_opy_
      if(bstack11111_opy_ (u"ࠨࡩ࡯ࡦࡨࡼ࠳ࡰࡳࠣਫ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack11111_opy_ (u"ࠧࡿࠩਬ")), bstack11111_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨਭ"), bstack11111_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫਮ")), bstack11111_opy_ (u"ࠪࡻࠬਯ")) as fp:
          fp.write(bstack11111_opy_ (u"ࠦࠧਰ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack11111_opy_ (u"ࠧ࡯࡮ࡥࡧࡻࡣࡧࡹࡴࡢࡥ࡮࠲࡯ࡹࠢ਱")))):
          with open(args[1], bstack11111_opy_ (u"࠭ࡲࠨਲ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack11111_opy_ (u"ࠧࡢࡵࡼࡲࡨࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡡࡱࡩࡼࡖࡡࡨࡧࠫࡧࡴࡴࡴࡦࡺࡷ࠰ࠥࡶࡡࡨࡧࠣࡁࠥࡼ࡯ࡪࡦࠣ࠴࠮࠭ਲ਼") in line), None)
            if index is not None:
                lines.insert(index+2, bstack111111lll_opy_)
            lines.insert(1, bstack11111llll_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack11111_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࡟ࡣࡵࡷࡥࡨࡱ࠮࡫ࡵࠥ਴")), bstack11111_opy_ (u"ࠩࡺࠫਵ")) as bstack1l1l11l1_opy_:
              bstack1l1l11l1_opy_.writelines(lines)
        CONFIG[bstack11111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬਸ਼")] = str(bstack1l1l1lll1l_opy_) + str(__version__)
        bstack11lll1ll_opy_ = 0 if bstack11l1ll1ll_opy_ < 0 else bstack11l1ll1ll_opy_
        try:
          if bstack1l1lll11_opy_ is True:
            bstack11lll1ll_opy_ = int(multiprocessing.current_process().name)
          elif bstack1lll1l1l_opy_ is True:
            bstack11lll1ll_opy_ = int(threading.current_thread().name)
        except:
          bstack11lll1ll_opy_ = 0
        CONFIG[bstack11111_opy_ (u"ࠦࡺࡹࡥࡘ࠵ࡆࠦ਷")] = False
        CONFIG[bstack11111_opy_ (u"ࠧ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦਸ")] = True
        bstack1lll11ll_opy_ = bstack1llll111l1_opy_(CONFIG, bstack11lll1ll_opy_)
        logger.debug(bstack1111l1111_opy_.format(str(bstack1lll11ll_opy_)))
        if CONFIG.get(bstack11111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪਹ")):
          bstack1l1ll1lll1_opy_(bstack1lll11ll_opy_)
        if bstack11111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ਺") in CONFIG and bstack11111_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭਻") in CONFIG[bstack11111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷ਼ࠬ")][bstack11lll1ll_opy_]:
          bstack111lll11l_opy_ = CONFIG[bstack11111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭਽")][bstack11lll1ll_opy_][bstack11111_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩਾ")]
        args.append(os.path.join(os.path.expanduser(bstack11111_opy_ (u"ࠬࢄࠧਿ")), bstack11111_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ੀ"), bstack11111_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩੁ")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1lll11ll_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack11111_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࡟ࡣࡵࡷࡥࡨࡱ࠮࡫ࡵࠥੂ"))
      bstack11l11l1ll_opy_ = True
      return bstack1lll1l1lll_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1l1lll1ll_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack11l1ll1ll_opy_
    global bstack111lll11l_opy_
    global bstack1l1lll11_opy_
    global bstack1lll1l1l_opy_
    global bstack1l1l1lll1l_opy_
    CONFIG[bstack11111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ੃")] = str(bstack1l1l1lll1l_opy_) + str(__version__)
    bstack11lll1ll_opy_ = 0 if bstack11l1ll1ll_opy_ < 0 else bstack11l1ll1ll_opy_
    try:
      if bstack1l1lll11_opy_ is True:
        bstack11lll1ll_opy_ = int(multiprocessing.current_process().name)
      elif bstack1lll1l1l_opy_ is True:
        bstack11lll1ll_opy_ = int(threading.current_thread().name)
    except:
      bstack11lll1ll_opy_ = 0
    CONFIG[bstack11111_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤ੄")] = True
    bstack1lll11ll_opy_ = bstack1llll111l1_opy_(CONFIG, bstack11lll1ll_opy_)
    logger.debug(bstack1111l1111_opy_.format(str(bstack1lll11ll_opy_)))
    if CONFIG.get(bstack11111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ੅")):
      bstack1l1ll1lll1_opy_(bstack1lll11ll_opy_)
    if bstack11111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ੆") in CONFIG and bstack11111_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫੇ") in CONFIG[bstack11111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪੈ")][bstack11lll1ll_opy_]:
      bstack111lll11l_opy_ = CONFIG[bstack11111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ੉")][bstack11lll1ll_opy_][bstack11111_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ੊")]
    import urllib
    import json
    bstack11l1l11l_opy_ = bstack11111_opy_ (u"ࠪࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠬੋ") + urllib.parse.quote(json.dumps(bstack1lll11ll_opy_))
    browser = self.connect(bstack11l1l11l_opy_)
    return browser
except Exception as e:
    pass
def bstack1lllll111_opy_():
    global bstack11l11l1ll_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1l1lll1ll_opy_
        bstack11l11l1ll_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1l1l1ll1l_opy_
      bstack11l11l1ll_opy_ = True
    except Exception as e:
      pass
def bstack11111ll11_opy_(context, bstack1l1llll1ll_opy_):
  try:
    context.page.evaluate(bstack11111_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧੌ"), bstack11111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻੍ࠩ")+ json.dumps(bstack1l1llll1ll_opy_) + bstack11111_opy_ (u"ࠨࡽࡾࠤ੎"))
  except Exception as e:
    logger.debug(bstack11111_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢࡾࢁࠧ੏"), e)
def bstack1lll1ll1l_opy_(context, message, level):
  try:
    context.page.evaluate(bstack11111_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤ੐"), bstack11111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧੑ") + json.dumps(message) + bstack11111_opy_ (u"ࠪ࠰ࠧࡲࡥࡷࡧ࡯ࠦ࠿࠭੒") + json.dumps(level) + bstack11111_opy_ (u"ࠫࢂࢃࠧ੓"))
  except Exception as e:
    logger.debug(bstack11111_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡣࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠥࢁࡽࠣ੔"), e)
def bstack1lllll1l1_opy_(self, url):
  global bstack1l1ll1l111_opy_
  try:
    bstack1llll1l11_opy_(url)
  except Exception as err:
    logger.debug(bstack1l1l11lll_opy_.format(str(err)))
  try:
    bstack1l1ll1l111_opy_(self, url)
  except Exception as e:
    try:
      bstack11ll1111l_opy_ = str(e)
      if any(err_msg in bstack11ll1111l_opy_ for err_msg in bstack11111lll_opy_):
        bstack1llll1l11_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1l1l11lll_opy_.format(str(err)))
    raise e
def bstack1l11lll11l_opy_(self):
  global bstack1llll1llll_opy_
  bstack1llll1llll_opy_ = self
  return
def bstack111l1lll1_opy_(self):
  global bstack1lll11111l_opy_
  bstack1lll11111l_opy_ = self
  return
def bstack1l1111lll_opy_(test_name, bstack1l1lll1lll_opy_):
  global CONFIG
  if CONFIG.get(bstack11111_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ੕"), False):
    bstack111l1l11_opy_ = os.path.relpath(bstack1l1lll1lll_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack111l1l11_opy_)
    bstack11ll1l111_opy_ = suite_name + bstack11111_opy_ (u"ࠢ࠮ࠤ੖") + test_name
    threading.current_thread().percySessionName = bstack11ll1l111_opy_
def bstack1ll1ll1111_opy_(self, test, *args, **kwargs):
  global bstack1l11l1llll_opy_
  test_name = None
  bstack1l1lll1lll_opy_ = None
  if test:
    test_name = str(test.name)
    bstack1l1lll1lll_opy_ = str(test.source)
  bstack1l1111lll_opy_(test_name, bstack1l1lll1lll_opy_)
  bstack1l11l1llll_opy_(self, test, *args, **kwargs)
def bstack1l111ll1_opy_(driver, bstack11ll1l111_opy_):
  if not bstack1ll1lll1l_opy_ and bstack11ll1l111_opy_:
      bstack111l111l1_opy_ = {
          bstack11111_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨ੗"): bstack11111_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ੘"),
          bstack11111_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ਖ਼"): {
              bstack11111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩਗ਼"): bstack11ll1l111_opy_
          }
      }
      bstack1ll1lll11l_opy_ = bstack11111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪਜ਼").format(json.dumps(bstack111l111l1_opy_))
      driver.execute_script(bstack1ll1lll11l_opy_)
  if bstack1lll1ll111_opy_:
      bstack11l1l111l_opy_ = {
          bstack11111_opy_ (u"࠭ࡡࡤࡶ࡬ࡳࡳ࠭ੜ"): bstack11111_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩ੝"),
          bstack11111_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫਫ਼"): {
              bstack11111_opy_ (u"ࠩࡧࡥࡹࡧࠧ੟"): bstack11ll1l111_opy_ + bstack11111_opy_ (u"ࠪࠤࡵࡧࡳࡴࡧࡧࠥࠬ੠"),
              bstack11111_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ੡"): bstack11111_opy_ (u"ࠬ࡯࡮ࡧࡱࠪ੢")
          }
      }
      if bstack1lll1ll111_opy_.status == bstack11111_opy_ (u"࠭ࡐࡂࡕࡖࠫ੣"):
          bstack11ll11lll_opy_ = bstack11111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬ੤").format(json.dumps(bstack11l1l111l_opy_))
          driver.execute_script(bstack11ll11lll_opy_)
          bstack1ll1l1111_opy_(driver, bstack11111_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ੥"))
      elif bstack1lll1ll111_opy_.status == bstack11111_opy_ (u"ࠩࡉࡅࡎࡒࠧ੦"):
          reason = bstack11111_opy_ (u"ࠥࠦ੧")
          bstack1l1llll11_opy_ = bstack11ll1l111_opy_ + bstack11111_opy_ (u"ࠫࠥ࡬ࡡࡪ࡮ࡨࡨࠬ੨")
          if bstack1lll1ll111_opy_.message:
              reason = str(bstack1lll1ll111_opy_.message)
              bstack1l1llll11_opy_ = bstack1l1llll11_opy_ + bstack11111_opy_ (u"ࠬࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴ࠽ࠤࠬ੩") + reason
          bstack11l1l111l_opy_[bstack11111_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ੪")] = {
              bstack11111_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭੫"): bstack11111_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ੬"),
              bstack11111_opy_ (u"ࠩࡧࡥࡹࡧࠧ੭"): bstack1l1llll11_opy_
          }
          bstack11ll11lll_opy_ = bstack11111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨ੮").format(json.dumps(bstack11l1l111l_opy_))
          driver.execute_script(bstack11ll11lll_opy_)
          bstack1ll1l1111_opy_(driver, bstack11111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ੯"), reason)
          bstack11l11lll1_opy_(reason, str(bstack1lll1ll111_opy_), str(bstack11l1ll1ll_opy_), logger)
def bstack1ll11ll1l_opy_(driver, test):
  if CONFIG.get(bstack11111_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫੰ"), False) and CONFIG.get(bstack11111_opy_ (u"࠭ࡰࡦࡴࡦࡽࡈࡧࡰࡵࡷࡵࡩࡒࡵࡤࡦࠩੱ"), bstack11111_opy_ (u"ࠢࡢࡷࡷࡳࠧੲ")) == bstack11111_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥੳ"):
      bstack1lll1l1ll1_opy_ = bstack1ll1l11ll_opy_(threading.current_thread(), bstack11111_opy_ (u"ࠩࡳࡩࡷࡩࡹࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬੴ"), None)
      bstack1ll111l1ll_opy_(driver, bstack1lll1l1ll1_opy_)
  if bstack1ll1l11ll_opy_(threading.current_thread(), bstack11111_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧੵ"), None) and bstack1ll1l11ll_opy_(
          threading.current_thread(), bstack11111_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ੶"), None):
      logger.info(bstack11111_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠣࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡯ࡳࠡࡷࡱࡨࡪࡸࡷࡢࡻ࠱ࠤࠧ੷"))
      bstack1ll1l11ll1_opy_.bstack11llll1l1_opy_(driver, class_name=test.parent.name, name=test.name, module_name=None,
                              path=test.source, bstack1l1l1l1l1_opy_=bstack1lll11l1l_opy_)
def bstack1ll11l1l1_opy_(test, bstack11ll1l111_opy_):
    try:
      data = {}
      if test:
        data[bstack11111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ੸")] = bstack11ll1l111_opy_
      if bstack1lll1ll111_opy_:
        if bstack1lll1ll111_opy_.status == bstack11111_opy_ (u"ࠧࡑࡃࡖࡗࠬ੹"):
          data[bstack11111_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ੺")] = bstack11111_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ੻")
        elif bstack1lll1ll111_opy_.status == bstack11111_opy_ (u"ࠪࡊࡆࡏࡌࠨ੼"):
          data[bstack11111_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ੽")] = bstack11111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ੾")
          if bstack1lll1ll111_opy_.message:
            data[bstack11111_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭੿")] = str(bstack1lll1ll111_opy_.message)
      user = CONFIG[bstack11111_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ઀")]
      key = CONFIG[bstack11111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫઁ")]
      url = bstack11111_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡿࢂࡀࡻࡾࡂࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡸ࡫ࡳࡴ࡫ࡲࡲࡸ࠵ࡻࡾ࠰࡭ࡷࡴࡴࠧં").format(user, key, bstack1ll11l1ll1_opy_)
      headers = {
        bstack11111_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩઃ"): bstack11111_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ઄"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1ll1l1l1l_opy_.format(str(e)))
def bstack1ll11lll1_opy_(test, bstack11ll1l111_opy_):
  global CONFIG
  global bstack1lll11111l_opy_
  global bstack1llll1llll_opy_
  global bstack1ll11l1ll1_opy_
  global bstack1lll1ll111_opy_
  global bstack111lll11l_opy_
  global bstack1l1l1ll1ll_opy_
  global bstack1l11lllll1_opy_
  global bstack1llll111ll_opy_
  global bstack11111l1l1_opy_
  global bstack1l1ll1llll_opy_
  global bstack1lll11l1l_opy_
  try:
    if not bstack1ll11l1ll1_opy_:
      with open(os.path.join(os.path.expanduser(bstack11111_opy_ (u"ࠬࢄࠧઅ")), bstack11111_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭આ"), bstack11111_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩઇ"))) as f:
        bstack1111l11ll_opy_ = json.loads(bstack11111_opy_ (u"ࠣࡽࠥઈ") + f.read().strip() + bstack11111_opy_ (u"ࠩࠥࡼࠧࡀࠠࠣࡻࠥࠫઉ") + bstack11111_opy_ (u"ࠥࢁࠧઊ"))
        bstack1ll11l1ll1_opy_ = bstack1111l11ll_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1l1ll1llll_opy_:
    for driver in bstack1l1ll1llll_opy_:
      if bstack1ll11l1ll1_opy_ == driver.session_id:
        if test:
          bstack1ll11ll1l_opy_(driver, test)
        bstack1l111ll1_opy_(driver, bstack11ll1l111_opy_)
  elif bstack1ll11l1ll1_opy_:
    bstack1ll11l1l1_opy_(test, bstack11ll1l111_opy_)
  if bstack1lll11111l_opy_:
    bstack1l11lllll1_opy_(bstack1lll11111l_opy_)
  if bstack1llll1llll_opy_:
    bstack1llll111ll_opy_(bstack1llll1llll_opy_)
  if bstack1lll1lll1_opy_:
    bstack11111l1l1_opy_()
def bstack1ll111111_opy_(self, test, *args, **kwargs):
  bstack11ll1l111_opy_ = None
  if test:
    bstack11ll1l111_opy_ = str(test.name)
  bstack1ll11lll1_opy_(test, bstack11ll1l111_opy_)
  bstack1l1l1ll1ll_opy_(self, test, *args, **kwargs)
def bstack1l1ll1l11l_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1lll1l11l1_opy_
  global CONFIG
  global bstack1l1ll1llll_opy_
  global bstack1ll11l1ll1_opy_
  bstack111ll11l1_opy_ = None
  try:
    if bstack1ll1l11ll_opy_(threading.current_thread(), bstack11111_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪઋ"), None):
      try:
        if not bstack1ll11l1ll1_opy_:
          with open(os.path.join(os.path.expanduser(bstack11111_opy_ (u"ࠬࢄࠧઌ")), bstack11111_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ઍ"), bstack11111_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩ઎"))) as f:
            bstack1111l11ll_opy_ = json.loads(bstack11111_opy_ (u"ࠣࡽࠥએ") + f.read().strip() + bstack11111_opy_ (u"ࠩࠥࡼࠧࡀࠠࠣࡻࠥࠫઐ") + bstack11111_opy_ (u"ࠥࢁࠧઑ"))
            bstack1ll11l1ll1_opy_ = bstack1111l11ll_opy_[str(threading.get_ident())]
      except:
        pass
      if bstack1l1ll1llll_opy_:
        for driver in bstack1l1ll1llll_opy_:
          if bstack1ll11l1ll1_opy_ == driver.session_id:
            bstack111ll11l1_opy_ = driver
    bstack1lll1lll11_opy_ = bstack1ll1l11ll1_opy_.bstack1l11l11ll_opy_(CONFIG, test.tags)
    if bstack111ll11l1_opy_:
      threading.current_thread().isA11yTest = bstack1ll1l11ll1_opy_.bstack1ll1l11111_opy_(bstack111ll11l1_opy_, bstack1lll1lll11_opy_)
    else:
      threading.current_thread().isA11yTest = bstack1lll1lll11_opy_
  except:
    pass
  bstack1lll1l11l1_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1lll1ll111_opy_
  bstack1lll1ll111_opy_ = self._test
def bstack1lllll111l_opy_():
  global bstack1llll11l_opy_
  try:
    if os.path.exists(bstack1llll11l_opy_):
      os.remove(bstack1llll11l_opy_)
  except Exception as e:
    logger.debug(bstack11111_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡤࡦ࡮ࡨࡸ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧ઒") + str(e))
def bstack1ll111llll_opy_():
  global bstack1llll11l_opy_
  bstack1l1lll1l1_opy_ = {}
  try:
    if not os.path.isfile(bstack1llll11l_opy_):
      with open(bstack1llll11l_opy_, bstack11111_opy_ (u"ࠬࡽࠧઓ")):
        pass
      with open(bstack1llll11l_opy_, bstack11111_opy_ (u"ࠨࡷࠬࠤઔ")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack1llll11l_opy_):
      bstack1l1lll1l1_opy_ = json.load(open(bstack1llll11l_opy_, bstack11111_opy_ (u"ࠧࡳࡤࠪક")))
  except Exception as e:
    logger.debug(bstack11111_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡶࡪࡧࡤࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪખ") + str(e))
  finally:
    return bstack1l1lll1l1_opy_
def bstack11l11ll1l_opy_(platform_index, item_index):
  global bstack1llll11l_opy_
  try:
    bstack1l1lll1l1_opy_ = bstack1ll111llll_opy_()
    bstack1l1lll1l1_opy_[item_index] = platform_index
    with open(bstack1llll11l_opy_, bstack11111_opy_ (u"ࠤࡺ࠯ࠧગ")) as outfile:
      json.dump(bstack1l1lll1l1_opy_, outfile)
  except Exception as e:
    logger.debug(bstack11111_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡽࡲࡪࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠡࡨ࡬ࡰࡪࡀࠠࠨઘ") + str(e))
def bstack11l1lllll_opy_(bstack1ll1l1l1l1_opy_):
  global CONFIG
  bstack1lllll11_opy_ = bstack11111_opy_ (u"ࠫࠬઙ")
  if not bstack11111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨચ") in CONFIG:
    logger.info(bstack11111_opy_ (u"࠭ࡎࡰࠢࡳࡰࡦࡺࡦࡰࡴࡰࡷࠥࡶࡡࡴࡵࡨࡨࠥࡻ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡩࡨࡲࡪࡸࡡࡵࡧࠣࡶࡪࡶ࡯ࡳࡶࠣࡪࡴࡸࠠࡓࡱࡥࡳࡹࠦࡲࡶࡰࠪછ"))
  try:
    platform = CONFIG[bstack11111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪજ")][bstack1ll1l1l1l1_opy_]
    if bstack11111_opy_ (u"ࠨࡱࡶࠫઝ") in platform:
      bstack1lllll11_opy_ += str(platform[bstack11111_opy_ (u"ࠩࡲࡷࠬઞ")]) + bstack11111_opy_ (u"ࠪ࠰ࠥ࠭ટ")
    if bstack11111_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧઠ") in platform:
      bstack1lllll11_opy_ += str(platform[bstack11111_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨડ")]) + bstack11111_opy_ (u"࠭ࠬࠡࠩઢ")
    if bstack11111_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫણ") in platform:
      bstack1lllll11_opy_ += str(platform[bstack11111_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬત")]) + bstack11111_opy_ (u"ࠩ࠯ࠤࠬથ")
    if bstack11111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬદ") in platform:
      bstack1lllll11_opy_ += str(platform[bstack11111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ધ")]) + bstack11111_opy_ (u"ࠬ࠲ࠠࠨન")
    if bstack11111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ઩") in platform:
      bstack1lllll11_opy_ += str(platform[bstack11111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬપ")]) + bstack11111_opy_ (u"ࠨ࠮ࠣࠫફ")
    if bstack11111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪબ") in platform:
      bstack1lllll11_opy_ += str(platform[bstack11111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫભ")]) + bstack11111_opy_ (u"ࠫ࠱ࠦࠧમ")
  except Exception as e:
    logger.debug(bstack11111_opy_ (u"࡙ࠬ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡯࡮ࡨࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡸࡺࡲࡪࡰࡪࠤ࡫ࡵࡲࠡࡴࡨࡴࡴࡸࡴࠡࡩࡨࡲࡪࡸࡡࡵ࡫ࡲࡲࠬય") + str(e))
  finally:
    if bstack1lllll11_opy_[len(bstack1lllll11_opy_) - 2:] == bstack11111_opy_ (u"࠭ࠬࠡࠩર"):
      bstack1lllll11_opy_ = bstack1lllll11_opy_[:-2]
    return bstack1lllll11_opy_
def bstack1l1l11l1l1_opy_(path, bstack1lllll11_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1l1111ll_opy_ = ET.parse(path)
    bstack11llll1l_opy_ = bstack1l1111ll_opy_.getroot()
    bstack1ll1111ll1_opy_ = None
    for suite in bstack11llll1l_opy_.iter(bstack11111_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭઱")):
      if bstack11111_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨલ") in suite.attrib:
        suite.attrib[bstack11111_opy_ (u"ࠩࡱࡥࡲ࡫ࠧળ")] += bstack11111_opy_ (u"ࠪࠤࠬ઴") + bstack1lllll11_opy_
        bstack1ll1111ll1_opy_ = suite
    bstack1l11ll11l_opy_ = None
    for robot in bstack11llll1l_opy_.iter(bstack11111_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪવ")):
      bstack1l11ll11l_opy_ = robot
    bstack1111l1l1_opy_ = len(bstack1l11ll11l_opy_.findall(bstack11111_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫશ")))
    if bstack1111l1l1_opy_ == 1:
      bstack1l11ll11l_opy_.remove(bstack1l11ll11l_opy_.findall(bstack11111_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬષ"))[0])
      bstack1ll1l1ll11_opy_ = ET.Element(bstack11111_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭સ"), attrib={bstack11111_opy_ (u"ࠨࡰࡤࡱࡪ࠭હ"): bstack11111_opy_ (u"ࠩࡖࡹ࡮ࡺࡥࡴࠩ઺"), bstack11111_opy_ (u"ࠪ࡭ࡩ࠭઻"): bstack11111_opy_ (u"ࠫࡸ࠶઼ࠧ")})
      bstack1l11ll11l_opy_.insert(1, bstack1ll1l1ll11_opy_)
      bstack1ll11l1111_opy_ = None
      for suite in bstack1l11ll11l_opy_.iter(bstack11111_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫઽ")):
        bstack1ll11l1111_opy_ = suite
      bstack1ll11l1111_opy_.append(bstack1ll1111ll1_opy_)
      bstack1lll111l11_opy_ = None
      for status in bstack1ll1111ll1_opy_.iter(bstack11111_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ા")):
        bstack1lll111l11_opy_ = status
      bstack1ll11l1111_opy_.append(bstack1lll111l11_opy_)
    bstack1l1111ll_opy_.write(path)
  except Exception as e:
    logger.debug(bstack11111_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡥࡷࡹࡩ࡯ࡩࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡳ࡫ࡲࡢࡶ࡬ࡲ࡬ࠦࡲࡰࡤࡲࡸࠥࡸࡥࡱࡱࡵࡸࠬિ") + str(e))
def bstack1l11lll1ll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1llll1lll1_opy_
  global CONFIG
  if bstack11111_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࡱࡣࡷ࡬ࠧી") in options:
    del options[bstack11111_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࡲࡤࡸ࡭ࠨુ")]
  bstack1l1l1lll1_opy_ = bstack1ll111llll_opy_()
  for bstack1l1l1111ll_opy_ in bstack1l1l1lll1_opy_.keys():
    path = os.path.join(os.getcwd(), bstack11111_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࡡࡵࡩࡸࡻ࡬ࡵࡵࠪૂ"), str(bstack1l1l1111ll_opy_), bstack11111_opy_ (u"ࠫࡴࡻࡴࡱࡷࡷ࠲ࡽࡳ࡬ࠨૃ"))
    bstack1l1l11l1l1_opy_(path, bstack11l1lllll_opy_(bstack1l1l1lll1_opy_[bstack1l1l1111ll_opy_]))
  bstack1lllll111l_opy_()
  return bstack1llll1lll1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1ll111l1l1_opy_(self, ff_profile_dir):
  global bstack1ll11ll1_opy_
  if not ff_profile_dir:
    return None
  return bstack1ll11ll1_opy_(self, ff_profile_dir)
def bstack1lllll1ll1_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1llll1ll_opy_
  bstack1ll1ll1ll_opy_ = []
  if bstack11111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨૄ") in CONFIG:
    bstack1ll1ll1ll_opy_ = CONFIG[bstack11111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩૅ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack11111_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࠣ૆")],
      pabot_args[bstack11111_opy_ (u"ࠣࡸࡨࡶࡧࡵࡳࡦࠤે")],
      argfile,
      pabot_args.get(bstack11111_opy_ (u"ࠤ࡫࡭ࡻ࡫ࠢૈ")),
      pabot_args[bstack11111_opy_ (u"ࠥࡴࡷࡵࡣࡦࡵࡶࡩࡸࠨૉ")],
      platform[0],
      bstack1llll1ll_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack11111_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹ࡬ࡩ࡭ࡧࡶࠦ૊")] or [(bstack11111_opy_ (u"ࠧࠨો"), None)]
    for platform in enumerate(bstack1ll1ll1ll_opy_)
  ]
def bstack11lll11l_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1l1l1ll11l_opy_=bstack11111_opy_ (u"࠭ࠧૌ")):
  global bstack1l1l111l1_opy_
  self.platform_index = platform_index
  self.bstack1l1l111ll1_opy_ = bstack1l1l1ll11l_opy_
  bstack1l1l111l1_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack111llll11_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1l1l1l1111_opy_
  global bstack111ll1l11_opy_
  if not bstack11111_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦ્ࠩ") in item.options:
    item.options[bstack11111_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪ૎")] = []
  for v in item.options[bstack11111_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ૏")]:
    if bstack11111_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡓࡐࡆ࡚ࡆࡐࡔࡐࡍࡓࡊࡅ࡙ࠩૐ") in v:
      item.options[bstack11111_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭૑")].remove(v)
    if bstack11111_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡈࡒࡉࡂࡔࡊࡗࠬ૒") in v:
      item.options[bstack11111_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨ૓")].remove(v)
  item.options[bstack11111_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩ૔")].insert(0, bstack11111_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡑࡎࡄࡘࡋࡕࡒࡎࡋࡑࡈࡊ࡞࠺ࡼࡿࠪ૕").format(item.platform_index))
  item.options[bstack11111_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ૖")].insert(0, bstack11111_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡇࡉࡋࡒࡏࡄࡃࡏࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘ࠺ࡼࡿࠪ૗").format(item.bstack1l1l111ll1_opy_))
  if bstack111ll1l11_opy_:
    item.options[bstack11111_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭૘")].insert(0, bstack11111_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡈࡒࡉࡂࡔࡊࡗ࠿ࢁࡽࠨ૙").format(bstack111ll1l11_opy_))
  return bstack1l1l1l1111_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack111l11l11_opy_(command, item_index):
  if bstack11111111_opy_.get_property(bstack11111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ૚")):
    os.environ[bstack11111_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨ૛")] = json.dumps(CONFIG[bstack11111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ૜")][item_index % bstack1ll111l1l_opy_])
  global bstack111ll1l11_opy_
  if bstack111ll1l11_opy_:
    command[0] = command[0].replace(bstack11111_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ૝"), bstack11111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡶࡨࡰࠦࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠠ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽࠦࠧ૞") + str(
      item_index) + bstack11111_opy_ (u"ࠫࠥ࠭૟") + bstack111ll1l11_opy_, 1)
  else:
    command[0] = command[0].replace(bstack11111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫૠ"),
                                    bstack11111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡹࡤ࡬ࠢࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠣ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤ࡯ࡴࡦ࡯ࡢ࡭ࡳࡪࡥࡹࠢࠪૡ") + str(item_index), 1)
def bstack111ll11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1l1ll11ll_opy_
  bstack111l11l11_opy_(command, item_index)
  return bstack1l1ll11ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1l1llll111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1l1ll11ll_opy_
  bstack111l11l11_opy_(command, item_index)
  return bstack1l1ll11ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1lll1ll11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1l1ll11ll_opy_
  bstack111l11l11_opy_(command, item_index)
  return bstack1l1ll11ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack1lll1111ll_opy_(self, runner, quiet=False, capture=True):
  global bstack1l1ll111l_opy_
  bstack11111l1l_opy_ = bstack1l1ll111l_opy_(self, runner, quiet=False, capture=True)
  if self.exception:
    if not hasattr(runner, bstack11111_opy_ (u"ࠧࡦࡺࡦࡩࡵࡺࡩࡰࡰࡢࡥࡷࡸࠧૢ")):
      runner.exception_arr = []
    if not hasattr(runner, bstack11111_opy_ (u"ࠨࡧࡻࡧࡤࡺࡲࡢࡥࡨࡦࡦࡩ࡫ࡠࡣࡵࡶࠬૣ")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack11111l1l_opy_
def bstack1l1lll1l11_opy_(self, name, context, *args):
  os.environ[bstack11111_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪ૤")] = json.dumps(CONFIG[bstack11111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭૥")][int(threading.current_thread()._name) % bstack1ll111l1l_opy_])
  global bstack1l1lllll1_opy_
  if name == bstack11111_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠬ૦"):
    bstack1l1lllll1_opy_(self, name, context, *args)
    try:
      if not bstack1ll1lll1l_opy_:
        bstack111ll11l1_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll11l1lll_opy_(bstack11111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ૧")) else context.browser
        bstack1l1llll1ll_opy_ = str(self.feature.name)
        bstack11111ll11_opy_(context, bstack1l1llll1ll_opy_)
        bstack111ll11l1_opy_.execute_script(bstack11111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫ૨") + json.dumps(bstack1l1llll1ll_opy_) + bstack11111_opy_ (u"ࠧࡾࡿࠪ૩"))
      self.driver_before_scenario = False
    except Exception as e:
      logger.debug(bstack11111_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡪࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡪࡪࡧࡴࡶࡴࡨ࠾ࠥࢁࡽࠨ૪").format(str(e)))
  elif name == bstack11111_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ૫"):
    bstack1l1lllll1_opy_(self, name, context, *args)
    try:
      if not hasattr(self, bstack11111_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࡢࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ૬")):
        self.driver_before_scenario = True
      if (not bstack1ll1lll1l_opy_):
        scenario_name = args[0].name
        feature_name = bstack1l1llll1ll_opy_ = str(self.feature.name)
        bstack1l1llll1ll_opy_ = feature_name + bstack11111_opy_ (u"ࠫࠥ࠳ࠠࠨ૭") + scenario_name
        bstack111ll11l1_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll11l1lll_opy_(bstack11111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ૮")) else context.browser
        if self.driver_before_scenario:
          bstack11111ll11_opy_(context, bstack1l1llll1ll_opy_)
          bstack111ll11l1_opy_.execute_script(bstack11111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫ૯") + json.dumps(bstack1l1llll1ll_opy_) + bstack11111_opy_ (u"ࠧࡾࡿࠪ૰"))
    except Exception as e:
      logger.debug(bstack11111_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡪࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡨ࡫࡮ࡢࡴ࡬ࡳ࠿ࠦࡻࡾࠩ૱").format(str(e)))
  elif name == bstack11111_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪ૲"):
    try:
      bstack111l1l11l_opy_ = args[0].status.name
      bstack111ll11l1_opy_ = threading.current_thread().bstackSessionDriver if bstack11111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ૳") in threading.current_thread().__dict__.keys() else context.browser
      if str(bstack111l1l11l_opy_).lower() == bstack11111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ૴"):
        bstack1l11llll_opy_ = bstack11111_opy_ (u"ࠬ࠭૵")
        bstack11l11lll_opy_ = bstack11111_opy_ (u"࠭ࠧ૶")
        bstack1l111l1ll_opy_ = bstack11111_opy_ (u"ࠧࠨ૷")
        try:
          import traceback
          bstack1l11llll_opy_ = self.exception.__class__.__name__
          bstack1l1l1l1l11_opy_ = traceback.format_tb(self.exc_traceback)
          bstack11l11lll_opy_ = bstack11111_opy_ (u"ࠨࠢࠪ૸").join(bstack1l1l1l1l11_opy_)
          bstack1l111l1ll_opy_ = bstack1l1l1l1l11_opy_[-1]
        except Exception as e:
          logger.debug(bstack11111l1ll_opy_.format(str(e)))
        bstack1l11llll_opy_ += bstack1l111l1ll_opy_
        bstack1lll1ll1l_opy_(context, json.dumps(str(args[0].name) + bstack11111_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣૹ") + str(bstack11l11lll_opy_)),
                            bstack11111_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤૺ"))
        if self.driver_before_scenario:
          bstack11l1ll111_opy_(getattr(context, bstack11111_opy_ (u"ࠫࡵࡧࡧࡦࠩૻ"), None), bstack11111_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧૼ"), bstack1l11llll_opy_)
          bstack111ll11l1_opy_.execute_script(bstack11111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ૽") + json.dumps(str(args[0].name) + bstack11111_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨ૾") + str(bstack11l11lll_opy_)) + bstack11111_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨ૿"))
        if self.driver_before_scenario:
          bstack1ll1l1111_opy_(bstack111ll11l1_opy_, bstack11111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ଀"), bstack11111_opy_ (u"ࠥࡗࡨ࡫࡮ࡢࡴ࡬ࡳࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢଁ") + str(bstack1l11llll_opy_))
      else:
        bstack1lll1ll1l_opy_(context, bstack11111_opy_ (u"ࠦࡕࡧࡳࡴࡧࡧࠥࠧଂ"), bstack11111_opy_ (u"ࠧ࡯࡮ࡧࡱࠥଃ"))
        if self.driver_before_scenario:
          bstack11l1ll111_opy_(getattr(context, bstack11111_opy_ (u"࠭ࡰࡢࡩࡨࠫ଄"), None), bstack11111_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢଅ"))
        bstack111ll11l1_opy_.execute_script(bstack11111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭ଆ") + json.dumps(str(args[0].name) + bstack11111_opy_ (u"ࠤࠣ࠱ࠥࡖࡡࡴࡵࡨࡨࠦࠨଇ")) + bstack11111_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࡽࡾࠩଈ"))
        if self.driver_before_scenario:
          bstack1ll1l1111_opy_(bstack111ll11l1_opy_, bstack11111_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦଉ"))
    except Exception as e:
      logger.debug(bstack11111_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧଊ").format(str(e)))
  elif name == bstack11111_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭ଋ"):
    try:
      bstack111ll11l1_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll11l1lll_opy_(bstack11111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ଌ")) else context.browser
      if context.failed is True:
        bstack1111ll11l_opy_ = []
        bstack1l1lllllll_opy_ = []
        bstack111l1111_opy_ = []
        bstack1l1ll11111_opy_ = bstack11111_opy_ (u"ࠨࠩ଍")
        try:
          import traceback
          for exc in self.exception_arr:
            bstack1111ll11l_opy_.append(exc.__class__.__name__)
          for exc_tb in self.exc_traceback_arr:
            bstack1l1l1l1l11_opy_ = traceback.format_tb(exc_tb)
            bstack11lllll1l_opy_ = bstack11111_opy_ (u"ࠩࠣࠫ଎").join(bstack1l1l1l1l11_opy_)
            bstack1l1lllllll_opy_.append(bstack11lllll1l_opy_)
            bstack111l1111_opy_.append(bstack1l1l1l1l11_opy_[-1])
        except Exception as e:
          logger.debug(bstack11111l1ll_opy_.format(str(e)))
        bstack1l11llll_opy_ = bstack11111_opy_ (u"ࠪࠫଏ")
        for i in range(len(bstack1111ll11l_opy_)):
          bstack1l11llll_opy_ += bstack1111ll11l_opy_[i] + bstack111l1111_opy_[i] + bstack11111_opy_ (u"ࠫࡡࡴࠧଐ")
        bstack1l1ll11111_opy_ = bstack11111_opy_ (u"ࠬࠦࠧ଑").join(bstack1l1lllllll_opy_)
        if not self.driver_before_scenario:
          bstack1lll1ll1l_opy_(context, bstack1l1ll11111_opy_, bstack11111_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧ଒"))
          bstack11l1ll111_opy_(getattr(context, bstack11111_opy_ (u"ࠧࡱࡣࡪࡩࠬଓ"), None), bstack11111_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣଔ"), bstack1l11llll_opy_)
          bstack111ll11l1_opy_.execute_script(bstack11111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧକ") + json.dumps(bstack1l1ll11111_opy_) + bstack11111_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢࡾࡿࠪଖ"))
          bstack1ll1l1111_opy_(bstack111ll11l1_opy_, bstack11111_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦଗ"), bstack11111_opy_ (u"࡙ࠧ࡯࡮ࡧࠣࡷࡨ࡫࡮ࡢࡴ࡬ࡳࡸࠦࡦࡢ࡫࡯ࡩࡩࡀࠠ࡝ࡰࠥଘ") + str(bstack1l11llll_opy_))
          bstack1ll111ll1_opy_ = bstack1llll11ll_opy_(bstack1l1ll11111_opy_, self.feature.name, logger)
          if (bstack1ll111ll1_opy_ != None):
            bstack1l1ll1lll_opy_.append(bstack1ll111ll1_opy_)
      else:
        if not self.driver_before_scenario:
          bstack1lll1ll1l_opy_(context, bstack11111_opy_ (u"ࠨࡆࡦࡣࡷࡹࡷ࡫࠺ࠡࠤଙ") + str(self.feature.name) + bstack11111_opy_ (u"ࠢࠡࡲࡤࡷࡸ࡫ࡤࠢࠤଚ"), bstack11111_opy_ (u"ࠣ࡫ࡱࡪࡴࠨଛ"))
          bstack11l1ll111_opy_(getattr(context, bstack11111_opy_ (u"ࠩࡳࡥ࡬࡫ࠧଜ"), None), bstack11111_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥଝ"))
          bstack111ll11l1_opy_.execute_script(bstack11111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩଞ") + json.dumps(bstack11111_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࡀࠠࠣଟ") + str(self.feature.name) + bstack11111_opy_ (u"ࠨࠠࡱࡣࡶࡷࡪࡪࠡࠣଠ")) + bstack11111_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡯࡮ࡧࡱࠥࢁࢂ࠭ଡ"))
          bstack1ll1l1111_opy_(bstack111ll11l1_opy_, bstack11111_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨଢ"))
          bstack1ll111ll1_opy_ = bstack1llll11ll_opy_(bstack1l1ll11111_opy_, self.feature.name, logger)
          if (bstack1ll111ll1_opy_ != None):
            bstack1l1ll1lll_opy_.append(bstack1ll111ll1_opy_)
    except Exception as e:
      logger.debug(bstack11111_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࠦࡦࡦࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫଣ").format(str(e)))
  else:
    bstack1l1lllll1_opy_(self, name, context, *args)
  if name in [bstack11111_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠪତ"), bstack11111_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬଥ")]:
    bstack1l1lllll1_opy_(self, name, context, *args)
    if (name == bstack11111_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ଦ") and self.driver_before_scenario) or (
            name == bstack11111_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭ଧ") and not self.driver_before_scenario):
      try:
        bstack111ll11l1_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll11l1lll_opy_(bstack11111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ନ")) else context.browser
        bstack111ll11l1_opy_.quit()
      except Exception:
        pass
def bstack111ll11ll_opy_(config, startdir):
  return bstack11111_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡾ࠴ࢂࠨ଩").format(bstack11111_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣପ"))
notset = Notset()
def bstack1ll111ll1l_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1lll1lll_opy_
  if str(name).lower() == bstack11111_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࠪଫ"):
    return bstack11111_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥବ")
  else:
    return bstack1lll1lll_opy_(self, name, default, skip)
def bstack1lll1111_opy_(item, when):
  global bstack1ll1lll111_opy_
  try:
    bstack1ll1lll111_opy_(item, when)
  except Exception as e:
    pass
def bstack1l11111l1_opy_():
  return
def bstack1l1llllll1_opy_(type, name, status, reason, bstack1l1ll11l11_opy_, bstack1l11ll1l_opy_):
  bstack111l111l1_opy_ = {
    bstack11111_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬଭ"): type,
    bstack11111_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩମ"): {}
  }
  if type == bstack11111_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩଯ"):
    bstack111l111l1_opy_[bstack11111_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫର")][bstack11111_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ଱")] = bstack1l1ll11l11_opy_
    bstack111l111l1_opy_[bstack11111_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ଲ")][bstack11111_opy_ (u"ࠫࡩࡧࡴࡢࠩଳ")] = json.dumps(str(bstack1l11ll1l_opy_))
  if type == bstack11111_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭଴"):
    bstack111l111l1_opy_[bstack11111_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩଵ")][bstack11111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬଶ")] = name
  if type == bstack11111_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫଷ"):
    bstack111l111l1_opy_[bstack11111_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬସ")][bstack11111_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪହ")] = status
    if status == bstack11111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ଺"):
      bstack111l111l1_opy_[bstack11111_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ଻")][bstack11111_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ଼࠭")] = json.dumps(str(reason))
  bstack1ll1lll11l_opy_ = bstack11111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬଽ").format(json.dumps(bstack111l111l1_opy_))
  return bstack1ll1lll11l_opy_
def bstack111111l1_opy_(driver_command, response):
    if driver_command == bstack11111_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬା"):
        bstack11ll1l1l1_opy_.bstack11l1llll_opy_({
            bstack11111_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨି"): response[bstack11111_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩୀ")],
            bstack11111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫୁ"): bstack11ll1l1l1_opy_.current_test_uuid()
        })
def bstack1llll11l1l_opy_(item, call, rep):
  global bstack1l1111l1l_opy_
  global bstack1l1ll1llll_opy_
  global bstack1ll1lll1l_opy_
  name = bstack11111_opy_ (u"ࠬ࠭ୂ")
  try:
    if rep.when == bstack11111_opy_ (u"࠭ࡣࡢ࡮࡯ࠫୃ"):
      bstack1ll11l1ll1_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1ll1lll1l_opy_:
          name = str(rep.nodeid)
          bstack11llll11_opy_ = bstack1l1llllll1_opy_(bstack11111_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨୄ"), name, bstack11111_opy_ (u"ࠨࠩ୅"), bstack11111_opy_ (u"ࠩࠪ୆"), bstack11111_opy_ (u"ࠪࠫେ"), bstack11111_opy_ (u"ࠫࠬୈ"))
          threading.current_thread().bstack111l1lll_opy_ = name
          for driver in bstack1l1ll1llll_opy_:
            if bstack1ll11l1ll1_opy_ == driver.session_id:
              driver.execute_script(bstack11llll11_opy_)
      except Exception as e:
        logger.debug(bstack11111_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬ୉").format(str(e)))
      try:
        bstack1llllllll1_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack11111_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ୊"):
          status = bstack11111_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧୋ") if rep.outcome.lower() == bstack11111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨୌ") else bstack11111_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥ୍ࠩ")
          reason = bstack11111_opy_ (u"ࠪࠫ୎")
          if status == bstack11111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ୏"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack11111_opy_ (u"ࠬ࡯࡮ࡧࡱࠪ୐") if status == bstack11111_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭୑") else bstack11111_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭୒")
          data = name + bstack11111_opy_ (u"ࠨࠢࡳࡥࡸࡹࡥࡥࠣࠪ୓") if status == bstack11111_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ୔") else name + bstack11111_opy_ (u"ࠪࠤ࡫ࡧࡩ࡭ࡧࡧࠥࠥ࠭୕") + reason
          bstack11lll1111_opy_ = bstack1l1llllll1_opy_(bstack11111_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭ୖ"), bstack11111_opy_ (u"ࠬ࠭ୗ"), bstack11111_opy_ (u"࠭ࠧ୘"), bstack11111_opy_ (u"ࠧࠨ୙"), level, data)
          for driver in bstack1l1ll1llll_opy_:
            if bstack1ll11l1ll1_opy_ == driver.session_id:
              driver.execute_script(bstack11lll1111_opy_)
      except Exception as e:
        logger.debug(bstack11111_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡩ࡯࡯ࡶࡨࡼࡹࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬ୚").format(str(e)))
  except Exception as e:
    logger.debug(bstack11111_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡴࡢࡶࡨࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿࢂ࠭୛").format(str(e)))
  bstack1l1111l1l_opy_(item, call, rep)
def bstack1ll111l1ll_opy_(driver, bstack11l1l111_opy_):
  PercySDK.screenshot(driver, bstack11l1l111_opy_)
def bstack11ll11l11_opy_(driver):
  if bstack11llll1ll_opy_.bstack111111ll_opy_() is True or bstack11llll1ll_opy_.capturing() is True:
    return
  bstack11llll1ll_opy_.bstack1ll11ll11l_opy_()
  while not bstack11llll1ll_opy_.bstack111111ll_opy_():
    bstack1l111lll_opy_ = bstack11llll1ll_opy_.bstack111ll111_opy_()
    bstack1ll111l1ll_opy_(driver, bstack1l111lll_opy_)
  bstack11llll1ll_opy_.bstack1ll1lllll_opy_()
def bstack1111ll111_opy_(sequence, driver_command, response = None, bstack11ll1l1l_opy_ = None, args = None):
    try:
      if sequence != bstack11111_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪଡ଼"):
        return
      if not CONFIG.get(bstack11111_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪଢ଼"), False):
        return
      bstack1l111lll_opy_ = bstack1ll1l11ll_opy_(threading.current_thread(), bstack11111_opy_ (u"ࠬࡶࡥࡳࡥࡼࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ୞"), None)
      for command in bstack1ll11lllll_opy_:
        if command == driver_command:
          for driver in bstack1l1ll1llll_opy_:
            bstack11ll11l11_opy_(driver)
      bstack1l11111l_opy_ = CONFIG.get(bstack11111_opy_ (u"࠭ࡰࡦࡴࡦࡽࡈࡧࡰࡵࡷࡵࡩࡒࡵࡤࡦࠩୟ"), bstack11111_opy_ (u"ࠢࡢࡷࡷࡳࠧୠ"))
      if driver_command in bstack11l111ll1_opy_[bstack1l11111l_opy_]:
        bstack11llll1ll_opy_.bstack1lll1111l1_opy_(bstack1l111lll_opy_, driver_command)
    except Exception as e:
      pass
def bstack1l1lllll1l_opy_(framework_name):
  global bstack1l1l1lll1l_opy_
  global bstack11l11l1ll_opy_
  global bstack1llll1111_opy_
  bstack1l1l1lll1l_opy_ = framework_name
  logger.info(bstack1lll1l1111_opy_.format(bstack1l1l1lll1l_opy_.split(bstack11111_opy_ (u"ࠨ࠯ࠪୡ"))[0]))
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack1111111ll_opy_:
      Service.start = bstack1ll1l11lll_opy_
      Service.stop = bstack111lll1l1_opy_
      webdriver.Remote.get = bstack1lllll1l1_opy_
      WebDriver.close = bstack1ll11111l_opy_
      WebDriver.quit = bstack1l11ll1l11_opy_
      webdriver.Remote.__init__ = bstack1l11ll1ll_opy_
      WebDriver.getAccessibilityResults = getAccessibilityResults
      WebDriver.get_accessibility_results = getAccessibilityResults
      WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
      WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
      WebDriver.performScan = perform_scan
      WebDriver.perform_scan = perform_scan
    if not bstack1111111ll_opy_ and bstack11ll1l1l1_opy_.on():
      webdriver.Remote.__init__ = bstack1llll1ll1_opy_
    WebDriver.execute = bstack111ll111l_opy_
    bstack11l11l1ll_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack1111111ll_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack1lllll11l_opy_
  except Exception as e:
    pass
  bstack1lllll111_opy_()
  if not bstack11l11l1ll_opy_:
    bstack1l1lll1111_opy_(bstack11111_opy_ (u"ࠤࡓࡥࡨࡱࡡࡨࡧࡶࠤࡳࡵࡴࠡ࡫ࡱࡷࡹࡧ࡬࡭ࡧࡧࠦୢ"), bstack1ll1ll1l11_opy_)
  if bstack1l11lllll_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack1lll11lll_opy_
    except Exception as e:
      logger.error(bstack1l11l1ll1_opy_.format(str(e)))
  if bstack1llllll111_opy_():
    bstack111l11lll_opy_(CONFIG, logger)
  if (bstack11111_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩୣ") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if CONFIG.get(bstack11111_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ୤"), False):
          bstack1ll11l1ll_opy_(bstack1111ll111_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1ll111l1l1_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack111l1lll1_opy_
      except Exception as e:
        logger.warn(bstack1l1llll1_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack1l11lll11l_opy_
      except Exception as e:
        logger.debug(bstack1ll11l11l_opy_ + str(e))
    except Exception as e:
      bstack1l1lll1111_opy_(e, bstack1l1llll1_opy_)
    Output.start_test = bstack1ll1ll1111_opy_
    Output.end_test = bstack1ll111111_opy_
    TestStatus.__init__ = bstack1l1ll1l11l_opy_
    QueueItem.__init__ = bstack11lll11l_opy_
    pabot._create_items = bstack1lllll1ll1_opy_
    try:
      from pabot import __version__ as bstack1111111l_opy_
      if version.parse(bstack1111111l_opy_) >= version.parse(bstack11111_opy_ (u"ࠬ࠸࠮࠲࠷࠱࠴ࠬ୥")):
        pabot._run = bstack1lll1ll11l_opy_
      elif version.parse(bstack1111111l_opy_) >= version.parse(bstack11111_opy_ (u"࠭࠲࠯࠳࠶࠲࠵࠭୦")):
        pabot._run = bstack1l1llll111_opy_
      else:
        pabot._run = bstack111ll11l_opy_
    except Exception as e:
      pabot._run = bstack111ll11l_opy_
    pabot._create_command_for_execution = bstack111llll11_opy_
    pabot._report_results = bstack1l11lll1ll_opy_
  if bstack11111_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ୧") in str(framework_name).lower():
    if not bstack1111111ll_opy_:
      return
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l1lll1111_opy_(e, bstack11l1111ll_opy_)
    Runner.run_hook = bstack1l1lll1l11_opy_
    Step.run = bstack1lll1111ll_opy_
  if bstack11111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ୨") in str(framework_name).lower():
    if not bstack1111111ll_opy_:
      return
    try:
      if CONFIG.get(bstack11111_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ୩"), False):
          bstack1ll11l1ll_opy_(bstack1111ll111_opy_)
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
def bstack1l1llll1l1_opy_():
  global CONFIG
  if bstack11111_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ୪") in CONFIG and int(CONFIG[bstack11111_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ୫")]) > 1:
    logger.warn(bstack11ll1l11_opy_)
def bstack1l1l11l11l_opy_(arg, bstack11l11llll_opy_, bstack1ll1l1llll_opy_=None):
  global CONFIG
  global bstack1l1l11llll_opy_
  global bstack1111l1l11_opy_
  global bstack1111111ll_opy_
  global bstack11111111_opy_
  bstack1l1lll11l_opy_ = bstack11111_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ୬")
  if bstack11l11llll_opy_ and isinstance(bstack11l11llll_opy_, str):
    bstack11l11llll_opy_ = eval(bstack11l11llll_opy_)
  CONFIG = bstack11l11llll_opy_[bstack11111_opy_ (u"࠭ࡃࡐࡐࡉࡍࡌ࠭୭")]
  bstack1l1l11llll_opy_ = bstack11l11llll_opy_[bstack11111_opy_ (u"ࠧࡉࡗࡅࡣ࡚ࡘࡌࠨ୮")]
  bstack1111l1l11_opy_ = bstack11l11llll_opy_[bstack11111_opy_ (u"ࠨࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ୯")]
  bstack1111111ll_opy_ = bstack11l11llll_opy_[bstack11111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬ୰")]
  bstack11111111_opy_.bstack1l1l1111_opy_(bstack11111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫୱ"), bstack1111111ll_opy_)
  os.environ[bstack11111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭୲")] = bstack1l1lll11l_opy_
  os.environ[bstack11111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࠫ୳")] = json.dumps(CONFIG)
  os.environ[bstack11111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡎࡕࡃࡡࡘࡖࡑ࠭୴")] = bstack1l1l11llll_opy_
  os.environ[bstack11111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ୵")] = str(bstack1111l1l11_opy_)
  os.environ[bstack11111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑ࡛ࡗࡉࡘ࡚࡟ࡑࡎࡘࡋࡎࡔࠧ୶")] = str(True)
  if bstack11l11111l_opy_(arg, [bstack11111_opy_ (u"ࠩ࠰ࡲࠬ୷"), bstack11111_opy_ (u"ࠪ࠱࠲ࡴࡵ࡮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ୸")]) != -1:
    os.environ[bstack11111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡆࡘࡁࡍࡎࡈࡐࠬ୹")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack1lll1lllll_opy_)
    return
  bstack1lll111lll_opy_()
  global bstack111111111_opy_
  global bstack11l1ll1ll_opy_
  global bstack1llll1ll_opy_
  global bstack111ll1l11_opy_
  global bstack1l1111111_opy_
  global bstack1llll1111_opy_
  global bstack1l1lll11_opy_
  arg.append(bstack11111_opy_ (u"ࠧ࠳ࡗࠣ୺"))
  arg.append(bstack11111_opy_ (u"ࠨࡩࡨࡰࡲࡶࡪࡀࡍࡰࡦࡸࡰࡪࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡪ࡯ࡳࡳࡷࡺࡥࡥ࠼ࡳࡽࡹ࡫ࡳࡵ࠰ࡓࡽࡹ࡫ࡳࡵ࡙ࡤࡶࡳ࡯࡮ࡨࠤ୻"))
  arg.append(bstack11111_opy_ (u"ࠢ࠮࡙ࠥ୼"))
  arg.append(bstack11111_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡥ࠻ࡖ࡫ࡩࠥ࡮࡯ࡰ࡭࡬ࡱࡵࡲࠢ୽"))
  global bstack1l1l1ll111_opy_
  global bstack1ll11ll11_opy_
  global bstack11l1llll1_opy_
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
    bstack11l1llll1_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack1lll111ll_opy_(CONFIG) and bstack1ll111l11l_opy_():
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
    logger.debug(bstack11111_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡱࠣࡶࡺࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࡵࠪ୾"))
  bstack1llll1ll_opy_ = CONFIG.get(bstack11111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ୿"), {}).get(bstack11111_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭஀"))
  bstack1l1lll11_opy_ = True
  bstack1l1lllll1l_opy_(bstack1llll1ll11_opy_)
  os.environ[bstack11111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭஁")] = CONFIG[bstack11111_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨஂ")]
  os.environ[bstack11111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪஃ")] = CONFIG[bstack11111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ஄")]
  os.environ[bstack11111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬஅ")] = bstack1111111ll_opy_.__str__()
  from _pytest.config import main as bstack1ll1ll11l1_opy_
  bstack1ll1ll11l1_opy_(arg)
  if bstack11111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺࠧஆ") in multiprocessing.current_process().__dict__.keys():
    for bstack1l11l111_opy_ in multiprocessing.current_process().bstack_error_list:
      bstack1ll1l1llll_opy_.append(bstack1l11l111_opy_)
def bstack1ll1ll1ll1_opy_(arg):
  bstack1l1lllll1l_opy_(bstack1l111l11l_opy_)
  os.environ[bstack11111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬஇ")] = str(bstack1111l1l11_opy_)
  from behave.__main__ import main as bstack11l1l1ll_opy_
  bstack11l1l1ll_opy_(arg)
def bstack11ll1lll1_opy_():
  logger.info(bstack1ll1ll1l1l_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack11111_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫஈ"), help=bstack11111_opy_ (u"࠭ࡇࡦࡰࡨࡶࡦࡺࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡤࡱࡱࡪ࡮࡭ࠧஉ"))
  parser.add_argument(bstack11111_opy_ (u"ࠧ࠮ࡷࠪஊ"), bstack11111_opy_ (u"ࠨ࠯࠰ࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬ஋"), help=bstack11111_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡵࡴࡧࡵࡲࡦࡳࡥࠨ஌"))
  parser.add_argument(bstack11111_opy_ (u"ࠪ࠱ࡰ࠭஍"), bstack11111_opy_ (u"ࠫ࠲࠳࡫ࡦࡻࠪஎ"), help=bstack11111_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡤࡧࡨ࡫ࡳࡴࠢ࡮ࡩࡾ࠭ஏ"))
  parser.add_argument(bstack11111_opy_ (u"࠭࠭ࡧࠩஐ"), bstack11111_opy_ (u"ࠧ࠮࠯ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ஑"), help=bstack11111_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧஒ"))
  bstack11lllllll_opy_ = parser.parse_args()
  try:
    bstack1lll11ll11_opy_ = bstack11111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡩࡨࡲࡪࡸࡩࡤ࠰ࡼࡱࡱ࠴ࡳࡢ࡯ࡳࡰࡪ࠭ஓ")
    if bstack11lllllll_opy_.framework and bstack11lllllll_opy_.framework not in (bstack11111_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪஔ"), bstack11111_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬக")):
      bstack1lll11ll11_opy_ = bstack11111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠮ࡺ࡯࡯࠲ࡸࡧ࡭ࡱ࡮ࡨࠫ஖")
    bstack1lll1l111l_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1lll11ll11_opy_)
    bstack1l1ll11ll1_opy_ = open(bstack1lll1l111l_opy_, bstack11111_opy_ (u"࠭ࡲࠨ஗"))
    bstack11l111ll_opy_ = bstack1l1ll11ll1_opy_.read()
    bstack1l1ll11ll1_opy_.close()
    if bstack11lllllll_opy_.username:
      bstack11l111ll_opy_ = bstack11l111ll_opy_.replace(bstack11111_opy_ (u"࡚ࠧࡑࡘࡖࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧ஘"), bstack11lllllll_opy_.username)
    if bstack11lllllll_opy_.key:
      bstack11l111ll_opy_ = bstack11l111ll_opy_.replace(bstack11111_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪங"), bstack11lllllll_opy_.key)
    if bstack11lllllll_opy_.framework:
      bstack11l111ll_opy_ = bstack11l111ll_opy_.replace(bstack11111_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪச"), bstack11lllllll_opy_.framework)
    file_name = bstack11111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭஛")
    file_path = os.path.abspath(file_name)
    bstack1111l1ll_opy_ = open(file_path, bstack11111_opy_ (u"ࠫࡼ࠭ஜ"))
    bstack1111l1ll_opy_.write(bstack11l111ll_opy_)
    bstack1111l1ll_opy_.close()
    logger.info(bstack1llll111l_opy_)
    try:
      os.environ[bstack11111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ஝")] = bstack11lllllll_opy_.framework if bstack11lllllll_opy_.framework != None else bstack11111_opy_ (u"ࠨࠢஞ")
      config = yaml.safe_load(bstack11l111ll_opy_)
      config[bstack11111_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧட")] = bstack11111_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡵࡨࡸࡺࡶࠧ஠")
      bstack1ll11l1l11_opy_(bstack1ll1111lll_opy_, config)
    except Exception as e:
      logger.debug(bstack1llll111_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack11111lll1_opy_.format(str(e)))
def bstack1ll11l1l11_opy_(bstack1ll11lll_opy_, config, bstack1llllll1ll_opy_={}):
  global bstack1111111ll_opy_
  global bstack111ll1l1l_opy_
  if not config:
    return
  bstack111l1l1ll_opy_ = bstack1l1l1ll1_opy_ if not bstack1111111ll_opy_ else (
    bstack1lll1l11_opy_ if bstack11111_opy_ (u"ࠩࡤࡴࡵ࠭஡") in config else bstack1l1ll11l1l_opy_)
  bstack1lll11l1l1_opy_ = False
  bstack1ll11l111l_opy_ = False
  if bstack1111111ll_opy_ is True:
      if bstack11111_opy_ (u"ࠪࡥࡵࡶࠧ஢") in config:
          bstack1lll11l1l1_opy_ = True
      else:
          bstack1ll11l111l_opy_ = True
  bstack1lllll11ll_opy_ = {
      bstack11111_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫண"): bstack11ll1l1l1_opy_.bstack1llll1111l_opy_(),
      bstack11111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬத"): bstack1ll1l11ll1_opy_.bstack1lllll11l1_opy_(config),
      bstack11111_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ஥"): config.get(bstack11111_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭஦"), False),
      bstack11111_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ஧"): bstack1ll11l111l_opy_,
      bstack11111_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨந"): bstack1lll11l1l1_opy_
  }
  data = {
    bstack11111_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬன"): config[bstack11111_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ப")],
    bstack11111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ஫"): config[bstack11111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ஬")],
    bstack11111_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ஭"): bstack1ll11lll_opy_,
    bstack11111_opy_ (u"ࠨࡦࡨࡸࡪࡩࡴࡦࡦࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬம"): os.environ.get(bstack11111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫய"), bstack111ll1l1l_opy_),
    bstack11111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬர"): bstack11l1ll11_opy_,
    bstack11111_opy_ (u"ࠫࡴࡶࡴࡪ࡯ࡤࡰࡤ࡮ࡵࡣࡡࡸࡶࡱ࠭ற"): bstack1l11l1111_opy_(),
    bstack11111_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨல"): {
      bstack11111_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫள"): str(config[bstack11111_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧழ")]) if bstack11111_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨவ") in config else bstack11111_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࠥஶ"),
      bstack11111_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩ࡛࡫ࡲࡴ࡫ࡲࡲࠬஷ"): sys.version,
      bstack11111_opy_ (u"ࠫࡷ࡫ࡦࡦࡴࡵࡩࡷ࠭ஸ"): bstack1l11ll1ll1_opy_(os.getenv(bstack11111_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠢஹ"), bstack11111_opy_ (u"ࠨࠢ஺"))),
      bstack11111_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࠩ஻"): bstack11111_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ஼"),
      bstack11111_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࠪ஽"): bstack111l1l1ll_opy_,
      bstack11111_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨா"): bstack1lllll11ll_opy_,
      bstack11111_opy_ (u"ࠫࡹ࡫ࡳࡵࡪࡸࡦࡤࡻࡵࡪࡦࠪி"): os.environ[bstack11111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪீ")],
      bstack11111_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩு"): bstack11l1ll1l1_opy_(os.environ.get(bstack11111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩூ"), bstack111ll1l1l_opy_)),
      bstack11111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ௃"): config[bstack11111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ௄")] if config[bstack11111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭௅")] else bstack11111_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࠧெ"),
      bstack11111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧே"): str(config[bstack11111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨை")]) if bstack11111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ௉") in config else bstack11111_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤொ"),
      bstack11111_opy_ (u"ࠩࡲࡷࠬோ"): sys.platform,
      bstack11111_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬௌ"): socket.gethostname()
    }
  }
  update(data[bstack11111_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹ்ࠧ")], bstack1llllll1ll_opy_)
  try:
    response = bstack1lll11l11l_opy_(bstack11111_opy_ (u"ࠬࡖࡏࡔࡖࠪ௎"), bstack1ll1l1lll1_opy_(bstack1lll1ll11_opy_), data, {
      bstack11111_opy_ (u"࠭ࡡࡶࡶ࡫ࠫ௏"): (config[bstack11111_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩௐ")], config[bstack11111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ௑")])
    })
    if response:
      logger.debug(bstack1lllll1l11_opy_.format(bstack1ll11lll_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack11ll111l1_opy_.format(str(e)))
def bstack1l11ll1ll1_opy_(framework):
  return bstack11111_opy_ (u"ࠤࡾࢁ࠲ࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࡿࢂࠨ௒").format(str(framework), __version__) if framework else bstack11111_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࡽࢀࠦ௓").format(
    __version__)
def bstack1lll111lll_opy_():
  global CONFIG
  global bstack11l111l1_opy_
  if bool(CONFIG):
    return
  try:
    bstack11111ll1l_opy_()
    logger.debug(bstack111llll1_opy_.format(str(CONFIG)))
    bstack11l111l1_opy_ = bstack1ll1l1l1_opy_.bstack1l111llll_opy_(CONFIG, bstack11l111l1_opy_)
    bstack11ll11111_opy_()
  except Exception as e:
    logger.error(bstack11111_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࡹࡵ࠲ࠠࡦࡴࡵࡳࡷࡀࠠࠣ௔") + str(e))
    sys.exit(1)
  sys.excepthook = bstack111l1ll11_opy_
  atexit.register(bstack111ll1lll_opy_)
  signal.signal(signal.SIGINT, bstack11111111l_opy_)
  signal.signal(signal.SIGTERM, bstack11111111l_opy_)
def bstack111l1ll11_opy_(exctype, value, traceback):
  global bstack1l1ll1llll_opy_
  try:
    for driver in bstack1l1ll1llll_opy_:
      bstack1ll1l1111_opy_(driver, bstack11111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ௕"), bstack11111_opy_ (u"ࠨࡓࡦࡵࡶ࡭ࡴࡴࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦ࡜࡯ࠤ௖") + str(value))
  except Exception:
    pass
  bstack1llll1l1l_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1llll1l1l_opy_(message=bstack11111_opy_ (u"ࠧࠨௗ"), bstack1lll11lll1_opy_ = False):
  global CONFIG
  bstack1111l11l1_opy_ = bstack11111_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡆࡺࡦࡩࡵࡺࡩࡰࡰࠪ௘") if bstack1lll11lll1_opy_ else bstack11111_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ௙")
  try:
    if message:
      bstack1llllll1ll_opy_ = {
        bstack1111l11l1_opy_ : str(message)
      }
      bstack1ll11l1l11_opy_(bstack1ll11llll_opy_, CONFIG, bstack1llllll1ll_opy_)
    else:
      bstack1ll11l1l11_opy_(bstack1ll11llll_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1l1l11111_opy_.format(str(e)))
def bstack1ll11l1l1l_opy_(bstack11l11l11l_opy_, size):
  bstack1ll1lll1_opy_ = []
  while len(bstack11l11l11l_opy_) > size:
    bstack1l11l11l1_opy_ = bstack11l11l11l_opy_[:size]
    bstack1ll1lll1_opy_.append(bstack1l11l11l1_opy_)
    bstack11l11l11l_opy_ = bstack11l11l11l_opy_[size:]
  bstack1ll1lll1_opy_.append(bstack11l11l11l_opy_)
  return bstack1ll1lll1_opy_
def bstack11l111lll_opy_(args):
  if bstack11111_opy_ (u"ࠪ࠱ࡲ࠭௚") in args and bstack11111_opy_ (u"ࠫࡵࡪࡢࠨ௛") in args:
    return True
  return False
def run_on_browserstack(bstack11ll1ll1_opy_=None, bstack1ll1l1llll_opy_=None, bstack1lll11l11_opy_=False):
  global CONFIG
  global bstack1l1l11llll_opy_
  global bstack1111l1l11_opy_
  global bstack111ll1l1l_opy_
  bstack1l1lll11l_opy_ = bstack11111_opy_ (u"ࠬ࠭௜")
  bstack1l1ll11lll_opy_(bstack1ll1ll111l_opy_, logger)
  if bstack11ll1ll1_opy_ and isinstance(bstack11ll1ll1_opy_, str):
    bstack11ll1ll1_opy_ = eval(bstack11ll1ll1_opy_)
  if bstack11ll1ll1_opy_:
    CONFIG = bstack11ll1ll1_opy_[bstack11111_opy_ (u"࠭ࡃࡐࡐࡉࡍࡌ࠭௝")]
    bstack1l1l11llll_opy_ = bstack11ll1ll1_opy_[bstack11111_opy_ (u"ࠧࡉࡗࡅࡣ࡚ࡘࡌࠨ௞")]
    bstack1111l1l11_opy_ = bstack11ll1ll1_opy_[bstack11111_opy_ (u"ࠨࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ௟")]
    bstack11111111_opy_.bstack1l1l1111_opy_(bstack11111_opy_ (u"ࠩࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ௠"), bstack1111l1l11_opy_)
    bstack1l1lll11l_opy_ = bstack11111_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ௡")
  if not bstack1lll11l11_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack1lll1lllll_opy_)
      return
    if sys.argv[1] == bstack11111_opy_ (u"ࠫ࠲࠳ࡶࡦࡴࡶ࡭ࡴࡴࠧ௢") or sys.argv[1] == bstack11111_opy_ (u"ࠬ࠳ࡶࠨ௣"):
      logger.info(bstack11111_opy_ (u"࠭ࡂࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡖࡹࡵࡪࡲࡲ࡙ࠥࡄࡌࠢࡹࡿࢂ࠭௤").format(__version__))
      return
    if sys.argv[1] == bstack11111_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭௥"):
      bstack11ll1lll1_opy_()
      return
  args = sys.argv
  bstack1lll111lll_opy_()
  global bstack111111111_opy_
  global bstack1ll111l1l_opy_
  global bstack1l1lll11_opy_
  global bstack1lll1l1l_opy_
  global bstack11l1ll1ll_opy_
  global bstack1llll1ll_opy_
  global bstack111ll1l11_opy_
  global bstack1ll1l1l1ll_opy_
  global bstack1l1111111_opy_
  global bstack1llll1111_opy_
  global bstack1ll1ll1l1_opy_
  bstack1ll111l1l_opy_ = len(CONFIG.get(bstack11111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ௦"), []))
  if not bstack1l1lll11l_opy_:
    if args[1] == bstack11111_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ௧") or args[1] == bstack11111_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠶ࠫ௨"):
      bstack1l1lll11l_opy_ = bstack11111_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ௩")
      args = args[2:]
    elif args[1] == bstack11111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ௪"):
      bstack1l1lll11l_opy_ = bstack11111_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ௫")
      args = args[2:]
    elif args[1] == bstack11111_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭௬"):
      bstack1l1lll11l_opy_ = bstack11111_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧ௭")
      args = args[2:]
    elif args[1] == bstack11111_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ௮"):
      bstack1l1lll11l_opy_ = bstack11111_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫ௯")
      args = args[2:]
    elif args[1] == bstack11111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ௰"):
      bstack1l1lll11l_opy_ = bstack11111_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ௱")
      args = args[2:]
    elif args[1] == bstack11111_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭௲"):
      bstack1l1lll11l_opy_ = bstack11111_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ௳")
      args = args[2:]
    else:
      if not bstack11111_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ௴") in CONFIG or str(CONFIG[bstack11111_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ௵")]).lower() in [bstack11111_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ௶"), bstack11111_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬ௷")]:
        bstack1l1lll11l_opy_ = bstack11111_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ௸")
        args = args[1:]
      elif str(CONFIG[bstack11111_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ௹")]).lower() == bstack11111_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭௺"):
        bstack1l1lll11l_opy_ = bstack11111_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ௻")
        args = args[1:]
      elif str(CONFIG[bstack11111_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ௼")]).lower() == bstack11111_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ௽"):
        bstack1l1lll11l_opy_ = bstack11111_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪ௾")
        args = args[1:]
      elif str(CONFIG[bstack11111_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ௿")]).lower() == bstack11111_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ఀ"):
        bstack1l1lll11l_opy_ = bstack11111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧఁ")
        args = args[1:]
      elif str(CONFIG[bstack11111_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫం")]).lower() == bstack11111_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩః"):
        bstack1l1lll11l_opy_ = bstack11111_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪఄ")
        args = args[1:]
      else:
        os.environ[bstack11111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭అ")] = bstack1l1lll11l_opy_
        bstack1ll1ll1lll_opy_(bstack11l11l11_opy_)
  os.environ[bstack11111_opy_ (u"ࠬࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࡠࡗࡖࡉࡉ࠭ఆ")] = bstack1l1lll11l_opy_
  bstack111ll1l1l_opy_ = bstack1l1lll11l_opy_
  global bstack1lll1l1lll_opy_
  if bstack11ll1ll1_opy_:
    try:
      os.environ[bstack11111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨఇ")] = bstack1l1lll11l_opy_
      bstack1ll11l1l11_opy_(bstack1ll1llll1_opy_, CONFIG)
    except Exception as e:
      logger.debug(bstack1l1l11111_opy_.format(str(e)))
  global bstack1l1l1ll111_opy_
  global bstack1ll11ll11_opy_
  global bstack1l11l1llll_opy_
  global bstack1l1l1ll1ll_opy_
  global bstack1llll111ll_opy_
  global bstack1l11lllll1_opy_
  global bstack1lll1l11l1_opy_
  global bstack1ll11ll1_opy_
  global bstack1l1ll11ll_opy_
  global bstack1l1l111l1_opy_
  global bstack1l1l1l1111_opy_
  global bstack1llllll11_opy_
  global bstack1l1lllll1_opy_
  global bstack1l1ll111l_opy_
  global bstack1l1ll1l111_opy_
  global bstack1l111111l_opy_
  global bstack1lll1lll_opy_
  global bstack1ll1lll111_opy_
  global bstack1llll1lll1_opy_
  global bstack1l1111l1l_opy_
  global bstack11l1llll1_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1l1l1ll111_opy_ = webdriver.Remote.__init__
    bstack1ll11ll11_opy_ = WebDriver.quit
    bstack1llllll11_opy_ = WebDriver.close
    bstack1l1ll1l111_opy_ = WebDriver.get
    bstack11l1llll1_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1lll1l1lll_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    global bstack11111l1l1_opy_
    from QWeb.keywords import browser
    bstack11111l1l1_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1lll111ll_opy_(CONFIG) and bstack1ll111l11l_opy_():
    if bstack1l1lll111l_opy_() < version.parse(bstack1l11l1lll1_opy_):
      logger.error(bstack11l1l1l11_opy_.format(bstack1l1lll111l_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1l111111l_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1l11l1ll1_opy_.format(str(e)))
  if not CONFIG.get(bstack11111_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡂࡷࡷࡳࡈࡧࡰࡵࡷࡵࡩࡑࡵࡧࡴࠩఈ"), False) and not bstack11ll1ll1_opy_:
    logger.info(bstack1l1lll11ll_opy_)
  if bstack1l1lll11l_opy_ != bstack11111_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨఉ") or (bstack1l1lll11l_opy_ == bstack11111_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩఊ") and not bstack11ll1ll1_opy_):
    bstack11l1l1l1l_opy_()
  if (bstack1l1lll11l_opy_ in [bstack11111_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩఋ"), bstack11111_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪఌ"), bstack11111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭఍")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1ll111l1l1_opy_
        bstack1l11lllll1_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack1l1llll1_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack1llll111ll_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack1ll11l11l_opy_ + str(e))
    except Exception as e:
      bstack1l1lll1111_opy_(e, bstack1l1llll1_opy_)
    if bstack1l1lll11l_opy_ != bstack11111_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧఎ"):
      bstack1lllll111l_opy_()
    bstack1l11l1llll_opy_ = Output.start_test
    bstack1l1l1ll1ll_opy_ = Output.end_test
    bstack1lll1l11l1_opy_ = TestStatus.__init__
    bstack1l1ll11ll_opy_ = pabot._run
    bstack1l1l111l1_opy_ = QueueItem.__init__
    bstack1l1l1l1111_opy_ = pabot._create_command_for_execution
    bstack1llll1lll1_opy_ = pabot._report_results
  if bstack1l1lll11l_opy_ == bstack11111_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧఏ"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l1lll1111_opy_(e, bstack11l1111ll_opy_)
    bstack1l1lllll1_opy_ = Runner.run_hook
    bstack1l1ll111l_opy_ = Step.run
  if bstack1l1lll11l_opy_ == bstack11111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨఐ"):
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
      logger.debug(bstack11111_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡱࠣࡶࡺࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࡵࠪ఑"))
  try:
    framework_name = bstack11111_opy_ (u"ࠪࡖࡴࡨ࡯ࡵࠩఒ") if bstack1l1lll11l_opy_ in [bstack11111_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪఓ"), bstack11111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫఔ"), bstack11111_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧక")] else bstack111l11ll1_opy_(bstack1l1lll11l_opy_)
    bstack11ll1l1l1_opy_.launch(CONFIG, {
      bstack11111_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠨఖ"): bstack11111_opy_ (u"ࠨࡽ࠳ࢁ࠲ࡩࡵࡤࡷࡰࡦࡪࡸࠧగ").format(framework_name) if bstack1l1lll11l_opy_ == bstack11111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩఘ") and bstack1ll1l11l1_opy_() else framework_name,
      bstack11111_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧఙ"): bstack11l1ll1l1_opy_(framework_name),
      bstack11111_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩచ"): __version__,
      bstack11111_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡷࡶࡩࡩ࠭ఛ"): bstack1l1lll11l_opy_
    })
  except Exception as e:
    logger.debug(bstack1lll1llll1_opy_.format(bstack11111_opy_ (u"࠭ࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭జ"), str(e)))
  if bstack1l1lll11l_opy_ in bstack1111111l1_opy_:
    try:
      framework_name = bstack11111_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ఝ") if bstack1l1lll11l_opy_ in [bstack11111_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧఞ"), bstack11111_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨట")] else bstack1l1lll11l_opy_
      if bstack1111111ll_opy_ and bstack11111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪఠ") in CONFIG and CONFIG[bstack11111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫడ")] == True:
        if bstack11111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬఢ") in CONFIG:
          os.environ[bstack11111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧణ")] = os.getenv(bstack11111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨత"), json.dumps(CONFIG[bstack11111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨథ")]))
          CONFIG[bstack11111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩద")].pop(bstack11111_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨధ"), None)
          CONFIG[bstack11111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫన")].pop(bstack11111_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪ఩"), None)
        bstack111l11l1_opy_, bstack1l1llll1l_opy_ = bstack1ll1l11ll1_opy_.bstack1llllllll_opy_(CONFIG, bstack1l1lll11l_opy_, bstack11l1ll1l1_opy_(framework_name), str(bstack1l1lll111l_opy_()))
        if not bstack111l11l1_opy_ is None:
          os.environ[bstack11111_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫప")] = bstack111l11l1_opy_
          os.environ[bstack11111_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡖࡈࡗ࡙ࡥࡒࡖࡐࡢࡍࡉ࠭ఫ")] = str(bstack1l1llll1l_opy_)
    except Exception as e:
      logger.debug(bstack1lll1llll1_opy_.format(bstack11111_opy_ (u"ࠨࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨబ"), str(e)))
  if bstack1l1lll11l_opy_ == bstack11111_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩభ"):
    bstack1l1lll11_opy_ = True
    if bstack11ll1ll1_opy_ and bstack1lll11l11_opy_:
      bstack1llll1ll_opy_ = CONFIG.get(bstack11111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧమ"), {}).get(bstack11111_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭య"))
      bstack1l1lllll1l_opy_(bstack1ll11ll1l1_opy_)
    elif bstack11ll1ll1_opy_:
      bstack1llll1ll_opy_ = CONFIG.get(bstack11111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩర"), {}).get(bstack11111_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨఱ"))
      global bstack1l1ll1llll_opy_
      try:
        if bstack11l111lll_opy_(bstack11ll1ll1_opy_[bstack11111_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪల")]) and multiprocessing.current_process().name == bstack11111_opy_ (u"ࠨ࠲ࠪళ"):
          bstack11ll1ll1_opy_[bstack11111_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬఴ")].remove(bstack11111_opy_ (u"ࠪ࠱ࡲ࠭వ"))
          bstack11ll1ll1_opy_[bstack11111_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧశ")].remove(bstack11111_opy_ (u"ࠬࡶࡤࡣࠩష"))
          bstack11ll1ll1_opy_[bstack11111_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩస")] = bstack11ll1ll1_opy_[bstack11111_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪహ")][0]
          with open(bstack11ll1ll1_opy_[bstack11111_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ఺")], bstack11111_opy_ (u"ࠩࡵࠫ఻")) as f:
            bstack111111l1l_opy_ = f.read()
          bstack1ll111111l_opy_ = bstack11111_opy_ (u"ࠥࠦࠧ࡬ࡲࡰ࡯ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡶࡨࡰࠦࡩ࡮ࡲࡲࡶࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡦ࠽ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡪ࠮ࡻࡾࠫ࠾ࠤ࡫ࡸ࡯࡮ࠢࡳࡨࡧࠦࡩ࡮ࡲࡲࡶࡹࠦࡐࡥࡤ࠾ࠤࡴ࡭࡟ࡥࡤࠣࡁࠥࡖࡤࡣ࠰ࡧࡳࡤࡨࡲࡦࡣ࡮࠿ࠏࡪࡥࡧࠢࡰࡳࡩࡥࡢࡳࡧࡤ࡯࠭ࡹࡥ࡭ࡨ࠯ࠤࡦࡸࡧ࠭ࠢࡷࡩࡲࡶ࡯ࡳࡣࡵࡽࠥࡃࠠ࠱ࠫ࠽ࠎࠥࠦࡴࡳࡻ࠽ࠎࠥࠦࠠࠡࡣࡵ࡫ࠥࡃࠠࡴࡶࡵࠬ࡮ࡴࡴࠩࡣࡵ࡫࠮࠱࠱࠱ࠫࠍࠤࠥ࡫ࡸࡤࡧࡳࡸࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡣࡶࠤࡪࡀࠊࠡࠢࠣࠤࡵࡧࡳࡴࠌࠣࠤࡴ࡭࡟ࡥࡤࠫࡷࡪࡲࡦ࠭ࡣࡵ࡫࠱ࡺࡥ࡮ࡲࡲࡶࡦࡸࡹࠪࠌࡓࡨࡧ࠴ࡤࡰࡡࡥࠤࡂࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠌࡓࡨࡧ࠴ࡤࡰࡡࡥࡶࡪࡧ࡫ࠡ࠿ࠣࡱࡴࡪ࡟ࡣࡴࡨࡥࡰࠐࡐࡥࡤࠫ࠭࠳ࡹࡥࡵࡡࡷࡶࡦࡩࡥࠩࠫ࡟ࡲࠧࠨ఼ࠢ").format(str(bstack11ll1ll1_opy_))
          bstack1l1ll1l1l1_opy_ = bstack1ll111111l_opy_ + bstack111111l1l_opy_
          bstack1111lll1_opy_ = bstack11ll1ll1_opy_[bstack11111_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧఽ")] + bstack11111_opy_ (u"ࠬࡥࡢࡴࡶࡤࡧࡰࡥࡴࡦ࡯ࡳ࠲ࡵࡿࠧా")
          with open(bstack1111lll1_opy_, bstack11111_opy_ (u"࠭ࡷࠨి")):
            pass
          with open(bstack1111lll1_opy_, bstack11111_opy_ (u"ࠢࡸ࠭ࠥీ")) as f:
            f.write(bstack1l1ll1l1l1_opy_)
          import subprocess
          bstack11llllll1_opy_ = subprocess.run([bstack11111_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࠣు"), bstack1111lll1_opy_])
          if os.path.exists(bstack1111lll1_opy_):
            os.unlink(bstack1111lll1_opy_)
          os._exit(bstack11llllll1_opy_.returncode)
        else:
          if bstack11l111lll_opy_(bstack11ll1ll1_opy_[bstack11111_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬూ")]):
            bstack11ll1ll1_opy_[bstack11111_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ృ")].remove(bstack11111_opy_ (u"ࠫ࠲ࡳࠧౄ"))
            bstack11ll1ll1_opy_[bstack11111_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ౅")].remove(bstack11111_opy_ (u"࠭ࡰࡥࡤࠪె"))
            bstack11ll1ll1_opy_[bstack11111_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪే")] = bstack11ll1ll1_opy_[bstack11111_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫై")][0]
          bstack1l1lllll1l_opy_(bstack1ll11ll1l1_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack11ll1ll1_opy_[bstack11111_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ౉")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack11111_opy_ (u"ࠪࡣࡤࡴࡡ࡮ࡧࡢࡣࠬొ")] = bstack11111_opy_ (u"ࠫࡤࡥ࡭ࡢ࡫ࡱࡣࡤ࠭ో")
          mod_globals[bstack11111_opy_ (u"ࠬࡥ࡟ࡧ࡫࡯ࡩࡤࡥࠧౌ")] = os.path.abspath(bstack11ll1ll1_opy_[bstack11111_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦ్ࠩ")])
          exec(open(bstack11ll1ll1_opy_[bstack11111_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ౎")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack11111_opy_ (u"ࠨࡅࡤࡹ࡬࡮ࡴࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠨ౏").format(str(e)))
          for driver in bstack1l1ll1llll_opy_:
            bstack1ll1l1llll_opy_.append({
              bstack11111_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ౐"): bstack11ll1ll1_opy_[bstack11111_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭౑")],
              bstack11111_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ౒"): str(e),
              bstack11111_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ౓"): multiprocessing.current_process().name
            })
            bstack1ll1l1111_opy_(driver, bstack11111_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭౔"), bstack11111_opy_ (u"ࠢࡔࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠ࡝ࡰౕࠥ") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1l1ll1llll_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1111l1l11_opy_, CONFIG, logger)
      bstack1l1l1l1ll1_opy_()
      bstack1l1llll1l1_opy_()
      bstack11l11llll_opy_ = {
        bstack11111_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨౖࠫ"): args[0],
        bstack11111_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩ౗"): CONFIG,
        bstack11111_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫౘ"): bstack1l1l11llll_opy_,
        bstack11111_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ౙ"): bstack1111l1l11_opy_
      }
      percy.bstack1l1l111l_opy_()
      if bstack11111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨౚ") in CONFIG:
        bstack1ll111l11_opy_ = []
        manager = multiprocessing.Manager()
        bstack1l1l11lll1_opy_ = manager.list()
        if bstack11l111lll_opy_(args):
          for index, platform in enumerate(CONFIG[bstack11111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ౛")]):
            if index == 0:
              bstack11l11llll_opy_[bstack11111_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ౜")] = args
            bstack1ll111l11_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack11l11llll_opy_, bstack1l1l11lll1_opy_)))
        else:
          for index, platform in enumerate(CONFIG[bstack11111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫౝ")]):
            bstack1ll111l11_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack11l11llll_opy_, bstack1l1l11lll1_opy_)))
        for t in bstack1ll111l11_opy_:
          t.start()
        for t in bstack1ll111l11_opy_:
          t.join()
        bstack1ll1l1l1ll_opy_ = list(bstack1l1l11lll1_opy_)
      else:
        if bstack11l111lll_opy_(args):
          bstack11l11llll_opy_[bstack11111_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ౞")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack11l11llll_opy_,))
          test.start()
          test.join()
        else:
          bstack1l1lllll1l_opy_(bstack1ll11ll1l1_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack11111_opy_ (u"ࠪࡣࡤࡴࡡ࡮ࡧࡢࡣࠬ౟")] = bstack11111_opy_ (u"ࠫࡤࡥ࡭ࡢ࡫ࡱࡣࡤ࠭ౠ")
          mod_globals[bstack11111_opy_ (u"ࠬࡥ࡟ࡧ࡫࡯ࡩࡤࡥࠧౡ")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1l1lll11l_opy_ == bstack11111_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬౢ") or bstack1l1lll11l_opy_ == bstack11111_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ౣ"):
    percy.init(bstack1111l1l11_opy_, CONFIG, logger)
    percy.bstack1l1l111l_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack1l1lll1111_opy_(e, bstack1l1llll1_opy_)
    bstack1l1l1l1ll1_opy_()
    bstack1l1lllll1l_opy_(bstack1lll1l1l11_opy_)
    if bstack1111111ll_opy_ and bstack11111_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭౤") in args:
      i = args.index(bstack11111_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧ౥"))
      args.pop(i)
      args.pop(i)
    if bstack1111111ll_opy_:
      args.insert(0, str(bstack111111111_opy_))
      args.insert(0, str(bstack11111_opy_ (u"ࠪ࠱࠲ࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨ౦")))
    if bstack11ll1l1l1_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack1l1ll1111_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack11l1l1111_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack11111_opy_ (u"ࠦࡗࡕࡂࡐࡖࡢࡓࡕ࡚ࡉࡐࡐࡖࠦ౧"),
        ).parse_args(bstack1l1ll1111_opy_)
        args.insert(args.index(bstack11l1l1111_opy_[0]), str(bstack11111_opy_ (u"ࠬ࠳࠭࡭࡫ࡶࡸࡪࡴࡥࡳࠩ౨")))
        args.insert(args.index(bstack11l1l1111_opy_[0]), str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡲࡰࡤࡲࡸࡤࡲࡩࡴࡶࡨࡲࡪࡸ࠮ࡱࡻࠪ౩"))))
        if bstack1ll1ll11_opy_(os.environ.get(bstack11111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࠬ౪"))) and str(os.environ.get(bstack11111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࡥࡔࡆࡕࡗࡗࠬ౫"), bstack11111_opy_ (u"ࠩࡱࡹࡱࡲࠧ౬"))) != bstack11111_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ౭"):
          for bstack11llll11l_opy_ in bstack11l1l1111_opy_:
            args.remove(bstack11llll11l_opy_)
          bstack1lll11l111_opy_ = os.environ.get(bstack11111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࡡࡗࡉࡘ࡚ࡓࠨ౮")).split(bstack11111_opy_ (u"ࠬ࠲ࠧ౯"))
          for bstack1l1ll1111l_opy_ in bstack1lll11l111_opy_:
            args.append(bstack1l1ll1111l_opy_)
      except Exception as e:
        logger.error(bstack11111_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡦࡺࡴࡢࡥ࡫࡭ࡳ࡭ࠠ࡭࡫ࡶࡸࡪࡴࡥࡳࠢࡩࡳࡷࠦࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠴ࠠࡆࡴࡵࡳࡷࠦ࠭ࠡࠤ౰").format(e))
    pabot.main(args)
  elif bstack1l1lll11l_opy_ == bstack11111_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨ౱"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1l1lll1111_opy_(e, bstack1l1llll1_opy_)
    for a in args:
      if bstack11111_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡑࡎࡄࡘࡋࡕࡒࡎࡋࡑࡈࡊ࡞ࠧ౲") in a:
        bstack11l1ll1ll_opy_ = int(a.split(bstack11111_opy_ (u"ࠩ࠽ࠫ౳"))[1])
      if bstack11111_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡇࡉࡋࡒࡏࡄࡃࡏࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧ౴") in a:
        bstack1llll1ll_opy_ = str(a.split(bstack11111_opy_ (u"ࠫ࠿࠭౵"))[1])
      if bstack11111_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡈࡒࡉࡂࡔࡊࡗࠬ౶") in a:
        bstack111ll1l11_opy_ = str(a.split(bstack11111_opy_ (u"࠭࠺ࠨ౷"))[1])
    bstack1ll1llll1l_opy_ = None
    if bstack11111_opy_ (u"ࠧ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽ࠭౸") in args:
      i = args.index(bstack11111_opy_ (u"ࠨ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢ࡭ࡹ࡫࡭ࡠ࡫ࡱࡨࡪࡾࠧ౹"))
      args.pop(i)
      bstack1ll1llll1l_opy_ = args.pop(i)
    if bstack1ll1llll1l_opy_ is not None:
      global bstack1l1l1lll_opy_
      bstack1l1l1lll_opy_ = bstack1ll1llll1l_opy_
    bstack1l1lllll1l_opy_(bstack1lll1l1l11_opy_)
    run_cli(args)
    if bstack11111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠭౺") in multiprocessing.current_process().__dict__.keys():
      for bstack1l11l111_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1ll1l1llll_opy_.append(bstack1l11l111_opy_)
  elif bstack1l1lll11l_opy_ == bstack11111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ౻"):
    percy.init(bstack1111l1l11_opy_, CONFIG, logger)
    percy.bstack1l1l111l_opy_()
    bstack11lll1l11_opy_ = bstack1l1lllll_opy_(args, logger, CONFIG, bstack1111111ll_opy_)
    bstack11lll1l11_opy_.bstack1111l111l_opy_()
    bstack1l1l1l1ll1_opy_()
    bstack1lll1l1l_opy_ = True
    bstack1llll1111_opy_ = bstack11lll1l11_opy_.bstack1l11llllll_opy_()
    bstack11lll1l11_opy_.bstack11l11llll_opy_(bstack1ll1lll1l_opy_)
    bstack1l1111111_opy_ = bstack11lll1l11_opy_.bstack1llll11ll1_opy_(bstack1l1l11l11l_opy_, {
      bstack11111_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬ౼"): bstack1l1l11llll_opy_,
      bstack11111_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ౽"): bstack1111l1l11_opy_,
      bstack11111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩ౾"): bstack1111111ll_opy_
    })
    bstack1ll1ll1l1_opy_ = 1 if len(bstack1l1111111_opy_) > 0 else 0
  elif bstack1l1lll11l_opy_ == bstack11111_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ౿"):
    try:
      from behave.__main__ import main as bstack11l1l1ll_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1l1lll1111_opy_(e, bstack11l1111ll_opy_)
    bstack1l1l1l1ll1_opy_()
    bstack1lll1l1l_opy_ = True
    bstack11l11ll1_opy_ = 1
    if bstack11111_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨಀ") in CONFIG:
      bstack11l11ll1_opy_ = CONFIG[bstack11111_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩಁ")]
    bstack1l1l1l1l_opy_ = int(bstack11l11ll1_opy_) * int(len(CONFIG[bstack11111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ಂ")]))
    config = Configuration(args)
    bstack11ll11ll1_opy_ = config.paths
    if len(bstack11ll11ll1_opy_) == 0:
      import glob
      pattern = bstack11111_opy_ (u"ࠫ࠯࠰࠯ࠫ࠰ࡩࡩࡦࡺࡵࡳࡧࠪಃ")
      bstack1l1ll1ll_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1l1ll1ll_opy_)
      config = Configuration(args)
      bstack11ll11ll1_opy_ = config.paths
    bstack111l11ll_opy_ = [os.path.normpath(item) for item in bstack11ll11ll1_opy_]
    bstack1ll11111ll_opy_ = [os.path.normpath(item) for item in args]
    bstack1l11ll111_opy_ = [item for item in bstack1ll11111ll_opy_ if item not in bstack111l11ll_opy_]
    import platform as pf
    if pf.system().lower() == bstack11111_opy_ (u"ࠬࡽࡩ࡯ࡦࡲࡻࡸ࠭಄"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack111l11ll_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1l11ll11l1_opy_)))
                    for bstack1l11ll11l1_opy_ in bstack111l11ll_opy_]
    bstack1llll11111_opy_ = []
    for spec in bstack111l11ll_opy_:
      bstack1l1l11l111_opy_ = []
      bstack1l1l11l111_opy_ += bstack1l11ll111_opy_
      bstack1l1l11l111_opy_.append(spec)
      bstack1llll11111_opy_.append(bstack1l1l11l111_opy_)
    execution_items = []
    for bstack1l1l11l111_opy_ in bstack1llll11111_opy_:
      for index, _ in enumerate(CONFIG[bstack11111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩಅ")]):
        item = {}
        item[bstack11111_opy_ (u"ࠧࡢࡴࡪࠫಆ")] = bstack11111_opy_ (u"ࠨࠢࠪಇ").join(bstack1l1l11l111_opy_)
        item[bstack11111_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨಈ")] = index
        execution_items.append(item)
    bstack1l11ll11ll_opy_ = bstack1ll11l1l1l_opy_(execution_items, bstack1l1l1l1l_opy_)
    for execution_item in bstack1l11ll11ll_opy_:
      bstack1ll111l11_opy_ = []
      for item in execution_item:
        bstack1ll111l11_opy_.append(bstack1l11l1l1l_opy_(name=str(item[bstack11111_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩಉ")]),
                                             target=bstack1ll1ll1ll1_opy_,
                                             args=(item[bstack11111_opy_ (u"ࠫࡦࡸࡧࠨಊ")],)))
      for t in bstack1ll111l11_opy_:
        t.start()
      for t in bstack1ll111l11_opy_:
        t.join()
  else:
    bstack1ll1ll1lll_opy_(bstack11l11l11_opy_)
  if not bstack11ll1ll1_opy_:
    bstack1l11llll11_opy_()
  bstack1ll1l1l1_opy_.bstack1l1l1ll11_opy_()
def browserstack_initialize(bstack11111l11l_opy_=None):
  run_on_browserstack(bstack11111l11l_opy_, None, True)
def bstack1l11llll11_opy_():
  global CONFIG
  global bstack111ll1l1l_opy_
  global bstack1ll1ll1l1_opy_
  bstack11ll1l1l1_opy_.stop()
  bstack11ll1l1l1_opy_.bstack1lll11111_opy_()
  if bstack1ll1l11ll1_opy_.bstack1lllll11l1_opy_(CONFIG):
    bstack1ll1l11ll1_opy_.bstack1lll111111_opy_()
  [bstack1ll1l111ll_opy_, bstack1lll111l1l_opy_] = bstack1lll11l1_opy_()
  if bstack1ll1l111ll_opy_ is not None and bstack1l1l111ll_opy_() != -1:
    sessions = bstack1l111l11_opy_(bstack1ll1l111ll_opy_)
    bstack11ll1111_opy_(sessions, bstack1lll111l1l_opy_)
  if bstack111ll1l1l_opy_ == bstack11111_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬಋ") and bstack1ll1ll1l1_opy_ != 0:
    sys.exit(bstack1ll1ll1l1_opy_)
def bstack111l11ll1_opy_(bstack111lllll_opy_):
  if bstack111lllll_opy_:
    return bstack111lllll_opy_.capitalize()
  else:
    return bstack11111_opy_ (u"࠭ࠧಌ")
def bstack1llllll1l_opy_(bstack1l1l1ll1l1_opy_):
  if bstack11111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ಍") in bstack1l1l1ll1l1_opy_ and bstack1l1l1ll1l1_opy_[bstack11111_opy_ (u"ࠨࡰࡤࡱࡪ࠭ಎ")] != bstack11111_opy_ (u"ࠩࠪಏ"):
    return bstack1l1l1ll1l1_opy_[bstack11111_opy_ (u"ࠪࡲࡦࡳࡥࠨಐ")]
  else:
    bstack11ll1l111_opy_ = bstack11111_opy_ (u"ࠦࠧ಑")
    if bstack11111_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬಒ") in bstack1l1l1ll1l1_opy_ and bstack1l1l1ll1l1_opy_[bstack11111_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ಓ")] != None:
      bstack11ll1l111_opy_ += bstack1l1l1ll1l1_opy_[bstack11111_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧಔ")] + bstack11111_opy_ (u"ࠣ࠮ࠣࠦಕ")
      if bstack1l1l1ll1l1_opy_[bstack11111_opy_ (u"ࠩࡲࡷࠬಖ")] == bstack11111_opy_ (u"ࠥ࡭ࡴࡹࠢಗ"):
        bstack11ll1l111_opy_ += bstack11111_opy_ (u"ࠦ࡮ࡕࡓࠡࠤಘ")
      bstack11ll1l111_opy_ += (bstack1l1l1ll1l1_opy_[bstack11111_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩಙ")] or bstack11111_opy_ (u"࠭ࠧಚ"))
      return bstack11ll1l111_opy_
    else:
      bstack11ll1l111_opy_ += bstack111l11ll1_opy_(bstack1l1l1ll1l1_opy_[bstack11111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨಛ")]) + bstack11111_opy_ (u"ࠣࠢࠥಜ") + (
              bstack1l1l1ll1l1_opy_[bstack11111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫಝ")] or bstack11111_opy_ (u"ࠪࠫಞ")) + bstack11111_opy_ (u"ࠦ࠱ࠦࠢಟ")
      if bstack1l1l1ll1l1_opy_[bstack11111_opy_ (u"ࠬࡵࡳࠨಠ")] == bstack11111_opy_ (u"ࠨࡗࡪࡰࡧࡳࡼࡹࠢಡ"):
        bstack11ll1l111_opy_ += bstack11111_opy_ (u"ࠢࡘ࡫ࡱࠤࠧಢ")
      bstack11ll1l111_opy_ += bstack1l1l1ll1l1_opy_[bstack11111_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬಣ")] or bstack11111_opy_ (u"ࠩࠪತ")
      return bstack11ll1l111_opy_
def bstack11lll111_opy_(bstack1111l1lll_opy_):
  if bstack1111l1lll_opy_ == bstack11111_opy_ (u"ࠥࡨࡴࡴࡥࠣಥ"):
    return bstack11111_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡧࡳࡧࡨࡲࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡧࡳࡧࡨࡲࠧࡄࡃࡰ࡯ࡳࡰࡪࡺࡥࡥ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧದ")
  elif bstack1111l1lll_opy_ == bstack11111_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧಧ"):
    return bstack11111_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡴࡨࡨࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡲࡦࡦࠥࡂࡋࡧࡩ࡭ࡧࡧࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩನ")
  elif bstack1111l1lll_opy_ == bstack11111_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ಩"):
    return bstack11111_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽࡫ࡷ࡫ࡥ࡯࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥ࡫ࡷ࡫ࡥ࡯ࠤࡁࡔࡦࡹࡳࡦࡦ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨಪ")
  elif bstack1111l1lll_opy_ == bstack11111_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣಫ"):
    return bstack11111_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡸࡥࡥ࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡶࡪࡪࠢ࠿ࡇࡵࡶࡴࡸ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬಬ")
  elif bstack1111l1lll_opy_ == bstack11111_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸࠧಭ"):
    return bstack11111_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࠤࡧࡨࡥ࠸࠸࠶࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࠦࡩࡪࡧ࠳࠳࠸ࠥࡂ࡙࡯࡭ࡦࡱࡸࡸࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪಮ")
  elif bstack1111l1lll_opy_ == bstack11111_opy_ (u"ࠨࡲࡶࡰࡱ࡭ࡳ࡭ࠢಯ"):
    return bstack11111_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡥࡰࡦࡩ࡫࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡥࡰࡦࡩ࡫ࠣࡀࡕࡹࡳࡴࡩ࡯ࡩ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨರ")
  else:
    return bstack11111_opy_ (u"ࠨ࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡧࡲࡡࡤ࡭࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡧࡲࡡࡤ࡭ࠥࡂࠬಱ") + bstack111l11ll1_opy_(
      bstack1111l1lll_opy_) + bstack11111_opy_ (u"ࠩ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨಲ")
def bstack1111lll1l_opy_(session):
  return bstack11111_opy_ (u"ࠪࡀࡹࡸࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡳࡱࡺࠦࡃࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠠࡴࡧࡶࡷ࡮ࡵ࡮࠮ࡰࡤࡱࡪࠨ࠾࠽ࡣࠣ࡬ࡷ࡫ࡦ࠾ࠤࡾࢁࠧࠦࡴࡢࡴࡪࡩࡹࡃࠢࡠࡤ࡯ࡥࡳࡱࠢ࠿ࡽࢀࡀ࠴ࡧ࠾࠽࠱ࡷࡨࡃࢁࡽࡼࡿ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁ࠵ࡴࡳࡀࠪಳ").format(
    session[bstack11111_opy_ (u"ࠫࡵࡻࡢ࡭࡫ࡦࡣࡺࡸ࡬ࠨ಴")], bstack1llllll1l_opy_(session), bstack11lll111_opy_(session[bstack11111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡸࡺࡡࡵࡷࡶࠫವ")]),
    bstack11lll111_opy_(session[bstack11111_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ಶ")]),
    bstack111l11ll1_opy_(session[bstack11111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨಷ")] or session[bstack11111_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨಸ")] or bstack11111_opy_ (u"ࠩࠪಹ")) + bstack11111_opy_ (u"ࠥࠤࠧ಺") + (session[bstack11111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭಻")] or bstack11111_opy_ (u"಼ࠬ࠭")),
    session[bstack11111_opy_ (u"࠭࡯ࡴࠩಽ")] + bstack11111_opy_ (u"ࠢࠡࠤಾ") + session[bstack11111_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬಿ")], session[bstack11111_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫೀ")] or bstack11111_opy_ (u"ࠪࠫು"),
    session[bstack11111_opy_ (u"ࠫࡨࡸࡥࡢࡶࡨࡨࡤࡧࡴࠨೂ")] if session[bstack11111_opy_ (u"ࠬࡩࡲࡦࡣࡷࡩࡩࡥࡡࡵࠩೃ")] else bstack11111_opy_ (u"࠭ࠧೄ"))
def bstack11ll1111_opy_(sessions, bstack1lll111l1l_opy_):
  try:
    bstack11l1l11l1_opy_ = bstack11111_opy_ (u"ࠢࠣ೅")
    if not os.path.exists(bstack11lllll11_opy_):
      os.mkdir(bstack11lllll11_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11111_opy_ (u"ࠨࡣࡶࡷࡪࡺࡳ࠰ࡴࡨࡴࡴࡸࡴ࠯ࡪࡷࡱࡱ࠭ೆ")), bstack11111_opy_ (u"ࠩࡵࠫೇ")) as f:
      bstack11l1l11l1_opy_ = f.read()
    bstack11l1l11l1_opy_ = bstack11l1l11l1_opy_.replace(bstack11111_opy_ (u"ࠪࡿࠪࡘࡅࡔࡗࡏࡘࡘࡥࡃࡐࡗࡑࡘࠪࢃࠧೈ"), str(len(sessions)))
    bstack11l1l11l1_opy_ = bstack11l1l11l1_opy_.replace(bstack11111_opy_ (u"ࠫࢀࠫࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠧࢀࠫ೉"), bstack1lll111l1l_opy_)
    bstack11l1l11l1_opy_ = bstack11l1l11l1_opy_.replace(bstack11111_opy_ (u"ࠬࢁࠥࡃࡗࡌࡐࡉࡥࡎࡂࡏࡈࠩࢂ࠭ೊ"),
                                              sessions[0].get(bstack11111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤࡴࡡ࡮ࡧࠪೋ")) if sessions[0] else bstack11111_opy_ (u"ࠧࠨೌ"))
    with open(os.path.join(bstack11lllll11_opy_, bstack11111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡳࡧࡳࡳࡷࡺ࠮ࡩࡶࡰࡰ್ࠬ")), bstack11111_opy_ (u"ࠩࡺࠫ೎")) as stream:
      stream.write(bstack11l1l11l1_opy_.split(bstack11111_opy_ (u"ࠪࡿ࡙ࠪࡅࡔࡕࡌࡓࡓ࡙࡟ࡅࡃࡗࡅࠪࢃࠧ೏"))[0])
      for session in sessions:
        stream.write(bstack1111lll1l_opy_(session))
      stream.write(bstack11l1l11l1_opy_.split(bstack11111_opy_ (u"ࠫࢀࠫࡓࡆࡕࡖࡍࡔࡔࡓࡠࡆࡄࡘࡆࠫࡽࠨ೐"))[1])
    logger.info(bstack11111_opy_ (u"ࠬࡍࡥ࡯ࡧࡵࡥࡹ࡫ࡤࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡣࡷ࡬ࡰࡩࠦࡡࡳࡶ࡬ࡪࡦࡩࡴࡴࠢࡤࡸࠥࢁࡽࠨ೑").format(bstack11lllll11_opy_));
  except Exception as e:
    logger.debug(bstack1ll1ll1l_opy_.format(str(e)))
def bstack1l111l11_opy_(bstack1ll1l111ll_opy_):
  global CONFIG
  try:
    host = bstack11111_opy_ (u"࠭ࡡࡱ࡫࠰ࡧࡱࡵࡵࡥࠩ೒") if bstack11111_opy_ (u"ࠧࡢࡲࡳࠫ೓") in CONFIG else bstack11111_opy_ (u"ࠨࡣࡳ࡭ࠬ೔")
    user = CONFIG[bstack11111_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫೕ")]
    key = CONFIG[bstack11111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ೖ")]
    bstack1l11ll1lll_opy_ = bstack11111_opy_ (u"ࠫࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧࠪ೗") if bstack11111_opy_ (u"ࠬࡧࡰࡱࠩ೘") in CONFIG else bstack11111_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨ೙")
    url = bstack11111_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡽࢀ࠾ࢀࢃࡀࡼࡿ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁ࠴ࡹࡥࡴࡵ࡬ࡳࡳࡹ࠮࡫ࡵࡲࡲࠬ೚").format(user, key, host, bstack1l11ll1lll_opy_,
                                                                                bstack1ll1l111ll_opy_)
    headers = {
      bstack11111_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡷࡽࡵ࡫ࠧ೛"): bstack11111_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬ೜"),
    }
    proxies = bstack1lll1ll1l1_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstack11111_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨೝ")], response.json()))
  except Exception as e:
    logger.debug(bstack1l1lllll11_opy_.format(str(e)))
def bstack1lll11l1_opy_():
  global CONFIG
  global bstack11l1ll11_opy_
  try:
    if bstack11111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧೞ") in CONFIG:
      host = bstack11111_opy_ (u"ࠬࡧࡰࡪ࠯ࡦࡰࡴࡻࡤࠨ೟") if bstack11111_opy_ (u"࠭ࡡࡱࡲࠪೠ") in CONFIG else bstack11111_opy_ (u"ࠧࡢࡲ࡬ࠫೡ")
      user = CONFIG[bstack11111_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪೢ")]
      key = CONFIG[bstack11111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬೣ")]
      bstack1l11ll1lll_opy_ = bstack11111_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩ೤") if bstack11111_opy_ (u"ࠫࡦࡶࡰࠨ೥") in CONFIG else bstack11111_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ೦")
      url = bstack11111_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡼࡿ࠽ࡿࢂࡆࡻࡾ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠯࡬ࡶࡳࡳ࠭೧").format(user, key, host, bstack1l11ll1lll_opy_)
      headers = {
        bstack11111_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡶࡼࡴࡪ࠭೨"): bstack11111_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ೩"),
      }
      if bstack11111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ೪") in CONFIG:
        params = {bstack11111_opy_ (u"ࠪࡲࡦࡳࡥࠨ೫"): CONFIG[bstack11111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ೬")], bstack11111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ೭"): CONFIG[bstack11111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ೮")]}
      else:
        params = {bstack11111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ೯"): CONFIG[bstack11111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ೰")]}
      proxies = bstack1lll1ll1l1_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack1lll1l1l1l_opy_ = response.json()[0][bstack11111_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡢࡶ࡫࡯ࡨࠬೱ")]
        if bstack1lll1l1l1l_opy_:
          bstack1lll111l1l_opy_ = bstack1lll1l1l1l_opy_[bstack11111_opy_ (u"ࠪࡴࡺࡨ࡬ࡪࡥࡢࡹࡷࡲࠧೲ")].split(bstack11111_opy_ (u"ࠫࡵࡻࡢ࡭࡫ࡦ࠱ࡧࡻࡩ࡭ࡦࠪೳ"))[0] + bstack11111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡷ࠴࠭೴") + bstack1lll1l1l1l_opy_[
            bstack11111_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ೵")]
          logger.info(bstack111l111ll_opy_.format(bstack1lll111l1l_opy_))
          bstack11l1ll11_opy_ = bstack1lll1l1l1l_opy_[bstack11111_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ೶")]
          bstack1ll1l1l11_opy_ = CONFIG[bstack11111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ೷")]
          if bstack11111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ೸") in CONFIG:
            bstack1ll1l1l11_opy_ += bstack11111_opy_ (u"ࠪࠤࠬ೹") + CONFIG[bstack11111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭೺")]
          if bstack1ll1l1l11_opy_ != bstack1lll1l1l1l_opy_[bstack11111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ೻")]:
            logger.debug(bstack1111ll1ll_opy_.format(bstack1lll1l1l1l_opy_[bstack11111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ೼")], bstack1ll1l1l11_opy_))
          return [bstack1lll1l1l1l_opy_[bstack11111_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ೽")], bstack1lll111l1l_opy_]
    else:
      logger.warn(bstack11lll11l1_opy_)
  except Exception as e:
    logger.debug(bstack11l1l1l1_opy_.format(str(e)))
  return [None, None]
def bstack1llll1l11_opy_(url, bstack11llll111_opy_=False):
  global CONFIG
  global bstack1l1l1l1ll_opy_
  if not bstack1l1l1l1ll_opy_:
    hostname = bstack1lll11ll1l_opy_(url)
    is_private = bstack1l1l1l1l1l_opy_(hostname)
    if (bstack11111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ೾") in CONFIG and not bstack1ll1ll11_opy_(CONFIG[bstack11111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭೿")])) and (is_private or bstack11llll111_opy_):
      bstack1l1l1l1ll_opy_ = hostname
def bstack1lll11ll1l_opy_(url):
  return urlparse(url).hostname
def bstack1l1l1l1l1l_opy_(hostname):
  for bstack11lll111l_opy_ in bstack1ll1lll11_opy_:
    regex = re.compile(bstack11lll111l_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack1ll11l1lll_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def getAccessibilityResults(driver):
  global CONFIG
  global bstack11l1ll1ll_opy_
  bstack1lllllll11_opy_ = not (bstack1ll1l11ll_opy_(threading.current_thread(), bstack11111_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧഀ"), None) and bstack1ll1l11ll_opy_(
          threading.current_thread(), bstack11111_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪഁ"), None))
  bstack1llll1l1ll_opy_ = getattr(driver, bstack11111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬം"), None) != True
  if not bstack1ll1l11ll1_opy_.bstack1l1l1111l_opy_(CONFIG, bstack11l1ll1ll_opy_) or (bstack1llll1l1ll_opy_ and bstack1lllllll11_opy_):
    logger.warning(bstack11111_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳ࠯ࠤഃ"))
    return {}
  try:
    logger.debug(bstack11111_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠫഄ"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack1ll11l111_opy_.bstack1l11lll1l1_opy_)
    return results
  except Exception:
    logger.error(bstack11111_opy_ (u"ࠣࡐࡲࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡽࡥࡳࡧࠣࡪࡴࡻ࡮ࡥ࠰ࠥഅ"))
    return {}
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack11l1ll1ll_opy_
  bstack1lllllll11_opy_ = not (bstack1ll1l11ll_opy_(threading.current_thread(), bstack11111_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ആ"), None) and bstack1ll1l11ll_opy_(
          threading.current_thread(), bstack11111_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩഇ"), None))
  bstack1llll1l1ll_opy_ = getattr(driver, bstack11111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫഈ"), None) != True
  if not bstack1ll1l11ll1_opy_.bstack1l1l1111l_opy_(CONFIG, bstack11l1ll1ll_opy_) or (bstack1llll1l1ll_opy_ and bstack1lllllll11_opy_):
    logger.warning(bstack11111_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡴࡷࡰࡱࡦࡸࡹ࠯ࠤഉ"))
    return {}
  try:
    logger.debug(bstack11111_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡷࡺࡳ࡭ࡢࡴࡼࠫഊ"))
    logger.debug(perform_scan(driver))
    bstack1ll11llll1_opy_ = driver.execute_async_script(bstack1ll11l111_opy_.bstack111l1ll1_opy_)
    return bstack1ll11llll1_opy_
  except Exception:
    logger.error(bstack11111_opy_ (u"ࠢࡏࡱࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡺࡳ࡭ࡢࡴࡼࠤࡼࡧࡳࠡࡨࡲࡹࡳࡪ࠮ࠣഋ"))
    return {}
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack11l1ll1ll_opy_
  bstack1lllllll11_opy_ = not (bstack1ll1l11ll_opy_(threading.current_thread(), bstack11111_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬഌ"), None) and bstack1ll1l11ll_opy_(
          threading.current_thread(), bstack11111_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ഍"), None))
  bstack1llll1l1ll_opy_ = getattr(driver, bstack11111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪഎ"), None) != True
  if not bstack1ll1l11ll1_opy_.bstack1l1l1111l_opy_(CONFIG, bstack11l1ll1ll_opy_) or (bstack1llll1l1ll_opy_ and bstack1lllllll11_opy_):
    logger.warning(bstack11111_opy_ (u"ࠦࡓࡵࡴࠡࡣࡱࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣࡧࡦࡴ࡮ࡰࡶࠣࡶࡺࡴࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡥࡤࡲ࠳ࠨഏ"))
    return {}
  try:
    bstack1ll1lll1l1_opy_ = driver.execute_async_script(bstack1ll11l111_opy_.perform_scan, {bstack11111_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࠬഐ"): kwargs.get(bstack11111_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷࡥࡣࡰ࡯ࡰࡥࡳࡪࠧ഑"), None) or bstack11111_opy_ (u"ࠧࠨഒ")})
    return bstack1ll1lll1l1_opy_
  except Exception:
    logger.error(bstack11111_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡷࡻ࡮ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡦࡥࡳ࠴ࠢഓ"))
    return {}