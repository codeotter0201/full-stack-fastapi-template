.PHONY: test-db-up test-db-down test test-clean

# 測試資料庫相關設定
TEST_DB_NAME := test_db
TEST_DB_USER := test_user
TEST_DB_PASSWORD := test_password
TEST_DB_PORT := 5791
TEST_DB_CONTAINER := test-postgres

# 啟動測試資料庫
test-db-up:
	@echo "啟動測試資料庫..."
	docker run --name $(TEST_DB_CONTAINER) \
		-e POSTGRES_USER=$(TEST_DB_USER) \
		-e POSTGRES_PASSWORD=$(TEST_DB_PASSWORD) \
		-e POSTGRES_DB=$(TEST_DB_NAME) \
		-p $(TEST_DB_PORT):5432 \
		-d postgres:15
	@echo "等待資料庫啟動..."
	@sleep 5

# 停止測試資料庫
test-db-down:
	@echo "停止測試資料庫..."
	docker stop $(TEST_DB_CONTAINER) || true
	docker rm $(TEST_DB_CONTAINER) || true

# 執行測試
test: test-db-up
	@echo "執行測試..."
	python app/tests_pre_start.py
	bash scripts/test.sh
	@echo "測試完成，清理環境..."
	@make test-db-down

# 清理測試環境
test-clean: test-db-down
	@echo "清理測試環境..."
	docker system prune -f 