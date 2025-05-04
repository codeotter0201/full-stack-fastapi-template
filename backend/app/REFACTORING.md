# 重構說明

## 目標

本次重構的主要目標是棄用舊的 `crud.py` 和 `models.py` 文件，遷移到新的模組化架構。這樣做可以：

1. 將商業邏輯和資料存取分離，符合現代軟體設計的關注點分離原則
2. 提高代碼的可讀性和可維護性
3. 更好地支持測試和依賴注入
4. 遵循更清晰的分層架構

## 新架構說明

新的架構分為以下幾個主要部分：

- **模型層 (Models)**：位於 `app/models/` 目錄下，包含所有數據庫模型的定義
- **結構層 (Schemas)**：位於 `app/schemas/` 目錄下，包含所有 API 請求和響應模型的定義
- **服務層 (Services)**：位於 `app/services/` 目錄下，包含所有業務邏輯
- **倉庫層 (Repositories)**：位於 `app/repositories/` 目錄下，包含所有資料存取邏輯

## 棄用的檔案

以下檔案已被棄用，但為了保持向後兼容性暫時保留：

1. `app/crud.py`：已被新的服務層替代
2. `app/models.py`：已被 `app/models/` 下的模組化模型替代

這些檔案現在只是簡單重新導出相應的新模塊功能，並添加了棄用警告。

## 替代方案

### 替代 `crud.py`

舊的方式：

```python
from app import crud

user = crud.get_user_by_email(session=session, email=email)
```

新的方式：

```python
from app.services.user import UserService

user_service = UserService(session)
user = user_service.get_by_email(email)
```

### 替代 `models.py`

舊的方式：

```python
from app.models import User, Item
```

新的方式：

```python
from app.models import User, Item  # 直接從 app.models 模塊中導入
```

## 重要變化

1. 使用 `UserService` 和 `ItemService` 來處理與用戶和項目相關的業務邏輯
2. 使用 `UserRepository` 和 `ItemRepository` 來處理與資料庫交互的邏輯
3. 添加了新的測試文件來測試服務層的功能
4. 保持 API 接口不變，只更改了內部實現

## 自動警告

當使用棄用的模塊時，系統會顯示警告訊息提醒開發者使用新的結構。例如：

```
DeprecationWarning: The crud module is deprecated. Use app.services instead.
```

## 遷移步驟

要完全遷移到新架構，請按照以下步驟操作：

1. 將所有 `from app import crud` 替換為適當的服務模塊導入
2. 將所有直接使用 `crud` 模塊的代碼替換為使用相應的服務層代碼
3. 更新測試以使用新的服務層而不是 `crud` 模塊

## 注意事項

- 為保持向後兼容性，舊的 `crud.py` 和 `models.py` 文件仍然可以使用，但將來會被移除
- 新的功能應使用新的架構來實現
- 建議逐步更新現有代碼以使用新架構，並確保測試覆蓋所有變更
