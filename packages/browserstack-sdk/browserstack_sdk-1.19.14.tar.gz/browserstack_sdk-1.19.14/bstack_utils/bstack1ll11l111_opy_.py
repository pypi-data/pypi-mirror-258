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
class bstack11l1ll1lll_opy_(object):
  bstack111ll1ll1_opy_ = os.path.join(os.path.expanduser(bstack11111_opy_ (u"ࠫࢃ່࠭")), bstack11111_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯້ࠬ"))
  bstack11l1llll11_opy_ = os.path.join(bstack111ll1ll1_opy_, bstack11111_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳ࠯࡬ࡶࡳࡳ໊࠭"))
  bstack11l1lll1ll_opy_ = None
  perform_scan = None
  bstack1l11lll1l1_opy_ = None
  bstack111l1ll1_opy_ = None
  bstack11ll111lll_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack11111_opy_ (u"ࠧࡪࡰࡶࡸࡦࡴࡣࡦ໋ࠩ")):
      cls.instance = super(bstack11l1ll1lll_opy_, cls).__new__(cls)
      cls.instance.bstack11l1lll111_opy_()
    return cls.instance
  def bstack11l1lll111_opy_(self):
    try:
      with open(self.bstack11l1llll11_opy_, bstack11111_opy_ (u"ࠨࡴࠪ໌")) as bstack1l1l11l11_opy_:
        bstack11l1lll1l1_opy_ = bstack1l1l11l11_opy_.read()
        data = json.loads(bstack11l1lll1l1_opy_)
        if bstack11111_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫໍ") in data:
          self.bstack11ll11ll1l_opy_(data[bstack11111_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷࠬ໎")])
        if bstack11111_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬ໏") in data:
          self.bstack11ll1l111l_opy_(data[bstack11111_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭໐")])
    except:
      pass
  def bstack11ll1l111l_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts[bstack11111_opy_ (u"࠭ࡳࡤࡣࡱࠫ໑")]
      self.bstack1l11lll1l1_opy_ = scripts[bstack11111_opy_ (u"ࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࠫ໒")]
      self.bstack111l1ll1_opy_ = scripts[bstack11111_opy_ (u"ࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࡘࡻ࡭࡮ࡣࡵࡽࠬ໓")]
      self.bstack11ll111lll_opy_ = scripts[bstack11111_opy_ (u"ࠩࡶࡥࡻ࡫ࡒࡦࡵࡸࡰࡹࡹࠧ໔")]
  def bstack11ll11ll1l_opy_(self, bstack11l1lll1ll_opy_):
    if bstack11l1lll1ll_opy_ != None and len(bstack11l1lll1ll_opy_) != 0:
      self.bstack11l1lll1ll_opy_ = bstack11l1lll1ll_opy_
  def store(self):
    try:
      with open(self.bstack11l1llll11_opy_, bstack11111_opy_ (u"ࠪࡻࠬ໕")) as file:
        json.dump({
          bstack11111_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡸࠨ໖"): self.bstack11l1lll1ll_opy_,
          bstack11111_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࡸࠨ໗"): {
            bstack11111_opy_ (u"ࠨࡳࡤࡣࡱࠦ໘"): self.perform_scan,
            bstack11111_opy_ (u"ࠢࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࠦ໙"): self.bstack1l11lll1l1_opy_,
            bstack11111_opy_ (u"ࠣࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࡘࡻ࡭࡮ࡣࡵࡽࠧ໚"): self.bstack111l1ll1_opy_,
            bstack11111_opy_ (u"ࠤࡶࡥࡻ࡫ࡒࡦࡵࡸࡰࡹࡹࠢ໛"): self.bstack11ll111lll_opy_
          }
        }, file)
    except:
      pass
  def bstack1l1l1l111_opy_(self, bstack11l1lll11l_opy_):
    try:
      return any(command.get(bstack11111_opy_ (u"ࠪࡲࡦࡳࡥࠨໜ")) == bstack11l1lll11l_opy_ for command in self.bstack11l1lll1ll_opy_)
    except:
      return False
bstack1ll11l111_opy_ = bstack11l1ll1lll_opy_()