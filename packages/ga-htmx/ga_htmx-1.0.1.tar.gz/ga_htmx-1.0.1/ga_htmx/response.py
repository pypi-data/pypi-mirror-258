"""
🔗Response Headers Reference
Header	                Description
----------------------- ------------------------------------------------------------
HX-Location             Allows you to do a client-side redirect that does not do a full page reload
HX-Push-Url             pushes a new url into the history stack
HX-Redirect             can be used to do a client-side redirect to a new location
HX-Refresh              if set to “true” the client side will do a a full refresh of the page
HX-Replace-Url          replaces the current URL in the location bar
HX-Reswap               Allows you to specify how the response will be swapped. See hx-swap for possible values
HX-Retarget             A CSS selector that updates the target of the content update to a different element on the page
HX-Reselect             A CSS selector that allows you to choose which part of the response is used to be swapped in. Overrides an existing hx-select on the triggering element
HX-Trigger              allows you to trigger client side events, see the documentation for more info (https://htmx.org/headers/hx-trigger/)
HX-Trigger-After-Settle allows you to trigger client side events, see the documentation for more info (https://htmx.org/headers/hx-trigger/)
HX-Trigger-After-Swap   allows you to trigger client side events, see the documentation for more info (https://htmx.org/headers/hx-trigger/)
"""
HXLocation           = "HX-Location"
HXPushUrl            = "HX-Push-Url"
HXRedirect           = "HX-Redirect"
HXRefresh            = "HX-Refresh"
HXReplaceUrl         = "HX-Replace-Url"
HXReswap             = "HX-Reswap"
HXRetarget           = "HX-Retarget"
HXReselect           = "HX-Reselect"
HXTrigger            = "HX-Trigger"
HXTriggerAfterSettle = "HX-Trigger-After-Settle"
HXTriggerAfterSwap   = "HX-Trigger-After-Swap"

