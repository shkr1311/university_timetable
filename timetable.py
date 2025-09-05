import pandas as pd
import numpy as np
import random
from datetime import datetime
import json

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

# Define programme structures according to NEP 2020
PROGRAMMES = {
    'FYUP': {'years': 4, 'semesters': 8, 'code_prefix': 'UG'},
    'B.Ed': {'years': 2, 'semesters': 4, 'code_prefix': 'BED'},
    'M.Ed': {'years': 2, 'semesters': 4, 'code_prefix': 'MED'},
    'ITEP': {'years': 4, 'semesters': 8, 'code_prefix': 'ITEP'}
}

# Course categories as per NEP 2020
COURSE_CATEGORIES = {
    'Major': {'credits': [3, 4, 5], 'weight': 0.4},
    'Minor': {'credits': [2, 3, 4], 'weight': 0.25},
    'Skill-Based': {'credits': [2, 3], 'weight': 0.15},
    'AEC': {'credits': [2, 3], 'weight': 0.1},
    'VAC': {'credits': [1, 2], 'weight': 0.1}
}

# Major course subjects by discipline
MAJOR_SUBJECTS = {
    'Education': [
        'Foundations of Education', 'Educational Psychology', 'Curriculum and Pedagogy',
        'Assessment and Evaluation', 'Educational Technology', 'Inclusive Education',
        'Teacher Development', 'Educational Leadership', 'Research Methods in Education',
        'Philosophy of Education', 'Sociology of Education', 'Comparative Education',
        'Educational Planning and Management', 'Guidance and Counselling',
        'School Management and Administration', 'Educational Statistics',
        'Child Development and Learning', 'Environmental Education',
        'Peace Education', 'Gender and Education', 'Adult and Continuing Education',
        'Distance Education', 'Educational Measurement', 'Action Research',
        'Classroom Management', 'Learning Disabilities', 'Gifted Education'
    ],
    'Science': [
        'Physics', 'Chemistry', 'Biology', 'Mathematics', 'Computer Science',
        'Environmental Science', 'Biotechnology', 'Microbiology', 'Botany',
        'Zoology', 'Biochemistry', 'Genetics', 'Ecology', 'Astronomy',
        'Geology', 'Statistics', 'Applied Mathematics', 'Data Science',
        'Artificial Intelligence', 'Machine Learning', 'Quantum Physics',
        'Organic Chemistry', 'Inorganic Chemistry', 'Physical Chemistry',
        'Molecular Biology', 'Cell Biology', 'Bioinformatics'
    ],
    'Commerce': [
        'Accounting', 'Business Studies', 'Economics', 'Marketing',
        'Finance', 'Entrepreneurship', 'Business Law', 'International Business',
        'Corporate Finance', 'Investment Analysis', 'Banking', 'Insurance',
        'Taxation', 'Auditing', 'Cost Accounting', 'Management Accounting',
        'Financial Markets', 'Business Ethics', 'Operations Management',
        'Human Resource Management', 'Strategic Management', 'Supply Chain Management',
        'Digital Marketing', 'E-Commerce', 'Business Analytics', 'Retail Management'
    ],
    'Humanities': [
        'History', 'Political Science', 'Philosophy', 'Literature',
        'Linguistics', 'Anthropology', 'Sociology', 'Geography',
        'Art History', 'Music', 'Fine Arts', 'Theatre Studies',
        'Cultural Studies', 'Archaeological Studies', 'Medieval History',
        'Modern History', 'Ancient History', 'World History', 'Indian Philosophy',
        'Western Philosophy', 'Ethics', 'Logic', 'Aesthetics',
        'Comparative Literature', 'Creative Writing', 'Journalism', 'Mass Communication'
    ]
}

# Minor interdisciplinary subjects
MINOR_SUBJECTS = [
    'Psychology', 'Digital Humanities', 'Media Studies', 'Public Administration',
    'International Relations', 'Criminology', 'Social Work', 'Library Science',
    'Information Science', 'Cognitive Science', 'Neuroscience', 'Behavioral Economics',
    'Game Theory', 'Operations Research', 'Sustainable Development',
    'Climate Studies', 'Urban Planning', 'Rural Development', 'Gender Studies',
    'Disability Studies', 'Human Rights', 'Conflict Resolution', 'Peace Studies',
    'Development Studies', 'Area Studies', 'Translation Studies', 'Comparative Religion'
]

