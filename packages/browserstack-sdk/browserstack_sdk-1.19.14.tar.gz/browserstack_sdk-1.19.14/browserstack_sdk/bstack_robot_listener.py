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
import datetime
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack1l111lllll_opy_ import RobotHandler
from bstack_utils.capture import bstack11lll1ll11_opy_
from bstack_utils.bstack1l1111111l_opy_ import bstack1l11l11lll_opy_, bstack11lllll1l1_opy_, bstack1l1111lll1_opy_
from bstack_utils.bstack1ll1llllll_opy_ import bstack11ll1l1l1_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1ll1l11ll_opy_, bstack11l1111l1_opy_, Result, \
    bstack1l111ll1ll_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack11111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦ഻ࠪ"): [],
        bstack11111_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ഼࠭"): [],
        bstack11111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬഽ"): []
    }
    bstack1l111lll11_opy_ = []
    bstack1l11l1l1l1_opy_ = []
    @staticmethod
    def bstack1l111ll111_opy_(log):
        if not (log[bstack11111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪാ")] and log[bstack11111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫി")].strip()):
            return
        active = bstack11ll1l1l1_opy_.bstack1l111ll1l1_opy_()
        log = {
            bstack11111_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪീ"): log[bstack11111_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫു")],
            bstack11111_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩൂ"): datetime.datetime.utcnow().isoformat() + bstack11111_opy_ (u"࡛ࠧࠩൃ"),
            bstack11111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩൄ"): log[bstack11111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ൅")],
        }
        if active:
            if active[bstack11111_opy_ (u"ࠪࡸࡾࡶࡥࠨെ")] == bstack11111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩേ"):
                log[bstack11111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬൈ")] = active[bstack11111_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭൉")]
            elif active[bstack11111_opy_ (u"ࠧࡵࡻࡳࡩࠬൊ")] == bstack11111_opy_ (u"ࠨࡶࡨࡷࡹ࠭ോ"):
                log[bstack11111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩൌ")] = active[bstack11111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦ്ࠪ")]
        bstack11ll1l1l1_opy_.bstack1ll1l11l1l_opy_([log])
    def __init__(self):
        self.messages = Messages()
        self._1l1111l111_opy_ = None
        self._1l1111ll11_opy_ = None
        self._11llll1111_opy_ = OrderedDict()
        self.bstack11llllll1l_opy_ = bstack11lll1ll11_opy_(self.bstack1l111ll111_opy_)
    @bstack1l111ll1ll_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack11llll1l1l_opy_()
        if not self._11llll1111_opy_.get(attrs.get(bstack11111_opy_ (u"ࠫ࡮ࡪࠧൎ")), None):
            self._11llll1111_opy_[attrs.get(bstack11111_opy_ (u"ࠬ࡯ࡤࠨ൏"))] = {}
        bstack1l11l11l11_opy_ = bstack1l1111lll1_opy_(
                bstack1l11l111ll_opy_=attrs.get(bstack11111_opy_ (u"࠭ࡩࡥࠩ൐")),
                name=name,
                bstack1l111lll1l_opy_=bstack11l1111l1_opy_(),
                file_path=os.path.relpath(attrs[bstack11111_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ൑")], start=os.getcwd()) if attrs.get(bstack11111_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ൒")) != bstack11111_opy_ (u"ࠩࠪ൓") else bstack11111_opy_ (u"ࠪࠫൔ"),
                framework=bstack11111_opy_ (u"ࠫࡗࡵࡢࡰࡶࠪൕ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack11111_opy_ (u"ࠬ࡯ࡤࠨൖ"), None)
        self._11llll1111_opy_[attrs.get(bstack11111_opy_ (u"࠭ࡩࡥࠩൗ"))][bstack11111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ൘")] = bstack1l11l11l11_opy_
    @bstack1l111ll1ll_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack11lll1lll1_opy_()
        self._1l11111111_opy_(messages)
        for bstack11lll1ll1l_opy_ in self.bstack1l111lll11_opy_:
            bstack11lll1ll1l_opy_[bstack11111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪ൙")][bstack11111_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ൚")].extend(self.store[bstack11111_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩ൛")])
            bstack11ll1l1l1_opy_.bstack1l11l11111_opy_(bstack11lll1ll1l_opy_)
        self.bstack1l111lll11_opy_ = []
        self.store[bstack11111_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪ൜")] = []
    @bstack1l111ll1ll_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack11llllll1l_opy_.start()
        if not self._11llll1111_opy_.get(attrs.get(bstack11111_opy_ (u"ࠬ࡯ࡤࠨ൝")), None):
            self._11llll1111_opy_[attrs.get(bstack11111_opy_ (u"࠭ࡩࡥࠩ൞"))] = {}
        driver = bstack1ll1l11ll_opy_(threading.current_thread(), bstack11111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ൟ"), None)
        bstack1l1111111l_opy_ = bstack1l1111lll1_opy_(
            bstack1l11l111ll_opy_=attrs.get(bstack11111_opy_ (u"ࠨ࡫ࡧࠫൠ")),
            name=name,
            bstack1l111lll1l_opy_=bstack11l1111l1_opy_(),
            file_path=os.path.relpath(attrs[bstack11111_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩൡ")], start=os.getcwd()),
            scope=RobotHandler.bstack1l11111ll1_opy_(attrs.get(bstack11111_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪൢ"), None)),
            framework=bstack11111_opy_ (u"ࠫࡗࡵࡢࡰࡶࠪൣ"),
            tags=attrs[bstack11111_opy_ (u"ࠬࡺࡡࡨࡵࠪ൤")],
            hooks=self.store[bstack11111_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬ൥")],
            bstack11lll1llll_opy_=bstack11ll1l1l1_opy_.bstack1l1111llll_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack11111_opy_ (u"ࠢࡼࡿࠣࡠࡳࠦࡻࡾࠤ൦").format(bstack11111_opy_ (u"ࠣࠢࠥ൧").join(attrs[bstack11111_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ൨")]), name) if attrs[bstack11111_opy_ (u"ࠪࡸࡦ࡭ࡳࠨ൩")] else name
        )
        self._11llll1111_opy_[attrs.get(bstack11111_opy_ (u"ࠫ࡮ࡪࠧ൪"))][bstack11111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ൫")] = bstack1l1111111l_opy_
        threading.current_thread().current_test_uuid = bstack1l1111111l_opy_.bstack1l111ll11l_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack11111_opy_ (u"࠭ࡩࡥࠩ൬"), None)
        self.bstack11llllllll_opy_(bstack11111_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ൭"), bstack1l1111111l_opy_)
    @bstack1l111ll1ll_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack11llllll1l_opy_.reset()
        bstack11llll111l_opy_ = bstack1l11111l11_opy_.get(attrs.get(bstack11111_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ൮")), bstack11111_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ൯"))
        self._11llll1111_opy_[attrs.get(bstack11111_opy_ (u"ࠪ࡭ࡩ࠭൰"))][bstack11111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ൱")].stop(time=bstack11l1111l1_opy_(), duration=int(attrs.get(bstack11111_opy_ (u"ࠬ࡫࡬ࡢࡲࡶࡩࡩࡺࡩ࡮ࡧࠪ൲"), bstack11111_opy_ (u"࠭࠰ࠨ൳"))), result=Result(result=bstack11llll111l_opy_, exception=attrs.get(bstack11111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ൴")), bstack11lllll1ll_opy_=[attrs.get(bstack11111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ൵"))]))
        self.bstack11llllllll_opy_(bstack11111_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ൶"), self._11llll1111_opy_[attrs.get(bstack11111_opy_ (u"ࠪ࡭ࡩ࠭൷"))][bstack11111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ൸")], True)
        self.store[bstack11111_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩ൹")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack1l111ll1ll_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack11llll1l1l_opy_()
        current_test_id = bstack1ll1l11ll_opy_(threading.current_thread(), bstack11111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨൺ"), None)
        bstack1l111111l1_opy_ = current_test_id if bstack1ll1l11ll_opy_(threading.current_thread(), bstack11111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡥࠩൻ"), None) else bstack1ll1l11ll_opy_(threading.current_thread(), bstack11111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡹ࡮ࡺࡥࡠ࡫ࡧࠫർ"), None)
        if attrs.get(bstack11111_opy_ (u"ࠩࡷࡽࡵ࡫ࠧൽ"), bstack11111_opy_ (u"ࠪࠫൾ")).lower() in [bstack11111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪൿ"), bstack11111_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧ඀")]:
            hook_type = bstack11llll1ll1_opy_(attrs.get(bstack11111_opy_ (u"࠭ࡴࡺࡲࡨࠫඁ")), bstack1ll1l11ll_opy_(threading.current_thread(), bstack11111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫං"), None))
            hook_name = bstack11111_opy_ (u"ࠨࡽࢀࠫඃ").format(attrs.get(bstack11111_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩ඄"), bstack11111_opy_ (u"ࠪࠫඅ")))
            if hook_type in [bstack11111_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨආ"), bstack11111_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡆࡒࡌࠨඇ")]:
                hook_name = bstack11111_opy_ (u"࡛࠭ࡼࡿࡠࠤࢀࢃࠧඈ").format(bstack1l111l1lll_opy_.get(hook_type), attrs.get(bstack11111_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧඉ"), bstack11111_opy_ (u"ࠨࠩඊ")))
            bstack1l111l11l1_opy_ = bstack11lllll1l1_opy_(
                bstack1l11l111ll_opy_=bstack1l111111l1_opy_ + bstack11111_opy_ (u"ࠩ࠰ࠫඋ") + attrs.get(bstack11111_opy_ (u"ࠪࡸࡾࡶࡥࠨඌ"), bstack11111_opy_ (u"ࠫࠬඍ")).lower(),
                name=hook_name,
                bstack1l111lll1l_opy_=bstack11l1111l1_opy_(),
                file_path=os.path.relpath(attrs.get(bstack11111_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬඎ")), start=os.getcwd()),
                framework=bstack11111_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬඏ"),
                tags=attrs[bstack11111_opy_ (u"ࠧࡵࡣࡪࡷࠬඐ")],
                scope=RobotHandler.bstack1l11111ll1_opy_(attrs.get(bstack11111_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨඑ"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack1l111l11l1_opy_.bstack1l111ll11l_opy_()
            threading.current_thread().current_hook_id = bstack1l111111l1_opy_ + bstack11111_opy_ (u"ࠩ࠰ࠫඒ") + attrs.get(bstack11111_opy_ (u"ࠪࡸࡾࡶࡥࠨඓ"), bstack11111_opy_ (u"ࠫࠬඔ")).lower()
            self.store[bstack11111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩඕ")] = [bstack1l111l11l1_opy_.bstack1l111ll11l_opy_()]
            if bstack1ll1l11ll_opy_(threading.current_thread(), bstack11111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪඖ"), None):
                self.store[bstack11111_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫ඗")].append(bstack1l111l11l1_opy_.bstack1l111ll11l_opy_())
            else:
                self.store[bstack11111_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧ඘")].append(bstack1l111l11l1_opy_.bstack1l111ll11l_opy_())
            if bstack1l111111l1_opy_:
                self._11llll1111_opy_[bstack1l111111l1_opy_ + bstack11111_opy_ (u"ࠩ࠰ࠫ඙") + attrs.get(bstack11111_opy_ (u"ࠪࡸࡾࡶࡥࠨක"), bstack11111_opy_ (u"ࠫࠬඛ")).lower()] = { bstack11111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨග"): bstack1l111l11l1_opy_ }
            bstack11ll1l1l1_opy_.bstack11llllllll_opy_(bstack11111_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧඝ"), bstack1l111l11l1_opy_)
        else:
            bstack1l111llll1_opy_ = {
                bstack11111_opy_ (u"ࠧࡪࡦࠪඞ"): uuid4().__str__(),
                bstack11111_opy_ (u"ࠨࡶࡨࡼࡹ࠭ඟ"): bstack11111_opy_ (u"ࠩࡾࢁࠥࢁࡽࠨච").format(attrs.get(bstack11111_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪඡ")), attrs.get(bstack11111_opy_ (u"ࠫࡦࡸࡧࡴࠩජ"), bstack11111_opy_ (u"ࠬ࠭ඣ"))) if attrs.get(bstack11111_opy_ (u"࠭ࡡࡳࡩࡶࠫඤ"), []) else attrs.get(bstack11111_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧඥ")),
                bstack11111_opy_ (u"ࠨࡵࡷࡩࡵࡥࡡࡳࡩࡸࡱࡪࡴࡴࠨඦ"): attrs.get(bstack11111_opy_ (u"ࠩࡤࡶ࡬ࡹࠧට"), []),
                bstack11111_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧඨ"): bstack11l1111l1_opy_(),
                bstack11111_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫඩ"): bstack11111_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭ඪ"),
                bstack11111_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫණ"): attrs.get(bstack11111_opy_ (u"ࠧࡥࡱࡦࠫඬ"), bstack11111_opy_ (u"ࠨࠩත"))
            }
            if attrs.get(bstack11111_opy_ (u"ࠩ࡯࡭ࡧࡴࡡ࡮ࡧࠪථ"), bstack11111_opy_ (u"ࠪࠫද")) != bstack11111_opy_ (u"ࠫࠬධ"):
                bstack1l111llll1_opy_[bstack11111_opy_ (u"ࠬࡱࡥࡺࡹࡲࡶࡩ࠭න")] = attrs.get(bstack11111_opy_ (u"࠭࡬ࡪࡤࡱࡥࡲ࡫ࠧ඲"))
            if not self.bstack1l11l1l1l1_opy_:
                self._11llll1111_opy_[self._11llllll11_opy_()][bstack11111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪඳ")].add_step(bstack1l111llll1_opy_)
                threading.current_thread().current_step_uuid = bstack1l111llll1_opy_[bstack11111_opy_ (u"ࠨ࡫ࡧࠫප")]
            self.bstack1l11l1l1l1_opy_.append(bstack1l111llll1_opy_)
    @bstack1l111ll1ll_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack11lll1lll1_opy_()
        self._1l11111111_opy_(messages)
        current_test_id = bstack1ll1l11ll_opy_(threading.current_thread(), bstack11111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧࠫඵ"), None)
        bstack1l111111l1_opy_ = current_test_id if current_test_id else bstack1ll1l11ll_opy_(threading.current_thread(), bstack11111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡻࡩࡵࡧࡢ࡭ࡩ࠭බ"), None)
        bstack1l11l1l11l_opy_ = bstack1l11111l11_opy_.get(attrs.get(bstack11111_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫභ")), bstack11111_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ම"))
        bstack1l1111l1l1_opy_ = attrs.get(bstack11111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧඹ"))
        if bstack1l11l1l11l_opy_ != bstack11111_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨය") and not attrs.get(bstack11111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩර")) and self._1l1111l111_opy_:
            bstack1l1111l1l1_opy_ = self._1l1111l111_opy_
        bstack1l111111ll_opy_ = Result(result=bstack1l11l1l11l_opy_, exception=bstack1l1111l1l1_opy_, bstack11lllll1ll_opy_=[bstack1l1111l1l1_opy_])
        if attrs.get(bstack11111_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ඼"), bstack11111_opy_ (u"ࠪࠫල")).lower() in [bstack11111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ඾"), bstack11111_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧ඿")]:
            bstack1l111111l1_opy_ = current_test_id if current_test_id else bstack1ll1l11ll_opy_(threading.current_thread(), bstack11111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡷ࡬ࡸࡪࡥࡩࡥࠩව"), None)
            if bstack1l111111l1_opy_:
                bstack1l111l1l11_opy_ = bstack1l111111l1_opy_ + bstack11111_opy_ (u"ࠢ࠮ࠤශ") + attrs.get(bstack11111_opy_ (u"ࠨࡶࡼࡴࡪ࠭ෂ"), bstack11111_opy_ (u"ࠩࠪස")).lower()
                self._11llll1111_opy_[bstack1l111l1l11_opy_][bstack11111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭හ")].stop(time=bstack11l1111l1_opy_(), duration=int(attrs.get(bstack11111_opy_ (u"ࠫࡪࡲࡡࡱࡵࡨࡨࡹ࡯࡭ࡦࠩළ"), bstack11111_opy_ (u"ࠬ࠶ࠧෆ"))), result=bstack1l111111ll_opy_)
                bstack11ll1l1l1_opy_.bstack11llllllll_opy_(bstack11111_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ෇"), self._11llll1111_opy_[bstack1l111l1l11_opy_][bstack11111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ෈")])
        else:
            bstack1l111111l1_opy_ = current_test_id if current_test_id else bstack1ll1l11ll_opy_(threading.current_thread(), bstack11111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡪࡦࠪ෉"), None)
            if bstack1l111111l1_opy_ and len(self.bstack1l11l1l1l1_opy_) == 1:
                current_step_uuid = bstack1ll1l11ll_opy_(threading.current_thread(), bstack11111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡷࡹ࡫ࡰࡠࡷࡸ࡭ࡩ්࠭"), None)
                self._11llll1111_opy_[bstack1l111111l1_opy_][bstack11111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭෋")].bstack1l11l11l1l_opy_(current_step_uuid, duration=int(attrs.get(bstack11111_opy_ (u"ࠫࡪࡲࡡࡱࡵࡨࡨࡹ࡯࡭ࡦࠩ෌"), bstack11111_opy_ (u"ࠬ࠶ࠧ෍"))), result=bstack1l111111ll_opy_)
            else:
                self.bstack1l111l1l1l_opy_(attrs)
            self.bstack1l11l1l1l1_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack11111_opy_ (u"࠭ࡨࡵ࡯࡯ࠫ෎"), bstack11111_opy_ (u"ࠧ࡯ࡱࠪා")) == bstack11111_opy_ (u"ࠨࡻࡨࡷࠬැ"):
                return
            self.messages.push(message)
            bstack1l1111l11l_opy_ = []
            if bstack11ll1l1l1_opy_.bstack1l111ll1l1_opy_():
                bstack1l1111l11l_opy_.append({
                    bstack11111_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬෑ"): bstack11l1111l1_opy_(),
                    bstack11111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫි"): message.get(bstack11111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬී")),
                    bstack11111_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫු"): message.get(bstack11111_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ෕")),
                    **bstack11ll1l1l1_opy_.bstack1l111ll1l1_opy_()
                })
                if len(bstack1l1111l11l_opy_) > 0:
                    bstack11ll1l1l1_opy_.bstack1ll1l11l1l_opy_(bstack1l1111l11l_opy_)
        except Exception as err:
            pass
    def close(self):
        bstack11ll1l1l1_opy_.bstack1l11111lll_opy_()
    def bstack1l111l1l1l_opy_(self, bstack1l11l11ll1_opy_):
        if not bstack11ll1l1l1_opy_.bstack1l111ll1l1_opy_():
            return
        kwname = bstack11111_opy_ (u"ࠧࡼࡿࠣࡿࢂ࠭ූ").format(bstack1l11l11ll1_opy_.get(bstack11111_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨ෗")), bstack1l11l11ll1_opy_.get(bstack11111_opy_ (u"ࠩࡤࡶ࡬ࡹࠧෘ"), bstack11111_opy_ (u"ࠪࠫෙ"))) if bstack1l11l11ll1_opy_.get(bstack11111_opy_ (u"ࠫࡦࡸࡧࡴࠩේ"), []) else bstack1l11l11ll1_opy_.get(bstack11111_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬෛ"))
        error_message = bstack11111_opy_ (u"ࠨ࡫ࡸࡰࡤࡱࡪࡀࠠ࡝ࠤࡾ࠴ࢂࡢࠢࠡࡾࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࡡࠨࡻ࠲ࡿ࡟ࠦࠥࢂࠠࡦࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࡡࠨࡻ࠳ࡿ࡟ࠦࠧො").format(kwname, bstack1l11l11ll1_opy_.get(bstack11111_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧෝ")), str(bstack1l11l11ll1_opy_.get(bstack11111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩෞ"))))
        bstack1l1111l1ll_opy_ = bstack11111_opy_ (u"ࠤ࡮ࡻࡳࡧ࡭ࡦ࠼ࠣࡠࠧࢁ࠰ࡾ࡞ࠥࠤࢁࠦࡳࡵࡣࡷࡹࡸࡀࠠ࡝ࠤࡾ࠵ࢂࡢࠢࠣෟ").format(kwname, bstack1l11l11ll1_opy_.get(bstack11111_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ෠")))
        bstack11lllllll1_opy_ = error_message if bstack1l11l11ll1_opy_.get(bstack11111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ෡")) else bstack1l1111l1ll_opy_
        bstack1l111l1ll1_opy_ = {
            bstack11111_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ෢"): self.bstack1l11l1l1l1_opy_[-1].get(bstack11111_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ෣"), bstack11l1111l1_opy_()),
            bstack11111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ෤"): bstack11lllllll1_opy_,
            bstack11111_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ෥"): bstack11111_opy_ (u"ࠩࡈࡖࡗࡕࡒࠨ෦") if bstack1l11l11ll1_opy_.get(bstack11111_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ෧")) == bstack11111_opy_ (u"ࠫࡋࡇࡉࡍࠩ෨") else bstack11111_opy_ (u"ࠬࡏࡎࡇࡑࠪ෩"),
            **bstack11ll1l1l1_opy_.bstack1l111ll1l1_opy_()
        }
        bstack11ll1l1l1_opy_.bstack1ll1l11l1l_opy_([bstack1l111l1ll1_opy_])
    def _11llllll11_opy_(self):
        for bstack1l11l111ll_opy_ in reversed(self._11llll1111_opy_):
            bstack11llll11ll_opy_ = bstack1l11l111ll_opy_
            data = self._11llll1111_opy_[bstack1l11l111ll_opy_][bstack11111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ෪")]
            if isinstance(data, bstack11lllll1l1_opy_):
                if not bstack11111_opy_ (u"ࠧࡆࡃࡆࡌࠬ෫") in data.bstack1l111l1111_opy_():
                    return bstack11llll11ll_opy_
            else:
                return bstack11llll11ll_opy_
    def _1l11111111_opy_(self, messages):
        try:
            bstack11llll11l1_opy_ = BuiltIn().get_variable_value(bstack11111_opy_ (u"ࠣࠦࡾࡐࡔࡍࠠࡍࡇ࡙ࡉࡑࢃࠢ෬")) in (bstack1l11l1111l_opy_.DEBUG, bstack1l11l1111l_opy_.TRACE)
            for message, bstack1l111l11ll_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack11111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ෭"))
                level = message.get(bstack11111_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ෮"))
                if level == bstack1l11l1111l_opy_.FAIL:
                    self._1l1111l111_opy_ = name or self._1l1111l111_opy_
                    self._1l1111ll11_opy_ = bstack1l111l11ll_opy_.get(bstack11111_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧ෯")) if bstack11llll11l1_opy_ and bstack1l111l11ll_opy_ else self._1l1111ll11_opy_
        except:
            pass
    @classmethod
    def bstack11llllllll_opy_(self, event: str, bstack11lllll11l_opy_: bstack1l11l11lll_opy_, bstack1l11111l1l_opy_=False):
        if event == bstack11111_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ෰"):
            bstack11lllll11l_opy_.set(hooks=self.store[bstack11111_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࠪ෱")])
        if event == bstack11111_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨෲ"):
            event = bstack11111_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪෳ")
        if bstack1l11111l1l_opy_:
            bstack11llll1l11_opy_ = {
                bstack11111_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭෴"): event,
                bstack11lllll11l_opy_.bstack1l111l111l_opy_(): bstack11lllll11l_opy_.bstack1l11l111l1_opy_(event)
            }
            self.bstack1l111lll11_opy_.append(bstack11llll1l11_opy_)
        else:
            bstack11ll1l1l1_opy_.bstack11llllllll_opy_(event, bstack11lllll11l_opy_)
class Messages:
    def __init__(self):
        self._11llll1lll_opy_ = []
    def bstack11llll1l1l_opy_(self):
        self._11llll1lll_opy_.append([])
    def bstack11lll1lll1_opy_(self):
        return self._11llll1lll_opy_.pop() if self._11llll1lll_opy_ else list()
    def push(self, message):
        self._11llll1lll_opy_[-1].append(message) if self._11llll1lll_opy_ else self._11llll1lll_opy_.append([message])
class bstack1l11l1111l_opy_:
    FAIL = bstack11111_opy_ (u"ࠪࡊࡆࡏࡌࠨ෵")
    ERROR = bstack11111_opy_ (u"ࠫࡊࡘࡒࡐࡔࠪ෶")
    WARNING = bstack11111_opy_ (u"ࠬ࡝ࡁࡓࡐࠪ෷")
    bstack1l1111ll1l_opy_ = bstack11111_opy_ (u"࠭ࡉࡏࡈࡒࠫ෸")
    DEBUG = bstack11111_opy_ (u"ࠧࡅࡇࡅ࡙ࡌ࠭෹")
    TRACE = bstack11111_opy_ (u"ࠨࡖࡕࡅࡈࡋࠧ෺")
    bstack1l11l1l1ll_opy_ = [FAIL, ERROR]
def bstack1l11l1l111_opy_(bstack11lllll111_opy_):
    if not bstack11lllll111_opy_:
        return None
    if bstack11lllll111_opy_.get(bstack11111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ෻"), None):
        return getattr(bstack11lllll111_opy_[bstack11111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭෼")], bstack11111_opy_ (u"ࠫࡺࡻࡩࡥࠩ෽"), None)
    return bstack11lllll111_opy_.get(bstack11111_opy_ (u"ࠬࡻࡵࡪࡦࠪ෾"), None)
def bstack11llll1ll1_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack11111_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ෿"), bstack11111_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ฀")]:
        return
    if hook_type.lower() == bstack11111_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧก"):
        if current_test_uuid is None:
            return bstack11111_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭ข")
        else:
            return bstack11111_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨฃ")
    elif hook_type.lower() == bstack11111_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ค"):
        if current_test_uuid is None:
            return bstack11111_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡆࡒࡌࠨฅ")
        else:
            return bstack11111_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪฆ")