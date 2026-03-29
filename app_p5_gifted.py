import streamlit as st
import streamlit.components.v1 as components
import random
import math
import zipfile
import io
import time
import itertools

# ==========================================
# ⚙️ ตรวจสอบไลบรารี pdfkit
# ==========================================
try:
    import pdfkit
    HAS_PDFKIT = True
except ImportError:
    HAS_PDFKIT = False

# ==========================================
# 🎨 ตั้งค่าหน้าเพจ Web App & Professional CSS (ธีม ป.5 โทนส้ม-แดง ท้าทายขึ้น)
# ==========================================
st.set_page_config(page_title="Math Generator - Primary 5 (Gifted)", page_icon="🏆", layout="wide")

st.markdown("""
<style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1200px; }
    div[data-testid="stSidebar"] div.stButton > button { background-color: #d35400; color: white; border-radius: 8px; height: 3.5rem; font-size: 18px; font-weight: bold; border: none; box-shadow: 0 4px 6px rgba(211,84,0,0.3); }
    div[data-testid="stSidebar"] div.stButton > button:hover { background-color: #e67e22; box-shadow: 0 6px 12px rgba(211,84,0,0.4); }
    .main-header { background: linear-gradient(135deg, #c0392b, #e67e22); padding: 2rem; border-radius: 15px; color: white; margin-bottom: 2rem; box-shadow: 0 10px 20px rgba(0,0,0,0.15); }
    .main-header h1 { margin: 0; font-size: 2.8rem; font-weight: 800; text-shadow: 2px 2px 4px rgba(0,0,0,0.2); }
    .main-header p { margin: 10px 0 0 0; font-size: 1.2rem; opacity: 0.9; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🏆 Math Worksheet Pro <span style="font-size: 20px; background: #f1c40f; color: #333; padding: 5px 15px; border-radius: 20px; vertical-align: middle;">ป.5 & เตรียมสอบเข้า ม.1</span></h1>
    <p>ระบบสร้างโจทย์คณิตศาสตร์ประยุกต์ สถิติ และเรขาคณิตขั้นสูง</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 📚 ฐานข้อมูลหลักสูตร (Master Database ป.5 - ฉบับสมบูรณ์ ลำดับการเรียนรู้เพื่อสอบแข่งขัน)
# ==========================================
curriculum_db = {
    "ป.5": {
        "บทที่ 1: รากฐานตัวเลขและการดำเนินการ": [
            "การบวก ลบ คูณ หารระคน (กฎ PEMDAS)",
            "จำนวนเต็มลบเบื้องต้น", # ✨ เพิ่มใหม่
            "เทคนิคคิดเลขเร็วและสมบัติการแจกแจง",
            "ทฤษฎีจำนวน (จำนวนเฉพาะ, ตัวประกอบ, สมบัติการหารลงตัว)",
            "ระบบเลขฐานต่างๆ เบื้องต้น", # ✨ เพิ่มใหม่ (ฐาน 2, ฐาน 5, ฯลฯ)
            "โจทย์ปัญหา ห.ร.ม. และ ค.ร.น. (แบ่งของ, นาฬิกาปลุก)",
            "เลขยกกำลังเบื้องต้นและการหาเลขโดดหลักหน่วย"
        ],
        "บทที่ 2: โลกของเศษส่วนและทศนิยม": [
            "การบวกและการลบเศษส่วน", 
            "การคูณและการหารเศษส่วน",
            "การบวก ลบ คูณ หารระคน (เศษส่วน)",
            "เศษส่วนซ้อน (Complex Fractions)", # ✨ เพิ่มใหม่
            "โจทย์ปัญหาเศษส่วน และโจทย์ปัญหาเศษส่วนต่อเนื่อง (ของที่เหลือ)",
            "ทศนิยมซ้ำและการแปลงเป็นเศษส่วน", # ✨ เพิ่มใหม่
            "การบวกและการลบทศนิยม", 
            "การคูณและการหารทศนิยม",
            "โจทย์ปัญหาทศนิยม"
        ],
        "บทที่ 3: สัดส่วนและร้อยละในชีวิตจริง": [
            "ความสัมพันธ์ของ เศษส่วน ทศนิยม และร้อยละ",
            "อัตราส่วนเบื้องต้นและอัตราส่วนที่เท่ากัน",
            "โจทย์ปัญหาอัตราส่วน และโจทย์ปัญหาของผสม", # ✨ อัปเกรด (ของผสม)
            "โจทย์ปัญหาบัญญัติไตรยางศ์ (Unitary Method)",
            "การเขียนเศษส่วนในรูปร้อยละ",
            "โจทย์ปัญหาร้อยละ (กำไร ขาดทุน ลดราคา)",
            "ดอกเบี้ยเงินฝากและภาษีเบื้องต้น"
        ],
        "บทที่ 4: พีชคณิตและสมการปราบเซียน": [
            "แบบรูปและอนุกรม (Number Patterns)",
            "โอเปอเรชันและเครื่องหมายสมมติ (Operation)",
            "การแก้สมการเชิงเส้นตัวแปรเดียว",
            "การสร้างสมการจากโจทย์ปัญหา",
            "โจทย์ปัญหาคลาสสิก (นับขาสัตว์, เหรียญ)",
            "โจทย์ปัญหาอายุ และ การทำงานร่วมกัน"
        ],
        "บทที่ 5: มิติสัมพันธ์และเรขาคณิต": [
            "การแปลงหน่วยวัด (ความยาว พื้นที่ ปริมาตร)",
            "มาตราส่วนและทิศทาง",
            "เส้นขนาน มุมแย้ง และมุมภายใน",
            "มุมภายในรูปหลายเหลี่ยม",
            "สมบัติและพื้นที่รูปสามเหลี่ยม",
            "สมบัติและพื้นที่รูปสี่เหลี่ยม (คางหมู, ว่าว, ด้านขนาน, เปียกปูน)",
            "วงกลม (ส่วนประกอบ, เส้นรอบวง, พื้นที่)",
            "ทฤษฎีบทพีทาโกรัสเบื้องต้น", # ✨ เพิ่มใหม่ (ตัวช่วยหาความยาวด้าน)
            "โจทย์ปัญหาพื้นที่และความยาวรอบรูปประยุกต์",
            "เรขาคณิตประยุกต์ (หาพื้นที่แรเงาเชิงซ้อน)",
            "ลักษณะและรูปคลี่ของเรขาคณิต 3 มิติ",
            "ปริมาตรและความจุทรงสี่เหลี่ยมมุมฉาก"
        ],
        "บทที่ 6: สถิติ ความน่าจะเป็น และตรรกะขั้นสูง": [
            "การอ่านแผนภูมิแท่ง แผนภูมิวงกลม และกราฟเส้น",
            "การหาค่าเฉลี่ย (Average)", 
            "เซตและแผนภาพเวนน์-ออยเลอร์ (Venn Diagram)",
            "หลักการนับเบื้องต้น (การแข่งขันพบกันหมด, จัดชุดเสื้อผ้า)",
            "ความน่าจะเป็นเบื้องต้น (สุ่มหยิบของ)",
            "อัตราเร็ว ระยะทาง และเวลา (รถไฟข้ามสะพาน, กระแสน้ำ)",
            "มุมระหว่างเข็มนาฬิกา (Clock Angles)",
            "ปริศนาตัวเลขซ่อนตัว (Cryptarithm)" # ✨ เพิ่มใหม่ (ตรรกะเชาวน์ปัญญา)
        ]
    }
}
# ==========================================
# 1. คลังคำศัพท์และฟังก์ชันตัวช่วย (Helpers)
# ==========================================
NAMES = ["อคิณ", "นาวิน", "ภูผา", "สายฟ้า", "เจ้านาย", "ข้าวหอม", "ใบบัว", "มะลิ", "น้ำใส", "ญาญ่า", "ปลื้ม", "พายุ", "ธาม", "คิน", "พริม"]
PLACE_EMOJIS = {"บ้าน": "🏠", "โรงเรียน": "🏫", "ตลาด": "🛒", "วัด": "🛕", "สวนสาธารณะ": "🌳", "โรงพยาบาล": "🏥"}

def f_html(n, d, c="#2c3e50", b=True):
    w = "bold" if b else "normal"
    return f"<span style='display:inline-flex; flex-direction:column; vertical-align:middle; text-align:center; line-height:1.4; margin:0 4px;'><span style='border-bottom:2px solid {c}; padding:0 4px; font-weight:{w}; color:{c};'>{n}</span><span style='padding:0 4px; font-weight:{w}; color:{c};'>{d}</span></span>"

def generate_vertical_table_html(a, b, op, result="", is_key=False):
    a_str, b_str = f"{a:,}", f"{b:,}"
    ans_val = f"{result:,}" if is_key and result != "" else ""
    border_ans = "border-bottom: 4px double #000;" if is_key else ""
    return f"""<div style='margin-left: 60px; display: block; font-family: "Sarabun", sans-serif; font-size: 26px; margin-top: 15px; margin-bottom: 15px;'>
        <table style='border-collapse: collapse; text-align: right;'>
            <tr><td style='padding: 0 10px 0 0; border: none;'>{a_str}</td><td rowspan='2' style='vertical-align: middle; text-align: left; padding: 0 0 0 15px; font-size: 28px; font-weight: bold; border: none;'>{op}</td></tr>
            <tr><td style='padding: 5px 10px 5px 0; border: none; border-bottom: 2px solid #000;'>{b_str}</td></tr>
            <tr><td style='padding: 5px 10px 0 0; border: none; {border_ans} height: 35px;'>{ans_val}</td><td style='border: none;'></td></tr>
        </table></div>"""

def generate_decimal_vertical_html(a, b, op, is_key=False):
    str_a, str_b = f"{a:.2f}", f"{b:.2f}"
    ans = a + b if op == '+' else round(a - b, 2)
    str_ans = f"{ans:.2f}"
    max_len = max(len(str_a), len(str_b), len(str_ans)) + 1 
    str_a, str_b, str_ans = str_a.rjust(max_len, " "), str_b.rjust(max_len, " "), str_ans.rjust(max_len, " ")
    strike, top_marks = [False] * max_len, [""] * max_len
    
    if is_key:
        if op == '+':
            carry = 0
            for i in range(max_len - 1, -1, -1):
                if str_a[i] == '.': continue
                da = int(str_a[i]) if str_a[i].strip() else 0
                db = int(str_b[i]) if str_b[i].strip() else 0
                s = da + db + carry
                carry = s // 10
                if carry > 0 and i > 0:
                    next_i = i - 1
                    if str_a[next_i] == '.': next_i -= 1
                    if next_i >= 0: top_marks[next_i] = str(carry)
        elif op == '-':
            a_digits = [int(c) if c.strip() and c != '.' else 0 for c in list(str_a)]
            b_digits = [int(c) if c.strip() and c != '.' else 0 for c in list(str_b)]
            for i in range(max_len - 1, -1, -1):
                if str_a[i] == '.': continue
                if a_digits[i] < b_digits[i]:
                    for j in range(i-1, -1, -1):
                        if str_a[j] == '.': continue
                        if a_digits[j] > 0 and str_a[j].strip() != "":
                            strike[j] = True
                            a_digits[j] -= 1
                            top_marks[j] = str(a_digits[j])
                            for k in range(j+1, i):
                                if str_a[k] == '.': continue
                                strike[k] = True
                                a_digits[k] = 9
                                top_marks[k] = "9"
                            strike[i] = True
                            a_digits[i] += 10
                            top_marks[i] = str(a_digits[i])
                            break
                            
    a_tds = ""
    for i in range(max_len):
        val = str_a[i].strip() if str_a[i].strip() else ""
        if str_a[i] == '.': val = "."
        td_content = val
        if val and val != '.':
            mark = top_marks[i]
            if strike[i] and is_key: td_content = f'<div style="position: relative;"><span style="position: absolute; top: -25px; left: 50%; transform: translateX(-50%); font-size: 20px; color: red; font-weight: bold;">{mark}</span><span style="text-decoration: line-through; text-decoration-color: red; text-decoration-thickness: 2px;">{val}</span></div>'
            elif mark and is_key: td_content = f'<div style="position: relative;"><span style="position: absolute; top: -25px; left: 50%; transform: translateX(-50%); font-size: 20px; color: red; font-weight: bold;">{mark}</span><span>{val}</span></div>'
        a_tds += f"<td style='width: 35px; text-align: center; height: 50px; vertical-align: bottom;'>{td_content}</td>"
        
    b_tds = "".join([f"<td style='width: 35px; text-align: center; border-bottom: 2px solid #000; height: 40px; vertical-align: bottom;'>{c.strip() if c.strip() else ('.' if c=='.' else '')}</td>" for c in str_b])
    ans_tds = "".join([f"<td style='width: 35px; text-align: center; color: red; font-weight: bold; height: 45px; vertical-align: bottom;'>{c.strip() if c.strip() else ('.' if c=='.' else '')}</td>" for c in str_ans]) if is_key else "".join([f"<td style='width: 35px; height: 45px;'></td>" for _ in str_ans])
    return f"""<div style="display: block; margin-left: 60px; margin-top: 15px; margin-bottom: 15px;"><div style="display: inline-block; font-family: 'Sarabun', sans-serif; font-size: 32px; line-height: 1.2;"><table style="border-collapse: collapse;"><tr><td style="width: 20px;"></td>{a_tds}<td style="width: 50px; text-align: left; padding-left: 15px; vertical-align: middle;" rowspan="2">{op}</td></tr><tr><td></td>{b_tds}</tr><tr><td></td>{ans_tds}<td></td></tr><tr><td></td><td colspan="{max_len}" style="border-bottom: 6px double #000; height: 10px;"></td><td></td></tr></table></div></div>"""

def render_short_div(nums, mode="gcd"):
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    steps, current_nums, divisors = [], list(nums), []
    while True:
        found = False
        for p in primes:
            if all(n % p == 0 for n in current_nums):
                divisors.append(p); steps.append(list(current_nums))
                current_nums = [n // p for n in current_nums]; found = True; break
        if not found: break
    if mode == "lcm":
        while True:
            found = False
            for p in primes:
                if sum(1 for n in current_nums if n % p == 0) >= 2:
                    divisors.append(p); steps.append(list(current_nums))
                    current_nums = [n // p if n % p == 0 else n for n in current_nums]; found = True; break
            if not found: break
    html = "<div style='display:block; text-align:center; margin: 20px 0;'><div style='display:inline-block; text-align:left; font-family:\"Courier New\", Courier, monospace; font-size:20px; background:#f8f9fa; padding:15px 25px; border-radius:8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); border: 1px solid #e0e0e0;'>"
    for i in range(len(divisors)):
        html += f"<div style='display: flex; align-items: baseline;'><div style='width: 35px; text-align: right; color: #c0392b; font-weight: bold; padding-right: 12px;'>{divisors[i]}</div><div style='border-left: 2px solid #2c3e50; border-bottom: 2px solid #2c3e50; padding: 4px 15px; display: flex; gap: 20px;'>"
        for n in steps[i]: html += f"<div style='width: 40px; text-align: center; color: #333;'>{n}</div>"
        html += "</div></div>"
    html += f"<div style='display: flex; align-items: baseline;'><div style='width: 35px; text-align: right; padding-right: 12px;'></div><div style='padding: 6px 15px 0px 15px; display: flex; gap: 20px; color: #2980b9; font-weight: bold; border-bottom: 4px double #2980b9;'>"
    for n in current_nums: html += f"<div style='width: 40px; text-align: center;'>{n}</div>"
    html += "</div></div></div></div>"
    return html, divisors, current_nums

# ==========================================
# 2. ฟังก์ชันวาด SVG สำหรับ ป.5
# ==========================================

# 2.1 ปริมาตรและความจุทรงลูกบาศก์/ทรงสี่เหลี่ยมมุมฉาก
def draw_prism_svg(w_lbl, l_lbl, h_lbl, is_water=False):
    svg = '<div style="text-align:center; margin:15px 0;"><svg width="280" height="220">'
    fill_front, fill_top, fill_right = ("#aed6f1", "#85c1e9", "#5dade2") if is_water else ("#d5f5e3", "#abebc6", "#82e0aa")
    stroke_c = "#2874a6" if is_water else "#27ae60"
    
    if is_water:
        y_offset = 60 
        svg += '<line x1="80" y1="10" x2="80" y2="130" stroke="#bdc3c7" stroke-width="2"/>'
        svg += '<line x1="80" y1="130" x2="220" y2="130" stroke="#bdc3c7" stroke-width="2"/>'
        svg += '<line x1="40" y1="160" x2="80" y2="130" stroke="#bdc3c7" stroke-width="2"/>'
        # ระดับน้ำ
        svg += f'<polygon points="40,{30+y_offset} 80,{10+y_offset} 220,{10+y_offset} 180,{30+y_offset}" fill="{fill_top}" stroke="{stroke_c}" stroke-width="2" opacity="0.85"/>'
        svg += f'<rect x="40" y="{30+y_offset}" width="140" height="{130-y_offset}" fill="{fill_front}" stroke="{stroke_c}" stroke-width="2" opacity="0.85"/>'
        svg += f'<polygon points="180,{30+y_offset} 220,{10+y_offset} 220,130 180,160" fill="{fill_right}" stroke="{stroke_c}" stroke-width="2" opacity="0.85"/>'
        # โครงกระจก
        svg += '<polygon points="40,30 80,10 220,10 180,30" fill="none" stroke="#95a5a6" stroke-width="2"/>'
        svg += '<line x1="40" y1="30" x2="40" y2="160" stroke="#95a5a6" stroke-width="2"/>'
        svg += '<line x1="180" y1="30" x2="180" y2="160" stroke="#95a5a6" stroke-width="2"/>'
        svg += '<line x1="220" y1="10" x2="220" y2="130" stroke="#95a5a6" stroke-width="2"/>'
        svg += '<line x1="40" y1="160" x2="180" y2="160" stroke="#95a5a6" stroke-width="2"/>'
    else:
        # กล่องทึบ
        svg += f'<rect x="40" y="60" width="140" height="100" fill="{fill_front}" stroke="{stroke_c}" stroke-width="3"/>'
        svg += f'<polygon points="40,60 80,20 220,20 180,60" fill="{fill_top}" stroke="{stroke_c}" stroke-width="3"/>'
        svg += f'<polygon points="180,60 220,20 220,120 180,160" fill="{fill_right}" stroke="{stroke_c}" stroke-width="3"/>'
        
    svg += f'<text x="110" y="185" font-family="Sarabun" font-size="16" fill="#2c3e50" font-weight="bold" text-anchor="middle">{l_lbl}</text>'
    svg += f'<text x="210" y="150" font-family="Sarabun" font-size="16" fill="#2c3e50" font-weight="bold">{w_lbl}</text>'
    
    if is_water: 
        svg += f'<text x="5" y="{95+y_offset/2}" font-family="Sarabun" font-size="16" fill="#2980b9" font-weight="bold">{h_lbl}</text>'
    else: 
        svg += f'<text x="5" y="115" font-family="Sarabun" font-size="16" fill="#2c3e50" font-weight="bold">{h_lbl}</text>'
    
    return svg + '</svg></div>'

# 2.2 กล่องลูกแก้ว ความน่าจะเป็น
def draw_marbles_box_svg(color_counts):
    color_map = {"สีแดง": "#e74c3c", "สีฟ้า": "#3498db", "สีเขียว": "#2ecc71", "สีเหลือง": "#f1c40f", "สีดำ": "#2c3e50", "สีขาว": "#fdfefe"}
    total_marbles = sum(color_counts.values())
    cols = 10 if total_marbles > 20 else 8
    rows = (total_marbles + cols - 1) // cols
    marble_r, col_w, row_h = 12, 36, 36
    box_width, box_height = max(320, cols * col_w + 30), max(140, rows * row_h + 60)
    width, height = box_width + 100, box_height + 40
    svg = f'<div style="text-align:center; margin: 15px 0;"><svg width="{width}" height="{height}">'
    box_x, box_y = 50, 20
    
    # วาดกล่องทึบ
    svg += f'<rect x="{box_x}" y="{box_y}" width="{box_width}" height="{box_height}" fill="#ebedef" stroke="#7f8c8d" stroke-width="4" rx="10"/>'
    svg += f'<path d="M {box_x} {box_y + 35} L {box_x + box_width} {box_y + 35}" stroke="#bdc3c7" stroke-width="2" stroke-dasharray="5,5"/>'
    svg += f'<text x="{box_x + box_width/2}" y="{box_y + 25}" font-family="Sarabun" font-size="16" font-weight="bold" fill="#34495e" text-anchor="middle">กล่องทึบ (มองไม่เห็นด้านใน)</text>'
    
    marbles = []
    for c_name, count in color_counts.items():
        for _ in range(count): marbles.append(color_map[c_name])
    random.shuffle(marbles)
    
    start_x, start_y = box_x + 25 + marble_r, box_y + 35 + 15 + marble_r
    for i, color in enumerate(marbles):
        cx, cy = start_x + ((i % cols) * col_w), start_y + ((i // cols) * row_h)
        svg += f'<circle cx="{cx}" cy="{cy}" r="{marble_r}" fill="{color}" stroke="#34495e" stroke-width="2"/>'
        svg += f'<circle cx="{cx-3}" cy="{cy-3}" r="3" fill="#ffffff" opacity="0.4"/>'
    return svg + '</svg></div>'

# 2.3 กล่องแสดงค่าเฉลี่ย
def draw_avg_box(icon, count, label_count, avg_val, label_avg, bg_color="#f1f8ff", border_color="#3498db"):
    box_style = f"border: 2px dashed {border_color}; border-radius: 8px; padding: 10px 15px; display: inline-block; text-align: center; margin: 5px; background-color: {bg_color}; vertical-align: top; min-width: 140px;"
    return f'<div style="{box_style}"><div style="font-size:24px;">{icon} {count} {label_count}</div><div style="font-size: 14px; font-weight: bold; color: #7f8c8d; margin-top: 5px;">ค่าเฉลี่ย</div><div style="font-size: 20px; font-weight: bold; color: #e74c3c;">{avg_val} {label_avg}</div></div>'

# 2.4 วาดเส้นขนาน และมุมแย้ง
def draw_angle_feature(vx, vy, ax, ay, bx, by, r_arc, r_text, label, color_arc, color_text, is_x=False):
    len_a = math.hypot(ax - vx, ay - vy)
    len_b = math.hypot(bx - vx, by - vy)
    if len_a == 0 or len_b == 0: return ""
    sx, sy = vx + (ax - vx) * r_arc / len_a, vy + (ay - vy) * r_arc / len_a
    ex, ey = vx + (bx - vx) * r_arc / len_b, vy + (by - vy) * r_arc / len_b
    sweep = 1 if (sx - vx) * (ey - vy) - (sy - vy) * (ex - vx) > 0 else 0
    arc_svg = f'<path d="M {sx} {sy} A {r_arc} {r_arc} 0 0 {sweep} {ex} {ey}" fill="none" stroke="{color_arc}" stroke-width="3"/>'
    mid_x, mid_y = (sx - vx)/r_arc + (ex - vx)/r_arc, (sy - vy)/r_arc + (ey - vy)/r_arc
    len_mid = math.hypot(mid_x, mid_y)
    tx, ty = (vx, vy - r_text) if len_mid == 0 else (vx + (mid_x / len_mid) * r_text, vy + (mid_y / len_mid) * r_text)
    font_size = "18px" if is_x else "16px"
    return arc_svg + f'<text x="{tx}" y="{ty+6}" font-size="{font_size}" font-weight="bold" font-family="Sarabun" text-anchor="middle" fill="{color_text}">{label}</text>'

def draw_parallel_svg(dir_key, pos1, val1, pos2, val2):
    angle_meta = {
        "dir1": {"bot": (110, 165), "top": (210, 15), "V1": (180, 60), "V2": (140, 120), "acute": ["TR_ext", "BL_int", "TL_int", "BR_ext"]},
        "dir2": {"bot": (220, 165), "top": (120, 15), "V1": (150, 60), "V2": (190, 120), "acute": ["TL_ext", "BR_int", "TR_int", "BL_ext"]}
    }
    def get_arms(pos, V1, V2, bot, top):
        if pos == "TL_ext": return V1, top, (40, V1[1])
        if pos == "TR_ext": return V1, (300, V1[1]), top
        if pos == "BL_int": return V1, (40, V1[1]), V2
        if pos == "BR_int": return V1, V2, (300, V1[1])
        if pos == "TL_int": return V2, V1, (40, V2[1])
        if pos == "TR_int": return V2, (300, V2[1]), V1
        if pos == "BL_ext": return V2, (40, V2[1]), bot
        if pos == "BR_ext": return V2, bot, (300, V2[1])

    svg = '<div style="text-align:center; margin:15px 0;"><svg width="340" height="200">'
    # เส้นขนาน 2 เส้น
    svg += '<line x1="40" y1="60" x2="300" y2="60" stroke="#2980b9" stroke-width="4"/><line x1="40" y1="120" x2="300" y2="120" stroke="#2980b9" stroke-width="4"/>'
    # สัญลักษณ์ลูกศรขนาน
    svg += '<polygon points="275,55 285,60 275,65" fill="#2980b9"/><polygon points="275,115 285,120 275,125" fill="#2980b9"/>'
    
    lbl_style = 'font-family:Sarabun; font-size:16px; font-weight:bold; fill:#2c3e50;'
    meta = angle_meta[dir_key]
    bot, top = meta["bot"], meta["top"]
    # เส้นตัด
    svg += f'<line x1="{bot[0]}" y1="{bot[1]}" x2="{top[0]}" y2="{top[1]}" stroke="#8e44ad" stroke-width="3"/>'
    
    V1, V2 = meta["V1"], meta["V2"]
    def draw_pos(pos, val, is_var):
        vx, arm1, arm2 = get_arms(pos, V1, V2, bot, top)
        return draw_angle_feature(vx[0], vx[1], arm1[0], arm1[1], arm2[0], arm2[1], 25, 45, "x" if is_var else f"{val}°", "#2ecc71", "#c0392b", is_x=is_var)
    
    svg += draw_pos(pos1, val1, is_var=False) + draw_pos(pos2, val2, is_var=True)
    return svg + '</svg></div>'

# 2.5 วาดพื้นที่แรเงาซ้อนทับ (Gifted)
def draw_shaded_svg(scenario, W, H, p1=0):
    svg = '<div style="text-align:center; margin:15px 0;"><svg width="460" height="240">'
    max_w, max_h = 200, 140 
    scale = min(max_w / W, max_h / H)
    draw_w, draw_h = W * scale, H * scale
    ox, oy = (460 - draw_w) / 2, (240 - draw_h) / 2
    lbl_style = 'font-family:Sarabun; font-size:16px; font-weight:bold; fill:#c0392b;'
    lbl_style_sm = 'font-family:Sarabun; font-size:15px; font-weight:bold; fill:#2980b9;'
    
    if scenario == "frame":
        border_scale = p1 * scale
        svg += f'<rect x="{ox}" y="{oy}" width="{draw_w}" height="{draw_h}" fill="#bdc3c7" stroke="#2c3e50" stroke-width="3"/>'
        svg += f'<rect x="{ox+border_scale}" y="{oy+border_scale}" width="{draw_w-2*border_scale}" height="{draw_h-2*border_scale}" fill="#ffffff" stroke="#2c3e50" stroke-width="2"/>'
        svg += f'<text x="{ox + draw_w/2}" y="{oy - 10}" {lbl_style} text-anchor="middle">{W} ม.</text>'
        svg += f'<text x="{ox - 15}" y="{oy + draw_h/2 + 5}" {lbl_style} text-anchor="end">{H} ม.</text>'
        svg += f'<text x="{ox + draw_w/2}" y="{oy + border_scale/2 + 5}" {lbl_style_sm} text-anchor="middle">กว้าง {p1} ม.</text>'
        
    elif scenario == "cross_path":
        p_scale = p1 * scale
        svg += f'<rect x="{ox}" y="{oy}" width="{draw_w}" height="{draw_h}" fill="#ffffff" stroke="none"/>'
        svg += f'<rect x="{ox}" y="{oy + (draw_h - p_scale)/2}" width="{draw_w}" height="{p_scale}" fill="#bdc3c7" stroke="none"/>'
        svg += f'<rect x="{ox + (draw_w - p_scale)/2}" y="{oy}" width="{p_scale}" height="{draw_h}" fill="#bdc3c7" stroke="none"/>'
        svg += f'<rect x="{ox}" y="{oy}" width="{draw_w}" height="{draw_h}" fill="none" stroke="#2c3e50" stroke-width="3"/>'
        svg += f'<text x="{ox + draw_w/2}" y="{oy + draw_h + 20}" {lbl_style} text-anchor="middle">{W} ม.</text>'
        svg += f'<text x="{ox - 15}" y="{oy + draw_h/2 + 5}" {lbl_style} text-anchor="end">{H} ม.</text>'
        svg += f'<text x="{ox + draw_w + 15}" y="{oy + draw_h/2 + 5}" {lbl_style_sm} text-anchor="start">ทางกว้าง {p1} ม.</text>'
        
    elif scenario == "triangle_in_rect":
        svg += f'<rect x="{ox}" y="{oy}" width="{draw_w}" height="{draw_h}" fill="#bdc3c7" stroke="#2c3e50" stroke-width="3"/>'
        svg += f'<polygon points="{ox},{oy+draw_h} {ox+draw_w},{oy+draw_h} {ox+draw_w/2},{oy}" fill="#ffffff" stroke="#2c3e50" stroke-width="2"/>'
        svg += f'<text x="{ox + draw_w/2}" y="{oy + draw_h + 25}" {lbl_style} text-anchor="middle">{W} ซม.</text>'
        svg += f'<text x="{ox - 15}" y="{oy + draw_h/2 + 5}" {lbl_style} text-anchor="end">{H} ซม.</text>'
        
    return svg + '</svg></div>'

# ==========================================
# ฟังก์ชันตัวช่วยสำหรับการตั้งหารยาวทศนิยม (ป.5)
# ==========================================
def get_decimal_long_div_html(divisor, dividend_str, max_dp=3):
    div_chars, ans_chars, steps, curr_val, i, dp_count = list(dividend_str), [], [], 0, 0, 0
    while True:
        if i < len(div_chars): char = div_chars[i]
        else:
            if '.' not in div_chars:
                div_chars.append('.'); ans_chars.append('.'); i += 1
                continue
            char = '0'; div_chars.append('0')
        if char == '.':
            if '.' not in ans_chars: ans_chars.append('.')
            i += 1; continue
        curr_val = curr_val * 10 + int(char)
        q = curr_val // divisor
        ans_chars.append(str(q))
        mul = q * divisor
        rem = curr_val - mul
        if q > 0 or i >= len(dividend_str) - 1:
            steps.append({'col': i, 'curr': curr_val, 'mul': mul, 'rem': rem})
        curr_val = rem
        if '.' in ans_chars: dp_count = len(ans_chars) - ans_chars.index('.') - 1
        i += 1
        if i >= len(dividend_str) and curr_val == 0: break
        if dp_count >= max_dp: break
    first_nonzero = False
    for j in range(len(ans_chars)):
        if ans_chars[j] == '.':
            if not first_nonzero and j > 0: ans_chars[j-1] = '0'
            break
        if ans_chars[j] != '0': first_nonzero = True
        elif not first_nonzero: ans_chars[j] = ''
    
    html = "<div style='margin: 15px 40px; font-family: \"Sarabun\", sans-serif; font-size: 24px;'><table style='border-collapse: collapse; text-align: center;'>"
    html += "<tr><td style='border: none;'></td>"
    for c in ans_chars: html += f"<td style='padding: 2px 10px; color: #c0392b; font-weight: bold;'>{c}</td>"
    html += "<td style='border: none;'></td></tr>" 
    html += f"<tr><td style='padding: 2px 15px; font-weight: bold; text-align: right;'>{divisor}</td>"
    for j, c in enumerate(div_chars):
        html += f"<td style='border-top: 2px solid #333; {'border-left: 2px solid #333;' if j == 0 else ''} padding: 2px 10px; font-weight: bold;'>{c}</td>"
    html += "<td style='border: none;'></td></tr>"
    for idx, step in enumerate(steps):
        if step['mul'] == 0 and step['curr'] == 0 and idx != len(steps)-1: continue
        if idx > 0:
            html += "<tr><td style='border: none;'></td>"
            cv_str, cols, c_ptr = str(step['curr']), [], step['col']
            while len(cols) < len(cv_str):
                if div_chars[c_ptr] != '.': cols.append(c_ptr)
                c_ptr -= 1
            cols.reverse()
            for j in range(len(div_chars) + 1):
                html += f"<td style='padding: 2px 10px;'>{cv_str[cols.index(j)]}</td>" if j in cols else "<td style='border: none;'></td>"
            html += "</tr>"
        html += "<tr><td style='border: none;'></td>"
        mul_str, cols, c_ptr = str(step['mul']), [], step['col']
        while len(cols) < len(mul_str):
            if div_chars[c_ptr] != '.': cols.append(c_ptr)
            c_ptr -= 1
        cols.reverse()
        for j in range(len(div_chars) + 1):
            if j in cols: html += f"<td style='border-bottom: 2px solid #333; padding: 2px 10px;'>{mul_str[cols.index(j)]}</td>"
            elif len(cols) > 0 and j == cols[-1] + 1: html += "<td style='padding: 2px 10px; font-weight: bold; color: #e74c3c;'>-</td>"
            else: html += "<td style='border: none;'></td>"
        html += "</tr>"
    if len(steps) > 0:
        html += "<tr><td style='border: none;'></td>"
        rem_str, cols, c_ptr = str(steps[-1]['rem']), [], steps[-1]['col']
        while len(cols) < len(rem_str):
            if div_chars[c_ptr] != '.': cols.append(c_ptr)
            c_ptr -= 1
        cols.reverse()
        for j in range(len(div_chars) + 1):
            html += f"<td style='border-bottom: 4px double #333; padding: 2px 10px;'>{rem_str[cols.index(j)]}</td>" if j in cols else "<td style='border: none;'></td>"
        html += "</tr>"
    html += "</table></div>"
    return html

def draw_frac(n, d):
    return f"<span style='display:inline-flex; flex-direction:column; vertical-align:middle; text-align:center; margin:0 4px; font-weight:bold; font-size:18px;'><span style='border-bottom:2px solid #2c3e50; padding:0 4px;'>{n}</span><span style='padding:0 4px;'>{d}</span></span>"

# ==========================================
# 3. Logic & Dynamic Difficulty Scaling (ป.5)
# ==========================================
def generate_questions_logic(grade, main_t, sub_t, num_q, is_challenge=False):
    questions, seen = [], set()
    
    for _ in range(num_q):
        q, sol, attempts = "", "", 0
        
        while attempts < 300:
            actual_sub_t = sub_t
            if sub_t == "แบบทดสอบรวมปลายภาค":
                rand_main = random.choice(list(curriculum_db[grade].keys()))
                actual_sub_t = random.choice(curriculum_db[grade][rand_main])




            # ================= หมวดที่ 1: รากฐานตัวเลขและการดำเนินการ (ป.5) =================
            elif actual_sub_t == "การบวก ลบ คูณ หารระคน (กฎ PEMDAS)":
                # สุ่มรูปแบบโจทย์ 4 สไตล์ เพื่อความหลากหลายสุดขีด
                scenario = random.choice(["theme_park", "savings", "library", "pure_math_v2"])

                if scenario == "theme_park":
                    # สไตล์ที่ 1: การไปเที่ยวและแชร์ค่าใช้จ่าย (ตรรกะการรวมบิล)
                    adults = random.randint(2, 4)
                    children = random.randint(2, 5)
                    p_adult = random.choice([120, 150, 200])
                    p_child = random.choice([60, 80, 100])
                    food = random.choice([150, 200, 300])
                    
                    cost_adults = adults * p_adult
                    cost_children = children * p_child
                    total_cost = cost_adults + cost_children + food
                    
                    q = f"ครอบครัวหนึ่งไปเที่ยวสวนสนุก มีผู้ใหญ่ <b>{adults} คน</b> และเด็ก <b>{children} คน</b> <br>ค่าบัตรผู้ใหญ่ราคาคนละ <b>{p_adult} บาท</b> ค่าบัตรเด็กราคาคนละ <b>{p_child} บาท</b> <br>นอกจากนี้ครอบครัวนี้ยังซื้ออาหารรับประทานร่วมกันอีก <b>{food} บาท</b> <br>ครอบครัวนี้ต้องจ่ายเงินรวมทั้งหมดกี่บาท?"

                    sol = f"""<span style='color:#2c3e50; line-height: 1.8;'>
                    <div style='background-color:#fcf3cf; border-left:4px solid #f1c40f; padding:15px; margin-bottom:15px; border-radius:8px;'>
                    💡 <b>การแปลภาษาไทย เป็น "สมการคณิตศาสตร์":</b><br>
                    1. <b>"บัตรผู้ใหญ่...คนละ / บัตรเด็ก...คนละ"</b> ➔ การนับของที่ราคาเท่าๆ กันหลายๆ ใบ ต้องใช้ <b style='color:#e74c3c;'>เครื่องหมายคูณ (×)</b> และเพื่อไม่ให้ราคาผู้ใหญ่กับเด็กปนกัน เราต้องใส่ <b>วงเล็บ ( )</b> แยกกลุ่มให้ชัดเจน<br>
                    2. <b>"รวมทั้งหมด / ซื้อเพิ่มอีก"</b> ➔ การนำค่าใช้จ่ายแต่ละก้อนมากองรวมกัน ต้องเชื่อมด้วย <b style='color:#3498db;'>เครื่องหมายบวก (+)</b><br>
                    <b>ประโยคสัญลักษณ์:</b> (<span style='color:#8e44ad;'>{adults}</span> <b style='color:#e74c3c;'>×</b> <span style='color:#8e44ad;'>{p_adult}</span>) <b style='color:#3498db;'>+</b> (<span style='color:#e67e22;'>{children}</span> <b style='color:#e74c3c;'>×</b> <span style='color:#e67e22;'>{p_child}</span>) <b style='color:#3498db;'>+</b> {food} = ?
                    </div>
                    <b>วิธีทำอย่างละเอียดแบบ Step-by-step:</b><br>
                    👉 <b>ขั้นที่ 1: คิดค่าบัตรกลุ่มผู้ใหญ่ (ทำในวงเล็บแรก)</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ผู้ใหญ่ <span style='color:#8e44ad;'>{adults}</span> คน × ราคา <span style='color:#8e44ad;'>{p_adult}</span> บาท = <b><span style='color:#27ae60;'>{cost_adults:,}</span> บาท</b> <i>(นี่คือเงินก้อนที่ 1)</i><br><br>
                    
                    👉 <b>ขั้นที่ 2: คิดค่าบัตรกลุ่มเด็ก (ทำในวงเล็บที่สอง)</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;เด็ก <span style='color:#e67e22;'>{children}</span> คน × ราคา <span style='color:#e67e22;'>{p_child}</span> บาท = <b><span style='color:#27ae60;'>{cost_children:,}</span> บาท</b> <i>(นี่คือเงินก้อนที่ 2)</i><br><br>
                    
                    👉 <b>ขั้นที่ 3: นำค่าใช้จ่ายทุกก้อนมารวมกัน</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ค่าผู้ใหญ่ <span style='color:#27ae60;'>{cost_adults:,}</span> + ค่าเด็ก <span style='color:#27ae60;'>{cost_children:,}</span> + ค่าอาหาร <span style='color:#3498db;'>{food}</span><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;= {cost_adults + cost_children:,} + {food}<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;= <b><span style='color:#c0392b;'>{total_cost:,}</span> บาท</b><br><br>
                    <b>ตอบ: ครอบครัวนี้ต้องจ่ายเงินรวมทั้งหมด {total_cost:,} บาท</b></span>"""

                elif scenario == "savings":
                    # สไตล์ที่ 2: การเก็บเงิน ออมเงิน และการใช้จ่าย (มีการคูณ บวก และลบ)
                    save_per_day = random.choice([15, 20, 25, 30])
                    days = random.randint(10, 20)
                    bonus = random.choice([100, 150, 200, 500])
                    buy_toy = random.randint(150, 350)
                    
                    total_saved = save_per_day * days
                    money_after_bonus = total_saved + bonus
                    final_money = money_after_bonus - buy_toy
                    
                    q = f"น้องใบบัวตั้งใจออมเงินวันละ <b>{save_per_day} บาท</b> เป็นเวลา <b>{days} วัน</b> <br>จากนั้นคุณตาให้รางวัลเด็กดีเพิ่มอีก <b>{bonus} บาท</b> <br>ใบบัวจึงนำเงินในกระปุกไปซื้อหนังสือการ์ตูนราคา <b>{buy_toy} บาท</b> <br>สุดท้ายแล้วใบบัวจะเหลือเงินกี่บาท?"

                    sol = f"""<span style='color:#2c3e50; line-height: 1.8;'>
                    <div style='background-color:#e8f8f5; border-left:4px solid #1abc9c; padding:15px; margin-bottom:15px; border-radius:8px;'>
                    💡 <b>การแปลภาษาไทย เป็น "สมการคณิตศาสตร์":</b><br>
                    1. <b>"ออมเงินวันละ... เป็นเวลา..."</b> ➔ การสะสมเงินทีละเท่าๆ กันทุกวัน คือการ <b>ทวีคูณ</b> ต้องใช้ <b style='color:#e74c3c;'>เครื่องหมายคูณ (×)</b><br>
                    2. <b>"ให้รางวัลเพิ่มอีก"</b> ➔ การได้รับมาเพิ่ม ทำให้เงินเยอะขึ้น ต้องใช้ <b style='color:#3498db;'>เครื่องหมายบวก (+)</b><br>
                    3. <b>"นำเงินไปซื้อ... / เหลือเงิน"</b> ➔ การซื้อของคือการจ่ายเงินออกไป ทำให้เงินลดลง ต้องใช้ <b style='color:#9b59b6;'>เครื่องหมายลบ (-)</b><br>
                    <b>ประโยคสัญลักษณ์:</b> (<span style='color:#2980b9;'>{save_per_day}</span> <b style='color:#e74c3c;'>×</b> <span style='color:#2980b9;'>{days}</span>) <b style='color:#3498db;'>+</b> {bonus} <b style='color:#9b59b6;'>-</b> {buy_toy} = ?
                    </div>
                    <b>วิธีทำอย่างละเอียดและที่มาของตัวเลข:</b><br>
                    👉 <b>ขั้นที่ 1: คำนวณเงินออมในกระปุก</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;วันละ <span style='color:#2980b9;'>{save_per_day}</span> บาท × <span style='color:#2980b9;'>{days}</span> วัน = <b><span style='color:#27ae60;'>{total_saved:,}</span> บาท</b> <i>(ตัวเลขจำนวนวันกับเงินรายวัน รวมร่างกันเป็นเงินก้อนแรก)</i><br><br>
                    
                    👉 <b>ขั้นที่ 2: รวมกับเงินรางวัลที่คุณตาให้</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;เงินในกระปุก <span style='color:#27ae60;'>{total_saved:,}</span> บาท <b style='color:#3498db;'>+ บวกเพิ่ม</b> เงินรางวัล {bonus} บาท = <b><span style='color:#e67e22;'>{money_after_bonus:,}</span> บาท</b> <i>(นี่คือเงินทั้งหมดที่ใบบัวมีก่อนไปร้านหนังสือ)</i><br><br>
                    
                    👉 <b>ขั้นที่ 3: หักเงินค่าซื้อหนังสือการ์ตูน</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;เงินที่มี <span style='color:#e67e22;'>{money_after_bonus:,}</span> บาท <b style='color:#9b59b6;'>- ลบออก</b> ค่าหนังสือ {buy_toy} บาท = <b><span style='color:#c0392b;'>{final_money:,}</span> บาท</b><br><br>
                    <b>ตอบ: ใบบัวจะเหลือเงิน {final_money:,} บาท</b></span>"""

                elif scenario == "library":
                    # สไตล์ที่ 3: การจัดของ บริจาค และแบ่งกลุ่ม (มีการคูณ ลบ และหาร)
                    boxes = random.randint(4, 8)
                    books_per_box = random.choice([25, 30, 40, 50])
                    donate = random.choice([20, 30, 40, 50])
                    shelves = random.randint(3, 6)
                    
                    total_books = boxes * books_per_box
                    books_left = total_books - donate
                    
                    # บังคับให้เลขหารลงตัว
                    remainder = books_left % shelves
                    if remainder != 0:
                        donate -= remainder  # ปรับยอดบริจาคเพื่อให้หารลงตัว
                        books_left = total_books - donate
                        
                    ans = books_left // shelves
                    
                    q = f"ห้องสมุดแห่งหนึ่งได้รับบริจาคหนังสือมา <b>{boxes} ลัง</b> แต่ละลังมีหนังสือ <b>{books_per_box} เล่ม</b> <br>บรรณารักษ์คัดหนังสือที่ชำรุดออกไปทิ้ง <b>{donate} เล่ม</b> <br>จากนั้นนำหนังสือที่เหลือทั้งหมด ไปจัดเรียงใส่ชั้นวาง <b>{shelves} ชั้น ชั้นละเท่าๆ กัน</b> <br>แต่ละชั้นจะมีหนังสือกี่เล่ม?"

                    sol = f"""<span style='color:#2c3e50; line-height: 1.8;'>
                    <div style='background-color:#fef5e7; border-left:4px solid #e67e22; padding:15px; margin-bottom:15px; border-radius:8px;'>
                    💡 <b>การแปลภาษาไทย เป็น "สมการคณิตศาสตร์":</b><br>
                    1. <b>"ได้มา...ลัง ลังละ..."</b> ➔ ต้องหาจำนวนหนังสือทั้งหมดก่อน โดยใช้ <b style='color:#e74c3c;'>เครื่องหมายคูณ (×)</b><br>
                    2. <b>"คัดที่ชำรุดออกไปทิ้ง"</b> ➔ ของหายไป มีน้อยลง ต้องใช้ <b style='color:#9b59b6;'>เครื่องหมายลบ (-)</b><br>
                    3. <b>"นำที่เหลือ จัดใส่ชั้น ชั้นละเท่าๆ กัน"</b> ➔ การแบ่งกลุ่มกลุ่มละเท่ากัน คือพระเอกของ <b style='color:#d35400;'>เครื่องหมายหาร (÷)</b><br>
                    <b>ประโยคสัญลักษณ์:</b> [(<span style='color:#8e44ad;'>{boxes}</span> <b style='color:#e74c3c;'>×</b> <span style='color:#8e44ad;'>{books_per_box}</span>) <b style='color:#9b59b6;'>-</b> {donate}] <b style='color:#d35400;'>÷</b> {shelves} = ?
                    </div>
                    <b>วิธีทำอย่างละเอียดและที่มาของตัวเลข:</b><br>
                    👉 <b>ขั้นที่ 1: หาจำนวนหนังสือทั้งหมดที่ได้รับมาก่อน</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;มี <span style='color:#8e44ad;'>{boxes}</span> ลัง × ลังละ <span style='color:#8e44ad;'>{books_per_box}</span> เล่ม = <b><span style='color:#27ae60;'>{total_books:,}</span> เล่ม</b> <i>(ตัวเลขลังหายไป กลายเป็นยอดหนังสือรวม)</i><br><br>
                    
                    👉 <b>ขั้นที่ 2: หักหนังสือที่ชำรุดออกไป</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;มีหนังสือ <span style='color:#27ae60;'>{total_books:,}</span> เล่ม <b style='color:#9b59b6;'>- ลบออก</b> ที่ชำรุด {donate} เล่ม = <b><span style='color:#e67e22;'>{books_left:,}</span> เล่ม</b> <i>(นี่คือหนังสือสภาพดีที่พร้อมจะเอาไปจัดขึ้นชั้น)</i><br><br>
                    
                    👉 <b>ขั้นที่ 3: นำหนังสือสภาพดีไปแบ่งจัดใส่ชั้น</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;หนังสือ <span style='color:#e67e22;'>{books_left:,}</span> เล่ม <b style='color:#d35400;'>÷ หารแบ่ง</b> ใส่ {shelves} ชั้น = <b><span style='color:#c0392b;'>{ans:,}</span> เล่ม</b><br><br>
                    <b>ตอบ: แต่ละชั้นจะมีหนังสือ {ans:,} เล่ม</b></span>"""

                else:
                    # สไตล์ที่ 4: สมการวงเล็บซ้อนวงเล็บ (วัดความแม่นยำเรื่องลำดับการทำเครื่องหมายขั้นสูง)
                    # รูปแบบ: A - (B + C) * D / E
                    b = random.randint(5, 15)
                    c = random.randint(5, 15)
                    d = random.randint(2, 6)
                    e = random.choice([2, 3, 4, 5])
                    
                    # บังคับให้หารลงตัว
                    sum_bc = b + c
                    while (sum_bc * d) % e != 0:
                        c += 1
                        sum_bc = b + c
                        
                    mul_div_res = (sum_bc * d) // e
                    
                    # ให้ A มากกว่าผลลัพธ์ก้อนหลัง จะได้ไม่ติดลบ
                    a = mul_div_res + random.randint(10, 50)
                    final_ans = a - mul_div_res
                    
                    q = f"จงหาผลลัพธ์ของสมการต่อไปนี้ โดยใช้กฎลำดับการคำนวณทางคณิตศาสตร์<br><br><div style='text-align:center; font-size:28px; font-weight:bold; letter-spacing:2px; background:#f8f9fa; padding:15px; border-radius:10px; border:2px dashed #bdc3c7;'>{a} - ({b} + {c}) × {d} ÷ {e} = ?</div>"

                    sol = f"""<span style='color:#2c3e50; line-height: 1.8;'>
                    <div style='background-color:#fcf3cf; border-left:4px solid #f1c40f; padding:15px; margin-bottom:15px; border-radius:8px;'>
                    💡 <b>กฎข้อตกลงระดับโลก (PEMDAS / ลำดับการคำนวณ):</b><br>
                    <b>อันดับ 1:</b> ต้องทำใน <b>วงเล็บ ( )</b> ก่อนเสมอ ไม่ว่าข้างในจะเป็นเครื่องหมายอะไรก็ตาม!<br>
                    <b>อันดับ 2:</b> ทำ <b>คูณ (×)</b> หรือ <b>หาร (÷)</b> โดยไล่จากซ้ายไปขวา<br>
                    <b>อันดับ 3:</b> ทำ <b>บวก (+)</b> หรือ <b>ลบ (-)</b> เป็นลำดับสุดท้าย
                    </div>
                    <b>วิธีทำอย่างละเอียดแบบ Step-by-step:</b><br>
                    👉 <b>ขั้นที่ 1: ทำในวงเล็บก่อนเป็นอันดับแรก</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;โจทย์คือ: {a} - <b style='color:#8e44ad;'>({b} + {c})</b> × {d} ÷ {e}<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ในวงเล็บคือ <b style='color:#8e44ad;'>{b} + {c}</b> = <b><span style='color:#27ae60;'>{sum_bc}</span></b> <i>(วงเล็บจะแตกสลาย กลายเป็นตัวเลข <span style='color:#27ae60;'>{sum_bc}</span>)</i><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;สมการปัจจุบันเหลือ: {a} - <span style='color:#27ae60;'>{sum_bc}</span> <b style='color:#e74c3c;'>×</b> {d} <b style='color:#e74c3c;'>÷</b> {e}<br><br>
                    
                    👉 <b>ขั้นที่ 2: จัดการ คูณ(×) และ หาร(÷) โดยทำจากซ้ายไปขวา</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• <i>เจอคูณก่อนทำคูณ:</i> <span style='color:#27ae60;'>{sum_bc}</span> <b style='color:#e74c3c;'>×</b> {d} = <b><span style='color:#2980b9;'>{sum_bc * d}</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;สมการปัจจุบันเหลือ: {a} - <span style='color:#2980b9;'>{sum_bc * d}</span> <b style='color:#e74c3c;'>÷</b> {e}<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• <i>เจอหารทำหารต่อ:</i> <span style='color:#2980b9;'>{sum_bc * d}</span> <b style='color:#e74c3c;'>÷</b> {e} = <b><span style='color:#d35400;'>{mul_div_res}</span></b> <i>(ก้อนตัวเลขด้านหลังถูกยุบรวมเหลือแค่นี้)</i><br><br>
                    
                    👉 <b>ขั้นที่ 3: จัดการลบ (-) เป็นขั้นตอนสุดท้าย</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;นำตัวเลขตัวตั้ง มาลบกับผลลัพธ์ของก้อนด้านหลัง<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;{a} - <span style='color:#d35400;'>{mul_div_res}</span> = <b><span style='color:#c0392b;'>{final_ans}</span></b><br><br>
                    <b>ตอบ: {final_ans}</b></span>"""




            elif actual_sub_t == "จำนวนเต็มลบเบื้องต้น":
                # สุ่มสถานการณ์ 3 รูปแบบ เพื่อให้เด็กเห็นภาพว่าจำนวนเต็มลบใช้ทำอะไรในชีวิตจริง
                scenario = random.choice(["temperature", "submarine", "debt"])

                if scenario == "temperature":
                    # สไตล์ที่ 1: อุณหภูมิ (ยอดฮิต)
                    t_start = random.randint(-15, -2) # อุณหภูมิเริ่มต้น (ติดลบ)
                    t_drop = random.randint(3, 10)    # อุณหภูมิลดลง
                    t_rise = random.randint(5, 20)    # อุณหภูมิเพิ่มขึ้น
                    
                    step1_val = t_start - t_drop
                    final_ans = step1_val + t_rise
                    
                    ans_text = f"อุณหภูมิ {final_ans} องศาเซลเซียส" if final_ans >= 0 else f"อุณหภูมิติดลบ {abs(final_ans)} องศาเซลเซียส (หรือ {final_ans} องศา)"
                    
                    q = f"เมืองหิมะแห่งหนึ่ง มีอุณหภูมิเริ่มต้นในตอนเช้า <b>{t_start} องศาเซลเซียส</b> <br>พอตกดึกอากาศหนาวจัด อุณหภูมิ <b>ลดลงไปอีก {t_drop} องศาเซลเซียส</b> <br>เมื่อถึงรุ่งเช้าของอีกวัน มีแสงแดดส่อง ทำให้อุณหภูมิ <b>เพิ่มขึ้น {t_rise} องศาเซลเซียส</b> <br>จงหาว่าอุณหภูมิในตอนท้ายคือเท่าใด?"
                    
                    sol = f"""<span style='color:#2c3e50; line-height: 1.8;'>
                    <div style='background-color:#fcf3cf; border-left:4px solid #f1c40f; padding:15px; margin-bottom:15px; border-radius:8px;'>
                    💡 <b>การแปลภาษาไทย เป็น "สมการคณิตศาสตร์":</b><br>
                    • <b>"อุณหภูมิเริ่มต้น {t_start} องศา"</b> ➔ เป็นจุดสตาร์ทของเรา เขียนแทนด้วย <b style='color:#3498db;'>({t_start})</b><br>
                    • <b>"ลดลงไปอีก {t_drop} องศา"</b> ➔ คำว่า <i>'ลดลง/หนาวลง'</i> คือการหักค่าออกไป ต้องใช้ <b style='color:#c0392b;'>เครื่องหมายลบ (-)</b><br>
                    • <b>"เพิ่มขึ้น {t_rise} องศา"</b> ➔ คำว่า <i>'เพิ่มขึ้น/อุ่นขึ้น'</i> คือการบวกค่าเข้าไป ต้องใช้ <b style='color:#27ae60;'>เครื่องหมายบวก (+)</b><br>
                    <b>ประโยคสัญลักษณ์:</b> <span style='color:#3498db;'>({t_start})</span> <b style='color:#c0392b;'>-</b> {t_drop} <b style='color:#27ae60;'>+</b> {t_rise} = ?
                    </div>
                    
                    <div style='background-color:#e8f8f5; border-left:4px solid #1abc9c; padding:15px; margin-bottom:15px; border-radius:8px;'>
                    🧠 <b>แนวคิดเรื่องเส้นจำนวน (Number Line):</b><br>
                    ให้นึกภาพเทอร์โมมิเตอร์ที่มีเลข 0 อยู่ตรงกลาง<br>
                    - การ <b style='color:#c0392b;'>ลบ (-)</b> คือการเดินถอยหลัง <b>ลงไปด้านล่าง (ตัวเลขติดลบเยอะขึ้น)</b><br>
                    - การ <b style='color:#27ae60;'>บวก (+)</b> คือการเดินขึ้น <b>ไปด้านบน (ตัวเลขมีค่ามากขึ้น)</b>
                    </div>

                    <b>วิธีทำอย่างละเอียดและที่มาของตัวเลข:</b><br>
                    👉 <b>ขั้นที่ 1: คิดอุณหภูมิตอนตกดึก</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;อุณหภูมิเดิมคือ <span style='color:#3498db;'>{t_start}</span> แล้ว <b style='color:#c0392b;'>ลดลง {t_drop}</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;สมการคือ: <span style='color:#3498db;'>({t_start})</span> <b style='color:#c0392b;'>- {t_drop}</b> = <b><span style='color:#8e44ad;'>{step1_val}</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;<i>(อธิบาย: เราติดลบอยู่แล้ว {abs(t_start)} องศา แล้วถอยหลังลึกลงไปอีก {t_drop} ก้าว ทำให้เรายิ่งติดลบหนักขึ้นไปอยู่ที่ <span style='color:#8e44ad;'>{step1_val}</span>)</i><br><br>
                    
                    👉 <b>ขั้นที่ 2: คิดอุณหภูมิตอนรุ่งเช้า (ได้แสงแดด)</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;นำตัวเลขอุณหภูมิล่าสุดคือ <span style='color:#8e44ad;'>{step1_val}</span> มาทำให้ <b style='color:#27ae60;'>เพิ่มขึ้น {t_rise}</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;สมการคือ: <span style='color:#8e44ad;'>({step1_val})</span> <b style='color:#27ae60;'>+ {t_rise}</b> = <b><span style='color:#e74c3c;'>{final_ans}</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;<i>(อธิบาย: เราอยู่ที่ <span style='color:#8e44ad;'>{step1_val}</span> จากนั้นเดินขึ้นมาทางด้านบน {t_rise} ก้าว จึงมาหยุดอยู่ที่ <span style='color:#e74c3c;'>{final_ans}</span>)</i><br><br>
                    
                    <b>ตอบ: {ans_text}</b>
                    </span>"""

                elif scenario == "submarine":
                    # สไตล์ที่ 2: ระดับน้ำทะเล (ใต้ผิวน้ำ)
                    d_start = random.randint(20, 80) # ความลึกเริ่มต้น (ต้องนำไปแปลงเป็นเลขลบ)
                    d_dive = random.randint(15, 40)  # ดำลึกลงไปอีก
                    d_rise = random.randint(30, 100) # ลอยตัวขึ้นมา
                    
                    # แปลงเป็นระดับบนแกน Y (ใต้น้ำ = ติดลบ)
                    y_start = -d_start
                    step1_val = y_start - d_dive
                    final_ans = step1_val + d_rise
                    
                    if final_ans < 0:
                        ans_text = f"อยู่ใต้ผิวน้ำ {abs(final_ans)} เมตร (ระดับ {final_ans} เมตร)"
                    elif final_ans == 0:
                        ans_text = f"ลอยอยู่ปริ่มผิวน้ำพอดี (ระดับ 0 เมตร)"
                    else:
                        ans_text = f"ลอยอยู่เหนือผิวน้ำ {final_ans} เมตร"
                    
                    q = f"เรือดำน้ำลำหนึ่ง กำลังลอยอยู่ใต้ผิวน้ำที่ระดับ <b>{d_start} เมตร</b> <br>เพื่อหลบหลีกศัตรู กัปตันสั่งให้ <b>ดำลึกลงไปอีก {d_dive} เมตร</b> <br>เมื่อปลอดภัยแล้ว จึงสั่งให้ <b>ลอยตัวขึ้นมา {d_rise} เมตร</b> <br>จงหาว่าปัจจุบันเรือดำน้ำลำนี้อยู่ที่ระดับใดเมื่อเทียบกับผิวน้ำ?"
                    
                    sol = f"""<span style='color:#2c3e50; line-height: 1.8;'>
                    <div style='background-color:#fcf3cf; border-left:4px solid #f1c40f; padding:15px; margin-bottom:15px; border-radius:8px;'>
                    💡 <b>การแปลภาษาไทย เป็น "สมการคณิตศาสตร์":</b><br>
                    ในการวัดระดับความสูง <b>เราจะให้ "ผิวน้ำ" มีค่าเป็น 0</b> เสมอ!<br>
                    • <b>"อยู่ใต้ผิวน้ำ {d_start} เมตร"</b> ➔ แปลว่าอยู่ต่ำกว่าศูนย์ ต้องเขียนเป็น <b>เลขติดลบ</b> คือ <b style='color:#3498db;'>-{d_start}</b><br>
                    • <b>"ดำลึกลงไปอีก {d_dive} เมตร"</b> ➔ คือการลงไปต่ำกว่าเดิม ต้องหักออกด้วย <b style='color:#c0392b;'>เครื่องหมายลบ (-)</b><br>
                    • <b>"ลอยตัวขึ้นมา {d_rise} เมตร"</b> ➔ คือการขึ้นมาใกล้ระดับศูนย์มากขึ้น ต้องใช้ <b style='color:#27ae60;'>เครื่องหมายบวก (+)</b><br>
                    <b>ประโยคสัญลักษณ์:</b> <span style='color:#3498db;'>(-{d_start})</span> <b style='color:#c0392b;'>-</b> {d_dive} <b style='color:#27ae60;'>+</b> {d_rise} = ?
                    </div>

                    <b>วิธีทำอย่างละเอียดและที่มาของตัวเลข:</b><br>
                    👉 <b>ขั้นที่ 1: คำนวณความลึกตอนหลบศัตรู</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ตำแหน่งเดิมคือ <span style='color:#3498db;'>(-{d_start})</span> แล้ว <b style='color:#c0392b;'>ดำลึกลง (- {d_dive})</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;สมการคือ: <span style='color:#3498db;'>(-{d_start})</span> <b style='color:#c0392b;'>- {d_dive}</b> = <b><span style='color:#8e44ad;'>{step1_val}</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;<i>(อธิบาย: อยู่ใต้น้ำอยู่แล้ว แล้วลงไปลึกกว่าเดิมอีก ตัวเลขจึงยิ่งติดลบมากขึ้น กลายเป็น <span style='color:#8e44ad;'>{step1_val}</span>)</i><br><br>
                    
                    👉 <b>ขั้นที่ 2: คำนวณตำแหน่งตอนปลอดภัย</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;นำตำแหน่งลึกสุดคือ <span style='color:#8e44ad;'>{step1_val}</span> มา <b style='color:#27ae60;'>ลอยตัวขึ้น (+ {d_rise})</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;สมการคือ: <span style='color:#8e44ad;'>({step1_val})</span> <b style='color:#27ae60;'>+ {d_rise}</b> = <b><span style='color:#e74c3c;'>{final_ans}</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;<i>(อธิบาย: จากจุดที่ลึกที่สุด เราเดินสวนทางบวกขึ้นมา {d_rise} เมตร จึงมาหยุดที่ <span style='color:#e74c3c;'>{final_ans}</span>)</i><br><br>
                    
                    <b>ตอบ: เรือดำน้ำ {ans_text}</b>
                    </span>"""

                else:
                    # สไตล์ที่ 3: สถานะการเงิน/หนี้สิน (เด็กจะเข้าใจง่ายที่สุด)
                    names = ["ข้าวหอม", "พายุ", "ธาม", "มะลิ"]
                    name = random.choice(names)
                    
                    debt1 = random.randint(20, 50)  # ยืมครั้งแรก (หนี้)
                    debt2 = random.randint(15, 40)  # ยืมเพิ่มอีก (หนี้เพิ่ม)
                    pay_back = random.randint(40, 150) # ได้เงินมาคืน
                    
                    start_val = -debt1
                    step1_val = start_val - debt2
                    final_ans = step1_val + pay_back
                    
                    if final_ans < 0:
                        ans_text = f"ยังคงเป็นหนี้เพื่อนอยู่ {abs(final_ans)} บาท (สถานะการเงินคือ {final_ans} บาท)"
                    elif final_ans == 0:
                        ans_text = f"ใช้หนี้หมดพอดี และไม่มีเงินเหลือ (สถานะการเงิน 0 บาท)"
                    else:
                        ans_text = f"ใช้หนี้หมดและมีเงินเหลือเป็นของตัวเอง {final_ans} บาท"
                    
                    q = f"{name}ลืมเอาเงินมาโรงเรียน จึง <b>ยืมเงินเพื่อนไป {debt1} บาท</b> <br>ตอนบ่ายอยากกินขนม จึง <b>ขอยืมเงินเพื่อนเพิ่มอีก {debt2} บาท</b> <br>วันรุ่งขึ้น {name}ได้ค่าขนมมา จึง <b>นำเงินไปคืนเพื่อน {pay_back} บาท</b> <br>จงหาว่า สถานะการเงินของ{name}ในตอนนี้เป็นอย่างไร?"

                    sol = f"""<span style='color:#2c3e50; line-height: 1.8;'>
                    <div style='background-color:#fcf3cf; border-left:4px solid #f1c40f; padding:15px; margin-bottom:15px; border-radius:8px;'>
                    💡 <b>การแปลภาษาไทย เป็น "สมการคณิตศาสตร์":</b><br>
                    จำไว้ว่า <b>"หนี้สิน = การไม่มีเงิน แถมยังติดลบ"</b><br>
                    • <b>"ยืมเงินเพื่อน {debt1} บาท"</b> ➔ แปลว่าเงินในกระเป๋าเราติดลบ เขียนเป็น <b style='color:#3498db;'>-{debt1}</b><br>
                    • <b>"ยืมเพิ่มอีก {debt2} บาท"</b> ➔ คือการสร้างหนี้เพิ่ม หนี้คือการลบออก ต้องใช้ <b style='color:#c0392b;'>เครื่องหมายลบ (-)</b><br>
                    • <b>"นำเงินไปคืน {pay_back} บาท"</b> ➔ คือการนำเงินที่เรามี ไปหักล้างหนี้ ทำให้สถานะการเงินเราดีขึ้น ต้องใช้ <b style='color:#27ae60;'>เครื่องหมายบวก (+)</b><br>
                    <b>ประโยคสัญลักษณ์:</b> <span style='color:#3498db;'>(-{debt1})</span> <b style='color:#c0392b;'>-</b> {debt2} <b style='color:#27ae60;'>+</b> {pay_back} = ?
                    </div>

                    <b>วิธีทำอย่างละเอียดและที่มาของตัวเลข:</b><br>
                    👉 <b>ขั้นที่ 1: คำนวณหนี้สินรวมทั้งหมด</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ตอนแรกติดหนี้อยู่ <span style='color:#3498db;'>(-{debt1})</span> แล้ว <b style='color:#c0392b;'>ยืมเพิ่ม (- {debt2})</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;สมการคือ: <span style='color:#3498db;'>(-{debt1})</span> <b style='color:#c0392b;'>- {debt2}</b> = <b><span style='color:#8e44ad;'>{step1_val}</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;<i>(อธิบาย: เป็นหนี้อยู่แล้ว ไปยืมเพิ่มอีก หนี้ก็เลยพอกพูนขึ้น รวมเป็นยอดหนี้ทั้งหมด {abs(step1_val)} บาท หรือสถานะ <span style='color:#8e44ad;'>{step1_val}</span>)</i><br><br>
                    
                    👉 <b>ขั้นที่ 2: นำเงินไปหักล้างหนี้ (คืนเงิน)</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;นำยอดหนี้ <span style='color:#8e44ad;'>{step1_val}</span> มาทำการ <b style='color:#27ae60;'>คืนเงิน (+ {pay_back})</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;สมการคือ: <span style='color:#8e44ad;'>({step1_val})</span> <b style='color:#27ae60;'>+ {pay_back}</b> = <b><span style='color:#e74c3c;'>{final_ans}</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;<i>(อธิบาย: นำเงิน {pay_back} บาท ไปจ่ายหนี้ {abs(step1_val)} บาท ถ้าเงินพอจ่ายก็จะเหลือตังค์ทอน แต่ถ้าเงินไม่พอก็จะยังติดลบอยู่ ซึ่งผลลัพธ์ออกมาเป็น <span style='color:#e74c3c;'>{final_ans}</span>)</i><br><br>
                    
                    <b>ตอบ: {name} {ans_text}</b>
                    </span>"""




# ================= หมวดที่ 1: รากฐานตัวเลขและการดำเนินการ (ป.5) =================
            elif actual_sub_t == "เทคนิคคิดเลขเร็วและสมบัติการแจกแจง":
                # สุ่ม 3 สถานการณ์ (ข้อสอบแข่งขัน, ซื้อของปัดเศษ, ซื้อของจัดกรุ๊ป)
                scenario = random.choice(["pull_out_exam", "round_up_shop", "group_buy"])

                if scenario == "pull_out_exam":
                    # สไตล์ที่ 1: การดึงตัวร่วม (สไตล์ข้อสอบแข่งขันยอดฮิต)
                    # รูปแบบ: (A x B) + (A x C) = A x (B + C) โดยที่ B+C = 100 หรือ 1000
                    target_sum = random.choice([100, 1000])
                    common_a = random.choice([45, 99, 125, 255, 345, 875])
                    b = random.randint(15, target_sum // 2)
                    c = target_sum - b
                    
                    # สลับบวกลบให้หลากหลาย
                    op = random.choice(["+", "-"])
                    if op == "-":
                        # ถ้าเป็นลบ ต้องให้ B - C = 100 หรือ 10
                        target_diff = random.choice([10, 100])
                        c = random.randint(15, 90)
                        b = c + target_diff
                        
                    part1 = common_a * b
                    part2 = common_a * c
                    final_ans = part1 + part2 if op == "+" else part1 - part2
                    target_num = b + c if op == "+" else b - c
                    
                    op_color = "#3498db" if op == "+" else "#9b59b6"
                    op_text = "บวก" if op == "+" else "ลบ"

                    q = f"จงหาผลลัพธ์ของสมการต่อไปนี้ <b>(โดยใช้เทคนิคคิดเลขเร็ว)</b><br><br><div style='text-align:center; font-size:28px; font-weight:bold; letter-spacing:2px; background:#f8f9fa; padding:15px; border-radius:10px; border:2px dashed #bdc3c7;'>( {common_a:,} × {b:,} ) <span style='color:{op_color};'>{op}</span> ( {common_a:,} × {c:,} ) = ?</div>"

                    sol = f"""<span style='color:#2c3e50; line-height: 1.8;'>
                    <div style='background-color:#fcf3cf; border-left:4px solid #f1c40f; padding:15px; margin-bottom:15px; border-radius:8px;'>
                    💡 <b>สมบัติการแจกแจง (Distributive Property) - "เทคนิคการดึงตัวร่วม":</b><br>
                    เมื่อเราเห็นตัวเลขหน้าตาเหมือนกันเป๊ะ คูณอยู่กับกลุ่มตัวเลขอื่น เราสามารถ <b>"ดึงตัวที่เหมือนกันออกมาไว้ข้างนอก"</b> ได้เลย เพื่อให้เลขที่เหลือรวมกันเป็นเลขกลมๆ คิดง่ายๆ แบบไม่ต้องตั้งคูณยาวๆ
                    <br>
                    </div>
                    <b>วิธีทำอย่างละเอียดแบบ Step-by-step:</b><br>
                    👉 <b>ขั้นที่ 1: สังเกตหา "ฝาแฝด" (ตัวร่วม)</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ในโจทย์มีตัวเลขที่เหมือนกันคือ <b style='color:#e74c3c;'>{common_a:,}</b> ซึ่งกำลัง <b style='color:#27ae60;'>คูณ (×)</b> อยู่กับตัวเลขอื่นทั้งสองวงเล็บ<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;วงเล็บหน้า: <span style='color:#e74c3c;'>{common_a:,}</span> คูณอยู่กับ <span style='color:#2980b9;'>{b:,}</span><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;วงเล็บหลัง: <span style='color:#e74c3c;'>{common_a:,}</span> คูณอยู่กับ <span style='color:#2980b9;'>{c:,}</span><br><br>
                    
                    👉 <b>ขั้นที่ 2: ใช้เวทมนตร์ "ดึงตัวร่วม" ออกมา</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ให้ดึง <span style='color:#e74c3c;'>{common_a:,}</span> ออกมาวางไว้ข้างหน้าสุดเพียงตัวเดียว แล้วเอาตัวเลขที่เหลือมารวมกันในวงเล็บใหญ่ โดยใช้เครื่องหมาย <b style='color:{op_color};'>{op_text} ({op})</b> ตามโจทย์<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;สมการใหม่จะกลายเป็น: <b><span style='color:#e74c3c;'>{common_a:,}</span> <span style='color:#27ae60;'>×</span> ( <span style='color:#2980b9;'>{b:,}</span> <span style='color:{op_color};'>{op}</span> <span style='color:#2980b9;'>{c:,}</span> )</b><br><br>
                    
                    👉 <b>ขั้นที่ 3: คำนวณในวงเล็บ (ซึ่งกลายเป็นเลขกลมๆ คิดง่ายมาก)</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ในวงเล็บ: <span style='color:#2980b9;'>{b:,}</span> <span style='color:{op_color};'>{op}</span> <span style='color:#2980b9;'>{c:,}</span> = <b><span style='color:#8e44ad;'>{target_num:,}</span></b> <i>(ตัวเลขยุบรวมกันอย่างสวยงาม)</i><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;นำกลับไปคูณตัวหน้า: <span style='color:#e74c3c;'>{common_a:,}</span> <span style='color:#27ae60;'>×</span> <span style='color:#8e44ad;'>{target_num:,}</span><br><br>
                    
                    👉 <b>ขั้นที่ 4: คูณขั้นสุดท้าย</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;การคูณด้วยหลักร้อยหลักสิบ ให้เติม 0 ต่อท้ายได้เลย ➔ {common_a:,} เติมศูนย์ = <b><span style='color:#c0392b;'>{final_ans:,}</span></b><br><br>
                    <b>ตอบ: {final_ans:,}</b></span>"""

                elif scenario == "round_up_shop":
                    # สไตล์ที่ 2: ปัดเลข 99 หรือ 98 (เทคนิคซื้อของในชีวิตประจำวัน)
                    # รูปแบบ: A x 99 = A x (100 - 1)
                    item = random.choice(["เสื้อยืด", "หนังสือ", "ของเล่น", "หมอน"])
                    count = random.randint(4, 9)
                    price = random.choice([98, 99, 198, 199, 998, 999])
                    
                    # คำนวณส่วนต่าง
                    if price in [98, 99]: base = 100
                    elif price in [198, 199]: base = 200
                    else: base = 1000
                    
                    diff = base - price
                    total_price = count * price
                    
                    q = f"คุณแม่ต้องการซื้อ{item}จำนวน <b>{count} ชิ้น</b> ราคาชิ้นละ <b>{price} บาท</b> <br>คุณแม่จะต้องจ่ายเงินกี่บาท? <b>(จงแสดงวิธีคิดเลขเร็วโดยใช้สมบัติการแจกแจง)</b>"

                    sol = f"""<span style='color:#2c3e50; line-height: 1.8;'>
                    <div style='background-color:#e8f8f5; border-left:4px solid #1abc9c; padding:15px; margin-bottom:15px; border-radius:8px;'>
                    💡 <b>การแปลภาษาไทย เป็น "สมการคณิตศาสตร์":</b><br>
                    • <b>"ราคาชิ้นละ... ซื้อหลายชิ้น"</b> ➔ การนับเพิ่มครั้งละเท่าๆ กัน ต้องใช้ <b style='color:#e74c3c;'>เครื่องหมายคูณ (×)</b><br>
                    • <b>ประโยคสัญลักษณ์ตั้งต้น:</b> {count} <b style='color:#e74c3c;'>×</b> {price} = ?<br><br>
                    🔥 <b>เทคนิคคิดเลขเร็ว (ปัดเลขแล้วทอนคืน):</b><br>
                    ราคา <span style='color:#2980b9;'>{price}</span> บาท มันคิดยาก เราสามารถมองเป็น <b>{base} บาท ลบออกด้วยเงินทอน {diff} บาท</b> ➔ <span style='color:#2980b9;'>({base} - {diff})</span>
                    </div>
                    <b>วิธีทำอย่างละเอียดแบบ Step-by-step:</b><br>
                    👉 <b>ขั้นที่ 1: เปลี่ยนตัวเลขให้คิดง่ายขึ้น</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;จากสมการเดิม: {count} <b style='color:#e74c3c;'>×</b> <span style='color:#2980b9;'>{price}</span><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;เปลี่ยนเลข {price} เป็น ({base} - {diff}) ➔ จะได้สมการใหม่: <b>{count} <span style='color:#e74c3c;'>×</span> <span style='color:#8e44ad;'>({base} - {diff})</span></b><br><br>
                    
                    👉 <b>ขั้นที่ 2: ใช้ "สมบัติการแจกแจง" (คูณกระจายเข้าไป)</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;เราต้องกระจาย {count} เข้าไปคูณตัวเลขในวงเล็บทีละตัว<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• กระจายเข้าไปหา {base} ➔ ({count} × {base}) = <b><span style='color:#27ae60;'>{count * base:,}</span></b> <i>(คิดเสมือนว่าซื้อของชิ้นละ {base} บาท)</i><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• กระจายเข้าไปหา {diff} ➔ ({count} × {diff}) = <b><span style='color:#c0392b;'>{count * diff}</span></b> <i>(คิดเสมือนว่าคือเงินทอนที่ต้องได้คืนชิ้นละ {diff} บาท)</i><br><br>
                    
                    👉 <b>ขั้นที่ 3: นำมาลบกันเพื่อหาค่าใช้จ่ายจริง</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;นำยอดที่คิดเกิน <span style='color:#27ae60;'>{count * base:,}</span> <b style='color:#9b59b6;'>ลบ (-)</b> ด้วยยอดเงินทอนรวม <span style='color:#c0392b;'>{count * diff}</span><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;สมการ: <span style='color:#27ae60;'>{count * base:,}</span> - <span style='color:#c0392b;'>{count * diff}</span> = <b><span style='color:#d35400;'>{total_price:,}</span></b><br><br>
                    <b>ตอบ: คุณแม่จะต้องจ่ายเงิน {total_price:,} บาท</b></span>"""

                else:
                    # สไตล์ที่ 3: ซื้อของจัดกรุ๊ป (กระจายแจกแจง)
                    # รูปแบบ: A x B + A x C = A x (B + C) ประยุกต์ใช้กับชีวิตจริง
                    item1, item2 = random.sample(["สมุด", "ปากกา", "ยางลบ", "ไม้บรรทัด", "ดินสอ"], 2)
                    people = random.choice([15, 20, 25, 30, 40])
                    p1 = random.randint(12, 25)
                    p2 = random.choice([x for x in range(5, 25) if (p1 + x) % 10 == 0]) # บังคับให้ราคารวมกันลงท้ายด้วย 0
                    
                    total_per_person = p1 + p2
                    total_all = people * total_per_person
                    
                    q = f"คุณครูต้องการจัดชุดเครื่องเขียนแจกนักเรียน <b>{people} คน</b> <br>โดยนักเรียนแต่ละคนจะได้รับ {item1} 1 ชิ้น <b>ราคา {p1} บาท</b> และ {item2} 1 ชิ้น <b>ราคา {p2} บาท</b> <br>คุณครูต้องใช้งบประมาณทั้งหมดกี่บาท? <b>(จงแสดงวิธีคิดเลขเร็วโดยใช้สมบัติการแจกแจง)</b>"

                    sol = f"""<span style='color:#2c3e50; line-height: 1.8;'>
                    <div style='background-color:#fef5e7; border-left:4px solid #e67e22; padding:15px; margin-bottom:15px; border-radius:8px;'>
                    💡 <b>การแปลภาษาไทย เป็น "สมการคณิตศาสตร์":</b><br>
                    ข้อนี้มีวิธีคิด 2 แบบ:<br>
                    • <b>แบบคนทั่วไป:</b> คิดค่า{item1}ของเด็กทุกคนก่อน แล้วไปบวกกับค่า{item2}ของเด็กทุกคน ➔ (<span style='color:#e74c3c;'>{people}</span> × {p1}) + (<span style='color:#e74c3c;'>{people}</span> × {p2})<br>
                    • <b>แบบคิดเลขเร็ว (ใช้สมบัติการแจกแจง):</b> ในเมื่อเด็กทุกคนได้ของ 2 อย่างเหมือนกัน เราก็ <b>"รวมราคาของ 1 ชุด"</b> ก่อน แล้วค่อย <b>"คูณจำนวนเด็กทีเดียว"</b> ➔ <span style='color:#e74c3c;'>{people}</span> × ({p1} + {p2})<br>
                    <br>
                    </div>
                    <b>วิธีทำอย่างละเอียดแบบ Step-by-step:</b><br>
                    👉 <b>ขั้นที่ 1: คิดราคาสิ่งของ 1 ชุดก่อน (บวกกันในวงเล็บ)</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ราคา{item1} <span style='color:#2980b9;'>{p1}</span> บาท <b style='color:#3498db;'>บวก (+)</b> ราคา{item2} <span style='color:#2980b9;'>{p2}</span> บาท<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;{p1} + {p2} = <b><span style='color:#8e44ad;'>{total_per_person}</span> บาท/ชุด</b> <i>(ตัวเลขยุบรวมกัน กลายเป็นราคาแพ็กเกจ)</i><br><br>
                    
                    👉 <b>ขั้นที่ 2: นำราคาชุด ไปคูณจำนวนนักเรียน</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;มีนักเรียน <span style='color:#e74c3c;'>{people}</span> คน ต้องการคนละ 1 ชุด ➔ ต้องใช้ <b style='color:#27ae60;'>เครื่องหมายคูณ (×)</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;สมการ: <span style='color:#e74c3c;'>{people}</span> <b style='color:#27ae60;'>×</b> <span style='color:#8e44ad;'>{total_per_person}</span><br><br>
                    
                    👉 <b>ขั้นที่ 3: คูณเลข</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;{people} × {total_per_person} = <b><span style='color:#c0392b;'>{total_all:,}</span> บาท</b><br><br>
                    <b>ตอบ: คุณครูต้องใช้งบประมาณทั้งหมด {total_all:,} บาท</b></span>"""




# ================= หมวดที่ 1: รากฐานตัวเลขและการดำเนินการ (ป.5) =================
            elif actual_sub_t == "ทฤษฎีจำนวน (จำนวนเฉพาะ, ตัวประกอบ, สมบัติการหารลงตัว)":
                # สุ่ม 3 สถานการณ์: การหาตัวประกอบ (ชีวิตประจำวัน), จำนวนเฉพาะ (รหัสลับ), กฎการหารลงตัว (ข้อสอบแข่งขัน)
                scenario = random.choice(["factors_grouping", "prime_passcode", "divisibility_rule"])

                if scenario == "factors_grouping":
                    # สไตล์ที่ 1: การหาตัวประกอบทั้งหมด (ประยุกต์กับการจัดของ)
                    # เลือกตัวเลขที่มีตัวประกอบเยอะๆ เพื่อให้เด็กฝึกหาคู่คูณ
                    target_num = random.choice([24, 30, 36, 40, 48, 60])
                    items = random.choice(["คุกกี้", "ลูกอม", "โดนัท", "ส้ม", "หนังสือ"])
                    
                    # หาตัวประกอบทั้งหมด
                    factors = []
                    for i in range(1, target_num + 1):
                        if target_num % i == 0:
                            factors.append(i)
                    
                    ways = len(factors)
                    factors_str = ", ".join(map(str, factors))
                    
                    # สร้างคู่คูณเพื่อแสดงในเฉลย
                    pairs_html = ""
                    for i in range(ways // 2):
                        pairs_html += f"&nbsp;&nbsp;&nbsp;&nbsp;• แบ่งกล่องละ <span style='color:#e74c3c;'>{factors[i]}</span> ชิ้น จะได้ <span style='color:#2980b9;'>{factors[-(i+1)]}</span> กล่อง (เพราะ {factors[i]} × {factors[-(i+1)]} = {target_num})<br>"
                    if ways % 2 != 0: # กรณีเป็นเลขกำลังสองสมบูรณ์ เช่น 36
                        mid = factors[ways//2]
                        pairs_html += f"&nbsp;&nbsp;&nbsp;&nbsp;• แบ่งกล่องละ <span style='color:#e74c3c;'>{mid}</span> ชิ้น จะได้ <span style='color:#2980b9;'>{mid}</span> กล่อง (เพราะ {mid} × {mid} = {target_num})<br>"

                    q = f"ร้านเบเกอรี่อบ <b>{items}ได้ทั้งหมด {target_num} ชิ้น</b> <br>ต้องการนำ{items}ทั้งหมดมา <b>แบ่งใส่กล่อง กล่องละเท่าๆ กัน โดยไม่ให้มี{items}เหลือเศษเลย</b> <br>เจ้าของร้านจะมีวิธีเลือก <b>'จำนวนชิ้นในแต่ละกล่อง'</b> ที่แตกต่างกันได้ทั้งหมดกี่วิธี? (ใส่ได้ตั้งแต่กล่องละ 1 ชิ้น จนถึงใส่กล่องเดียวรวด)"

                    sol = f"""<span style='color:#2c3e50; line-height: 1.8;'>
                    <div style='background-color:#fcf3cf; border-left:4px solid #f1c40f; padding:15px; margin-bottom:15px; border-radius:8px;'>
                    💡 <b>การแปลภาษาไทย เป็น "สมการคณิตศาสตร์":</b><br>
                    • <b>"แบ่งใส่กล่อง กล่องละเท่าๆ กัน"</b> ➔ คือการแบ่งกลุ่ม ซึ่งต้องใช้ <b style='color:#d35400;'>เครื่องหมายหาร (÷)</b><br>
                    • <b>"โดยไม่ให้มีเศษเหลือเลย"</b> ➔ แปลว่าการหารนั้นต้องเป็น <b>"การหารลงตัว"</b><br>
                    🔥 <b>สรุป:</b> โจทย์ข้อนี้กำลังสั่งให้เราหา <b>"ตัวประกอบทั้งหมดของ {target_num}"</b> นั่นเอง! (ตัวประกอบ คือ ตัวเลขทุกตัวที่สามารถนำไปหาร {target_num} ได้ลงตัวพอดี)
                    <br>
                    </div>
                    <b>วิธีทำอย่างละเอียดแบบ Step-by-step:</b><br>
                    👉 <b>ขั้นที่ 1: ใช้เทคนิค "จับคู่คูณ" (Factor Rainbow)</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;เราจะหาว่า "เลขอะไรสองตัวคูณกันแล้วได้ <span style='color:#8e44ad;'>{target_num}</span> บ้าง?" โดยเริ่มไล่จากแม่ 1 ขึ้นไปเรื่อยๆ:<br>
                    {pairs_html}<br>
                    
                    👉 <b>ขั้นที่ 2: นำตัวเลขมาเรียงลำดับ</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;เมื่อนำตัวเลขทั้งหมดที่เราหาได้มาเรียงจากน้อยไปมาก จะได้แก่: <b><span style='color:#27ae60;'>{factors_str}</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;<i>(ตัวเลขเหล่านี้แหละ คือจำนวนชิ้นที่เราสามารถจัดใส่กล่องได้โดยไม่มีเศษ)</i><br><br>
                    
                    👉 <b>ขั้นที่ 3: นับจำนวนวิธี</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;เมื่อนับดูแล้ว พบว่ามีตัวเลขทั้งหมด <b><span style='color:#c0392b;'>{ways}</span> ตัว</b><br><br>
                    <b>ตอบ: เจ้าของร้านมีวิธีเลือกจำนวนชิ้นใส่กล่องได้ทั้งหมด {ways} วิธี</b></span>"""

                elif scenario == "prime_passcode":
                    # สไตล์ที่ 2: จำนวนเฉพาะ (แนวข้อสอบเชาวน์/รหัสลับ)
                    ranges = [(10, 30), (20, 40), (30, 50)]
                    start_num, end_num = random.choice(ranges)
                    
                    def is_prime(n):
                        if n <= 1: return False
                        for i in range(2, int(n**0.5) + 1):
                            if n % i == 0: return False
                        return True
                        
                    primes = [p for p in range(start_num, end_num + 1) if is_prime(p)]
                    primes_str = " + ".join(map(str, primes))
                    final_sum = sum(primes)
                    
                    q = f"นักสืบจิ๋วต้องถอดรหัสผ่านเพื่อเปิดตู้เซฟ โดยมีคำใบ้ทิ้งไว้ว่า:<br><div style='text-align:center; font-size:22px; font-weight:bold; background:#f8f9fa; padding:15px; border-radius:10px; border:2px dashed #bdc3c7; margin: 10px 0;'>รหัสผ่าน คือ 'ผลรวม' ของ <span style='color:#e74c3c;'>จำนวนเฉพาะ (Prime Numbers)</span><br>ที่อยู่ตั้งแต่ {start_num} ถึง {end_num}</div><br>จงหาว่ารหัสผ่านของตู้เซฟนี้คือหมายเลขใด?"

                    sol = f"""<span style='color:#2c3e50; line-height: 1.8;'>
                    <div style='background-color:#e8f8f5; border-left:4px solid #1abc9c; padding:15px; margin-bottom:15px; border-radius:8px;'>
                    💡 <b>ทบทวนความจำเรื่อง "จำนวนเฉพาะ":</b><br>
                    <b>จำนวนเฉพาะ</b> คือ ตัวเลขที่มีแค่ <b>1 และตัวมันเอง</b> เท่านั้นที่หารมันลงตัว (พูดง่ายๆ คือไม่มีสูตรคูณแม่ไหนสร้างมันขึ้นมาได้เลย ยกเว้นแม่ 1)<br>
                    <i>ตัวอย่าง: 7 เป็นจำนวนเฉพาะ เพราะมีแค่ 1 กับ 7 ที่หารลงตัว (ไม่มีเลขอื่นคูณกันได้ 7)</i><br>
                    <br>
                    </div>
                    
                    <div style='background-color:#fcf3cf; border-left:4px solid #f1c40f; padding:15px; margin-bottom:15px; border-radius:8px;'>
                    💡 <b>การแปลภาษาไทย เป็น "สมการคณิตศาสตร์":</b><br>
                    • คำว่า <b>"ผลรวม"</b> ➔ คือการนำตัวเลขทุกตัวมากองรวมกัน ต้องเชื่อมด้วย <b style='color:#3498db;'>เครื่องหมายบวก (+)</b>
                    </div>

                    <b>วิธีทำอย่างละเอียดแบบ Step-by-step:</b><br>
                    👉 <b>ขั้นที่ 1: ค้นหาจำนวนเฉพาะตั้งแต่ {start_num} ถึง {end_num}</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;เราจะมาคัดกรองตัวเลขกันทีละตัว ตัวไหนมีสูตรคูณแม่ 2, 3, 5, 7 หารลงตัว ให้ตัดทิ้งทันที!<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• จำนวนเฉพาะที่รอดชีวิตมาได้แก่: <b><span style='color:#e74c3c;'>{", ".join(map(str, primes))}</span></b><br><br>
                    
                    👉 <b>ขั้นที่ 2: สร้างสมการผลรวม</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;นำจำนวนเฉพาะที่หาได้ทั้งหมดมา <b style='color:#3498db;'>บวก (+)</b> กัน<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;สมการ: <span style='color:#e74c3c;'>{primes_str}</span> = ?<br><br>
                    
                    👉 <b>ขั้นที่ 3: คิดเลขหาคำตอบ</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;เมื่อนำตัวเลขทั้งหมดมาบวกกัน จะได้ผลลัพธ์คือ <b><span style='color:#c0392b;'>{final_sum}</span></b><br><br>
                    <b>ตอบ: รหัสผ่านของตู้เซฟนี้คือ {final_sum}</b></span>"""

                else:
                    # สไตล์ที่ 3: สมบัติการหารลงตัว (ข้อสอบแข่งขันยอดฮิต)
                    # กฎของแม่ 9: เลขโดดทุกตัวบวกกันต้องหารด้วย 9 ลงตัว
                    rule_num = random.choice([3, 9])
                    
                    # สร้างตัวเลข 4 หลัก D1 D2 A D3 (A คือตัวแปร)
                    d1 = random.randint(1, 9)
                    d2 = random.randint(0, 9)
                    d3 = random.randint(0, 9)
                    
                    # หาค่า A ที่ทำให้ (D1+D2+A+D3) หารด้วย rule_num ลงตัว
                    # สุ่มตัวเลข 0-9 มาเทส
                    possible_a = []
                    for a_test in range(10):
                        if (d1 + d2 + a_test + d3) % rule_num == 0:
                            possible_a.append(a_test)
                            
                    # เลือก A มา 1 ตัวเพื่อเป็นเฉลย
                    a_ans = random.choice(possible_a)
                    
                    # ตัวเลขเต็มๆ เพื่อแสดงตอนสรุป
                    full_number = int(f"{d1}{d2}{a_ans}{d3}")
                    
                    # ผลรวมของเลขที่รู้แล้ว
                    known_sum = d1 + d2 + d3
                    
                    # หาพหุคูณของ rule_num ที่ใกล้เคียงและมากกว่า known_sum
                    target_sum = known_sum + a_ans
                    
                    q = f"ในข้อสอบแข่งขันเข้า ม.1 มีโจทย์อยู่ว่า:<br><div style='text-align:center; font-size:22px; font-weight:bold; background:#f8f9fa; padding:15px; border-radius:10px; border:2px dashed #bdc3c7; margin: 10px 0;'>กำหนดให้ตัวเลข 4 หลัก คือ <span style='color:#2980b9;'>{d1} {d2} <b>A</b> {d3}</span><br>สามารถหารด้วย <b>แม่ {rule_num}</b> ได้ลงตัวพอดี</div><br>จงหาว่าตัวอักษร <b>A</b> สามารถเป็นเลขโดด (0-9) ตัวใดได้บ้าง? (ตอบมา 1 จำนวน)"

                    sol = f"""<span style='color:#2c3e50; line-height: 1.8;'>
                    <div style='background-color:#fdf2e9; border-left:4px solid #e67e22; padding:15px; margin-bottom:15px; border-radius:8px;'>
                    💡 <b>อาวุธลับข้อสอบแข่งขัน "กฎการหารลงตัวของแม่ {rule_num}":</b><br>
                    เราไม่จำเป็นต้องเอา {rule_num} ไปตั้งหารยาวให้เสียเวลา! กฎทางคณิตศาสตร์บอกไว้ว่า:<br>
                    <b>"ถ้านำเลขโดดทุกหลักมา <span style='color:#3498db;'>บวก (+)</span> กัน แล้วผลรวมนั้นหารด้วย {rule_num} ลงตัว... ตัวเลขชุดนั้นทั้งชุดก็จะหารด้วย {rule_num} ลงตัวด้วย!"</b>
                    <br>
                    </div>
                    <b>วิธีทำอย่างละเอียดแบบ Step-by-step:</b><br>
                    👉 <b>ขั้นที่ 1: นำเลขโดดที่รู้ค่าแล้วมาบวกกัน</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ตัวเลขที่เรามีคือ {d1}, {d2}, <b>A</b>, {d3}<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;นำตัวเลขที่รู้ค่ามา <b style='color:#3498db;'>บวก (+)</b> กัน: {d1} + {d2} + {d3} = <b><span style='color:#8e44ad;'>{known_sum}</span></b> <i>(ตัวเลขยุบรวมกันเหลือ {known_sum})</i><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ดังนั้น ผลรวมของเลขทุกหลักคือ: <b><span style='color:#8e44ad;'>{known_sum}</span> <span style='color:#3498db;'>+</span> A</b><br><br>
                    
                    👉 <b>ขั้นที่ 2: ท่องสูตรคูณแม่ {rule_num} เพื่อหาเป้าหมาย</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;เราต้องการให้ผลรวม (<span style='color:#8e44ad;'>{known_sum}</span> + A) หารด้วย {rule_num} ลงตัว <br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ลองท่องสูตรคูณแม่ {rule_num} ดูว่ามีผลลัพธ์ไหนที่ <b>"มากกว่าหรือเท่ากับ {known_sum}"</b> บ้าง<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;พหุคูณของ {rule_num} ที่เป็นไปได้คือ: {target_sum - rule_num if (target_sum - rule_num) >= known_sum else ""}, <b><span style='color:#27ae60;'>{target_sum}</span></b>, {target_sum + rule_num}...<br><br>
                    
                    👉 <b>ขั้นที่ 3: หาค่า A ด้วยการลบ (-)</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ถ้าเราอยากให้ผลรวมกลายเป็น <b><span style='color:#27ae60;'>{target_sum}</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;เราต้องหาว่า ขาดอีกเท่าไหร่ถึงจะถึง {target_sum}? ซึ่งคิดได้จากการนำเป้าหมาย <b style='color:#c0392b;'>ลบ (-)</b> ด้วยของที่มีอยู่<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;สมการ: A = <span style='color:#27ae60;'>{target_sum}</span> <b style='color:#c0392b;'>-</b> <span style='color:#8e44ad;'>{known_sum}</span> = <b><span style='color:#c0392b;'>{a_ans}</span></b><br><br>
                    
                    <i>(ตรวจคำตอบ: ถ้า A = {a_ans} ตัวเลขคือ {full_number} ซึ่ง {full_number} ÷ {rule_num} = {full_number // rule_num} ลงตัวเป๊ะ!)</i><br><br>
                    <b>ตอบ: A สามารถเป็นเลข {a_ans} ได้</b></span>"""




# ================= หมวดที่ 1: รากฐานตัวเลขและการดำเนินการ (ป.5) =================
            elif actual_sub_t == "ระบบเลขฐานต่างๆ เบื้องต้น":
                scenario = random.choice(["base2_to_10", "base10_to_other", "base_compare"])

                if scenario == "base2_to_10":
                    # สไตล์ที่ 1: แปลงเลขฐาน 2 เป็นฐาน 10 (แกะกล่องของหุ่นยนต์)
                    length = random.choice([4, 5])
                    binary_str = "1" + "".join([random.choice(["0", "1"]) for _ in range(length - 1)])
                    decimal_val = int(binary_str, 2)
                    
                    # สร้างตารางกล่องใส่ของให้เด็กเห็นภาพ
                    box_html = "<table style='width:100%; text-align:center; border-collapse:collapse; margin: 10px 0; font-size:18px;'>"
                    box_html += "<tr><td colspan='{}' style='background-color:#2c3e50; color:white; padding:5px; border-radius:5px 5px 0 0;'><b>ตารางขนาดกล่องของหุ่นยนต์ (ฐาน 2)</b></td></tr>".format(length)
                    
                    row1, row2, row3 = "<tr>", "<tr>", "<tr>"
                    steps_html = ""
                    powers = []
                    
                    for i in range(length):
                        power = length - 1 - i
                        digit = int(binary_str[i])
                        place_value = 2 ** power
                        val = digit * place_value
                        powers.append(val)
                        
                        # วาดตาราง
                        row1 += f"<td style='border:1px solid #bdc3c7; padding:10px; background-color:#ebf5fb;'><b>กล่องจุ {place_value} ชิ้น</b><br>(2<sup>{power}</sup>)</td>"
                        row2 += f"<td style='border:1px solid #bdc3c7; padding:10px; font-size:24px; color:#e74c3c;'><b>{digit}</b></td>"
                        row3 += f"<td style='border:1px solid #bdc3c7; padding:10px; color:#27ae60;'><b>{val}</b> ชิ้น</td>"
                        
                        # อธิบายทีละบรรทัด
                        steps_html += f"&nbsp;&nbsp;&nbsp;&nbsp;• <b>กล่องขนาด {place_value} ชิ้น:</b> มีอยู่ <span style='color:#e74c3c;'>{digit} กล่อง</span> ➔ เทของออกมาได้ {digit} × {place_value} = <b><span style='color:#27ae60;'>{val}</span> ชิ้น</b><br>"

                    row1 += "</tr>"; row2 += "</tr>"; row3 += "</tr>"
                    box_html += row1 + row2 + row3 + "</table>"
                    sum_str = " + ".join(map(str, powers))

                    q = f"หุ่นยนต์ R2D2 ส่งรหัสลับเป็นตัวเลข <b>{binary_str}<sub>2</sub></b> (อ่านว่า เลขฐานสอง) <br>จงแปลรหัสนี้ให้กลับมาเป็น <b>'เลขฐานสิบ' (ตัวเลขปกติที่มนุษย์ใช้)</b> เพื่อให้เราอ่านรู้เรื่อง"

                    sol = f"""<span style='color:#2c3e50; line-height: 1.8;'>
                    <div style='background-color:#fcf3cf; border-left:4px solid #f1c40f; padding:15px; margin-bottom:15px; border-radius:8px;'>
                    💡 <b>ปูพื้นฐาน: ทำไมมนุษย์ใช้ฐาน 10 แต่หุ่นยนต์ใช้ฐาน 2?</b><br>
                    • มนุษย์มี 10 นิ้ว เวลาเรานับของ เราจะจัดกล่องทีละ 10 (กล่องหลักหน่วย, หลักสิบ, หลักร้อย...)<br>
                    • แต่หุ่นยนต์มีแค่ <b>สวิตช์เปิด (1) กับ สวิตช์ปิด (0)</b> หุ่นยนต์เลยต้องจัดกล่องทีละ 2 (กล่องหลัก 1, กล่องจุ 2, กล่องจุ 4, กล่องจุ 8...)<br>
                                        </div>
                    
                    <div style='background-color:#e8f8f5; border-left:4px solid #1abc9c; padding:15px; margin-bottom:15px; border-radius:8px;'>
                    🧠 <b>การแปลเป็น "สมการคณิตศาสตร์":</b><br>
                    โจทย์ให้เลข <b>{binary_str}<sub>2</sub></b> มา ให้เรานึกภาพว่ามันคือ <b>"จำนวนกล่อง"</b> ที่หุ่นยนต์แพ็กของส่งมาให้เรา!<br>
                    • <b>ขั้นแรก:</b> เราต้อง <b>"เปิดกล่อง (Unpack)"</b> แต่ละใบดูว่ามีของอยู่กี่ชิ้น โดยใช้ <b style='color:#e74c3c;'>เครื่องหมายคูณ (×)</b><br>
                    • <b>ขั้นที่สอง:</b> เราต้องเทของทั้งหมดมากองรวมกันบนพื้นมนุษย์ โดยใช้ <b style='color:#3498db;'>เครื่องหมายบวก (+)</b>
                    </div>

                    <b>วิธีทำอย่างละเอียดแบบ Step-by-step:</b><br>
                    👉 <b>ขั้นที่ 1: สร้างตารางขนาดกล่อง (เริ่มจากขวาสุดคือกล่องละ 1 ชิ้น แล้วคูณ 2 ไปเรื่อยๆ ทางซ้าย)</b><br>
                    {box_html}<br>
                    
                    👉 <b>ขั้นที่ 2: แกะกล่องทีละใบ (นำตัวเลขไปคูณขนาดกล่อง)</b><br>
                    {steps_html}<br>
                    
                    👉 <b>ขั้นที่ 3: เทของทุกกล่องมารวมกัน (บวก)</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;นำของที่เราแกะได้จากทุกกล่องมา <b style='color:#3498db;'>บวก (+)</b> รวมกัน<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;สมการ: {sum_str} = <b><span style='color:#8e44ad;'>{decimal_val}</span></b><br><br>
                    
                    <b>ตอบ: รหัสหุ่นยนต์ {binary_str}<sub>2</sub> มีค่าเท่ากับ {decimal_val} ชิ้นในโลกมนุษย์</b></span>"""

                elif scenario == "base10_to_other":
                    # สไตล์ที่ 2: แปลงฐาน 10 เป็นฐานอื่นๆ (จัดของลงกล่องมนุษย์ต่างดาว)
                    base_target = random.choice([4, 5])
                    planet = "ควินโต (Quinto)" if base_target == 5 else "ควอดรา (Quadra)"
                    decimal_val = random.randint(35, 95)
                    
                    steps = []
                    current = decimal_val
                    while current > 0:
                        rem = current % base_target
                        quotient = current // base_target
                        steps.append((current, quotient, rem))
                        current = quotient
                        
                    base_str = "".join([str(s[2]) for s in steps[::-1]])
                    
                    div_html = ""
                    labels = ["ชิ้นย่อย (เศษที่ใส่ถุงไม่ได้)", "ถุงเล็ก (เศษที่ใส่ลังไม่ได้)", "ลังใหญ่"]
                    for i, s in enumerate(steps):
                        label = labels[i] if i < len(labels) else f"กล่องไซส์ {i+1}"
                        div_html += f"&nbsp;&nbsp;&nbsp;&nbsp;• นำของ <span style='color:#2980b9;'>{s[0]}</span> ชิ้น มาจัดกลุ่มละ {base_target} ชิ้น ➔ {s[0]} ÷ {base_target} = ได้ <b><span style='color:#2980b9;'>{s[1]}</span> กลุ่ม</b> <b style='color:#c0392b;'>(เหลือเศษ {s[2]})</b><br>"
                        div_html += f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i>*เศษ <span style='color:#c0392b;'>{s[2]}</span> ตัวนี้คือ '{label}' ที่จะถูกเขียนเป็นเลขประจำหลักที่ {i+1} นับจากขวา</i><br><br>"

                    q = f"คุณแม่ซื้อแอปเปิ้ลมาทั้งหมด <b>{decimal_val} ผล</b> <br>บังเอิญมนุษย์ต่างดาวจากดาว{planet}มาเยี่ยมบ้าน พวกเขามีนิ้วมือแค่ {base_target} นิ้ว จึงนับของด้วย <b>'ระบบเลขฐาน {base_target}'</b> (คือจัดของเป็นกลุ่มละ {base_target} ชิ้นเท่านั้น) <br>มนุษย์ต่างดาวจะจดบันทึกจำนวนแอปเปิ้ล <b>{decimal_val} ผล</b> ให้เป็นเลขฐาน {base_target} ได้ว่าอย่างไร?"

                    sol = f"""<span style='color:#2c3e50; line-height: 1.8;'>
                    <div style='background-color:#e8f8f5; border-left:4px solid #1abc9c; padding:15px; margin-bottom:15px; border-radius:8px;'>
                    💡 <b>การแปลเป็น "สมการคณิตศาสตร์":</b><br>
                    • มนุษย์ต่างดาวไม่รู้จักเลข {decimal_val} เพราะพวกเขาจัดของใส่ถุง <b>"ถุงละ {base_target} ชิ้น"</b> เท่านั้น!<br>
                    • <b>"การจัดของใส่ถุงให้เท่าๆ กัน"</b> ➔ เราต้องใช้ <b style='color:#d35400;'>เครื่องหมายหาร (÷)</b> (ใช้วิธีหารสั้น)<br>
                    • <b>"ของที่ล้นถุง (เศษเหลือ)"</b> ➔ ของที่ยัดลงถุงไม่ได้ จะถูกวางไว้ข้างนอก และมันก็คือ <b>ตัวเลขในแต่ละหลัก</b> ของเลขฐานนั่นเอง!
                    <br>                    </div>
                    <b>วิธีทำอย่างละเอียดแบบ Step-by-step (เทคนิคหารจัดกลุ่มแล้วเก็บเศษ):</b><br>
                    👉 <b>ขั้นที่ 1: จัดแอปเปิ้ลลงถุง โดยใช้ <span style='color:#e74c3c;'>แม่ {base_target}</span> หารไปเรื่อยๆ จนกว่าจะไม่เหลือของให้จัด</b><br>
                    {div_html}
                    
                    👉 <b>ขั้นที่ 2: นำ 'เศษ' ที่ล้นถุงออกมาเขียนเรียงกันเป็นเลขฐาน</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;กฎเหล็กคือ: <b>ต้องอ่านเศษจากล่างขึ้นบน!</b> (เพราะเศษตัวสุดท้ายคือกล่องใบใหญ่ที่สุด ต้องอยู่หลักซ้ายมือสุด ส่วนเศษตัวแรกคือแอปเปิ้ลลูกเดี่ยวๆ ต้องอยู่ขวาสุด)<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;เรียงเศษจากล่างขึ้นบน: <b><span style='color:#27ae60;'>{" , ".join([str(s[2]) for s in steps[::-1]])}</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;นำมาเขียนติดกัน จะได้เป็น <b><span style='color:#8e44ad;'>{base_str}</span></b><br><br>
                    
                    <b>ตอบ: แอปเปิ้ล {decimal_val} ผล เขียนเป็นเลขฐาน {base_target} ได้คือ {base_str}<sub>{base_target}</sub></b></span>"""

                else:
                    # สไตล์ที่ 3: เปรียบเทียบจำนวนต่างฐาน (อัปเกรดความละเอียดขั้นสุด)
                    base_a = 2
                    base_b = 5
                    
                    dec_a = random.randint(15, 25)
                    dec_b = dec_a + random.randint(3, 8)
                    
                    def to_base(n, b):
                        if n == 0: return "0"
                        res = ""
                        while n > 0:
                            res = str(n % b) + res
                            n //= b
                        return res
                        
                    str_a = to_base(dec_a, base_a)
                    str_b = to_base(dec_b, base_b)
                    
                    diff_dec = dec_b - dec_a

                    # สร้างขั้นตอนกระจายเลขฐาน A
                    steps_a_html = ""
                    powers_a = []
                    len_a = len(str_a)
                    for i in range(len_a):
                        power = len_a - 1 - i
                        digit = int(str_a[i])
                        place_val = base_a ** power
                        val = digit * place_val
                        powers_a.append(val)
                        steps_a_html += f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• นำเลข <span style='color:#e74c3c;'>{digit}</span> × ขนาดกล่อง {place_val} = <b>{val}</b><br>"
                    sum_a_str = " + ".join(map(str, powers_a))

                    # สร้างขั้นตอนกระจายเลขฐาน B
                    steps_b_html = ""
                    powers_b = []
                    len_b = len(str_b)
                    for i in range(len_b):
                        power = len_b - 1 - i
                        digit = int(str_b[i])
                        place_val = base_b ** power
                        val = digit * place_val
                        powers_b.append(val)
                        steps_b_html += f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• นำเลข <span style='color:#e74c3c;'>{digit}</span> × ขนาดกล่อง {place_val} = <b>{val}</b><br>"
                    sum_b_str = " + ".join(map(str, powers_b))
                    
                    q = f"มีกล่องสมบัติ 2 ใบ เขียนรหัสจำนวนเหรียญทองติดไว้หน้ากล่องดังนี้:<br>&nbsp;&nbsp;• กล่องใบที่ 1: <b>{str_a}<sub>{base_a}</sub></b> เหรียญ<br>&nbsp;&nbsp;• กล่องใบที่ 2: <b>{str_b}<sub>{base_b}</sub></b> เหรียญ<br>จงหาว่า <b>กล่องใบใดมีเหรียญทองอยู่จริงบนโลกมนุษย์ (ฐาน 10) มากกว่ากัน? และมากกว่าอยู่กี่เหรียญ?</b>"

                    sol = f"""<span style='color:#2c3e50; line-height: 1.8;'>
                    <div style='background-color:#fdf2e9; border-left:4px solid #e67e22; padding:15px; margin-bottom:15px; border-radius:8px;'>
                    💡 <b>ข้อควรระวัง (กับดักคณิตศาสตร์):</b><br>
                    เรา <b>"ห้าม"</b> นำเลขต่างฐานมาบวกลบกันตรงๆ เด็ดขาด! (เลข {str_a} ดูเยอะกว่าก็จริง แต่มันเป็นฐาน {base_a} ซึ่งกล่องมีขนาดเล็กนิดเดียว) <br>
                    วิธีที่ถูกต้องคือ ต้อง <b>"เทของออกจากกล่อง" (คูณค่าประจำหลักทีละตัว)</b> ให้กลายเป็น <b>เลขมนุษย์ (ฐาน 10)</b> ก่อน แล้วค่อยนำมา <b style='color:#c0392b;'>ลบ (-)</b> เพื่อหาความต่าง
                    </div>
                    <b>วิธีทำอย่างละเอียดแบบ Step-by-step:</b><br>
                    👉 <b>ขั้นที่ 1: แกะกล่องใบที่ 1 (แปลง {str_a} ฐาน {base_a} ➔ ฐาน 10)</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;เราจะนำตัวเลขทีละหลัก (จากซ้ายไปขวา) มา <b style='color:#e74c3c;'>คูณ (×)</b> กับขนาดของกล่องฐาน {base_a} (คือ 1, {base_a}, {base_a**2}, {base_a**3}...)<br>
                    {steps_a_html}
                    &nbsp;&nbsp;&nbsp;&nbsp;เมื่อนำของที่เทออกมาได้ทั้งหมดมา <b style='color:#3498db;'>บวก (+)</b> รวมกัน:<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;สมการ: {sum_a_str} = <b><span style='color:#2980b9;'>{dec_a}</span> เหรียญ</b><br><br>
                    
                    👉 <b>ขั้นที่ 2: แกะกล่องใบที่ 2 (แปลง {str_b} ฐาน {base_b} ➔ ฐาน 10)</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;เราจะนำตัวเลขทีละหลัก มา <b style='color:#e74c3c;'>คูณ (×)</b> กับขนาดของกล่องฐาน {base_b} (คือ 1, {base_b}, {base_b**2}...)<br>
                    {steps_b_html}
                    &nbsp;&nbsp;&nbsp;&nbsp;เมื่อนำของที่เทออกมาได้ทั้งหมดมา <b style='color:#3498db;'>บวก (+)</b> รวมกัน:<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;สมการ: {sum_b_str} = <b><span style='color:#27ae60;'>{dec_b}</span> เหรียญ</b><br><br>
                    
                    👉 <b>ขั้นที่ 3: เปรียบเทียบและหาความต่าง</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• หีบใบที่ 1 มีของจริง <span style='color:#2980b9;'>{dec_a}</span> เหรียญ<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• หีบใบที่ 2 มีของจริง <span style='color:#27ae60;'>{dec_b}</span> เหรียญ<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;เห็นชัดเจนว่า <b>หีบใบที่ 2 มีมากกว่า!</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;หาว่ามากกว่าอยู่เท่าไหร่ โดยนำมา <b style='color:#c0392b;'>ลบ (-)</b> กัน ➔ <span style='color:#27ae60;'>{dec_b}</span> - <span style='color:#2980b9;'>{dec_a}</span> = <b><span style='color:#c0392b;'>{diff_dec}</span> เหรียญ</b><br><br>
                    <b>ตอบ: หีบใบที่ 2 มีเหรียญทองมากกว่า และมากกว่าอยู่ {diff_dec} เหรียญ</b></span>"""





# ================= หมวดที่ 1: รากฐานตัวเลขและการดำเนินการ (ป.5) =================
            elif actual_sub_t == "โจทย์ปัญหา ห.ร.ม. และ ค.ร.น. (แบ่งของ, นาฬิกาปลุก)":
                # สุ่ม 6 สถานการณ์ครอบคลุมทุกสนามสอบแข่งขัน พร้อมขยายฐานข้อมูลสุ่มแบบจัดเต็ม!
                scenario = random.choice([
                    "gcd_sharing", "lcm_clocks", "gcd_tiles", "lcm_running", 
                    "gcd_remainder", "lcm_remainder"
                ])

                # ฐานข้อมูลตัวละครและสถานที่เพื่อความหลากหลาย
                names_pool = ["คุณครูใจดี", "ลุงชัย", "ป้าสมศรี", "พี่อาร์ม", "เจ้าของร้าน", "ชาวสวน", "ผู้จัดการ", "เชฟเบเกอรี่"]
                kids_names = ["พายุ", "สายฟ้า", "ต้นกล้า", "ตะวัน", "ภูผา", "ใบบัว", "ข้าวหอม", "มะลิ", "น้ำใส"]
                places_pool = ["สวนสาธารณะ", "สนามกีฬา", "ลานกีฬา", "ทะเลสาบ", "สวนลุมพินี"]
                vehicles_pool = ["วิ่ง", "ปั่นจักรยาน", "ขับรถโกคาร์ท", "พายเรือ"]

                if scenario == "gcd_sharing":
                    # [สไตล์ 1: ห.ร.ม. แบ่งของ - สุ่มเซ็ตสิ่งของให้เข้ากัน]
                    item_sets = [
                        ("ดอกกุหลาบ", "ดอกทานตะวัน", "ดอกมะลิ", "ดอก"),
                        ("ลูกปัดสีแดง", "ลูกปัดสีฟ้า", "ลูกปัดสีเขียว", "เม็ด"),
                        ("คุกกี้เนย", "คุกกี้ช็อกโกแลต", "คุกกี้สตรอว์เบอร์รี", "ชิ้น"),
                        ("ขนมจีบ", "ซาลาเปา", "ฮะเก๋า", "ลูก"),
                        ("เสื้อยืดสีดำ", "เสื้อยืดสีขาว", "เสื้อยืดสีเทา", "ตัว")
                    ]
                    selected_set = random.choice(item_sets)
                    item1, item2, item3, unit = selected_set
                    person = random.choice(names_pool)
                    
                    # สุ่มตัวเลข ห.ร.ม. ให้หลากหลายขึ้น (4 ถึง 25)
                    gcd_target = random.choice([4, 5, 6, 8, 10, 12, 15, 20, 25])
                    m1, m2, m3 = random.sample([2, 3, 5, 7, 11], 3)
                    n1, n2, n3 = gcd_target * m1, gcd_target * m2, gcd_target * m3
                    
                    divisors = []
                    current_nums = [n1, n2, n3]
                    steps_html = ""
                    temp_gcd = gcd_target
                    for p in [2, 3, 5, 7, 11]:
                        while temp_gcd % p == 0:
                            divisors.append(p)
                            next_nums = [x // p for x in current_nums]
                            steps_html += f"<tr><td style='border-right: 2px solid #2c3e50; border-bottom: 2px solid #2c3e50; padding: 5px 15px; color:#c0392b; font-weight:bold; text-align:right;'>{p}</td>"
                            steps_html += f"<td style='border-bottom: 2px solid #2c3e50; padding: 5px 15px; text-align:center;'><span style='color:#3498db;'>{current_nums[0]}</span>, <span style='color:#3498db;'>{current_nums[1]}</span>, <span style='color:#3498db;'>{current_nums[2]}</span></td></tr>"
                            current_nums = next_nums
                            temp_gcd //= p
                    
                    steps_html += f"<tr><td></td><td style='padding: 5px 15px; text-align:center; font-weight:bold; color:#27ae60; border-bottom: 4px double #27ae60;'>{current_nums[0]}, {current_nums[1]}, {current_nums[2]}</td></tr>"
                    total_items_per_bag = sum(current_nums)

                    q = f"{person}มี{item1} <b>{n1} {unit}</b>, {item2} <b>{n2} {unit}</b> และ{item3} <b>{n3} {unit}</b> <br>ต้องการจัดของเหล่านี้ใส่ตะกร้า <b>ตะกร้าละเท่าๆ กัน โดยไม่ปะปนกัน และไม่มีของเหลือเศษ</b> <br>จงหาว่า{person}จะจัดได้ <b>มากที่สุดกี่ตะกร้า</b> และแต่ละตะกร้ามีของกี่{unit}?"

                    sol = f"""<span style='color:#2c3e50; line-height: 1.8;'>
                    <div style='background-color:#fcf3cf; border-left:4px solid #f1c40f; padding:15px; margin-bottom:15px; border-radius:8px;'>
                    💡 <b>การแปลภาษาไทย เป็น "สมการคณิตศาสตร์":</b><br>
                    • <b>"แบ่งใส่ตะกร้า ตะกร้าละเท่าๆ กัน"</b> ➔ การแบ่งกลุ่มย่อยๆ ที่เท่ากัน ต้องใช้ <b style='color:#d35400;'>เครื่องหมายหาร (÷)</b><br>
                    • <b>"ไม่มีเศษ"</b> ➔ ต้องเป็น <b>การหารลงตัว</b><br>
                    • <b>"มากที่สุด"</b> ➔ คือการหาค่าที่มากที่สุด (Greatest)<br>
                    🔥 <b>สรุป:</b> หาร + ลงตัว + มากที่สุด = หา <b>ห.ร.ม. (หาร่วมมาก)</b><br>
                    
                    </div>
                    <b>วิธีทำอย่างละเอียดแบบ Step-by-step:</b><br>
                    👉 <b>ขั้นที่ 1: ตั้งหารสั้นเพื่อหา ห.ร.ม.</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;<i>หา 'แม่สูตรคูณ' ที่หารเลขทั้ง 3 ตัวลงตัวพร้อมกัน เพื่อดึงตัวร่วมออกมา</i><br>
                    <table style='margin: 10px 40px; font-size: 20px; border-collapse: collapse;'>{steps_html}</table>
                    
                    👉 <b>ขั้นที่ 2: สรุปผล ห.ร.ม. (จำนวนตะกร้า)</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;นำตัวหารด้านหน้า (<span style='color:#c0392b;'>สีแดง</span>) มา <b style='color:#e74c3c;'>คูณ (×)</b> กัน ➔ {" × ".join(map(str, divisors))} = <b><span style='color:#c0392b;'>{gcd_target}</span> ตะกร้า</b><br>
                    
                    👉 <b>ขั้นที่ 3: หาจำนวน{unit}ในแต่ละตะกร้า (ดูเศษด้านล่าง)</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ตัวเลขบรรทัดล่างสุด (<span style='color:#27ae60;'>สีเขียว</span>) คือจำนวนของแต่ละชนิดใน 1 ตะกร้า:<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• {item1} <span style='color:#27ae60;'>{current_nums[0]}</span> {unit}, {item2} <span style='color:#27ae60;'>{current_nums[1]}</span> {unit}, {item3} <span style='color:#27ae60;'>{current_nums[2]}</span> {unit}<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;รวมใน 1 ตะกร้ามีของ = <span style='color:#27ae60;'>{current_nums[0]}</span> + <span style='color:#27ae60;'>{current_nums[1]}</span> + <span style='color:#27ae60;'>{current_nums[2]}</span> = <b><span style='color:#8e44ad;'>{total_items_per_bag}</span> {unit}</b><br><br>
                    <b>ตอบ: จัดได้มากที่สุด {gcd_target} ตะกร้า ตะกร้าละ {total_items_per_bag} {unit}</b></span>"""

                elif scenario == "lcm_clocks":
                    # [สไตล์ 2: ค.ร.น. เหตุการณ์ที่เกิดซ้ำๆ (นาฬิกา, รถบัส, น้ำพุ)]
                    event_types = [
                        ("นาฬิกาปลุก 3 เรือน", "ดังทุกๆ", "ดังพร้อมกัน", "เรือน"),
                        ("รถโดยสาร 3 สาย", "ออกจากสถานีทุกๆ", "ออกพร้อมกัน", "สาย"),
                        ("น้ำพุเต้นระบำ 3 จุด", "พ่นน้ำทุกๆ", "พ่นน้ำพร้อมกัน", "จุด"),
                        ("ประภาคาร 3 แห่ง", "ส่องไฟวาบทุกๆ", "ส่องไฟพร้อมกัน", "แห่ง")
                    ]
                    event, verb_repeat, verb_together, unit_noun = random.choice(event_types)
                    
                    # ขยายเป้าหมาย ค.ร.น. ให้ยากขึ้น
                    lcm_target = random.choice([60, 120, 180, 240, 300, 360])
                    
                    # สุ่มตัวประกอบ 3 ตัวที่ทำให้เกิด ค.ร.น. นี้
                    valid_triplets = []
                    if lcm_target == 60: valid_triplets = [(10,15,20), (12,15,20), (15,20,30)]
                    elif lcm_target == 120: valid_triplets = [(15,24,40), (20,30,40), (24,30,40)]
                    elif lcm_target == 180: valid_triplets = [(20,36,45), (30,45,60), (36,45,60)]
                    elif lcm_target == 240: valid_triplets = [(30,48,80), (40,60,80), (48,60,80)]
                    elif lcm_target == 300: valid_triplets = [(25,50,60), (30,50,75), (50,60,75)]
                    else: valid_triplets = [(40,72,90), (60,72,90), (45,60,120)]
                    
                    t1, t2, t3 = random.choice(valid_triplets)
                        
                    start_h = random.randint(6, 12)
                    start_m = random.choice([0, 15, 30, 45])
                    start_time_str = f"{start_h:02d}:{start_m:02d}"
                    
                    divisors = []
                    current_nums = [t1, t2, t3]
                    steps_html = ""
                    running = True
                    while running:
                        divided_in_this_step = False
                        for p in [2, 3, 5, 7]:
                            if sum(1 for x in current_nums if x % p == 0) >= 2:
                                divisors.append(p)
                                steps_html += f"<tr><td style='border-right: 2px solid #2c3e50; border-bottom: 2px solid #2c3e50; padding: 5px 15px; color:#c0392b; font-weight:bold; text-align:right;'>{p}</td>"
                                steps_html += f"<td style='border-bottom: 2px solid #2c3e50; padding: 5px 15px; text-align:center;'><span style='color:#3498db;'>{current_nums[0]}</span>, <span style='color:#3498db;'>{current_nums[1]}</span>, <span style='color:#3498db;'>{current_nums[2]}</span></td></tr>"
                                current_nums = [x // p if x % p == 0 else x for x in current_nums]
                                divided_in_this_step = True
                                break 
                        if not divided_in_this_step:
                            running = False
                            
                    steps_html += f"<tr><td></td><td style='padding: 5px 15px; text-align:center; font-weight:bold; color:#27ae60; border-bottom: 4px double #27ae60;'>{current_nums[0]}, {current_nums[1]}, {current_nums[2]}</td></tr>"
                    hours_add = lcm_target // 60
                    total_mins = start_h * 60 + start_m + lcm_target
                    end_time_str = f"{(total_mins // 60) % 24:02d}:{total_mins % 60:02d}"

                    q = f"{event} {verb_repeat} <b>{t1} นาที, {t2} นาที และ {t3} นาที</b> ตามลำดับ <br>ถ้าทั้งสาม{unit_noun} <b>{verb_together}ครั้งแรกเวลา {start_time_str} น.</b> <br>จงหาว่าเหตุการณ์นี้จะ<b>{verb_together}อีกครั้งเวลาใด?</b>"

                    sol = f"""<span style='color:#2c3e50; line-height: 1.8;'>
                    <div style='background-color:#e8f8f5; border-left:4px solid #1abc9c; padding:15px; margin-bottom:15px; border-radius:8px;'>
                    💡 <b>การแปลเป็น "สมการคณิตศาสตร์":</b><br>
                    • <b>"เกิดเหตุการณ์ซ้ำๆ ทุกๆ..."</b> ➔ เวลาบวกเพิ่มขึ้นเรื่อยๆ ทีละช่วง เป็นลักษณะของ <b>"พหุคูณ" (สูตรคูณ)</b><br>
                    • <b>"เกิดขึ้นพร้อมกันอีกครั้ง"</b> ➔ หาจุดบรรจบในอนาคตที่น้อยที่สุด ➔ ต้องใช้วิธีหา <b>ค.ร.น.</b><br>
                    
                    </div>
                    <b>วิธีทำอย่างละเอียดแบบ Step-by-step:</b><br>
                    👉 <b>ขั้นที่ 1: ตั้งหารสั้นเพื่อหา ค.ร.น.</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;<i>(กฎเหล็กของ ค.ร.น. : หารลงตัวแค่ 2 ตัว ก็ใช้แม่สูตรคูณหารต่อได้เลย! ตัวไหนหารไม่ได้ให้ชักลงมา)</i><br>
                    <table style='margin: 10px 40px; font-size: 20px; border-collapse: collapse;'>{steps_html}</table>
                    
                    👉 <b>ขั้นที่ 2: สรุปผล ค.ร.น.</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;นำตัวหาร (<span style='color:#c0392b;'>สีแดง</span>) และเศษ (<span style='color:#27ae60;'>สีเขียว</span>) <b>คูณ (×) กันเป็นรูปตัว L</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ค.ร.น. = {" × ".join(map(str, divisors))} × {" × ".join(map(str, current_nums))} = <b><span style='color:#c0392b;'>{lcm_target}</span> นาที</b><br>
                    
                    👉 <b>ขั้นที่ 3: แปลงเวลาและบวกเพิ่ม</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• <span style='color:#c0392b;'>{lcm_target}</span> นาที แปลงเป็นชั่วโมง ➔ {lcm_target} ÷ 60 = <b><span style='color:#8e44ad;'>{hours_add}</span> ชั่วโมง</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• เวลาเริ่มต้น <span style='color:#2980b9;'>{start_time_str} น.</span> <b style='color:#3498db;'>บวกเพิ่ม (+)</b> อนาคต <span style='color:#8e44ad;'>{hours_add}</span> ชั่วโมง = <b><span style='color:#d35400;'>{end_time_str} น.</span></b><br><br>
                    <b>ตอบ: จะ{verb_together}อีกครั้งเวลา {end_time_str} น.</b></span>"""

                elif scenario == "gcd_tiles":
                    # [สไตล์ 3: ห.ร.ม. กระเบื้อง/พื้นที่ - สุ่มสถานที่และวัสดุ]
                    area_types = [
                        ("ห้องโถง", "กระเบื้อง"), ("ลานกว้าง", "แผ่นหิน"), 
                        ("บอร์ดนิทรรศการ", "กระดาษสี"), ("สวนหน้าบ้าน", "แผ่นหญ้าเทียม")
                    ]
                    location, material = random.choice(area_types)
                    
                    # ขยายขนาดพื้นที่
                    gcd_val = random.choice([12, 15, 20, 25, 30, 40, 50])
                    m_w = random.choice([4, 5, 6, 7])
                    m_l = random.choice([x for x in [5, 6, 7, 8, 9, 11] if math.gcd(m_w, x) == 1])
                    width = gcd_val * m_w
                    length = gcd_val * m_l
                    
                    divisors = []
                    temp_gcd = gcd_val
                    current_nums = [width, length]
                    steps_html = ""
                    for p in [2, 3, 5]:
                        while temp_gcd % p == 0:
                            divisors.append(p)
                            next_nums = [x // p for x in current_nums]
                            steps_html += f"<tr><td style='border-right: 2px solid #2c3e50; border-bottom: 2px solid #2c3e50; padding: 5px 15px; color:#c0392b; font-weight:bold; text-align:right;'>{p}</td>"
                            steps_html += f"<td style='border-bottom: 2px solid #2c3e50; padding: 5px 15px; text-align:center;'><span style='color:#3498db;'>{current_nums[0]}</span>, <span style='color:#3498db;'>{current_nums[1]}</span></td></tr>"
                            current_nums = next_nums
                            temp_gcd //= p
                    steps_html += f"<tr><td></td><td style='padding: 5px 15px; text-align:center; font-weight:bold; color:#27ae60; border-bottom: 4px double #27ae60;'>{current_nums[0]}, {current_nums[1]}</td></tr>"
                    total_tiles = current_nums[0] * current_nums[1]

                    q = f"พื้นที่{location}รูปสี่เหลี่ยมผืนผ้า กว้าง <b>{width} เซนติเมตร</b> ยาว <b>{length} เซนติเมตร</b> <br>ช่างต้องการปู{material}รูป <b>'สี่เหลี่ยมจัตุรัส'</b> ให้เต็มพื้นที่พอดี โดยไม่ต้องตัดเศษทิ้งเลย <br>จงหาว่าช่างต้องใช้{material} <b>ขนาดใหญ่ที่สุดด้านละกี่เซนติเมตร?</b> และต้องใช้ทั้งหมด <b>กี่แผ่น?</b>"

                    sol = f"""<span style='color:#2c3e50; line-height: 1.8;'>
                    <div style='background-color:#fcf3cf; border-left:4px solid #f1c40f; padding:15px; margin-bottom:15px; border-radius:8px;'>
                    💡 <b>การแปลเป็น "สมการคณิตศาสตร์":</b><br>
                    • <b>"สี่เหลี่ยมจัตุรัส"</b> ➔ ด้านกว้างต้องเท่ากับด้านยาว หมายความว่าตัวเลขที่เราเอามาหารความกว้างและยาวของห้อง ต้องเป็น <b>"ตัวหารร่วม" (เลขเดียวกัน)</b><br>
                    • <b>"ใหญ่ที่สุด และไม่ตัดทิ้ง"</b> ➔ หา <b>ห.ร.ม.</b> ของความกว้างและความยาว<br>
                    
                    </div>
                    <b>วิธีทำอย่างละเอียดแบบ Step-by-step:</b><br>
                    👉 <b>ขั้นที่ 1: ตั้งหารสั้นเพื่อหา ห.ร.ม. ของ {width} และ {length}</b><br>
                    <table style='margin: 10px 40px; font-size: 20px; border-collapse: collapse;'>{steps_html}</table>
                    
                    👉 <b>ขั้นที่ 2: สรุปผล ห.ร.ม. (หาขนาด{material})</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;นำตัวหาร (<span style='color:#c0392b;'>สีแดง</span>) <b>คูณ (×)</b> กัน ➔ {" × ".join(map(str, divisors))} = <b><span style='color:#c0392b;'>{gcd_val}</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;<i>({material}ต้องมีขนาด กว้าง {gcd_val} ซม. x ยาว {gcd_val} ซม.)</i><br><br>
                    
                    👉 <b>ขั้นที่ 3: หาจำนวนแผ่นที่ต้องใช้</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ดูเศษด้านล่างสุด (<span style='color:#27ae60;'>สีเขียว</span>) ➔ ด้านกว้างวางได้ <span style='color:#27ae60;'>{current_nums[0]}</span> แผ่น, ด้านยาววางได้ <span style='color:#27ae60;'>{current_nums[1]}</span> แผ่น<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;หาพื้นที่รวมโดยนำมา <b style='color:#e74c3c;'>คูณ (×)</b> กัน = <span style='color:#27ae60;'>{current_nums[0]}</span> × <span style='color:#27ae60;'>{current_nums[1]}</span> = <b><span style='color:#8e44ad;'>{total_tiles}</span> แผ่น</b><br><br>
                    <b>ตอบ: {material}ขนาดด้านละ {gcd_val} ซม. จำนวน {total_tiles} แผ่น</b></span>"""

                elif scenario == "lcm_running":
                    # [สไตล์ 4: ค.ร.น. วงโคจร (วิ่ง, ขับรถ) - สุ่มตัวละครและสถานที่]
                    place = random.choice(places_pool)
                    vehicle = random.choice(vehicles_pool)
                    name1, name2, name3 = random.sample(kids_names, 3)
                    
                    lcm_val = random.choice([60, 120, 180, 240, 360])
                    if lcm_val == 60: valid_triplets = [(10,15,20), (12,15,20)]
                    elif lcm_val == 120: valid_triplets = [(15,24,40), (20,30,40)]
                    elif lcm_val == 180: valid_triplets = [(20,36,45), (30,45,60)]
                    elif lcm_val == 240: valid_triplets = [(30,48,80), (40,60,80)]
                    else: valid_triplets = [(40,72,90), (60,72,90)]
                    t_a, t_b, t_c = random.choice(valid_triplets)
                    
                    divisors = []
                    current_nums = [t_a, t_b, t_c]
                    steps_html = ""
                    running = True
                    while running:
                        divided_in_this_step = False
                        for p in [2, 3, 5, 7]:
                            if sum(1 for x in current_nums if x % p == 0) >= 2:
                                divisors.append(p)
                                steps_html += f"<tr><td style='border-right: 2px solid #2c3e50; border-bottom: 2px solid #2c3e50; padding: 5px 15px; color:#c0392b; font-weight:bold; text-align:right;'>{p}</td>"
                                steps_html += f"<td style='border-bottom: 2px solid #2c3e50; padding: 5px 15px; text-align:center;'><span style='color:#3498db;'>{current_nums[0]}</span>, <span style='color:#3498db;'>{current_nums[1]}</span>, <span style='color:#3498db;'>{current_nums[2]}</span></td></tr>"
                                current_nums = [x // p if x % p == 0 else x for x in current_nums]
                                divided_in_this_step = True
                                break 
                        if not divided_in_this_step:
                            running = False
                    steps_html += f"<tr><td></td><td style='padding: 5px 15px; text-align:center; font-weight:bold; color:#27ae60; border-bottom: 4px double #27ae60;'>{current_nums[0]}, {current_nums[1]}, {current_nums[2]}</td></tr>"
                    laps_a = lcm_val // t_a

                    q = f"เพื่อน 3 คน {vehicle}ออกกำลังกายรอบ{place} โดยเริ่มออกจากจุดเริ่มต้นพร้อมกัน <br>&nbsp;&nbsp;• {name1} {vehicle} 1 รอบ ใช้เวลา <b>{t_a} นาที</b><br>&nbsp;&nbsp;• {name2} {vehicle} 1 รอบ ใช้เวลา <b>{t_b} นาที</b><br>&nbsp;&nbsp;• {name3} {vehicle} 1 รอบ ใช้เวลา <b>{t_c} นาที</b><br>จงหาว่า อีกกี่นาทีทั้งสามคนถึงจะ <b>เจอกันที่จุดเริ่มต้นพร้อมกันอีกครั้ง?</b> และตอนนั้น <b>{name1} {vehicle}ไปแล้วกี่รอบ?</b>"

                    sol = f"""<span style='color:#2c3e50; line-height: 1.8;'>
                    <div style='background-color:#e8f8f5; border-left:4px solid #1abc9c; padding:15px; margin-bottom:15px; border-radius:8px;'>
                    💡 <b>การแปลเป็น "สมการคณิตศาสตร์":</b><br>
                    • <b>"เจอกันที่จุดเริ่มต้นพร้อมกัน"</b> ➔ คือหาจุดบรรจบในอนาคต (พหุคูณร่วม) ➔ หา <b>ค.ร.น.</b>
                    <br>
                    </div>
                    <b>วิธีทำอย่างละเอียดแบบ Step-by-step:</b><br>
                    👉 <b>ขั้นที่ 1: ตั้งหารสั้นเพื่อหา ค.ร.น.</b><br>
                    <table style='margin: 10px 40px; font-size: 20px; border-collapse: collapse;'>{steps_html}</table>
                    
                    👉 <b>ขั้นที่ 2: สรุปผล ค.ร.น. (เวลาที่ใช้จนกว่าจะเจอกัน)</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ค.ร.น. = {" × ".join(map(str, divisors))} × {" × ".join(map(str, current_nums))} = <b><span style='color:#c0392b;'>{lcm_val}</span> นาที</b><br>
                    
                    👉 <b>ขั้นที่ 3: หาจำนวนรอบของ {name1}</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;เวลาทั้งหมด <span style='color:#c0392b;'>{lcm_val}</span> นาที แบ่งออกทีละรอบ รอบละ <span style='color:#2980b9;'>{t_a}</span> นาที ➔ ใช้ <b style='color:#d35400;'>การหาร (÷)</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;สมการ: <span style='color:#c0392b;'>{lcm_val}</span> ÷ <span style='color:#2980b9;'>{t_a}</span> = <b><span style='color:#8e44ad;'>{laps_a}</span> รอบ</b><br><br>
                    <b>ตอบ: จะเจอกันใน {lcm_val} นาที และ {name1} ทำได้ {laps_a} รอบ</b></span>"""

                elif scenario == "gcd_remainder":
                    # [สไตล์ 5: ห.ร.ม. แบบเหลือเศษ - เพิ่มขนาดตัวเลข]
                    gcd_ans = random.choice([12, 15, 20, 24, 30])
                    m = random.sample([3, 4, 5, 7, 11], 3)
                    base_nums = [gcd_ans * x for x in m]
                    
                    # สุ่มเศษที่น้อยกว่า ห.ร.ม.
                    remains = [random.randint(1, gcd_ans - 1) for _ in range(3)]
                    n1 = base_nums[0] + remains[0]
                    n2 = base_nums[1] + remains[1]
                    n3 = base_nums[2] + remains[2]

                    divisors = []
                    current_nums = base_nums.copy()
                    steps_html = ""
                    temp_gcd = gcd_ans
                    for p in [2, 3, 5, 7]:
                        while temp_gcd % p == 0:
                            divisors.append(p)
                            next_nums = [x // p for x in current_nums]
                            steps_html += f"<tr><td style='border-right: 2px solid #2c3e50; border-bottom: 2px solid #2c3e50; padding: 5px 15px; color:#c0392b; font-weight:bold; text-align:right;'>{p}</td>"
                            steps_html += f"<td style='border-bottom: 2px solid #2c3e50; padding: 5px 15px; text-align:center;'><span style='color:#3498db;'>{current_nums[0]}</span>, <span style='color:#3498db;'>{current_nums[1]}</span>, <span style='color:#3498db;'>{current_nums[2]}</span></td></tr>"
                            current_nums = next_nums
                            temp_gcd //= p
                    steps_html += f"<tr><td></td><td style='padding: 5px 15px; text-align:center; font-weight:bold; color:#27ae60; border-bottom: 4px double #27ae60;'>{current_nums[0]}, {current_nums[1]}, {current_nums[2]}</td></tr>"

                    q = f"จงหา <b>จำนวนนับที่มากที่สุด</b> ที่นำไปหารตัวเลข <b>{n1}, {n2} และ {n3}</b> <br>แล้ว <b>เหลือเศษ {remains[0]}, {remains[1]} และ {remains[2]}</b> ตามลำดับ?"

                    sol = f"""<span style='color:#2c3e50; line-height: 1.8;'>
                    <div style='background-color:#fdf2e9; border-left:4px solid #e67e22; padding:15px; margin-bottom:15px; border-radius:8px;'>
                    💡 <b>อาวุธลับสอบแข่งขัน "ห.ร.ม. แบบมีเศษ":</b><br>
                    • คำว่า <b>"เศษ"</b> แปลว่า <b>"มีเกินมาอยู่"</b> ทำให้หารไม่ลงตัว!<br>
                    • <b>เคล็ดลับ:</b> ถ้าอยากให้หารลงตัว ให้ <b>"เอาเศษไปลบ (-) ทิ้งซะก่อน"</b> แล้วค่อยเอาผลลัพธ์ที่ได้ไปหา ห.ร.ม. ตามปกติ
                    </div>
                    <b>วิธีทำอย่างละเอียดแบบ Step-by-step:</b><br>
                    👉 <b>ขั้นที่ 1: กำจัดเศษส่วนเกิน (นำตัวเลขไปลบเศษของมันเอง)</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• <span style='color:#2980b9;'>{n1}</span> <b style='color:#c0392b;'>- เศษ {remains[0]}</b> = <b><span style='color:#8e44ad;'>{base_nums[0]}</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• <span style='color:#2980b9;'>{n2}</span> <b style='color:#c0392b;'>- เศษ {remains[1]}</b> = <b><span style='color:#8e44ad;'>{base_nums[1]}</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• <span style='color:#2980b9;'>{n3}</span> <b style='color:#c0392b;'>- เศษ {remains[2]}</b> = <b><span style='color:#8e44ad;'>{base_nums[2]}</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;<i>(ตอนนี้เราได้เลข <span style='color:#8e44ad;'>{base_nums[0]}, {base_nums[1]}, {base_nums[2]}</span> ที่พร้อมหารลงตัวแล้ว)</i><br><br>
                    
                    👉 <b>ขั้นที่ 2: นำเลขใหม่ไปตั้งหารสั้น เพื่อหา ห.ร.ม.</b><br>
                    <table style='margin: 10px 40px; font-size: 20px; border-collapse: collapse;'>{steps_html}</table>
                    
                    👉 <b>ขั้นที่ 3: สรุปคำตอบ</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;นำตัวหาร (<span style='color:#c0392b;'>สีแดง</span>) <b>คูณ (×)</b> กัน ➔ {" × ".join(map(str, divisors))} = <b><span style='color:#c0392b;'>{gcd_ans}</span></b><br><br>
                    <b>ตอบ: จำนวนที่มากที่สุดที่ตรงตามเงื่อนไขคือ {gcd_ans}</b></span>"""

                else:
                    # [สไตล์ 6: ค.ร.น. แบบเหลือเศษเท่ากัน - สุ่มสิ่งของและคน]
                    items_pool = ["ลูกอม", "ลูกแก้ว", "สติกเกอร์", "แสตมป์"]
                    item = random.choice(items_pool)
                    person = random.choice(names_pool)
                    
                    lcm_base = random.choice([60, 120, 180, 240, 360])
                    if lcm_base == 60: div_nums = [4, 5, 6]
                    elif lcm_base == 120: div_nums = [6, 8, 10]
                    elif lcm_base == 180: div_nums = [9, 12, 15]
                    elif lcm_base == 240: div_nums = [12, 15, 16]
                    else: div_nums = [15, 18, 20]
                    
                    rem = random.randint(1, min(div_nums) - 1)
                    final_ans = lcm_base + rem

                    divisors = []
                    current_nums = div_nums.copy()
                    steps_html = ""
                    running = True
                    while running:
                        divided = False
                        for p in [2, 3, 5, 7]:
                            if sum(1 for x in current_nums if x % p == 0) >= 2:
                                divisors.append(p)
                                steps_html += f"<tr><td style='border-right: 2px solid #2c3e50; border-bottom: 2px solid #2c3e50; padding: 5px 15px; color:#c0392b; font-weight:bold; text-align:right;'>{p}</td>"
                                steps_html += f"<td style='border-bottom: 2px solid #2c3e50; padding: 5px 15px; text-align:center;'><span style='color:#3498db;'>{current_nums[0]}</span>, <span style='color:#3498db;'>{current_nums[1]}</span>, <span style='color:#3498db;'>{current_nums[2]}</span></td></tr>"
                                current_nums = [x // p if x % p == 0 else x for x in current_nums]
                                divided = True
                                break 
                        if not divided:
                            running = False
                    steps_html += f"<tr><td></td><td style='padding: 5px 15px; text-align:center; font-weight:bold; color:#27ae60; border-bottom: 4px double #27ae60;'>{current_nums[0]}, {current_nums[1]}, {current_nums[2]}</td></tr>"

                    q = f"{person}มี{item}อยู่กล่องหนึ่ง <br>ถ้านำ{item}มาแบ่งให้เด็ก <b>{div_nums[0]} คน, {div_nums[1]} คน หรือ {div_nums[2]} คน</b> (คนละเท่าๆ กัน) <br>ปรากฏว่าไม่ว่าจะแบ่งด้วยวิธีไหน ก็จะ <b>'เหลือเศษ {rem} ชิ้น'</b> เสมอ <br>จงหาว่า{person}มี{item} <b>อย่างน้อยที่สุดกี่ชิ้น?</b>"

                    sol = f"""<span style='color:#2c3e50; line-height: 1.8;'>
                    <div style='background-color:#e8f8f5; border-left:4px solid #1abc9c; padding:15px; margin-bottom:15px; border-radius:8px;'>
                    💡 <b>อาวุธลับสอบแข่งขัน "ค.ร.น. แบบมีเศษ":</b><br>
                    • <b>"แบ่งแล้วเหลือเศษเสมอ"</b> ➔ แปลว่าจำนวนของมีเยอะ <b>เกินกว่า</b> ที่จะหารลงตัว<br>
                    • <b>เคล็ดลับ:</b> เราต้องหาจำนวนที่ "พอดีเป๊ะ (หา ค.ร.น.)" ให้ได้เสียก่อน! จากนั้นค่อย <b>"บวก (+) เศษเพิ่มเข้าไปตอนจบ"</b> เพื่อแกล้งให้มันเหลือเศษตามโจทย์สั่ง
                    </div>
                    <b>วิธีทำอย่างละเอียดแบบ Step-by-step:</b><br>
                    👉 <b>ขั้นที่ 1: ตั้งหารสั้นเพื่อหา ค.ร.น. (หาของจำนวนพอดีเป๊ะ)</b><br>
                    <table style='margin: 10px 40px; font-size: 20px; border-collapse: collapse;'>{steps_html}</table>
                    
                    👉 <b>ขั้นที่ 2: สรุปผล ค.ร.น.</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ค.ร.น. = {" × ".join(map(str, divisors))} × {" × ".join(map(str, current_nums))} = <b><span style='color:#8e44ad;'>{lcm_base}</span> ชิ้น</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;<i>(ถ้ามีของ <span style='color:#8e44ad;'>{lcm_base}</span> ชิ้นเป๊ะๆ จะแจกให้เด็กกี่คนก็หารลงตัว)</i><br><br>
                    
                    👉 <b>ขั้นที่ 3: ทำให้เกิดเศษตามที่โจทย์สั่ง (บวกเพิ่ม)</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;โจทย์สั่งว่าต้องเหลือ <b>เศษ {rem} ชิ้น</b> เสมอ<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;เรานำก้อนพอดีเป๊ะ ไป <b style='color:#3498db;'>บวก (+)</b> เพิ่มอีก {rem} ชิ้น<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;สมการ: <span style='color:#8e44ad;'>{lcm_base}</span> <b style='color:#3498db;'>+</b> {rem} = <b><span style='color:#c0392b;'>{final_ans}</span> ชิ้น</b><br><br>
                    <b>ตอบ: {person}มี{item}อย่างน้อยที่สุด {final_ans} ชิ้น</b></span>"""





# ================= หมวดที่ 1: รากฐานตัวเลขและการดำเนินการ (ป.5) =================
            elif actual_sub_t == "เลขยกกำลังเบื้องต้นและการหาเลขโดดหลักหน่วย":
                # สุ่ม 5 สถานการณ์: เติบโตทวีคูณ, หลักหน่วยตัวเดียว, PEMDAS, กับดักครึ่งหนึ่ง, หลักหน่วยประยุกต์
                scenario = random.choice([
                    "exponential_growth", "units_digit_cycle", "pemdas_exponents",
                    "exponent_trap", "units_digit_sum"
                ])

                if scenario == "exponential_growth":
                    # [สไตล์ 1: ชีวิตประจำวัน - การเติบโตแบบทวีคูณ (โค้ดเดิม)]
                    themes = [
                        ("นักวิทยาศาสตร์", "เชื้อแบคทีเรียกลายพันธุ์", "แบ่งเซลล์เพิ่มขึ้น", "เซลล์"),
                        ("แฮกเกอร์", "ไวรัสคอมพิวเตอร์", "คัดลอกตัวเองส่งต่อ", "เครื่อง"),
                        ("อินฟลูเอนเซอร์", "คลิปวิดีโอไวรัล", "ถูกแชร์ต่อให้เพื่อน", "คน")
                    ]
                    person, item, action, unit = random.choice(themes)
                    base = random.choice([2, 3, 4, 5])
                    power = random.choice([4, 5, 6])
                    ans = base ** power
                    mult_str = " × ".join([str(base)] * power)
                    
                    q = f"เริ่มต้นมี {item} เพียงแค่ 1 {unit} <br>แต่ทุกๆ 1 ชั่วโมง {item} 1 {unit} จะ<b>{action}ทีละ {base} {unit}</b> <br>จงหาว่าเมื่อเวลาผ่านไป <b>{power} ชั่วโมง</b> จะมี {item} ทั้งหมดกี่{unit}? <br><i>(ให้เขียนคำตอบในรูปการคูณ และผลลัพธ์สุดท้าย)</i>"

                    sol = f"""<span style='color:#2c3e50; line-height: 1.8;'>
                    <div style='background-color:#fcf3cf; border-left:4px solid #f1c40f; padding:15px; margin-bottom:15px; border-radius:8px;'>
                    💡 <b>การแปลภาษาไทย เป็น "สมการคณิตศาสตร์":</b><br>
                    • <b>"เพิ่มขึ้นทีละ {base} {unit}"</b> ➔ การเพิ่มขึ้นแบบรวดเร็วโดยนำเลขเดิมมาคูณซ้ำๆ ต้องใช้ <b style='color:#e74c3c;'>เครื่องหมายเลขยกกำลัง (Exponent)</b><br>
                    • <b>"ผ่านไป {power} ชั่วโมง"</b> ➔ แปลว่าเกิดการคูณซ้ำกันทั้งหมด <b>{power} ครั้ง</b><br>
                    🔥 <b>ประโยคสัญลักษณ์:</b> นำตัวเลขที่เพิ่ม <span style='color:#e74c3c;'>({base})</span> มาเป็น <b>'ฐาน'</b> และนำจำนวนครั้ง <span style='color:#2980b9;'>({power})</span> มาเป็น <b>'เลขชี้กำลัง'</b> ➔ จะเขียนได้เป็น <b><span style='color:#8e44ad;'>{base}<sup>{power}</sup></span></b>
                    </div>
                    <b>วิธีทำอย่างละเอียดแบบ Step-by-step:</b><br>
                    👉 <b>ขั้นที่ 1: กระจายเลขยกกำลังให้อยู่ในรูปการคูณ</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;<b><span style='color:#8e44ad;'>{base}<sup>{power}</sup></span></b> ความหมายคือ: นำเลข <span style='color:#e74c3c;'>{base}</span> มาคูณตัวมันเองจำนวน <span style='color:#2980b9;'>{power} ครั้ง</span><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;สมการ: <b><span style='color:#e74c3c;'>{mult_str}</span></b><br>
                    
                    👉 <b>ขั้นที่ 2: ค่อยๆ จับคู่คูณ (×) ไปทีละสเตป</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• ชั่วโมงที่ 1: มี <b><span style='color:#27ae60;'>{base}</span></b> {unit}<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• ชั่วโมงที่ 2: {base} × {base} = <b><span style='color:#27ae60;'>{base**2}</span></b> {unit}<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;<i>(คูณต่อไปเรื่อยๆ จนครบ {power} ครั้ง)</i>...<br>
                    
                    👉 <b>ขั้นที่ 3: สรุปผลลัพธ์</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;เมื่อคูณครบ {power} ครั้ง จะได้ผลลัพธ์คือ <b><span style='color:#c0392b;'>{ans:,}</span> {unit}</b><br><br>
                    <b>ตอบ: จะมี {item} ทั้งหมด {ans:,} {unit}</b></span>"""

                elif scenario == "units_digit_cycle":
                    # [สไตล์ 2: หาหลักหน่วยตัวเดียว (โค้ดเดิม)]
                    base_num = random.choice([2, 3, 7, 8])
                    power_num = random.randint(1005, 2999)
                    
                    cycles = {2: [2, 4, 8, 6], 3: [3, 9, 7, 1], 7: [7, 9, 3, 1], 8: [8, 4, 2, 6]}
                    cycle_arr = cycles[base_num]
                    
                    rem = power_num % 4
                    quotient = power_num // 4
                    ans_digit = cycle_arr[rem - 1] if rem != 0 else cycle_arr[3]
                    
                    rem_text = f"เหลือเศษ {rem}" if rem != 0 else "หารลงตัวพอดี (เศษ 0)"
                    position_text = f"ตัวที่ {rem}" if rem != 0 else "ตัวที่ 4 (ตัวสุดท้าย)"

                    q = f"ในด่านทดสอบเข้าห้องเรียนพิเศษ รหัสผ่านคือ <b>'เลขโดดในหลักหน่วย'</b> ของผลลัพธ์ <br><div style='text-align:center;'><span style='font-size:28px; font-weight:bold; color:#2980b9;'>{base_num}<sup>{power_num}</sup></span></div><br>จงหาว่ารหัสผ่านที่ถูกต้องคือเลขใด?"

                    sol = f"""<span style='color:#2c3e50; line-height: 1.8;'>
                    <div style='background-color:#fdf2e9; border-left:4px solid #e67e22; padding:15px; margin-bottom:15px; border-radius:8px;'>
                    💡 <b>อาวุธลับสอบแข่งขัน "วงจรหลักหน่วย (Cycle of 4)":</b><br>
                    ความมหัศจรรย์ของคณิตศาสตร์คือ <b>"เลขหลักหน่วยของแม่ {base_num} จะวนลูปซ้ำเดิมทุกๆ 4 ครั้งเสมอ!"</b> ไม่ว่าเลขชี้กำลังจะเยอะแค่ไหน เราก็หาคำตอบได้โดยไม่ต้องคูณจริง!
                    </div>
                    <b>วิธีทำอย่างละเอียดแบบ Step-by-step:</b><br>
                    👉 <b>ขั้นที่ 1: หากฎการวนลูป (ลองคูณแม่ {base_num} ไปเรื่อยๆ ดูแค่ตัวท้าย)</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• {base_num}<sup>1</sup> = ลงท้ายด้วย <b><span style='color:#2980b9;'>{cycle_arr[0]}</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• {base_num}<sup>2</sup> = ลงท้ายด้วย <b><span style='color:#2980b9;'>{cycle_arr[1]}</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• {base_num}<sup>3</sup> = ลงท้ายด้วย <b><span style='color:#2980b9;'>{cycle_arr[2]}</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• {base_num}<sup>4</sup> = ลงท้ายด้วย <b><span style='color:#2980b9;'>{cycle_arr[3]}</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;สรุปวงจรคือ: <b>[ {cycle_arr[0]}, {cycle_arr[1]}, {cycle_arr[2]}, {cycle_arr[3]} ]</b> วนไปเรื่อยๆ<br>
                    
                    👉 <b>ขั้นที่ 2: นำเลขชี้กำลังมา <span style='color:#d35400;'>หาร (÷) ด้วย 4</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;สมการ: <span style='color:#e74c3c;'>{power_num}</span> ÷ 4 = ได้ {quotient} รอบ และ <b><span style='color:#c0392b;'>{rem_text}</span></b><br>
                    
                    👉 <b>ขั้นที่ 3: ดูเศษเพื่อหาคำตอบ</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• <b>เศษคือ {rem}</b> แปลว่าตกตำแหน่ง <b><span style='color:#27ae60;'>{position_text}</span></b> ในวงจร<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ซึ่งตัวเลขในตำแหน่งนั้นคือ <b><span style='color:#8e44ad;'>{ans_digit}</span></b><br><br>
                    <b>ตอบ: รหัสผ่าน (เลขโดดหลักหน่วย) คือ {ans_digit}</b></span>"""

                elif scenario == "pemdas_exponents":
                    # [สไตล์ 3: กฎ PEMDAS (โค้ดเดิม)]
                    a = random.choice([2, 3, 4])
                    p_a = random.choice([3, 4]) 
                    b = random.choice([4, 5, 6, 7])
                    p_b = 2
                    c = random.choice([3, 4, 5])
                    d = random.choice([8, 9, 10])
                    p_d = 2 
                    
                    val_a, val_b, val_d = a**p_a, b**p_b, d**p_d
                    mult_val = val_b * c
                    final_ans = val_a + mult_val - val_d

                    q = f"จงหาผลลัพธ์ของสมการเวทมนตร์ต่อไปนี้ โดยใช้กฎลำดับการคำนวณ (PEMDAS)<br><br><div style='text-align:center; font-size:26px; font-weight:bold; letter-spacing:2px; background:#f8f9fa; padding:15px; border-radius:10px; border:2px dashed #bdc3c7;'>{a}<sup>{p_a}</sup> + ( {b}<sup>{p_b}</sup> × {c} ) - {d}<sup>{p_d}</sup> = ?</div>"

                    sol = f"""<span style='color:#2c3e50; line-height: 1.8;'>
                    <div style='background-color:#e8f8f5; border-left:4px solid #1abc9c; padding:15px; margin-bottom:15px; border-radius:8px;'>
                    💡 <b>กฎลำดับการคำนวณขั้นสูง (PEMDAS with Exponents):</b><br>
                    <b>1.</b> ทำใน <b>วงเล็บ ( )</b> ก่อน<br>
                    <b>2.</b> แปลงร่าง <b>เลขยกกำลัง (Exponents)</b> ให้เป็นตัวเลขธรรมดา<br>
                    <b>3.</b> ทำ <b>คูณ (×) หรือ หาร (÷)</b> จากซ้ายไปขวา<br>
                    <b>4.</b> ทำ <b>บวก (+) หรือ ลบ (-)</b> จากซ้ายไปขวา
                    </div>
                    <b>วิธีทำอย่างละเอียดแบบ Step-by-step:</b><br>
                    👉 <b>ขั้นที่ 1: แปลงร่างเลขยกกำลังให้เป็นเลขธรรมดา</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• <span style='color:#e74c3c;'>{a}<sup>{p_a}</sup></span> = {a} คูณกัน {p_a} ครั้ง = <b><span style='color:#2980b9;'>{val_a}</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• <span style='color:#e74c3c;'>{b}<sup>{p_b}</sup></span> = {b} คูณกัน {p_b} ครั้ง = <b><span style='color:#2980b9;'>{val_b}</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• <span style='color:#e74c3c;'>{d}<sup>{p_d}</sup></span> = {d} คูณกัน {p_d} ครั้ง = <b><span style='color:#2980b9;'>{val_d}</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;➔ สมการใหม่: <span style='color:#2980b9;'>{val_a}</span> + <b>( <span style='color:#2980b9;'>{val_b}</span> × {c} )</b> - <span style='color:#2980b9;'>{val_d}</span><br>
                    
                    👉 <b>ขั้นที่ 2: จัดการในวงเล็บ (คูณ)</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ในวงเล็บ ( <span style='color:#2980b9;'>{val_b}</span> <b style='color:#e74c3c;'>×</b> {c} ) = <b><span style='color:#27ae60;'>{mult_val}</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;➔ ยุบเหลือ: <span style='color:#2980b9;'>{val_a}</span> <b style='color:#3498db;'>+</b> <span style='color:#27ae60;'>{mult_val}</span> <b style='color:#9b59b6;'>-</b> <span style='color:#2980b9;'>{val_d}</span><br>
                    
                    👉 <b>ขั้นที่ 3: ทำ บวก(+) และ ลบ(-) ซ้ายไปขวา</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• บวก: <span style='color:#2980b9;'>{val_a}</span> <b style='color:#3498db;'>+</b> <span style='color:#27ae60;'>{mult_val}</span> = <b><span style='color:#8e44ad;'>{val_a + mult_val}</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• ลบ: <span style='color:#8e44ad;'>{val_a + mult_val}</span> <b style='color:#9b59b6;'>-</b> <span style='color:#2980b9;'>{val_d}</span> = <b><span style='color:#c0392b;'>{final_ans}</span></b><br><br>
                    <b>ตอบ: {final_ans}</b></span>"""

                elif scenario == "exponent_trap":
                    # ✨ [สไตล์ 4 ใหม่ล่าสุด!: โจทย์กับดัก (Trap) ครึ่งหนึ่งของเลขยกกำลัง]
                    power_trap = random.choice([20, 50, 100, 256, 1000])
                    
                    q = f"โจทย์ปราบเซียนในการสอบแข่งขัน:<br><div style='text-align:center; font-size:24px; font-weight:bold; background:#f8f9fa; padding:15px; border-radius:10px; border:2px dashed #bdc3c7; margin: 10px 0;'>'ครึ่งหนึ่ง' ของ <b><span style='color:#2980b9;'>2<sup>{power_trap}</sup></span></b> มีค่าเท่ากับเท่าใด?</div><br><i>(เด็กส่วนใหญ่มักจะตอบ 1<sup>{power_trap}</sup> หรือ 2<sup>{power_trap // 2}</sup> ซึ่ง <b>ผิด</b>! จงแสดงวิธีคิดที่ถูกต้อง)</i>"

                    sol = f"""<span style='color:#2c3e50; line-height: 1.8;'>
                    <div style='background-color:#fef5e7; border-left:4px solid #e67e22; padding:15px; margin-bottom:15px; border-radius:8px;'>
                    💡 <b>ถอดรหัสกับดักคณิตศาสตร์:</b><br>
                    • คำว่า <b>"ครึ่งหนึ่ง"</b> แปลว่าเราต้องนำของสิ่งนั้นไป <b style='color:#d35400;'>หาร (÷) ด้วย 2</b><br>
                    • ดังนั้น ประโยคสัญลักษณ์ที่แท้จริงคือ: <b><span style='color:#2980b9;'>2<sup>{power_trap}</sup></span> <b style='color:#d35400;'>÷</b> 2</b><br>
                    <br>❌ <b>ทำไมถึงห้ามเอา 2 ไปหารฐานตรงๆ?</b><br>
                    เพราะ 2<sup>{power_trap}</sup> ไม่ใช่เลข 2! แต่มันคือเลข 2 เรียงต่อกันยาวๆ {power_trap} ตัว การเอา 2 ไปหารฐาน ทำให้ความหมายเพี้ยนไปหมดครับ
                    </div>
                    <b>วิธีทำอย่างละเอียดแบบ Step-by-step:</b><br>
                    👉 <b>ขั้นที่ 1: กระจายความหมายของ 2<sup>{power_trap}</sup> ให้เห็นภาพ</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;2<sup>{power_trap}</sup> หมายถึง ➔ <b>2 × 2 × 2 × 2 ... (มีเลข 2 อยู่ทั้งหมด <span style='color:#e74c3c;'>{power_trap} ตัว</span>)</b><br><br>
                    
                    👉 <b>ขั้นที่ 2: นำมาหารด้วย 2 (เพื่อหาครึ่งหนึ่ง)</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;เมื่อนำมาหารด้วย 2 ➔ <b style='color:#d35400;'>÷ 2</b> (หรือเขียนเป็นเศษส่วนคือ ส่วน 2)<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;เลข 2 ที่เป็นตัวหารด้านล่าง จะไป <b>'ตัดกับ'</b> เลข 2 ตัวบนได้ <b style='color:#c0392b;'>หายไป 1 ตัวพอดีเป๊ะ!</b><br><br>
                    
                    👉 <b>ขั้นที่ 3: สรุปจำนวนเลข 2 ที่เหลืออยู่</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;เดิมมีเลข 2 อยู่ {power_trap} ตัว ถูกตัดทิ้งไป 1 ตัว ➔ <span style='color:#e74c3c;'>{power_trap}</span> - 1 = <b><span style='color:#27ae60;'>{power_trap - 1} ตัว</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;เมื่อมีเลข 2 คูณกันอยู่ {power_trap - 1} ตัว เราจึงยุบกลับเป็นเลขยกกำลังได้คือ <b><span style='color:#8e44ad;'>2<sup>{power_trap - 1}</sup></span></b><br><br>
                    <b>ตอบ: ครึ่งหนึ่งของ 2<sup>{power_trap}</sup> คือ 2<sup>{power_trap - 1}</sup></b></span>"""

                else:
                    # ✨ [สไตล์ 5 ใหม่ล่าสุด!: หลักหน่วยประยุกต์บวกกัน]
                    base1 = random.choice([2, 3, 7, 8])
                    base2 = random.choice([x for x in [2, 3, 7, 8] if x != base1])
                    power_num = random.randint(2025, 2500)
                    
                    cycles = {2: [2, 4, 8, 6], 3: [3, 9, 7, 1], 7: [7, 9, 3, 1], 8: [8, 4, 2, 6]}
                    rem = power_num % 4
                    q_val = power_num // 4
                    
                    ans_d1 = cycles[base1][rem - 1] if rem != 0 else cycles[base1][3]
                    ans_d2 = cycles[base2][rem - 1] if rem != 0 else cycles[base2][3]
                    
                    sum_digits = ans_d1 + ans_d2
                    final_unit = sum_digits % 10

                    q = f"จงหา <b>'เลขโดดในหลักหน่วย'</b> ของผลลัพธ์จากการบวกกันของ<br><div style='text-align:center;'><span style='font-size:28px; font-weight:bold; color:#8e44ad;'>{base1}<sup>{power_num}</sup> <b style='color:#e74c3c;'>+</b> {base2}<sup>{power_num}</sup></span></div>"

                    sol = f"""<span style='color:#2c3e50; line-height: 1.8;'>
                    <div style='background-color:#e8f8f5; border-left:4px solid #1abc9c; padding:15px; margin-bottom:15px; border-radius:8px;'>
                    💡 <b>เทคนิคพิชิตข้อสอบ:</b><br>
                    ข้อนี้เหมือนเอาด่านถอดรหัส 2 ด่านมารวมกัน!<br>
                    1. เราต้องหาเลขหลักหน่วยของ <span style='color:#2980b9;'>{base1}<sup>{power_num}</sup></span> ให้ได้ก่อน<br>
                    2. ไปหาเลขหลักหน่วยของ <span style='color:#27ae60;'>{base2}<sup>{power_num}</sup></span><br>
                    3. นำ <b>'หลักหน่วยทั้งสองตัวมาบวก (+) กัน'</b> แล้วดูว่าหลักหน่วยของผลลัพธ์สุดท้ายคือเลขอะไร
                    </div>
                    <b>วิธีทำอย่างละเอียดแบบ Step-by-step:</b><br>
                    👉 <b>ขั้นที่ 1: หารอบลูป (Cycle) จากเลขชี้กำลัง</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;เลขชี้กำลังคือ <span style='color:#e74c3c;'>{power_num}</span> นำมาหารด้วย 4 (เพราะหลักหน่วยวนทุก 4 ครั้ง)<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;{power_num} ÷ 4 = ได้ {q_val} รอบ และ <b><span style='color:#c0392b;'>เหลือเศษ {rem if rem != 0 else 0}</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;<i>(เศษ {rem if rem != 0 else 0} แปลว่าเราต้องดูตัวเลข <b>ตำแหน่งที่ {rem if rem != 0 else 4}</b> ในวงจรของมัน)</i><br><br>
                    
                    👉 <b>ขั้นที่ 2: หาหลักหน่วยของ {base1}<sup>{power_num}</sup></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;วงจรของแม่ {base1} คือ: [ {cycles[base1][0]}, {cycles[base1][1]}, {cycles[base1][2]}, {cycles[base1][3]} ]<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ตัวที่ {rem if rem != 0 else 4} ในวงจรคือเลข <b><span style='color:#2980b9;'>{ans_d1}</span></b><br><br>
                    
                    👉 <b>ขั้นที่ 3: หาหลักหน่วยของ {base2}<sup>{power_num}</sup></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;วงจรของแม่ {base2} คือ: [ {cycles[base2][0]}, {cycles[base2][1]}, {cycles[base2][2]}, {cycles[base2][3]} ]<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ตัวที่ {rem if rem != 0 else 4} ในวงจรคือเลข <b><span style='color:#27ae60;'>{ans_d2}</span></b><br><br>
                    
                    👉 <b>ขั้นที่ 4: นำหลักหน่วยมา <span style='color:#c0392b;'>บวก (+)</span> กันตามโจทย์สั่ง</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;นำ <span style='color:#2980b9;'>{ans_d1}</span> + <span style='color:#27ae60;'>{ans_d2}</span> = <b><span style='color:#8e44ad;'>{sum_digits}</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;เลขโดดหลักหน่วยของ {sum_digits} ก็คือ <b><span style='color:#c0392b;'>{final_unit}</span></b><br><br>
                    <b>ตอบ: เลขโดดหลักหน่วยของผลลัพธ์คือ {final_unit}</b></span>"""




# ================= หมวดที่ 2: โลกของเศษส่วนและทศนิยม (ป.5) =================
            elif actual_sub_t == "การบวกและการลบเศษส่วน":
                scenario = random.choice(["chain_operation", "pole_trap", "mixed_borrowing_trap", "equation_balance"])

                # ฟังก์ชันพิเศษ: วาดเศษส่วนด้วย "กล่องทึบ 2px" (ไม่มีทางโดนเว็บลบทิ้งแน่นอน)
                def make_frac(n, d, w="", color="inherit"):
                    line_color = color if color != "inherit" else "#2c3e50"
                    line_html = f"<div style='height:2px; background-color:{line_color}; margin: 2px 0; width:100%;'></div>"
                    frac_html = f"<div style='display:inline-block; text-align:center; vertical-align:middle; line-height:1.1; font-size:18px; margin:0 4px;'><div style='padding:0 2px;'>{n}</div>{line_html}<div style='padding:0 2px;'>{d}</div></div>"
                    
                    if w != "":
                        return f"<div style='display:inline-block; vertical-align:middle; color:{color}; font-size:20px;'><b>{w}</b>{frac_html}</div>"
                    return f"<div style='display:inline-block; vertical-align:middle; color:{color}; font-weight:bold;'>{frac_html}</div>"

                def simplify_fraction(n, d):
                    gcd = math.gcd(abs(n), abs(d))
                    return n // gcd, d // gcd

                if scenario == "chain_operation":
                    # [สไตล์ 1: บวกลบต่อเนื่อง 3 ตัว] - แก้ไขบั๊กตัวเลขไม่ตรงกัน
                    d_sets = [(3, 4, 6), (4, 5, 10), (3, 5, 15), (4, 6, 8), (5, 6, 10)]
                    d1, d2, d3 = random.choice(d_sets)
                    n1 = random.randint(1, d1 - 1)
                    n2 = random.randint(1, d2 - 1)
                    n3 = random.randint(1, d3 - 1)
                    
                    lcm_12 = (d1 * d2) // math.gcd(d1, d2)
                    lcm_all = (lcm_12 * d3) // math.gcd(lcm_12, d3)
                    
                    new_n1 = n1 * (lcm_all // d1)
                    new_n2 = n2 * (lcm_all // d2)
                    new_n3 = n3 * (lcm_all // d3)
                    
                    # ลอจิกใหม่: ค่อยๆ เพิ่มค่า n1 จนกว่าผลลัพธ์จะไม่ติดลบ เพื่อให้ n1 และ new_n1 เชื่อมโยงกันเสมอ
                    while new_n1 + new_n2 <= new_n3:
                        n1 += 1
                        new_n1 = n1 * (lcm_all // d1)
                    
                    ans_n = new_n1 + new_n2 - new_n3
                    simp_n, simp_d = simplify_fraction(ans_n, lcm_all)
                    
                    if simp_n > simp_d:
                        w = simp_n // simp_d
                        rem = simp_n % simp_d
                        ans_str = make_frac(rem, simp_d, w=w) if rem != 0 else f"<b>{w}</b>"
                    else:
                        ans_str = make_frac(simp_n, simp_d)

                    q = f"คุณแม่กำลังทำขนมเค้กสูตรพิเศษ โดยใช้แป้งสาลี {make_frac(n1, d1)} <b>กิโลกรัม</b> <br>จากนั้นเติมผงโกโก้เพิ่มลงไปอีก {make_frac(n2, d2)} <b>กิโลกรัม</b> <br>แต่พบว่าส่วนผสมเยอะเกินไป จึงตักส่วนผสมออกไป {make_frac(n3, d3)} <b>กิโลกรัม</b> <br>จงหาว่าตอนนี้น้ำหนักของส่วนผสมทั้งหมดคือเท่าใด?"

                    sol = f"""<span style='color:#2c3e50; line-height: 1.8;'>
                    <div style='background-color:#fcf3cf; border-left:4px solid #f1c40f; padding:15px; margin-bottom:15px; border-radius:8px;'>
                    💡 <b>การแปลเป็น "สมการคณิตศาสตร์":</b><br>
                    • <b>"เติมเพิ่มลงไป"</b> ➔ ทำให้ของมีมากขึ้น ต้องใช้ <b style='color:#27ae60;'>บวก (+)</b><br>
                    • <b>"ตักออกไป"</b> ➔ ทำให้ของลดลง ต้องใช้ <b style='color:#c0392b;'>ลบ (-)</b><br>
                    • ประโยคสัญลักษณ์: <b>( {make_frac(n1, d1)} <span style='color:#27ae60;'>+</span> {make_frac(n2, d2)} ) <span style='color:#c0392b;'>-</span> {make_frac(n3, d3)} = ?</b><br><br>
                    ⚠️ <b>กฎเหล็กของเศษส่วน:</b> เราบวกลบกันตรงๆ ไม่ได้เด็ดขาด! เพราะขนาดของชิ้นส่วน (ตัวส่วนด้านล่าง) ไม่เท่ากัน เราต้องหา <b>ค.ร.น.</b> เพื่อหั่นชิ้นส่วนให้มีขนาดเท่ากันก่อน
                    </div>
                    <b>วิธีทำอย่างละเอียดแบบ Step-by-step:</b><br>
                    👉 <b>ขั้นที่ 1: หา ค.ร.น. ของตัวส่วน {d1}, {d2} และ {d3}</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;นำ {d1}, {d2}, {d3} ไปตั้งหารสั้น จะได้ ค.ร.น. คือ <b><span style='color:#8e44ad;'>{lcm_all}</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;<i>(แปลว่าเราต้องหั่นส่วนผสมทุกอย่างให้เป็นชิ้นเล็กๆ ขนาด {make_frac(1, lcm_all)} กิโลกรัม)</i><br><br>
                    
                    👉 <b>ขั้นที่ 2: แปลงร่างเศษส่วนทุกตัว ให้มีตัวส่วนเป็น {lcm_all}</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• {make_frac(n1, d1)} ➔ คูณด้วย {(lcm_all//d1)} ทั้งบนและล่าง ➔ {make_frac(new_n1, lcm_all, color="#2980b9")}<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• {make_frac(n2, d2)} ➔ คูณด้วย {(lcm_all//d2)} ทั้งบนและล่าง ➔ {make_frac(new_n2, lcm_all, color="#2980b9")}<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• {make_frac(n3, d3)} ➔ คูณด้วย {(lcm_all//d3)} ทั้งบนและล่าง ➔ {make_frac(new_n3, lcm_all, color="#2980b9")}<br><br>
                    
                    👉 <b>ขั้นที่ 3: นำตัวเศษ (ด้านบน) มาบวกลบกัน</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;สมการใหม่: ( <span style='color:#2980b9;'>{new_n1}</span> <b style='color:#27ae60;'>+</b> <span style='color:#2980b9;'>{new_n2}</span> ) <b style='color:#c0392b;'>-</b> <span style='color:#2980b9;'>{new_n3}</span><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;= {new_n1 + new_n2} - {new_n3} = <b><span style='color:#e67e22;'>{ans_n}</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ดังนั้นคำตอบคือ {make_frac(ans_n, lcm_all)}<br><br>
                    
                    👉 <b>ขั้นที่ 4: ตัดทอนเป็นเศษส่วนอย่างต่ำ (ถ้ามี)</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;เมื่อนำแม่ {math.gcd(ans_n, lcm_all)} มาตัดทั้งบนและล่าง จะได้ {ans_str} กิโลกรัม<br><br>
                    <b>ตอบ: น้ำหนักของส่วนผสมทั้งหมดคือ {ans_str} กิโลกรัม</b></span>"""

                elif scenario == "pole_trap":
                    # [สไตล์ 2: โจทย์กับดัก "ลบจาก 1"]
                    d1 = random.choice([3, 4, 5])
                    d2 = random.choice([6, 7, 8])
                    n1 = 1
                    n2 = random.choice([1, 2])
                    
                    lcm_all = (d1 * d2) // math.gcd(d1, d2)
                    new_n1 = n1 * (lcm_all // d1)
                    new_n2 = n2 * (lcm_all // d2)
                    sum_n = new_n1 + new_n2
                    
                    rem_n = lcm_all - sum_n
                    simp_n, simp_d = simplify_fraction(rem_n, lcm_all)
                    ans_str = make_frac(simp_n, simp_d)

                    q = f"โจทย์ปราบเซียนสอบเข้า ม.1:<br>เสาต้นหนึ่ง ปักอยู่ในโคลน {make_frac(n1, d1)} <b>ของความยาวเสา</b> <br>และจมอยู่ในน้ำ {make_frac(n2, d2)} <b>ของความยาวเสา</b> <br>ส่วนที่เหลือโผล่พ้นน้ำขึ้นมาในอากาศ <br>จงหาว่า <b>ส่วนที่โผล่พ้นน้ำคิดเป็นเศษส่วนเท่าใดของความยาวเสา?</b>"

                    sol = f"""<span style='color:#2c3e50; line-height: 1.8;'>
                    <div style='background-color:#fdf2e9; border-left:4px solid #e67e22; padding:15px; margin-bottom:15px; border-radius:8px;'>
                    💡 <b>ถอดรหัสกับดักคณิตศาสตร์ (Implicit Whole):</b><br>
                    โจทย์ข้อนี้ให้ตัวเลขมาแค่ 2 ตัว เด็กหลายคนจะเอามาแค่บวกหรือลบกันแล้วตอบเลย ซึ่ง <b>ผิด!</b><br>
                    • ความลับคือ: เสาทั้งต้นแบบเต็มๆ 1 ต้น ในทางเศษส่วนเราจะให้ค่ามันเท่ากับ <b>" 1 " (หรือ {make_frac(1, 1)}) เสมอ!</b><br>
                    • ประโยคสัญลักษณ์ที่แท้จริงคือ: <b><span style='color:#c0392b;'>1</span> - ( {make_frac(n1, d1)} + {make_frac(n2, d2)} ) = ?</b>
                    </div>
                    <b>วิธีทำอย่างละเอียดแบบ Step-by-step:</b><br>
                    👉 <b>ขั้นที่ 1: นำส่วนที่อยู่ในโคลนและน้ำมาบวกรวมกันก่อน</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;หา ค.ร.น. ของ {d1} และ {d2} ซึ่งก็คือ <b><span style='color:#8e44ad;'>{lcm_all}</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• โคลน: {make_frac(n1, d1)} ➔ แปลงเป็น {make_frac(new_n1, lcm_all, color="#2980b9")}<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• น้ำ: {make_frac(n2, d2)} ➔ แปลงเป็น {make_frac(new_n2, lcm_all, color="#2980b9")}<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;รวมโคลนและน้ำ: <span style='color:#2980b9;'>{new_n1}</span> + <span style='color:#2980b9;'>{new_n2}</span> = {make_frac(sum_n, lcm_all, color="#e74c3c")} <i>(นี่คือส่วนที่จมอยู่ทั้งหมด)</i><br><br>
                    
                    👉 <b>ขั้นที่ 2: นำเสาทั้งต้น (คือ 1) มาหักออก</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;เสาทั้งต้นมีค่าเท่ากับ 1 หรือเราจะมองเป็น {make_frac(lcm_all, lcm_all, color="#27ae60")} ก็ได้! (หั่นเป็น {lcm_all} ชิ้น และมีอยู่ครบ {lcm_all} ชิ้น)<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;นำเสาทั้งต้น <b style='color:#c0392b;'>ลบ (-)</b> ส่วนที่จม:<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;{make_frac(lcm_all, lcm_all)} - {make_frac(sum_n, lcm_all)} = {make_frac(rem_n, lcm_all, color="#d35400")}<br><br>
                    
                    👉 <b>ขั้นที่ 3: ตัดเป็นเศษส่วนอย่างต่ำ</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;เมื่อนำแม่ {math.gcd(rem_n, lcm_all)} มาตัด จะได้ {ans_str}<br><br>
                    <b>ตอบ: ส่วนที่โผล่พ้นน้ำคิดเป็น {ans_str} ของความยาวเสา</b></span>"""

                elif scenario == "mixed_borrowing_trap":
                    # [สไตล์ 3: จำนวนคละที่มีกับดัก "ต้องยืมตัวหน้า"]
                    w1 = random.randint(5, 12)
                    d1 = random.choice([4, 5, 6, 8])
                    n1 = random.randint(1, d1 // 2) 
                    
                    w2 = random.randint(1, 3)
                    d2 = random.choice([x for x in [3, 4, 5, 6, 8] if x != d1])
                    n2 = random.randint(d2 // 2 + 1, d2 - 1) 
                    
                    lcm_all = (d1 * d2) // math.gcd(d1, d2)
                    new_n1 = n1 * (lcm_all // d1)
                    new_n2 = n2 * (lcm_all // d2)
                    
                    final_n = new_n1 - new_n2
                    final_w = w1 - w2
                    borrowed = False
                    
                    if final_n < 0:
                        borrowed = True
                        final_w -= 1
                        final_n += lcm_all
                        
                    simp_n, simp_d = simplify_fraction(final_n, lcm_all)
                    ans_str = make_frac(simp_n, simp_d, w=final_w) if simp_n != 0 else f"<b>{final_w}</b>"

                    q = f"เชือกม้วนหนึ่งยาว {make_frac(n1, d1, w=w1)} <b>เมตร</b> <br>คุณพ่อตัดเชือกไปมัดกล่องพัสดุ {make_frac(n2, d2, w=w2)} <b>เมตร</b> <br>จะเหลือเชือกยาวกี่เมตร? <br><i>(จงแสดงวิธีทำโดยใช้เทคนิคการแปลงจำนวนคละ)</i>"

                    sol_borrow = ""
                    if borrowed:
                        sol_borrow = f"""
                    👉 <b>ขั้นที่ 3: เจอวิกฤต! ตัวเศษลบกันไม่ได้ ต้อง 'ยืม' จำนวนเต็ม</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;เราจะพบว่า <span style='color:#2980b9;'>{new_n1}</span> ลบ <span style='color:#e74c3c;'>{new_n2}</span> ไม่ได้! เพราะตัวตั้งน้อยกว่า <br>
                    &nbsp;&nbsp;&nbsp;&nbsp;วิธีแก้: ให้ไปยืมจำนวนเต็มด้านหน้ามา 1<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• เลข {w1} ถูกยืมไป 1 ➔ เหลือ <b><span style='color:#8e44ad;'>{w1 - 1}</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• เลข 1 ที่ยืมมา จะแปลงร่างเป็นเศษส่วนคือ {make_frac(lcm_all, lcm_all, color="#27ae60")} นำไปบวกกับของเดิม<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;➔ ตัวตั้งใหม่จะกลายเป็น: {make_frac(new_n1 + lcm_all, lcm_all, w=w1-1, color="#8e44ad")}<br><br>
                    
                    👉 <b>ขั้นที่ 4: ทำการลบตัวเลขชุดใหม่</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ลบจำนวนเต็ม: <span style='color:#8e44ad;'>{w1 - 1}</span> - {w2} = <b><span style='color:#d35400;'>{final_w}</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ลบเศษส่วน: {make_frac(new_n1 + lcm_all, lcm_all)} - {make_frac(new_n2, lcm_all)} = {make_frac(final_n, lcm_all, color="#d35400")}<br>
                        """
                    else:
                        sol_borrow = f"""
                    👉 <b>ขั้นที่ 3: นำตัวเลขมาลบกันตามปกติ (หน้าลบหน้า, หลังลบหลัง)</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ลบจำนวนเต็ม: <span style='color:#8e44ad;'>{w1}</span> - {w2} = <b><span style='color:#d35400;'>{final_w}</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ลบเศษส่วน: {make_frac(new_n1, lcm_all)} - {make_frac(new_n2, lcm_all)} = {make_frac(final_n, lcm_all, color="#d35400")}<br>
                        """

                    sol = f"""<span style='color:#2c3e50; line-height: 1.8;'>
                    <div style='background-color:#e8f8f5; border-left:4px solid #1abc9c; padding:15px; margin-bottom:15px; border-radius:8px;'>
                    💡 <b>เทคนิคการลบ "จำนวนคละ":</b><br>
                    • <b>"ตัดเชือกไปมัดกล่อง"</b> ➔ ของสั้นลง ต้องใช้ <b style='color:#c0392b;'>เครื่องหมายลบ (-)</b><br>
                    • เราสามารถแยก <b>"จำนวนเต็ม"</b> และ <b>"เศษส่วน"</b> ออกจากกันแล้วค่อยลบกันได้ เพื่อไม่ให้ตัวเลขเยอะเกินไป (หน้าลบหน้า, หลังลบหลัง)
                    </div>
                    <b>วิธีทำอย่างละเอียดแบบ Step-by-step:</b><br>
                    👉 <b>ขั้นที่ 1: แยกจำนวนเต็มกับเศษส่วน</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ประโยคสัญลักษณ์: ( {w1} - {w2} ) กับ ( {make_frac(n1, d1)} - {make_frac(n2, d2)} )<br><br>
                    
                    👉 <b>ขั้นที่ 2: หา ค.ร.น. เพื่อปรับเศษส่วนให้เท่ากัน</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ค.ร.น. ของ {d1} และ {d2} คือ <b><span style='color:#8e44ad;'>{lcm_all}</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• {make_frac(n1, d1)} ➔ แปลงเป็น {make_frac(new_n1, lcm_all, color="#2980b9")}<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• {make_frac(n2, d2)} ➔ แปลงเป็น {make_frac(new_n2, lcm_all, color="#e74c3c")}<br>
                    {sol_borrow}<br>
                    👉 <b>ขั้นสุดท้าย: ประกอบร่างและตัดทอน</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ประกอบร่างกลับเป็นจำนวนคละ จะได้ {make_frac(final_n, lcm_all, w=final_w)}<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ตัดทอนเป็นเศษส่วนอย่างต่ำ จะได้ <b>{ans_str}</b><br><br>
                    <b>ตอบ: จะเหลือเชือกยาว {ans_str} เมตร</b></span>"""

                elif scenario == "equation_balance":
                    # ✨ [สไตล์ 4: สมการตัวแปร - แก้ไขบั๊ก ค.ร.น. เพี้ยนให้สมบูรณ์ 100%]
                    lcm_pool = random.choice([12, 18, 20, 24, 30, 36, 40])
                    d1 = random.choice([x for x in [3, 4, 5, 6, 8, 9, 10, 12] if lcm_pool % x == 0])
                    n1 = random.randint(1, d1 - 1)
                    
                    ans_n = random.randint(1, lcm_pool // 2)
                    
                    new_n1 = n1 * (lcm_pool // d1)
                    new_n2 = ans_n + new_n1
                    
                    # ตัดทอนให้กลายเป็น n2/d2 ที่เด็กจะเห็นในโจทย์
                    n2, d2 = simplify_fraction(new_n2, lcm_pool)
                    
                    # ลอจิกใหม่: คำนวณหา ค.ร.น. ที่แท้จริงจากมุมมองของนักเรียน (ระหว่าง d1 และ d2 ที่เด็กเห็น)
                    student_lcm = (d1 * d2) // math.gcd(d1, d2)
                    
                    student_new_n1 = n1 * (student_lcm // d1)
                    student_new_n2 = n2 * (student_lcm // d2)
                    
                    student_ans_n = student_new_n2 - student_new_n1
                    simp_ans_n, simp_ans_d = simplify_fraction(student_ans_n, student_lcm)
                    ans_str = make_frac(simp_ans_n, simp_ans_d)

                    q = f"ชาวไร่เก็บเกี่ยวมะม่วงได้จำนวนหนึ่ง (สมมติว่าเป็นตะกร้า <b>A</b>) <br>ต่อมาเก็บมะม่วงเพิ่มได้อีก {make_frac(n1, d1)} <b>ตัน</b> <br>เมื่อนำไปชั่งน้ำหนักรวมกัน พบว่ามีมะม่วงทั้งหมด {make_frac(n2, d2)} <b>ตัน</b> <br>จงหาว่า ในตอนแรกชาวไร่เก็บมะม่วงได้ (ตะกร้า <b>A</b>) หนักกี่ตัน?"

                    sol = f"""<span style='color:#2c3e50; line-height: 1.8;'>
                    <div style='background-color:#fef5e7; border-left:4px solid #e67e22; padding:15px; margin-bottom:15px; border-radius:8px;'>
                    💡 <b>การแปลเป็น "สมการคณิตศาสตร์":</b><br>
                    • ให้ของที่ยังไม่รู้ค่าเป็นตัวแปร <b>A</b><br>
                    • <b>"เก็บเพิ่มได้อีก"</b> ➔ ใช้เครื่องหมาย <b style='color:#27ae60;'>บวก (+)</b><br>
                    • <b>"รวมกันพบว่ามี..."</b> ➔ คือผลลัพธ์หลังเครื่องหมาย <b>เท่ากับ (=)</b><br>
                    🔥 <b>ประโยคสัญลักษณ์:</b> <b><span style='color:#8e44ad;'>A</span> + {make_frac(n1, d1)} = {make_frac(n2, d2)}</b>
                    <br>
                    </div>
                    <b>วิธีทำอย่างละเอียดแบบ Step-by-step:</b><br>
                    👉 <b>ขั้นที่ 1: การย้ายข้างสมการ (Balancing)</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;เราต้องการหาค่า <span style='color:#8e44ad;'>A</span> จึงต้องย้าย {make_frac(n1, d1)} ไปฝั่งตรงข้าม<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;จากเดิมที่เป็นบวก พอย้ายข้ามสะพาน (เครื่องหมาย =) จะต้องเปลี่ยนเป็น <b>'ลบ' (-)</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;สมการใหม่: <span style='color:#8e44ad;'>A</span> = <b>{make_frac(n2, d2)} <span style='color:#c0392b;'>-</span> {make_frac(n1, d1)}</b><br><br>
                    
                    👉 <b>ขั้นที่ 2: หา ค.ร.น. ของ {d2} และ {d1} เพื่อปรับตัวส่วน</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ค.ร.น. ของ {d2} และ {d1} คือ <b><span style='color:#2980b9;'>{student_lcm}</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• {make_frac(n2, d2)} ➔ {make_frac(student_new_n2, student_lcm, color="#27ae60")}<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• {make_frac(n1, d1)} ➔ {make_frac(student_new_n1, student_lcm, color="#e74c3c")}<br><br>
                    
                    👉 <b>ขั้นที่ 3: ลบตัวเศษ</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;<span style='color:#8e44ad;'>A</span> = {make_frac(student_new_n2, student_lcm, color="#27ae60")} - {make_frac(student_new_n1, student_lcm, color="#e74c3c")} = <b>{make_frac(student_ans_n, student_lcm)}</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;คำตอบคือ {make_frac(student_ans_n, student_lcm)} และตัดทอนอย่างต่ำได้เป็น <b>{ans_str}</b><br><br>
                    <b>ตอบ: ตอนแรกชาวไร่เก็บมะม่วงได้ {ans_str} ตัน</b></span>"""




# ================= หมวดที่ 2: โลกของเศษส่วนและทศนิยม (ป.5) =================
            elif actual_sub_t == "การคูณและการหารเศษส่วน":
                # สุ่ม 4 สถานการณ์: ของ(คูณ), แบ่งแพ็ก(หาร), หาผลรวมจากส่วนย่อย(กับดัก), ระคน 3 ตัว(PEMDAS)
                scenario = random.choice(["multiply_of", "divide_pack", "reverse_fraction_trap", "pure_pemdas"])

                # ✨ ฟังก์ชันวาดเศษส่วนแนวตั้ง (ใช้กล่องทึบ 2px ตัดปัญหาเว็บลบเส้น)
                def make_frac(n, d, w="", color="inherit"):
                    line_color = color if color != "inherit" else "#2c3e50"
                    line_html = f"<div style='height:2px; background-color:{line_color}; margin: 2px 0; width:100%;'></div>"
                    frac_html = f"<div style='display:inline-block; text-align:center; vertical-align:middle; line-height:1.1; font-size:18px; margin:0 4px;'><div style='padding:0 2px;'>{n}</div>{line_html}<div style='padding:0 2px;'>{d}</div></div>"
                    if w != "":
                        return f"<div style='display:inline-block; vertical-align:middle; color:{color}; font-size:20px;'><b>{w}</b>{frac_html}</div>"
                    return f"<div style='display:inline-block; vertical-align:middle; color:{color}; font-weight:bold;'>{frac_html}</div>"

                def simplify_fraction(n, d):
                    gcd = math.gcd(abs(n), abs(d))
                    return n // gcd, d // gcd

                if scenario == "multiply_of":
                    # ✨ [สไตล์ 1: การคูณ (Fraction of a whole) - แปลงคำว่า "ของ" เป็นคูณ]
                    jobs = [("ลุงชัย", "ที่ดิน", "ขุดบ่อเลี้ยงปลา", "ไร่"), 
                            ("ป้าสมศรี", "ผ้าไหม", "ตัดชุดเดรส", "เมตร"), 
                            ("โรงงาน", "ข้าวสาร", "บริจาคให้เด็กกำพร้า", "ตัน")]
                    person, item, action, unit = random.choice(jobs)
                    
                    # จำนวนเต็มและเศษส่วนตั้งต้น
                    w1 = random.randint(12, 30)
                    d1 = random.choice([2, 3, 4, 5, 8])
                    n1 = random.choice([x for x in range(1, d1) if math.gcd(x, d1) == 1])
                    
                    # เศษส่วนที่นำไปใช้
                    d2 = random.choice([3, 4, 5, 6, 7, 9])
                    n2 = random.randint(1, d2 - 1)
                    
                    # แปลงจำนวนคละเป็นเศษเกิน
                    imp_n1 = w1 * d1 + n1
                    imp_d1 = d1
                    
                    # ผลคูณ
                    ans_n = imp_n1 * n2
                    ans_d = imp_d1 * d2
                    simp_n, simp_d = simplify_fraction(ans_n, ans_d)
                    
                    if simp_n > simp_d and simp_d != 1:
                        ans_w = simp_n // simp_d
                        ans_rem = simp_n % simp_d
                        ans_str = make_frac(ans_rem, simp_d, w=ans_w)
                    elif simp_d == 1:
                        ans_str = f"<b>{simp_n}</b>"
                    else:
                        ans_str = make_frac(simp_n, simp_d)

                    q = f"{person}มี{item}ทั้งหมด {make_frac(n1, d1, w=w1)} <b>{unit}</b> <br>แบ่งพื้นที่ {make_frac(n2, d2)} <b><u>ของ</u>{item}ทั้งหมด</b> ไป{action} <br>จงหาว่า{person}ใช้{item}ไป{action}ทั้งหมดกี่{unit}?"

                    sol = f"""<span style='color:#2c3e50; line-height: 1.8;'>
                    <div style='background-color:#fcf3cf; border-left:4px solid #f1c40f; padding:15px; margin-bottom:15px; border-radius:8px;'>
                    💡 <b>การแปลภาษาไทย เป็น "สมการคณิตศาสตร์":</b><br>
                    • <b><span style='color:#c0392b;'>⚠️ กับดัก!</span></b> เด็กหลายคนเห็นคำว่า "แบ่ง" แล้วรีบเอาไปลบหรือหารทันที ซึ่งผิดครับ!<br>
                    • สังเกตคำว่า <b>"ของ"</b> ให้ดี! ในทางคณิตศาสตร์ คำว่า <b>เศษส่วน <u>ของ</u> สิ่งใดสิ่งหนึ่ง</b> หมายถึง <b>การคูณ (×)</b> เสมอ!<br>
                    • ประโยคสัญลักษณ์: <b>{make_frac(n1, d1, w=w1)} <span style='color:#e74c3c;'>×</span> {make_frac(n2, d2)} = ?</b>
                    <br>
                    </div>
                    <b>วิธีทำอย่างละเอียดแบบ Step-by-step:</b><br>
                    👉 <b>ขั้นที่ 1: แปลง 'จำนวนคละ' ให้เป็น 'เศษเกิน' ก่อนเสมอ</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;{make_frac(n1, d1, w=w1)} ➔ เอา ล่างคูณหน้าบวกบน: ({d1} × {w1}) + {n1} = <b><span style='color:#2980b9;'>{imp_n1}</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ดังนั้นจะได้เศษเกินคือ {make_frac(imp_n1, imp_d1, color="#2980b9")}<br><br>
                    
                    👉 <b>ขั้นที่ 2: นำมาคูณกัน (กฎของการคูณ: บนคูณบน ล่างคูณล่าง)</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;สมการ: {make_frac(imp_n1, imp_d1, color="#2980b9")} <b style='color:#e74c3c;'>×</b> {make_frac(n2, d2, color="#e67e22")}<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• ตัวบนคูณกัน: <span style='color:#2980b9;'>{imp_n1}</span> × <span style='color:#e67e22;'>{n2}</span> = <b><span style='color:#8e44ad;'>{ans_n}</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• ตัวล่างคูณกัน: <span style='color:#2980b9;'>{imp_d1}</span> × <span style='color:#e67e22;'>{d2}</span> = <b><span style='color:#8e44ad;'>{ans_d}</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ได้ผลลัพธ์เบื้องต้นคือ {make_frac(ans_n, ans_d, color="#8e44ad")}<br><br>
                    
                    👉 <b>ขั้นที่ 3: ตัดทอนเป็นเศษส่วนอย่างต่ำ / จำนวนคละ</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;นำแม่ {math.gcd(ans_n, ans_d)} มาตัดทั้งบนและล่าง จะได้คำตอบคือ <b><span style='color:#27ae60;'>{ans_str}</span></b><br><br>
                    <b>ตอบ: {person}ใช้{item}ไป {ans_str} {unit}</b></span>"""

                elif scenario == "divide_pack":
                    # ✨ [สไตล์ 2: การหาร (Division into parts) - บังคับให้หารลงตัวเป็นจำนวนถุงเป๊ะๆ]
                    items = [("น้ำตาลทราย", "กิโลกรัม", "ถุง"), ("น้ำยาล้างจาน", "ลิตร", "ขวด"), ("ริบบิ้น", "เมตร", "เส้น")]
                    item, unit, pack = random.choice(items)
                    
                    ans_bags = random.randint(12, 45) # คำตอบคือจำนวนถุง
                    d2 = random.choice([2, 3, 4, 5, 8])
                    n2 = random.choice([x for x in range(1, d2) if math.gcd(x, d2) == 1])
                    
                    # หาก้อนใหญ่ (W1 N1/D1) จาก ans_bags * (N2/D2)
                    total_n = ans_bags * n2
                    total_d = d2
                    w1 = total_n // total_d
                    n1 = total_n % total_d
                    d1 = total_d
                    
                    # ถ้าเศษเป็น 0 ให้เพิ่มจำนวนถุงไปอีก 1 ให้มันกลายเป็นจำนวนคละ
                    if n1 == 0:
                        ans_bags += 1
                        total_n = ans_bags * n2
                        w1 = total_n // total_d
                        n1 = total_n % total_d
                        
                    imp_n1 = w1 * d1 + n1

                    q = f"แม่ค้ามี{item}ทั้งหมด {make_frac(n1, d1, w=w1)} <b>{unit}</b> <br>นำมา <b>แบ่งใส่{pack} {pack}ละเท่าๆ กัน</b> โดยแต่ละ{pack}จุ {make_frac(n2, d2)} <b>{unit}</b> <br>จงหาว่าแม่ค้าจะแบ่ง{item}ได้ทั้งหมด <b>กี่{pack}พอดี?</b>"

                    sol = f"""<span style='color:#2c3e50; line-height: 1.8;'>
                    <div style='background-color:#e8f8f5; border-left:4px solid #1abc9c; padding:15px; margin-bottom:15px; border-radius:8px;'>
                    💡 <b>การแปลภาษาไทย เป็น "สมการคณิตศาสตร์":</b><br>
                    • คีย์เวิร์ดสำคัญคือ <b>"แบ่งใส่{pack} {pack}ละเท่าๆ กัน"</b> <br>
                    • การนำของก้อนใหญ่ มาแบ่งเป็นกลุ่มย่อยๆ ขนาดเท่าๆ กัน คือหน้าที่ของ <b style='color:#d35400;'>เครื่องหมายหาร (÷)</b><br>
                    • ประโยคสัญลักษณ์: <b>{make_frac(n1, d1, w=w1)} <span style='color:#d35400;'>÷</span> {make_frac(n2, d2)} = ?</b>
                    <br>
                    </div>
                    <b>วิธีทำอย่างละเอียดแบบ Step-by-step:</b><br>
                    👉 <b>ขั้นที่ 1: แปลง 'จำนวนคละ' ให้เป็น 'เศษเกิน'</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;{make_frac(n1, d1, w=w1)} ➔ ({d1} × {w1}) + {n1} = <b><span style='color:#2980b9;'>{imp_n1}</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;สมการปัจจุบัน: {make_frac(imp_n1, d1, color="#2980b9")} <b style='color:#d35400;'>÷</b> {make_frac(n2, d2, color="#e67e22")}<br><br>
                    
                    👉 <b>ขั้นที่ 2: กฎเวทมนตร์ของการหารเศษส่วน!</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;เราไม่สามารถหารเศษส่วนตรงๆ ได้ ต้องใช้คาถา: <b>"เปลี่ยนหารเป็นคูณ แล้วกลับเศษเป็นส่วน (ตีลังกาตัวหลัง)"</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• เปลี่ยน <b style='color:#d35400;'>÷</b> เป็น <b style='color:#e74c3c;'>×</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• เปลี่ยน {make_frac(n2, d2, color="#e67e22")} เป็น <b>{make_frac(d2, n2, color="#e67e22")}</b> <i>(เอาส่วนขึ้นบน เอาเศษลงล่าง)</i><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;สมการใหม่: {make_frac(imp_n1, d1, color="#2980b9")} <b style='color:#e74c3c;'>×</b> {make_frac(d2, n2, color="#e67e22")}<br><br>
                    
                    👉 <b>ขั้นที่ 3: คูณเศษส่วน (บนคูณบน ล่างคูณล่าง)</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• ตัวบน: <span style='color:#2980b9;'>{imp_n1}</span> × <span style='color:#e67e22;'>{d2}</span> = <b><span style='color:#8e44ad;'>{imp_n1 * d2}</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• ตัวล่าง: <span style='color:#2980b9;'>{d1}</span> × <span style='color:#e67e22;'>{n2}</span> = <b><span style='color:#8e44ad;'>{d1 * n2}</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ได้เป็น {make_frac(imp_n1 * d2, d1 * n2, color="#8e44ad")} ซึ่งเมื่อนำมาหารกัน ({imp_n1 * d2} ÷ {d1 * n2}) จะลงตัวได้ <b><span style='color:#27ae60;'>{ans_bags}</span></b> พอดีเป๊ะ!<br><br>
                    <b>ตอบ: แม่ค้าจะแบ่งได้ทั้งหมด {ans_bags} {pack}พอดี</b></span>"""

                elif scenario == "reverse_fraction_trap":
                    # ✨ [สไตล์ 3: โจทย์กับดัก (Reverse Fraction) - บอกส่วนย่อย ให้หาทั้งหมด]
                    d1 = random.choice([5, 7, 8, 9, 11, 12])
                    n1 = random.choice([x for x in range(2, d1) if math.gcd(x, d1) == 1])
                    
                    # บังคับให้จำนวนคน/ระยะทาง หารด้วย n1 ลงตัว
                    part_value = random.choice([15, 20, 25, 30, 40, 50])
                    known_val = part_value * n1
                    total_val = part_value * d1
                    
                    q = f"โจทย์ปราบเซียนสอบเข้าห้อง Gifted:<br>โรงเรียนแห่งหนึ่งมีนักเรียนชาย {make_frac(n1, d1)} <b>ของนักเรียนทั้งหมด</b> <br>ถ้านับจำนวนนักเรียนชายได้ <b>{known_val} คน</b> <br>จงหาว่าโรงเรียนนี้ <b>มีนักเรียนรวมทั้งหมดกี่คน?</b>"

                    sol = f"""<span style='color:#2c3e50; line-height: 1.8;'>
                    <div style='background-color:#fdf2e9; border-left:4px solid #e67e22; padding:15px; margin-bottom:15px; border-radius:8px;'>
                    💡 <b>ถอดรหัสกับดักคณิตศาสตร์ (Visual Thinking):</b><br>
                    • <b><span style='color:#c0392b;'>⚠️ ระวังโดนหลอก!</span></b> เด็ก 90% จะเอา {known_val} ไปคูณกับ {make_frac(n1, d1)} ทันที ซึ่งผิด! เพราะ {known_val} ไม่ใช่จำนวนนักเรียนทั้งหมด แต่มันคือส่วนย่อย!<br>
                    • <b>แนวคิดบาร์โมเดล (Bar Model):</b> เศษส่วน {make_frac(n1, d1)} หมายความว่า ถ้านักเรียนทั้งโรงเรียนถูกแบ่งเป็น <b><span style='color:#2980b9;'>{d1} ส่วนเท่าๆ กัน</span></b> จะเป็นนักเรียนชายไปแล้ว <b><span style='color:#e74c3c;'>{n1} ส่วน</span></b>
                    <br>
                    </div>
                    <b>วิธีทำอย่างละเอียดแบบ Step-by-step:</b><br>
                    <b>วิธีคิดแบบวาดภาพ (Bar Model):</b><br>
                    👉 <b>ขั้นที่ 1: เทียบสัดส่วนหาค่าของ "1 ส่วน"</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;เรารู้แล้วว่า นักเรียนชาย <span style='color:#e74c3c;'>{n1} ส่วน</span> มีค่าเท่ากับ <span style='color:#8e44ad;'>{known_val} คน</span><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ถ้าอยากรู้ว่า <span style='color:#27ae60;'>1 ส่วน</span> มีกี่คน? ให้เอาไป <b style='color:#d35400;'>หาร (÷)</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;➔ {known_val} ÷ {n1} = <b><span style='color:#27ae60;'>{part_value} คน</span></b> <i>(ตอนนี้เรารู้แล้วว่า 1 บล็อกมีค่า {part_value})</i><br><br>
                    
                    👉 <b>ขั้นที่ 2: หาจำนวนนักเรียนทั้งหมด</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;นักเรียนทั้งหมดมี <span style='color:#2980b9;'>{d1} ส่วน</span> <br>
                    &nbsp;&nbsp;&nbsp;&nbsp;นำไป <b style='color:#e74c3c;'>คูณ (×)</b> กับค่าของ 1 ส่วน ➔ {d1} × <span style='color:#27ae60;'>{part_value}</span> = <b><span style='color:#c0392b;'>{total_val} คน</span></b><br><br>
                    
                    <i>📝 <b>(แถม) วิธีคิดแบบสมการพีชคณิตสำหรับเด็กโต:</b><br>
                    ให้ นักเรียนทั้งหมด = A<br>
                    A × {make_frac(n1, d1)} = {known_val}<br>
                    ย้ายข้าง ➔ A = {known_val} <b style='color:#d35400;'>÷</b> {make_frac(n1, d1)}<br>
                    เปลี่ยนหารเป็นคูณกลับเศษเป็นส่วน ➔ A = {known_val} <b style='color:#e74c3c;'>×</b> {make_frac(d1, n1)} = {total_val}</i><br><br>
                    <b>ตอบ: โรงเรียนนี้มีนักเรียนทั้งหมด {total_val} คน</b></span>"""

                else:
                    # ✨ [สไตล์ 4: การคูณหารระคน 3 ตัว (Cross Cancellation Test)]
                    # สุ่มตัวเลขที่ตัดทอนไขว้กันได้สวยงาม
                    pool = [12, 14, 15, 16, 18, 20, 21, 24, 25, 27, 28, 30, 32, 35, 36]
                    n1, d1, n2, d2, n3, d3 = random.sample(pool, 6)
                    
                    # รูปแบบ A/B * C/D / E/F
                    # ก่อนคำนวณ ต้องเปลี่ยนหารเป็นคูณ E/F -> d3/n3
                    final_num = n1 * n2 * d3
                    final_den = d1 * d2 * n3
                    
                    simp_n, simp_d = simplify_fraction(final_num, final_den)
                    if simp_n > simp_d and simp_d != 1:
                        w = simp_n // simp_d
                        rem = simp_n % simp_d
                        ans_str = make_frac(rem, simp_d, w=w)
                    elif simp_d == 1:
                        ans_str = f"<b>{simp_n}</b>"
                    else:
                        ans_str = make_frac(simp_n, simp_d)

                    q = f"จงหาผลลัพธ์ของสมการเศษส่วนต่อไปนี้ (ฝึกเทคนิคการตัดทอนไขว้)<br><br><div style='text-align:center; font-size:24px; font-weight:bold; letter-spacing:1px; background:#f8f9fa; padding:15px; border-radius:10px; border:2px dashed #bdc3c7;'>{make_frac(n1, d1)} × {make_frac(n2, d2)} ÷ {make_frac(n3, d3)} = ?</div>"

                    sol = f"""<span style='color:#2c3e50; line-height: 1.8;'>
                    <div style='background-color:#fef5e7; border-left:4px solid #e67e22; padding:15px; margin-bottom:15px; border-radius:8px;'>
                    💡 <b>กฎลำดับการคำนวณ (PEMDAS) และเวทมนตร์เศษส่วน:</b><br>
                    • เมื่อมีแค่คูณกับหารอยู่ด้วยกัน ให้ทำจาก <b>ซ้ายไปขวา</b><br>
                    • กฎเหล็ก: <b>ห้ามตัดทอนตัวเลขข้ามเครื่องหมายหารเด็ดขาด!</b> ต้องทำการ "เปลี่ยนหารเป็นคูณ กลับเศษเป็นส่วน" ให้เป็นเครื่องหมายคูณทั้งหมดก่อน ค่อยทำการตัดทอนทีเดียว
                    </div>
                    <b>วิธีทำอย่างละเอียดแบบ Step-by-step:</b><br>
                    👉 <b>ขั้นที่ 1: ตีลังกาเศษส่วนหลังเครื่องหมายหาร</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ตัวปัญหาคือ <b style='color:#d35400;'>÷</b> {make_frac(n3, d3, color="#c0392b")}<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;เปลี่ยนเป็น <b style='color:#27ae60;'>×</b> <b>{make_frac(d3, n3, color="#27ae60")}</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;สมการทั้งหมดจะกลายเป็น: <b>{make_frac(n1, d1, color="#2980b9")} × {make_frac(n2, d2, color="#2980b9")} <span style='color:#27ae60;'>×</span> {make_frac(d3, n3, color="#27ae60")}</b><br><br>
                    
                    👉 <b>ขั้นที่ 2: รวบกระดานคูณ (บนคูณบน ล่างคูณล่าง)</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;นำตัวเศษ (ด้านบน) ทั้งหมดมาคูณกัน: {n1} × {n2} × {d3} = <b><span style='color:#8e44ad;'>{final_num:,}</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;นำตัวส่วน (ด้านล่าง) ทั้งหมดมาคูณกัน: {d1} × {d2} × {n3} = <b><span style='color:#8e44ad;'>{final_den:,}</span></b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;<i>(ในข้อสอบจริง เด็กๆ สามารถใช้เทคนิค 'จับคู่ตัดทอนแนวทแยง' บนล่าง ก่อนที่จะคูณตัวเลขให้ใหญ่ขึ้นได้ครับ เพื่อความรวดเร็ว)</i><br><br>
                    
                    👉 <b>ขั้นที่ 3: ตัดทอนเป็นเศษส่วนอย่างต่ำ</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ผลลัพธ์คือ {make_frac(f"{final_num:,}", f"{final_den:,}")}<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;เมื่อนำแม่ {math.gcd(final_num, final_den)} มาตัดทอนทั้งบนและล่างให้เป็นเศษส่วนอย่างต่ำ จะได้ <b><span style='color:#c0392b;'>{ans_str}</span></b><br><br>
                    <b>ตอบ: {ans_str}</b></span>"""




                    # ================= หมวดที่ 2: โลกของเศษส่วนและทศนิยม (ป.5) =================
            elif actual_sub_t == "การบวก ลบ คูณ หารระคน (เศษส่วน)":
                # สุ่ม 3 สถานการณ์ระดับปราบเซียน (กับดักของที่เหลือ, ผสมแล้วแบ่งแพ็ก, สมการ PEMDAS)
                scenario = random.choice(["remainder_trap", "mix_and_pack", "pemdas_fraction"])

                # ✨ ฟังก์ชันวาดเศษส่วน (กล่องทึบ 2px ป้องกันเว็บลบเส้นทิ้ง)
                def make_frac(n, d, w="", color="inherit"):
                    line_color = color if color != "inherit" else "#2c3e50"
                    line_html = f"<div style='height:2px; background-color:{line_color}; margin: 2px 0; width:100%;'></div>"
                    frac_html = f"<div style='display:inline-block; text-align:center; vertical-align:middle; line-height:1.1; font-size:18px; margin:0 4px;'><div style='padding:0 2px;'>{n}</div>{line_html}<div style='padding:0 2px;'>{d}</div></div>"
                    if w != "":
                        return f"<div style='display:inline-block; vertical-align:middle; color:{color}; font-size:20px;'><b>{w}</b>{frac_html}</div>"
                    return f"<div style='display:inline-block; vertical-align:middle; color:{color}; font-weight:bold;'>{frac_html}</div>"

                def simplify_fraction(n, d):
                    gcd = math.gcd(abs(n), abs(d))
                    return n // gcd, d // gcd

                if scenario == "remainder_trap":
                    # ✨ [สไตล์ 1: โจทย์กับดัก "ของที่เหลือ" (Fraction of Remainder) ข้อสอบยอดฮิต]
                    people = ["คุณพ่อ", "คุณแม่", "พี่ชาย", "คุณลุง", "ป้าสมศรี"]
                    person = random.choice(people)
                    
                    d1 = random.choice([4, 5, 6, 8, 10])
                    n1 = random.randint(1, d1 // 2)
                    d2 = random.choice([3, 4, 5, 6])
                    n2 = random.randint(1, d2 - 1)
                    k = random.choice([50, 100, 200, 300])
                    
                    # ลอจิกทำให้ตัวเลขลงตัวเป๊ะๆ
                    total_money = d1 * d2 * k
                    
                    spent_1 = total_money * n1 // d1
                    remain_1 = total_money - spent_1
                    spent_2 = remain_1 * n2 // d2
                    final_remain = remain_1 - spent_2

                    q = f"โจทย์ปราบเซียนสอบเข้า ม.1:<br>{person}มีเงินอยู่ <b>{total_money:,} บาท</b> <br>นำไปซื้อของใช้ในบ้าน {make_frac(n1, d1)} <b>ของเงินทั้งหมด</b> <br>จากนั้นนำไปซื้อเสื้อผ้า {make_frac(n2, d2)} <b><u>ของเงินที่เหลือ</u></b> <br>จงหาว่าตอนนี้{person} <b>เหลือเงินกี่บาท?</b>"

                    sol = f"""<span style='color:#2c3e50; line-height: 1.8;'>
                    <div style='background-color:#fdf2e9; border-left:4px solid #e67e22; padding:15px; margin-bottom:15px; border-radius:8px;'>
                    💡 <b>ถอดรหัสกับดักคณิตศาสตร์ (Visual Thinking):</b><br>
                    • คำว่า <b>"ของ"</b> ในทางคณิตศาสตร์แปลว่า <b style='color:#e74c3c;'>การคูณ (×)</b> เสมอ!<br>
                    • <b><span style='color:#c0392b;'>⚠️ กับดักอันตราย:</span></b> เด็กส่วนใหญ่จะเอา {make_frac(n1, d1)} ไปบวกกับ {make_frac(n2, d2)} ซึ่ง <b>ผิดมหันต์!</b> <br>
                    เพราะก้อนที่สองเขาบอกว่า <b>"ของเงินที่เหลือ"</b> (ไม่ได้เทียบจากเงินก้อนแรก) เราต้องหาเงินที่เหลือก่อน แล้วค่อยเอาไป <b style='color:#e74c3c;'>คูณ (×)</b> เพื่อหาค่าใช้จ่ายก้อนที่สองครับ!
                    </div>
                    <b>วิธีทำอย่างละเอียดแบบ Step-by-step:</b><br>
                    👉 <b>ขั้นที่ 1: หาค่าใช้จ่ายก้อนแรก (ซื้อของใช้)</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;จ่ายไป {make_frac(n1, d1)} <b>ของ</b> เงินทั้งหมด ({total_money:,} บาท)<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;เปลี่ยนคำว่า 'ของ' เป็น 'คูณ': {make_frac(n1, d1)} <b style='color:#e74c3c;'>×</b> {total_money:,}<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;= ({total_money:,} ÷ {d1}) × {n1} = <b><span style='color:#c0392b;'>{spent_1:,}</span> บาท</b> <i>(นี่คือเงินที่จ่ายไป)</i><br><br>
                    
                    👉 <b>ขั้นที่ 2: หา "เงินที่เหลือ" (จุดสำคัญที่สุด!)</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;เงินเดิม <span style='color:#2980b9;'>{total_money:,}</span> <b style='color:#3498db;'>ลบ (-)</b> เงินที่จ่ายไป <span style='color:#c0392b;'>{spent_1:,}</span><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;= <span style='color:#2980b9;'>{total_money:,}</span> - <span style='color:#c0392b;'>{spent_1:,}</span> = <b><span style='color:#8e44ad;'>{remain_1:,}</span> บาท</b> <i>(นี่คือเงินก้อนใหม่ที่เราจะเอาไปคิดต่อ)</i><br><br>
                    
                    👉 <b>ขั้นที่ 3: หาค่าใช้จ่ายก้อนที่สอง (ซื้อเสื้อผ้า)</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;จ่ายไป {make_frac(n2, d2)} <b>ของเงินที่เหลือ</b> (ซึ่งก็คือ <span style='color:#8e44ad;'>{remain_1:,}</span> บาท)<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;สมการ: {make_frac(n2, d2)} <b style='color:#e74c3c;'>×</b> <span style='color:#8e44ad;'>{remain_1:,}</span><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;= (<span style='color:#8e44ad;'>{remain_1:,}</span> ÷ {d2}) × {n2} = <b><span style='color:#c0392b;'>{spent_2:,}</span> บาท</b><br><br>
                    
                    👉 <b>ขั้นที่ 4: หาเงินที่เหลือสุทธิในกระเป๋า</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;นำเงินที่เหลือจากรอบแรก <span style='color:#8e44ad;'>{remain_1:,}</span> <b style='color:#3498db;'>ลบ (-)</b> ค่าเสื้อผ้า <span style='color:#c0392b;'>{spent_2:,}</span><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;= <span style='color:#8e44ad;'>{remain_1:,}</span> - <span style='color:#c0392b;'>{spent_2:,}</span> = <b><span style='color:#27ae60;'>{final_remain:,}</span> บาท</b><br><br>
                    <b>ตอบ: ตอนนี้{person}เหลือเงิน {final_remain:,} บาท</b></span>"""

                elif scenario == "mix_and_pack":
                    # ✨ [สไตล์ 2: โจทย์ "ผสมแล้วแบ่ง" (Combine & Divide) - ทดสอบวงเล็บและการหารเศษส่วน]
                    # วนลูปสุ่มจนกว่าตัวเลขจะหารลงตัวเป็นจำนวนเต็ม (ถุง)
                    while True:
                        w1 = random.randint(1, 5)
                        d1 = random.choice([2, 4, 5, 8, 10])
                        n1 = random.randint(1, d1 - 1)
                        
                        w2 = random.randint(1, 5)
                        d2 = random.choice([2, 4, 5, 8, 10])
                        n2 = random.randint(1, d2 - 1)
                        
                        d3 = random.choice([2, 4, 5, 8, 10, 12, 16])
                        n3 = random.randint(1, d3 - 1)

                        # คำนวณ (W1 + W2)
                        sum_n = (w1 * d1 + n1) * d2 + (w2 * d2 + n2) * d1
                        sum_d = d1 * d2
                        
                        # คำนวณ (W1 + W2) / W3 (หารเศษส่วน = คูณส่วนกลับ)
                        if (sum_n * d3) % (sum_d * n3) == 0:
                            ans_bags = (sum_n * d3) // (sum_d * n3)
                            break
                            
                    # หา ค.ร.น. ของ d1, d2 เพื่อแสดงในเฉลย
                    lcm_12 = (d1 * d2) // math.gcd(d1, d2)
                    new_n1 = ((w1 * d1 + n1) * (lcm_12 // d1))
                    new_n2 = ((w2 * d2 + n2) * (lcm_12 // d2))
                    total_sum_n = new_n1 + new_n2

                    q = f"ชาวสวนเก็บน้ำผึ้งถังแรกได้ปริมาตร {make_frac(n1, d1, w=w1)} <b>ลิตร</b> <br>และเก็บถังที่สองได้ปริมาตร {make_frac(n2, d2, w=w2)} <b>ลิตร</b> <br>นำน้ำผึ้งทั้งสองถังมา <b>'เทผสมรวมกัน'</b> แล้ว <b>'แบ่งใส่ขวด'</b> ขวดละ {make_frac(n3, d3)} <b>ลิตร</b> เท่าๆ กัน <br>จงหาว่าชาวสวนจะแบ่งน้ำผึ้งได้ทั้งหมด <b>กี่ขวดพอดี?</b>"

                    sol = f"""<span style='color:#2c3e50; line-height: 1.8;'>
                    <div style='background-color:#e8f8f5; border-left:4px solid #1abc9c; padding:15px; margin-bottom:15px; border-radius:8px;'>
                    💡 <b>การแปลภาษาไทย เป็น "สมการคณิตศาสตร์":</b><br>
                    • <b>"เทผสมรวมกัน"</b> ➔ เอาของมากองรวมกัน ต้องใช้ <b style='color:#27ae60;'>เครื่องหมายบวก (+)</b><br>
                    • <b>"แบ่งใส่ขวด ขวดละเท่าๆ กัน"</b> ➔ การแบ่งกลุ่มย่อยขนาดเท่ากัน คือพระเอกของ <b style='color:#d35400;'>เครื่องหมายหาร (÷)</b><br>
                    🔥 <b>ประโยคสัญลักษณ์:</b> ต้องใส่วงเล็บให้การผสมเสร็จก่อนเสมอ!<br>
                    <b>( {make_frac(n1, d1, w=w1)} <span style='color:#27ae60;'>+</span> {make_frac(n2, d2, w=w2)} ) <span style='color:#d35400;'>÷</span> {make_frac(n3, d3)} = ?</b>
                    </div>
                    <b>วิธีทำอย่างละเอียดแบบ Step-by-step:</b><br>
                    👉 <b>ขั้นที่ 1: ทำในวงเล็บ (เทน้ำผึ้งผสมกัน)</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;เปลี่ยนจำนวนคละให้เป็นเศษเกินก่อน:<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• ถังแรก: {make_frac(n1, d1, w=w1)} = {make_frac(w1 * d1 + n1, d1, color="#2980b9")}<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• ถังสอง: {make_frac(n2, d2, w=w2)} = {make_frac(w2 * d2 + n2, d2, color="#2980b9")}<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;หา ค.ร.น. ของ {d1} และ {d2} คือ <b><span style='color:#8e44ad;'>{lcm_12}</span></b> เพื่อบวกกัน:<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;{make_frac(new_n1, lcm_12)} + {make_frac(new_n2, lcm_12)} = <b>{make_frac(total_sum_n, lcm_12, color="#8e44ad")} ลิตร</b> <i>(นี่คือน้ำผึ้งถังใหญ่ที่ผสมเสร็จแล้ว)</i><br><br>
                    
                    👉 <b>ขั้นที่ 2: แบ่งใส่ขวด (การหารเศษส่วน)</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;นำน้ำผึ้งถังใหญ่ <b style='color:#d35400;'>หาร (÷)</b> ด้วยปริมาตรขวด<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;สมการ: {make_frac(total_sum_n, lcm_12, color="#8e44ad")} <b style='color:#d35400;'>÷</b> {make_frac(n3, d3, color="#e74c3c")}<br><br>
                    
                    👉 <b>ขั้นที่ 3: กฎเวทมนตร์ของการหารเศษส่วน!</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;<b>"เปลี่ยนหารเป็นคูณ แล้วกลับเศษเป็นส่วน (ตีลังกาตัวหลัง)"</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;สมการจะเปลี่ยนเป็น: {make_frac(total_sum_n, lcm_12, color="#8e44ad")} <b style='color:#27ae60;'>×</b> {make_frac(d3, n3, color="#e74c3c")}<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;= <span style='color:#8e44ad;'>{total_sum_n}</span> × <span style='color:#e74c3c;'>{d3}</span> ÷ (<span style='color:#8e44ad;'>{lcm_12}</span> × <span style='color:#e74c3c;'>{n3}</span>)<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;= {total_sum_n * d3} ÷ {lcm_12 * n3} = <b><span style='color:#c0392b;'>{ans_bags}</span></b><br><br>
                    <b>ตอบ: จะแบ่งน้ำผึ้งได้ทั้งหมด {ans_bags} ขวดพอดี</b></span>"""

                else:
                    # ✨ [สไตล์ 3: สมการวงเล็บซ้อน (PEMDAS Fraction) - ทดสอบความแม่นยำระดับสุดยอด]
                    while True:
                        d1 = random.choice([2, 3, 4, 5])
                        n1 = random.randint(1, d1 - 1)
                        d2 = random.choice([2, 3, 4, 5])
                        n2 = random.randint(1, d2 - 1)
                        d3 = random.choice([2, 3, 4, 5])
                        n3 = random.randint(1, d3 + 2) # มีโอกาสเป็นเศษเกิน
                        d4 = random.choice([2, 3, 4, 5])
                        n4 = random.randint(1, d4 - 1)

                        # คำนวณ (N1/D1 + N2/D2)
                        s_n = n1 * d2 + n2 * d1
                        s_d = d1 * d2
                        
                        # คำนวณ * (N3/D3)
                        m_n = s_n * n3
                        m_d = s_d * d3
                        
                        # คำนวณ - N4/D4
                        f_n = m_n * d4 - n4 * m_d
                        f_d = m_d * d4

                        # ตรวจสอบให้ผลลัพธ์เป็นบวก และตัวเลขไม่เฟ้อเกินไป
                        if f_n > 0:
                            simp_n, simp_d = simplify_fraction(f_n, f_d)
                            if simp_d < 40: 
                                break
                                
                    # ตัวแปรแสดงผลในวงเล็บ (หา ค.ร.น.)
                    lcm_12 = (d1 * d2) // math.gcd(d1, d2)
                    step1_n1 = n1 * (lcm_12 // d1)
                    step1_n2 = n2 * (lcm_12 // d2)
                    step1_sum_n = step1_n1 + step1_n2
                    step1_simp_n, step1_simp_d = simplify_fraction(step1_sum_n, lcm_12)
                    
                    # ตัวแปรการคูณ
                    step2_mult_n = step1_simp_n * n3
                    step2_mult_d = step1_simp_d * d3
                    step2_simp_n, step2_simp_d = simplify_fraction(step2_mult_n, step2_mult_d)
                    
                    # ตัวแปรการลบ
                    lcm_34 = (step2_simp_d * d4) // math.gcd(step2_simp_d, d4)
                    step3_n1 = step2_simp_n * (lcm_34 // step2_simp_d)
                    step3_n2 = n4 * (lcm_34 // d4)
                    
                    final_ans_str = make_frac(simp_n, simp_d)

                    q = f"จงหาผลลัพธ์ของสมการเศษส่วนต่อไปนี้ โดยใช้กฎลำดับการคำนวณ (PEMDAS)<br><br><div style='text-align:center; font-size:24px; font-weight:bold; letter-spacing:1px; background:#f8f9fa; padding:15px; border-radius:10px; border:2px dashed #bdc3c7;'>( {make_frac(n1, d1)} + {make_frac(n2, d2)} ) × {make_frac(n3, d3)} - {make_frac(n4, d4)} = ?</div>"

                    sol = f"""<span style='color:#2c3e50; line-height: 1.8;'>
                    <div style='background-color:#fef5e7; border-left:4px solid #e67e22; padding:15px; margin-bottom:15px; border-radius:8px;'>
                    💡 <b>กฎลำดับการคำนวณสากล (PEMDAS):</b><br>
                    สมการนี้มีทั้งบวก, คูณ, ลบ และวงเล็บผสมกันอยู่ ถ้าทำผิดลำดับคำตอบจะผิดทันที!<br>
                    <b>อันดับ 1:</b> ทำใน <b>วงเล็บ ( )</b> ก่อนเสมอ<br>
                    <b>อันดับ 2:</b> ทำเครื่องหมาย <b>คูณ (×)</b><br>
                    <b>อันดับ 3:</b> ทำเครื่องหมาย <b>ลบ (-)</b> เป็นลำดับสุดท้าย
                    </div>
                    <b>วิธีทำอย่างละเอียดแบบ Step-by-step:</b><br>
                    👉 <b>ขั้นที่ 1: เคลียร์ในวงเล็บ (การบวกเศษส่วน)</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;วงเล็บคือ: {make_frac(n1, d1)} + {make_frac(n2, d2)} (หา ค.ร.น. ของ {d1},{d2} ได้ {lcm_12})<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;แปลงร่าง: {make_frac(step1_n1, lcm_12)} + {make_frac(step1_n2, lcm_12)} = {make_frac(step1_sum_n, lcm_12)} <br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ตัดทอนอย่างต่ำได้เป็น <b>{make_frac(step1_simp_n, step1_simp_d, color="#8e44ad")}</b> <i>(วงเล็บแตกสลาย กลายเป็นตัวเลขนี้)</i><br><br>
                    
                    👉 <b>ขั้นที่ 2: จัดการเครื่องหมาย คูณ (×)</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;สมการปัจจุบัน: {make_frac(step1_simp_n, step1_simp_d, color="#8e44ad")} <b style='color:#27ae60;'>×</b> {make_frac(n3, d3)} - {make_frac(n4, d4)}<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;<i>(การคูณเศษส่วน ไม่ต้องหา ค.ร.น. ให้เอา บนคูณบน ล่างคูณล่าง ได้เลย!)</i><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;= {make_frac(f"{step1_simp_n} × {n3}", f"{step1_simp_d} × {d3}")} = {make_frac(step2_mult_n, step2_mult_d)}<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ตัดทอนอย่างต่ำได้เป็น <b>{make_frac(step2_simp_n, step2_simp_d, color="#e67e22")}</b> <i>(ก้อนการคูณยุบรวมกันเหลือแค่นี้)</i><br><br>
                    
                    👉 <b>ขั้นที่ 3: จัดการเครื่องหมาย ลบ (-) เป็นขั้นตอนสุดท้าย</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;นำผลลัพธ์มาลบตัวสุดท้าย: {make_frac(step2_simp_n, step2_simp_d, color="#e67e22")} <b style='color:#c0392b;'>-</b> {make_frac(n4, d4)}<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;หา ค.ร.น. ของ {step2_simp_d} และ {d4} ได้ <b>{lcm_34}</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;แปลงร่าง: {make_frac(step3_n1, lcm_34)} - {make_frac(step3_n2, lcm_34)} = {make_frac(f_n, f_d)}<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ตัดทอนอย่างต่ำจะได้คำตอบสุดท้ายคือ <b><span style='color:#c0392b;'>{final_ans_str}</span></b><br><br>
                    <b>ตอบ: {final_ans_str}</b></span>"""




            elif actual_sub_t == "การคูณเศษส่วน":
                d1 = random.randint(3, 15)
                n1 = random.randint(1, d1 * 2) if is_challenge else random.randint(1, d1 - 1)
                
                type_mul = random.choice(["frac", "whole"])
                if type_mul == "whole":
                    n2 = random.randint(2, 20)
                    d2 = 1
                    q = f"จงหาผลลัพธ์ของ {draw_frac(n1, d1)} <b style='color:#e74c3c;'>×</b> <b>{n2}</b>"
                else:
                    d2 = random.randint(3, 15)
                    n2 = random.randint(1, d2 * 2) if is_challenge else random.randint(1, d2 - 1)
                    q = f"จงหาผลลัพธ์ของ {draw_frac(n1, d1)} <b style='color:#e74c3c;'>×</b> {draw_frac(n2, d2)}"
                
                ans_n_raw = n1 * n2
                ans_d_raw = d1 * d2
                gcd_ans = math.gcd(ans_n_raw, ans_d_raw)
                final_n, final_d = ans_n_raw // gcd_ans, ans_d_raw // gcd_ans
                
                ans_disp = str(final_n) if final_d == 1 else f"{final_n//final_d}{draw_frac(final_n%final_d, final_d)}" if final_n > final_d else draw_frac(final_n, final_d)
                
                sol = f"""<span style='color:#2c3e50;'>
                <div style='background-color:#ebf5fb; border-left:4px solid #3498db; padding:10px; margin-bottom:15px; border-radius:4px;'>
                💡 <b>เทคนิคการคูณเศษส่วน:</b><br>
                ไม่ต้องทำส่วนให้เท่ากัน! สามารถนำ <b>(เศษ × เศษ)</b> และ <b>(ส่วน × ส่วน)</b> ได้เลย ถ้ารูปไหนตัดทอนไขว้ได้ให้ตัดก่อนจะคำนวณง่ายขึ้น
                </div>
                <b>วิธีทำอย่างละเอียด:</b><br>
                👉 <b>ขั้นที่ 1: นำบนคูณบน ล่างคูณล่าง</b><br>
                &nbsp;&nbsp;&nbsp;&nbsp;{draw_frac(f"{n1} × {n2}", f"{d1} × {d2 if type_mul=='frac' else '1'}")} = <b>{draw_frac(ans_n_raw, ans_d_raw)}</b><br><br>
                """
                if gcd_ans > 1:
                    sol += f"""👉 <b>ขั้นที่ 2: ตัดทอนเป็นเศษส่วนอย่างต่ำ</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ใช้แม่ <b>{gcd_ans}</b> หารทั้งบนและล่าง จะได้ <b>{draw_frac(final_n, final_d) if final_d != 1 else final_n}</b><br><br>"""
                
                sol += f"<b>ตอบ: {ans_disp}</b></span>"



            elif actual_sub_t == "การหารเศษส่วน":
                d1 = random.randint(2, 10)
                n1 = random.randint(1, d1 * 2)
                
                type_div = random.choice(["frac", "whole"])
                if type_div == "whole":
                    n2 = random.randint(2, 12)
                    d2 = 1
                    q = f"จงหาผลลัพธ์ของ {draw_frac(n1, d1)} <b style='color:#e74c3c;'>÷</b> <b>{n2}</b>"
                    flip_text = f"{draw_frac(1, n2)}"
                else:
                    d2 = random.randint(2, 10)
                    n2 = random.randint(1, d2 - 1)
                    q = f"จงหาผลลัพธ์ของ {draw_frac(n1, d1)} <b style='color:#e74c3c;'>÷</b> {draw_frac(n2, d2)}"
                    flip_text = f"{draw_frac(d2, n2)}"
                
                ans_n_raw = n1 * d2
                ans_d_raw = d1 * n2
                gcd_ans = math.gcd(ans_n_raw, ans_d_raw)
                final_n, final_d = ans_n_raw // gcd_ans, ans_d_raw // gcd_ans
                
                ans_disp = str(final_n) if final_d == 1 else f"{final_n//final_d}{draw_frac(final_n%final_d, final_d)}" if final_n > final_d else draw_frac(final_n, final_d)
                
                sol = f"""<span style='color:#2c3e50;'>
                <div style='background-color:#fef5e7; border-left:4px solid #e67e22; padding:10px; margin-bottom:15px; border-radius:4px;'>
                💡 <b>คาถาการหารเศษส่วน:</b><br>
                <b>"ตัวหน้าเหมือนเดิม เปลี่ยนหาร(÷) เป็นคูณ(×) และกลับเศษเป็นส่วนที่ตัวหลัง"</b>
                </div>
                <b>วิธีทำอย่างละเอียด:</b><br>
                👉 <b>ขั้นที่ 1: เปลี่ยนเครื่องหมายและกลับตัวหลัง</b><br>
                &nbsp;&nbsp;&nbsp;&nbsp;จากโจทย์ กลายเป็น ➔ {draw_frac(n1, d1)} <b style='color:#27ae60;'>×</b> <b style='color:#8e44ad;'>{flip_text}</b><br><br>
                👉 <b>ขั้นที่ 2: คูณเศษส่วนตามปกติ (บน×บน, ล่าง×ล่าง)</b><br>
                &nbsp;&nbsp;&nbsp;&nbsp;{draw_frac(f"{n1} × {d2}", f"{d1} × {n2}")} = <b>{draw_frac(ans_n_raw, ans_d_raw)}</b><br><br>
                """
                if gcd_ans > 1:
                    sol += f"""👉 <b>ขั้นที่ 3: ทำให้เป็นเศษส่วนอย่างต่ำ/จำนวนคละ</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;จะได้ <b>{ans_disp}</b><br><br>"""
                    
                sol += f"<b>ตอบ: {ans_disp}</b></span>"



            # ================= หมวดที่ 2: ทศนิยม (ป.5) =================
            elif actual_sub_t == "การบวกและการลบทศนิยม":
                op = random.choice(["+", "-"])
                # ป.5 เน้นทศนิยม 2-3 ตำแหน่งที่ไม่เท่ากัน
                dp1, dp2 = random.choice([1, 2, 3]), random.choice([1, 2, 3])
                while dp1 == dp2: dp2 = random.choice([1, 2, 3])
                
                if op == "+": 
                    a = round(random.uniform(10.0, 500.0), dp1)
                    b = round(random.uniform(1.0, 99.0), dp2)
                else: 
                    a = round(random.uniform(100.0, 500.0), dp1)
                    b = round(random.uniform(10.0, a - 10.0), dp2)
                
                q = f"จงตั้งทดเพื่อหาผลลัพธ์ของ <b>{a} {op} {b}</b><br>{generate_decimal_vertical_html(a, b, op, is_key=False)}"
                
                sol = f"""<span style='color:#2c3e50;'>
                <div style='background-color:#fcf3cf; border-left:4px solid #f1c40f; padding:10px; margin-bottom:15px; border-radius:4px;'>
                💡 <b>เทคนิค:</b> เมื่อตำแหน่งทศนิยมไม่เท่ากัน ให้ <b>"เติม 0"</b> ด้านหลังตัวที่ตำแหน่งน้อยกว่า เพื่อให้การตั้งจุดทศนิยมและการยืมเลขไม่ผิดพลาด
                </div>
                {generate_decimal_vertical_html(a, b, op, is_key=True)}</span>"""



            elif actual_sub_t == "การคูณและการหารทศนิยม":
                op = random.choice(["×", "÷"])
                
                if op == "×":
                    # การคูณ: ทศนิยม 1-2 ตำแหน่ง คูณ ทศนิยม 1-2 ตำแหน่ง
                    v1 = round(random.uniform(1.1, 25.5), random.choice([1, 2]))
                    v2 = round(random.uniform(1.1, 9.9), random.choice([1, 2]))
                    ans = round(v1 * v2, 4)
                    
                    dec_p1 = len(str(v1).split('.')[1])
                    dec_p2 = len(str(v2).split('.')[1])
                    total_dec = dec_p1 + dec_p2
                    
                    ans_raw = int(str(v1).replace('.', '')) * int(str(v2).replace('.', ''))
                    
                    q = f"จงหาผลคูณของ <b>{v1} × {v2}</b>"
                    
                    sol = f"""<span style='color:#2c3e50;'>
                    <div style='background-color:#ebf5fb; border-left:4px solid #3498db; padding:10px; margin-bottom:15px; border-radius:4px;'>
                    💡 <b>เทคนิคการคูณทศนิยม:</b><br>
                    1. ถอดจุดออกแล้วนำตัวเลขมาตั้งคูณกันเหมือนจำนวนเต็มปกติ<br>
                    2. นำจำนวนตำแหน่งทศนิยมของตัวตั้งและตัวคูณมา <b>บวกกัน</b> เพื่อกำหนดตำแหน่งทศนิยมของคำตอบ
                    </div>
                    <b>วิธีทำ:</b><br>
                    👉 <b>ขั้นที่ 1:</b> {v1} มี <b>{dec_p1} ตำแหน่ง</b> และ {v2} มี <b>{dec_p2} ตำแหน่ง</b> (รวมเป็น <b style='color:#e74c3c;'>{total_dec} ตำแหน่ง</b>)<br>
                    👉 <b>ขั้นที่ 2:</b> ถอดจุดแล้วตั้งคูณ ➔ {int(str(v1).replace('.', ''))} × {int(str(v2).replace('.', ''))} = <b>{ans_raw:,}</b><br>
                    👉 <b>ขั้นที่ 3:</b> ใส่ทศนิยมกลับไป {total_dec} ตำแหน่ง จะได้ <b>{ans}</b><br><br>
                    <b>ตอบ: {ans}</b></span>"""
                
                else:
                    # การหารทศนิยมด้วยทศนิยม (เนื้อหาหลัก ป.5)
                    ans_raw = random.randint(12, 150)
                    divisor = round(random.choice([0.2, 0.4, 0.5, 1.2, 1.5, 2.5]), 1)
                    
                    dividend = round(ans_raw * divisor, 2)
                    
                    # หาวิธีเลื่อนจุด
                    move_step = 10 if len(str(divisor).split('.')[1]) == 1 else 100
                    new_dividend = dividend * move_step
                    new_divisor = int(divisor * move_step)
                    
                    # เช็คว่าผลคูณเป็น .0 ไหม ถ้าใช่ให้ตัดออก
                    new_dividend_str = str(int(new_dividend)) if new_dividend.is_integer() else str(new_dividend)
                    
                    q_eq = f"<div style='font-size: 24px; margin-bottom: 10px;'><b>{dividend} ÷ {divisor} = ?</b></div>"
                    
                    q = f"จงหาผลหารของทศนิยมต่อไปนี้<br>{q_eq}"
                    
                    long_div_html = get_decimal_long_div_html(new_divisor, new_dividend_str)
                    
                    sol = f"""<span style='color:#2c3e50;'>
                    <div style='background-color:#fcf3cf; border-left:4px solid #f1c40f; padding:10px; margin-bottom:15px; border-radius:4px;'>
                    💡 <b>เทคนิคการหารทศนิยม:</b><br>
                    <b>ห้ามตั้งหารถ้าตัวหารยังติดจุด!</b> ต้องเลื่อนจุดตัวหารให้เป็นจำนวนเต็มก่อน โดยเลื่อนจุดตัวตั้งตามไปเท่าๆ กัน (คือการคูณด้วย 10, 100 หรือ 1000)
                    </div>
                    <b>วิธีทำ:</b><br>
                    👉 <b>ขั้นที่ 1: เลื่อนจุดให้ตัวหารเป็นจำนวนเต็ม</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• ตัวหารคือ {divisor} เลื่อน 1 จุด (คูณ 10) กลายเป็น <b>{new_divisor}</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;• ตัวตั้งคือ {dividend} ต้องเลื่อน 1 จุดตามกัน กลายเป็น <b>{new_dividend_str}</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;<i>(โจทย์ใหม่คือ: <b>{new_dividend_str} ÷ {new_divisor}</b>)</i><br><br>
                    👉 <b>ขั้นที่ 2: ตั้งหารยาว</b><br>
                    {long_div_html}<br>
                    <b>ตอบ: {ans_raw}</b></span>"""



# ================= หมวดที่ 3: สถิติ, เรขาคณิต, ร้อยละ, สมการ (ป.5) =================
            elif actual_sub_t == "การหาค่าเฉลี่ย (Average)":
                items_count = random.randint(4, 6)
                target_avg = random.randint(20, 100)
                total = target_avg * items_count
                
                # สร้างตัวเลขสุ่มที่รวมกันได้ total พอดี
                nums = []
                current_sum = 0
                for i in range(items_count - 1):
                    n = random.randint(target_avg - 15, target_avg + 15)
                    nums.append(n)
                    current_sum += n
                
                last_num = total - current_sum
                # ถ้าเลขสุดท้ายติดลบ หรือโดดเกินไป ให้จัดใหม่แบบง่ายๆ
                if last_num <= 0 or abs(last_num - target_avg) > 30:
                    nums = [target_avg - 5, target_avg + 10, target_avg - 10, target_avg + 5][:items_count]
                    nums[-1] = total - sum(nums[:-1])
                    
                random.shuffle(nums)
                nums_str = ", ".join(map(str, nums))
                
                q = f"จงหา <b>'ค่าเฉลี่ย'</b> ของชุดข้อมูลต่อไปนี้: <b style='color:#2980b9;'>{nums_str}</b>"
                
                sol = f"""<span style='color:#2c3e50;'>
                <div style='background-color:#e8f8f5; border-left:4px solid #1abc9c; padding:10px; margin-bottom:15px; border-radius:4px;'>
                💡 <b>สูตรการหาค่าเฉลี่ย:</b><br>
                ค่าเฉลี่ย = (ผลรวมของข้อมูลทั้งหมด) ÷ (จำนวนของข้อมูล)
                </div>
                <b>วิธีทำอย่างละเอียด:</b><br>
                👉 <b>ขั้นที่ 1: หาผลรวมของข้อมูลทั้งหมด</b><br>
                &nbsp;&nbsp;&nbsp;&nbsp;นำ {nums_str.replace(', ', ' + ')} = <b>{total}</b><br><br>
                👉 <b>ขั้นที่ 2: นับจำนวนข้อมูล</b><br>
                &nbsp;&nbsp;&nbsp;&nbsp;ข้อมูลชุดนี้มีทั้งหมด <b>{items_count}</b> จำนวน<br><br>
                👉 <b>ขั้นที่ 3: นำผลรวมหารด้วยจำนวนข้อมูล</b><br>
                &nbsp;&nbsp;&nbsp;&nbsp;{total} ÷ {items_count} = <b>{target_avg}</b><br><br>
                <b>ตอบ: ค่าเฉลี่ยของข้อมูลชุดนี้คือ {target_avg}</b></span>"""



            elif actual_sub_t == "ความน่าจะเป็นเบื้องต้น (สุ่มหยิบของ)":
                colors = ["สีแดง", "สีฟ้า", "สีเขียว", "สีเหลือง"]
                selected_colors = random.sample(colors, 3)
                
                c1_qty = random.randint(3, 8)
                c2_qty = random.randint(2, 6)
                c3_qty = random.randint(1, 4)
                
                color_counts = {selected_colors[0]: c1_qty, selected_colors[1]: c2_qty, selected_colors[2]: c3_qty}
                total_marbles = sum(color_counts.values())
                
                target_color = random.choice(selected_colors)
                target_qty = color_counts[target_color]
                
                gcd_val = math.gcd(target_qty, total_marbles)
                ans_n, ans_d = target_qty // gcd_val, total_marbles // gcd_val
                ans_str = f"{ans_n}/{ans_d}"
                
                svg = draw_marbles_box_svg(color_counts)
                
                q = f"ในกล่องทึบใบหนึ่งมีลูกแก้วสีต่างๆ ดังภาพ หากสุ่มหยิบลูกแก้วขึ้นมา 1 ลูก โอกาสที่จะหยิบได้ลูกแก้ว <b><span style='color:#e74c3c;'>{target_color}</span></b> คิดเป็นเศษส่วนเท่าใด?<br>{svg}"
                
                sol = f"""<span style='color:#2c3e50;'>
                <div style='background-color:#fef5e7; border-left:4px solid #e67e22; padding:10px; margin-bottom:15px; border-radius:4px;'>
                💡 <b>หลักความน่าจะเป็นเบื้องต้น:</b><br>
                โอกาส (ความน่าจะเป็น) = (สิ่งที่สนใจ) ÷ (สิ่งที่เป็นไปได้ทั้งหมด)
                </div>
                <b>วิธีทำอย่างละเอียด:</b><br>
                👉 <b>ขั้นที่ 1: หาจำนวนลูกแก้วทั้งหมด (เหตุการณ์ที่เป็นไปได้ทั้งหมด)</b><br>
                &nbsp;&nbsp;&nbsp;&nbsp;ลูกแก้วในกล่องมี {selected_colors[0]} {c1_qty} ลูก, {selected_colors[1]} {c2_qty} ลูก, {selected_colors[2]} {c3_qty} ลูก<br>
                &nbsp;&nbsp;&nbsp;&nbsp;รวมทั้งหมด = <b>{total_marbles}</b> ลูก<br><br>
                👉 <b>ขั้นที่ 2: หาจำนวนลูกแก้วสีที่โจทย์ถาม (เหตุการณ์ที่สนใจ)</b><br>
                &nbsp;&nbsp;&nbsp;&nbsp;โจทย์ถามหา <b>{target_color}</b> ซึ่งมีอยู่ <b>{target_qty}</b> ลูก<br><br>
                👉 <b>ขั้นที่ 3: เขียนเป็นเศษส่วนและตัดทอน</b><br>
                &nbsp;&nbsp;&nbsp;&nbsp;โอกาสที่จะหยิบได้ = {draw_frac(target_qty, total_marbles)}<br>
                """
                if gcd_val > 1:
                    sol += f"&nbsp;&nbsp;&nbsp;&nbsp;ตัดทอนเป็นเศษส่วนอย่างต่ำโดยใช้แม่ {gcd_val} หาร จะได้ = <b>{draw_frac(ans_n, ans_d)}</b><br><br>"
                sol += f"<b>ตอบ: โอกาสที่จะได้{target_color}คือ {ans_str}</b></span>"



            elif actual_sub_t == "โจทย์ปัญหาพื้นที่และความยาวรอบรูป":
                # ป.5 จะเริ่มมีโจทย์พลิกแพลง เช่น ให้เส้นรอบรูปมา ถามหาพื้นที่
                scenario = random.choice([1, 2])
                
                if scenario == 1:
                    # ให้พื้นที่และด้านกว้างมา ถามหาความยาวรอบรูป
                    w = random.randint(5, 15)
                    l = random.randint(w + 2, w + 15)
                    area = w * l
                    peri = 2 * (w + l)
                    
                    q = f"สนามหญ้ารูปสี่เหลี่ยมผืนผ้าแห่งหนึ่งมี <b>พื้นที่ {area} ตารางเมตร</b> ถ้ารู้ว่าสนามหญ้ากว้าง <b>{w} เมตร</b> <br>สนามหญ้าแห่งนี้จะมีความยาวรอบรูปกี่เมตร?"
                    
                    sol = f"""<span style='color:#2c3e50;'>
                    <div style='background-color:#ebf5fb; border-left:4px solid #3498db; padding:10px; margin-bottom:15px; border-radius:4px;'>
                    💡 <b>เทคนิคย้อนกลับ (Reverse Engineering):</b><br>
                    โจทย์ให้พื้นที่มาก่อน เราต้องใช้สูตรพื้นที่ <i>(กว้าง × ยาว = พื้นที่)</i> เพื่อหา <b>"ด้านยาว"</b> ที่หายไป จากนั้นจึงจะไปหาความยาวรอบรูปได้
                    </div>
                    <b>วิธีทำอย่างละเอียด:</b><br>
                    👉 <b>ขั้นที่ 1: หาด้านยาวที่หายไป</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;จากสูตร: กว้าง × ยาว = พื้นที่<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;แทนค่า: {w} × ยาว = {area}<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;จะได้: ยาว = {area} ÷ {w} = <b>{l} เมตร</b><br><br>
                    👉 <b>ขั้นที่ 2: หาความยาวรอบรูป</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;สูตร: (กว้าง + ยาว) × 2<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;แทนค่า: ({w} + {l}) × 2 = {w+l} × 2 = <b>{peri} เมตร</b><br><br>
                    <b>ตอบ: ความยาวรอบรูปของสนามหญ้าคือ {peri} เมตร</b></span>"""
                else:
                    # ให้ความยาวรอบรูปจัตุรัสมา ถามหาพื้นที่
                    side = random.randint(8, 25)
                    peri = side * 4
                    area = side * side
                    
                    q = f"กระเบื้องรูปสี่เหลี่ยมจัตุรัสแผ่นหนึ่งมีความยาวรอบรูป <b>{peri} เซนติเมตร</b> กระเบื้องแผ่นนี้มีพื้นที่กี่ตารางเซนติเมตร?"
                    
                    sol = f"""<span style='color:#2c3e50;'>
                    <div style='background-color:#ebf5fb; border-left:4px solid #3498db; padding:10px; margin-bottom:15px; border-radius:4px;'>
                    💡 <b>เทคนิคย้อนกลับ (Reverse Engineering):</b><br>
                    โจทย์ให้ความยาวรอบรูปของสี่เหลี่ยมจัตุรัสมา (ซึ่งเกิดจาก ด้าน × 4) เราต้องนำไป <b>หาร 4</b> เพื่อหาความยาว 1 ด้านก่อน แล้วจึงนำไปหาพื้นที่
                    </div>
                    <b>วิธีทำอย่างละเอียด:</b><br>
                    👉 <b>ขั้นที่ 1: หาความยาวของ 1 ด้าน</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;สี่เหลี่ยมจัตุรัสมี 4 ด้านที่ยาวเท่ากัน<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ความยาว 1 ด้าน = {peri} ÷ 4 = <b>{side} เซนติเมตร</b><br><br>
                    👉 <b>ขั้นที่ 2: หาพื้นที่</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;สูตร: ด้าน × ด้าน<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;แทนค่า: {side} × {side} = <b>{area} ตารางเซนติเมตร</b><br><br>
                    <b>ตอบ: กระเบื้องแผ่นนี้มีพื้นที่ {area} ตารางเซนติเมตร</b></span>"""



            elif actual_sub_t == "เส้นขนานและมุมแย้ง":
                # สุ่มมุมและตำแหน่งของเส้นขนาน
                base_angle = random.randint(45, 135)
                dir_key = random.choice(["dir1", "dir2"])
                angle_type = random.choice(["มุมแย้งภายใน", "มุมภายในที่อยู่บนข้างเดียวกันของเส้นตัด", "มุมสมนัย (มุมแย้งภายนอก)"])
                
                if dir_key == "dir1":
                    pos_acute = ["TR_ext", "BL_int", "TL_int", "BR_ext"]
                else:
                    pos_acute = ["TL_ext", "BR_int", "TR_int", "BL_ext"]

                if angle_type == "มุมแย้งภายใน":
                    # มุมแย้งจะเท่ากัน
                    pos1 = "TL_int"
                    pos2 = "BR_int" if dir_key == "dir2" else "BL_int" # ปรับตำแหน่งให้เป็นมุมแย้ง
                    ans_val = base_angle
                    reason = "มุมแย้งจะมีขนาดเท่ากัน"
                    eq_str = f"x = {base_angle}°"
                
                elif angle_type == "มุมภายในที่อยู่บนข้างเดียวกันของเส้นตัด":
                    # มุมภายในรวมกันได้ 180
                    pos1 = "TL_int"
                    pos2 = "BL_int" if dir_key == "dir2" else "TR_int"
                    ans_val = 180 - base_angle
                    reason = "มุมภายในที่อยู่บนข้างเดียวกันของเส้นตัดรวมกันจะได้ 180°"
                    eq_str = f"x = 180° - {base_angle}° = {ans_val}°"
                    
                else:
                    # สมนัย/มุมตรงข้าม
                    pos1 = "TL_ext" if dir_key == "dir2" else "TR_ext"
                    pos2 = "TL_int" if dir_key == "dir2" else "TR_int"
                    ans_val = base_angle
                    reason = "มุมภายนอกและมุมภายในที่อยู่ตรงข้ามกันบนข้างเดียวกันของเส้นตัด (มุมสมนัย) มีขนาดเท่ากัน"
                    eq_str = f"x = {base_angle}°"

                svg = draw_parallel_svg(dir_key, pos1, base_angle, pos2, "x")
                
                q = f"กำหนดให้เส้นตรง AB ขนานกับเส้นตรง CD จากภาพจงหาขนาดของมุม <b>x</b><br>{svg}"
                
                sol = f"""<span style='color:#2c3e50;'>
                <div style='background-color:#fef5e7; border-left:4px solid #e67e22; padding:10px; margin-bottom:15px; border-radius:4px;'>
                💡 <b>สมบัติของเส้นขนาน:</b><br>
                เมื่อมีเส้นตรงเส้นหนึ่งตัดเส้นขนานคู่หนึ่ง <b>{reason}</b>
                </div>
                <b>วิธีทำ:</b><br>
                👉 พิจารณาตำแหน่งของมุม {base_angle}° และมุม x พบว่าเป็นความสัมพันธ์แบบ <b>{angle_type}</b><br>
                👉 ดังนั้น <b>{eq_str}</b><br><br>
                <b>ตอบ: ขนาดของมุม x คือ {ans_val}°</b></span>"""



            elif actual_sub_t == "ปริมาตรและความจุทรงสี่เหลี่ยมมุมฉาก":
                scenario = random.choice(["volume", "water"])
                
                w = random.randint(10, 30)
                l = random.randint(w + 5, 50)
                h = random.randint(15, 40)
                
                if scenario == "volume":
                    vol = w * l * h
                    svg = draw_prism_svg(f"กว้าง {w} ซม.", f"ยาว {l} ซม.", f"สูง {h} ซม.", is_water=False)
                    q = f"กล่องทรงสี่เหลี่ยมมุมฉากใบหนึ่งมีขนาดดังภาพ กล่องใบนี้มีความจุ (ปริมาตร) ทั้งหมดกี่ลูกบาศก์เซนติเมตร?<br>{svg}"
                    
                    sol = f"""<span style='color:#2c3e50;'>
                    <div style='background-color:#e8f8f5; border-left:4px solid #1abc9c; padding:10px; margin-bottom:15px; border-radius:4px;'>
                    💡 <b>สูตรหาปริมาตรทรงสี่เหลี่ยมมุมฉาก:</b><br>
                    ปริมาตร = ความกว้าง × ความยาว × ความสูง
                    </div>
                    <b>วิธีทำอย่างละเอียด:</b><br>
                    👉 <b>ขั้นที่ 1: สกัดข้อมูลจากภาพ</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ความกว้าง = {w} ซม., ความยาว = {l} ซม., ความสูง = {h} ซม.<br><br>
                    👉 <b>ขั้นที่ 2: แทนค่าในสูตร</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;{w} × {l} × {h} = <b>{vol:,}</b> ลูกบาศก์เซนติเมตร<br><br>
                    <b>ตอบ: ความจุกระดาษของกล่องใบนี้คือ {vol:,} ลูกบาศก์เซนติเมตร</b></span>"""
                else:
                    # ระดับน้ำ
                    h_water = random.randint(5, h - 5)
                    vol_water = w * l * h_water
                    svg = draw_prism_svg(f"กว้าง {w} ซม.", f"ยาว {l} ซม.", f"ระดับน้ำสูง {h_water} ซม.", is_water=True)
                    q = f"ตู้ปลาทรงสี่เหลี่ยมมุมฉาก มีน้ำบรรจุอยู่ตามระดับในภาพ ปริมาตรของน้ำในตู้ปลาคือเท่าใด?<br>{svg}"
                    
                    sol = f"""<span style='color:#2c3e50;'>
                    <div style='background-color:#e8f8f5; border-left:4px solid #1abc9c; padding:10px; margin-bottom:15px; border-radius:4px;'>
                    💡 <b>ข้อควรระวังเรื่องระดับน้ำ:</b><br>
                    การหาปริมาตรน้ำ ให้ใช้ <b>"ความสูงของระดับน้ำ"</b> ไม่ใช่ความสูงของตู้ปลาทั้งหมด! ส่วนความกว้างและความยาวจะเท่ากับขนาดของตู้
                    </div>
                    <b>วิธีทำอย่างละเอียด:</b><br>
                    👉 <b>ขั้นที่ 1: สกัดข้อมูล</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ความกว้างตู้ = {w} ซม., ความยาวตู้ = {l} ซม., <b>ความสูงของน้ำ = {h_water} ซม.</b><br><br>
                    👉 <b>ขั้นที่ 2: ใช้สูตร กว้าง × ยาว × สูง (ของน้ำ)</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;{w} × {l} × {h_water} = <b>{vol_water:,}</b> ลูกบาศก์เซนติเมตร<br><br>
                    <b>ตอบ: ปริมาตรของน้ำคือ {vol_water:,} ลูกบาศก์เซนติเมตร</b></span>"""



            elif actual_sub_t == "การเขียนเศษส่วนในรูปร้อยละ":
                # ป.5 จะเน้นตัวส่วนที่เป็นพหุคูณของ 100 เช่น 2, 4, 5, 10, 20, 25, 50
                d = random.choice([2, 4, 5, 10, 20, 25, 50])
                n = random.randint(1, d - 1)
                
                multiplier = 100 // d
                percent_val = n * multiplier
                
                q = f"จงเขียนเศษส่วน {draw_frac(n, d)} ให้อยู่ในรูปของ <b>ร้อยละ (เปอร์เซ็นต์)</b>"
                
                sol = f"""<span style='color:#2c3e50;'>
                <div style='background-color:#fcf3cf; border-left:4px solid #f1c40f; padding:10px; margin-bottom:15px; border-radius:4px;'>
                💡 <b>เทคนิคการแปลงร้อยละ:</b><br>
                คำว่า "ร้อยละ" หรือ "%" หมายถึง <b>"ส่วนเป็น 100"</b> ดังนั้นเราต้องหาตัวเลขมาคูณตัวส่วนให้กลายเป็น 100 ให้ได้
                </div>
                <b>วิธีทำอย่างละเอียด:</b><br>
                👉 <b>ขั้นที่ 1: หาตัวเลขมาคูณให้ส่วนเป็น 100</b><br>
                &nbsp;&nbsp;&nbsp;&nbsp;ตัวส่วนคือ <b>{d}</b> นำไปคูณกับอะไรได้ 100? ➔ (100 ÷ {d} = <b style='color:#e74c3c;'>{multiplier}</b>)<br><br>
                👉 <b>ขั้นที่ 2: นำไปคูณทั้งเศษและส่วน</b><br>
                &nbsp;&nbsp;&nbsp;&nbsp;{draw_frac(f"{n} × <b style='color:#e74c3c;'>{multiplier}</b>", f"{d} × <b style='color:#e74c3c;'>{multiplier}</b>")} = <b style='color:#2980b9;'>{draw_frac(percent_val, 100)}</b><br><br>
                👉 <b>ขั้นที่ 3: สรุปผล</b><br>
                &nbsp;&nbsp;&nbsp;&nbsp;เมื่อส่วนเป็น 100 แล้ว สามารถนำตัวเศษมาเขียนเป็นร้อยละได้เลย<br>
                &nbsp;&nbsp;&nbsp;&nbsp;➔ <b>ร้อยละ {percent_val}</b> หรือ <b>{percent_val}%</b><br><br>
                <b>ตอบ: ร้อยละ {percent_val} (หรือ {percent_val}%)</b></span>"""



            elif actual_sub_t == "การแก้สมการ (คูณ/หาร)":
                mode = random.choice(["mul", "div"])
                var = random.choice(["a", "b", "m", "x", "y"])
                
                ans_val = random.randint(12, 60)
                
                if mode == "mul":
                    coef = random.randint(3, 15)
                    res = coef * ans_val
                    q = f"จงแก้สมการเพื่อหาค่าของ <b>{var}</b><br><span style='font-size:24px;'><b>{coef}{var} = {res}</b></span>"
                    
                    sol = f"""<span style='color:#2c3e50;'>
                    <div style='background-color:#fef5e7; border-left:4px solid #e67e22; padding:10px; margin-bottom:15px; border-radius:4px;'>
                    💡 <b>หลักการแก้สมการ:</b><br>
                    ย้ายข้างตัวเลขที่อยู่กับตัวแปรไปอีกฝั่ง โดยต้อง <b>"เปลี่ยนเครื่องหมายให้เป็นตรงข้าม"</b><br>
                    (จาก คูณ เปลี่ยนเป็น หาร / จาก หาร เปลี่ยนเป็น คูณ)
                    </div>
                    <b>วิธีทำอย่างละเอียด:</b><br>
                    👉 <b>ขั้นที่ 1: วิเคราะห์สมการ</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;{coef}{var} หมายถึง {coef} <b>คูณ</b> อยู่กับ {var}<br><br>
                    👉 <b>ขั้นที่ 2: ย้ายข้าง</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ย้าย {coef} ไปอีกฝั่ง จาก <b>"คูณ"</b> ต้องเปลี่ยนเป็น <b>"หาร"</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;{var} = {res} ÷ {coef}<br><br>
                    👉 <b>ขั้นที่ 3: คำนวณผลลัพธ์</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;{var} = <b>{ans_val}</b><br><br>
                    <b>ตอบ: {var} = {ans_val}</b></span>"""
                else:
                    divisor = random.randint(3, 12)
                    dividend = ans_val
                    res = dividend
                    
                    q = f"จงแก้สมการเพื่อหาค่าของ <b>{var}</b><br><span style='font-size:24px;'><b>{draw_frac(var, divisor)} = {res}</b></span>"
                    
                    sol = f"""<span style='color:#2c3e50;'>
                    <div style='background-color:#fef5e7; border-left:4px solid #e67e22; padding:10px; margin-bottom:15px; border-radius:4px;'>
                    💡 <b>หลักการแก้สมการ:</b><br>
                    ย้ายข้างตัวเลขที่อยู่กับตัวแปรไปอีกฝั่ง โดยต้อง <b>"เปลี่ยนเครื่องหมายให้เป็นตรงข้าม"</b><br>
                    (จาก คูณ เปลี่ยนเป็น หาร / จาก หาร เปลี่ยนเป็น คูณ)
                    </div>
                    <b>วิธีทำอย่างละเอียด:</b><br>
                    👉 <b>ขั้นที่ 1: วิเคราะห์สมการ</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;{draw_frac(var, divisor)} หมายถึง {var} กำลังถูก <b>หาร</b> ด้วย {divisor}<br><br>
                    👉 <b>ขั้นที่ 2: ย้ายข้าง</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ย้าย {divisor} ไปอีกฝั่ง จาก <b>"หาร"</b> ต้องเปลี่ยนเป็น <b>"คูณ"</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;{var} = {res} × {divisor}<br><br>
                    👉 <b>ขั้นที่ 3: คำนวณผลลัพธ์</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;{var} = <b>{res * divisor}</b><br><br>
                    <b>ตอบ: {var} = {res * divisor}</b></span>"""



# ================= หมวดที่ 4: เตรียมสอบเข้า ม.1 Gifted (ป.5) =================
            elif actual_sub_t == "โจทย์ปัญหา ห.ร.ม. และ ค.ร.น.":
                prob_type = random.choice(["gcd", "lcm"])
                
                if prob_type == "gcd":
                    # โจทย์ปัญหา ห.ร.ม. (แบ่งของให้ได้มากที่สุด)
                    gcd_target = random.choice([4, 5, 6, 8, 10, 12, 15])
                    n1 = gcd_target * random.choice([2, 3, 4])
                    n2 = gcd_target * random.choice([5, 6, 7])
                    n3 = gcd_target * random.choice([8, 9, 11])
                    
                    items = ["ส้ม", "แอปเปิ้ล", "มังคุด"]
                    random.shuffle(items)
                    
                    q = f"แม่ค้ามี{items[0]} <b>{n1}</b> ผล, {items[1]} <b>{n2}</b> ผล และ{items[2]} <b>{n3}</b> ผล ต้องการจัดใส่ถาด ถาดละเท่าๆ กัน โดยไม่ปนกันและไม่มีผลไม้เหลืออยู่เลย<br>แม่ค้าจะจัดผลไม้ได้ <b>มากที่สุด</b> ถาดละกี่ผล?"
                    
                    html_div, divisors, _ = render_short_div([n1, n2, n3], mode="gcd")
                    ans = math.prod(divisors) if divisors else gcd_target
                    
                    sol = f"""<span style='color:#2c3e50;'>
                    <div style='background-color:#fcf3cf; border-left:4px solid #f1c40f; padding:10px; margin-bottom:15px; border-radius:4px;'>
                    💡 <b>วิเคราะห์คีย์เวิร์ด:</b><br>
                    คำว่า <b>"แบ่งเท่าๆ กันให้ได้มากที่สุดโดยไม่เหลือเศษ"</b> เป็นสัญญาณว่าต้องใช้ <b>ห.ร.ม. (หาร่วมมาก)</b>
                    </div>
                    <b>วิธีทำ: ตั้งหารสั้นเพื่อหา ห.ร.ม. ของ {n1}, {n2}, {n3}</b>
                    {html_div}
                    👉 นำตัวหารทั้งหมดมาคูณกัน: {" × ".join(map(str, divisors))} = <b>{ans}</b><br><br>
                    <b>ตอบ: จะจัดผลไม้ได้มากที่สุดถาดละ {ans} ผล</b></span>"""
                
                else:
                    # โจทย์ปัญหา ค.ร.น. (ออกพร้อมกัน)
                    lcm_target = random.choice([60, 120, 180, 240]) # นาที
                    times = []
                    if lcm_target == 60: times = [12, 15, 20]
                    elif lcm_target == 120: times = [15, 24, 40]
                    elif lcm_target == 180: times = [20, 36, 45]
                    else: times = [30, 40, 60]
                    
                    t1, t2, t3 = times[0], times[1], times[2]
                    
                    start_h = random.randint(6, 10)
                    start_m = random.choice([0, 15, 30])
                    
                    # คำนวณเวลาถัดไป
                    total_minutes = start_h * 60 + start_m + lcm_target
                    next_h = (total_minutes // 60) % 24
                    next_m = total_minutes % 60
                    
                    start_str = f"{start_h:02d}.{start_m:02d}"
                    next_str = f"{next_h:02d}.{next_m:02d}"
                    
                    q = f"รถโดยสาร 3 สาย ออกจากสถานีทุกๆ <b>{t1} นาที</b>, <b>{t2} นาที</b> และ <b>{t3} นาที</b> ตามลำดับ ถ้ารถทั้งสามสายออกพร้อมกันครั้งแรกเวลา <b>{start_str} น.</b><br>รถทั้งสามสายจะออกจากสถานีพร้อมกันอีกครั้งในเวลาใด?"
                    
                    html_div, divisors, remainders = render_short_div([t1, t2, t3], mode="lcm")
                    ans_lcm = math.prod(divisors) * math.prod(remainders)
                    
                    sol = f"""<span style='color:#2c3e50;'>
                    <div style='background-color:#ebf5fb; border-left:4px solid #3498db; padding:10px; margin-bottom:15px; border-radius:4px;'>
                    💡 <b>วิเคราะห์คีย์เวิร์ด:</b><br>
                    คำว่า <b>"เหตุการณ์ที่จะเกิดขึ้นพร้อมกันอีกครั้งในอนาคต"</b> เป็นสัญญาณว่าต้องใช้ <b>ค.ร.น. (คูณร่วมน้อย)</b>
                    </div>
                    <b>วิธีทำ: ตั้งหารสั้นเพื่อหา ค.ร.น. ของ {t1}, {t2}, {t3}</b>
                    {html_div}
                    👉 นำตัวหารและเศษมาคูณกัน: {" × ".join(map(str, divisors))} × {" × ".join(map(str, remainders))} = <b>{ans_lcm}</b> นาที<br>
                    👉 แปลง {ans_lcm} นาที เป็นชั่วโมง ➔ {ans_lcm} ÷ 60 = <b>{ans_lcm//60} ชั่วโมง</b><br>
                    👉 นับต่อจากเวลา {start_str} น. ไปอีก {ans_lcm//60} ชั่วโมง จะตรงกับเวลา <b>{next_str} น.</b><br><br>
                    <b>ตอบ: รถจะออกพร้อมกันอีกครั้งเวลา {next_str} น.</b></span>"""



            elif actual_sub_t == "โจทย์ปัญหาคลาสสิก (สมการประยุกต์)":
                # โจทย์หัวขาสัตว์ ยอดฮิตสอบเข้า ม.1
                animals = [("ไก่", 2, "วัว", 4), ("นก", 2, "สุนัข", 4), ("เป็ด", 2, "หมู", 4)]
                a1_name, a1_legs, a2_name, a2_legs = random.choice(animals)
                
                a1_count = random.randint(15, 40)
                a2_count = random.randint(10, 30)
                
                total_heads = a1_count + a2_count
                total_legs = (a1_count * a1_legs) + (a2_count * a2_legs)
                
                q = f"ฟาร์มแห่งหนึ่งมี{a1_name}และ{a2_name}รวมกันอยู่ <b>{total_heads} ตัว</b> ถ้านับขาสัตว์ทั้งสองชนิดรวมกันจะได้ <b>{total_legs} ขา</b><br>จงหาว่าฟาร์มแห่งนี้มี <b>{a2_name}</b> กี่ตัว?"
                
                # วิธีคิดลัดแบบประถม (สมมติให้เป็นสัตว์ขาเตี้ยทั้งหมด)
                assume_legs = total_heads * a1_legs
                diff_legs = total_legs - assume_legs
                leg_diff_per_animal = a2_legs - a1_legs
                ans_a2 = diff_legs // leg_diff_per_animal
                
                sol = f"""<span style='color:#2c3e50;'>
                <div style='background-color:#fcf3cf; border-left:4px solid #f1c40f; padding:10px; margin-bottom:15px; border-radius:4px;'>
                💡 <b>เทคนิคคิดลัด (ไม่ต้องตั้งสมการ X, Y):</b><br>
                ให้ <b>"สมมติว่าเป็นสัตว์ที่มีขาน้อยกว่าทั้งหมด"</b> แล้วดูว่าขาขาดไปเท่าไหร่ ขาที่ขาดไปนั้นคือขาของสัตว์ชนิดที่มีขามากกว่าที่ซ่อนอยู่นั่นเอง!
                </div>
                <b>วิธีทำอย่างละเอียด:</b><br>
                👉 <b>ขั้นที่ 1: สมมติว่าเป็น{a1_name}ทั้งหมด</b><br>
                &nbsp;&nbsp;&nbsp;&nbsp;ถ้ามี{a1_name}ทั้งหมด {total_heads} ตัว จะมีขารวม {total_heads} × {a1_legs} = <b>{assume_legs} ขา</b><br><br>
                👉 <b>ขั้นที่ 2: หาจำนวนขาที่หายไปจากความจริง</b><br>
                &nbsp;&nbsp;&nbsp;&nbsp;แต่ความจริงมี {total_legs} ขา แสดงว่าขาหายไป {total_legs} - {assume_legs} = <b>{diff_legs} ขา</b><br><br>
                👉 <b>ขั้นที่ 3: แลกเปลี่ยนสัตว์เพื่อเพิ่มขา</b><br>
                &nbsp;&nbsp;&nbsp;&nbsp;การเปลี่ยน{a1_name} 1 ตัว เป็น{a2_name} 1 ตัว จะได้ขาเพิ่มขึ้น {a2_legs} - {a1_legs} = <b>{leg_diff_per_animal} ขา</b><br>
                &nbsp;&nbsp;&nbsp;&nbsp;ต้องการขาเพิ่ม {diff_legs} ขา จึงต้องมี{a2_name}ทั้งหมด {diff_legs} ÷ {leg_diff_per_animal} = <b>{ans_a2} ตัว</b><br><br>
                <i>(ตรวจคำตอบ: {a2_name} {ans_a2} ตัว = {ans_a2*a2_legs} ขา, {a1_name} {total_heads-ans_a2} ตัว = {(total_heads-ans_a2)*a1_legs} ขา, รวม = {ans_a2*a2_legs + (total_heads-ans_a2)*a1_legs} ขา ตรงเป๊ะ!)</i><br><br>
                <b>ตอบ: มี{a2_name}ทั้งหมด {ans_a2} ตัว</b></span>"""



            elif actual_sub_t == "แบบรูปและอนุกรม (Number Patterns)":
                pattern_type = random.choice(["arithmetic", "geometric", "quadratic"])
                
                if pattern_type == "arithmetic":
                    start = random.randint(5, 50)
                    diff = random.randint(3, 15)
                    seq = [start + (i * diff) for i in range(5)]
                    q = f"จงหาจำนวนถัดไปของแบบรูปต่อไปนี้: <br><span style='font-size:24px; color:#2980b9; letter-spacing: 2px;'><b>{seq[0]},  {seq[1]},  {seq[2]},  {seq[3]},  {seq[4]},  <span style='color:#e74c3c;'>?</span></b></span>"
                    ans = seq[4] + diff
                    sol = f"<span style='color:#2c3e50;'><b>วิธีทำ:</b> สังเกตระยะห่างของตัวเลข พบว่าเพิ่มขึ้นทีละ <b>+{diff}</b> เท่าๆ กัน<br>ดังนั้น จำนวนถัดไปคือ {seq[4]} + {diff} = <b>{ans}</b></span>"
                
                elif pattern_type == "geometric":
                    start = random.randint(2, 5)
                    mult = random.choice([2, 3])
                    seq = [start * (mult ** i) for i in range(5)]
                    q = f"จงหาจำนวนถัดไปของแบบรูปต่อไปนี้: <br><span style='font-size:24px; color:#2980b9; letter-spacing: 2px;'><b>{seq[0]},  {seq[1]},  {seq[2]},  {seq[3]},  {seq[4]},  <span style='color:#e74c3c;'>?</span></b></span>"
                    ans = seq[4] * mult
                    sol = f"<span style='color:#2c3e50;'><b>วิธีทำ:</b> สังเกตระยะห่างของตัวเลข พบว่าเป็นการ <b>คูณด้วย {mult}</b> ต่อเนื่องกันไปเรื่อยๆ ({seq[0]}×{mult}={seq[1]}, {seq[1]}×{mult}={seq[2]}...)<br>ดังนั้น จำนวนถัดไปคือ {seq[4]} × {mult} = <b>{ans}</b></span>"
                
                else: # quadratic (+2, +4, +6...)
                    start = random.randint(2, 10)
                    step_start = random.choice([2, 3])
                    seq = [start]
                    current_step = step_start
                    for _ in range(4):
                        seq.append(seq[-1] + current_step)
                        current_step += step_start # step increases by itself (e.g. +2, +4, +6)
                        
                    q = f"จงหาจำนวนถัดไปของแบบรูปต่อไปนี้: <br><span style='font-size:24px; color:#2980b9; letter-spacing: 2px;'><b>{seq[0]},  {seq[1]},  {seq[2]},  {seq[3]},  {seq[4]},  <span style='color:#e74c3c;'>?</span></b></span>"
                    ans = seq[4] + current_step
                    sol = f"""<span style='color:#2c3e50;'>
                    <div style='background-color:#ebf5fb; border-left:4px solid #3498db; padding:10px; margin-bottom:15px; border-radius:4px;'>
                    💡 <b>เทคนิค: อนุกรมหลายชั้น (ระยะห่างไม่คงที่)</b><br>
                    ให้ลองหา <b>"ส่วนต่าง"</b> ของแต่ละคู่ตัวเลขดูก่อนว่ามีความสัมพันธ์กันอย่างไร
                    </div>
                    <b>วิธีทำ:</b><br>
                    👉 ส่วนต่างของคู่ที่ 1 ({seq[0]} ไป {seq[1]}) คือ <b>+{step_start}</b><br>
                    👉 ส่วนต่างของคู่ที่ 2 ({seq[1]} ไป {seq[2]}) คือ <b>+{step_start*2}</b><br>
                    👉 ส่วนต่างของคู่ที่ 3 ({seq[2]} ไป {seq[3]}) คือ <b>+{step_start*3}</b><br>
                    👉 ส่วนต่างของคู่ที่ 4 ({seq[3]} ไป {seq[4]}) คือ <b>+{step_start*4}</b><br>
                    แสดงว่าส่วนต่างตัวต่อไปจะต้องเป็น <b>+{current_step}</b><br>
                    ดังนั้น จำนวนถัดไปคือ {seq[4]} + {current_step} = <b>{ans}</b></span>"""



            elif actual_sub_t == "มาตราส่วนและทิศทาง":
                scale = random.choice([1000, 50000, 100000, 500000])
                map_dist = round(random.uniform(2.0, 12.5), 1)
                
                # คำนวณระยะทางจริง (ซม. -> กม.)
                real_dist_cm = map_dist * scale
                real_dist_km = real_dist_cm / 100000
                
                scale_str = f"1 : {scale:,}"
                
                q = f"แผนที่ฉบับหนึ่งใช้มาตราส่วน <b>{scale_str}</b> ถ้าวัดระยะทางบนแผนที่จากเมือง A ไปเมือง B ได้ <b>{map_dist} เซนติเมตร</b><br>ระยะทางจริงจากเมือง A ไปเมือง B คิดเป็นกี่<b>กิโลเมตร</b>?"
                
                sol = f"""<span style='color:#2c3e50;'>
                <div style='background-color:#e8f8f5; border-left:4px solid #1abc9c; padding:10px; margin-bottom:15px; border-radius:4px;'>
                💡 <b>ความรู้เรื่องมาตราส่วน:</b><br>
                มาตราส่วน {scale_str} หมายความว่า ระยะทางบนแผนที่ 1 ซม. เท่ากับ ระยะทางจริง {scale:,} ซม.<br>
                <b>(จำไว้ว่า: 100,000 ซม. = 1 กิโลเมตร)</b>
                </div>
                <b>วิธีทำอย่างละเอียด:</b><br>
                👉 <b>ขั้นที่ 1: หาระยะทางจริงในหน่วยเซนติเมตร (ซม.)</b><br>
                &nbsp;&nbsp;&nbsp;&nbsp;บนแผนที่ {map_dist} ซม. นำไปคูณกับมาตราส่วน<br>
                &nbsp;&nbsp;&nbsp;&nbsp;{map_dist} × {scale:,} = <b>{real_dist_cm:,.0f} เซนติเมตร</b><br><br>
                👉 <b>ขั้นที่ 2: แปลงหน่วยจาก เซนติเมตร เป็น กิโลเมตร</b><br>
                &nbsp;&nbsp;&nbsp;&nbsp;เนื่องจาก 1 กม. = 100,000 ซม. จึงต้องนำไป <b>หารด้วย 100,000</b><br>
                &nbsp;&nbsp;&nbsp;&nbsp;{real_dist_cm:,.0f} ÷ 100,000 = <b>{real_dist_km:,.2f} กิโลเมตร</b><br><br>
                <b>ตอบ: ระยะทางจริงคือ {real_dist_km:,.2f} กิโลเมตร</b></span>"""



            elif actual_sub_t == "เรขาคณิตประยุกต์ (หาพื้นที่แรเงา)":
                scenario = random.choice(["frame", "cross_path", "triangle_in_rect"])
                
                if scenario == "frame":
                    w_out = random.randint(20, 40)
                    l_out = random.randint(w_out + 5, 50)
                    border = random.choice([2, 3, 4, 5])
                    
                    w_in = w_out - (2 * border)
                    l_in = l_out - (2 * border)
                    
                    area_out = w_out * l_out
                    area_in = w_in * l_in
                    shaded_area = area_out - area_in
                    
                    svg = draw_shaded_svg("frame", l_out, w_out, border)
                    
                    q = f"จากรูป กรอบรูปสี่เหลี่ยมผืนผ้ามีขนาดภายนอกกว้าง {w_out} ม. ยาว {l_out} ม. มีความกว้างของขอบรอบด้านเท่ากันคือ {border} ม. <br>จงหา <b>พื้นที่ของขอบกรอบรูป (ส่วนที่ระบายสีเทา)</b><br>{svg}"
                    
                    sol = f"""<span style='color:#2c3e50;'>
                    <div style='background-color:#fcf3cf; border-left:4px solid #f1c40f; padding:10px; margin-bottom:15px; border-radius:4px;'>
                    💡 <b>เทคนิคหาพื้นที่แรเงาแบบกรอบ/โดนเจาะ:</b><br>
                    <b>พื้นที่แรเงา = พื้นที่รูปใหญ่ (ด้านนอก) - พื้นที่รูปเล็ก (ด้านใน)</b>
                    </div>
                    <b>วิธีทำอย่างละเอียด:</b><br>
                    👉 <b>ขั้นที่ 1: หาพื้นที่สี่เหลี่ยมรูปใหญ่ (ด้านนอก)</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;กว้าง {w_out} ม. × ยาว {l_out} ม. = <b>{area_out} ตร.ม.</b><br><br>
                    👉 <b>ขั้นที่ 2: หาความยาวด้านของรูปสี่เหลี่ยมเล็ก (ด้านใน)</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;<i>ระวัง! ขอบกินพื้นที่ 2 ฝั่ง (ซ้าย-ขวา / บน-ล่าง) ต้องหักออกฝั่งละ {border} ม.</i><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;กว้างด้านใน = {w_out} - {border} - {border} = <b>{w_in} ม.</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ยาวด้านใน = {l_out} - {border} - {border} = <b>{l_in} ม.</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;พื้นที่รูปเล็ก = {w_in} × {l_in} = <b>{area_in} ตร.ม.</b><br><br>
                    👉 <b>ขั้นที่ 3: จับมาลบกัน</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;พื้นที่แรเงา = {area_out} - {area_in} = <b>{shaded_area} ตร.ม.</b><br><br>
                    <b>ตอบ: พื้นที่ขอบกรอบรูปคือ {shaded_area} ตารางเมตร</b></span>"""
                    
                elif scenario == "cross_path":
                    w = random.randint(20, 50)
                    l = random.randint(w + 5, 80)
                    path = random.choice([2, 3, 4, 5])
                    
                    area_path_h = l * path
                    area_path_v = w * path
                    area_intersect = path * path
                    shaded_area = area_path_h + area_path_v - area_intersect
                    
                    svg = draw_shaded_svg("cross_path", l, w, path)
                    
                    q = f"ลานจอดรถรูปสี่เหลี่ยมผืนผ้ากว้าง {w} ม. ยาว {l} ม. มีการทำทางเดินกากบาทตัดกันตรงกลางซึ่งมีความกว้าง {path} ม. <br>จงหา <b>พื้นที่ของทางเดินทั้งหมด (ส่วนที่ระบายสีเทา)</b><br>{svg}"
                    
                    sol = f"""<span style='color:#2c3e50;'>
                    <div style='background-color:#fcf3cf; border-left:4px solid #f1c40f; padding:10px; margin-bottom:15px; border-radius:4px;'>
                    💡 <b>เทคนิคหาพื้นที่ทางเดินตัดกัน:</b><br>
                    นำพื้นที่ทางเดินแนวนอน + ทางเดินแนวตั้ง <b>แต่ต้องหัก "พื้นที่สี่เหลี่ยมจัตุรัสตรงกลางที่ซ้อนทับกันออก 1 ครั้ง" ด้วย!</b> (เพราะเราบวกซ้ำไป 2 รอบ)
                    </div>
                    <b>วิธีทำอย่างละเอียด:</b><br>
                    👉 <b>ขั้นที่ 1: หาพื้นที่ทางเดินแนวนอน</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ยาว {l} ม. × กว้าง {path} ม. = <b>{area_path_h} ตร.ม.</b><br><br>
                    👉 <b>ขั้นที่ 2: หาพื้นที่ทางเดินแนวตั้ง</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ยาว {w} ม. × กว้าง {path} ม. = <b>{area_path_v} ตร.ม.</b><br><br>
                    👉 <b>ขั้นที่ 3: หักพื้นที่ตรงกลางที่ซ้อนทับกัน</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;ทางตัดกันเป็นสี่เหลี่ยมจัตุรัสขนาด {path} × {path} = <b>{area_intersect} ตร.ม.</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;พื้นที่ทางเดินรวม = {area_path_h} + {area_path_v} - {area_intersect} = <b>{shaded_area} ตร.ม.</b><br><br>
                    <b>ตอบ: พื้นที่ทางเดินทั้งหมดคือ {shaded_area} ตารางเมตร</b></span>"""
                    
                else: # triangle_in_rect
                    w = random.randint(10, 30)
                    l = random.randint(w + 5, 40)
                    rect_area = w * l
                    tri_area = (l * w) // 2
                    
                    svg = draw_shaded_svg("triangle_in_rect", l, w)
                    
                    q = f"กระดาษรูปสี่เหลี่ยมผืนผ้ากว้าง {w} นิ้ว ยาว {l} นิ้ว ถูกตัดเป็นรูปสามเหลี่ยมดังภาพ (ส่วนที่ระบายสีขาว) จงหาว่า<b>พื้นที่ส่วนที่เหลือ (สีเทา)</b> มีขนาดกี่ตารางนิ้ว?<br>{svg}"
                    
                    sol = f"""<span style='color:#2c3e50;'>
                    <div style='background-color:#e8f8f5; border-left:4px solid #1abc9c; padding:10px; margin-bottom:15px; border-radius:4px;'>
                    💡 <b>เทคนิคลับเรขาคณิต:</b><br>
                    ถ้าเรามีรูปสามเหลี่ยมที่วาดแนบพอดีกึ่งกลางสี่เหลี่ยมมุมฉากแบบนี้ <b>พื้นที่ของสามเหลี่ยมจะเท่ากับ "ครึ่งหนึ่ง" ของพื้นที่สี่เหลี่ยมเสมอ!</b> แสดงว่าพื้นที่ส่วนที่เหลือ (สีเทา) ก็จะเท่ากับอีกครึ่งหนึ่งพอดี
                    </div>
                    <b>วิธีทำอย่างละเอียด:</b><br>
                    👉 <b>ขั้นที่ 1: หาพื้นที่สี่เหลี่ยมผืนผ้าทั้งหมด</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;กว้าง {w} นิ้ว × ยาว {l} นิ้ว = <b>{rect_area} ตร.นิ้ว</b><br><br>
                    👉 <b>ขั้นที่ 2: แบ่งครึ่งพื้นที่</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;พื้นที่สีเทา = ครึ่งหนึ่งของสี่เหลี่ยม ➔ {rect_area} ÷ 2 = <b>{tri_area} ตร.นิ้ว</b><br><br>
                    <b>ตอบ: พื้นที่ส่วนที่เหลือ (สีเทา) คือ {tri_area} ตารางนิ้ว</b></span>"""

            else:
                q = f"⚠️ [ระบบอยู่ระหว่างการอัปเดต] ไม่พบเงื่อนไขการสร้างโจทย์สำหรับหัวข้อ: <b>{actual_sub_t}</b>"
                sol = "กรุณาเลือกหัวข้ออื่น"

            # ==================================================
            # ระบบเช็คโจทย์ซ้ำ (ยันต์กันค้าง)
            # ==================================================
            if q not in seen: 
                seen.add(q)
                questions.append({"question": q, "solution": sol})
                break 
            elif attempts >= 299:
                questions.append({"question": q, "solution": sol})
                break
                
            attempts += 1  
            
    return questions

# ==========================================
# UI Rendering & Streamlit
# ==========================================
def extract_body(html_str):
    try: return html_str.split('<body>')[1].split('</body>')[0]
    except IndexError: return html_str

def create_page(grade, sub_t, questions, is_key=False, q_margin="20px", ws_height="180px", brand_name=""):
    title = "เฉลยแบบฝึกหัด (Answer Key)" if is_key else "แบบฝึกหัดคณิตศาสตร์"
    student_info = """
        <table style="width: 100%; margin-bottom: 10px; font-size: 18px; border-collapse: collapse;">
            <tr>
                <td style="width: 1%; white-space: nowrap; padding-right: 5px;"><b>ชื่อ-สกุล</b></td>
                <td style="border-bottom: 2px dotted #999; width: 60%;"></td>
                <td style="width: 1%; white-space: nowrap; padding-left: 20px; padding-right: 5px;"><b>ชั้น</b></td>
                <td style="border-bottom: 2px dotted #999; width: 15%;"></td>
                <td style="width: 1%; white-space: nowrap; padding-left: 20px; padding-right: 5px;"><b>เลขที่</b></td>
                <td style="border-bottom: 2px dotted #999; width: 15%;"></td>
            </tr>
        </table>
        """ if not is_key else ""
        
    html = f"""<!DOCTYPE html><html lang="th"><head><meta charset="utf-8">
    <style>
        @page {{ size: A4; margin: 15mm; }}
        body {{ font-family: 'Sarabun', sans-serif; padding: 20px; line-height: 1.6; color: #333; }}
        .header {{ text-align: center; border-bottom: 2px solid #333; margin-bottom: 10px; padding-bottom: 10px; }}
        .q-box {{ margin-bottom: {q_margin}; padding: 10px 15px; page-break-inside: avoid; font-size: 20px; line-height: 1.6; }}
        .workspace {{ height: {ws_height}; border: 2px dashed #bdc3c7; border-radius: 8px; margin: 15px 0; padding: 10px; color: #95a5a6; font-size: 16px; background-color: #fafbfc; }}
        .ans-line {{ margin-top: 10px; border-bottom: 1px dotted #999; width: 80%; height: 30px; font-weight: bold; font-size: 20px; display: flex; align-items: flex-end; padding-bottom: 5px; }}
        .sol-text {{ color: #333; font-size: 18px; display: block; margin-top: 15px; padding: 15px; background-color: #f1f8ff; border-left: 4px solid #3498db; border-radius: 4px; line-height: 1.6; }}
        .page-footer {{ text-align: right; font-size: 14px; color: #95a5a6; margin-top: 20px; border-top: 1px solid #eee; padding-top: 10px; }}
    </style></head><body>
    <div class="header"><h2>{title} - {grade}</h2><p><b>หมวดหมู่:</b> {sub_t}</p></div>
    {student_info}"""
    
    for i, item in enumerate(questions, 1):
        html += f'<div class="q-box"><b>ข้อที่ {i}.</b> '
        
        # 💡 ปรับเงื่อนไขซ่อนพื้นที่ทดเลข ให้ครอบคลุมเนื้อหา ป.5
        hide_ws = False
        if any(keyword in sub_t for keyword in ["(แบบตั้งหลัก)", "หารยาว", "การคูณและการหารทศนิยม", "การบวกและการลบทศนิยม"]):
            hide_ws = True
        elif any(keyword in item["question"] for keyword in ["จงหาผลบวกของ", "จงหาผลลบของ", "จงหาผลคูณของ", "วิธีหารยาว", "ตั้งทด"]):
            hide_ws = True
            
        if is_key:
            if hide_ws: 
                html += f'{item["solution"]}'
            else: 
                html += f'{item["question"]}<div class="sol-text">{item["solution"]}</div>'
        else:
            if hide_ws:
                html += f'{item["question"]}<div class="ans-line">ตอบ: </div>'
            else:
                html += f'{item["question"]}<div class="workspace">พื้นที่สำหรับแสดงวิธีทำอย่างละเอียด...</div><div class="ans-line">ตอบ: </div>'
        html += '</div>'
        
    if brand_name: 
        html += f'<div class="page-footer">&copy; 2026 {brand_name} | สงวนลิขสิทธิ์</div>'
        
    return html + "</body></html>"

# ==========================================
# 4. Streamlit UI (Sidebar & Result Grouping)
# ==========================================
st.sidebar.markdown("## ⚙️ พารามิเตอร์การสร้าง")

# 📚 บังคับเลือกเป็น ป.5 เท่านั้น
selected_grade = st.sidebar.selectbox("📚 เลือกระดับชั้น:", ["ป.5"])

# ดึงหัวข้อหลักจาก ป.5
main_topics_list = list(curriculum_db[selected_grade].keys())
main_topics_list.append("🌟 โหมดพิเศษ (สุ่มทุกเรื่อง)")

selected_main = st.sidebar.selectbox("📂 เลือกหัวข้อหลัก:", main_topics_list)

if selected_main == "🌟 โหมดพิเศษ (สุ่มทุกเรื่อง)":
    selected_sub = "แบบทดสอบรวมปลายภาค"
    st.sidebar.info("💡 โหมดนี้จะสุ่มดึงโจทย์จากทุกเรื่องในชั้นเรียนนี้มายำรวมกัน")
else:
    selected_sub = st.sidebar.selectbox("📝 เลือกหัวข้อย่อย:", curriculum_db[selected_grade][selected_main])

num_input = st.sidebar.number_input("🔢 จำนวนข้อ:", min_value=1, max_value=100, value=10)
st.sidebar.markdown("---")
is_challenge = st.sidebar.toggle("🔥 โหมดชาเลนจ์ (ท้าทาย)", value=False)
if is_challenge:
    st.sidebar.warning("เปิดโหมดชาเลนจ์แล้ว! ตัวเลขจะยากขึ้นและโจทย์จะท้าทายกว่าเดิม")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📏 ตั้งค่าหน้ากระดาษ")
spacing_level = st.sidebar.select_slider(
    "↕️ ความสูงของพื้นที่ทดเลข:", 
    options=["แคบ", "ปานกลาง", "กว้าง", "กว้างพิเศษ"], 
    value="กว้าง" # ป.5 ปกติใช้พื้นที่ทดเยอะ ปรับ default เป็นกว้าง
)

if spacing_level == "แคบ": q_margin, ws_height = "15px", "100px"
elif spacing_level == "ปานกลาง": q_margin, ws_height = "20px", "180px"
elif spacing_level == "กว้าง": q_margin, ws_height = "30px", "280px"
else: q_margin, ws_height = "40px", "400px"

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎨 ตั้งค่าแบรนด์")
brand_name = st.sidebar.text_input("🏷️ ชื่อแบรนด์ / ผู้สอน:", value="บ้านทีเด็ด")

# เปลี่ยนสีปุ่มให้เข้ากับธีม ป.5 (แดง/ส้ม)
if st.sidebar.button("🚀 สั่งสร้างใบงาน ป.5", type="primary", use_container_width=True):
    with st.spinner("กำลังออกแบบรูปภาพและสร้างเฉลยแบบ Step-by-Step..."):
        
        qs = generate_questions_logic("ป.5", selected_main, selected_sub, num_input, is_challenge)
        
        html_w = create_page("ป.5", selected_sub, qs, is_key=False, q_margin=q_margin, ws_height=ws_height, brand_name=brand_name)
        html_k = create_page("ป.5", selected_sub, qs, is_key=True, q_margin=q_margin, ws_height=ws_height, brand_name=brand_name)
        
        st.session_state['worksheet_html'] = html_w
        st.session_state['answerkey_html'] = html_k
        
        ebook_body = f'\n<div class="a4-wrapper">{extract_body(html_w)}</div>\n<div class="a4-wrapper">{extract_body(html_k)}</div>\n'
        
        full_ebook_html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700&display=swap" rel="stylesheet"><style>@page {{ size: A4; margin: 15mm; }} @media screen {{ body {{ font-family: 'Sarabun', sans-serif; background-color: #525659; display: flex; flex-direction: column; align-items: center; padding: 40px 0; margin: 0; }} .a4-wrapper {{ width: 210mm; min-height: 297mm; background: white; margin-bottom: 30px; box-shadow: 0 10px 20px rgba(0,0,0,0.3); padding: 15mm; box-sizing: border-box; }} }} @media print {{ body {{ font-family: 'Sarabun', sans-serif; background: transparent; padding: 0; display: block; margin: 0; }} .a4-wrapper {{ width: 100%; min-height: auto; margin: 0; padding: 0; box-shadow: none; page-break-after: always; }} }} .header {{ text-align: center; border-bottom: 2px solid #333; margin-bottom: 10px; padding-bottom: 10px; }} .q-box {{ margin-bottom: {q_margin}; padding: 10px 15px; page-break-inside: avoid; font-size: 20px; line-height: 1.6; }} .workspace {{ height: {ws_height}; border: 2px dashed #bdc3c7; border-radius: 8px; margin: 15px 0; padding: 10px; color: #95a5a6; font-size: 16px; background-color: #fafbfc; }} .ans-line {{ margin-top: 10px; border-bottom: 1px dotted #999; width: 80%; height: 30px; font-weight: bold; font-size: 20px; display: flex; align-items: flex-end; padding-bottom: 5px; }} .sol-text {{ color: #333; font-size: 18px; display: block; margin-top: 15px; padding: 15px; background-color: #f1f8ff; border-left: 4px solid #3498db; border-radius: 4px; line-height: 1.6; }} .page-footer {{ text-align: right; font-size: 14px; color: #95a5a6; margin-top: 20px; border-top: 1px solid #eee; padding-top: 10px; }} </style></head><body>{ebook_body}</body></html>"""

        filename_base = f"BaanTded_P5_Gifted_{int(time.time())}"
        st.session_state['ebook_html'] = full_ebook_html
        st.session_state['filename_base'] = filename_base
        
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr(f"{filename_base}_Full_EBook.html", full_ebook_html.encode('utf-8'))
            zip_file.writestr(f"{filename_base}_Worksheet.html", html_w.encode('utf-8'))
            zip_file.writestr(f"{filename_base}_AnswerKey.html", html_k.encode('utf-8'))
        st.session_state['zip_data'] = zip_buffer.getvalue()

if 'ebook_html' in st.session_state:
    st.success(f"✅ สร้างใบงานสำเร็จ! ลิขสิทธิ์โดย {brand_name}")
    c1, c2 = st.columns(2)
    with c1:
        st.download_button("📄 โหลดเฉพาะโจทย์", data=st.session_state['worksheet_html'], file_name=f"{st.session_state['filename_base']}_Worksheet.html", mime="text/html", use_container_width=True)
        st.download_button("🔑 โหลดเฉพาะเฉลย", data=st.session_state['answerkey_html'], file_name=f"{st.session_state['filename_base']}_AnswerKey.html", mime="text/html", use_container_width=True)
    with c2:
        st.download_button("📚 โหลดรวมเล่ม E-Book", data=st.session_state['ebook_html'], file_name=f"{st.session_state['filename_base']}_Full_EBook.html", mime="text/html", use_container_width=True)
        st.download_button("🗂️ โหลดแพ็กเกจ (.zip)", data=st.session_state['zip_data'], file_name=f"{st.session_state['filename_base']}.zip", mime="application/zip", use_container_width=True)
    st.markdown("---")
    components.html(st.session_state['ebook_html'], height=800, scrolling=True)
