# BioChem Django / Docker Stack

This repository contains the `bioweb` Django project plus the `products` and `contact` domain apps that power the BioChem storefront. The project is designed to run inside a Python virtualenv, but it can also be packaged into containers together with Celery workers for background tasks.

---
&dministraor lo setin :|:

cd chem_site/bioweb
./venv/bin/python manage.py createsuperuser

## 1. 快速啟動 (本機環境)

```bash
cd chem_site/bioweb
./venv/bin/pip install -r requirements.txt  # 若尚未安裝依賴
./venv/bin/python manage.py migrate
./venv/bin/python manage.py createsuperuser
./venv/bin/python manage.py runserver
```

伺服器預設在 <http://127.0.0.1:8000/>。

---

## 2. Docker 工作流程

> 若尚未建立 Dockerfile / docker-compose，可參考 `site.markdown` 內的目標結構。以下示範常用命令：

```bash
# 建置映像
docker build -t bioweb-app .

# 使用 docker-compose 啟動 (假設已有 compose 檔)
docker-compose up --build

# 只啟動 web 容器
docker-compose up web
```

---

## 3. Celery 佇列與排程

專案目前尚未內建 Celery 設定，但若要新增非同步任務，可依照下列指令執行：

```bash
# 啟動 worker（使用 Django 設定 bioweb.settings）
celery -A bioweb worker -l info

# 啟動排程 (beat)
celery -A bioweb beat -l info

# 若佇列與 scheduler 都要在同一進程，可用 celery multi
celery -A bioweb multi restart worker1 -l info
```

> 備註：記得在 `INSTALLED_APPS` 中加入 `django_celery_beat` 或其他需要的套件，並在 settings.py 設定 `CELERY_BROKER_URL`、`CELERY_RESULT_BACKEND`。

---

## 4. Django 架構樹狀圖

```
bioweb/                    ← Django 專案
├─ manage.py
├─ bioweb/                 ← 專案設定
│  ├─ settings.py
│  ├─ urls.py
│  ├─ wsgi.py / asgi.py
│  └─ templates/
│     ├─ base.html
│     ├─ home.html
│     └─ partials/
│        ├─ navbar.html
│        └─ footer.html
│
├─ products/               ← 產品領域 app
│  ├─ models.py (Category / Product / Document)
│  ├─ views.py (list/detail)
│  ├─ urls.py
│  └─ templates/products/
│     ├─ list.html
│     └─ detail.html
│
├─ contact/                ← 聯絡表單 app
│  ├─ views.py
│  ├─ urls.py
│  └─ templates/contact/contact.html
└─ static/ + media/        ← 靜態與上傳檔案
```

---

## 5. Elon Musk 式思維導讀

為了在此專案中快速決策，可以嘗試套用 Elon Musk 常強調的「第一性原理」與「極致迭代」思維：

1. **First Principles**  
   - 先拆解需求：BioChem 需要哪些最核心的功能（商品顯示、聯絡表單、付款 API…）？  
   - 針對每個需求往最底層拆：例如商品頁需要哪些資料欄位、靜態檔案要放在哪裡、Celery 是否必要等。

2. **Reasoning from Fundamentals**  
   - 不被既有流程綁住：若目前結構混亂，直接以 arrangements.txt 為藍圖重新配置，而非修修補補。  
   - 任何設定值（如 STATICFILES_DIRS）都應該有可驗證的理由，而非「因為 Django 常這麼做」。

3. **Iterate Quickly with Feedback**  
   - 每做完一段工作就跑 `manage.py check` / `pytest` / docker build，保持快速驗證循環。  
   - 若要導入 Celery 或 Docker，先做最小可行版（MVP），確認流程通了再加入優化（metrics、監控等）。

4. **Optimistic yet Engineer-Driven**  
   - 鎖定長期願景（BioChem 電商平台），但每天實作時專注在可度量的里程碑：  
     - ✅ 設定檔整合完成  
     - ✅ Products 模型與模板完成  
     - 🔜 新增付款流程 / API 整合  
   - 保持「工程師能理解」的文件與腳本，讓未來的你或其他開發者能迅速接手。

---

## 6. 後續建議

1. 將 docker-compose、Dockerfile、requirements.txt 重新生成並與 README 同步。  
2. 若要使用 Celery，先決定 broker（Redis / RabbitMQ）與排程需求，再正式寫入 settings。
3. 撰寫自動化測試（尤其是 products、contact 表單）以確保未來重構時不會破壞功能。

---

## 7. रहनु工具 (CRC-32 命名)

