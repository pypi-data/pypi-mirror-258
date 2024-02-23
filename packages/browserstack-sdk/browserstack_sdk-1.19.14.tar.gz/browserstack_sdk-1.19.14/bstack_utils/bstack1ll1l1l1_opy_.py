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
import sys
import logging
import tarfile
import io
import os
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack11l1l11lll_opy_
import tempfile
import json
bstack111ll1111l_opy_ = os.path.join(tempfile.gettempdir(), bstack11111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡨࡪࡨࡵࡨ࠰࡯ࡳ࡬࠭ጶ"))
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack11111_opy_ (u"ࠬࡢ࡮ࠦࠪࡤࡷࡨࡺࡩ࡮ࡧࠬࡷࠥࡡࠥࠩࡰࡤࡱࡪ࠯ࡳ࡞࡝ࠨࠬࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠩࡴ࡟ࠣ࠱ࠥࠫࠨ࡮ࡧࡶࡷࡦ࡭ࡥࠪࡵࠪጷ"),
      datefmt=bstack11111_opy_ (u"࠭ࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨጸ"),
      stream=sys.stdout
    )
  return logger
def bstack111l1ll11l_opy_():
  global bstack111ll1111l_opy_
  if os.path.exists(bstack111ll1111l_opy_):
    os.remove(bstack111ll1111l_opy_)
