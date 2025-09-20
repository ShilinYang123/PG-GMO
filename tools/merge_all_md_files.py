#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PG绠＄悊鎵嬪唽 - 鎵€鏈?md鏂囦欢鍚堝苟宸ュ叿
浣滆€咃細闆ㄤ繆
鍔熻兘锛氬皢S:\\PG-GMO\\02-Output\閮ㄩ棬鍩虹寤鸿宸ヤ綔鎴愭灉鐩綍涓嬬殑鎵€鏈?md鏂囦欢鍚堝苟鎴愪竴涓畬鏁寸殑.md鏂囦欢
"""

import os
import glob
from pathlib import Path
from datetime import datetime

def read_md_file(file_path):
    """璇诲彇markdown鏂囦欢鍐呭"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception as e:
        print(f"璇诲彇鏂囦欢澶辫触: {file_path} - {e}")
        return f"# 鏂囦欢璇诲彇澶辫触\n\n鏂囦欢璺緞: {file_path}\n閿欒淇℃伅: {e}"

def create_toc_entry(title, level=1):
    """鍒涘缓鐩綍鏉＄洰"""
    indent = "  " * (level - 1)
    anchor = title.lower().replace(" ", "-").replace("閮?, "bu").replace("鍔?, "ban")
    return f"{indent}- [{title}](#{anchor})"

