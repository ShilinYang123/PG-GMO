#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
閮ㄩ棬绠＄悊鎵嬪唽鎻愬彇宸ュ叿
浠庡畬鏁寸増绠＄悊鎵嬪唽涓彁鍙栨瘡涓儴闂ㄧ殑鍐呭锛岀敓鎴愮嫭绔嬬殑.md鏂囦欢

浣滆€? 闆ㄤ繆
鏃ユ湡: 2025-08-13
"""

import os
import re
from datetime import datetime

def extract_department_content():
    """浠庡畬鏁寸増鏂囦欢涓彁鍙栧悇閮ㄩ棬鍐呭"""
    
    # 鏂囦欢璺緞
    input_file = r"S:\\PG-GMO\\02-Output\PG绠＄悊鎵嬪唽_瀹屾暣鐗?md"
    output_dir = r"S:\\PG-GMO\\02-Output\閮ㄩ棬鐙珛鎵嬪唽"
    
    # 鍒涘缓杈撳嚭鐩綍
    os.makedirs(output_dir, exist_ok=True)
    
    # 閮ㄩ棬鍒楄〃锛堟寜椤哄簭锛?    departments = [
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
    
    print(f"寮€濮嬫彁鍙栭儴闂ㄥ唴瀹?..")
    print(f"杈撳叆鏂囦欢: {input_file}")
    print(f"杈撳嚭鐩綍: {output_dir}")
    print("-" * 60)
    
    try:
        # 璇诲彇瀹屾暣鏂囦欢
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 缁熻淇℃伅
        total_departments = len(departments)
        processed_count = 0
        
        for i, dept in enumerate(departments):
            print(f"姝ｅ湪澶勭悊: {dept}...")
            
            # 鏋勫缓閮ㄩ棬鏍囬妯″紡
            dept_pattern = f"# {dept}"
            
            # 鎵惧埌褰撳墠閮ㄩ棬鐨勫紑濮嬩綅缃?            dept_start = content.find(dept_pattern)
            if dept_start == -1:
                print(f"  鈿狅笍  鏈壘鍒伴儴闂? {dept}")
                continue
            
            # 鎵惧埌涓嬩竴涓儴闂ㄧ殑寮€濮嬩綅缃紙浣滀负褰撳墠閮ㄩ棬鐨勭粨鏉熶綅缃級
            if i + 1 < len(departments):
                next_dept = departments[i + 1]
                next_dept_pattern = f"# {next_dept}"
                dept_end = content.find(next_dept_pattern, dept_start + 1)
            else:
                # 鏈€鍚庝竴涓儴闂紝鎵惧埌鏂囨。淇℃伅閮ㄥ垎
                dept_end = content.find("---\n\n## 鏂囨。淇℃伅", dept_start)
                if dept_end == -1:
                    dept_end = len(content)
            
            if dept_end == -1:
                dept_end = len(content)
            
            # 鎻愬彇閮ㄩ棬鍐呭
            dept_content = content[dept_start:dept_end].strip()
            
            # 鐢熸垚閮ㄩ棬鏂囦欢澶撮儴
            file_header = f"""# {dept}绠＄悊鎵嬪唽

**鐢熸垚鏃堕棿锛?* {datetime.now().strftime('%Y骞?m鏈?d鏃?%H:%M')}
**浣滆€咃細** 闆ㄤ繆
**鐗堟湰锛?* v1.0
**鏉ユ簮锛?* PG绠＄悊鎵嬪唽瀹屾暣鐗?
---

"""
            
            # 澶勭悊鍐呭锛堢Щ闄ら儴闂ㄦ爣棰橈紝鍥犱负宸茬粡鍦ㄦ枃浠跺ご閮ㄦ坊鍔犱簡锛?            dept_content = dept_content.replace(f"# {dept}", "").strip()
            
            # 鐢熸垚瀹屾暣鍐呭
            full_content = file_header + dept_content
            
            # 娣诲姞鏂囨。灏鹃儴
            file_footer = f"""

---

## 鏂囨。淇℃伅

