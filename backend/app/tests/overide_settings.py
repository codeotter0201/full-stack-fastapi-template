# 測試環境設定檔
# 此檔案用於設定測試時所需的環境變數

import os

# 設定 PostgreSQL 測試環境變數
os.environ["POSTGRES_SERVER"] = "localhost"
os.environ["POSTGRES_USER"] = "test_user"
os.environ["POSTGRES_DB"] = "test_db"
os.environ["POSTGRES_PASSWORD"] = "test_password"
os.environ["POSTGRES_PORT"] = "5791"

# 設定其他需要的測試環境變數（如果有的話）
os.environ["ENVIRONMENT"] = "test"

os.environ["SECRET_KEY"] = "test_secret_key"
os.environ["FIRST_SUPERUSER"] = "test_superuser@example.com"
os.environ["FIRST_SUPERUSER_PASSWORD"] = "test_superuser_password"