# Skill-based courses
SKILL_COURSES = [
    'ICT Tools in Education', 'Data Analytics', 'Creative Writing', 'Public Speaking',
    'Digital Marketing', 'Web Development', 'Mobile App Development', 'Graphic Design',
    'Video Production', 'Photography', 'Foreign Language (French)', 'Foreign Language (German)',
    'Foreign Language (Spanish)', 'Foreign Language (Japanese)', 'Sign Language',
    'Entrepreneurship Skills', 'Financial Literacy', 'Project Management',
    'Leadership Skills', 'Teamwork and Collaboration', 'Critical Thinking',
    'Problem Solving', 'Innovation and Creativity', 'Time Management',
    'Stress Management', 'Emotional Intelligence', 'Communication Skills',
    'Presentation Skills', 'Research Methods', 'Academic Writing',
    'Technical Writing', 'Content Creation', 'Social Media Management',
    'Event Management', 'Community Engagement', 'Volunteering and Service Learning'
]

# Ability Enhancement Courses (AECs)
AEC_COURSES = [
    'English Communication', 'Hindi Communication', 'Regional Language',
    'Environmental Studies', 'Digital Literacy', 'Information Literacy',
    'Health and Wellness', 'Life Skills', 'Mathematical Thinking',
    'Scientific Temper', 'Logical Reasoning', 'Analytical Skills',
    'Computer Fundamentals', 'Internet and Web Technologies', 'Cyber Security Basics',
    'Data Privacy and Ethics', 'Research Ethics', 'Academic Integrity'
]

# Value-Added Courses (VACs)
VAC_COURSES = [
    'Ethics and Moral Values', 'Yoga and Meditation', 'Indian Knowledge Systems',
    'Indian Philosophy and Traditions', 'Constitutional Values', 'Human Values',
    'Social Service and Outreach', 'Community Development', 'Cultural Heritage',
    'Traditional Arts and Crafts', 'Folk Music and Dance', 'Ayurveda and Wellness',
    'Sustainable Living', 'Organic Farming', 'Water Conservation',
    'Waste Management', 'Renewable Energy', 'Climate Action'
]

# Faculty names (diverse Indian names)
FACULTY_NAMES = [
    'Dr. Priya Sharma', 'Prof. Rajesh Kumar', 'Dr. Sunita Verma', 'Prof. Amit Singh',
    'Dr. Meera Gupta', 'Prof. Vikram Patel', 'Dr. Kavya Reddy', 'Prof. Arjun Nair',
    'Dr. Pooja Agarwal', 'Prof. Sanjay Joshi', 'Dr. Deepika Rao', 'Prof. Rohit Mehta',
    'Dr. Shruti Iyer', 'Prof. Kiran Desai', 'Dr. Neha Bansal', 'Prof. Varun Chopra',
    'Dr. Anita Kulkarni', 'Prof. Suresh Pandey', 'Dr. Ritu Malhotra', 'Prof. Gaurav Tiwari',
    'Dr. Shweta Saxena', 'Prof. Manish Agrawal', 'Dr. Preeti Jain', 'Prof. Ashok Yadav',
    'Dr. Seema Chandra', 'Prof. Nitin Bhatia', 'Dr. Rashmi Sinha', 'Prof. Pramod Mishra',
    'Dr. Anjali Thakur', 'Prof. Ravi Krishnan', 'Dr. Nidhi Goyal', 'Prof. Sunil Bhatt',
    'Dr. Divya Menon', 'Prof. Ajay Dubey', 'Dr. Swati Kapoor', 'Prof. Manoj Shukla',
    'Dr. Pallavi Dixit', 'Prof. Santosh Kumar', 'Dr. Rekha Devi', 'Prof. Vinod Sharma',
    'Dr. Shalini Gupta', 'Prof. Ramesh Singh', 'Dr. Madhuri Patil', 'Prof. Hemant Jha',
    'Dr. Aditi Saxena', 'Prof. Deepak Agarwal', 'Dr. Usha Rani', 'Prof. Vijay Prasad',
    'Dr. Sarita Bhardwaj', 'Prof. Naresh Chandra', 'Dr. Geeta Sharma', 'Prof. Anil Kumar',
    'Dr. Smita Joshi', 'Prof. Rakesh Gupta', 'Dr. Archana Singh', 'Prof. Mukesh Yadav',
    'Dr. Vidya Sagar', 'Prof. Prakash Verma', 'Dr. Lakshmi Narayan', 'Prof. Brijesh Tiwari',
    'Dr. Sudha Rani', 'Prof. Harish Chandra', 'Dr. Nirmala Devi', 'Prof. Subhash Goel'
]

