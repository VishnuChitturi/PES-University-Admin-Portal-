import streamlit as st
import mysql.connector
import pandas as pd
from datetime import date

# ---------------------- DATABASE CONNECTION ----------------------
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Steveharrington00",
        database="UniversityDB2",
        auth_plugin="mysql_native_password"
    )

# ---------------------- PAGE SETUP ----------------------
st.set_page_config(
    page_title="University Admin Portal",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ---------------------- STYLING ----------------------
st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        }
        .main-title {
            font-size: 42px;
            color: #0d47a1;
            font-weight: 800;
            text-align: center;
            margin-bottom: 10px;
        }
        .sub-title {
            font-size: 22px;
            color: #1976d2;
            font-weight: 600;
            text-align: center;
            margin-bottom: 20px;
        }
        .stButton > button {
            background-color: #1976d2;
            color: white;
            font-weight: 600;
            border-radius: 10px;
            padding: 10px 24px;
        }
        .stButton > button:hover {
            background-color: #1565c0;
            color: white;
            transform: scale(1.02);
        }
    </style>
    <div class="main-title">🎓 University Management Portal</div>
    <div class="sub-title">Admin Dashboard</div>
""", unsafe_allow_html=True)

# ---------------------- NAVIGATION ----------------------
menu = st.sidebar.radio("📋 Select Action", ["➕ Add New Student", "🔍 Search or Edit Student"])

# ---------------------- ADD STUDENT ----------------------
if menu == "➕ Add New Student":
    st.subheader("🧾 Admission Form")

    with st.form("add_student_form"):
        col1, col2 = st.columns(2)
        with col1:
            srn = st.text_input("SRN (e.g., PES1UG23CS001)")
            student_name = st.text_input("Full Name")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            dob = st.date_input("Date of Birth", min_value=date(1999, 1, 1), max_value=date.today())

        with col2:
            dept_map = {
                "CSE": 1,
                "ECE": 2,
                "EEE": 3,
                "MECH": 4,
                "CIVIL": 5,
                "IT": 6
            }
            dept_name = st.selectbox("Department", list(dept_map.keys()))
            dept_id = dept_map[dept_name]
            year_of_study = st.selectbox("Year of Study", ["1", "2", "3", "4"])
            hostel_allotted = st.selectbox("Hostel Allotted", ["None", "IT", "NB", "NBX", "MM", "IH", "MESS"])
            scholarship_award = st.selectbox("Scholarship", ["None", "MRD", "CNR", "DAC"])
            lpa = st.number_input("Package (LPA)", min_value=0.0, max_value=100.0, value=0.0, step=0.1)

        submit = st.form_submit_button("💾 Add Student")

        if submit:
            if srn and student_name:
                conn = get_db_connection()
                cursor = conn.cursor()

                query = """
                    INSERT INTO student (srn, student_name, gender, dob, dept_id, year_of_study, cgpa)
                    VALUES (%s,%s,%s,%s,%s,%s,%s)
                """
                # Set default CGPA as 0 initially
                values = (srn, student_name, gender, dob, dept_id, year_of_study, 0.0)

                try:
                    cursor.execute(query, values)
                    conn.commit()
                    st.success(f"✅ Student {student_name} added successfully!")

                except mysql.connector.Error as err:
                    st.error(f"⚠️ Error: {err}")

                finally:
                    cursor.close()
                    conn.close()
            else:
                st.warning("⚠️ Please fill all mandatory fields!")

# ---------------------- SEARCH / EDIT STUDENT ----------------------
elif menu == "🔍 Search or Edit Student":
    st.subheader("🔎 Search Student Record")

    srn_search = st.text_input("Enter SRN (e.g., PES1UG23CS001)")
    search_btn = st.button("🔍 Search Student")

    if search_btn and srn_search:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM student WHERE srn = %s", (srn_search,))
        record = cursor.fetchone()

        if record:
            st.success(f"✅ Student {record['student_name']} found!")

            with st.form("edit_student_form"):
                st.write("### ✏️ Edit Student Details")

                col1, col2 = st.columns(2)
                with col1:
                    student_name = st.text_input("Full Name", record["student_name"])
                    gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(record["gender"]))
                    dob = st.date_input("Date of Birth", record["dob"], min_value=date(1999, 1, 1))

                with col2:
                    dept_id = st.selectbox("Department", ["CSE", "AIML", "ECE", "EEE", "MECH", "CIVIL", "IT"], index=0)
                    year_of_study = st.selectbox("Year of Study", ["1", "2", "3", "4"], index=int(record["year_of_study"]) - 1)
                    cgpa = st.number_input("CGPA", min_value=0.0, max_value=10.0, value=float(record["cgpa"]), step=0.1)

                update_btn = st.form_submit_button("💾 Save Changes")

                if update_btn:
                    update_query = """
                        UPDATE student SET student_name=%s, gender=%s, dob=%s, dept_id=%s,
                        year_of_study=%s, cgpa=%s WHERE srn=%s
                    """
                    values = (student_name, gender, dob, dept_id, year_of_study, cgpa, srn_search)

                    try:
                        cursor.execute(update_query, values)
                        conn.commit()
                        st.success("✅ Record updated successfully!")
                    except mysql.connector.Error as err:
                        st.error(f"⚠️ Error: {err}")

            cursor.close()
            conn.close()
        else:
            st.error("❌ No student found with that SRN.")
