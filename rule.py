import streamlit as st
import pandas as pd
import random

# ---------- Helper functions ----------
def empty_timetable():
    hours = ["07:30 - 08:30", "08:30 - 09:30", "09:30 - 10:30",
             "10:30 - 11:30", "11:30 - 12:30", "12:30 - 13:30",
             "13:30 - 14:30", "14:30 - 15:30", "15:30 - 16:30"]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    data = [["" for _ in days] for _ in hours]
    return pd.DataFrame(data, index=hours, columns=days)

COLORS = ['#fed330', '#26de81', '#fd9644', '#a55eea', '#eb3b5a']
def color_picker(course):
    if not course: return "background-color: #fff; color: #212121;"
    idx = abs(hash(course)) % len(COLORS)
    return f"background-color: {COLORS[idx]}; color: #212121;"

def show_timetable(timetable, course_color_mode=True):
    if course_color_mode:
        styled = timetable.style.applymap(lambda v: color_picker(v))
    else:
        styled = timetable.style.applymap(lambda v: "background-color: #fff; color: #212121;" if v else "background-color: #fff;")
    st.dataframe(styled, height=500, width=900)

# ---------- Session State ----------
if 'teachers' not in st.session_state:
    st.session_state.teachers = []
if 'courses' not in st.session_state:
    st.session_state.courses = []
if 'students' not in st.session_state:
    st.session_state.students = []
if 'rooms' not in st.session_state:
    # Added rooms state with some default rooms
    st.session_state.rooms = [
        {"id":"R101", "type":"Classroom", "capacity":40},
        {"id":"R102", "type":"Lab", "capacity":30},
        {"id":"R103", "type":"Classroom", "capacity":50},
    ]
if 'slots' not in st.session_state:
    st.session_state.slots = [
        "07:30 - 08:30", "08:30 - 09:30", "09:30 - 10:30", "10:30 - 11:30",
        "11:30 - 12:30", "12:30 - 13:30", "13:30 - 14:30", "14:30 - 15:30", "15:30 - 16:30"
    ]
if 'timetable' not in st.session_state:
    st.session_state.timetable = empty_timetable()
if 'assignments' not in st.session_state:
    st.session_state.assignments = []

# ---------- Main UI ----------
st.title("NEP 2020 Timetable Generator with Room Allotment")

