#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# nekoimi 2025/9/14
import abc
import json

from DrissionPage import Chromium
from DrissionPage.items import MixTab
from pydantic import BaseModel

from app.browser import get_browser


class FetchRequest(BaseModel):
    url: str
    timeout: int | None = 60


class BrowserDownloader(abc.ABC):

    @property
    def browser(self) -> Chromium:
        return get_browser()

    def wait_page_complete(self, page_tab: MixTab):
        page_tab.wait.doc_loaded()
        while page_tab.states.ready_state in ["connecting", "loading", "interactive"]:
            page_tab.wait(1, 3.5)

    def execute(self, req: FetchRequest, actions: list[dict], outputs: list[str]) -> dict:
        """Execute the provider-neutral browser job contract.

        Site-specific download() methods remain available as compatibility
        recipes; generic jobs intentionally expose only safe page operations.
        """
        cur_tab = None
        try:
            cur_tab = self.browser.new_tab()
            cur_tab.get(url=req.url, show_errmsg=True, interval=5, timeout=req.timeout)
            self.wait_page_complete(cur_tab)
            for action in actions:
                action_type = action.get("type", "").lower()
                selector = action.get("selector", "")
                timeout = (action.get("timeout_ms") or 0) / 1000
                if action_type == "wait":
                    if selector and not cur_tab.ele(selector, timeout=timeout or None):
                        raise TimeoutError(f"selector not found: {selector}")
                elif action_type == "click":
                    element = cur_tab.ele(selector, timeout=timeout or None)
                    if not element:
                        raise TimeoutError(f"selector not found: {selector}")
                    element.click.left()
                    self.wait_page_complete(cur_tab)
                elif action_type == "input":
                    element = cur_tab.ele(selector, timeout=timeout or None)
                    if not element:
                        raise TimeoutError(f"selector not found: {selector}")
                    element.input(action.get("value", ""))
                elif action_type == "script":
                    cur_tab.run_js(action.get("script", ""))
                elif action_type:
                    raise ValueError(f"unsupported browser action: {action_type}")

            requested = set(outputs or ["html"])
            result = {}
            if "html" in requested:
                result["html"] = cur_tab.html
            if "text" in requested:
                result["text"] = cur_tab.run_js("return document.body ? document.body.innerText : ''") or ""
            if "json" in requested:
                raw = cur_tab.run_js("return document.body ? document.body.innerText : ''") or ""
                try:
                    result["json"] = json.dumps(json.loads(raw), ensure_ascii=False)
                except (TypeError, ValueError):
                    result["json"] = "{}"
            if "screenshot" in requested:
                result["screenshot"] = cur_tab.get_screenshot(as_bytes="png")
            return result
        finally:
            if cur_tab:
                cur_tab.close()

    @abc.abstractmethod
    def download(self, req: FetchRequest) -> str:
        pass
