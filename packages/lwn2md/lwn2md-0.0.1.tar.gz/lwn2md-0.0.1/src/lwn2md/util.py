from bs4 import BeautifulSoup
from html2text import HTML2Text

base_url = "https://lwn.net"

head_template = """---
status: {status}
author: {author}
colletor: {collector}
collected_time: {collected_time}
translated_time: {translated_time}
translator: {translator}
proofreader: {proofreader}
---

# {title}
"""


def html2md(text: str, output: str = "") -> tuple[str, str]:
    soup = BeautifulSoup(text, "lxml")

    title: str = soup.title.string
    print(title)

    article_text: BeautifulSoup = soup.find("div", class_="ArticleText")

    # 移除摘要
    if article_text.center is not None:
        article_text.center.extract()

    # 处理作者信息
    feature_byline = article_text.find("div", class_="FeatureByline")
    if feature_byline:
        author = feature_byline.b.string
        feature_byline.extract()

    # 处理绝对链接
    links = article_text.find_all("a")
    for link in links:
        href = link.get("href", None)
        if href and not href.startswith("http") and not href.startswith("https"):
            link["href"] = f"{base_url}{href}"

    text_marker = HTML2Text()

    content = text_marker.handle(str(article_text))

    # 移除 article_text 中最后一个 “* * *” 后的所有内容
    parts = content.split("* * *")
    content = "".join(parts[:-1]) if len(parts) > 1 else content

    from datetime import date

    today = date.today().strftime("%Y%m%d")

    title_ = output if output != "" else title

    with open(f"{title_}.md", "w") as fp:
        fp.write(
            head_template.format(
                status="draft",
                author=author,
                collector="",
                collected_time=today,
                translated_time="",
                translator="",
                proofreader="",
                title=title,
            )
        )

        fp.write(content)

    return title, author, content