def merge_all_md_files():
    """鍚堝苟鎵€鏈?md鏂囦欢"""
    
    # 瀹氫箟閮ㄩ棬椤哄簭
    department_order = [
        "鎬荤粡鍔?,
        "PMC閮?, 
        "涓氬姟閮?,
        "鐮斿彂閮?,
        "鍝佽川閮?,
        "閲囪喘閮?,
        "浜旈噾閮?,
        "瑁呴厤閮?,
        "琛屾斂閮?,
        "璐㈠姟閮?
    ]
    
    # 婧愮洰褰曞拰杈撳嚭鏂囦欢
    source_dir = Path("S:/PG-GMO/02-Output/閮ㄩ棬鍩虹寤鸿宸ヤ綔鎴愭灉")
    output_file = Path("S:/PG-GMO/02-Output/PG绠＄悊鎵嬪唽_瀹屾暣鐗?md")
    
    print("=== PG绠＄悊鎵嬪唽 - 鎵€鏈?md鏂囦欢鍚堝苟宸ュ叿 ===")
    print(f"婧愮洰褰? {source_dir}")
    print(f"杈撳嚭鏂囦欢: {output_file}")
    print()
    
    # 寮€濮嬫瀯寤哄悎骞跺唴瀹?
    merged_content = []
    toc_entries = []
    
    # 娣诲姞鏂囨。澶撮儴
    current_time = datetime.now().strftime("%Y骞?m鏈?d鏃?%H:%M")
    header = f"""# PG绠＄悊鎵嬪唽 - 瀹屾暣鐗?

**鐢熸垚鏃堕棿锛?* {current_time}  
**浣滆€咃細** 闆ㄤ繆  
**鐗堟湰锛?* v1.0

---

## 鐩綍
"""
    
    merged_content.append(header)
    
    # 鎸夐儴闂ㄩ『搴忓鐞?
    total_files = 0
    processed_files = 0
    
    for dept_name in department_order:
        dept_dir = source_dir / dept_name
        
        if not dept_dir.exists():
            print(f"鈿狅笍  閮ㄩ棬鐩綍涓嶅瓨鍦? {dept_name}")
            continue
            
        print(f"馃搧 澶勭悊閮ㄩ棬: {dept_name}")
        
        # 娣诲姞閮ㄩ棬鏍囬鍒扮洰褰?
        toc_entries.append(create_toc_entry(dept_name, 1))
        
        # 鑾峰彇閮ㄩ棬涓嬬殑鎵€鏈?md鏂囦欢
        md_files = list(dept_dir.glob("*.md"))
        
        # 澶勭悊瀛愮洰褰曪紙濡侾MC閮ㄤ笅鐨勪粨鍌ㄩ儴锛?
        subdirs = [d for d in dept_dir.iterdir() if d.is_dir() and d.name != "闄勪欢"]
        
        # 鎸夋枃浠跺悕鎺掑簭
        md_files.sort(key=lambda x: x.name)
        
        if md_files:
            # 娣诲姞閮ㄩ棬绔犺妭
            dept_section = f"\n\n---\n\n# {dept_name}\n\n"
            merged_content.append(dept_section)
            
            # 澶勭悊閮ㄩ棬涓昏鏂囦欢
            for md_file in md_files:
                total_files += 1
                print(f"  馃搫 澶勭悊鏂囦欢: {md_file.name}")
                
                # 鎻愬彇绔犺妭鏍囬
                section_title = md_file.stem
                if section_title.startswith("0") and "-" in section_title:
                    section_title = section_title.split("-", 1)[1]
                
                # 娣诲姞鍒扮洰褰?
                toc_entries.append(create_toc_entry(section_title, 2))
                
                # 璇诲彇鏂囦欢鍐呭
                content = read_md_file(md_file)
                
                if content:
                    # 娣诲姞绔犺妭鏍囬鍜屽唴瀹?
                    section = f"\n## {section_title}\n\n{content}\n"
                    merged_content.append(section)
                    processed_files += 1
                else:
                    print(f"    鉂?鏂囦欢鍐呭涓虹┖: {md_file.name}")
        
        # 澶勭悊瀛愰儴闂?
        for subdir in subdirs:
            if subdir.name == "浠撳偍閮?:  # PMC閮ㄤ笅鐨勪粨鍌ㄩ儴
                print(f"  馃搧 澶勭悊瀛愰儴闂? {subdir.name}")
                toc_entries.append(create_toc_entry(f"{dept_name}-{subdir.name}", 2))
                
                # 娣诲姞瀛愰儴闂ㄧ珷鑺?
                subdept_section = f"\n\n## {dept_name}-{subdir.name}\n\n"
                merged_content.append(subdept_section)
                
                # 澶勭悊瀛愰儴闂ㄧ殑.md鏂囦欢
                sub_md_files = list(subdir.glob("*.md"))
                sub_md_files.sort(key=lambda x: x.name)
                
                for sub_md_file in sub_md_files:
                    total_files += 1
                    print(f"    馃搫 澶勭悊瀛愭枃浠? {sub_md_file.name}")
                    
                    # 鎻愬彇绔犺妭鏍囬
                    sub_section_title = sub_md_file.stem
                    if sub_section_title.startswith("0") and "-" in sub_section_title:
                        sub_section_title = sub_section_title.split("-", 1)[1]
                    
                    # 娣诲姞鍒扮洰褰?
                    toc_entries.append(create_toc_entry(sub_section_title, 3))
                    
                    # 璇诲彇鏂囦欢鍐呭
                    sub_content = read_md_file(sub_md_file)
                    
                    if sub_content:
                        # 娣诲姞瀛愮珷鑺傛爣棰樺拰鍐呭
                        sub_section = f"\n### {sub_section_title}\n\n{sub_content}\n"
                        merged_content.append(sub_section)
                        processed_files += 1
                    else:
                        print(f"      鉂?瀛愭枃浠跺唴瀹逛负绌? {sub_md_file.name}")
    
    # 鏋勫缓瀹屾暣鐨勭洰褰?
    toc_content = "\n".join(toc_entries)
    
    # 缁勮鏈€缁堝唴瀹?
    final_content = merged_content[0] + toc_content + "\n\n---\n" + "".join(merged_content[1:])
    
    # 娣诲姞鏂囨。灏鹃儴
    footer = f"\n\n---\n\n## 鏂囨。淇℃伅\n\n- **鐢熸垚鏃堕棿锛?* {current_time}\n- **鎬绘枃浠舵暟锛?* {total_files}\n- **鎴愬姛澶勭悊锛?* {processed_files}\n- **鎴愬姛鐜囷細** {processed_files/total_files*100:.1f}%\n- **鎶€鏈礋璐ｄ汉锛?* 闆ㄤ繆\n\n---\n\n*鏈枃妗ｇ敱PG绠＄悊鎵嬪唽鍚堝苟宸ュ叿鑷姩鐢熸垚*"
    
    final_content += footer
    
    # 鍐欏叆杈撳嚭鏂囦欢
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_content)
        
        print(f"\n鉁?鍚堝苟瀹屾垚锛?)
        print(f"馃搫 杈撳嚭鏂囦欢: {output_file}")
        print(f"馃搳 澶勭悊缁熻:")
        print(f"   - 鎬绘枃浠舵暟: {total_files}")
        print(f"   - 鎴愬姛澶勭悊: {processed_files}")
        print(f"   - 鎴愬姛鐜? {processed_files/total_files*100:.1f}%")
        
        return True
        
    except Exception as e:
        print(f"鉂?鍐欏叆鏂囦欢澶辫触: {e}")
        return False

def main():
    """涓诲嚱鏁?""
    try:
        success = merge_all_md_files()
        if success:
            print("\n馃帀 鎵€鏈?md鏂囦欢鍚堝苟瀹屾垚锛?)
        else:
            print("\n鉂?鍚堝苟杩囩▼涓嚭鐜伴敊璇?)
    except Exception as e:
        print(f"鉂?绋嬪簭鎵ц澶辫触: {e}")

if __name__ == "__main__":
    main()
