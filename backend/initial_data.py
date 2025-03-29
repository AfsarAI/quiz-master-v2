from flask import current_app as app
from models import db, User, Role, UserRoles, Qualification, Subject, UserSubjects, Chapter, Quiz, Question, RecentActivity
from flask_security import SQLAlchemyUserDatastore, hash_password
from datetime import datetime
import uuid
import random


def create_initial_data():
    with app.app_context():
        # Initialize the database
        db.create_all()

        # Check if database is empty
        if not User.query.first() and not Role.query.first() and not Qualification.query.first():
            print("Database is empty. Creating initial data...")
            create_roles()
            create_qualifications()
            create_subjects_and_chapters()
            create_quizzes_and_questions()
            create_admin_user()
            create_recent_activity()
            print("Initial data creation completed successfully!")
        else:
            print("Database already initialized. Skipping data creation.")
            
def create_roles():
    """Create Admin and User roles"""
    try:
        # Check if roles already exist
        admin_role = Role.query.filter_by(name='admin').first()
        user_role = Role.query.filter_by(name='user').first()
        
        if not admin_role:
            admin_role = Role(name='admin', description='Administrator with full access')
            db.session.add(admin_role)
            print("Admin role created")
        
        if not user_role:
            user_role = Role(name='user', description='Regular user with limited access')
            db.session.add(user_role)
            print("User role created")
            
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error creating roles: {e}")

def create_qualifications():
    """Create qualifications from class 6th to 12th and higher education"""
    qualifications_data = [
        {"name": "Class 6", "description": "6th Standard Education"},
        {"name": "Class 7", "description": "7th Standard Education"},
        {"name": "Class 8", "description": "8th Standard Education"},
        {"name": "Class 9", "description": "9th Standard Education"},
        {"name": "Class 10", "description": "10th Standard Education"},
        {"name": "Class 11", "description": "11th Standard Education"},
        {"name": "Class 12", "description": "12th Standard Education"},
        {"name": "B.Tech", "description": "Bachelor of Technology"},
        {"name": "M.Tech", "description": "Master of Technology"},
        {"name": "BSc", "description": "Bachelor of Science"},
        {"name": "BA", "description": "Bachelor of Arts"},
        {"name": "BS Online", "description": "IIT Madras Online Degree Program"}
    ]
    
    try:
        for qual_data in qualifications_data:
            existing_qual = Qualification.query.filter_by(name=qual_data["name"]).first()
            if not existing_qual:
                qualification = Qualification(
                    name=qual_data["name"],
                    description=qual_data["description"]
                )
                db.session.add(qualification)
                print(f"Added qualification: {qual_data['name']}")
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error creating qualifications: {e}")

