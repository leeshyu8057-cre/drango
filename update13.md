# BioChem 專案樹狀圖（Update #13）

```
django_docker_app/
├─ README.md
├─ Elonlogic.md
├─ admin_portal.txt
├─ owasp_checklist.md
├─ update13.md  ← 本檔
└─ chem_site/
   ├─ backup_1761658356/…
   ├─ backup_1761658381/…
   ├─ bioweb/
   │  ├─ arrangements.txt
   │  ├─ manage.py
   │  ├─ bioweb/
   │  │  ├─ __init__.py
   │  │  ├─ asgi.py
   │  │  ├─ settings.py
   │  │  ├─ templates/
   │  │  │  ├─ base.html
   │  │  │  ├─ home.html
   │  │  │  └─ partials/
   │  │  │     ├─ footer.html
   │  │  │     └─ navbar.html
   │  │  ├─ templates/admin/login.html
   │  │  └─ urls.py (admin path → `nebula-console/`)
   │  ├─ contact/
   │  │  ├─ templates/contact/contact.html
   │  │  ├─ urls.py
   │  │  └─ tests.py
   │  ├─ products/
   │  │  ├─ migrations/0001_initial.py
   │  │  ├─ templates/products/{list,detail}.html
   │  │  ├─ urls.py
   │  │  └─ tests.py
   │  ├─ static/
   │  │  └─ clone_assets/  ← 由 clone_site 複製的資源檔
   │  └─ templates/
   │     ├─ base.html
   │     ├─ home.html
   │     └─ partials/{footer.html,navbar.html}
   └─ products/ (legacy reference models / templates)
```

> *備註：clone_assets* 內仍保留原始 HTML / 圖片等大量檔案（CAS, ProductImage, Scripts…），如需完整清單請使用 `ls chem_site/bioweb/static/clone_assets`.

---

第二次救援補救紀錄（@2🚀）

本次補救目標：
- 後台管理鏡像功能全部到齊，且不再隱藏 admin（改為 `/admin/`）。
- 產品管理加入兩項能力：CSV 匯入、從 ChemicalBook URL 一鍵同步（爬蟲）。
- 保留既有 `products`/`contact` 架構，移除 PayPal 流程依賴（專案未啟用）。

已完成調整（此備份內）：
- admin 顯示：`chem_si​​te/bioweb/bioweb/urls.py:1` 改為 `path('admin/', admin.site.urls)`。
- 後台匯入：`chem_site/bioweb/products/admin.py:1` 提供 CSV 匯入頁（`admin/products/import.html`）。
- 後台同步：`chem_site/bioweb/products/admin.py:1` 新增「🤖 爬蟲同步」頁（`admin/products/sync.html`）。
- 列表按鈕：`chem_site/bioweb/products/templates/admin/products/change_list.html:1` 顯示「⇪ 匯入商品」「🤖 爬蟲同步」。

通用 CSV 欄位（建議）：
```
name,sku,cas_number,formula,purity,package,min_order_kg,supply_ability,update_time,description,supplier_name,supplier_location,external_image,category,keywords
```

錯誤可能與排除表（Error Matrix）
- Template 找不到 partials：確認 `TEMPLATES['DIRS']` 包含 `bioweb/templates`。
- ImageField 缺 Pillow：安裝 Pillow 後重新執行 `manage.py check`。
- 匯入日期格式錯誤：使用 `YYYY-MM-DD`。
- Admin 同步頁 404：確認 `change_list.html` 兩個按鈕存在，且 `get_urls()` 已增加 `sync/`、`import-data/`。

恢復腳本（本庫）：
- `restore.sh` 放在專案根目錄；會嘗試執行 `manage.py check/migrate/collectstatic`（若環境已有 Django）。
- 若環境未安裝 Django，腳本會略過執行步驟但不報錯。
