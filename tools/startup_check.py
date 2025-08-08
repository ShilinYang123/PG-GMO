# -*- coding: utf-8 -*-

import sys
from start import OfficeAssistantStartupChecker  # 使用正确的类名
import traceback

def main():
    try:
        checker = OfficeAssistantStartupChecker()
        success, message = checker.perform_startup_check()
        print(message)
        sys.exit(0 if success else 2)
    except Exception as e:
        print(f'启动检查失败: {str(e)}')
        traceback.print_exc()
        sys.exit(2)

if __name__ == '__main__':
    main()