使用 `backup_tool.py` 以 CRC-32（由備份時間戳衍生）為檔名建立壓縮備份：

```bash
# 在專案根目錄
python backup_tool.py                        # 備份整個 repo -> backups/<crc>.zip
python backup_tool.py --root chem_site/bioweb --dest ./backups/project
python backup_tool.py --exclude logs --exclude static
```

備份完成後會輸出原始 timestamp 與對應的 CRC 名稱，以方便對應與迭代。

祝開發順利！🚀

升級0.1🚀
三項工作 第1項"讀取我另一個專案/Users/3cn4gg/Documents/clonjv/clone_site後將資源檔加入目前專案的DJANGO_DOCKER_APP,詳細用ElonMask的邏輯來詳細解說流程樹狀圖說明存檔一份名Elonlogic.md",第2項檢查所有網頁對接跟根據owasp top10列出檢查這次的工作,新增後台管理員的幫我把這後台登入頁隱藏後並給我網址存檔,第三項給我一份這次修改後的樹狀圖存檔名為update13.md

＠2🚀
目前此專案網站沒有打算加入購物車功能但你以這網站的做範例全部比對"https://www.chemicalbook.com/ProductDetail_EN_lutein-powder-5-80_3566778.htm"不用價格欄因為我喜歡這模板,但就先把他的所有名稱、SKU、CAS、圖片、描述先照打先批次抓取克隆,前面問題中意思就是要在Django admin 後台登入頁加入管理及新增商品名功能,但是我要在加入一個很重要的功能有導入商品數據的功能以常用爬蟲數據能通用導入格式,

CODEX:
在 chem_site/bioweb/products/models.py (lines 13-54) 擴充 Product 模型，加入 external_image、purity、package、min_order_kg、supply_ability、update_time、release_date、supplier_name、supplier_location、keywords 等欄位，並建立 0002/0003 遷移（含 Lutein powder 範例資料）重現 ChemicalBook 風格。
chem_site/bioweb/products/admin.py (lines 1-151) 新增快速建檔邏輯（預先帶入 Lutein 範本資料）、自訂欄位分組，以及 CSV 匯入表單。admin/products/change_list.html 加入「匯入商品」按鈕，admin/products/import.html 提供上傳介面與欄位說明。
重新設計前端頁面：products/templates/products/list.html 改為 Recommended supplier 表格樣式；products/templates/products/detail.html 以 ChemicalBook 佈局呈現供應資訊、詢價卡及圖片（支援 external_image），與需求相符。
透過 products/migrations/0003_seed_lutein.py 匯入示範產品資料，搭配先前複製的 /static/clone_assets 圖資可直接使用；若需更多商品，可在 admin 下載 CSV 模板後匯入。
測試：./venv/bin/python manage.py test 全數通過（5 tests），確認欄位與模板改動未破壞既有流程。
導入格式範例
將 UTF-8 CSV 的欄位命名為：name,sku,cas_number,formula,purity,package,min_order_kg,supply_ability,update_time(YYYY-MM-DD),description,supplier_name,supplier_location,external_image,keywords,category，在 admin 產品列表頁的「匯入商品」按鈕上傳即可；相同 SKU 會更新，新的 SKU 會建立。
如還需更多欄位或實際爬蟲整合，再告訴我。

@3 project finishing 
先用ElonMask邏輯思維將整個專案網站全部檢查重新讀取後在給我一份最新的專案樹狀架構圖後包含每個資料夾及資料夾的分類能讓工程師快速理解的邏輯結構圖說明,給我一個可能在執行時普遍發生的錯誤及排除方法,在專案中新增Erroreveythink.md用最快能理解的樹狀圖跟心智圖

CODEX:
依「Elon Musk 第一性原理」重新盤點整個 django_docker_app，整理出最新的邏輯樹與心智圖，並寫入 Erroreveythink.md (line 1)。這份文檔清楚標示 chem_site/bioweb 為現役 Django 專案、products/contact 子 app、static/clone_assets 資源庫，以及其它備份/舊模板的位置，方便工程師快速導航。
同文檔附上心智圖（資料模型、後台管理、前台 UI、測試部署）與常見錯誤排除表，例如缺少 partials/navbar.html、未安裝 Pillow、CSV 匯入欄位錯誤、找不到隱藏 admin URL 等，對應解法如確認 TEMPLATES['DIRS']、pip install Pillow、使用標準 YYYY-MM-DD 日期、依 admin_portal.txt 的 nebula-console/ 登入。
若需要進一步把圖檔或子系統再細分/加註版本資訊，可在 Erroreveythink.md 中擴充對應節點即可。