def create_subjects_and_chapters():
    """Create subjects for each qualification and chapters for each subject"""
    # Dictionary mapping qualification types to appropriate subjects
    subjects_by_qualification = {
        "Class 6": ["Mathematics", "Science", "Social Studies", "English", "Hindi"],
        "Class 7": ["Mathematics", "Science", "Social Studies", "English", "Hindi"],
        "Class 8": ["Mathematics", "Science", "Social Studies", "English", "Hindi"],
        "Class 9": ["Mathematics", "Science", "Social Studies", "English", "Hindi"],
        "Class 10": ["Mathematics", "Science", "Social Studies", "English", "Hindi"],
        "Class 11": ["Physics", "Chemistry", "Mathematics", "Biology", "Computer Science"],
        "Class 12": ["Physics", "Chemistry", "Mathematics", "Biology", "Computer Science"],
        "B.Tech": ["Engineering Mathematics", "Data Structures", "Computer Networks", "Database Systems", "Operating Systems"],
        "M.Tech": ["Advanced Algorithms", "Machine Learning", "Artificial Intelligence", "Cloud Computing", "Data Mining"],
        "BSc": ["Physics", "Chemistry", "Mathematics", "Statistics", "Computer Science"],
        "BA": ["History", "Political Science", "Economics", "Sociology", "Psychology"],
        "BS Online": ["Programming", "Data Science", "Web Development", "Machine Learning", "Artificial Intelligence"]
    }
    
    # Dictionary of chapters for each subject
    chapters_by_subject = {
        # Mathematics chapters for school classes
        "Mathematics": ["Algebra", "Geometry", "Arithmetic", "Statistics", "Trigonometry"],
        "Science": ["Physics", "Chemistry", "Biology", "Environment", "Scientific Method"],
        "Social Studies": ["History", "Geography", "Civics", "Economics", "Current Affairs"],
        "English": ["Grammar", "Literature", "Writing", "Reading Comprehension", "Vocabulary"],
        "Hindi": ["Grammar", "Literature", "Writing", "Reading Comprehension", "Vocabulary"],
        
        # Higher education subjects
        "Physics": ["Mechanics", "Electromagnetism", "Thermodynamics", "Optics", "Modern Physics"],
        "Chemistry": ["Organic Chemistry", "Inorganic Chemistry", "Physical Chemistry", "Analytical Chemistry", "Biochemistry"],
        "Biology": ["Cell Biology", "Genetics", "Ecology", "Human Physiology", "Evolution"],
        "Computer Science": ["Programming Fundamentals", "Data Structures", "Algorithms", "Computer Architecture", "Operating Systems"],
        
        # B.Tech subjects
        "Engineering Mathematics": ["Calculus", "Linear Algebra", "Differential Equations", "Probability", "Numerical Methods"],
        "Data Structures": ["Arrays", "Linked Lists", "Trees", "Graphs", "Hashing"],
        "Computer Networks": ["Network Models", "Data Link Layer", "Network Layer", "Transport Layer", "Application Layer"],
        "Database Systems": ["ER Model", "Relational Model", "SQL", "Normalization", "Transaction Processing"],
        "Operating Systems": ["Process Management", "Memory Management", "File Systems", "I/O Systems", "Security"],
        
        # M.Tech subjects
        "Advanced Algorithms": ["Graph Algorithms", "Dynamic Programming", "Greedy Algorithms", "NP-Completeness", "Approximation Algorithms"],
        "Machine Learning": ["Supervised Learning", "Unsupervised Learning", "Neural Networks", "Decision Trees", "Support Vector Machines"],
        "Artificial Intelligence": ["Search Algorithms", "Knowledge Representation", "Planning", "Natural Language Processing", "Computer Vision"],
        "Cloud Computing": ["Virtualization", "Service Models", "Deployment Models", "Security", "Scalability"],
        "Data Mining": ["Data Preprocessing", "Association Rules", "Classification", "Clustering", "Anomaly Detection"],
        
        # BSc subjects
        "Statistics": ["Probability", "Sampling", "Hypothesis Testing", "Regression", "ANOVA"],
        
        # BA subjects
        "History": ["Ancient History", "Medieval History", "Modern History", "World History", "Indian History"],
        "Political Science": ["Political Theory", "Indian Constitution", "International Relations", "Public Administration", "Comparative Politics"],
        "Economics": ["Microeconomics", "Macroeconomics", "Development Economics", "International Economics", "Public Finance"],
        "Sociology": ["Social Theory", "Research Methods", "Social Institutions", "Social Change", "Social Problems"],
        "Psychology": ["Cognitive Psychology", "Social Psychology", "Developmental Psychology", "Abnormal Psychology", "Personality"],
        
        # BS Online subjects
        "Programming": ["Python", "Java", "C++", "JavaScript", "Data Structures"],
        "Data Science": ["Data Analysis", "Data Visualization", "Machine Learning", "Big Data", "Statistical Methods"],
        "Web Development": ["HTML/CSS", "JavaScript", "Backend Development", "Frontend Frameworks", "Database Integration"],
    }
    
    try:
        # Get all qualifications
        qualifications = Qualification.query.all()
        
        for qualification in qualifications:
            # Get subjects for this qualification
            subjects_list = subjects_by_qualification.get(qualification.name, [])
            
            for subject_name in subjects_list:
                # Check if subject already exists for this qualification
                existing_subject = Subject.query.filter_by(name=subject_name, qualification_id=qualification.id).first()
                
                if not existing_subject:
                    subject = Subject(
                        name=subject_name,
                        description=f"{subject_name} for {qualification.name}",
                        qualification_id=qualification.id
                    )
                    db.session.add(subject)
                    db.session.flush()  # Flush to get the subject ID
                    
                    # Add chapters for this subject
                    chapters_list = chapters_by_subject.get(subject_name, [])
                    if not chapters_list:
                        # If no specific chapters defined, use generic ones
                        chapters_list = [f"Chapter {i+1}" for i in range(5)]
                    
                    for chapter_name in chapters_list:
                        chapter = Chapter(
                            name=chapter_name,
                            description=f"{chapter_name} in {subject_name} for {qualification.name}",
                            subject_id=subject.id
                        )
                        db.session.add(chapter)
                    
                    print(f"Added subject {subject_name} with chapters for {qualification.name}")
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error creating subjects and chapters: {e}")

