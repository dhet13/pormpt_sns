import flet as ft


def show_toast(page: ft.Page, message: str, duration_ms: int = 5000, persist: bool = False) -> None:
    """더 안전한 토스트 표시 방식"""
    try:
        # SnackBar 속성이 없는 경우 대비
        if hasattr(page, 'snack_bar'):
            try:
                snack_bar = ft.SnackBar(ft.Text(message), open=True)
                page.snack_bar = snack_bar
                page.update()
            except Exception as ex:
                print(f"[toast error] snack_bar: {ex}")
                # 폴백: 콘솔 출력
                print(f"[TOAST] {message}")
        else:
            print(f"[TOAST] {message}")
    except Exception as ex:
        print(f"[toast error] {ex}")
        print(f"[TOAST] {message}")

    if persist:
        try:
            page.session.set("flash", message)
        except Exception:
            pass


