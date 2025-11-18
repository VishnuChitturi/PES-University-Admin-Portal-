import streamlit as st
import mysql.connector
import pandas as pd
import os
from datetime import date
from PIL import Image
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# ============= CONFIG =============
DB_CONFIG = dict(
    host="localhost",
    user="root",
    password="Steveharrington00",
    database="UniversityDB",
    auth_plugin="mysql_native_password"
)

PHOTOS_DIR = "photos"
IDCARDS_DIR = "id_cards"
os.makedirs(PHOTOS_DIR, exist_ok=True)
os.makedirs(IDCARDS_DIR, exist_ok=True)

ADMIN_ID = "hello_pes"
ADMIN_PASS = "pesu@admin.com"

def get_conn():
    return mysql.connector.connect(**DB_CONFIG)

def save_uploaded_photo(srn, uploaded_file):
    if not uploaded_file:
        return None
    ext = os.path.splitext(uploaded_file.name)[1].lower()
    out_path = os.path.join(PHOTOS_DIR, f"{srn}{ext}")
    image = Image.open(uploaded_file)
    rgb = image.convert("RGB")
    rgb.save(out_path, format="JPEG", quality=85)
    return out_path

def generate_id_card_pdf(srn, student):
    pdf_path = os.path.join(IDCARDS_DIR, f"{srn}_idcard.pdf")
    c = canvas.Canvas(pdf_path, pagesize=letter)
    w, h = letter
    card_w, card_h = 420, 260
    x = (w - card_w) / 2
    y = h - 80 - card_h

    # Simple header
    c.setFillColorRGB(0, 0, 0.6)
    c.rect(x, y + card_h - 50, card_w, 50, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(x + 130, y + card_h - 35, "UNIVERSITY ID CARD")

    # Photo
    photo_path = student.get("photo_path")
    if photo_path and os.path.exists(photo_path):
        c.drawImage(photo_path, x + 12, y + 40, width=120, height=160, preserveAspectRatio=True)

    # Info
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica", 12)
    lines = [
        f"Name: {student.get('student_name','')}",
        f"SRN: {student.get('srn','')}",
        f"Dept: {student.get('dept_name','')}",
        f"Semester: {student.get('semester','')}",
        f"Year: {student.get('year_of_study','')}",
    ]
    tx, ty = x + 150, y + card_h - 80
    for line in lines:
        c.drawString(tx, ty, line)
        ty -= 16

    c.setFont("Helvetica-Oblique", 10)
    c.drawString(x + 12, y + 10, "Issued by: University Admin Office")
    c.save()
    return pdf_path

# ===================================================
# SIMPLE LOGIN PAGE
# ===================================================
st.set_page_config(page_title="University Portal", layout="wide")
st.title("🎓 PES University Admin Portal")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.subheader("Admin Login")
    user = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == ADMIN_ID and password == ADMIN_PASS:
            st.session_state.logged_in = True
            st.success("✅ Login successful! Welcome Admin.")
            st.rerun()
        else:
            st.error("❌ Invalid credentials. Please try again.")
    st.stop()

st.title("🎓 Admin Side Student Details Management Portal")
st.sidebar.title("📁 Menu")

if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.rerun()

choice = st.sidebar.radio("", ["➕ Add Student", "🔍 Search / Edit Student"])

if choice == "➕ Add Student":
    st.header("📝 Admission Form — Add New Student")
    with st.form("add_form"):
        col1, col2 = st.columns([2, 1])
        with col1:
            srn = st.text_input("SRN (e.g. PES1UG23CS001)")
            student_name = st.text_input("Full Name")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            dob = st.date_input("Date of Birth", min_value=date(1999, 1, 1), value=date(2004, 1, 1))
            dept_name = st.selectbox("Department", ["CSE", "AIML", "ECE", "EEE", "ME", "IT"])
            semester = st.selectbox("Semester", [1,2,3,4,5,6,7,8])
            year_of_study = st.selectbox("Year of Study", [1,2,3,4])
            cgpa = st.number_input("Current CGPA", min_value=0.0, max_value=10.0, step=0.01)
        with col2:
            uploaded_photo = st.file_uploader("Upload Photo", type=["jpg", "jpeg", "png"])
            if uploaded_photo:
                st.image(uploaded_photo, width=180)
            hostel = st.selectbox("Hostel", ["None","IT","NB","NBX","MM","IH","MESS"])
            scholarship = st.selectbox("Scholarship", ["None","MRD","CNR","DAC"])
            placement_company = st.text_input("Placement Company (if any)")
            lpa = st.number_input("Package (LPA)", min_value=0.0, step=0.1)
            red_marks = st.number_input("Red Marks", min_value=0, step=1)

        st.divider()
        st.subheader("👨‍👩‍👦 Family & Address")
        pcol1, pcol2 = st.columns(2)
        with pcol1:
            father_name = st.text_input("Father's Name/Guardian's Name *")
            mother_name = st.text_input("Mother's Name")
            parent_contact = st.text_input("Parent Contact No.*")
        with pcol2:
            present_address = st.text_area("Present Address *")
            permanent_address = st.text_area("Permanent Address *")

        submitted = st.form_submit_button("💾 Save Student")

        if submitted:
            if not srn or not student_name:
                st.error("SRN and Full Name are required!")
            else:
                photo_path = save_uploaded_photo(srn, uploaded_photo) if uploaded_photo else None
                dept_map = {"CSE":1, "AIML":2, "ECE":3, "EEE":4, "ME":5, "IT":6}
                dept_id = dept_map.get(dept_name)

                if hostel == "None":
                    hostel_id = None
                else:
                    conn = get_conn()
                    cur = conn.cursor()
                    cur.execute("SELECT hostel_id FROM hostel WHERE hostel_name = %s", (hostel,))
                    row = cur.fetchone()
                    hostel_id = row[0] if row else None
                    cur.close()
                    conn.close()

                try:
                    conn = get_conn()
                    cur = conn.cursor()
                    cur.execute("""
                        INSERT INTO student (srn, student_name, gender, dob, dept_id, semester, year_of_study, hostel_id, 
                        scholarship_award, cgpa, lpa, placement_company, red_marks, permanent_address, present_address,
                        father_name, mother_name, parent_contact, photo_path)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        ON DUPLICATE KEY UPDATE
                        student_name=VALUES(student_name), gender=VALUES(gender), dob=VALUES(dob),
                        dept_id=VALUES(dept_id), semester=VALUES(semester), year_of_study=VALUES(year_of_study),
                        hostel_id=VALUES(hostel_id), scholarship_award=VALUES(scholarship_award),
                        cgpa=VALUES(cgpa), lpa=VALUES(lpa), placement_company=VALUES(placement_company),
                        red_marks=VALUES(red_marks), permanent_address=VALUES(permanent_address),
                        present_address=VALUES(present_address), father_name=VALUES(father_name),
                        mother_name=VALUES(mother_name), parent_contact=VALUES(parent_contact),
                        photo_path=VALUES(photo_path)
                    """, (srn, student_name, gender, dob, dept_id, semester, year_of_study, hostel_id, scholarship, cgpa, lpa,
                          placement_company, red_marks, permanent_address, present_address, father_name, mother_name,
                          parent_contact, photo_path))
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.success("✅ Student added/updated successfully!")
                except mysql.connector.Error as e:
                    st.error("Database Error: " + str(e))

elif choice == "🔍 Search / Edit Student":
    st.header("🔍 Search Student")

    if "search_results" not in st.session_state:
        st.session_state.search_results = []
    if "pdf_path" not in st.session_state:
        st.session_state.pdf_path = None

    srn_search = st.text_input("Enter SRN or part of student name")

    if st.button("Search"):
        conn = get_conn()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT s.*, d.dept_name, h.hostel_name
            FROM student s
            LEFT JOIN department d ON s.dept_id = d.dept_id
            LEFT JOIN hostel h ON s.hostel_id = h.hostel_id
            WHERE s.srn = %s OR s.student_name LIKE %s
        """, (srn_search, f"%{srn_search}%"))
        rows = cur.fetchall()
        cur.close()
        conn.close()

        if not rows:
            st.warning("No matching student found.")
            st.session_state.search_results = []
        else:
            st.session_state.search_results = rows

    if st.session_state.search_results:
        data = st.session_state.search_results[0]
        left, right = st.columns([1, 2])

        with left:
            if data.get("photo_path") and os.path.exists(data["photo_path"]):
                st.image(data["photo_path"], width=200, caption=data["student_name"])
            else:
                st.image("https://via.placeholder.com/200x250.png?text=No+Photo", width=200)

            if st.button("🎫 Generate ID Card", key="gen_id"):
                pdf_path = generate_id_card_pdf(data["srn"], data)
                st.session_state.pdf_path = pdf_path
                st.success("✅ ID Card generated successfully!")

            if st.session_state.pdf_path and os.path.exists(st.session_state.pdf_path):
                with open(st.session_state.pdf_path, "rb") as f:
                    st.download_button("⬇️ Download ID Card", f, file_name=os.path.basename(st.session_state.pdf_path))

        with right:
            st.subheader(f"{data['student_name']} — {data['srn']}")
            st.markdown(f"**Department:** {data['dept_name']} | **Semester:** {data['semester']}")
            st.markdown(f"**CGPA:** {data['cgpa']} | **Placement:** {data['placement_company'] or 'N/A'}")
            st.markdown(f"**Hostel:** {data['hostel_name'] or 'None'} | **Scholarship:** {data['scholarship_award']}")
            st.divider()

            with st.expander("📄 Edit Details", expanded=True):
                new_name = st.text_input("Full Name", data["student_name"])
                new_gender = st.selectbox("Gender", ["Male", "Female", "Other"], 
                    index=["Male", "Female", "Other"].index(data["gender"]))
                dept_options = ["CSE", "AIML", "ECE", "EEE", "ME", "IT"]
                dept_map = {"CSE":1, "AIML":2, "ECE":3, "EEE":4, "ME":5, "IT":6}
                current_dept = data["dept_name"]
                if current_dept not in dept_options:
                    rev_map = {
                        "Computer Science and Engineering":"CSE",
                        "Artificial Intelligence and Machine Learning":"AIML",
                        "Electronics and Communication Engineering":"ECE",
                        "Electrical and Electronics Engineering":"EEE",
                        "Mechanical Engineering":"ME",
                        "Information Technology":"IT"
                    }
                    current_dept = rev_map.get(current_dept, "CSE")

                new_dept = st.selectbox("Department", dept_options, index=dept_options.index(current_dept))
                new_semester = st.selectbox("Semester", [1,2,3,4,5,6,7,8], index=int(data["semester"]) - 1)
                new_year = st.selectbox("Year of Study", [1,2,3,4], index=int(data["year_of_study"]) - 1)
                new_cgpa = st.number_input("CGPA", min_value=0.0, max_value=10.0, value=float(data.get("cgpa", 0.0)))
                new_red = st.number_input("Red Marks", min_value=0, value=int(data.get("red_marks", 0)))
                new_place = st.text_input("Placement Company", data.get("placement_company", ""))
                new_lpa = st.number_input("Package (LPA)", min_value=0.0, step=0.1, value=float(data.get("lpa", 0.0)))
                new_scholar = st.selectbox("Scholarship", ["None", "MRD", "CNR", "DAC"], 
                    index=["None", "MRD", "CNR", "DAC"].index(data.get("scholarship_award", "None")))
                new_hostel = st.text_input("Hostel", data.get("hostel_name", ""))
                new_present = st.text_area("Present Address", data.get("present_address", ""))
                new_permanent = st.text_area("Permanent Address", data.get("permanent_address", ""))
                new_father = st.text_input("Father's Name", data.get("father_name", ""))
                new_mother = st.text_input("Mother's Name", data.get("mother_name", ""))
                new_parent_contact = st.text_input("Parent Contact", data.get("parent_contact", ""))

                update = st.button("💾 Save Changes", key="update_btn")
                if update:
                    new_dept_id = dept_map.get(new_dept, 1)
                    conn = get_conn()
                    cur = conn.cursor()
                    cur.execute("""
                        UPDATE student 
                        SET student_name=%s, gender=%s, dept_id=%s, semester=%s, year_of_study=%s,
                            scholarship_award=%s, cgpa=%s, red_marks=%s, placement_company=%s, 
                            lpa=%s, present_address=%s, permanent_address=%s, father_name=%s, 
                            mother_name=%s, parent_contact=%s
                        WHERE srn=%s
                    """, (new_name, new_gender, new_dept_id, new_semester, new_year, new_scholar, 
                        new_cgpa, new_red, new_place, new_lpa, new_present, new_permanent, 
                        new_father, new_mother, new_parent_contact, data["srn"]))
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.success("✅ Student updated successfully.")
                    st.session_state.search_results = []