def create_quizzes_and_questions():
    """Create quizzes and questions for each qualification, subject, and chapter"""
    try:
        # Create whole quizzes (linked to qualifications)
        qualifications = Qualification.query.all()
        
        for qualification in qualifications:
            # Create whole quiz for each qualification
            whole_quiz = Quiz(
                title=f"General Quiz for {qualification.name}",
                quiz_type="whole",
                qualification_id=qualification.id,
                subject_id=None,
                chapter_id=None,
                date_created=datetime.now(),
                duration=30  # 30 minutes
            )
            db.session.add(whole_quiz)
            db.session.flush()
            
            # Add 10 random questions to the whole quiz
            add_random_questions(whole_quiz.id, 10)
            
            # Get all subjects for this qualification
            subjects = Subject.query.filter_by(qualification_id=qualification.id).all()
            
            for subject in subjects:
                # Create 2 subject quizzes for each subject
                for i in range(2):
                    subject_quiz = Quiz(
                        title=f"{subject.name} Quiz {i+1} for {qualification.name}",
                        quiz_type="subject",
                        qualification_id=qualification.id,
                        subject_id=subject.id,
                        chapter_id=None,
                        date_created=datetime.now(),
                        duration=20  # 20 minutes
                    )
                    db.session.add(subject_quiz)
                    db.session.flush()
                    
                    # Add 5 questions to the subject quiz
                    add_subject_questions(subject_quiz.id, subject.id, 5)
                
                # Get all chapters for this subject
                chapters = Chapter.query.filter_by(subject_id=subject.id).all()
                
                for chapter in chapters:
                    # Create 2 chapter quizzes for each chapter
                    for i in range(2):
                        chapter_quiz = Quiz(
                            title=f"{chapter.name} Quiz {i+1} for {subject.name}",
                            quiz_type="chapter",
                            qualification_id=qualification.id,
                            subject_id=subject.id,
                            chapter_id=chapter.id,
                            date_created=datetime.now(),
                            duration=15  # 15 minutes
                        )
                        db.session.add(chapter_quiz)
                        db.session.flush()
                        
                        # Add 5 questions to the chapter quiz
                        add_chapter_questions(chapter_quiz.id, subject.id, chapter.id, 5)
        
        db.session.commit()
        print("Created quizzes and questions successfully")
    except Exception as e:
        db.session.rollback()
        print(f"Error creating quizzes and questions: {e}")

def add_random_questions(quiz_id, count):
    """Add random questions to a whole quiz"""
    question_templates = [
        "What is the correct answer to {subject} problem?",
        "Which of the following is true about {subject}?",
        "In {subject}, what is the principle behind {concept}?",
        "Calculate the result of the following {subject} problem.",
        "Identify the correct statement about {subject}."
    ]
    
    subjects = ["Mathematics", "Science", "Physics", "Chemistry", "Biology", "History", "Geography"]
    concepts = ["conservation of energy", "Newton's laws", "cell division", "chemical bonding", "democracy", "plate tectonics"]
    
    for i in range(count):
        subject = random.choice(subjects)
        concept = random.choice(concepts)
        question_text = random.choice(question_templates).format(subject=subject, concept=concept)
        
        # Create options
        options = [
            f"Option A for question {i+1}",
            f"Option B for question {i+1}",
            f"Option C for question {i+1}",
            f"Option D for question {i+1}"
        ]
        
        # Randomly select correct option
        correct_option = random.randint(0, 3)
        
        question = Question(
            quiz_id=quiz_id,
            subject_id=None,  # Not tied to a specific subject
            chapter_id=None,  # Not tied to a specific chapter
            question_text=question_text,
            option1=options[0],
            option2=options[1],
            option3=options[2],
            option4=options[3],
            correct_option=correct_option
        )
        db.session.add(question)

