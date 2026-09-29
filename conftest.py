import base64
import functools
import http.server
import threading

import pytest

from config.settings import BASE_URL, MOCK_SITE_DIR


def pytest_addoption(parser):
    parser.addoption(
        "--mock-site",
        action="store_true",
        default=False,
        help="Run against the bundled offline replica of XYZ Bank instead of the live site.",
    )


@pytest.fixture(scope="session")
def app_url(request):
    """URL of the bank under test (live GlobalSQA site by default)."""
    if not request.config.getoption("--mock-site"):
        yield BASE_URL
        return

    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass

    handler = functools.partial(QuietHandler, directory=str(MOCK_SITE_DIR))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{server.server_port}/index.html#/login"
    server.shutdown()


@pytest.fixture
def ctx():
    """Scenario-scoped dict for sharing data (balances, account no.) between steps."""
    return {}


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "viewport": {"width": 1366, "height": 768}}


# ---------- attach screenshots to the pytest-html report ----------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call":
        return

    html_plugin = item.config.pluginmanager.getplugin("html")
    if html_plugin is None:
        return
    extras = getattr(report, "extras", [])
    page = item.funcargs.get("page")

    # Screenshots taken by the "a screenshot named ... is taken" step
    for path in item.funcargs.get("ctx", {}).get("screenshots", []):
        extras.append(html_plugin.extras.png(base64.b64encode(path.read_bytes()).decode(), path.name))

    # Automatic screenshot on failure
    if report.failed and page is not None:
        try:
            png = page.screenshot(full_page=True)
            extras.append(html_plugin.extras.png(base64.b64encode(png).decode(), "failure"))
        except Exception:
            pass
    report.extras = extras
