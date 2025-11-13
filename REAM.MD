# Quick Logic Guide (Backup Tool & Workflow)

## 1. 任務分化思路
1. **定位根目錄**：所有指令以 `django_docker_app/` 為起點，確保虛擬環境及專案檔案一致。
2. **備份範圍判斷**：決定要備份整個 repo 或僅 `chem_site/bioweb`，必要時可排除 logs / 靜態檔。
3. **CRC32 命名**：以當前時間戳 (`YYYYMMDD_HHMMSS`) 計算 CRC32，確保備份檔名唯一且可追蹤。
4. **壓縮與檢查**：使用 `zipfile` 將檔案寫入 `backups/`（自動跳過 venv、backups、__pycache__、node_modules…）。
5. **記錄輸出**：備份完成後會印出來源路徑、timestamp 與 CRC 名稱，方便登錄或排程檢視。

## 2. 流程圖（文字版）
```
啟動 Shell
  └─> 決定 root 路徑 (預設 .)
        ├─> 準備排除列表 (DEFAULT_EXCLUDES + --exclude)
        ├─> 建立 backups 目錄
        ├─> 計算 timestamp → CRC32
        └─> 走訪 root.rglob('*')
              ├─> 排除 venv/backups/__pycache__/pyc
              └─> ZIP 寫入 (相對路徑)
完成 → 顯示「Backup created」+ timestamp + CRC
```

## 3. 指令速查
```bash
# 備份整個專案（預設產出 backups/<crc>.zip）
python backup_tool.py

# 只備份 Django 專案並放到自訂資料夾
python backup_tool.py --root chem_site/bioweb --dest ./backups/project

# 指定排除資料夾（可重複）
python backup_tool.py --exclude logs --exclude static/clone_assets

# 自動化（例）：每天凌晨 2 點備份 bioweb 專案
0 2 * * * cd /path/to/django_docker_app && \
    /usr/bin/python backup_tool.py --root chem_site/bioweb >> backup.log 2>&1
```

## 4. 故障排除
| 問題 | 可能原因 | 處理方式 |
| --- | --- | --- |
| `Root directory not found` | `--root` 路徑輸入錯誤 | 確認實際路徑或改用絕對路徑 |
| 備份檔太大 | 含入 clone_assets 或 venv | 使用 `--exclude` 排除大型資料夾 |
| 權限錯誤 | 目的目錄無寫入權限 | 變更 `--dest` 或調整資料夾權限 |

保持這份 REAM.MD 在根目錄，工程師即可快速掌握備份工具的邏輯與操作。***
