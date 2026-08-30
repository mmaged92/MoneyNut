import re

from django.urls import get_script_prefix, set_script_prefix


class HomeAssistantIngressMiddleware:
    """Make Django work behind Home Assistant's prefixed Ingress URL."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ingress_path = request.META.get(
            "HTTP_X_INGRESS_PATH", ""
        ).rstrip("/")

        previous_prefix = get_script_prefix()

        if ingress_path:
            request.META["SCRIPT_NAME"] = ingress_path
            set_script_prefix(f"{ingress_path}/")

        try:
            response = self.get_response(request)
        finally:
            set_script_prefix(previous_prefix)

        if not ingress_path:
            return response

        # Keep MoneyNut's cookies inside its Home Assistant Ingress path.
        cookie_path = f"{ingress_path}/"

        for cookie_name in (
            "moneynut_csrftoken",
            "moneynut_sessionid",
        ):
            if cookie_name in response.cookies:
                response.cookies[cookie_name]["path"] = cookie_path

        # Correct hard-coded root URLs in rendered HTML.
        content_type = response.get("Content-Type", "")

        if (
            "text/html" in content_type
            and not getattr(response, "streaming", False)
        ):
            html = response.content.decode(response.charset)

            html = re.sub(
                r"""(?P<attribute>href|src|action)=(?P<quote>["'])/(?!/)""",
                rf"""\g<attribute>=\g<quote>{ingress_path}/""",
                html,
            )

            html = re.sub(
                r"""url\((?P<quote>["']?)/(?!/)""",
                rf"""url(\g<quote>{ingress_path}/""",
                html,
            )

            ingress_script = f"""
<script>
(() => {{
    const base = "{ingress_path}";

    const prefixUrl = (url) => {{
        if (
            typeof url === "string" &&
            url.startsWith("/") &&
            !url.startsWith(base + "/")
        ) {{
            return base + url;
        }}

        return url;
    }};

    const originalFetch = window.fetch.bind(window);

    window.fetch = (resource, options) => {{
        if (typeof resource === "string") {{
            resource = prefixUrl(resource);
        }}

        return originalFetch(resource, options);
    }};

    const originalOpen = XMLHttpRequest.prototype.open;

    XMLHttpRequest.prototype.open = function(method, url, ...rest) {{
        return originalOpen.call(
            this,
            method,
            prefixUrl(url),
            ...rest
        );
    }};
}})();
</script>
"""

            html = html.replace(
                "</head>",
                f"{ingress_script}</head>",
                1,
            )

            response.content = html.encode(response.charset)
            response["Content-Length"] = len(response.content)

        return response