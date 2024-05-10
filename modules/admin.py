import streamlit as st
import datetime
import ast
import time
import pandas as pd
from db.db import (
    add_teacher_details,
    fetch_id_from_staff_table,
    fetch_staffinfo_by_id,
    delete_teacher_details,
    edit_teacher_details,
    add_student_details,
    fetch_id_from_student_table,
    fetch_studentinfo_by_id,
    delete_student_details,
    edit_student_details,
    get_all_subject_ids_with_names,
    add_timetable_details,
    get_timetable_details,
    get_timetable_details_for_display
)

days =["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
def find_index(lst,value):
    for i in range(len(lst)):
        if lst[i] == value:
            return i
# Sidebar options for Admin Panel
sidebar_options = [
    "Add Teacher Details",
    "Delete Teacher Details",
    "Edit Teacher Details",
    "View Teacher Details",
    "Add Student Details",
    "Delete Student Details",
    "Edit Student Details",
    "View Student Details",
    "Add the Timetable",
    "Edit the Timetable",
    "View the Timetable"
]

subjects = ("Tamil", "English", "Maths", "Physics", "Chemistry", "Computer", "Social", "Science")

def admin_page():
    st.sidebar.title("Admin Options")
    selected_option = st.sidebar.radio("Select Operation", sidebar_options)
    st.markdown("---")

    if selected_option == "Add Teacher Details":
        st.markdown("### Add Teacher Details")
        col1, col2, col3 = st.columns(3)
        department = None
        with col1:
            name = st.text_input("Enter the Name", key="staffname",value="")
            phone = st.text_input("Enter the Phone Number (+91)", value="+91", key="staffno")
        with col2:
            email = st.text_input("Enter the Email", key="staffmail",value="")
            handling_class = st.multiselect("Select the Class", options=range(1, 13), default=1, key="staffclass")
        with col3:
            if 11 in handling_class or 12 in handling_class:
                department = st.selectbox("Select the Department", options=(
                    "Tamil", "English", "Maths", "Physics", "Chemistry", "Computer"),
                                          key="staffdept12",index=0)
            else:
                department = st.selectbox("Select the Department",
                                          options=("Tamil", "English", "Maths", "Social", "Science"), key="staffdept10",index=0)
        add_teacher_btn = st.button("Add Teacher Details")
        if add_teacher_btn:
            add_teacher_details(name, email, phone, handling_class, department)
            st.success("Teacher details added successfully!")
            st.markdown("---")
            time.sleep(2)
            st.rerun()

    elif selected_option == "Delete Teacher Details":
        st.markdown("### Delete Teacher Details")
        ids_db = fetch_id_from_staff_table()
        if ids_db is not None:
            ids_reformatted = [i[0] for i in ids_db]
            id = st.selectbox("Select the ID", options=ids_reformatted)
            name = fetch_staffinfo_by_id(id)
            st.warning(f"Are you sure you want to delete the details of {name[2]}?")
            delete_btn = st.button("Delete Teacher Details")
            if delete_btn:
                delete_teacher_details(id)
                st.success("Teacher details deleted successfully!")
                st.markdown("---")
                time.sleep(2)
                st.rerun()
        else:
            st.error("No staff details found.")

    elif selected_option == "Edit Teacher Details":
        st.markdown("### Edit Teacher Details")
        ids_db = fetch_id_from_staff_table()
        if ids_db is not None:
            ids_reformatted = [i[0] for i in ids_db]
            id = st.selectbox("Select the ID", options=ids_reformatted)
            result = fetch_staffinfo_by_id(id)
            st.info(f"Editing details for {result[2]}")
            col1, col2, col3 = st.columns(3)
            with col1:
                phone = st.text_input("Enter the Phone Number (+91)", value=result[4], key="estaffno")
            with col2:
                name = st.text_input("Enter the Name", key="estaffname", value=result[2])
                handling_class = st.multiselect("Select the Class", options=range(1, 13),
                                                default=[int(i) for i in ast.literal_eval(result[5])],
                                                key="estaffclass")
            with col3:
                email = st.text_input("Enter the Email", key="estaffmail", value=result[3])
                department = st.selectbox("Select the Department", options=(
                    "Tamil", "English", "Maths", "Physics", "Chemistry", "Biology", "Computer", "Accountancy",
                    "Commerce",
                    "Social", "Science"), key="estaffdept12",
                                          index=["Tamil", "English", "Maths", "Physics", "Chemistry", "Biology",
                                                 "Computer", "Accountancy", "Commerce", "Social", "Science"].index(
                                              result[6]))
            edit_staff_btn = st.button("Edit Staff Details")
            if edit_staff_btn:
                edit_teacher_details(id, name, email, phone, handling_class, department)
                st.success("Teacher details updated successfully!")
                st.markdown("---")
                time.sleep(2)
                st.rerun()
        else:
            st.error("No staff details found.")

    elif selected_option == "View Teacher Details":
        st.markdown("### View Teacher Details")
        ids_db = fetch_id_from_staff_table()
        if ids_db is not None:
            staff_data = [["ID", "Name", "Email", "Phone", "Class", "Department"]]
            for i in ids_db:
                result = list(fetch_staffinfo_by_id(i[0]))
                result.pop(1)
                staff_data.append(result)
            df = pd.DataFrame(staff_data[1:], columns=staff_data[0])
            category = st.selectbox("Select the Category", ["Name", "Department"], key="viewstdetails")
            if category == "Name":
                name = st.multiselect("Select the Name", options=df["Name"].unique())
                st.dataframe(df[df["Name"].isin(name)])
            elif category == "Department":
                department = st.multiselect("Select the Department", options=df["Department"].unique())
                st.dataframe(df[df["Department"].isin(department)])
            st.markdown("---")
        else:
            st.error("No staff details found.")

    elif selected_option == "Add Student Details":
        st.markdown("### Add Student Details")
        col4, col5, col6 = st.columns(3)
        tenth_mark = -1
        eleventh_mark = -1
        with col4:
            name = st.text_input("Enter the Name", key="stname")
            class_ = st.selectbox("Select the Class", options=range(1, 13), key="stclass", index=0)
            if class_ > 10:
                tenth_mark = st.number_input("Enter the Tenth Mark", min_value=0, max_value=500, key="sttenth")
        with col5:
            email = st.text_input("Enter the Email", key="stemail")
            dob = st.date_input("Select the Date of Birth", value=datetime.date.today(),
                                min_value=datetime.date(2000, 1, 1))
            if class_ > 11:
                eleventh_mark = st.number_input("Enter the Eleventh Mark", min_value=0, max_value=600, key="steleventh")
        with col6:
            phone = st.text_input("Enter the Phone Number", key="stphone", value="+91")
            address = st.text_area("Enter the Address", key="staddress")
        add_student_details_btn = st.button("Add Student Details", key="addstbtn")
        if add_student_details_btn:
            add_student_details(name, email, phone, class_, dob, address, tenth_mark, eleventh_mark)
            st.success("Student details added successfully!")
            st.markdown("---")
            time.sleep(2)
            st.rerun()

    elif selected_option == "Delete Student Details":
        st.markdown("### Delete Student Details")
        ids_db = fetch_id_from_student_table()
        if ids_db is not None:
            ids_reformatted = [i[0] for i in ids_db]
            id = st.selectbox("Select the ID", options=ids_reformatted)
            name = fetch_studentinfo_by_id(id)
            st.warning(f"Are you sure you want to delete the details of {name[1]}?")
            delete_btn = st.button("Delete Student Details")
            if delete_btn:
                delete_student_details(id)
                st.success("Student details deleted successfully!")
                st.markdown("---")
                time.sleep(2)
                st.rerun()
        else:
            st.error("No student details found.")

    elif selected_option == "Edit Student Details":
        st.markdown("### Edit Student Details")
        ids_db = fetch_id_from_student_table()
        if ids_db is not None:
            ids_reformatted = [i[0] for i in ids_db]
            id = st.selectbox("Select the ID", options=ids_reformatted)
            result = fetch_studentinfo_by_id(id)
            st.info(f"Editing details for {result[1]}")
            tenth_mark = -1
            eleventh_mark = -1
            col4, col5, col6 = st.columns(3)
            with col4:
                name = st.text_input("Enter the Name", key="estname", value=result[1])
                class_ = st.selectbox("Select the Class", options=range(1, 13), key="estclass",
                                      index=find_index(range(1, 13), int(result[4])))
                if class_ > 10:
                    tenth_mark = st.number_input("Enter the Tenth Mark", min_value=0, max_value=500, key="esttenth",
                                                 value=result[7])
            with col5:
                email = st.text_input("Enter the Email", key="estemail", value=result[2])
                dob = st.date_input("Select the Date of Birth", value=datetime.datetime.strptime(result[5], "%Y-%m-%d"),
                                    min_value=datetime.date(2000, 1, 1))
                if class_ > 11:
                    eleventh_mark = st.number_input("Enter the Eleventh Mark", min_value=0, max_value=600,
                                                    key="esteleventh", value=result[8])
            with col6:
                phone = st.text_input("Enter the Phone Number", key="estphone", value=result[3])
                address = st.text_area("Enter the Address", key="estaddress", value=result[6])
            edit_student_btn = st.button("Edit Student Details")
            if edit_student_btn:
                edit_student_details(id, name, email, phone, class_, dob, address, tenth_mark, eleventh_mark)
                st.success("Student details updated successfully!")
                st.markdown("---")
                time.sleep(2)
                st.rerun()
        else:
            st.error("No student details found.")

    elif selected_option == "View Student Details":
        st.markdown("### View Student Details")
        ids_db = fetch_id_from_student_table()
        if ids_db is not None:
            ids_reformatted = [i[0] for i in ids_db]
            student_data = [
                ["ID", "Name", "Email", "Phone", "Class", "Date of Birth", "Address", "Tenth Mark", "Eleventh Mark"]]
            for i in ids_db:
                result = list(fetch_studentinfo_by_id(int(i[0])))
                result.pop(-1)
                student_data.append(result)
            df = pd.DataFrame(student_data[1:], columns=student_data[0])
            category = st.selectbox("Select the Category", ["Class", "Name"], key="viewstdetails")
            if category == "Class":
                class_ = st.multiselect("Select the Class", options=df["Class"].unique())
                st.dataframe(df[df["Class"].isin(class_)])
            elif category == "Name":
                name = st.multiselect("Select the Name", options=df["Name"].unique())
                st.dataframe(df[df["Name"].isin(name)])
            st.markdown("---")
        else:
            st.error("No student details found.")
    elif selected_option == "Add the Timetable":
        st.markdown("### Add Timetable Details")
        subject_ids_with_names = get_all_subject_ids_with_names()
        if subject_ids_with_names:
            st.header("Subject IDs and Names")
            for subject_id, subject_name in subject_ids_with_names.items():
                st.write(f"{subject_id} : {subject_name}")
        else:
            st.error("No subjects found in the database")
        st.write("Enter the subject id")
        grade = st.selectbox("Select the grade", options=range(1, 13), index=0)
        time_table = pd.DataFrame(columns=range(1, 8), index=days)
        time_table = st.data_editor(time_table)
        add_time_table_btn = st.button("Add Time Table ", key="addtimetablebtn")
        if add_time_table_btn:
            add_timetable_details(grade, time_table)
            st.success("Time table details added successfully!")
            st.markdown("---")
            time.sleep(2)
            st.rerun()
    elif selected_option == "Edit the Timetable":
        st.markdown("### Edit Timetable Details")
        subject_ids_with_names = get_all_subject_ids_with_names()
        if subject_ids_with_names:
            st.header("Subject IDs and Names")
            for subject_id, subject_name in subject_ids_with_names.items():
                st.write(f"{subject_id} : {subject_name}")
        else:
            st.error("No subjects found in the database")
        st.write("Enter the subject id")
        grade = st.selectbox("Select the grade", options=range(1, 13), index=0)
        time_table = get_timetable_details(grade)
        time_table = st.data_editor(time_table)
        edit_time_table_btn = st.button("Edit Time table", key="edittimetable")
        if edit_time_table_btn:
            add_timetable_details(grade, time_table, True)
            st.success("Time table details added successfully!")
            st.markdown("---")
            time.sleep(2)
            st.rerun()
    elif selected_option == "View the Timetable":
        st.markdown("### View Timetable Details")
        st.write("Enter the subject id")
        grade = st.selectbox("Select the grade", options=range(1, 13), index=0)
        time_table = get_timetable_details_for_display(grade)
        view_time_table_btn = st.button("View Time table", key="viewtimetable")
        if view_time_table_btn:
            st.dataframe(time_table)
