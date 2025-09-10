import streamlit as st
import pandas as pd
import numpy as np
import random

# ----- DATA STORAGE -----
# For simplicity, use session state to store data temporarily

if 'teachers' not in st.session_state:
    st.session_state.teachers = pd.DataFrame(columns=['TeacherID', 'Name', 'Expertise', 'MaxLoad', 'Availability'])

if 'courses' not in st.session_state:
    st.session_state.courses = pd.DataFrame(columns=['CourseID', 'Name', 'Credits', 'TheoryHours', 'PracticalHours'])

if 'rooms' not in st.session_state:
    st.session_state.rooms = pd.DataFrame(columns=['RoomID', 'Capacity', 'Type'])

if 'students' not in st.session_state:
    st.session_state.students = pd.DataFrame(columns=['StudentID', 'Name', 'Program', 'EnrolledCourses'])

if 'time_slots' not in st.session_state:
    st.session_state.time_slots = ['Mon-9AM','Mon-11AM','Mon-2PM','Tue-9AM','Tue-11AM', 'Tue-2PM',
                                  'Wed-9AM','Wed-11AM','Wed-2PM','Thu-9AM','Thu-11AM','Thu-2PM',
                                  'Fri-9AM','Fri-11AM','Fri-2PM']

# ----- ADMIN PANEL FOR DATA INPUT -----
def admin_panel():
    st.sidebar.title("Admin Panel")

    menu = st.sidebar.radio("Choose Operation:", ['Import Data', 'Add Teacher', 'Add Course', 'Add Room', 'Add Student', 'Generate Timetable'])

    if menu == 'Import Data':
        st.subheader("Import Teachers, Courses, Rooms, Students")
        uploaded_files = st.file_uploader("Upload CSV or Excel files (Teachers, Courses, Rooms, Students)", accept_multiple_files=True)
        for file in uploaded_files:
            try:
                if file.name.endswith('.csv'):
                    df = pd.read_csv(file)
                else:
                    df = pd.read_excel(file)
                if 'TeacherID' in df.columns:
                    st.session_state.teachers = df
                    st.success(f'Teachers loaded: {len(df)}')
                elif 'CourseID' in df.columns:
                    st.session_state.courses = df
                    st.success(f'Courses loaded: {len(df)}')
                elif 'RoomID' in df.columns:
                    st.session_state.rooms = df
                    st.success(f'Rooms loaded: {len(df)}')
                elif 'StudentID' in df.columns:
                    st.session_state.students = df
                    st.success(f'Students loaded: {len(df)}')
                else:
                    st.warning(f'Unknown file type: {file.name}')
            except Exception as e:
                st.error(f'Failed to load {file.name}: {e}')

    elif menu == 'Add Teacher':
        st.subheader("Add Teacher")
        tid = st.text_input("Teacher ID")
        name = st.text_input("Name")
        expertise = st.text_input("Expertise (e.g. B.Ed, M.Ed courses)")
        max_load = st.number_input("Maximum Load (hours)", min_value=1, max_value=40, value=20)
        availability = st.text_input("Available Time Slots (comma-separated from predefined slots)")
        if st.button("Add Teacher"):
            new_teacher = {'TeacherID': tid, 'Name': name, 'Expertise': expertise,
                           'MaxLoad': max_load, 'Availability': [a.strip() for a in availability.split(',')]}
            st.session_state.teachers = st.session_state.teachers.append(new_teacher, ignore_index=True)
            st.success(f"Teacher {name} added.")

    elif menu == 'Add Course':
        st.subheader("Add Course")
        cid = st.text_input("Course ID")
        cname = st.text_input("Course Name")
        credits = st.number_input("Credits", min_value=1, max_value=6, value=3)
        theory = st.number_input("Theory Hours", min_value=0, max_value=credits*2, value=2)
        practical = st.number_input("Practical Hours", min_value=0, max_value=credits*2, value=1)
        if st.button("Add Course"):
            new_course = {'CourseID': cid, 'Name': cname, 'Credits': credits,
                          'TheoryHours': theory, 'PracticalHours': practical}
            st.session_state.courses = st.session_state.courses.append(new_course, ignore_index=True)
            st.success(f"Course {cname} added.")

    elif menu == 'Add Room':
        st.subheader("Add Room")
        rid = st.text_input("Room ID")
        capacity = st.number_input("Room Capacity", min_value=5, max_value=200, value=40)
        typ = st.selectbox("Room Type", ['Classroom', 'Lab'])
        if st.button("Add Room"):
            new_room = {'RoomID': rid, 'Capacity': capacity, 'Type': typ}
            st.session_state.rooms = st.session_state.rooms.append(new_room, ignore_index=True)
            st.success(f"Room {rid} added.")

    elif menu == 'Add Student':
        st.subheader("Add Student")
        sid = st.text_input("Student ID")
        sname = st.text_input("Student Name")
        program = st.selectbox("Program", ['B.Ed', 'M.Ed', 'FYUP', 'ITEP'])
        enrolled_courses = st.text_area("Enrolled Course IDs (comma-separated)")
        if st.button("Add Student"):
            new_student = {'StudentID': sid, 'Name': sname, 'Program': program,
                           'EnrolledCourses': [c.strip() for c in enrolled_courses.split(',')]}
            st.session_state.students = st.session_state.students.append(new_student, ignore_index=True)
            st.success(f"Student {sname} added.")