# Room types and capacities
ROOMS = {
    'Classroom': {'prefix': 'CR', 'capacity_range': (30, 80), 'count': 50},
    'Laboratory': {'prefix': 'LAB', 'capacity_range': (20, 40), 'count': 25},
    'Seminar Hall': {'prefix': 'SH', 'capacity_range': (50, 150), 'count': 10},
    'Computer Lab': {'prefix': 'CL', 'capacity_range': (25, 45), 'count': 15},
    'Tutorial Room': {'prefix': 'TR', 'capacity_range': (15, 25), 'count': 20}
}

def generate_course_code(category, subject, programme, year, semester):
    """Generate course code based on NEP 2020 structure"""
    prog_code = PROGRAMMES[programme]['code_prefix']
    category_code = category[:2].upper()
    year_sem = f"{year}{semester}"
    subject_code = ''.join([word[0] for word in subject.split()[:3]]).upper()
    return f"{prog_code}{category_code}{year_sem}{subject_code}"

def generate_rooms():
    """Generate room database"""
    rooms = []
    room_id = 1
    
    for room_type, details in ROOMS.items():
        for i in range(details['count']):
            room_number = f"{details['prefix']}-{i+1:03d}"
            capacity = random.randint(*details['capacity_range'])
            rooms.append({
                'room_id': room_id,
                'room_number': room_number,
                'room_type': room_type,
                'capacity': capacity,
                'building': random.choice(['Main Building', 'Science Block', 'Commerce Block', 'Arts Block', 'Education Block']),
                'floor': random.randint(1, 4),
                'amenities': random.choice([
                    'Projector, Whiteboard',
                    'Smart Board, AC, Projector',
                    'Whiteboard, Audio System',
                    'Lab Equipment, Safety Features',
                    'Computer Systems, Internet'
                ])
            })
            room_id += 1
    
    return rooms