tabs = st.tabs(["Admin Panel", "User Panel"])
with tabs[0]:
    st.header("Admin Panel")

    # ---- Teachers ----
    st.subheader("Add Teacher")
    teacher_id = st.text_input("Teacher ID")
    teacher_name = st.text_input("Teacher Name")
    if st.button("Add Teacher"):
        if teacher_id and teacher_name:
            if not any(t['id']==teacher_id for t in st.session_state.teachers):
                st.session_state.teachers.append({"id": teacher_id, "name": teacher_name})
                st.success("Teacher added!")
            else:
                st.warning("Teacher ID already exists.")
        else:
            st.warning("Please enter both ID and Name.")
    st.write("**Teachers List:**")
    st.write(pd.DataFrame(st.session_state.teachers))

    # ---- Courses ----
    st.subheader("Add Course (with NEP credits)")
    course_id = st.text_input("Course ID")
    course_name = st.text_input("Course Name")
    course_credits = st.number_input("Credits (per NEP)", min_value=1, step=1)
    course_teacher = st.selectbox("Assign Teacher", options=[t["name"] for t in st.session_state.teachers] or [""])
    if st.button("Add Course"):
        if course_id and course_name and course_teacher:
            teacher_obj = next((t for t in st.session_state.teachers if t["name"] == course_teacher), None)
            if not any(c['id'] == course_id for c in st.session_state.courses):
                st.session_state.courses.append({
                    "id": course_id,
                    "name": course_name,
                    "credits": course_credits,
                    "teacher_id": teacher_obj["id"] if teacher_obj else ""
                })
                st.success("Course added!")
            else:
                st.warning("Course ID already exists.")
        else:
            st.warning("Please enter all details.")
    st.write("**Courses List:**")
    st.write(pd.DataFrame(st.session_state.courses))

    # ---- Rooms ----
    st.subheader("Manage Rooms")
    room_id = st.text_input("Room ID")
    room_type = st.selectbox("Room Type", options=["Classroom", "Lab"])
    room_capacity = st.number_input("Capacity", min_value=1)
    if st.button("Add Room"):
        if room_id and room_type and room_capacity:
            if not any(r['id'] == room_id for r in st.session_state.rooms):
                st.session_state.rooms.append({"id": room_id, "type": room_type, "capacity": room_capacity})
                st.success("Room added!")
            else:
                st.warning("Room ID already exists.")
        else:
            st.warning("Please enter all details.")
    st.write("**Rooms List:**")
    st.write(pd.DataFrame(st.session_state.rooms))

    # ---- Time slots ----
    st.subheader("Manage Time Slots")
    new_slot = st.text_input("Add New Time Slot (e.g., 16:30 - 17:30)")
    if st.button("Add Slot"):
        if new_slot:
            if new_slot not in st.session_state.slots:
                st.session_state.slots.append(new_slot)
                st.success("Slot added!")
            else:
                st.warning("This slot already exists.")
    st.write("Time Slots:")
    st.write(st.session_state.slots)

    # ---- Generate Timetable (Rule-based) ----
    st.subheader("Automate Timetable Assignment with Rooms")
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    course_color_mode = st.toggle("Color each course for visibility", value=True)
    timetable = empty_timetable()
    assignments = []

    generate = st.button("Create Timetable Automatically (Rule Based)")

    if generate:
        course_idx = 0
        teacher_busy = {d: {slot: [] for slot in st.session_state.slots} for d in days}
        room_busy = {d: {slot: [] for slot in st.session_state.slots} for d in days}

        for col, day in enumerate(days):
            for row, slot in enumerate(st.session_state.slots):
                if course_idx < len(st.session_state.courses):
                    course = st.session_state.courses[course_idx]
                    # Try to find a room available for this slot
                    assigned_room = None
                    for room in st.session_state.rooms:
                        if room['id'] not in room_busy[day][slot]:
                            assigned_room = room['id']
                            break
                    if assigned_room and course['teacher_id'] not in teacher_busy[day][slot]:
                        cell_val = f"{course['name']} ({course['id']}) | {course['teacher_id']} | {assigned_room}"
                        timetable.iat[row, col] = cell_val
                        assignments.append({"course_id": course['id'], "teacher_id": course['teacher_id'],
                                            "room_id": assigned_room, "day": day, "slot": slot})
                        teacher_busy[day][slot].append(course['teacher_id'])
                        room_busy[day][slot].append(assigned_room)
                        course_idx += 1
                else:
                    break
        st.session_state.timetable = timetable
        st.session_state.assignments = assignments
        st.success("Timetable generated with room allotment.")
        # ---- Store to CSV for admin download ----
        timetable_long = []
        for d in list(timetable.columns):
            for t in list(timetable.index):
                val = timetable.loc[t, d]
                if val:
                    timetable_long.append({'Day': d, 'Time': t, 'Assignment': val})
        timetable_long_df = pd.DataFrame(timetable_long)
        st.write("**Download as CSV:**")
        st.download_button("Download Timetable CSV", timetable_long_df.to_csv(index=False).encode('utf-8'), "timetable.csv")
    elif st.session_state.timetable is not None:
        timetable = st.session_state.timetable

    st.subheader("View Full Timetable")
    show_timetable(timetable, course_color_mode)

with tabs[1]:
    st.header("User Panel")

    options = ["Student", "Teacher"]
    role = st.radio("I am a", options)

    # ---- Student Section ----
    if role == "Student":
        st.subheader("Student View")
        sid = st.text_input("Enter your Student ID")
        sname = st.text_input("Enter your Name")
        scourses = st.multiselect("Choose Your Courses", [c["name"] for c in st.session_state.courses])
        smax_credits = st.number_input("Max Credits (NEP)", min_value=1, step=1, value=8)
        if st.button("Register Student"):
            selected_courselist = [c for c in st.session_state.courses if c["name"] in scourses]
            total_credits = int(sum(float(c["credits"]) for c in selected_courselist))
            if selected_courselist and total_credits <= smax_credits:
                st.session_state.students.append({
                    "id": sid,
                    "name": sname,
                    "courses": [c["id"] for c in selected_courselist],
                    "max_credits": smax_credits
                })
                st.success(f"Student {sname} registered with total credits {total_credits:.0f}.")
            elif total_credits > smax_credits:
                st.warning(f"Selected courses exceed allowed credit limit ({total_credits} > {smax_credits})")

        st.write("**Your Personalized Timetable**")
        student = next((s for s in st.session_state.students if s["id"] == sid), None)
        if student:
            st.write(f"Credits allowed: {student['max_credits']}")
            student_courses = set(student['courses'])
            timetable = st.session_state.timetable.copy()
            for row in timetable.index:
                for col in timetable.columns:
                    val = timetable.at[row, col]
                    if val:
                        cid = val.split("(")[-1].split(")")[0].replace(" ", "")
                        if cid not in student_courses:
                            timetable.at[row, col] = ""
            show_timetable(timetable, course_color_mode)

    # ---- Teacher Section ----
    if role == "Teacher":
        st.subheader("Teacher View")
        tid = st.text_input("Enter your Teacher ID")
        timetable = st.session_state.timetable.copy()
        for row in timetable.index:
            for col in timetable.columns:
                val = timetable.at[row, col]
                if val:
                    if f"| {tid} " not in val:
                        timetable.at[row, col] = ""
        st.write(f"Classes for Teacher ID: {tid}")
        show_timetable(timetable, course_color_mode)