# ----- GENETIC ALGORITHM ENGINE (Very simplified skeleton) -----
def fitness_function(timetable):
    # Placeholder: Calculate fitness considering hard and soft constraints
    # e.g. count conflicts, room capacity violations, faculty overload, gaps
    fitness = 100  # Higher better
    # Penalize conflicts and violations (decrease fitness)
    return fitness

def initial_population(pop_size, courses, timeslots, rooms, teachers):
    population = []
    for _ in range(pop_size):
        timetable = []
        # Random assignment for each course - simplistic
        for idx, course in courses.iterrows():
            slot = random.choice(timeslots)
            room = random.choice(rooms['RoomID'].tolist())
            teacher = random.choice(teachers['TeacherID'].tolist())
            timetable.append({'CourseID': course['CourseID'], 'Time': slot, 'Room': room, 'Teacher': teacher})
        population.append(timetable)
    return population

def crossover(parent1, parent2):
    # One-point crossover example
    pivot = len(parent1) // 2
    child = parent1[:pivot] + parent2[pivot:]
    return child

def mutate(timetable, timeslots, rooms, teachers, mutation_rate=0.1):
    for gene in timetable:
        if random.random() < mutation_rate:
            gene['Time'] = random.choice(timeslots)
        if random.random() < mutation_rate:
            gene['Room'] = random.choice(rooms['RoomID'].tolist())
        if random.random() < mutation_rate:
            gene['Teacher'] = random.choice(teachers['TeacherID'].tolist())
    return timetable

def genetic_algorithm(population, generations, courses, timeslots, rooms, teachers):
    for gen in range(generations):
        population = sorted(population, key=lambda x: fitness_function(x), reverse=True)
        next_gen = population[:len(population)//2]  # Keep best half
        while len(next_gen) < len(population):
            parent1, parent2 = random.sample(next_gen, 2)
            child = crossover(parent1, parent2)
            child = mutate(child, timeslots, rooms, teachers)
            next_gen.append(child)
        population = next_gen
        best_fit = fitness_function(population[0])
        st.write(f"Generation {gen+1}: Best Fitness = {best_fit}")
    return population[0]

# ----- MAIN APP -----
def main():
    st.title("AI/ML Timetable Generator - NEP 2020")

    admin_panel()

    if st.sidebar.button("Generate Timetable"):
        if st.session_state.courses.empty or st.session_state.teachers.empty or st.session_state.rooms.empty:
            st.error("Please ensure you have added courses, teachers, and rooms.")
            return
        population = initial_population(20, st.session_state.courses, st.session_state.time_slots,
                                        st.session_state.rooms, st.session_state.teachers)
        best_timetable = genetic_algorithm(population, 30, st.session_state.courses,
                                           st.session_state.time_slots, st.session_state.rooms,
                                           st.session_state.teachers)

        st.subheader("Generated Timetable")
        df = pd.DataFrame(best_timetable)
        st.dataframe(df)

if __name__ == "__main__":
    main()