def generate_courses():
    """Generate comprehensive course database"""
    courses = []
    course_id = 1
    
    for programme, prog_details in PROGRAMMES.items():
        for year in range(1, prog_details['years'] + 1):
            for semester in [1, 2]:  # Two semesters per year
                actual_semester = (year - 1) * 2 + semester
                
                # Generate courses for each category
                for category, cat_details in COURSE_CATEGORIES.items():
                    num_courses = max(2, int(8 * cat_details['weight']))  # Minimum 2 courses per category
                    
                    for _ in range(num_courses):
                        if category == 'Major':
                            # Select major subject based on programme
                            if programme in ['B.Ed', 'M.Ed', 'ITEP']:
                                subject_pool = MAJOR_SUBJECTS['Education']
                            else:  # FYUP
                                discipline = random.choice(list(MAJOR_SUBJECTS.keys()))
                                subject_pool = MAJOR_SUBJECTS[discipline]
                        elif category == 'Minor':
                            subject_pool = MINOR_SUBJECTS
                        elif category == 'Skill-Based':
                            subject_pool = SKILL_COURSES
                        elif category == 'AEC':
                            subject_pool = AEC_COURSES
                        else:  # VAC
                            subject_pool = VAC_COURSES
                        
                        subject = random.choice(subject_pool)
                        course_code = generate_course_code(category, subject, programme, year, actual_semester)
                        credits = random.choice(cat_details['credits'])
                        
                        # Determine course type and hours
                        if 'Lab' in subject or 'ICT' in subject or 'Computer' in subject:
                            course_type = 'Lab'
                            theory_hours = credits - 1
                            lab_hours = 2
                            tutorial_hours = 0
                        elif category == 'Skill-Based':
                            course_type = 'Practical'
                            theory_hours = credits - 1
                            lab_hours = 0
                            tutorial_hours = 1
                        else:
                            course_type = 'Theory'
                            theory_hours = credits
                            lab_hours = 0
                            tutorial_hours = 1 if credits >= 3 else 0
                        
                        # Assign faculty
                        faculty = random.choice(FACULTY_NAMES)
                        
                        # Determine enrollment based on programme and year
                        base_enrollment = {
                            'FYUP': [120, 110, 100, 90],
                            'B.Ed': [80, 75],
                            'M.Ed': [30, 25],
                            'ITEP': [60, 55, 50, 45]
                        }
                        
                        enrollment = base_enrollment[programme][year-1] + random.randint(-15, 15)
                        if category == 'Minor':
                            enrollment = int(enrollment * 0.6)  # Minor courses have fewer students
                        elif category in ['Skill-Based', 'AEC', 'VAC']:
                            enrollment = int(enrollment * 0.4)  # Specialized courses have fewer students
                        
                        courses.append({
                            'course_id': course_id,
                            'course_code': course_code,
                            'course_name': subject,
                            'category': category,
                            'programme': programme,
                            'year': year,
                            'semester': actual_semester,
                            'credits': credits,
                            'course_type': course_type,
                            'theory_hours': theory_hours,
                            'lab_hours': lab_hours,
                            'tutorial_hours': tutorial_hours,
                            'total_weekly_hours': theory_hours + lab_hours + tutorial_hours,
                            'faculty_assigned': faculty,
                            'enrollment': enrollment,
                            'prerequisite': random.choice([None, None, None, f"Basic {subject.split()[0]}"]),  # 25% have prerequisites
                            'co_requisite': None,
                            'assessment_pattern': random.choice([
                                'Mid-term (30%) + End-term (50%) + Assignment (20%)',
                                'Continuous Assessment (40%) + End-term (60%)',
                                'Project (50%) + Presentation (30%) + Viva (20%)',
                                'Practical (60%) + Theory (40%)'
                            ])
                        })
                        
                        course_id += 1
    
    return courses

def assign_rooms_to_courses(courses, rooms):
    """Assign appropriate rooms to courses"""
    course_room_assignments = []
    assignment_id = 1
    
    for course in courses:
        # Determine suitable room type
        if course['course_type'] == 'Lab':
            suitable_rooms = [r for r in rooms if r['room_type'] in ['Laboratory', 'Computer Lab']]
        elif course['enrollment'] > 60:
            suitable_rooms = [r for r in rooms if r['room_type'] == 'Seminar Hall']
        elif course['course_type'] == 'Practical':
            suitable_rooms = [r for r in rooms if r['room_type'] in ['Laboratory', 'Classroom']]
        else:
            suitable_rooms = [r for r in rooms if r['room_type'] in ['Classroom', 'Tutorial Room']]
        
        # Filter by capacity
        suitable_rooms = [r for r in suitable_rooms if r['capacity'] >= course['enrollment']]
        
        if suitable_rooms:
            assigned_room = random.choice(suitable_rooms)
            course_room_assignments.append({
                'assignment_id': assignment_id,
                'course_id': course['course_id'],
                'room_id': assigned_room['room_id'],
                'capacity_utilization': round((course['enrollment'] / assigned_room['capacity']) * 100, 2)
            })
            assignment_id += 1
    
    return course_room_assignments

def generate_time_slots():
    """Generate time slots for the week"""
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    time_slots = [
        '09:00-10:00', '10:00-11:00', '11:30-12:30', '12:30-13:30',
        '14:30-15:30', '15:30-16:30', '16:30-17:30'
    ]
    
    slots = []
    slot_id = 1
    
    for day in days:
        for time_slot in time_slots:
            slots.append({
                'slot_id': slot_id,
                'day': day,
                'time_slot': time_slot,
                'slot_type': 'Regular',
                'duration_minutes': 60
            })
            slot_id += 1
    
    return slots

