# Roots 實作演練 — 工程深度解析

| 項目 | 詳情 |
|------|------|
| 考試領域 | D2 — 模型上下文協議 (23%), D4 — 安全與防護機制 (15%) |
| 任務說明 | 2.2 (MCP 基本要素 — roots), 4.3 (存取控制) |
| 來源 | model-context-protocol-advanced-topics / 02-roots-and-messages / 第 08 課 |

---

## 一句話摘要

Roots 是客戶端定義的 `file://` URI，告訴 MCP 伺服器它被允許存取哪些目錄。客戶端透過回呼提供它們，而伺服器必須自行實作授權邏輯來執行存取邊界。

---

## 什麼是 Roots？

Roots 是 MCP 的**檔案系統存取控制**機制。它們回答了一個問題：「這個伺服器應該能看到哪些目錄？」

關鍵特性：
- Roots 由**客戶端定義**（通常來自使用者輸入）
- 它們使用 `file://` URI 格式
- 伺服器在執行時**請求**客戶端提供 roots（非寫死）
- MCP SDK **不會**自動執行 root 邊界——你必須自己實作

---

## 步驟 1：從使用者輸入定義 Roots

```python
# main.py
import sys

async def main():
    # 從命令列參數取得根目錄
    root_paths = sys.argv[1:]
    if not root_paths:
        print("Usage: uv run main.py <root1> [root2] ...")
        sys.exit(1)

    # 將 roots 傳給 MCP 客戶端
    doc_client = await stack.enter_async_context(
        MCPClient(
            command="uv", args=["run", "mcp_server.py"], roots=root_paths
        )
    )
```

理想情況下，使用者指定伺服器可以存取哪些目錄。程式接受 CLI 參數作為路徑，並傳給 `MCPClient`。

---

## 步驟 2：建立 Root 物件

```python
# mcp_client.py
from mcp.types import Root, ListRootsResult
from pydantic import FileUrl
from pathlib import Path

def _create_roots(self, root_paths: list[str]) -> list[Root]:
    """將路徑字串轉換為 Root 物件。"""
    roots = []
    for path in root_paths:
        p = Path(path).resolve()
        file_url = FileUrl(f"file://{p}")
        roots.append(Root(uri=file_url, name=p.name or "Root"))
    return roots
```

根據 MCP 規範，所有 roots 必須有以 `file://` 開頭的 URI。此函數將使用者提供的路徑轉換為正確的 `Root` 物件。

---

## 步驟 3：Roots 回呼

```python
# mcp_client.py
async def _handle_list_roots(
    self, context: RequestContext["ClientSession", None]
) -> ListRootsResult | ErrorData:
    """伺服器請求 roots 時的回呼。"""
    return ListRootsResult(roots=self._roots)
```

客戶端不會立即將 roots 發送給伺服器。相反，伺服器在未來某個時間點請求它們。回呼在 `ListRootsResult` 物件內回傳 roots。

此回呼傳入 `ClientSession`：

```python
self._session = await self._exit_stack.enter_async_context(
    ClientSession(
        _stdio,
        _write,
        list_roots_callback=self._handle_list_roots
        if self._roots
        else None,
    )
)
```

---

## 步驟 4：伺服器存取 Roots

```python
# mcp_server.py
@mcp.tool()
async def list_roots(ctx: Context):
    """列出所有可存取的根目錄。"""
    roots_result = await ctx.session.list_roots()
    client_roots = roots_result.roots
    return [file_url_to_path(root.uri) for root in client_roots]
```

Roots 透過呼叫 `ctx.session.list_roots()` 來存取。這會向客戶端發送請求，觸發根目錄列表回呼。

伺服器在兩種情境中使用 roots：
1. **授權檔案存取** — 在工具讀取或寫入檔案之前
2. **為 LLM 解析路徑** — 當 Claude 需要找到檔案位置時（例如「讀取 todos.txt」）

---

## 步驟 5：實作存取控制

**重要**：MCP SDK 不會執行 root 邊界。你必須自己實作該檢查。

```python
# mcp_server.py
async def is_path_allowed(requested_path: Path, ctx: Context) -> bool:
    roots_result = await ctx.session.list_roots()
    client_roots = roots_result.roots

    if not requested_path.exists():
        return False

    if requested_path.is_file():
        requested_path = requested_path.parent

    for root in client_roots:
        root_path = file_url_to_path(root.uri)
        try:
            requested_path.relative_to(root_path)
            return True
        except ValueError:
            continue

    return False
```

授權函數的運作方式：
1. 從客戶端取得 roots 清單
2. 檢查請求的路徑是否存在
3. 對於檔案，檢查其父目錄
4. 使用 `relative_to()` 驗證路徑是否在允許的 root 內
5. 如果沒有匹配的 root，回傳 `False`

---

## 步驟 6：在工具中使用授權

```python
@mcp.tool()
async def convert_video(input_path: str, format: str, *, ctx: Context):
    """將 MP4 影片檔轉換為其他格式。"""
    input_file = VideoConverter.validate_input(input_path)

    # 確保輸入檔案在某個 root 內
    if not await is_path_allowed(input_file, ctx):
        raise ValueError(f"Access to path is not allowed: {input_path}")

    return await VideoConverter.convert(input_path, format)
```

每個存取檔案系統的工具都應在繼續之前呼叫 `is_path_allowed()`。

---

## CCA 考試相關性

- Roots 是 **D2 基本要素**（任務 2.2）也是 **D4 安全關注點**（任務 4.3）
- 最關鍵的考試重點：**MCP SDK 不會自動執行 root 邊界**——你必須自己實作授權
- 回呼模式（客戶端透過 `list_roots_callback` 按需提供 roots）是常考重點
- Root URI 必須使用 `file://` 協議
- 預期會有情境題，存取控制缺失，你需要找出漏洞
- `relative_to()` 路徑驗證模式是 D4 中常見的實作細節考點

---

## 記憶卡

| # | 問題 | 答案 |
|---|------|------|
| 1 | 在 MCP 中，誰定義 roots？ | **客戶端**定義 roots，通常基於使用者輸入 |
| 2 | Roots 必須使用什麼 URI 協議？ | `file://` |
| 3 | MCP SDK 會自動執行 root 邊界嗎？ | **不會**——你必須自己實作授權邏輯 |
| 4 | 伺服器如何向客戶端請求 roots？ | 呼叫 `ctx.session.list_roots()`，觸發客戶端的 `list_roots_callback` |
| 5 | Roots 回呼回傳什麼？ | 一個包含 `Root` 物件清單的 `ListRootsResult` 物件 |
| 6 | 用什麼 Python 方法檢查路徑是否在 root 內？ | `Path.relative_to()`——如果路徑在 root 外會拋出 `ValueError` |
| 7 | 伺服器在哪兩種情境中使用 roots？ | 1) 授權檔案/資料夾存取，2) 為 LLM 解析路徑 |
| 8 | `list_roots_callback` 在哪裡註冊？ | 在 `ClientSession` 建構函數中 |
