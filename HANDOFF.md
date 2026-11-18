# 交接說明（給接手的 AI agent）

> 這份文件是為了從 Claude Code 交給別的 agent（例如 Codex）繼續做。**規則以 `CLAUDE.md` 為準**（與使用者討論後定稿，優先於舊版作業手冊）。交作業前可以刪除本檔與 `AGENTS.md`、`tools/`，它們不屬於 wiki 內容。

## 1. 專案是什麼
- 這是一份課程作業：用 Karpathy 的 LLM Wiki 模式（`raw/` 原始資料 → `wiki/` 由 AI 維護 → `CLAUDE.md` 規則；三個動作 ingest／query／lint）建立「GTA 歷代介紹」wiki，再用 wiki 產生一份給「沒玩過 GTA 的大學生」看的教學 HTML 簡報。
- **截止：2026-11-23 23:59**（遲交到 2026-11-24 16:00）。今天是 2026-11-18。
- 繳交項目：①主題簡介 ②wiki 的 GitHub repo 連結（入口 `wiki/index.md`，repo 要設 public）③簡報的 GitHub Pages 網址 ④loop／graph 說明 ⑤`wiki/log.md` 的執行與檢查紀錄 ⑥反思三題（結論→證據→調整，證據要指到 log.md 的哪一筆）。
- 繳交內容裡不要放個人資料（學號、姓名等）；本 repo 是要公開的。

## 2. 目前進度（2026-11-18）
| 步驟 | 狀態 |
|---|---|
| 步驟一：討論範圍、定稿 `CLAUDE.md` | ✅ 完成（commit `fb84fde`）|
| 步驟一：取得 12 篇來源存進 `raw/` | ✅ 完成（raw/01–12，每篇開頭有 source_url 與 fetched）|
| 步驟一：12 篇逐篇 ingest（每篇一個 commit）| ✅ 完成 |
| 第一次 Lint（raw/01–05 後）| ✅ commit `8325de5` |
| 第二次 Lint（raw/01–12 後）| ✅ 已寫進 `wiki/log.md`，**尚未 commit** |
| 第二次 Lint 的「修正 1：來源標註正確性」| ✅ 已修改 18 個 wiki 頁並寫進 log，**尚未 commit** |
| Lint 其餘項目（結構、規則、術語、時效、你本人的抽查）| ⬜ 見第 4 節 |
| 步驟二：query 擬大綱 → 生成 `slides/index.html` → 簡報檢查 | ⬜ 未開始 |
| 步驟三：loop／graph 說明 | ⬜ 未開始 |
| 步驟四：統計表與反思 | ⬜ 未開始 |
| push 到 GitHub、開 Pages | ⬜ 未開始（目前沒有 remote）|

**接手後第一件事**：`git status` 會看到約 20 個已修改檔案（18 個 wiki 頁、`wiki/log.md`、`tools/`、`HANDOFF.md`、`AGENTS.md`）。先 commit，建議訊息：
```
lint+fix: 第二次健檢與來源標註正確性修正
```

## 3. 專案慣例（請照做）
**目錄**：`raw/`（只新增，不可修改）、`wiki/games|concepts|entities|sources/`、`wiki/index.md`、`wiki/log.md`（只能往下加，不改舊紀錄；改錯就在新的一筆說明）。檔名：遊戲頁用英文原名（`GTA V.md`），其餘用中文；來源摘要頁與 raw 同編號。

**Ingest（一次一篇）**：①讀完 raw，用 5 點列出重點、矛盾與預計更新的頁面，**等使用者回「可以」才寫檔**；②寫 sources 摘要頁，更新相關 games／concepts／entities；③自我檢查：本次寫入的每個事實回 raw 找原句，列成表格（事實 | wiki 頁 | raw 原句 | 是否符合），不符的直接修正；④更新 `index.md`，在 `log.md` 加一筆；⑤使用者隨機抽 2 個事實回原文核對，結果補在「人工檢查」那一行；⑥commit。
- 這個專案裡所有逐篇 ingest 的 commit 訊息格式：`ingest: raw/NN 標題`。

**寫作規則重點**（完整版看 `CLAUDE.md`）：繁體中文；不確定寫「待查」，不要用自己的記憶補；每個年份、數字、平台、地點句尾標來源 `[raw/NN]`；來源矛盾兩邊都保留並標「⚠ 來源矛盾」；會變動的資訊標「截至」；讀者是沒玩過 GTA 的大學生，術語第一次出現要解釋；暴力與成人內容以教學角度寫，不渲染細節。

