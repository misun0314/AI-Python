import os
import sys
import streamlit.web.cli as stcli

if __name__ == '__main__':
    # Streamlit이 내부 파일들을 찾을 수 있도록 기본 경로를 설정
    script_path = os.path.join(os.path.dirname(__file__), 'app.py')
    
    # streamlit run app.py --server.port=8501 등을 명령어로 주입하는 효과
    sys.argv = ["streamlit", "run", script_path, "--global.developmentMode=false"]
    sys.exit(stcli.main())