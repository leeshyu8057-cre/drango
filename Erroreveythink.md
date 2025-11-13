# ErrorEverything – BioChem Project Snapshot

## 1. 目錄邏輯樹（Elon 模式拆解）
```
django_docker_app/
├─ chem_site/                         # 主專案根目錄
│  ├─ bioweb/                         # 現行 Django 專案
│  │  ├─ manage.py
│  │  ├─ bioweb/                      # 設定＋URL＋共用模板
│  │  │  ├─ settings.py               # 開發環境設定（DEBUG, static/media, apps）
│  │  │  ├─ urls.py                   # 隱藏 admin (nebula-console) + app routes
│  │  │  └─ templates/
│  │  │     ├─ base.html
│  │  │     ├─ home.html
│  │  │     └─ partials/{navbar,footer}.html
│  │  ├─ products/                    # 商品領域 app
│  │  │  ├─ models.py                 # Category/Product/Document with ChemicalBook fields
│  │  │  ├─ admin.py                  # 快速新增＋CSV匯入＋DocumentInline
│  │  │  ├─ migrations/               # 0001 schema, 0002 field擴充, 0003 Lutein seed
│  │  │  ├─ templates/products/       # list/detail mimic ChemicalBook
│  │  │  └─ tests.py                  # list/detail view tests
│  │  ├─ contact/                     # 聯絡表單 app
│  │  │  ├─ views.py / urls.py / templates/contact
│  │  │  └─ tests.py
│  │  ├─ static/
│  │  │  └─ clone_assets/             # 從 clone_site 匯入的資源庫
│  │  └─ templates/                   # 舊版共用模板
│  ├─ backup_*                        # 舊備份骨架，不再使用
│  ├─ contact/, products/, templates/ # 早期版本殘留
│  └─ venv/                           # 舊虛擬環境
├─ Elonlogic.md / owasp_checklist.md  # 文檔
├─ admin_portal.txt                   # 隱藏後台位置紀錄
├─ README.md / update13.md            # 使用說明與最新樹狀圖
└─ venv/                              # 專案根虛擬環境（未使用，可刪或留）
```

## 2. 心智圖（常見任務 → 關聯模組）
```
目標：ChemicalBook 風格 BioChem
├─ 資料模型
│  ├─ Category/Product/Document (products/models.py)
│  ├─ Lutein 範本 (migration 0003)
│  └─ Static assets (static/clone_assets)
├─ 後台管理
│  ├─ 隱藏 admin URL (urls.py -> nebula-console)
│  ├─ 快速預填表單 (ProductAdmin.get_changeform_initial_data)
│  └─ CSV 匯入 (ProductImportForm + import_products view)
├─ 前台 UI
│  ├─ 列表：Recommended supplier 表格 (products/templates/list.html)
│  └─ 詳細：Inquiry 模板 (products/templates/detail.html)
├─ 測試與部署
│  ├─ ./venv/bin/python manage.py test
│  ├─ Pillow 依賴 (ImageField)
│  └─ README / Elonlogic 指引
```

## 3. 常見錯誤 & 快速排除
| 錯誤情境 | 可能原因 | 解決步驟 |
| --- | --- | --- |
| `django.template.exceptions.TemplateDoesNotExist: partials/navbar.html` | 測試環境未載入 `bioweb/bioweb/templates/partials/navbar.html`（或路徑錯誤） | 確認 `TEMPLATES['DIRS'] = [BASE_DIR / 'bioweb' / 'templates']`，並確保 `collectstatic` / git 也包含 partials |
| `products.Product.image: Cannot use ImageField because Pillow is not installed` | 新環境缺 Pillow | `cd chem_site/bioweb && ./venv/bin/pip install Pillow` 然後重跑 `manage.py check` |
| 匯入商品 CSV 後欄位錯位或日期錯誤 | CSV 未含 `sku`、日期格式非 `YYYY-MM-DD` | 依 `admin/products/import` 提示整理欄位；日期使用 ISO 格式；非數值欄位請留空 |
| 無法找到 admin 登入頁 | admin 已改至 `nebula-console/` | 依 `admin_portal.txt` 提供的 URL，或在 `urls.py` 修改 `HIDDEN_ADMIN_PATH` 後重新部署 |
