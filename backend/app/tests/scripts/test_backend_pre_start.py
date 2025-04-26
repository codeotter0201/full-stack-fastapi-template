from unittest.mock import MagicMock, patch, ANY

from sqlmodel import select

from app.backend_pre_start import init, logger


def test_init_successful_connection() -> None:
    engine_mock = MagicMock()

    session_mock = MagicMock()
    exec_mock = MagicMock(return_value=True)
    session_mock.configure_mock(**{"exec.return_value": exec_mock})

    # 創建一個模擬的上下文管理器，返回 session_mock
    session_context_manager = MagicMock()
    session_context_manager.__enter__.return_value = session_mock
    session_context_manager.__exit__.return_value = None

    # 創建一個會返回上下文管理器的 Session 類別
    session_class_mock = MagicMock(return_value=session_context_manager)

    with (
        patch("app.backend_pre_start.Session", session_class_mock),
        patch.object(logger, "info"),
        patch.object(logger, "error"),
        patch.object(logger, "warn"),
    ):
        try:
            init(engine_mock)
            connection_successful = True
        except Exception:
            connection_successful = False

        assert (
            connection_successful
        ), "The database connection should be successful and not raise an exception."

        # 確認 Session 被使用正確的引擎呼叫
        session_class_mock.assert_called_once_with(engine_mock)

        # 使用 ANY 代替 select(1)，因為每次 select(1) 都會創建不同的物件
        session_mock.exec.assert_called_once_with(ANY)
