import sqlite3
import json
import pandas as pd
import datetime


def login(id, password, role):
    conn = sqlite3.connect("Academy.db")
    cursor = conn.cursor()
    select_query = f"SELECT password FROM {role} WHERE id = ?"
    cursor.execute(select_query, (id,))
    result = cursor.fetchone()
    if result is not None and result[0] == password:
        return "success"
    if result is None:
        return "User Id not Found"
    conn.close()
    return "Wrong Password"


def change_password(id, password, role):
    conn = sqlite3.connect("Academy.db")
    cursor = conn.cursor()
    update_query = f"""UPDATE {role} 
                         SET password = ?
                         WHERE id = ?;"""
    cursor.execute(update_query, (password, id))
    conn.commit()
    conn.close()


def create_teacher_table():
    conn = sqlite3.connect("Academy.db")
    cursor = conn.cursor()
    create_table_query = """CREATE TABLE IF NOT EXISTS teacher (
                            id INTEGER PRIMARY KEY,
                            password TEXT NOT NULL,
                            name TEXT NOT NULL,
                            email TEXT NOT NULL UNIQUE,
                            phone TEXT,
                            handling_class TEXT,
                            department TEXT
                            );"""
    cursor.execute(create_table_query)
    conn.commit()
    conn.close()


def create_table_subjects():
    # Connect to the SQLite database
    conn = sqlite3.connect('Academy.db')
    cursor = conn.cursor()

    # SQL code to create the Subjects table if it does not exist
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS Subjects (
        subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_name VARCHAR(100) NOT NULL
    );
    """

    # SQL code to insert values into the Subjects table if they do not exist
    insert_values_sql = """
    INSERT INTO Subjects (subject_name) SELECT * FROM (SELECT 
    "Tamil" AS subject_name
    UNION SELECT "English"
    UNION SELECT "Maths"
    UNION SELECT "Physics"
    UNION SELECT "Chemistry"
    UNION SELECT "Computer"
    UNION SELECT "Social"
    UNION SELECT "Science"
    ) AS temp WHERE NOT EXISTS (SELECT * FROM Subjects);
    """

    # Execute the SQL statements
    cursor.execute(create_table_sql)
    cursor.execute(insert_values_sql)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def add_teacher_details(name, email, phone, handling_class, department):
    create_teacher_table()
    handling_class_str = json.dumps(handling_class)

    conn = sqlite3.connect("Academy.db")
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM teacher")
    value = cursor.fetchone()
    id = 0
    if value[0] is not None:
        id = value[0] + 1
    password = str(id)
    insert_query = """INSERT INTO teacher (id, password, name, email, phone, handling_class, department) 
                         VALUES (?, ?, ?, ?, ?, ?, ?);"""
    cursor.execute(insert_query, (id, password, name, email, phone, handling_class_str, department))
    conn.commit()
    conn.close()


def delete_teacher_details(id):
    conn = sqlite3.connect("Academy.db")
    cursor = conn.cursor()
    delete_query = "DELETE FROM teacher WHERE id = ?;"
    cursor.execute(delete_query, (id,))
    conn.commit()
    conn.close()


def fetch_id_from_staff_table():
    conn = sqlite3.connect("Academy.db")
    cursor = conn.cursor()
    select_query = f"SELECT id From teacher;"
    cursor.execute(select_query)
    result = cursor.fetchall()
    conn.close()
    return result


def fetch_staffinfo_by_id(id):
    conn = sqlite3.connect("Academy.db")
    cursor = conn.cursor()
    select_query = f"SELECT * FROM teacher WHERE id = ?;"
    cursor.execute(select_query, (id,))
    name = cursor.fetchone()
    conn.close()
    return name


def edit_teacher_details(id, name, email, phone, handling_class, department):
    conn = sqlite3.connect("Academy.db")
    cursor = conn.cursor()
    handling_class = json.dumps(handling_class)
    update_query = """UPDATE teacher 
                      SET name = ?, email = ?, phone = ?, handling_class = ?, department = ?
                      WHERE id = ?;"""
    cursor.execute(update_query, (name, email, phone, handling_class, department, id))
    conn.commit()
    conn.close()


def create_student_table():
    conn = sqlite3.connect("Academy.db")
    cursor = conn.cursor()
    create_table_query = """CREATE TABLE IF NOT EXISTS student (
                            id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            email TEXT NOT NULL UNIQUE,
                            phone TEXT,
                            class TEXT,
                            dob DATE,
                            address TEXT,
                            tenth_mark INTEGER,
                            eleventh_mark INTEGER,
                            password TEXT DEFAULT NULL
                            );"""
    cursor.execute(create_table_query)
    conn.commit()
    conn.close()


def add_student_details(name, email, phone, _class, dob, address, tenth_mark=None, eleventh_mark=None):
    create_student_table()
    conn = sqlite3.connect("Academy.db")
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM student")
    value = cursor.fetchone()
    id = int(str(dob)[1:4])*10 + 0
    if value[0] is not None:
        id = value[0] + 1
    password = str(id)
    insert_query = """INSERT INTO student (id, name, email, phone, class, dob, address, tenth_mark, eleventh_mark, password) 
                      VALUES (?, ?, ?, ?,  ?, ?, ?, ?, ?, ?);"""
    cursor.execute(insert_query,
                   (id, name, email, phone, _class, dob, address, tenth_mark, eleventh_mark, password))

    conn.commit()
    conn.close()

def fetch_id_from_student_table(class_name=None):
    try:
        conn = sqlite3.connect("Academy.db")
        cursor = conn.cursor()
        if class_name:
            select_query = "SELECT id FROM student WHERE class = ?;"
            cursor.execute(select_query, (class_name,))
        else:
            select_query = "SELECT id FROM student;"
            cursor.execute(select_query)
        result = cursor.fetchall()
        return result
    except sqlite3.Error as e:
        print("Error fetching IDs from student table:", e)
        return None
    finally:
        conn.close()



def fetch_studentinfo_by_id(id):
    conn = sqlite3.connect("Academy.db")
    cursor = conn.cursor()
    select_query = f"SELECT * FROM student WHERE id = ?;"
    cursor.execute(select_query, (id,))
    name = cursor.fetchone()
    conn.close()
    return name


def delete_student_details(id):
    conn = sqlite3.connect("Academy.db")
    cursor = conn.cursor()
    delete_query = "DELETE FROM student WHERE id = ?;"
    cursor.execute(delete_query, (id,))
    conn.commit()
    conn.close()


def edit_student_details(id, name, email, phone, _class, dob, address, tenth_mark, eleventh_mark):
    conn = sqlite3.connect("Academy.db")
    cursor = conn.cursor()
    update_query = """UPDATE student 
                      SET name = COALESCE(?, name),
                          email = COALESCE(?, email),
                          phone = COALESCE(?, phone),
                          class = COALESCE(?, class),
                          dob = COALESCE(?, dob),
                          address = COALESCE(?, address),
                          tenth_mark = COALESCE(?, tenth_mark),
                          eleventh_mark = COALESCE(?, eleventh_mark)
                      WHERE id = ?;"""
    cursor.execute(update_query, (name, email, phone, _class, dob, address, tenth_mark, eleventh_mark, id))
    conn.commit()
    conn.close()


def get_all_subject_ids_with_names():
    create_table_subjects()
    # Connect to the SQLite database
    conn = sqlite3.connect('Academy.db')
    cursor = conn.cursor()

    try:
        select_all_subjects_sql = """
        SELECT subject_id, subject_name FROM Subjects
        """
        cursor.execute(select_all_subjects_sql)
        results = cursor.fetchall()
        subject_dict = {}
        for subject_id, subject_name in results:
            subject_dict[subject_id] = subject_name
        return subject_dict
    finally:
        conn.close()


def get_all_subject_names_with_ids():
    create_table_subjects()
    # Connect to the SQLite database
    conn = sqlite3.connect('Academy.db')
    cursor = conn.cursor()

    try:
        select_all_subjects_sql = """
        SELECT subject_id, subject_name FROM Subjects
        """
        cursor.execute(select_all_subjects_sql)
        results = cursor.fetchall()
        subject_dict = {}
        for subject_id, subject_name in results:
            subject_dict[subject_name] = subject_id
        return subject_dict
    finally:
        conn.close()


def create_Timetable_table():
    try:
        conn = sqlite3.connect('Academy.db')
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Timetable (
                grade VARCHAR(10),
                period INTEGER,
                day_of_week VARCHAR(10) NOT NULL,
                subject_id INT,
                PRIMARY KEY (grade, period, day_of_week),
                FOREIGN KEY (subject_id) REFERENCES Subjects(subject_id)
            );
        """)
        conn.commit()
        print("Timetable table created successfully.")
    except sqlite3.Error as e:
        print("Error creating Timetable table:", e)


