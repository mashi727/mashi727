<p align="center">
  <img src="assets/banner.svg" alt="Massy — Tools that finish the work where it starts." width="100%">
</p>

<p align="center">
  <b>手元の作業を、手元で完結させる道具をつくっています。</b><br>
  <sub>演奏会の録画、紙のアンケート、スキャンした本、計測データ — 目の前の素材を、そのまま使える形へ。</sub>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/PySide6-41CD52?style=flat-square&logo=qt&logoColor=white" alt="PySide6">
  <img src="https://img.shields.io/badge/Swift-F05138?style=flat-square&logo=swift&logoColor=white" alt="Swift">
  <img src="https://img.shields.io/badge/Go-00ADD8?style=flat-square&logo=go&logoColor=white" alt="Go">
  <img src="https://img.shields.io/badge/FFmpeg-007808?style=flat-square&logo=ffmpeg&logoColor=white" alt="FFmpeg">
  <img src="https://img.shields.io/badge/LuaTeX-008080?style=flat-square&logo=latex&logoColor=white" alt="LuaTeX">
</p>

## 👤 About

計測・信号処理とメディア処理のパイプラインを、自分で使う道具として作っています。実験物理の出身です。

**進め方** — システムズエンジニアリングの枠組みで、上流を自分で担い、実装を AI に委任しています。

- **要求定義**：ドメインの知識から、創出すべき価値と課題を定める
- **機能割付**：人が判断すべきこと（UI）と、機械に任せることを分ける
- **V&V**：Verification（仕様どおりに作られているか：lint・テスト・件数の突き合わせ）と、Validation（実物で目的を果たすか：実際の録画・計測データでの確認）で受け入れる

各リポジトリの「考え方」の PAD（問題分析図）が、その要求と機能割付です。

**得意なこと**

