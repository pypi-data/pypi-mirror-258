from ..files import abspath_from_current_file


def get_html_template() -> str:
    html = abspath_from_current_file("index.html", __file__)
    with open(html, encoding="utf-8") as f:
        return f.read()
