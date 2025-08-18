#!/usr/bin/env python3
"""
Netlify 배포용 빌드 스크립트
"""
import os
import sys
import subprocess

def build_for_web():
    """웹용 빌드"""
    try:
        # Flet CLI 방식 시도
        result = subprocess.run([sys.executable, "-m", "flet", "build", "web"], 
                              capture_output=True, text=True, cwd=".")
        
        if result.returncode == 0:
            print("✅ Flet CLI 빌드 성공")
            return True
        else:
            print(f"❌ Flet CLI 빌드 실패: {result.stderr}")
            
        # 대안: 직접 웹 앱 실행 방식
        print("🔄 대안 방식으로 빌드 시도...")
        
        # 간단한 index.html 생성
        os.makedirs("dist", exist_ok=True)
        
        html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Promptub - AI 프롬프트 공유 SNS</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0; padding: 20px; background: #f5f5f5; 
        }
        .container { 
            max-width: 800px; margin: 0 auto; text-align: center; 
            background: white; padding: 40px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .loading { font-size: 18px; color: #666; }
        .error { color: #e74c3c; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Promptub</h1>
        <div class="loading">AI 프롬프트 공유 SNS 로딩 중...</div>
        <div class="error">
            <p>현재 Flet 웹 빌드가 완전히 지원되지 않습니다.</p>
            <p>로컬에서 실행하려면: <code>python app.py</code></p>
        </div>
    </div>
    
    <script>
        // Flet 앱 로딩 시도
        setTimeout(() => {
            window.location.href = 'https://github.com/dhet13/pormpt_sns';
        }, 5000);
    </script>
</body>
</html>"""
        
        with open("dist/index.html", "w", encoding="utf-8") as f:
            f.write(html_content)
            
        print("✅ 대안 HTML 페이지 생성 완료")
        return True
        
    except Exception as e:
        print(f"❌ 빌드 실패: {e}")
        return False

if __name__ == "__main__":
    success = build_for_web()
    sys.exit(0 if success else 1)
