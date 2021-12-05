import os

from docutils.nodes import raw
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective

from docs.examples import get_normalized_example_name


_IDOM_EXAMPLE_HOST = os.environ.get("IDOM_DOC_EXAMPLE_SERVER_HOST", "")
_IDOM_STATIC_HOST = os.environ.get("IDOM_DOC_STATIC_SERVER_HOST", "/docs").rstrip("/")


class IteractiveWidget(SphinxDirective):

    has_content = False
    required_arguments = 1
    _next_id = 0

    option_spec = {
        "activate-result": directives.flag,
        "margin": float,
    }

    def run(self):
        IteractiveWidget._next_id += 1
        container_id = f"idom-widget-{IteractiveWidget._next_id}"
        view_id = get_normalized_example_name(
            self.arguments[0],
            # only used if example name starts with "/"
            self.get_source_info()[0],
        )
        return [
            raw(
                "",
                f"""
                <div>
                    <div
                        id="{container_id}"
                        class="interactive widget-container center-content"
                        style="margin-bottom: {self.options.get("margin", 0)}px;"
                    />
                    <script type="module">
                        import {{ mountWidgetExample }} from "{_IDOM_STATIC_HOST}/_static/custom.js";
                        mountWidgetExample(
                            "{container_id}",
                            "{view_id}",
                            "{_IDOM_EXAMPLE_HOST}",
                            {"false" if "activate-result" in self.options else "true"},
                        );
                    </script>
                </div>
                """,
                format="html",
            )
        ]


def setup(app: Sphinx) -> None:
    app.add_directive("idom-view", IteractiveWidget)