def add_timetable_details(grade, df, delete=False):
    create_Timetable_table()
    conn = sqlite3.connect('Academy.db')
    cursor = conn.cursor()
    if (delete):
        cursor.execute("DELETE FROM Timetable WHERE grade=?", (grade,))
        conn.commit()
    for day, row in df.iterrows():
        for period, subject_id in row.items():
            if pd.notnull(subject_id):
                cursor.execute('''
                    INSERT INTO Timetable (grade, period, day_of_week, subject_id)
                    VALUES (?, ?, ?, ?)
                ''', (grade, period, day, subject_id))
    conn.commit()


def get_timetable_details(grade):
    try:
        conn = sqlite3.connect('Academy.db')
        cursor = conn.cursor()
        # Execute SQL query to select timetable details for the specified grade
        cursor.execute("SELECT * FROM Timetable WHERE grade= ?", (str(grade),))
        rows = cursor.fetchall()

        df = pd.DataFrame(rows, columns=['grade', 'period', 'day_of_week', 'subject_id'])
        df.set_index('day_of_week', inplace=True)
        # Pivot the DataFrame based on 'day_of_week'
        pivoted_df = df.pivot_table(index='day_of_week', columns='period', values='subject_id', aggfunc='first')
        return pivoted_df

    except sqlite3.Error as e:
        print("Error retrieving timetable details:", e)
        return None


