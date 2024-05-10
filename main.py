from modules.teacher import teacher_page
from modules.student import student_page
from modules.admin import admin_page
import time
import streamlit as st
from db.db import (
    login,
    change_password,
    fetch_staffinfo_by_id,
    fetch_studentinfo_by_id
)

def find_index(lst, value):
    for i in range(len(lst)):
        if lst[i] == value:
            return i



def initialize_variable():
    # Initialize session state attributes
    if 'new_user' not in st.session_state:
        st.session_state.new_user = False
    if 'login' not in st.session_state:
        st.session_state.login = False
    if 'role' not in st.session_state:
        st.session_state.role = None

def main_page():
    if not st.session_state.login:
        st.session_state.uid = st.text_input(label="Enter the ID", key="id")
        password = st.text_input(label="Enter the Password", type="password", key="password")
        role = st.selectbox(label="Who are You?", options=("student", "teacher", "admin"))
        login_btn = st.button("Login", key="login_btn")
        if login_btn:
            result = login(st.session_state.uid, password, role)
            if result == "success":
                st.session_state.role = role
                if (st.session_state.uid == password):
                    st.session_state.new_user = True
                st.session_state.login = True
                st.success("Login successful!")
                st.markdown("---")
                st.rerun()
            else:
                st.error(result)
    if st.session_state.login:
        if st.session_state.new_user:
            new_password = st.text_input("Enter the New Password", key="newpasswordstudent", type="password")
            retype_password = st.text_input("Retype Your Password", key="retypepasswordstudent", type="password")
            change_password_btn = st.button("Change Password", key="changepasswordstudent")
            if change_password_btn:
                if new_password.strip() != retype_password.strip():
                    st.warning("Passwords not Match")
                else:
                    change_password(st.session_state.uid, new_password, st.session_state.role)
                    st.success("Password Updated Successfully")
                    st.session_state.new_user = False
                    time.sleep(2)
                    st.rerun()
        else:
            if st.session_state.role == "admin":
                admin_page()
            if st.session_state.role == "student":
                student_details = list(fetch_studentinfo_by_id(st.session_state.uid))
                st.markdown(f"### Welcome, {student_details[1]}")
                student_page(student_details)
            if st.session_state.role == "teacher":
                teacher_details = list(fetch_staffinfo_by_id(st.session_state.uid))
                st.markdown(f"### Welcome, {teacher_details[2]}")
                teacher_page(teacher_details)
        logout = st.button("Logout", key="logout_btn")
        if logout:
            st.session_state.role = None
            st.session_state.login = False
            st.success("Logged out successfully!")
            st.markdown("---")
            time.sleep(2)
            st.rerun()
if  __name__ == '__main__':
    st.set_page_config(
        page_title="School Management System",
        page_icon=":school:",
        layout="centered",
        initial_sidebar_state="expanded"
    )
    initialize_variable()
    main_page()