def bstack1l1l1ll11_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack1l111llll_opy_(config, log_level):
  bstack111l1lllll_opy_ = log_level
  if bstack11111_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩጹ") in config:
    bstack111l1lllll_opy_ = bstack11l1l11lll_opy_[config[bstack11111_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪጺ")]]
  if config.get(bstack11111_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫጻ"), False):
    logging.getLogger().setLevel(bstack111l1lllll_opy_)
    return bstack111l1lllll_opy_
  global bstack111ll1111l_opy_
  bstack1l1l1ll11_opy_()
  bstack111l1ll1l1_opy_ = logging.Formatter(
    fmt=bstack11111_opy_ (u"ࠪࡠࡳࠫࠨࡢࡵࡦࡸ࡮ࡳࡥࠪࡵࠣ࡟ࠪ࠮࡮ࡢ࡯ࡨ࠭ࡸࡣ࡛ࠦࠪ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩ࠮ࡹ࡝ࠡ࠯ࠣࠩ࠭ࡳࡥࡴࡵࡤ࡫ࡪ࠯ࡳࠨጼ"),
    datefmt=bstack11111_opy_ (u"ࠫࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭ጽ")
  )
  bstack111l1llll1_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack111ll1111l_opy_)
  file_handler.setFormatter(bstack111l1ll1l1_opy_)
  bstack111l1llll1_opy_.setFormatter(bstack111l1ll1l1_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack111l1llll1_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack11111_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴ࠱ࡶࡪࡳ࡯ࡵࡧ࠱ࡶࡪࡳ࡯ࡵࡧࡢࡧࡴࡴ࡮ࡦࡥࡷ࡭ࡴࡴࠧጾ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack111l1llll1_opy_.setLevel(bstack111l1lllll_opy_)
  logging.getLogger().addHandler(bstack111l1llll1_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack111l1lllll_opy_
def bstack111l1ll1ll_opy_(config):
  try:
    bstack111l1lll11_opy_ = set([
      bstack11111_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨጿ"), bstack11111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪፀ"), bstack11111_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫፁ"), bstack11111_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ፂ"), bstack11111_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠬፃ"),
      bstack11111_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡘࡷࡪࡸࠧፄ"), bstack11111_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡦࡹࡳࠨፅ"), bstack11111_opy_ (u"࠭࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡘࡷࡪࡸࠧፆ"), bstack11111_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼࡔࡦࡹࡳࠨፇ")
    ])
    bstack111l1l1l11_opy_ = bstack11111_opy_ (u"ࠨࠩፈ")
    with open(bstack11111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬፉ")) as bstack111l1lll1l_opy_:
      bstack111l1l1l1l_opy_ = bstack111l1lll1l_opy_.read()
      bstack111l1l1l11_opy_ = re.sub(bstack11111_opy_ (u"ࡵࠫࡣ࠮࡜ࡴ࠭ࠬࡃࠨ࠴ࠪࠥ࡞ࡱࠫፊ"), bstack11111_opy_ (u"ࠫࠬፋ"), bstack111l1l1l1l_opy_, flags=re.M)
      bstack111l1l1l11_opy_ = re.sub(
        bstack11111_opy_ (u"ࡷ࠭࡞ࠩ࡞ࡶ࠯࠮ࡅࠨࠨፌ") + bstack11111_opy_ (u"࠭ࡼࠨፍ").join(bstack111l1lll11_opy_) + bstack11111_opy_ (u"ࠧࠪ࠰࠭ࠨࠬፎ"),
        bstack11111_opy_ (u"ࡳࠩ࡟࠶࠿࡛ࠦࡓࡇࡇࡅࡈ࡚ࡅࡅ࡟ࠪፏ"),
        bstack111l1l1l11_opy_, flags=re.M | re.I
      )
    def bstack111l1l1lll_opy_(dic):
      bstack111l1ll111_opy_ = {}
      for key, value in dic.items():
        if key in bstack111l1lll11_opy_:
          bstack111l1ll111_opy_[key] = bstack11111_opy_ (u"ࠩ࡞ࡖࡊࡊࡁࡄࡖࡈࡈࡢ࠭ፐ")
        else:
          if isinstance(value, dict):
            bstack111l1ll111_opy_[key] = bstack111l1l1lll_opy_(value)
          else:
            bstack111l1ll111_opy_[key] = value
      return bstack111l1ll111_opy_
    bstack111l1ll111_opy_ = bstack111l1l1lll_opy_(config)
    return {
      bstack11111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭ፑ"): bstack111l1l1l11_opy_,
      bstack11111_opy_ (u"ࠫ࡫࡯࡮ࡢ࡮ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧፒ"): json.dumps(bstack111l1ll111_opy_)
    }
  except Exception as e:
    return {}
def bstack1ll1l11l1l_opy_(config):
  global bstack111ll1111l_opy_
  try:
    if config.get(bstack11111_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹࠧፓ"), False):
      return
    uuid = os.getenv(bstack11111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫፔ"))
    if not uuid or uuid == bstack11111_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬፕ"):
      return
    bstack111ll11111_opy_ = [bstack11111_opy_ (u"ࠨࡴࡨࡵࡺ࡯ࡲࡦ࡯ࡨࡲࡹࡹ࠮ࡵࡺࡷࠫፖ"), bstack11111_opy_ (u"ࠩࡓ࡭ࡵ࡬ࡩ࡭ࡧࠪፗ"), bstack11111_opy_ (u"ࠪࡴࡾࡶࡲࡰ࡬ࡨࡧࡹ࠴ࡴࡰ࡯࡯ࠫፘ"), bstack111ll1111l_opy_]
    bstack1l1l1ll11_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack11111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠱ࡱࡵࡧࡴ࠯ࠪፙ") + uuid + bstack11111_opy_ (u"ࠬ࠴ࡴࡢࡴ࠱࡫ࡿ࠭ፚ"))
    with tarfile.open(output_file, bstack11111_opy_ (u"ࠨࡷ࠻ࡩࡽࠦ፛")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack111ll11111_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack111l1ll1ll_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack111l1l1ll1_opy_ = data.encode()
        tarinfo.size = len(bstack111l1l1ll1_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack111l1l1ll1_opy_))
    bstack1ll1111l11_opy_ = MultipartEncoder(
      fields= {
        bstack11111_opy_ (u"ࠧࡥࡣࡷࡥࠬ፜"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack11111_opy_ (u"ࠨࡴࡥࠫ፝")), bstack11111_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯ࡹ࠯ࡪࡾ࡮ࡶࠧ፞")),
        bstack11111_opy_ (u"ࠪࡧࡱ࡯ࡥ࡯ࡶࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬ፟"): uuid
      }
    )
    response = requests.post(
      bstack11111_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡻࡰ࡭ࡱࡤࡨ࠲ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡥ࡯࡭ࡪࡴࡴ࠮࡮ࡲ࡫ࡸ࠵ࡵࡱ࡮ࡲࡥࡩࠨ፠"),
      data=bstack1ll1111l11_opy_,
      headers={bstack11111_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫ፡"): bstack1ll1111l11_opy_.content_type},
      auth=(config[bstack11111_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ።")], config[bstack11111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ፣")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack11111_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡶࡲ࡯ࡳࡦࡪࠠ࡭ࡱࡪࡷ࠿ࠦࠧ፤") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack11111_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡲࡩ࡯࡮ࡨࠢ࡯ࡳ࡬ࡹ࠺ࠨ፥") + str(e))
  finally:
    try:
      bstack111l1ll11l_opy_()
    except:
      pass