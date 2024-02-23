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
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack1ll1l1lll1_opy_, bstack1lll11l11l_opy_
class bstack11l11111_opy_:
  working_dir = os.getcwd()
  bstack111l11111_opy_ = False
  config = {}
  binary_path = bstack11111_opy_ (u"ࠫࠬᎭ")
  bstack11111ll11l_opy_ = bstack11111_opy_ (u"ࠬ࠭Ꭾ")
  bstack11llll1ll_opy_ = False
  bstack1111llll11_opy_ = None
  bstack1111ll11ll_opy_ = {}
  bstack1111l1llll_opy_ = 300
  bstack1111l111l1_opy_ = False
  logger = None
  bstack1111ll1l1l_opy_ = False
  bstack1111l11lll_opy_ = bstack11111_opy_ (u"࠭ࠧᎯ")
  bstack111l11l111_opy_ = {
    bstack11111_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧᎰ") : 1,
    bstack11111_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹࠩᎱ") : 2,
    bstack11111_opy_ (u"ࠩࡨࡨ࡬࡫ࠧᎲ") : 3,
    bstack11111_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪᎳ") : 4
  }
  def __init__(self) -> None: pass
  def bstack111l11l11l_opy_(self):
    bstack111l111l1l_opy_ = bstack11111_opy_ (u"ࠫࠬᎴ")
    bstack11111llll1_opy_ = sys.platform
    bstack1111l1l1ll_opy_ = bstack11111_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫᎵ")
    if re.match(bstack11111_opy_ (u"ࠨࡤࡢࡴࡺ࡭ࡳࢂ࡭ࡢࡥࠣࡳࡸࠨᎶ"), bstack11111llll1_opy_) != None:
      bstack111l111l1l_opy_ = bstack11l1ll1111_opy_ + bstack11111_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠭ࡰࡵࡻ࠲ࡿ࡯ࡰࠣᎷ")
      self.bstack1111l11lll_opy_ = bstack11111_opy_ (u"ࠨ࡯ࡤࡧࠬᎸ")
    elif re.match(bstack11111_opy_ (u"ࠤࡰࡷࡼ࡯࡮ࡽ࡯ࡶࡽࡸࢂ࡭ࡪࡰࡪࡻࢁࡩࡹࡨࡹ࡬ࡲࢁࡨࡣࡤࡹ࡬ࡲࢁࡽࡩ࡯ࡥࡨࢀࡪࡳࡣࡽࡹ࡬ࡲ࠸࠸ࠢᎹ"), bstack11111llll1_opy_) != None:
      bstack111l111l1l_opy_ = bstack11l1ll1111_opy_ + bstack11111_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠰ࡻ࡮ࡴ࠮ࡻ࡫ࡳࠦᎺ")
      bstack1111l1l1ll_opy_ = bstack11111_opy_ (u"ࠦࡵ࡫ࡲࡤࡻ࠱ࡩࡽ࡫ࠢᎻ")
      self.bstack1111l11lll_opy_ = bstack11111_opy_ (u"ࠬࡽࡩ࡯ࠩᎼ")
    else:
      bstack111l111l1l_opy_ = bstack11l1ll1111_opy_ + bstack11111_opy_ (u"ࠨ࠯ࡱࡧࡵࡧࡾ࠳࡬ࡪࡰࡸࡼ࠳ࢀࡩࡱࠤᎽ")
      self.bstack1111l11lll_opy_ = bstack11111_opy_ (u"ࠧ࡭࡫ࡱࡹࡽ࠭Ꮎ")
    return bstack111l111l1l_opy_, bstack1111l1l1ll_opy_
  def bstack1111llllll_opy_(self):
    try:
      bstack1111l1111l_opy_ = [os.path.join(expanduser(bstack11111_opy_ (u"ࠣࢀࠥᎿ")), bstack11111_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᏀ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack1111l1111l_opy_:
        if(self.bstack1111ll1111_opy_(path)):
          return path
      raise bstack11111_opy_ (u"࡙ࠥࡳࡧ࡬ࡣࡧࠣࡸࡴࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠢᏁ")
    except Exception as e:
      self.logger.error(bstack11111_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥࠡࡲࡤࡸ࡭ࠦࡦࡰࡴࠣࡴࡪࡸࡣࡺࠢࡧࡳࡼࡴ࡬ࡰࡣࡧ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࠯ࠣࡿࢂࠨᏂ").format(e))
  def bstack1111ll1111_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack1111lll1l1_opy_(self, bstack111l111l1l_opy_, bstack1111l1l1ll_opy_):
    try:
      bstack1111l11l11_opy_ = self.bstack1111llllll_opy_()
      bstack1111l1l111_opy_ = os.path.join(bstack1111l11l11_opy_, bstack11111_opy_ (u"ࠬࡶࡥࡳࡥࡼ࠲ࡿ࡯ࡰࠨᏃ"))
      bstack1111l1l1l1_opy_ = os.path.join(bstack1111l11l11_opy_, bstack1111l1l1ll_opy_)
      if os.path.exists(bstack1111l1l1l1_opy_):
        self.logger.info(bstack11111_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡼࡿ࠯ࠤࡸࡱࡩࡱࡲ࡬ࡲ࡬ࠦࡤࡰࡹࡱࡰࡴࡧࡤࠣᏄ").format(bstack1111l1l1l1_opy_))
        return bstack1111l1l1l1_opy_
      if os.path.exists(bstack1111l1l111_opy_):
        self.logger.info(bstack11111_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡺࡪࡲࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࢁࡽ࠭ࠢࡸࡲࡿ࡯ࡰࡱ࡫ࡱ࡫ࠧᏅ").format(bstack1111l1l111_opy_))
        return self.bstack1111ll1l11_opy_(bstack1111l1l111_opy_, bstack1111l1l1ll_opy_)
      self.logger.info(bstack11111_opy_ (u"ࠣࡆࡲࡻࡳࡲ࡯ࡢࡦ࡬ࡲ࡬ࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥ࡬ࡲࡰ࡯ࠣࡿࢂࠨᏆ").format(bstack111l111l1l_opy_))
      response = bstack1lll11l11l_opy_(bstack11111_opy_ (u"ࠩࡊࡉ࡙࠭Ꮗ"), bstack111l111l1l_opy_, {}, {})
      if response.status_code == 200:
        with open(bstack1111l1l111_opy_, bstack11111_opy_ (u"ࠪࡻࡧ࠭Ꮘ")) as file:
          file.write(response.content)
        self.logger.info(bstack1111ll1lll_opy_ (u"ࠦࡉࡵࡷ࡯࡮ࡲࡥࡩ࡫ࡤࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡢࡰࡧࠤࡸࡧࡶࡦࡦࠣࡥࡹࠦࡻࡣ࡫ࡱࡥࡷࡿ࡟ࡻ࡫ࡳࡣࡵࡧࡴࡩࡿࠥᏉ"))
        return self.bstack1111ll1l11_opy_(bstack1111l1l111_opy_, bstack1111l1l1ll_opy_)
      else:
        raise(bstack1111ll1lll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠣࡸ࡭࡫ࠠࡧ࡫࡯ࡩ࠳ࠦࡓࡵࡣࡷࡹࡸࠦࡣࡰࡦࡨ࠾ࠥࢁࡲࡦࡵࡳࡳࡳࡹࡥ࠯ࡵࡷࡥࡹࡻࡳࡠࡥࡲࡨࡪࢃࠢᏊ"))
    except:
      self.logger.error(bstack11111_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠥᏋ"))
  def bstack1111lll111_opy_(self, bstack111l111l1l_opy_, bstack1111l1l1ll_opy_):
    try:
      bstack1111l1l1l1_opy_ = self.bstack1111lll1l1_opy_(bstack111l111l1l_opy_, bstack1111l1l1ll_opy_)
      bstack111l11ll1l_opy_ = self.bstack11111lllll_opy_(bstack111l111l1l_opy_, bstack1111l1l1ll_opy_, bstack1111l1l1l1_opy_)
      return bstack1111l1l1l1_opy_, bstack111l11ll1l_opy_
    except Exception as e:
      self.logger.error(bstack11111_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣ࡫ࡪࡺࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡰࡢࡶ࡫ࠦᏌ").format(e))
    return bstack1111l1l1l1_opy_, False
  def bstack11111lllll_opy_(self, bstack111l111l1l_opy_, bstack1111l1l1ll_opy_, bstack1111l1l1l1_opy_, bstack1111ll11l1_opy_ = 0):
    if bstack1111ll11l1_opy_ > 1:
      return False
    if bstack1111l1l1l1_opy_ == None or os.path.exists(bstack1111l1l1l1_opy_) == False:
      self.logger.warn(bstack11111_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡱࡣࡷ࡬ࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤ࠭ࠢࡵࡩࡹࡸࡹࡪࡰࡪࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠨᏍ"))
      bstack1111l1l1l1_opy_ = self.bstack1111lll1l1_opy_(bstack111l111l1l_opy_, bstack1111l1l1ll_opy_)
      self.bstack11111lllll_opy_(bstack111l111l1l_opy_, bstack1111l1l1ll_opy_, bstack1111l1l1l1_opy_, bstack1111ll11l1_opy_+1)
    bstack111l111lll_opy_ = bstack11111_opy_ (u"ࠤࡡ࠲࠯ࡆࡰࡦࡴࡦࡽࡡ࠵ࡣ࡭࡫ࠣࡠࡩ࠴࡜ࡥ࠭࠱ࡠࡩ࠱ࠢᏎ")
    command = bstack11111_opy_ (u"ࠪࡿࢂࠦ࠭࠮ࡸࡨࡶࡸ࡯࡯࡯ࠩᏏ").format(bstack1111l1l1l1_opy_)
    bstack1111lll1ll_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack111l111lll_opy_, bstack1111lll1ll_opy_) != None:
      return True
    else:
      self.logger.error(bstack11111_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡺࡪࡸࡳࡪࡱࡱࠤࡨ࡮ࡥࡤ࡭ࠣࡪࡦ࡯࡬ࡦࡦࠥᏐ"))
      bstack1111l1l1l1_opy_ = self.bstack1111lll1l1_opy_(bstack111l111l1l_opy_, bstack1111l1l1ll_opy_)
      self.bstack11111lllll_opy_(bstack111l111l1l_opy_, bstack1111l1l1ll_opy_, bstack1111l1l1l1_opy_, bstack1111ll11l1_opy_+1)
  def bstack1111ll1l11_opy_(self, bstack1111l1l111_opy_, bstack1111l1l1ll_opy_):
    try:
      working_dir = os.path.dirname(bstack1111l1l111_opy_)
      shutil.unpack_archive(bstack1111l1l111_opy_, working_dir)
      bstack1111l1l1l1_opy_ = os.path.join(working_dir, bstack1111l1l1ll_opy_)
      os.chmod(bstack1111l1l1l1_opy_, 0o755)
      return bstack1111l1l1l1_opy_
    except Exception as e:
      self.logger.error(bstack11111_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡷࡱࡾ࡮ࡶࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠨᏑ"))
  def bstack1111ll111l_opy_(self):
    try:
      percy = str(self.config.get(bstack11111_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬᏒ"), bstack11111_opy_ (u"ࠢࡧࡣ࡯ࡷࡪࠨᏓ"))).lower()
      if percy != bstack11111_opy_ (u"ࠣࡶࡵࡹࡪࠨᏔ"):
        return False
      self.bstack11llll1ll_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack11111_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪࡥࡵࡧࡦࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᏕ").format(e))
  def bstack1111l11111_opy_(self):
    try:
      bstack1111l11111_opy_ = str(self.config.get(bstack11111_opy_ (u"ࠪࡴࡪࡸࡣࡺࡅࡤࡴࡹࡻࡲࡦࡏࡲࡨࡪ࠭Ꮦ"), bstack11111_opy_ (u"ࠦࡦࡻࡴࡰࠤᏗ"))).lower()
      return bstack1111l11111_opy_
    except Exception as e:
      self.logger.error(bstack11111_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡨࡸࡪࡩࡴࠡࡲࡨࡶࡨࡿࠠࡤࡣࡳࡸࡺࡸࡥࠡ࡯ࡲࡨࡪ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨᏘ").format(e))
  def init(self, bstack111l11111_opy_, config, logger):
    self.bstack111l11111_opy_ = bstack111l11111_opy_
    self.config = config
    self.logger = logger
    if not self.bstack1111ll111l_opy_():
      return
    self.bstack1111ll11ll_opy_ = config.get(bstack11111_opy_ (u"࠭ࡰࡦࡴࡦࡽࡔࡶࡴࡪࡱࡱࡷࠬᏙ"), {})
    self.bstack11111ll1l1_opy_ = config.get(bstack11111_opy_ (u"ࠧࡱࡧࡵࡧࡾࡉࡡࡱࡶࡸࡶࡪࡓ࡯ࡥࡧࠪᏚ"), bstack11111_opy_ (u"ࠣࡣࡸࡸࡴࠨᏛ"))
    try:
      bstack111l111l1l_opy_, bstack1111l1l1ll_opy_ = self.bstack111l11l11l_opy_()
      bstack1111l1l1l1_opy_, bstack111l11ll1l_opy_ = self.bstack1111lll111_opy_(bstack111l111l1l_opy_, bstack1111l1l1ll_opy_)
      if bstack111l11ll1l_opy_:
        self.binary_path = bstack1111l1l1l1_opy_
        thread = Thread(target=self.bstack111l111l11_opy_)
        thread.start()
      else:
        self.bstack1111ll1l1l_opy_ = True
        self.logger.error(bstack11111_opy_ (u"ࠤࡌࡲࡻࡧ࡬ࡪࡦࠣࡴࡪࡸࡣࡺࠢࡳࡥࡹ࡮ࠠࡧࡱࡸࡲࡩࠦ࠭ࠡࡽࢀ࠰࡛ࠥ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡑࡧࡵࡧࡾࠨᏜ").format(bstack1111l1l1l1_opy_))
    except Exception as e:
      self.logger.error(bstack11111_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᏝ").format(e))
  def bstack1111l11l1l_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack11111_opy_ (u"ࠫࡱࡵࡧࠨᏞ"), bstack11111_opy_ (u"ࠬࡶࡥࡳࡥࡼ࠲ࡱࡵࡧࠨᏟ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack11111_opy_ (u"ࠨࡐࡶࡵ࡫࡭ࡳ࡭ࠠࡱࡧࡵࡧࡾࠦ࡬ࡰࡩࡶࠤࡦࡺࠠࡼࡿࠥᏠ").format(logfile))
      self.bstack11111ll11l_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack11111_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡪࡺࠠࡱࡧࡵࡧࡾࠦ࡬ࡰࡩࠣࡴࡦࡺࡨ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᏡ").format(e))
  def bstack111l111l11_opy_(self):
    bstack1111l111ll_opy_ = self.bstack1111l11ll1_opy_()
    if bstack1111l111ll_opy_ == None:
      self.bstack1111ll1l1l_opy_ = True
      self.logger.error(bstack11111_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡵࡱ࡮ࡩࡳࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥ࠮ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼࠦᏢ"))
      return False
    command_args = [bstack11111_opy_ (u"ࠤࡤࡴࡵࡀࡥࡹࡧࡦ࠾ࡸࡺࡡࡳࡶࠥᏣ") if self.bstack111l11111_opy_ else bstack11111_opy_ (u"ࠪࡩࡽ࡫ࡣ࠻ࡵࡷࡥࡷࡺࠧᏤ")]
    bstack11111ll1ll_opy_ = self.bstack1111lll11l_opy_()
    if bstack11111ll1ll_opy_ != None:
      command_args.append(bstack11111_opy_ (u"ࠦ࠲ࡩࠠࡼࡿࠥᏥ").format(bstack11111ll1ll_opy_))
    env = os.environ.copy()
    env[bstack11111_opy_ (u"ࠧࡖࡅࡓࡅ࡜ࡣ࡙ࡕࡋࡆࡐࠥᏦ")] = bstack1111l111ll_opy_
    bstack111l1111l1_opy_ = [self.binary_path]
    self.bstack1111l11l1l_opy_()
    self.bstack1111llll11_opy_ = self.bstack111l11111l_opy_(bstack111l1111l1_opy_ + command_args, env)
    self.logger.debug(bstack11111_opy_ (u"ࠨࡓࡵࡣࡵࡸ࡮ࡴࡧࠡࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠢᏧ"))
    bstack1111ll11l1_opy_ = 0
    while self.bstack1111llll11_opy_.poll() == None:
      bstack11111lll11_opy_ = self.bstack111l111111_opy_()
      if bstack11111lll11_opy_:
        self.logger.debug(bstack11111_opy_ (u"ࠢࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡳࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠥᏨ"))
        self.bstack1111l111l1_opy_ = True
        return True
      bstack1111ll11l1_opy_ += 1
      self.logger.debug(bstack11111_opy_ (u"ࠣࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠠࡓࡧࡷࡶࡾࠦ࠭ࠡࡽࢀࠦᏩ").format(bstack1111ll11l1_opy_))
      time.sleep(2)
    self.logger.error(bstack11111_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡊࡦ࡯࡬ࡦࡦࠣࡥ࡫ࡺࡥࡳࠢࡾࢁࠥࡧࡴࡵࡧࡰࡴࡹࡹࠢᏪ").format(bstack1111ll11l1_opy_))
    self.bstack1111ll1l1l_opy_ = True
    return False
  def bstack111l111111_opy_(self, bstack1111ll11l1_opy_ = 0):
    try:
      if bstack1111ll11l1_opy_ > 10:
        return False
      bstack11111lll1l_opy_ = os.environ.get(bstack11111_opy_ (u"ࠪࡔࡊࡘࡃ࡚ࡡࡖࡉࡗ࡜ࡅࡓࡡࡄࡈࡉࡘࡅࡔࡕࠪᏫ"), bstack11111_opy_ (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳ࡱࡵࡣࡢ࡮࡫ࡳࡸࡺ࠺࠶࠵࠶࠼ࠬᏬ"))
      bstack1111l1ll1l_opy_ = bstack11111lll1l_opy_ + bstack11l1l1lll1_opy_
      response = requests.get(bstack1111l1ll1l_opy_)
      return True if response.json() else False
    except:
      return False
  def bstack1111l11ll1_opy_(self):
    bstack1111l1ll11_opy_ = bstack11111_opy_ (u"ࠬࡧࡰࡱࠩᏭ") if self.bstack111l11111_opy_ else bstack11111_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨᏮ")
    bstack111llll111_opy_ = bstack11111_opy_ (u"ࠢࡢࡲ࡬࠳ࡦࡶࡰࡠࡲࡨࡶࡨࡿ࠯ࡨࡧࡷࡣࡵࡸ࡯࡫ࡧࡦࡸࡤࡺ࡯࡬ࡧࡱࡃࡳࡧ࡭ࡦ࠿ࡾࢁࠫࡺࡹࡱࡧࡀࡿࢂࠨᏯ").format(self.config[bstack11111_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭Ᏸ")], bstack1111l1ll11_opy_)
    uri = bstack1ll1l1lll1_opy_(bstack111llll111_opy_)
    try:
      response = bstack1lll11l11l_opy_(bstack11111_opy_ (u"ࠩࡊࡉ࡙࠭Ᏹ"), uri, {}, {bstack11111_opy_ (u"ࠪࡥࡺࡺࡨࠨᏲ"): (self.config[bstack11111_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭Ᏻ")], self.config[bstack11111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᏴ")])})
      if response.status_code == 200:
        bstack1111l1l11l_opy_ = response.json()
        if bstack11111_opy_ (u"ࠨࡴࡰ࡭ࡨࡲࠧᏵ") in bstack1111l1l11l_opy_:
          return bstack1111l1l11l_opy_[bstack11111_opy_ (u"ࠢࡵࡱ࡮ࡩࡳࠨ᏶")]
        else:
          raise bstack11111_opy_ (u"ࠨࡖࡲ࡯ࡪࡴࠠࡏࡱࡷࠤࡋࡵࡵ࡯ࡦࠣ࠱ࠥࢁࡽࠨ᏷").format(bstack1111l1l11l_opy_)
      else:
        raise bstack11111_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡬ࡥࡵࡥ࡫ࠤࡵ࡫ࡲࡤࡻࠣࡸࡴࡱࡥ࡯࠮ࠣࡖࡪࡹࡰࡰࡰࡶࡩࠥࡹࡴࡢࡶࡸࡷࠥ࠳ࠠࡼࡿ࠯ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࠦࡂࡰࡦࡼࠤ࠲ࠦࡻࡾࠤᏸ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack11111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡵ࡫ࡲࡤࡻࠣࡴࡷࡵࡪࡦࡥࡷࠦᏹ").format(e))
  def bstack1111lll11l_opy_(self):
    bstack1111llll1l_opy_ = os.path.join(tempfile.gettempdir(), bstack11111_opy_ (u"ࠦࡵ࡫ࡲࡤࡻࡆࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠢᏺ"))
    try:
      if bstack11111_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭ᏻ") not in self.bstack1111ll11ll_opy_:
        self.bstack1111ll11ll_opy_[bstack11111_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧᏼ")] = 2
      with open(bstack1111llll1l_opy_, bstack11111_opy_ (u"ࠧࡸࠩᏽ")) as fp:
        json.dump(self.bstack1111ll11ll_opy_, fp)
      return bstack1111llll1l_opy_
    except Exception as e:
      self.logger.error(bstack11111_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡨࡸࡥࡢࡶࡨࠤࡵ࡫ࡲࡤࡻࠣࡧࡴࡴࡦ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣ᏾").format(e))
  def bstack111l11111l_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack1111l11lll_opy_ == bstack11111_opy_ (u"ࠩࡺ࡭ࡳ࠭᏿"):
        bstack111l11l1ll_opy_ = [bstack11111_opy_ (u"ࠪࡧࡲࡪ࠮ࡦࡺࡨࠫ᐀"), bstack11111_opy_ (u"ࠫ࠴ࡩࠧᐁ")]
        cmd = bstack111l11l1ll_opy_ + cmd
      cmd = bstack11111_opy_ (u"ࠬࠦࠧᐂ").join(cmd)
      self.logger.debug(bstack11111_opy_ (u"ࠨࡒࡶࡰࡱ࡭ࡳ࡭ࠠࡼࡿࠥᐃ").format(cmd))
      with open(self.bstack11111ll11l_opy_, bstack11111_opy_ (u"ࠢࡢࠤᐄ")) as bstack1111lllll1_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1111lllll1_opy_, text=True, stderr=bstack1111lllll1_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1111ll1l1l_opy_ = True
      self.logger.error(bstack11111_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺࠢࡺ࡭ࡹ࡮ࠠࡤ࡯ࡧࠤ࠲ࠦࡻࡾ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠࡼࡿࠥᐅ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack1111l111l1_opy_:
        self.logger.info(bstack11111_opy_ (u"ࠤࡖࡸࡴࡶࡰࡪࡰࡪࠤࡕ࡫ࡲࡤࡻࠥᐆ"))
        cmd = [self.binary_path, bstack11111_opy_ (u"ࠥࡩࡽ࡫ࡣ࠻ࡵࡷࡳࡵࠨᐇ")]
        self.bstack111l11111l_opy_(cmd)
        self.bstack1111l111l1_opy_ = False
    except Exception as e:
      self.logger.error(bstack11111_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡲࡴࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡷࡪࡶ࡫ࠤࡨࡵ࡭࡮ࡣࡱࡨࠥ࠳ࠠࡼࡿ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠦᐈ").format(cmd, e))
  def bstack1l1l111l_opy_(self):
    if not self.bstack11llll1ll_opy_:
      return
    try:
      bstack111l11ll11_opy_ = 0
      while not self.bstack1111l111l1_opy_ and bstack111l11ll11_opy_ < self.bstack1111l1llll_opy_:
        if self.bstack1111ll1l1l_opy_:
          self.logger.info(bstack11111_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡸ࡫ࡴࡶࡲࠣࡪࡦ࡯࡬ࡦࡦࠥᐉ"))
          return
        time.sleep(1)
        bstack111l11ll11_opy_ += 1
      os.environ[bstack11111_opy_ (u"࠭ࡐࡆࡔࡆ࡝ࡤࡈࡅࡔࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࠬᐊ")] = str(self.bstack1111ll1ll1_opy_())
      self.logger.info(bstack11111_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡳࡦࡶࡸࡴࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤࠣᐋ"))
    except Exception as e:
      self.logger.error(bstack11111_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸ࡫ࡴࡶࡲࠣࡴࡪࡸࡣࡺ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᐌ").format(e))
  def bstack1111ll1ll1_opy_(self):
    if self.bstack111l11111_opy_:
      return
    try:
      bstack111l11l1l1_opy_ = [platform[bstack11111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᐍ")].lower() for platform in self.config.get(bstack11111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᐎ"), [])]
      bstack111l1111ll_opy_ = sys.maxsize
      bstack111l111ll1_opy_ = bstack11111_opy_ (u"ࠫࠬᐏ")
      for browser in bstack111l11l1l1_opy_:
        if browser in self.bstack111l11l111_opy_:
          bstack1111l1lll1_opy_ = self.bstack111l11l111_opy_[browser]
        if bstack1111l1lll1_opy_ < bstack111l1111ll_opy_:
          bstack111l1111ll_opy_ = bstack1111l1lll1_opy_
          bstack111l111ll1_opy_ = browser
      return bstack111l111ll1_opy_
    except Exception as e:
      self.logger.error(bstack11111_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡢࡦࡵࡷࠤࡵࡲࡡࡵࡨࡲࡶࡲ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨᐐ").format(e))