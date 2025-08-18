import flet as ft


def show_toast(page: ft.Page, message: str, duration_ms: int = 1000, persist: bool = False) -> None:
    """플로팅 토스트 (1초 노출)"""
    print(f"[DEBUG] 토스트 호출됨: {message}")
    
    # 플로팅 토스트 컨테이너 생성
    toast_container = ft.Container(
        content=ft.Text(
            message, 
            color=ft.Colors.WHITE, 
            size=14, 
            weight=ft.FontWeight.W_500,
            text_align=ft.TextAlign.CENTER
        ),
        bgcolor=ft.Colors.BLACK87,
        padding=ft.padding.symmetric(horizontal=24, vertical=12),
        border_radius=25,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=10,
            color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
            offset=ft.Offset(0, 4)
        ),
        animate_opacity=200,
        opacity=1.0,
    )
    
    # 토스트를 페이지 중앙 하단에 배치
    toast_overlay = ft.Container(
        content=toast_container,
        alignment=ft.alignment.bottom_center,
        padding=ft.padding.only(bottom=80),
        width=page.window_width if hasattr(page, 'window_width') else 1200,
        height=page.window_height if hasattr(page, 'window_height') else 800,
    )
    
    try:
        # 기존 토스트 제거 (중복 방지)
        if hasattr(page, 'overlay') and page.overlay:
            # 기존 토스트 오버레이 제거
            page.overlay = [item for item in page.overlay if not _is_toast_overlay(item)]
        
        # 새 토스트 추가
        if hasattr(page, 'overlay') and page.overlay is not None:
            page.overlay.append(toast_overlay)
        else:
            page.overlay = [toast_overlay]
        
        page.update()
        print(f"[DEBUG] 플로팅 토스트 표시 성공: {message}")
        
        # 1초 후 토스트 제거
        import threading
        import time
        
        def remove_toast():
            time.sleep(1.0)  # 1초 고정
            try:
                if hasattr(page, 'overlay') and toast_overlay in page.overlay:
                    page.overlay.remove(toast_overlay)
                    page.update()
                    print(f"[DEBUG] 토스트 제거됨: {message}")
            except Exception as e:
                print(f"[ERROR] 토스트 제거 실패: {e}")
        
        # 백그라운드에서 토스트 제거
        threading.Thread(target=remove_toast, daemon=True).start()
        
    except Exception as ex:
        print(f"[ERROR] 플로팅 토스트 실패: {ex}")
        # 에러 시에도 콘솔에 메시지 출력
        print(f"[FALLBACK] 메시지: {message}")

    if persist:
        try:
            page.session.set("flash", message)
        except Exception:
            pass


def _is_toast_overlay(item) -> bool:
    """토스트 오버레이인지 확인"""
    try:
        # 토스트 오버레이의 특징으로 식별
        return (hasattr(item, 'alignment') and 
                item.alignment == ft.alignment.bottom_center and
                hasattr(item, 'padding') and
                hasattr(item.padding, 'bottom'))
    except Exception:
        return False


def _close_dialog(page: ft.Page):
    """다이얼로그 닫기"""
    try:
        if page.dialog:
            page.dialog.open = False
            page.update()
    except Exception:
        pass
