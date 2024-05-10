import time
from models.originality_checker import originality_checker
import streamlit as st
import datetime
from models.grammar_correction import Grammer_Correction
from models.plagarism_check import plagarism_check

def get_the_originality_score(file):
    score = originality_checker(file).compute_model()
    if score >= 0.5:
        return True
    else:
        return True
from db.db import (
    check_notes_existence,
    get_timetable_details,
    get_notes_details,
    get_all_subject_ids_with_names,
    insert_notes,
    fetch_details_from_malpractice_table,
    insert_data_into_malpractice_table,
    fetch_studentinfo_by_id
)
# Function to display the profile view
def display_student_profile(teacher_details):
    st.markdown("""
        <style>
            .profile-container {
                display: flex;
                align-items: center;
                padding: 20px;
                border-radius: 10px;
                background-color: #333;
                color: white;
                animation: slideInLeft 1s ease-in-out;
            }
            @keyframes slideInLeft {
                from { transform: translateX(-100%); }
                to { transform: translateX(0%); }
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="profile-container">
            <div>
                <h2>{}</h2>
                <ul style="list-style-type: none; padding: 0;">
                    <li><strong>Email:</strong> {}</li>
                    <li><strong>Phone No:</strong> {}</li>
                    <li><strong>Grade:</strong> {}</li>
                </ul>
            </div>
        </div>
        <br>
    """.format(*teacher_details), unsafe_allow_html=True)



def student_page(student_details):
    if 'selected_option' not in st.session_state:
        st.session_state.selected_option = "Home"
    sidebar_options = [
        "Home",
        "Upload the Notes"
    ]
    selected_option = st.sidebar.radio("Select Operation", sidebar_options,
                                       index=sidebar_options.index(st.session_state.selected_option))

    # Update selected option in session state
    st.session_state.selected_option = selected_option

    if selected_option == "Home":
        formatted_student_details = []
        formatted_student_details.extend(
            [student_details[1], student_details[2], student_details[3], student_details[4]])
        display_student_profile(formatted_student_details)
    elif selected_option ==  "Upload the Notes":
        day = datetime.datetime.now().weekday()
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Saturday']
        period_no = st.selectbox("Select the period",options=range(1,8),index=0)
        df = get_timetable_details(student_details[4])
        subject_name =  get_all_subject_ids_with_names()[df.loc[days_of_week[day],period_no]]
        if not check_notes_existence(subject_name,student_details[4],st.session_state.uid,period_no):
            malpractice_details = fetch_details_from_malpractice_table(student_details[0],period_no,datetime.date.today())
            already_exist_notes = get_notes_details(student_details[4], df.loc[days_of_week[day], period_no], period_no)
            if len(already_exist_notes) != 0:
                if malpractice_details is None:
                    notes = st.file_uploader(f"Upload the Notes for {subject_name}",type="txt")
                    upload_notes_btn = st.button("Upload Your Notes")
                    if upload_notes_btn:
                        st.info("Please Wait! We are Verifying Your Notes")
                        text = notes.read()
                        if get_the_originality_score(text):
                            already_exist_notes = already_exist_notes
                            print(already_exist_notes)
                            for i in range(len(already_exist_notes)):
                                if already_exist_notes[i][0] >= 60 :
                                    other_student_details = fetch_studentinfo_by_id(list(already_exist_notes[i])[0])
                                    score = plagarism_check().calculate_common_score(text.decode('utf-8'), list(already_exist_notes[i])[1])
                                    print(score)
                                    #print(other_student_details,list(already_exist_notes[0])[0])
                                    if score >= 40.0:
                                        insert_data_into_malpractice_table(student_details[0], student_details[1],
                                                                           student_details[4], period_no,
                                                                           f"{student_details[1]} copied notes from {other_student_details[1]}")
                                        st.warning("We have found your work at our space")
                                        time.sleep(2)
                                        st.rerun()
                            else:
                                already_exist_notes = list(already_exist_notes[0])
                                st.success("Congratulations! Your Work is Genuine")
                                st.info("We are further proceeding your work to Grammar correction tool")
                                notes = Grammer_Correction(text).make_grammer_error_free()
                                st.info("Thanks for Your Patience.")
                                insert_notes(notes,subject_name,period_no,st.session_state.uid,student_details[4],already_exist_notes[-2],already_exist_notes[-1],True)
                                st.success("Notes Uploaded Successfully")
                                time.sleep(2)
                                st.rerun()
                        else:
                            insert_data_into_malpractice_table(student_details[0],student_details[1],student_details[4],period_no,"Notes is created with help of AI")
                            st.warning("You have Created Your Work with help of AI")
                            time.sleep(2)
                            st.rerun()
                else:
                    st.info("Notes Already Uploaded")
                    st.warning(list(malpractice_details[0])[-1])
            else:
                st.warning("Please wait for Teacher to Upload the notes")
        else:
            st.warning("Already Notes Uploaded")