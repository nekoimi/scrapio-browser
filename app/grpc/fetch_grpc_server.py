#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# nekoimi 2025/9/13
from concurrent.futures import ThreadPoolExecutor
import time

from loguru import logger
from app.downloader.browser import BrowserDownloader, FetchRequest
from app.downloader.default.downloader import DefaultBrowserDownloader
from app.downloader.javdb.downloader import JavDBBrowserDownloader
from app.downloader.sehuatang.downloader import SehuatangBrowserDownloader
from app.grpc.fetch_pb2 import FetchResponse
from app.grpc.fetch_pb2 import BrowserJobResponse, BrowserHealthResponse
from app.grpc.fetch_pb2_grpc import PageFetchServiceServicer

thread_pool = ThreadPoolExecutor(max_workers=10)


class ChromiumPageFetchServiceServicer(PageFetchServiceServicer):
    default_downloader: BrowserDownloader
    javdb_downloader: BrowserDownloader
    sehuatang_downloader: BrowserDownloader

    def __init__(self):
        self.default_downloader = DefaultBrowserDownloader()
        self.javdb_downloader = JavDBBrowserDownloader()
        self.sehuatang_downloader = SehuatangBrowserDownloader()

    def Fetch(self, request, context):
        try:
            html = self.default_downloader.download(
                req=FetchRequest(url=request.url, timeout=request.timeout)
            )
            return FetchResponse(success=True, html=html)
        except Exception as e:
            return FetchResponse(success=False, error=str(e))

    def FetchJavDB(self, request, context):
        try:
            html = self.javdb_downloader.download(
                req=FetchRequest(url=request.url, timeout=request.timeout)
            )
            return FetchResponse(success=True, html=html)
        except Exception as e:
            return FetchResponse(success=False, error=str(e))

    def FetchSehuatang(self, request, context):
        try:
            html = self.sehuatang_downloader.download(
                req=FetchRequest(url=request.url, timeout=request.timeout)
            )
            return FetchResponse(success=True, html=html)
        except Exception as e:
            return FetchResponse(success=False, error=str(e))

    def Execute(self, request, context):
        started = time.monotonic()
        logger.info("browser job started request_id={} recipe={} url={}", request.request_id, request.recipe, request.url)
        if not request.url:
            return BrowserJobResponse(
                success=False,
                protocol_version=request.protocol_version or "browser-job.v1",
                request_id=request.request_id,
                error_code="INVALID_JOB",
                error="url is required",
            )
        downloader = {
            "javdb": self.javdb_downloader,
            "sehuatang": self.sehuatang_downloader,
        }.get(request.recipe.lower(), self.default_downloader)
        try:
            timeout = request.timeout_ms / 1000 if request.timeout_ms > 0 else 60
            actions = [
                {
                    "type": item.type,
                    "selector": item.selector,
                    "value": item.value,
                    "script": item.script,
                    "timeout_ms": item.timeout_ms,
                }
                for item in request.actions
            ]
            req = FetchRequest(url=request.url, timeout=timeout)
            if request.recipe and not actions and list(request.outputs or ["html"]) == ["html"]:
                result = {"html": downloader.download(req)}
            else:
                result = downloader.execute(req=req, actions=actions, outputs=list(request.outputs))
            return BrowserJobResponse(
                success=True,
                protocol_version=request.protocol_version or "browser-job.v1",
                request_id=request.request_id,
                html=result.get("html", ""),
                text=result.get("text", ""),
                json=result.get("json", ""),
                screenshot=result.get("screenshot", b""),
                duration_ms=int((time.monotonic() - started) * 1000),
            )
        except TimeoutError as exc:
            return BrowserJobResponse(
                success=False,
                protocol_version=request.protocol_version or "browser-job.v1",
                request_id=request.request_id,
                error_code="TIMEOUT",
                error=str(exc),
                duration_ms=int((time.monotonic() - started) * 1000),
            )
        except Exception as exc:
            return BrowserJobResponse(
                success=False,
                protocol_version=request.protocol_version or "browser-job.v1",
                request_id=request.request_id,
                error_code="EXECUTION_FAILED",
                error=str(exc),
                duration_ms=int((time.monotonic() - started) * 1000),
            )

    def Health(self, request, context):
        return BrowserHealthResponse(
            ready=True,
            protocol_version=request.protocol_version or "browser-job.v1",
            request_id=request.request_id,
            message="ready",
        )
