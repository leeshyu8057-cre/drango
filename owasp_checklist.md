# BioChem OWASP Top 10 檢查（針對最新整合工作）

| 項目 | 檢查結果 / 待辦 | 相關檔案 / 說明 |
| --- | --- | --- |
| A01:2021 Broken Access Control | ✅ 使用 Django auth + 自訂隱藏 URL `nebula-console/`，降低掃描風險。但尚未啟用登入節流 / MFA。 | `chem_site/bioweb/bioweb/urls.py#L8`，`admin_portal.txt` |
| A02:2021 Cryptographic Failures | ⚠️ `SECRET_KEY` 仍為預設，需改用環境變數；HTTPS 於部署時需強制。 | `chem_site/bioweb/bioweb/settings.py:22` |
| A03:2021 Injection | ✅ 不使用原生 SQL；`contact` 表單目前只做伺服器端渲染，請保持 `csrf_token`。若未來匯入 `clone_assets` HTML，需過濾。 | `chem_site/bioweb/products/views.py:1-26`, `contact/views.py:1-11` |
| A04:2021 Insecure Design | ⚠️ `contact` 無 spam 防護、`clone_assets` HTML 可能含舊 script；導入前需 Threat Model。 | `chem_site/bioweb/contact/templates/contact/contact.html` |
| A05:2021 Security Misconfiguration | ⚠️ `DEBUG=True`、允許所有 HOST，僅適用開發；記得於生產修改。 | `chem_site/bioweb/bioweb/settings.py:26-28` |
| A06:2021 Vulnerable Components | ⚠️ 未針對 `requirements.txt` 鎖版；請使用 `pip freeze > requirements.txt` 並執行 `pip-audit`。 | `chem_site/bioweb/venv` |
| A07:2021 Identification & Authentication Failures | ✅ Admin 登入頁客製化、使用 Django session；建議加上 `django-axes` 或 reCAPTCHA。 | `chem_site/bioweb/bioweb/templates/admin/login.html` |
| A08:2021 Software and Data Integrity Failures | ⚠️ `clone_assets` 來源未驗證 hash；若用於生產，請加入 checksum 或簽章流程。 | `chem_site/bioweb/static/clone_assets` |
| A09:2021 Security Logging & Monitoring Failures | ⚠️ 尚未設定自訂 logging handler；建議至少把 admin/登入錯誤寫入檔案。 | `chem_site/bioweb/bioweb/settings.py` |
| A10:2021 SSRF | ✅ 目前無外部 HTTP 請求（PayPal API 尚未啟用），請保持隔離。 | N/A |

> 「檢查所有網頁對接」結果：`/`, `/products/`, `/products/<id>/`, `/contact/`, `/nebula-console/` 均可對應到 view / template，表單具備 CSRF token；靜態資源由 `STATICFILES_DIRS` 提供。後續接上 PayPal 或 API 時需重新進行安全檢查。
