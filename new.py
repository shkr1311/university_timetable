# Required installations (run in your environment)
# pip install streamlit pandas numpy

import streamlit as st
import pandas as pd
import numpy as np
import random

# Genetic Algorithm essentials

def fitness(timetable, students, faculty, rooms):
    # Calculate how many constraints are met; higher is better
    penalty = 0
    # Example constraints checked:
    # - No student has clashes in timetable
    # - Faculty not double booked
    # - Room capacity sufficient
    # Implement logic as per your problem requirements
    #
    # Placeholder example (improve with real constraint checks)
    return -penalty

def create_individual(courses, time_slots, rooms, faculty_list):
    # Randomly assign each course to a time slot, room, and faculty qualified
    individual = []
    for course in courses.itertuples():
        time_slot = random.choice(time_slots['Time_Slot_ID'].tolist())
        room = random.choice(rooms['Room_ID'].tolist())
        # Pick a faculty who can teach this course
        qualified = faculty_list[faculty_list['Expertise_Courses'].apply(lambda x: course.Course_ID in eval(x))]
        if qualified.empty:
            fac_id = None
        else:
            fac_id = qualified.sample(1)['Faculty_ID'].values[0]
        individual.append((course.Course_ID, time_slot, room, fac_id))
    return individual

def crossover(parent1, parent2):
    # Single point crossover
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def mutation(individual, time_slots, rooms, faculty_list, mutation_rate=0.1):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            course_id, _, _, _ = individual[i]
            time_slot = random.choice(time_slots['Time_Slot_ID'].tolist())
            room = random.choice(rooms['Room_ID'].tolist())
            qualified = faculty_list[faculty_list['Expertise_Courses'].apply(lambda x: course_id in eval(x))]
            if qualified.empty:
                fac_id = None
            else:
                fac_id = qualified.sample(1)['Faculty_ID'].values[0]
            individual[i] = (course_id, time_slot, room, fac_id)
    return individual

def genetic_algorithm(courses, time_slots, rooms, faculty_list, population_size=50, generations=100):
    population = [create_individual(courses, time_slots, rooms, faculty_list) for _ in range(population_size)]
    for gen in range(generations):
        population = sorted(population, key=lambda ind: fitness(ind, None, None, None), reverse=True)
        next_gen = population[:10]  # elitism: keep top 10
        while len(next_gen) < population_size:
            p1, p2 = random.sample(population[:20], 2)
            c1, c2 = crossover(p1, p2)
            c1 = mutation(c1, time_slots, rooms, faculty_list)
            c2 = mutation(c2, time_slots, rooms, faculty_list)
            next_gen.extend([c1, c2])
        population = next_gen
        # (Optional) show progress on Streamlit
        st.write(f"Generation {gen+1}, Best Fitness: {fitness(population[0], None, None, None)}")
    return population[0]

# Streamlit UI

def main():
    st.title("NEP 2020 AI Timetable Generator")

    st.sidebar.header("Upload Data Files")
    courses_file = st.sidebar.file_uploader("Courses CSV")
    time_slots_file = st.sidebar.file_uploader("Time Slots CSV")
    faculty_file = st.sidebar.file_uploader("Faculty CSV")
    rooms_file = st.sidebar.file_uploader("Rooms CSV")

    if courses_file and time_slots_file and faculty_file and rooms_file:
        courses = pd.read_csv(courses_file)
        time_slots = pd.read_csv(time_slots_file)
        faculty = pd.read_csv(faculty_file)
        rooms = pd.read_csv(rooms_file)

        st.write("Courses Loaded:", len(courses))
        st.write("Time Slots Loaded:", len(time_slots))
        st.write("Faculty Loaded:", len(faculty))
        st.write("Rooms Loaded:", len(rooms))

        if st.button("Generate Timetable"):
            best_timetable = genetic_algorithm(courses, time_slots, rooms, faculty)
            timetable_df = pd.DataFrame(best_timetable, columns=["Course_ID", "Time_Slot", "Room", "Faculty_ID"])
            st.write("Generated Timetable")
            st.dataframe(timetable_df)

            # Offer download option
            csv = timetable_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Timetable CSV", csv, "timetable.csv")

if __name__ == "__main__":
    main()
