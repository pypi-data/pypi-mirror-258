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
import threading
bstack1lllll1lll1_opy_ = 1000
bstack1lllll1l1l1_opy_ = 5
bstack1llllll1111_opy_ = 30
bstack1lllll1ll1l_opy_ = 2
class bstack1lllll1l1ll_opy_:
    def __init__(self, handler, bstack1llllll11l1_opy_=bstack1lllll1lll1_opy_, bstack1llllll111l_opy_=bstack1lllll1l1l1_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1llllll11l1_opy_ = bstack1llllll11l1_opy_
        self.bstack1llllll111l_opy_ = bstack1llllll111l_opy_
        self.lock = threading.Lock()
        self.timer = None
    def start(self):
        if not self.timer:
            self.bstack1lllll1ll11_opy_()
    def bstack1lllll1ll11_opy_(self):
        self.timer = threading.Timer(self.bstack1llllll111l_opy_, self.bstack1llllll1l11_opy_)
        self.timer.start()
    def bstack1llllll11ll_opy_(self):
        self.timer.cancel()
    def bstack1lllll1l11l_opy_(self):
        self.bstack1llllll11ll_opy_()
        self.bstack1lllll1ll11_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1llllll11l1_opy_:
                t = threading.Thread(target=self.bstack1llllll1l11_opy_)
                t.start()
                self.bstack1lllll1l11l_opy_()
    def bstack1llllll1l11_opy_(self):
        if len(self.queue) <= 0:
            return
        data = self.queue[:self.bstack1llllll11l1_opy_]
        del self.queue[:self.bstack1llllll11l1_opy_]
        self.handler(data)
    def shutdown(self):
        self.bstack1llllll11ll_opy_()
        while len(self.queue) > 0:
            self.bstack1llllll1l11_opy_()