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
    "http://69.63.200.80:8080",
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
                self.assertIn("CodingPlan Docs", html)
                self.assertNotIn("Codinghub Docs", html)
                self.assertNotIn("Codinghub Plan Docs", html)
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
        self.assertIn("<title>CodingPlan教程中心</title>", html)
        self.assertIn('content="CodingPlan教程中心：', html)
        self.assertNotIn("Codinghub 教程中心", html)

    def test_codex_page_uses_local_coding_hub_flow(self):
        html = self.read("codex.html")
        css = self.read("assets/css/styles.css")
        expected_text = [
            "https://coding-hub.sonic.nyc.mn",
            "https://coding-hub.sonic.nyc.mn/keys",
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
        self.assertNotIn("Codex App 自助安装配置全流程，入口已替换为当前 Coding Hub 地址。", html)
        self.assertNotIn('class="visual-card flow-card"', html)
        self.assertEqual(html.count("assets/images/codex/codex-app-flow.png"), 1)
        self.assertIn('class="comic-frame flow-hero-frame reveal"', html)
        self.assertIn("max-height: min(68vh, 760px)", css)
        self.assertIn(".comic-frame.flow-hero-frame img", css)
        self.assertIn("width: min(450px, 100%)", css)
        self.assertIn("object-fit: contain", css)

    def test_gpt_image_uses_coding_hub_domain(self):
        html = self.read("gpt-image-skill.html")
        self.assertIn('export OPENAI_BASE_URL="https://coding-hub.sonic.nyc.mn"', html)
        self.assertNotIn("69.63.200.80", html)

    def test_homepage_matches_reference_home_structure_without_feishu(self):
        html = self.read("index.html")
        css = self.read("assets/css/styles.css")
        expected_text = [
            "Codinghub 自助入口",
            "AI 工具配置，",
            "一次讲清。",
            "设计 · 科技 · 效率",
            "Coding Hub",
            "统一密钥 · 统一模型",
            "配置 Codex",
            "Cherry",
            "绘图",
            "OpenClaw",
            "四条路径",
            "一眼看懂",
            "当前先展示 Codex App 的完整流程图",
        ]
        for text in expected_text:
            with self.subTest(text=text):
                self.assertIn(text, html)

        expected_hooks = [
            'class="nav-action"',
            'class="light-wall"',
            'class="light-beam beam-one"',
            'class="visual-grid comic-preview-grid single-preview-grid"',
        ]
        for hook in expected_hooks:
            with self.subTest(hook=hook):
                self.assertIn(hook, html)

        self.assertIn('<a class="primary-btn" href="codex.html">配置 Codex</a>', html)
        self.assertNotIn("deployment.html", html)
        self.assertNotIn(">部署<", html)
        self.assertNotIn('data-home-tool="deploy"', html)
        self.assertNotIn('data-home-panel="deploy"', html)
        self.assertNotIn('href="deployment.html">部署站点</a>', html)
        self.assertNotIn('href="gpt-image-skill.html">生成图片</a>', html)
        self.assertNotIn('data-home-card="deploy"', html)
        self.assertNotIn("Cloudflare Pages 部署", html)
        self.assertEqual(html.count("assets/images/codex/codex-app-flow.png"), 1)
        self.assertNotIn("assets/images/codex/windows-store-codex.png", html)
        self.assertNotIn("assets/images/codex/codex-first-launch.png", html)
        self.assertNotIn("assets/images/codex/create-api-key.png", html)
        self.assertNotIn("assets/images/codex/use-api-key.png", html)
        self.assertIn("overflow-x: hidden", css)
        self.assertIn(".hero-actions .primary-btn", css)
        self.assertIn(".hub-line span", css)
        self.assertIn(".single-preview-grid", css)
        self.assertIn("grid-template-columns: minmax(160px, 190px)", css)
        self.assertIn("height: 150px", css)

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