def add_subject_questions(quiz_id, subject_id, count):
    """Add subject-specific questions to a subject quiz"""
    # Get the subject name
    subject = Subject.query.get(subject_id)
    subject_name = subject.name if subject else "Unknown Subject"
    
    question_templates = [
        f"What is the fundamental concept in {subject_name}?",
        f"Which principle is most important in {subject_name}?",
        f"How would you solve this {subject_name} problem?",
        f"In {subject_name}, what is the relationship between X and Y?",
        f"What is the application of {subject_name} in real life?"
    ]
    
    for i in range(count):
        question_text = question_templates[i % len(question_templates)]
        
        # Create options
        options = [
            f"First possible answer for {subject_name}",
            f"Second possible answer for {subject_name}",
            f"Third possible answer for {subject_name}",
            f"Fourth possible answer for {subject_name}"
        ]
        
        # Randomly select correct option
        correct_option = random.randint(0, 3)
        
        question = Question(
            quiz_id=quiz_id,
            subject_id=subject_id,
            chapter_id=None,  # Not tied to a specific chapter
            question_text=question_text,
            option1=options[0],
            option2=options[1],
            option3=options[2],
            option4=options[3],
            correct_option=correct_option
        )
        db.session.add(question)

def add_chapter_questions(quiz_id, subject_id, chapter_id, count):
    """Add chapter-specific questions to a chapter quiz"""
    # Get the chapter name
    chapter = Chapter.query.get(chapter_id)
    chapter_name = chapter.name if chapter else "Unknown Chapter"
    
    # Get the subject name
    subject = Subject.query.get(subject_id)
    subject_name = subject.name if subject else "Unknown Subject"
    
    question_templates = [
        f"In the {chapter_name} chapter of {subject_name}, what is the key concept?",
        f"Which formula is used in {chapter_name}?",
        f"Explain the process described in {chapter_name}.",
        f"What is the significance of {chapter_name} in {subject_name}?",
        f"How does {chapter_name} relate to other chapters in {subject_name}?"
    ]
    
    for i in range(count):
        question_text = question_templates[i % len(question_templates)]
        
        # Create options
        options = [
            f"First answer related to {chapter_name}",
            f"Second answer related to {chapter_name}",
            f"Third answer related to {chapter_name}",
            f"Fourth answer related to {chapter_name}"
        ]
        
        # Randomly select correct option
        correct_option = random.randint(0, 3)
        
        question = Question(
            quiz_id=quiz_id,
            subject_id=subject_id,
            chapter_id=chapter_id,
            question_text=question_text,
            option1=options[0],
            option2=options[1],
            option3=options[2],
            option4=options[3],
            correct_option=correct_option
        )
        db.session.add(question)

def create_admin_user():
    """Create admin user with appropriate role"""
    try:
        # Check if admin already exists
        existing_admin = User.query.filter_by(email='admin@study.iitm.ac.in').first()
        
        if not existing_admin:
            # Get admin role
            admin_role = Role.query.filter_by(name='admin').first()
            
            # Get a qualification (B.Tech)
            qualification = Qualification.query.filter_by(name='B.Tech').first()
            
            if not qualification:
                print("Error: B.Tech qualification not found")
                return
            
            # Create admin user
            admin_user = User(
                email='admin@study.iitm.ac.in',
                password=hash_password('admin123'),  # You should use a stronger password in production
                fullname='Admin User',
                dob=datetime.strptime('1990-01-01', '%Y-%m-%d'),
                gender='male',
                qualification_id=qualification.id,
                fs_uniquifier=str(uuid.uuid4()),
                active=True,
                created_at=datetime.now()
            )
            db.session.add(admin_user)
            db.session.flush()
            
            # Add admin role to user
            if admin_role:
                user_role = UserRoles(
                    user_id=admin_user.id,
                    role_id=admin_role.id
                )
                db.session.add(user_role)
            
            # Add subjects to admin user (all B.Tech subjects)
            subjects = Subject.query.filter_by(qualification_id=qualification.id).all()
            for subject in subjects:
                user_subject = UserSubjects(
                    user_id=admin_user.id,
                    subject_id=subject.id
                )
                db.session.add(user_subject)
            
            print("Admin user created successfully")
            db.session.commit()
        else:
            print("Admin user already exists")
    except Exception as e:
        db.session.rollback()
        print(f"Error creating admin user: {e}")

def create_recent_activity():
    """Create recent activity entry for data initialization"""
    try:
        # Get admin user
        admin_user = User.query.filter_by(email='admin@study.iitm.ac.in').first()
        
        if admin_user:
            activity = RecentActivity(
                user_id=admin_user.id,
                action="Auto data added by admin",
                timestamp=datetime.now()
            )
            db.session.add(activity)
            db.session.commit()
            print("Recent activity created")
        else:
            print("Admin user not found, cannot create activity")
    except Exception as e:
        db.session.rollback()
        print(f"Error creating recent activity: {e}")

# Call the function to create all initial data
create_initial_data()