def get_timetable_details_for_display(grade):
    try:
        conn = sqlite3.connect('Academy.db')
        cursor = conn.cursor()
        # Execute SQL query to select timetable details for the specified grade
        cursor.execute("SELECT * FROM Timetable WHERE grade= ?", (str(grade),))
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=['grade', 'period', 'day_of_week', 'subject_id'])
        subject_ids_with_names = get_all_subject_ids_with_names()
        df['subject_id'].replace(subject_ids_with_names, inplace=True)
        # Pivot the DataFrame based on 'day_of_week'
        pivoted_df = df.pivot_table(index='day_of_week', columns='period', values='subject_id', aggfunc='first')
        return pivoted_df

    except sqlite3.Error as e:
        print("Error retrieving timetable details:", e)
        return None


def get_period_by_subject_id_grade_day(subject_name, grade,day_of_week=None):
    try:
        subject_id = get_all_subject_names_with_ids()[subject_name]
        if day_of_week is None:
            day_of_week = datetime.datetime.now().weekday()
        else:
            day_of_week = datetime.datetime.strptime(day_of_week, '%Y-%m-%d').weekday()
        conn = sqlite3.connect('Academy.db')
        cursor = conn.cursor()
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Saturday']
        cursor.execute("""
            SELECT period FROM Timetable
            WHERE subject_id = ? AND grade = ? AND day_of_week = ?
        """, (subject_id, grade, days_of_week[day_of_week]))
        periods = cursor.fetchall()
        return [period[0] for period in periods] if periods else []
    except sqlite3.Error as e:
        print("Error retrieving period number for the specified day:", e)
        return []


