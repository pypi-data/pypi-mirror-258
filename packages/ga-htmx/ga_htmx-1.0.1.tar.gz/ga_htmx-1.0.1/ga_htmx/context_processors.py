from .options import DEFAULT_HX_TARGET, DEFAULT_HX_TARGET_ID, DEFAULT_HX_SWAP, DEFAULT_HX_SWAP_DELAY, DEFAULT_HX_ATTRS
from collections import OrderedDict

__attrs = OrderedDict()
for key, value in DEFAULT_HX_ATTRS.items():
    __attrs[f"default_{key}"] = value

def htmx(request):
    return {
        'default_hx_target': DEFAULT_HX_TARGET,
        'default_hx_target_id': DEFAULT_HX_TARGET_ID,
        'default_hx_swap': DEFAULT_HX_SWAP,
        'default_hx_swap_delayed': f"{DEFAULT_HX_SWAP} {DEFAULT_HX_SWAP_DELAY}" if DEFAULT_HX_SWAP_DELAY else DEFAULT_HX_SWAP,
        **__attrs,
    }