# Generate all datasets
print("Generating NEP 2020 University Timetable Dataset...")

courses = generate_courses()
rooms = generate_rooms()
course_room_assignments = assign_rooms_to_courses(courses, rooms)
time_slots = generate_time_slots()

# Create DataFrames
courses_df = pd.DataFrame(courses)
rooms_df = pd.DataFrame(rooms)
assignments_df = pd.DataFrame(course_room_assignments)
slots_df = pd.DataFrame(time_slots)

# Create faculty dataset
faculty_courses = courses_df.groupby('faculty_assigned').agg({
    'course_id': 'count',
    'total_weekly_hours': 'sum',
    'enrollment': 'sum'
}).rename(columns={
    'course_id': 'total_courses',
    'total_weekly_hours': 'total_teaching_hours',
    'enrollment': 'total_students'
}).reset_index()

faculty_courses['faculty_id'] = range(1, len(faculty_courses) + 1)
faculty_courses = faculty_courses[['faculty_id', 'faculty_assigned', 'total_courses', 'total_teaching_hours', 'total_students']]

# Display summary statistics
print(f"\n=== DATASET SUMMARY ===")
print(f"Total Courses Generated: {len(courses)}")
print(f"Total Faculty: {len(faculty_courses)}")
print(f"Total Rooms: {len(rooms)}")
print(f"Total Time Slots: {len(time_slots)}")

print(f"\n=== COURSES BY PROGRAMME ===")
print(courses_df['programme'].value_counts())

print(f"\n=== COURSES BY CATEGORY ===")
print(courses_df['category'].value_counts())

print(f"\n=== COURSES BY TYPE ===")
print(courses_df['course_type'].value_counts())

print(f"\n=== ROOM DISTRIBUTION ===")
print(rooms_df['room_type'].value_counts())

# Display sample data
print(f"\n=== SAMPLE COURSES ===")
print(courses_df[['course_code', 'course_name', 'category', 'programme', 'credits', 'faculty_assigned', 'enrollment']].head(10))

print(f"\n=== SAMPLE ROOMS ===")
print(rooms_df[['room_number', 'room_type', 'capacity', 'building']].head(10))

print(f"\n=== SAMPLE FACULTY WORKLOAD ===")
print(faculty_courses.head(10))

# Save to CSV files with download functionality
def save_to_csv(dataframe, filename):
    """Save DataFrame to CSV and provide download link"""
    csv_content = dataframe.to_csv(index=False)
    print(f"\n=== {filename.upper()} ===")
    print(f"Rows: {len(dataframe)}")
    print(f"Columns: {len(dataframe.columns)}")
    return csv_content

# Generate student enrollment data to reach 400+ rows
def generate_student_enrollments(courses):
    """Generate student enrollment details"""
    enrollments = []
    enrollment_id = 1
    
    # Generate student IDs
    student_ids = [f"STU{i:05d}" for i in range(1, 2001)]  # 2000 students
    student_names = [
        f"{random.choice(['Aarav', 'Vivaan', 'Aditya', 'Vihaan', 'Arjun', 'Reyansh', 'Ayaan', 'Krishna', 'Ishaan', 'Shaurya', 'Atharv', 'Advik', 'Aadhya', 'Ananya', 'Anika', 'Avni', 'Diya', 'Ira', 'Kavya', 'Kiara', 'Myra', 'Navya', 'Priya', 'Riya', 'Sara', 'Shreya']))} {random.choice(['Sharma', 'Verma', 'Singh', 'Kumar', 'Gupta', 'Agarwal', 'Patel', 'Jain', 'Mishra', 'Yadav', 'Tiwari', 'Chandra', 'Bansal', 'Saxena', 'Goyal', 'Mittal', 'Singhal', 'Joshi', 'Bhatt', 'Srivastava'])}"
        for _ in range(2000)
    ]
    
    for course in courses:
        # Randomly enroll students in each course
        enrolled_students = random.sample(list(zip(student_ids, student_names)), course['enrollment'])
        
        for student_id, student_name in enrolled_students:
            enrollments.append({
                'enrollment_id': enrollment_id,
                'course_id': course['course_id'],
                'student_id': student_id,
                'student_name': student_name,
                'programme': course['programme'],
                'year': course['year'],
                'semester': course['semester'],
                'enrollment_date': f"2024-0{random.randint(1,8)}-{random.randint(1,28):02d}",
                'status': random.choice(['Active', 'Active', 'Active', 'Active', 'Dropped']),  # 20% dropout rate
                'grade': random.choice(['A+', 'A', 'B+', 'B', 'C+', 'C', 'D', None]),  # Some courses ongoing
                'attendance_percentage': random.randint(65, 100)
            })
            enrollment_id += 1
    
    return enrollments