**狀態提醒**：這個專案的使用者每次是明確說「提交…」才 commit；Claude 在 commit 訊息結尾加了 `Co-Authored-By` 行，你不需要照抄。

## 4. 接下來要做什麼（依優先順序）
### A. 把 Lint 剩下的項目做完（詳見 `wiki/log.md` 最後兩個 lint／fix 紀錄）
1. **結構**
   - 12 個來源摘要頁都是孤兒頁：在各頁「相關頁」加一行「來源摘要：[[0N-…]]」連到對應的 `wiki/sources/` 頁。
   - 3 頁 frontmatter 的 `sources` 沒列內文引用的 raw：`GTA IV`（缺 raw/03）、`GTA San Andreas`（缺 raw/09）、`Rockstar Games`（缺 raw/08）。
   - `wiki/log.md` 第一次 Lint 的紀錄裡有一個寫成雙方括號加「0X-...」的範例被當成斷鏈（log 不能改舊紀錄，在下一筆說明即可）。
2. **規則修改（改 `CLAUDE.md`，單獨一個 commit，作為作業反思題第 3 題「workflow 修改」的證據）**，建議加入：
   - 來源沒有日期時，「截至」用抓取日，並在 `sources` 頁註明；來源只給年月時用 `YYYY-MM`。
   - 同時標多篇來源 `[raw/A][raw/B]` 時，只有兩篇都有寫的內容才能這樣標；細節只在一篇就只標那一篇。
   - 「一句話介紹」也要標來源。
   - `sources` 頁的 frontmatter 只列本篇，比較用的引用不算。
   - 新增術語表頁（見下）。
3. **術語表**：新增 `wiki/concepts/術語表.md`（一行一詞），各頁首次出現時連結。優先：Metacritic、GameRankings、ESRB、主線、移植、限時獨占、外傳、資料片、引擎、宇宙、NPC、mod。（Metacritic 與 GameRankings 目前整個 wiki 都沒有解釋。）
4. **時效（需要網路）**：GTA VI 頁有 7 處「截至 2026-11-18 尚未發售」，**2026-11-19 就過期**。11-19 之後抓新來源（Rockstar Newswire 官方公告，加一份評分彙整或新聞）存成 `raw/13-…`、`raw/14-…`，走一次完整 ingest 更新那 7 處（含 Metacritic、預購與發售狀態）。目前 raw/03、raw/06 在發售前一天就寫「已發售」，與官方 raw/04 矛盾。
5. **使用者本人的抽查**：使用者本人從任一篇 ingest 的自我檢查表隨機抽 2 個事實回 raw 核對，補在 `wiki/log.md` 的「人工檢查」；`raw/01` 那一筆總體人工檢查行目前是空的。其他 11 篇的「人工檢查」是 Claude 代抽的（log 裡有註明），請不要改成「使用者本人」。
6. **選配**：所有 game 頁的 ESRB 分級都是「待查」（raw/ 沒有分級來源），簡報裡不要放分級資訊，除非補 ESRB 來源。

### B. 步驟二：簡報（`slides/index.html`）
- 先用 Query 規則（只用 wiki 內容）擬大綱，用表格輸出「頁碼 | 標題 | 重點（3 點內）| 依據的 wiki 頁」，找不到依據的頁標「缺來源」，不要用自己的知識補。**大綱要先給使用者確認再生成 HTML。**
- 建議大綱：封面 → GTA 是什麼 → 三個時代一張圖 → 歷代時間軸 → 2D → 3D → HD（含 GTA Online）→ GTA VI（標「截至」日期）→ 共通玩法 → 小測驗 3 題 → 一頁回顧 → 參考資料（列 raw 來源）。
- 單一 HTML、不用外部套件、方向鍵或點擊換頁、右下角頁碼；每頁底部小字標依據的 wiki 頁（例如「來源：wiki/games/GTA V.md」）；每頁文字不超過 5 行；時間軸與三個時代用圖示；小測驗可點選並顯示對錯；不要用遊戲截圖或官方圖片，用色塊與文字；手機版面也要能用。
- 完成後逐頁檢查「每頁的事實是否都能在對應 wiki 頁找到」，寫進 `wiki/log.md`；再開瀏覽器翻一遍（換頁、文字溢出、手機版），有問題只重生該頁。
- **簡報用到的數字一律帶「截至」日期**；並排矛盾的項目（見 log 的 Lint 紀錄第 5 節）只能用各來源共識的部分。不要把三款遊戲的預算並列比較（IV 是開發預算、V 是開發加行銷預算、VI 是未證實的傳聞，定義不同）。