def create_notes_table():
    try:
        conn = sqlite3.connect('Academy.db')
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Notes (
                id INTEGER ,
                notes TEXT NOT NULL,
                grade TEXT NOT NULL,
                subject_id INT,
                date DATE NOT NULL,
                day VARCHAR(10) NOT NULL,
                period_no INTEGER,
                title TEXT NOT NULL,
                chapter INTEGER NOT NULL,
                UNIQUE (id, period_no, day, date, subject_id,grade),
                FOREIGN KEY (subject_id) REFERENCES Subjects(subject_id)
            );
        """)
        conn.commit()
    except sqlite3.Error as e:
        print("Error creating Notes table:", e)
def check_notes_existence(subject_name, grade, id, period_no):
    try:
        create_notes_table()
        subject_id = get_all_subject_names_with_ids()[subject_name]
        date = datetime.date.today()
        day = datetime.datetime.now().weekday()
        conn = sqlite3.connect('Academy.db')
        cursor = conn.cursor()
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Saturday']
        cursor.execute("""
            SELECT COUNT(*) FROM Notes 
            WHERE subject_id = ? AND grade = ? AND id = ? AND period_no = ? AND date = ? AND day = ?
        """, (subject_id, grade, id, period_no, date, days_of_week[day]))
        count = cursor.fetchone()[0]
        return count > 0
    except sqlite3.Error as e:
        print("Error checking notes existence:", e)
        return False
def insert_notes(notes, subject_name,period_no, id, grade,title,chapter,is_student=False):
    try:
        subject_id = get_all_subject_names_with_ids()[subject_name]
        date = datetime.date.today()
        day = datetime.datetime.now().weekday()
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Saturday']
        conn = sqlite3.connect('Academy.db')
        cursor = conn.cursor()
        if(is_student):
            cursor.execute("""
                INSERT INTO Notes (notes, subject_id, date, day, period_no, id, grade, title, chapter)
                VALUES (?, ?, ?, ?, ?, ?, ?,?,?)
            """, (notes, subject_id, date, days_of_week[day], period_no, id, grade,title,chapter))
            conn.commit()
        else:
            cursor.execute("""
                          INSERT INTO Notes (notes, subject_id, date, day, period_no, id, grade, title, chapter)
                          VALUES (?, ?, ?, ?, ?, ?, ?,?,?)
                      """, (notes.read(), subject_id, date, days_of_week[day], period_no, id, grade, title, chapter))
            conn.commit()
        print("Notes inserted successfully.")
    except sqlite3.Error as e:
        print("Error inserting notes:", e)
def get_notes_details(grade, subject_id, period_no):
    try:
        # Get today's date and format it
        today_date = datetime.datetime.now().date().strftime("%Y-%m-%d")
        conn = sqlite3.connect('Academy.db')
        cursor = conn.cursor()
        if subject_id is not None:
            cursor.execute("""
                SELECT * FROM Notes
                WHERE grade = ? AND subject_id = ? AND period_no = ? AND date = ?
            """, (grade, int(subject_id), period_no, str(today_date)))
        else:
            cursor.execute("""
                          SELECT * FROM Notes
                          WHERE grade = ? AND period_no = ? AND date = ?
                      """, (grade,  period_no, str(today_date)))
        notes_details = cursor.fetchall()
        return notes_details
    except sqlite3.Error as e:
        print("Error fetching notes details:", e)
        return None
def fetch_notes_data():
    try:
        conn = sqlite3.connect('Academy.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM Notes
        """)
        notes_data = cursor.fetchall()
        return notes_data
    except sqlite3.Error as e:
        print("Error fetching notes data:", e)
        return None


def create_malpractice_table():
    try:
        conn = sqlite3.connect('Academy.db')
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Malpractice (
                student_id INTEGER,
                student_name TEXT,
                date DATE,
                grade VARCHAR(10),
                period_no INTEGER,
                description TEXT,
                PRIMARY KEY (student_id, date, period_no)
            );
        """)
        conn.commit()
        print("Malpractice table created successfully.")
    except sqlite3.Error as e:
        print("Error creating Malpractice table:", e)

def insert_data_into_malpractice_table(student_id, student_name, grade, period_no, description):
    try:
        create_malpractice_table()
        conn = sqlite3.connect('Academy.db')
        cursor = conn.cursor()
        today_date = datetime.date.today()
        cursor.execute("""
            INSERT INTO Malpractice (student_id, student_name, date, grade, period_no, description)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (student_id, student_name, today_date, grade, period_no, description))
        conn.commit()
        print("Data inserted into Malpractice table successfully.")
    except sqlite3.Error as e:
        print("Error inserting data into Malpractice table:", e)

