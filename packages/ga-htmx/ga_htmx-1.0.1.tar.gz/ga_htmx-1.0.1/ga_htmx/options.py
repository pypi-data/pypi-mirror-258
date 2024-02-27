from django.conf import settings

DEFAULT_HX_SWAP = getattr(settings, "HX_DEFAULT_SWAP", "innerHTML")
DEFAULT_HX_SWAP_DELAY = getattr(settings, "HX_DEFAULT_SWAP_DELAY", "swap:0.5s")
DEFAULT_HX_SWAP_DELAYED = f"{DEFAULT_HX_SWAP} {DEFAULT_HX_SWAP_DELAY}" if DEFAULT_HX_SWAP_DELAY else DEFAULT_HX_SWAP
DEFAULT_HX_ATTRS = getattr(settings, "HX_DEFAULT_ATTRS", {})
DEFAULT_HX_TARGET = getattr(settings, "HX_DEFAULT_TARGET", "")
DEFAULT_HX_TARGET_ID = f"#{DEFAULT_HX_TARGET}"
HTMX_ENABLED = getattr(settings, "HTMX_ENABLED", False)
AUTO_PUSH = getattr(settings, "HX_AUTO_PUSH", False)