courses = generate_courses()
rooms = generate_rooms()
course_room_assignments = assign_rooms_to_courses(courses, rooms)
time_slots = generate_time_slots()
student_enrollments = generate_student_enrollments(courses)

# Create DataFrames
courses_df = pd.DataFrame(courses)
rooms_df = pd.DataFrame(rooms)
assignments_df = pd.DataFrame(course_room_assignments)
slots_df = pd.DataFrame(time_slots)
enrollments_df = pd.DataFrame(student_enrollments)

# Create faculty dataset
faculty_courses = courses_df.groupby('faculty_assigned').agg({
    'course_id': 'count',
    'total_weekly_hours': 'sum',
    'enrollment': 'sum'
}).rename(columns={
    'course_id': 'total_courses',
    'total_weekly_hours': 'total_teaching_hours',
    'enrollment': 'total_students'
}).reset_index()

faculty_courses['faculty_id'] = range(1, len(faculty_courses) + 1)
faculty_courses['department'] = [random.choice(['Education', 'Science', 'Commerce', 'Humanities', 'Skill Development']) for _ in range(len(faculty_courses))]
faculty_courses['experience_years'] = [random.randint(2, 35) for _ in range(len(faculty_courses))]
faculty_courses['qualification'] = [random.choice(['Ph.D.', 'M.Phil.', 'M.Ed.', 'M.Sc.', 'M.A.', 'M.Com.']) for _ in range(len(faculty_courses))]
faculty_courses['specialization'] = [random.choice(['Curriculum Studies', 'Educational Psychology', 'Assessment', 'Technology Integration', 'Special Education', 'Subject Teaching']) for _ in range(len(faculty_courses))]
faculty_courses = faculty_courses[['faculty_id', 'faculty_assigned', 'department', 'qualification', 'specialization', 'experience_years', 'total_courses', 'total_teaching_hours', 'total_students']]

# Generate timetable schedule data
def generate_timetable_schedule(courses, rooms, time_slots):
    """Generate actual timetable schedule"""
    schedule = []
    schedule_id = 1
    
    for course in courses[:500]:  # Limit to first 500 courses for timetable
        # Assign random time slots for each course
        weekly_hours = course['total_weekly_hours']
        assigned_room = random.choice([r for r in rooms if r['capacity'] >= course['enrollment']])
        
        for hour in range(weekly_hours):
            day = random.choice(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'])
            time_slot = random.choice(['09:00-10:00', '10:00-11:00', '11:30-12:30', '12:30-13:30', '14:30-15:30', '15:30-16:30'])
            
            schedule.append({
                'schedule_id': schedule_id,
                'course_id': course['course_id'],
                'room_id': assigned_room['room_id'],
                'day': day,
                'time_slot': time_slot,
                'week_number': random.randint(1, 16),  # 16 weeks per semester
                'session_type': random.choice(['Theory', 'Lab', 'Tutorial', 'Practical']),
                'faculty_id': random.randint(1, len(faculty_courses))
            })
            schedule_id += 1
    
    return schedule

timetable_schedule = generate_timetable_schedule(courses, rooms, time_slots)
schedule_df = pd.DataFrame(timetable_schedule)

print(f"\n=== DATASET GENERATION COMPLETE ===")
print(f"The dataset includes {len(courses)} courses following NEP 2020 guidelines")
print(f"with balanced distribution across all required categories and programmes.")