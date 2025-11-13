# ElonLogic — BioChem 資源整合流程

## 0. 核心思維（Elon Musk 式第一性原理）
1. **定義問題本質**：BioChem 需要大量產品資源（圖片、HTML 說明、GHS 圖標）才能快速擴充內容，這些資料已存在 `clone_site` 的 `assets/` 中。
2. **拆解成基本事實**：
   - 資源全為靜態檔案（HTML、圖片、SVG、JS）。
   - Django 專案已設定 `STATICFILES_DIRS = [BASE_DIR / 'static']`，可直接掛載任何靜態資料夾。
   - 需保留原始結構以便未來批次解析或轉換。
3. **由基本事實重建解法**：
   - 將 `clone_site/assets` 複製到 `chem_site/bioweb/static/clone_assets`，作為原始素材儲存庫。
   - 在 README / 文檔中記錄掛載位置與用途，方便團隊後續撰寫轉換腳本、管理靜態資源。

## 1. 流程步驟
1. `ls /Users/3cn4gg/Documents/clonjv/clone_site`  
   - 確認來源專案結構，辨識 `assets` 為主要資源根目錄。
2. `cp -R /Users/3cn4gg/Documents/clonjv/clone_site/assets chem_site/bioweb/static/clone_assets`  
   - 以原樣遞迴複製，維持檔名、語系分類與 HTML 內容，方便未來比對。
3. 驗證：`ls chem_site/bioweb/static`  
   - 確保 `clone_assets` 目錄存在並包含所有子檔案。
4. 建立本說明 `Elonlogic.md`  
   - 將思考過程、行動與輸出整理成文檔，供團隊追溯。

## 2. 整合後的檔案樹（節錄）
```
chem_site/bioweb/static/
└─ clone_assets/
   ├─ AboutUS_EN.aspx
   ├─ Account/
   ├─ BookCircleBanner/
   ├─ CAS/
   ├─ CASDetailList_0.htm
   ├─ ChemicalProductProperty_DE_CB02079569.htm
   ├─ ChemicalProductProperty_EN_CB02079569.htm
   ├─ ChemicalProductProperty_JP_CB02079569.htm
   ├─ ChemicalProductProperty_KR_CB02079569.htm
   ├─ CompanyLogo/
   ├─ ContactUS_EN.aspx
   ├─ Content/
   ├─ GHS02.jpg … GHS09.jpg
   ├─ NewsImg/
   ├─ ProductCatalog_EN/
   ├─ ProductDetail_EN_*.htm
   ├─ ProductImage/
   ├─ Scripts/
   ├─ Terms_EN.aspx
   └─ … (其餘 HTML / 影像 / SVG / uploadfile 等子目錄)
```

## 3. 後續建議
1. 建立自動化腳本，將 HTML 轉為 Django-friendly JSON / fixtures，方便批次匯入 `products` 模型。
2. 針對常用圖片（GHS、ProductImage）建立命名規則與 CDN/Cloud 儲存策略，減少未來部署負擔。
3. 在 README 中附上 `clone_assets` 來源與更新流程，確保版權與同步性。