def fetch_details_from_malpractice_table(student_id, period_no, date):
    try:
        create_malpractice_table()
        conn = sqlite3.connect('Academy.db')
        cursor = conn.cursor()
        date_obj = date
        cursor.execute("""
            SELECT * FROM Malpractice
            WHERE student_id = ? AND period_no = ? AND date = ?
        """, (int(student_id), int(period_no), date_obj))
        rows = cursor.fetchall()
        if rows:
            print("Details retrieved successfully.")
            return rows
        else:
            print("No details found for the specified parameters.")
            return None
    except sqlite3.Error as e:
        print("Error retrieving details from Malpractice table:", e)
        return None
def fetch_all_details_from_malpractice_table():
    try:
        create_malpractice_table()
        conn = sqlite3.connect('Academy.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM Malpractice
        """)
        rows = cursor.fetchall()
        if rows:
            print("Details retrieved successfully.")
            return rows
        else:
            print("No details found for the specified parameters.")
            return None
    except sqlite3.Error as e:
        print("Error retrieving details from Malpractice table:", e)
        return None
def fetch_student_info_not_uploaded_the_notes(date,period_no,grade):
    student_ids = [list(i)[0] for i in fetch_id_from_student_table(grade)]
    student_uploaded_notes = [i if list(i) is None else list(i)[0] for i in get_notes_details(str(grade),None,period_no)]
    if None not in student_uploaded_notes and len(student_uploaded_notes)>1:
        pending_list = []
        for i in student_ids:
            if i not in student_uploaded_notes:
                pending_list.append(i)
        return pending_list
    else:
        return [-1]

def create_model_trained_details_table():
    try:
        conn = sqlite3.connect('Academy.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS model_trained_details (
                grade INTEGER,
                date DATE,
                period_no INTEGER,
                PRIMARY KEY (grade, date, period_no)
            )
        ''')
        conn.commit()
        print("model_trained_details table created successfully.")
    except sqlite3.Error as e:
        print("Error creating model_trained_details table:", e)
def create_understanding_info_table():
    try:
        conn = sqlite3.connect('Academy.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS UnderstandingInfo (
                grade INTEGER,
                period_no INTEGER,
                id INTEGER,
                date DATE,
                subject_name TEXT,
                understanding_score REAL,
                title TEXT,
                PRIMARY KEY (grade, period_no, id, date, subject_name)
            )
        ''')
        conn.commit()
        print("UnderstandingInfo table created successfully.")
    except sqlite3.Error as e:
        print("Error creating UnderstandingInfo table:", e)
def insert_into_understanding_info(grade, period_no, id, date, subject_name, understanding_score, title):
    try:
        create_understanding_info_table()
        conn = sqlite3.connect('Academy.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO UnderstandingInfo (grade, period_no, id, date, subject_name, understanding_score, title)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (grade, period_no, id, date, subject_name, understanding_score, title))
        conn.commit()
        print("Values inserted into UnderstandingInfo successfully.")
    except sqlite3.Error as e:
        print("Error inserting values into UnderstandingInfo:", e)

def insert_model_trained_details(grade, date, period_no):
    try:
        create_model_trained_details_table()
        conn = sqlite3.connect('Academy.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO model_trained_details (grade, date, period_no)
            VALUES (?, ?, ?)
        ''', (grade, date, period_no))
        conn.commit()
        print("Values inserted into model_trained_details table successfully.")
    except sqlite3.Error as e:
        print("Error inserting values into model_trained_details table:", e)
def get_model_trained_details(grade, date, period_no):
    try:
        conn = sqlite3.connect('Academy.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM model_trained_details
            WHERE grade = ? AND date = ? AND period_no = ?
        ''', (grade, date, period_no))
        row = cursor.fetchone()
        conn.close()
        return row is not None
    except sqlite3.Error as e:
        print("Error retrieving model_trained_details:", e)
        return False
def get_all_understanding_info():
    try:
        conn = sqlite3.connect('Academy.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM UnderstandingInfo
        ''')
        rows = cursor.fetchall()
        conn.close()
        return rows
    except sqlite3.Error as e:
        print("Error retrieving all UnderstandingInfo:", e)
        return None
if __name__ == "__main__":
    create_malpractice_table()
    create_notes_table()
    create_table_subjects()
    create_Timetable_table()
    create_understanding_info_table()
    create_model_trained_details_table()
    create_student_table()
    create_teacher_table()