- 大容量の計測データを普通の PC で扱う — [iq-analyzer](https://github.com/mashi727/iq-analyzer)（100 GB 級の IQ データをメモリに載せずに閲覧）
- 録音・録画の処理パイプライン — [media-scribe-workflow](https://github.com/mashi727/media-scribe-workflow)（複数 ASR の突き合わせ、TC・相互相関による音声同期）
- 人が判断する所だけを GUI に残すデスクトップアプリ — [Chaptr](https://github.com/mashi727/chaptr) / [enquete](https://github.com/mashi727/enquete) / [book-viewer](https://github.com/mashi727/book-viewer)
- 手順や計画の構造を検査できる形にする道具 — [padkit](https://github.com/mashi727/padkit)

<sub>技術：Python（PySide6・NumPy・ffmpeg）· Swift（Vision）· Go · PHP / MySQL · LuaLaTeX · GitHub Actions（CI・リリースビルド）</sub>

## 🧭 Philosophy — [道具は How である](https://github.com/mashi727/tool-philosophy)

道具の中身は問いません。どういう仕組みで動いているのか、誰が作ったのかは、あまり問題にしません。その代わり、四つのことだけは厳しく問います。

1. 目的にかなう働きをするか
2. 何度やっても同じ結果が出るか（再現性）
3. ほかの道具とうまくつながるか（相互運用性と再利用性）
4. 何をしたかの跡が残り、失敗したときに正直に言うか（来歴と、失敗の仕方）

あとの三つは機械に調べさせることができます（Verification）。最初の一つだけは、そうはいきません（Validation）。目的は道具の中にはないからです。

<sub><a href="https://github.com/mashi727/tool-philosophy">→ 実際にやってきたことの記録を読む</a></sub>

## ✦ Featured — 代表作

<!-- FEATURED:START -->
<sub>01 · 🧭 Ideas &amp; Workflow</sub>

### [padkit](https://github.com/mashi727/padkit)

**手順を図にすると、構造が見える。**

<a href="https://github.com/mashi727/padkit"><img src="https://raw.githubusercontent.com/mashi727/padkit/main/docs/images/release-process.align-depth.png" alt="padkit の画面" width="100%"></a>

LLM が書いた手順や計画を PAD（問題分析図）に描くツールチェーン。散文では頭の中で組み立て直すしかない入れ子・反復・分岐の構造が、そのまま2次元の図として見える。描画エンジンが終了コード 0 のまま図を崩す入力は、独自パーサとの AST 突き合わせで止める。Claude Skill も同梱。

<sub><a href="https://github.com/mashi727/padkit">→ mashi727/padkit を開く</a></sub>

<br>

<sub>02 · 🎬 Video &amp; Audio</sub>

### [media-scribe-workflow](https://github.com/mashi727/media-scribe-workflow)

**録画を、引き直せる知識に。**

<a href="https://github.com/mashi727/media-scribe-workflow"><img src="https://raw.githubusercontent.com/mashi727/media-scribe-workflow/main/docs/images/dashboard-overview.png" alt="media-scribe-workflow の画面" width="100%"></a>

動画・音声から字幕・チャプター・記録 PDF を作る CLI 群。できた記録をトピックごとに束ね直すと、動画をまたいだ索引になる（例：レッスン動画 31 本 → 奏法の課題 84 件）。

<sub><a href="https://github.com/mashi727/media-scribe-workflow">→ mashi727/media-scribe-workflow を開く</a></sub>

<br>

<sub>03 · 🎬 Video &amp; Audio</sub>

### [chaptr](https://github.com/mashi727/chaptr)

**波形を見ながら、動画にチャプターを。**

<a href="https://github.com/mashi727/chaptr"><img src="https://raw.githubusercontent.com/mashi727/chaptr/main/docs/images/editing.png" alt="chaptr の画面" width="100%"></a>

演奏会・レッスン・講義の長尺録画を、2 段の波形とメルスペクトログラムを見ながら章立てするデスクトップアプリ。人が決めるべき境界の判断だけを GUI に残し、書き出しは media-scribe-workflow の CLI に任せている。

<sub><a href="https://github.com/mashi727/chaptr">→ mashi727/chaptr を開く</a></sub>

<br>

<sub>04 · 📈 Measurement &amp; Science</sub>

### [iq-analyzer](https://github.com/mashi727/iq-analyzer)

**100 GB 級の IQ 計測データを、普通の PC で。**

<a href="https://github.com/mashi727/iq-analyzer"><img src="https://raw.githubusercontent.com/mashi727/iq-analyzer/main/docs/images/spectrogram_detail.png" alt="iq-analyzer の画面" width="100%"></a>

Rohde &amp; Schwarz・Keysight の IQ 録音を、メモリに載せずに閲覧する。振幅エンベロープのキャッシュで 121 GB の WVD を 1.6 秒で開き、スペクトログラムはメモリ一定で計算する。

<sub><a href="https://github.com/mashi727/iq-analyzer">→ mashi727/iq-analyzer を開く</a></sub>
<!-- FEATURED:END -->

## ⚡ Now — この1か月、いちばん手を動かしているもの

<sub>直近 30 日のコミット数順。見出しをクリックすると開閉します。</sub>

<!-- NOW:START -->
<details open>
<summary>🥇 <a href="https://github.com/mashi727/book-viewer"><b>book-viewer</b></a> — 🔥 21 commits / 30日 · <sub>Python</sub></summary>
<br>

<a href="https://github.com/mashi727/book-viewer"><img src="assets/now/book-viewer.svg" alt="book-viewer の直近の活動" width="100%"></a>
<p>自炊本 PDF リーダー。見開き・右綴じを PDF 自体に記録し、読書位置を保持</p>
<p align="right"><a href="https://github.com/mashi727/book-viewer"><b>→ mashi727/book-viewer を開く</b></a></p>
<a href="https://github.com/mashi727/book-viewer"><img src="https://raw.githubusercontent.com/mashi727/book-viewer/main/docs/images/main.png" alt="book-viewer の画面" width="100%"></a>

</details>
<details>
<summary>🥈 <a href="https://github.com/mashi727/tool-philosophy"><b>tool-philosophy</b></a> — 🔥 14 commits / 30日 · <sub>Shell</sub></summary>
<br>

<a href="https://github.com/mashi727/tool-philosophy"><img src="assets/now/tool-philosophy.svg" alt="tool-philosophy の直近の活動" width="100%"></a>
<p>道具は How である ── 中身は問わず、目的・再現性・つながり・正直な失敗の四つを問う。実際にやってきたことの記録</p>
<p align="right"><a href="https://github.com/mashi727/tool-philosophy"><b>→ mashi727/tool-philosophy を開く</b></a></p>
<a href="https://github.com/mashi727/tool-philosophy"><img src="https://raw.githubusercontent.com/mashi727/tool-philosophy/main/docs/pad/concept.png" alt="tool-philosophy の画面" width="100%"></a>

</details>
<details>
<summary>🥉 <a href="https://github.com/mashi727/iq-analyzer"><b>iq-analyzer</b></a> — 🔥 7 commits / 30日 · <sub>Python</sub></summary>
<br>

<a href="https://github.com/mashi727/iq-analyzer"><img src="assets/now/iq-analyzer.svg" alt="iq-analyzer の直近の活動" width="100%"></a>
<p>Rohde &amp; Schwarz の IQ 計測データ（IQW / WVH / WVD / iq.tar）を扱う高速ビューア</p>
<p align="right"><a href="https://github.com/mashi727/iq-analyzer"><b>→ mashi727/iq-analyzer を開く</b></a></p>
<a href="https://github.com/mashi727/iq-analyzer"><img src="https://raw.githubusercontent.com/mashi727/iq-analyzer/main/docs/images/main_window.png" alt="iq-analyzer の画面" width="100%"></a>

</details>
<!-- NOW:END -->

## 🗂 All projects

<sub>分野も各行も、最近更新したものが上に来ます（GitHub Actions で毎日自動更新）。</sub>

<!-- INDEX:START -->
#### 📈 Measurement & Science

- [**iq-analyzer**](https://github.com/mashi727/iq-analyzer) — Rohde & Schwarz の IQ 計測データ（IQW / WVH / WVD / iq.tar）を扱う高速ビューア <sub>2026‑10</sub>
- [**route-planner**](https://github.com/mashi727/route-planner) — 標高プロファイルを解析するサイクリング用ルートプランナー <sub>2026‑10</sub>
- [**mandelbrot-viewer**](https://github.com/mashi727/mandelbrot-viewer) — 3 枚の連動プロットで段階的に拡大するマンデルブロ集合ビューア（Numba） <sub>2026‑10</sub>
- [**iPhone-G-Sensor**](https://github.com/mashi727/iPhone-G-Sensor) — iPhone のモーションセンサー記録と、地理院地図上での推測航法による可視化 <sub>2026‑10</sub>

#### 🎬 Video & Audio

- [**chaptr**](https://github.com/mashi727/chaptr) — 演奏会・レッスン・講義の長尺録画を、2 段の波形とメルスペクトログラムを見ながら章立てするデスクトップアプリ（macOS / Windows）。書き出しは media-scribe-workflow の CLI が担う <sub>2026‑10</sub>
- [**score-viewer**](https://github.com/mashi727/score-viewer) — Chaptr のサポートツール。譜面を見ながら、曲名をコピーし返し練習の開始小節を確かめる楽譜 PDF ビューア <sub>2026‑10</sub>
- [**youtube-cover-cropper**](https://github.com/mashi727/youtube-cover-cropper) — YouTube サムネイル用に 16:9・1280×720 で切り出し <sub>2026‑10</sub>
- [**media-scribe-workflow**](https://github.com/mashi727/media-scribe-workflow) — 動画・音声から字幕・チャプター・LuaTeX レポート PDF を生成する CLI 群とパイプライン（Whisper / Deepgram） <sub>2026‑10</sub>
- [**fb-video-downloader**](https://github.com/mashi727/fb-video-downloader) — Facebook 動画の取得と、内容に即したファイル名の自動付与 <sub>2026‑10</sub>

#### 📄 Documents & PDF

- [**macos-vision-ocr**](https://github.com/mashi727/macos-vision-ocr) — Apple Vision による PDF OCR の CLI（オフライン・多言語） <sub>2026‑10</sub>
- [**vision-book-digitizer**](https://github.com/mashi727/vision-book-digitizer) — スキャン書籍 PDF → Markdown + 図版。縦書き対応、Apple Vision でオフライン処理 <sub>2026‑10</sub>
- [**perspective-corrector**](https://github.com/mashi727/perspective-corrector) — スライドを撮影した写真の台形歪みを補正 <sub>2026‑10</sub>
- [**markdown-uploader**](https://github.com/mashi727/markdown-uploader) — Markdown（数式・画像・コールアウト）を Notion へアップロード <sub>2026‑10</sub>
- [**luatex-docker-remote**](https://github.com/mashi727/luatex-docker-remote) — リモートの Docker で LuaTeX をコンパイル。`.sty` の自動同期と日本語組版に対応 <sub>2026‑10</sub>
- [**enquete**](https://github.com/mashi727/enquete) — 紙のアンケート（スキャン PDF）のチェック判定・自由記述 OCR・校正を、結果を PDF 自体に埋め込んで一気通貫で <sub>2026‑10</sub>
- [**book-viewer**](https://github.com/mashi727/book-viewer) — 自炊本 PDF リーダー。見開き・右綴じを PDF 自体に記録し、読書位置を保持 <sub>2026‑10</sub>

#### 🧭 Ideas & Workflow

- [**tool-philosophy**](https://github.com/mashi727/tool-philosophy) — 道具は How である ── 中身は問わず、目的・再現性・つながり・正直な失敗の四つを問う。実際にやってきたことの記録 <sub>2026‑10</sub>
- [**padkit**](https://github.com/mashi727/padkit) — SPD で書いた手順・計画を PAD（問題分析図）として検査・描画する。黙って図を崩す入力を止める lint、SVG/PDF 出力、Claude Skill <sub>2026‑10</sub>

#### 🧰 CLI & Utilities

- [**deepl-cli**](https://github.com/mashi727/deepl-cli) — DeepL API のコマンドラインクライアント。標準入出力・クリップボードに対応 <sub>2026‑10</sub>
- [**claude-imedict**](https://github.com/mashi727/claude-imedict) — Claude Code の対話履歴から自分の語彙を抽出し、macOS 標準と azooKey のユーザー辞書を生成する（読みは macOS 内蔵のトークナイザで推定） <sub>2026‑10</sub>
<!-- INDEX:END -->

---

<details>
<summary><b>Contribution graph</b></summary>
<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/mashi727/mashi727/output/github-contribution-grid-snake-dark.svg">
  <img alt="contribution snake" src="https://raw.githubusercontent.com/mashi727/mashi727/output/github-contribution-grid-snake.svg">
</picture>

</details>
