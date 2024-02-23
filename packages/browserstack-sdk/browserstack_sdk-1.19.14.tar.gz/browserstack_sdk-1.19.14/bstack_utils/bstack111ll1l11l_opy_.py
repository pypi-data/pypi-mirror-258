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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result
def _111lll1111_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack111ll1l111_opy_:
    def __init__(self, handler):
        self._111ll11l1l_opy_ = {}
        self._111ll11ll1_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        self._111ll11l1l_opy_[bstack11111_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨጔ")] = Module._inject_setup_function_fixture
        self._111ll11l1l_opy_[bstack11111_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧጕ")] = Module._inject_setup_module_fixture
        self._111ll11l1l_opy_[bstack11111_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ጖")] = Class._inject_setup_class_fixture
        self._111ll11l1l_opy_[bstack11111_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ጗")] = Class._inject_setup_method_fixture
        Module._inject_setup_function_fixture = self.bstack111ll1l1ll_opy_(bstack11111_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬጘ"))
        Module._inject_setup_module_fixture = self.bstack111ll1l1ll_opy_(bstack11111_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫጙ"))
        Class._inject_setup_class_fixture = self.bstack111ll1l1ll_opy_(bstack11111_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫጚ"))
        Class._inject_setup_method_fixture = self.bstack111ll1l1ll_opy_(bstack11111_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ጛ"))
    def bstack111ll11lll_opy_(self, bstack111ll11l11_opy_, hook_type):
        meth = getattr(bstack111ll11l11_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._111ll11ll1_opy_[hook_type] = meth
            setattr(bstack111ll11l11_opy_, hook_type, self.bstack111ll1llll_opy_(hook_type))
    def bstack111ll1l1l1_opy_(self, instance, bstack111ll111ll_opy_):
        if bstack111ll111ll_opy_ == bstack11111_opy_ (u"ࠨࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠤጜ"):
            self.bstack111ll11lll_opy_(instance.obj, bstack11111_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠣጝ"))
            self.bstack111ll11lll_opy_(instance.obj, bstack11111_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠧጞ"))
        if bstack111ll111ll_opy_ == bstack11111_opy_ (u"ࠤࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠥጟ"):
            self.bstack111ll11lll_opy_(instance.obj, bstack11111_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠤጠ"))
            self.bstack111ll11lll_opy_(instance.obj, bstack11111_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪࠨጡ"))
        if bstack111ll111ll_opy_ == bstack11111_opy_ (u"ࠧࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠧጢ"):
            self.bstack111ll11lll_opy_(instance.obj, bstack11111_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠦጣ"))
            self.bstack111ll11lll_opy_(instance.obj, bstack11111_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠣጤ"))
        if bstack111ll111ll_opy_ == bstack11111_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠤጥ"):
            self.bstack111ll11lll_opy_(instance.obj, bstack11111_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠣጦ"))
            self.bstack111ll11lll_opy_(instance.obj, bstack11111_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠧጧ"))
    @staticmethod
    def bstack111ll1ll11_opy_(hook_type, func, args):
        if hook_type in [bstack11111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪጨ"), bstack11111_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧጩ")]:
            _111lll1111_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack111ll1llll_opy_(self, hook_type):
        def bstack111ll1lll1_opy_(arg=None):
            self.handler(hook_type, bstack11111_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭ጪ"))
            result = None
            exception = None
            try:
                self.bstack111ll1ll11_opy_(hook_type, self._111ll11ll1_opy_[hook_type], (arg,))
                result = Result(result=bstack11111_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧጫ"))
            except Exception as e:
                result = Result(result=bstack11111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨጬ"), exception=e)
                self.handler(hook_type, bstack11111_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨጭ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11111_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩጮ"), result)
        def bstack111ll1ll1l_opy_(this, arg=None):
            self.handler(hook_type, bstack11111_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫጯ"))
            result = None
            exception = None
            try:
                self.bstack111ll1ll11_opy_(hook_type, self._111ll11ll1_opy_[hook_type], (this, arg))
                result = Result(result=bstack11111_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬጰ"))
            except Exception as e:
                result = Result(result=bstack11111_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ጱ"), exception=e)
                self.handler(hook_type, bstack11111_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ጲ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11111_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧጳ"), result)
        if hook_type in [bstack11111_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨጴ"), bstack11111_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬጵ")]:
            return bstack111ll1ll1l_opy_
        return bstack111ll1lll1_opy_
    def bstack111ll1l1ll_opy_(self, bstack111ll111ll_opy_):
        def bstack111ll111l1_opy_(this, *args, **kwargs):
            self.bstack111ll1l1l1_opy_(this, bstack111ll111ll_opy_)
            self._111ll11l1l_opy_[bstack111ll111ll_opy_](this, *args, **kwargs)
        return bstack111ll111l1_opy_