- **鐢熸垚鏃堕棿锛?* {datetime.now().strftime('%Y骞?m鏈?d鏃?%H:%M')}
- **閮ㄩ棬锛?* {dept}
- **鎶€鏈礋璐ｄ汉锛?* 闆ㄤ繆
- **鏂囨。鐘舵€侊細** 宸插畬鎴?"""
            
            full_content += file_footer
            
            # 淇濆瓨閮ㄩ棬鏂囦欢
            output_file = os.path.join(output_dir, f"{dept}绠＄悊鎵嬪唽.md")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(full_content)
            
            processed_count += 1
            print(f"  鉁?宸茬敓鎴? {output_file}")
            print(f"  馃搫 鍐呭闀垮害: {len(full_content):,} 瀛楃")
        
        # 杈撳嚭缁熻淇℃伅
        print("-" * 60)
        print(f"馃搳 澶勭悊缁熻:")
        print(f"  鎬婚儴闂ㄦ暟: {total_departments}")
        print(f"  鎴愬姛澶勭悊: {processed_count}")
        print(f"  鎴愬姛鐜? {processed_count/total_departments*100:.1f}%")
        print(f"  杈撳嚭鐩綍: {output_dir}")
        
        # 鐢熸垚绱㈠紩鏂囦欢
        create_index_file(output_dir, departments, processed_count)
        
        print("\n馃帀 閮ㄩ棬绠＄悊鎵嬪唽鎻愬彇瀹屾垚锛?)
        
    except Exception as e:
        print(f"鉂?澶勭悊杩囩▼涓彂鐢熼敊璇? {str(e)}")
        return False
    
    return True

def create_index_file(output_dir, departments, processed_count):
    """鍒涘缓绱㈠紩鏂囦欢"""
    
    index_content = f"""# 閮ㄩ棬绠＄悊鎵嬪唽绱㈠紩

**鐢熸垚鏃堕棿锛?* {datetime.now().strftime('%Y骞?m鏈?d鏃?%H:%M')}
**浣滆€咃細** 闆ㄤ繆
**鐗堟湰锛?* v1.0

---

## 姒傝堪

鏈洰褰曞寘鍚玃G鍏徃鍚勯儴闂ㄧ殑鐙珛绠＄悊鎵嬪唽锛屾瘡涓儴闂ㄧ殑绠＄悊鍒跺害銆佹祦绋嬭鑼冦€佸矖浣嶈亴璐ｇ瓑鍐呭宸叉彁鍙栦负鐙珛鐨?md鏂囦欢銆?
## 閮ㄩ棬鍒楄〃

"""
    
    for i, dept in enumerate(departments, 1):
        file_name = f"{dept}绠＄悊鎵嬪唽.md"
        file_path = os.path.join(output_dir, file_name)
        
        if os.path.exists(file_path):
            # 鑾峰彇鏂囦欢澶у皬
            file_size = os.path.getsize(file_path)
            size_kb = file_size / 1024
            
            index_content += f"{i}. [{dept}绠＄悊鎵嬪唽](./{file_name}) ({size_kb:.1f} KB)\n"
        else:
            index_content += f"{i}. {dept}绠＄悊鎵嬪唽 (鏈敓鎴?\n"
    
    index_content += f"""

## 缁熻淇℃伅

- **鎬婚儴闂ㄦ暟锛?* {len(departments)}
- **鎴愬姛鐢熸垚锛?* {processed_count}
- **鎴愬姛鐜囷細** {processed_count/len(departments)*100:.1f}%
- **鐢熸垚鏃堕棿锛?* {datetime.now().strftime('%Y骞?m鏈?d鏃?%H:%M')}

## 浣跨敤璇存槑

1. 姣忎釜閮ㄩ棬鐨勭鐞嗘墜鍐岄兘鏄嫭绔嬬殑.md鏂囦欢
2. 鏂囦欢鍐呭鍖呮嫭閮ㄩ棬鏋舵瀯銆佽亴璐ｅ垎宸ャ€佺鐞嗗埗搴︺€佷綔涓氭祦绋嬬瓑
3. 鎵€鏈夋枃浠堕噰鐢║TF-8缂栫爜锛屽彲鐢ㄤ换浣曟敮鎸丮arkdown鐨勭紪杈戝櫒鎵撳紑
4. 寤鸿浣跨敤涓撲笟鐨凪arkdown缂栬緫鍣ㄦ煡鐪嬶紝浠ヨ幏寰楁渶浣抽槄璇讳綋楠?
---

**鎶€鏈礋璐ｄ汉锛?* 闆ㄤ繆  
**椤圭洰锛?* PG绠＄悊鎵嬪唽鏁板瓧鍖? 
**鐗堟湰锛?* v1.0
"""
    
    # 淇濆瓨绱㈠紩鏂囦欢
    index_file = os.path.join(output_dir, "README.md")
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"  馃搵 宸茬敓鎴愮储寮曟枃浠? {index_file}")

if __name__ == "__main__":
    print("=" * 60)
    print("PG绠＄悊鎵嬪唽 - 閮ㄩ棬鍐呭鎻愬彇宸ュ叿")
    print("=" * 60)
    
    success = extract_department_content()
    
    if success:
        print("\n鉁?鎵€鏈変换鍔″凡瀹屾垚")
    else:
        print("\n鉂?浠诲姟鎵ц澶辫触")
