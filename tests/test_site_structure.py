import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PAGES = [
    "index.html",
    "codex.html",
    "cherry-studio.html",
    "gpt-image-skill.html",
    "openclaw.html",
    "deployment.html",
]

ASSETS = [
    "assets/css/styles.css",
    "assets/js/main.js",
    "assets/favicon.svg",
    "assets/images/codex/codex-app-flow.png",
    "assets/images/codex/windows-store-codex.png",
    "assets/images/codex/codex-first-launch.png",
    "assets/images/codex/create-api-key.png",
    "assets/images/codex/use-api-key.png",
]

BLOCKED_STRINGS = [
    "coding-plan-docs.yeelight.com",
    "yeelight.feishu.cn",
    "www.feishu.cn/docx",
    "assets/images/feishu-",
    "https://coding-hub.yeelight.com",
    "飞书",
    "example.com",
    "your-model-name",
]


class StaticSiteStructureTest(unittest.TestCase):
    def read(self, path):
        return (ROOT / path).read_text(encoding="utf-8")

    def test_required_static_files_exist(self):
        for path in PAGES + ASSETS:
            with self.subTest(path=path):
                self.assertTrue((ROOT / path).is_file(), f"missing {path}")

    def test_pages_use_shared_assets_and_nav(self):
        for page in PAGES:
            html = self.read(page)
            with self.subTest(page=page):
                self.assertIn('href="assets/css/styles.css"', html)
                self.assertIn('src="assets/js/main.js"', html)
                self.assertIn('href="assets/favicon.svg"', html)
                self.assertRegex(html, r'<nav class="nav"')
                for href in PAGES:
                    self.assertIn(f'href="{href}"', html)

    def test_interaction_hooks_are_present(self):
        all_html = "\n".join(self.read(page) for page in PAGES)
        required_hooks = [
            'class="reveal',
            "data-zoom",
            'class="copy-btn"',
            'class="lightbox"',
            "data-scroll-progress",
            "data-home-hero",
            "data-command-generator",
            'class="rail-link',
        ]
        for hook in required_hooks:
            with self.subTest(hook=hook):
                self.assertIn(hook, all_html)

    def test_no_copied_source_domain_or_feishu_assets(self):
        searchable = []
        for pattern in ["*.html", "*.css", "*.js", "*.md"]:
            searchable.extend(ROOT.glob(pattern))
            searchable.extend((ROOT / "assets").glob(f"**/{pattern}"))
        for path in searchable:
            text = path.read_text(encoding="utf-8")
            for blocked in BLOCKED_STRINGS:
                with self.subTest(path=path.relative_to(ROOT), blocked=blocked):
                    self.assertNotIn(blocked, text)

    def test_cloudflare_pages_needs_no_build_step(self):
        package_json = ROOT / "package.json"
        self.assertFalse(package_json.exists(), "pure static site should not require npm build")
        html = self.read("index.html")
        self.assertRegex(html, r"<!doctype html>", "index should be a direct HTML entry")
        self.assertNotRegex(html, re.compile(r"<script[^>]+type=[\"']module[\"']", re.I))

    def test_codex_page_uses_local_coding_hub_flow(self):
        html = self.read("codex.html")
        css = self.read("assets/css/styles.css")
        expected_text = [
            "http://69.63.200.80:8080/login",
            "Codex Desktop App",
            "注册账号",
            "建议使用企微邮箱",
            "安装 Codex App",
            "codex订阅",
            "使用密钥",
            "config.toml",
            "auth.json",
            "macOS 配置方法",
            "Windows 配置方法",
            "Microsoft Store",
            "Download for macOS (Apple Silicon)",
            "Download for macOS (Intel)",
            "Download for Windows",
            "gpt-5.5",
            "请用一句话介绍 Coding Hub。",
        ]
        for text in expected_text:
            with self.subTest(text=text):
                self.assertIn(text, html)

        expected_images = [
            "assets/images/codex/codex-app-flow.png",
            "assets/images/codex/windows-store-codex.png",
            "assets/images/codex/codex-first-launch.png",
            "assets/images/codex/create-api-key.png",
            "assets/images/codex/use-api-key.png",
        ]
        for image in expected_images:
            with self.subTest(image=image):
                self.assertIn(image, html)

        self.assertNotIn("建议使用工作邮箱或团队统一要求的邮箱", html)
        self.assertIn("max-height: min(82vh, 920px)", css)
        self.assertIn("width: auto", css)

    def test_homepage_template_preview_section_is_removed(self):
        html = self.read("index.html")
        removed_text = [
            "视觉预览",
            "用统一模板维护长篇教程",
            "每个教程页都使用同一套 hero",
            "首页 hero 和路径选择",
            "教程页结构：目录、步骤、代码块、FAQ",
        ]
        for text in removed_text:
            with self.subTest(text=text):
                self.assertNotIn(text, html)


if __name__ == "__main__":
    unittest.main()