### C. 發布與繳交
- `git remote add origin …`、push 到 GitHub（public）；Settings → Pages → main 分支根目錄；簡報網址是 `https://<帳號>.github.io/gta-llm-wiki/slides/`；交出前用無痕視窗確認打得開。
- 步驟三：流程圖（取得資料 → Ingest → 對照 raw → 更新索引／日誌 →〔還有來源就回頭〕→ Lint → 查詢擬大綱 → 對得回 Wiki？→ 生成 HTML → 瀏覽檢查 → 發布）；說明重複執行、檢查點、設計理由。這個專案實際跑出來的流程比手冊多了「Lint 發現缺口 → 回頭補來源 → 再跑一圈」，可以拿 commit 順序（`8325de5` 之前與之後）當證據；若有 CLAUDE.md 的修改 commit，就畫「改前」「改後」兩張圖。
- 步驟四：從 `wiki/log.md` 彙整統計表（節點：取得資料／Ingest 自我檢查／人工抽查／Lint／大綱對應檢查／HTML 瀏覽檢查；欄位：執行次數、發現問題數、問題類型舉 1 例、處理方式），再寫反思三題。**反思的例子只能引用這個專案自己的 log**。

## 5. 這個專案踩過的錯（接手後請持續檢查）
- **合併標註**：把只出現在其中一篇 raw 的細節，掛在 `[raw/A][raw/B]` 兩篇下（共抓到 20 處，集中在「一句話介紹」與資料表欄位）。
- **改語氣**：把原文的「褒貶不一」寫成「普通」，把「觀察」寫成「意圖」。
- **自己的推論**：「系列最成功」「1930 年代」「評論在發售前刊出」「研究起來比較方便」等 raw 沒有的話。
- **誤譯慣用語**：例如「previously worked the beat」是「以前在這一區巡邏」，不是「離開警察局」。
- **來源把未來寫成過去**：維基百科在 GTA VI 發售前一天就寫「已發售」。
- 關鍵詞 grep 抓不到上述大部分錯誤（原句確實存在，只是意思被改）；要靠逐句比對語意。

## 6. 工具（`tools/`）
都是純 Python 標準函式庫，用 `python -I`（避免載入當前目錄的模組）。這些腳本原本放在 Claude 的暫存資料夾，這裡是備份。
| 檔案 | 用途 | 用法 |
|---|---|---|
| `tools/lint2.py` | 第二次 Lint 的完整掃描（孤兒頁、斷鏈、frontmatter、並排標註、未標來源、截至日期、game 欄位、術語、log）| `python -I tools/lint2.py .` |
| `tools/lint.py` | 第一次 Lint 的簡化版 | `python -I tools/lint.py .` |
| `tools/combo.py` | 列出所有「同時標 2 篇以上來源」的片段，供人工逐句檢查 | `python -I tools/combo.py .` |
| `tools/recheck.py` | 對 18 個易出錯的詞，確認每個標註的 raw 真的有這個詞 | `python -I tools/recheck.py .` |
| `tools/h2md.py` | 把網頁 HTML 轉成 markdown（抓 raw 用；只做格式轉換，不摘要）| 先用 curl 下載 HTML，再 `python -I tools/h2md.py in.html out.md <source_url> <fetched> id bodyContent`（維基百科）|

抓 raw 的做法：curl 下載 → `h2md.py` 轉換 → 檔案開頭加 `source_url`／`fetched`；比對前請先把 raw 裡的不換行空格（U+00A0）換成一般空格。

## 7. 環境備註
- Windows 11；有 Git Bash 與 PowerShell。git 會跳 LF→CRLF 警告，可忽略。
- 專案目錄：`C:\Users\timli\gta-llm-wiki`；目前在 `master` 分支。
- 檔名含中文與全形括號（例如 `罪惡城（Vice City）.md`），用 git 時路徑要加引號。
