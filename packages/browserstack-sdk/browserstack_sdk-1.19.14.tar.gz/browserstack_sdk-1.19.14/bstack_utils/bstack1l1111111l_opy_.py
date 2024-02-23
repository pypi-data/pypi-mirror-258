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
from uuid import uuid4
from bstack_utils.helper import bstack11l1111l1_opy_, bstack11l11l1lll_opy_
from bstack_utils.bstack1lll111l_opy_ import bstack1lllllll1l1_opy_
class bstack1l11l11lll_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, bstack1l111lll1l_opy_=None, framework=None, tags=[], scope=[], bstack1llll1l1l11_opy_=None, bstack1llll1l11ll_opy_=True, bstack1llll1l1ll1_opy_=None, bstack1ll11lll_opy_=None, result=None, duration=None, bstack1l11l111ll_opy_=None, meta={}):
        self.bstack1l11l111ll_opy_ = bstack1l11l111ll_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1llll1l11ll_opy_:
            self.uuid = uuid4().__str__()
        self.bstack1l111lll1l_opy_ = bstack1l111lll1l_opy_
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1llll1l1l11_opy_ = bstack1llll1l1l11_opy_
        self.bstack1llll1l1ll1_opy_ = bstack1llll1l1ll1_opy_
        self.bstack1ll11lll_opy_ = bstack1ll11lll_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
    def bstack1l111ll11l_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack1llll11llll_opy_(self):
        bstack1llll1ll11l_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack11111_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬᒠ"): bstack1llll1ll11l_opy_,
            bstack11111_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࠬᒡ"): bstack1llll1ll11l_opy_,
            bstack11111_opy_ (u"ࠫࡻࡩ࡟ࡧ࡫࡯ࡩࡵࡧࡴࡩࠩᒢ"): bstack1llll1ll11l_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack11111_opy_ (u"࡛ࠧ࡮ࡦࡺࡳࡩࡨࡺࡥࡥࠢࡤࡶ࡬ࡻ࡭ࡦࡰࡷ࠾ࠥࠨᒣ") + key)
            setattr(self, key, val)
    def bstack1llll1l1111_opy_(self):
        return {
            bstack11111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᒤ"): self.name,
            bstack11111_opy_ (u"ࠧࡣࡱࡧࡽࠬᒥ"): {
                bstack11111_opy_ (u"ࠨ࡮ࡤࡲ࡬࠭ᒦ"): bstack11111_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩᒧ"),
                bstack11111_opy_ (u"ࠪࡧࡴࡪࡥࠨᒨ"): self.code
            },
            bstack11111_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫᒩ"): self.scope,
            bstack11111_opy_ (u"ࠬࡺࡡࡨࡵࠪᒪ"): self.tags,
            bstack11111_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩᒫ"): self.framework,
            bstack11111_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᒬ"): self.bstack1l111lll1l_opy_
        }
    def bstack1llll1lll1l_opy_(self):
        return {
         bstack11111_opy_ (u"ࠨ࡯ࡨࡸࡦ࠭ᒭ"): self.meta
        }
    def bstack1llll1ll111_opy_(self):
        return {
            bstack11111_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡔࡨࡶࡺࡴࡐࡢࡴࡤࡱࠬᒮ"): {
                bstack11111_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡡࡱࡥࡲ࡫ࠧᒯ"): self.bstack1llll1l1l11_opy_
            }
        }
    def bstack1llll1l1lll_opy_(self, bstack1llll1ll1ll_opy_, details):
        step = next(filter(lambda st: st[bstack11111_opy_ (u"ࠫ࡮ࡪࠧᒰ")] == bstack1llll1ll1ll_opy_, self.meta[bstack11111_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᒱ")]), None)
        step.update(details)
    def bstack1lllll11111_opy_(self, bstack1llll1ll1ll_opy_):
        step = next(filter(lambda st: st[bstack11111_opy_ (u"࠭ࡩࡥࠩᒲ")] == bstack1llll1ll1ll_opy_, self.meta[bstack11111_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᒳ")]), None)
        step.update({
            bstack11111_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᒴ"): bstack11l1111l1_opy_()
        })
    def bstack1l11l11l1l_opy_(self, bstack1llll1ll1ll_opy_, result, duration=None):
        bstack1llll1l1ll1_opy_ = bstack11l1111l1_opy_()
        if bstack1llll1ll1ll_opy_ is not None and self.meta.get(bstack11111_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᒵ")):
            step = next(filter(lambda st: st[bstack11111_opy_ (u"ࠪ࡭ࡩ࠭ᒶ")] == bstack1llll1ll1ll_opy_, self.meta[bstack11111_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᒷ")]), None)
            step.update({
                bstack11111_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᒸ"): bstack1llll1l1ll1_opy_,
                bstack11111_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨᒹ"): duration if duration else bstack11l11l1lll_opy_(step[bstack11111_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᒺ")], bstack1llll1l1ll1_opy_),
                bstack11111_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᒻ"): result.result,
                bstack11111_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᒼ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1llll1l111l_opy_):
        if self.meta.get(bstack11111_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᒽ")):
            self.meta[bstack11111_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᒾ")].append(bstack1llll1l111l_opy_)
        else:
            self.meta[bstack11111_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᒿ")] = [ bstack1llll1l111l_opy_ ]
    def bstack1llll1llll1_opy_(self):
        return {
            bstack11111_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᓀ"): self.bstack1l111ll11l_opy_(),
            **self.bstack1llll1l1111_opy_(),
            **self.bstack1llll11llll_opy_(),
            **self.bstack1llll1lll1l_opy_()
        }
    def bstack1llll11lll1_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack11111_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᓁ"): self.bstack1llll1l1ll1_opy_,
            bstack11111_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩᓂ"): self.duration,
            bstack11111_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᓃ"): self.result.result
        }
        if data[bstack11111_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᓄ")] == bstack11111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᓅ"):
            data[bstack11111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫᓆ")] = self.result.bstack11ll1lll11_opy_()
            data[bstack11111_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᓇ")] = [{bstack11111_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᓈ"): self.result.bstack111llll11l_opy_()}]
        return data
    def bstack1llll1lll11_opy_(self):
        return {
            bstack11111_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᓉ"): self.bstack1l111ll11l_opy_(),
            **self.bstack1llll1l1111_opy_(),
            **self.bstack1llll11llll_opy_(),
            **self.bstack1llll11lll1_opy_(),
            **self.bstack1llll1lll1l_opy_()
        }
    def bstack1l11l111l1_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack11111_opy_ (u"ࠩࡖࡸࡦࡸࡴࡦࡦࠪᓊ") in event:
            return self.bstack1llll1llll1_opy_()
        elif bstack11111_opy_ (u"ࠪࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᓋ") in event:
            return self.bstack1llll1lll11_opy_()
    def bstack1l111l111l_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1llll1l1ll1_opy_ = time if time else bstack11l1111l1_opy_()
        self.duration = duration if duration else bstack11l11l1lll_opy_(self.bstack1l111lll1l_opy_, self.bstack1llll1l1ll1_opy_)
        if result:
            self.result = result
class bstack1l1111lll1_opy_(bstack1l11l11lll_opy_):
    def __init__(self, hooks=[], bstack11lll1llll_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack11lll1llll_opy_ = bstack11lll1llll_opy_
        super().__init__(*args, **kwargs, bstack1ll11lll_opy_=bstack11111_opy_ (u"ࠫࡹ࡫ࡳࡵࠩᓌ"))
    @classmethod
    def bstack1llll1l1l1l_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11111_opy_ (u"ࠬ࡯ࡤࠨᓍ"): id(step),
                bstack11111_opy_ (u"࠭ࡴࡦࡺࡷࠫᓎ"): step.name,
                bstack11111_opy_ (u"ࠧ࡬ࡧࡼࡻࡴࡸࡤࠨᓏ"): step.keyword,
            })
        return bstack1l1111lll1_opy_(
            **kwargs,
            meta={
                bstack11111_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࠩᓐ"): {
                    bstack11111_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᓑ"): feature.name,
                    bstack11111_opy_ (u"ࠪࡴࡦࡺࡨࠨᓒ"): feature.filename,
                    bstack11111_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩᓓ"): feature.description
                },
                bstack11111_opy_ (u"ࠬࡹࡣࡦࡰࡤࡶ࡮ࡵࠧᓔ"): {
                    bstack11111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᓕ"): scenario.name
                },
                bstack11111_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᓖ"): steps,
                bstack11111_opy_ (u"ࠨࡧࡻࡥࡲࡶ࡬ࡦࡵࠪᓗ"): bstack1lllllll1l1_opy_(test)
            }
        )
    def bstack1llll1lllll_opy_(self):
        return {
            bstack11111_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᓘ"): self.hooks
        }
    def bstack1llll1l11l1_opy_(self):
        if self.bstack11lll1llll_opy_:
            return {
                bstack11111_opy_ (u"ࠪ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠩᓙ"): self.bstack11lll1llll_opy_
            }
        return {}
    def bstack1llll1lll11_opy_(self):
        return {
            **super().bstack1llll1lll11_opy_(),
            **self.bstack1llll1lllll_opy_()
        }
    def bstack1llll1llll1_opy_(self):
        return {
            **super().bstack1llll1llll1_opy_(),
            **self.bstack1llll1l11l1_opy_()
        }
    def bstack1l111l111l_opy_(self):
        return bstack11111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭ᓚ")
class bstack11lllll1l1_opy_(bstack1l11l11lll_opy_):
    def __init__(self, hook_type, *args, **kwargs):
        self.hook_type = hook_type
        super().__init__(*args, **kwargs, bstack1ll11lll_opy_=bstack11111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᓛ"))
    def bstack1l111l1111_opy_(self):
        return self.hook_type
    def bstack1llll1ll1l1_opy_(self):
        return {
            bstack11111_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᓜ"): self.hook_type
        }
    def bstack1llll1lll11_opy_(self):
        return {
            **super().bstack1llll1lll11_opy_(),
            **self.bstack1llll1ll1l1_opy_()
        }
    def bstack1llll1llll1_opy_(self):
        return {
            **super().bstack1llll1llll1_opy_(),
            **self.bstack1llll1ll1l1_opy_()
        }
    def bstack1l111l111l_opy_(self):
        return bstack11111_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࠩᓝ")