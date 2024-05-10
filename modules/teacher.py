import datetime
from models.bert_model import calculate_similarity_score
import pandas as pd
import streamlit as st
import ast
import time
from db.db import (
    get_period_by_subject_id_grade_day,
    check_notes_existence,
    insert_notes,
    fetch_all_details_from_malpractice_table,
    fetch_student_info_not_uploaded_the_notes,
    fetch_studentinfo_by_id,
    insert_into_understanding_info,
    get_notes_details,
    insert_model_trained_details,
    get_model_trained_details,
    get_all_understanding_info
)
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def display_teacher_profile(teacher_details):
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
                    <li><strong>Department:</strong> {}</li>
                </ul>
            </div>
        </div>
        <br>
    """.format(*teacher_details), unsafe_allow_html=True)



def teacher_page(teacher_details):

    sidebar_options = [
        "Home",
        "Upload the Notes",
        "MalPractice Details",
        "Train the Model",
        "Visualize the Content"
    ]
    selected_option = st.sidebar.radio("Select Operation", sidebar_options,
                                       index=0)

    if selected_option == "Home":
        formatted_teacher_details = []
        formatted_teacher_details.extend(
            [teacher_details[2], teacher_details[3], teacher_details[4], teacher_details[6]])
        display_teacher_profile(formatted_teacher_details)
    elif selected_option == "Upload the Notes":
        grade = st.selectbox("Select the Grade", options=ast.literal_eval(teacher_details[5]), index=0)
        if grade:
            period_nos = get_period_by_subject_id_grade_day(teacher_details[-1], grade)
            if len(period_nos) == 0:
                st.warning(f"There is no period for the class {grade} Today")
            else:
                period = st.selectbox("Select the Period", options=period_nos, index=0)
                if (not check_notes_existence(teacher_details[-1], grade, st.session_state.uid, period)):
                    teacher_notes = st.file_uploader("Upload the Notes", type="txt")
                    col1, col2 = st.columns(2)
                    title = None
                    chapter = None
                    with col1:
                        title = st.text_input("Enter the title", key="getnotestitle")
                    with col2:
                        chapter = st.number_input("Enter the Chapter Number", key="getnoteschapter", min_value=0,
                                                  step=1)
                    upload_notes_btn = st.button("Upload Notes", key="uploadnotesbtn")
                    if upload_notes_btn:
                        insert_notes(teacher_notes, teacher_details[-1], period, st.session_state.uid, grade, title,
                                     chapter)
                        st.success("Notes Uploaded Successfully")
                        time.sleep(2)
                        st.rerun()
                else:
                    st.warning("You Already Uploaded the Notes")
    elif selected_option == "MalPractice Details":
        grade = st.selectbox("Select the grade",options=ast.literal_eval(teacher_details[5]),index=0)
        df = pd.DataFrame(fetch_all_details_from_malpractice_table(),
                          columns=["Student ID", "Name", "Date", "Grade", "period_no", "Description"])
        if grade:
            df = df[df["Grade"]==str(grade)]
            if df is not None:
                day_of_week = st.selectbox("Select the date",options=df["Date"].unique(),index=0)
                if day_of_week is not None:
                    period_no = get_period_by_subject_id_grade_day(teacher_details[-1], grade,day_of_week)
                    filtered_period_no = st.selectbox("Select the Period",options=period_no)
                    if filtered_period_no:
                        df = df[df["period_no"] == filtered_period_no]
                        if df.shape[0] == 0:
                            st.info("No Details Found")
                        else:
                            st.dataframe(df[["Name","Description"]])
                else:
                    st.info("No Details found")
            else:
                st.info("No Details Found")
    elif selected_option == "Train the Model":
        grade = st.selectbox("Select the Grade", options=ast.literal_eval(teacher_details[5]), index=0)
        if grade:
            period_nos = get_period_by_subject_id_grade_day(teacher_details[-1], grade)
            if len(period_nos) == 0:
                st.warning(f"There is no period for the class {grade} Today")
            else:
                period = st.selectbox("Select the Period", options=period_nos, index=0)
                if not check_notes_existence(teacher_details[-1], grade, st.session_state.uid, period):
                    st.warning("Notes not Uploaded Yet!")
                else:
                    if not get_model_trained_details(grade,datetime.date.today(),period):
                        st.info("Ready to Train the Model")
                        df = pd.DataFrame(fetch_all_details_from_malpractice_table(),
                                          columns=["Student ID", "Name", "Date", "Grade", "period_no", "Description"])
                        today = datetime.date.today()
                        df["Date"] = pd.to_datetime(df["Date"])
                        df["Date"] = df["Date"].dt.date
                        filtered_df = df[(df["Grade"] == str(grade)) & (df["Date"] == today) & (df["period_no"] == period)]
                        if filtered_df.shape[0] != 0:
                            st.markdown("### MalPractice Details")
                            st.dataframe(filtered_df[["Name","Description"]])
                            st.warning("For Students who involved in Malpractice consider their understanding level as -1")
                        ids = fetch_student_info_not_uploaded_the_notes(today,period,grade)
                        if(ids[0]==-1):
                            st.warning("No notes have been uploaded by students yet.")
                        else:
                            pending_ids = []
                            for i in ids:
                                if i not in filtered_df["Student ID"].values:
                                    pending_ids.append(i)
                            if(len(pending_ids)!=0):
                                st.markdown("### Pending Student Details")
                                for i in range(len(pending_ids)):
                                    st.write(f"{i+1} {list(fetch_studentinfo_by_id(pending_ids[i]))[1]}")
                            else:
                                st.info("All the Students Uploaded their Notes")
                                train_the_model_btn = st.button("Train the Model")
                                title = list(get_notes_details( grade, None, period)[0])[-2]
                                if train_the_model_btn:
                                    for i in filtered_df[["Student ID"]].values:
                                        insert_into_understanding_info(grade,period,int(i[0]),today,teacher_details[-1],-1,title)
                                    teacher_notes = [list(i)[1]  for i in get_notes_details(grade,None,period) if list(i)[0]<60 ][0]
                                    if not isinstance(teacher_notes,str):
                                        teacher_notes = teacher_notes.decode('utf-8')
                                    notes_details = get_notes_details(grade,None,period)
                                    st.info("Model Under Training")
                                    for notes_detail in notes_details:
                                        notes_detail = list(notes_detail)
                                        print(notes_detail)
                                        if notes_detail[0]>=60:
                                            understanding_score = calculate_similarity_score(teacher_notes,notes_detail[1])
                                            insert_into_understanding_info(grade, period, int(notes_detail[0]), today, teacher_details[-1],
                                                                           int(understanding_score*100), title)
                                    st.success("Model Training Process Successful")
                                    insert_model_trained_details(grade,today,period)
                                    time.sleep(2)
                                    st.rerun()
                    else:
                        st.info("Model Already Trained")

    elif selected_option == "Visualize the Content":
        df = pd.DataFrame(get_all_understanding_info(),columns=["Grade","period_no","Student_id","Date","Subject Name","Understanding Score","Title"])
        grade = st.selectbox("Select the Grade",options=ast.literal_eval(teacher_details[-2]),index=0)
        if grade:
            visulaization_options =["Title Based Analysis","OverAll Class Analysis","Individual/Comparative Analysis"]
            df = df[df["Grade"]==grade]
            selected_visualaization_option = st.selectbox("Select the Option",options=visulaization_options)
            if selected_visualaization_option == "Title Based Analysis":
                title = st.selectbox("Select the Title",options=df["Title"].unique(),)
                df = df[df["Title"]==title]
                difficulty_levels = ["Malpractice", "Low Understanding", "Medium Understanding", "Well Understood"]
                count_0 = df[df["Understanding Score"] < 0]["Understanding Score"].shape[0]
                count_1 = df[(df["Understanding Score"] > 0) & (df["Understanding Score"] < 30)]["Understanding Score"].shape[0]
                count_2 = df[(df["Understanding Score"] >= 30) & (df["Understanding Score"] <= 60)]["Understanding Score"].shape[0]
                count_3 = df[df["Understanding Score"] >= 60]["Understanding Score"].shape[0]
                fig = make_subplots(rows=1, cols=1)
                bar_trace = go.Bar(x=difficulty_levels, y=[count_0,count_1,count_2,count_3], marker=dict(color='skyblue'))
                fig.add_trace(bar_trace)
                fig.update_layout(
                    xaxis=dict(title='Difficulty Level'),
                    yaxis=dict(title='Count'),
                    title=dict(text='Difficulty Level Distribution', x=0.5),
                    bargap=0.15
                )
                st.plotly_chart(fig, use_container_width=True)
            elif selected_visualaization_option == "OverAll Class Analysis":
                df = df[["Date","Understanding Score"]]
                df['Date'] = pd.to_datetime(df['Date'])
                df.set_index('Date', inplace=True)
                df_resampled = df.resample('D').mean()
                df_resampled['Understanding Score'] = df_resampled['Understanding Score'].interpolate()
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df_resampled.index,
                    y=df_resampled['Understanding Score'],
                    mode='lines+markers',
                    line=dict(shape='spline'),  # Use 'spline' to generate a smooth curve
                    marker=dict(color='blue', size=8),
                    name='Understanding Score'
                ))

                fig.update_layout(
                    title='Understanding Score Over Time',
                    xaxis=dict(title='Date'),
                    yaxis=dict(title='Understanding Score'),
                    hovermode='x',
                    template='plotly_white',
                    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
                    margin=dict(l=40, r=40, t=80, b=40),
                    showlegend=True
                )
                st.plotly_chart(fig)
            elif selected_visualaization_option == "Individual/Comparative Analysis":
                df = df[["Student_id", "Date", "Understanding Score"]]
                # Set 'Date' column as the index
                df['Date'] = pd.to_datetime(df['Date'])
                df.set_index('Date', inplace=True)

                # Resample the data to daily frequency and calculate mean understanding score for each date and student
                df = df.groupby(['Student_id', pd.Grouper(freq='D')]).mean().reset_index()
                fig = go.Figure()

                # Add traces for each student's mean understanding score over time
                for student_id in df["Student_id"].unique():
                    student_data = df[df["Student_id"] == student_id]
                    fig.add_trace(go.Scatter(
                        x=df["Date"],
                        y=student_data["Understanding Score"],
                        mode='lines+markers',
                        name=list(fetch_studentinfo_by_id(int(student_id)))[1],
                        line=dict(shape='spline'),
                        marker=dict(size=8),
                    ))

                fig.update_layout(
                    title='Mean Understanding Scores Over Time',
                    xaxis=dict(title='Date'),
                    yaxis=dict(title='Mean Understanding Score'),
                    hovermode='x',
                    template='plotly_white',
                    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
                    margin=dict(l=40, r=40, t=80, b=40),
                    showlegend=True
                )

                st.plotly_chart(fig)