# =====================================================================
#  STUDENT ATTENDANCE MONITORING SYSTEM  (Console-Based)
#  Users: Admin, Teacher, Student
#  Style: if / elif / else only  (no def functions)
#  Data is saved to attendance_records.txt (same folder as this file)
#
#  A "class" is one subject inside one section, and every class has a
#  Class ID (C001, C002, ...). Teachers are assigned to a class by
#  typing its Class ID.
#
#  Every time the program asks you to type something that was already
#  entered before (a teacher, student, subject, section or class), it
#  first shows a TITLED table with only the information you need.
#
#  NEW IN THIS VERSION
#   - The Admin can now REMOVE what he added. The last action in each
#     Admin menu is a remove choice:
#        Admin > Teacher  -> Remove Teacher
#        Admin > Student  -> Remove Student
#        Admin > Classes  -> Remove Class
#   - Every removal asks "Type Y to confirm" first.
#   - Teacher > Check Attendance records TODAY'S DATE automatically. The
#     teacher no longer types a date, so a wrong date cannot be entered.
#   - A section can hold as many subjects and students as you like.
#     Choose the section once, then keep adding subjects (or students)
#     one after another until you answer N to "Add another?".
# =====================================================================

# ------------------------- TODAY'S DATE ------------------------------
# Attendance is always recorded with today's date, read from the computer's
# clock. This is the only import in the program (built into Python).
from datetime import date

# ------------------------- DATA FILE (STORAGE) -----------------------
# The data file is kept in the same folder as this script, no matter which
# folder VS Code (or the terminal) starts the program from.
# __file__ holds the full path of this script. We cut off the file name and
# keep the folder part, then add attendance_records.txt to it.
DATA_FILE = "attendance_records.txt"
if "__file__" in globals():
    here = __file__.replace("\\", "/")
    slash = here.rfind("/")
    DATA_FILE = here[:slash + 1] + "attendance_records.txt"
print("Data file: " + DATA_FILE)

# ---------------------------- DATA STORAGE ---------------------------
# subjects   -> {"code": "", "name": "", "units": ""}
# teachers   -> {"id": "", "password": "", "last": "", "first": "", "address": ""}
# students   -> {"id": "", "password": "", "last": "", "first": "", "age": "", "address": "", "contact": "", "section": ""}
# sections   -> just the section names, for example "BSIT-1A"
# classes    -> {"id": "C001", "section": "", "code": "", "teacher": "<teacher id, or empty>"}
# attendance -> {"date": "", "code": "", "section": "", "student_id": "", "status": ""}
subjects = []
teachers = []
students = []
sections = []
classes = []
attendance = []

# Each line of the text file is one record, fields separated by |
#   SUBJECT|code|name|units
#   TEACHER|id|password|last name|first name|address
#   STUDENT|id|password|last name|first name|age|address|contact|section
#   SECTION|name
#   CLASS|class id|section|subject code|teacher id
#   ATTENDANCE|date|code|section|student id|status

# Opening in "a" (append) mode creates the file if it is missing and never
# erases what is already inside, so no file-existence check is needed.
fh = open(DATA_FILE, "a")
fh.close()

fh = open(DATA_FILE, "r")
for line in fh:
    line = line.strip()
    parts = line.split("|")

    if parts[0] == "SUBJECT" and len(parts) == 4:
        subjects.append({"code": parts[1], "name": parts[2], "units": parts[3]})

    elif parts[0] == "TEACHER" and len(parts) == 6:
        teachers.append({"id": parts[1], "password": parts[2], "last": parts[3],
                         "first": parts[4], "address": parts[5]})

    elif parts[0] == "STUDENT" and len(parts) == 9:
        students.append({"id": parts[1], "password": parts[2], "last": parts[3], "first": parts[4],
                         "age": parts[5], "address": parts[6], "contact": parts[7], "section": parts[8]})

    elif parts[0] == "SECTION" and (len(parts) == 2 or len(parts) == 3):
        sections.append(parts[1])
        # OLD FILES (previous version) kept the subjects inside the SECTION line
        # like  SECTION|name|code~teacher;code~teacher
        # Each one is turned into a class and given a new Class ID.
        if len(parts) == 3 and parts[2] != "":
            for piece in parts[2].split(";"):
                pair = piece.split("~")
                if len(pair) == 2:
                    highest = 0
                    for cl in classes:
                        num = cl["id"][1:]
                        if num.isdigit() and int(num) > highest:
                            highest = int(num)
                    classes.append({"id": "C" + f"{highest + 1:03d}", "section": parts[1],
                                    "code": pair[0], "teacher": pair[1]})

    elif parts[0] == "CLASS" and len(parts) == 5:
        classes.append({"id": parts[1], "section": parts[2], "code": parts[3], "teacher": parts[4]})

    elif parts[0] == "ATTENDANCE" and len(parts) == 6:
        attendance.append({"date": parts[1], "code": parts[2], "section": parts[3],
                           "student_id": parts[4], "status": parts[5]})

    elif line != "":
        print("Warning: skipped an unreadable line in the data file.")
fh.close()

if len(subjects) > 0 or len(teachers) > 0 or len(students) > 0 or len(sections) > 0 or len(attendance) > 0:
    print("Saved data loaded.")

ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

running = True
while running:
    print("\n" + "=" * 62)
    print("        STUDENT ATTENDANCE MONITORING SYSTEM")
    print("=" * 62)
    print("[1] Admin")
    print("[2] Teacher")
    print("[3] Student")
    print("[4] Exit")
    role = input("Login as: ").strip()

    # =================================================================
    #                              ADMIN
    # =================================================================
    if role == "1":
        user = input("Admin username: ").strip()
        pw = input("Admin password: ").strip()

        if user == ADMIN_USER and pw == ADMIN_PASS:
            print("\nWelcome, Admin!")
            admin_on = True
            mode = "main"          # which admin menu is showing right now
            while admin_on:
                show_table = False
                show_classes = False
                show_section = ""      # name of the section whose students should be shown

                # ---------------------- MAIN ADMIN MENU ----------------------
                if mode == "main":
                    print("\n--- ADMIN MENU ---")
                    print("[1] Teacher")
                    print("[2] Student")
                    print("[3] Subject")
                    print("[4] Classes")
                    print("[5] Logout")
                    a = input("Choose: ").strip()

                    if a == "1":
                        mode = "teacher"
                    elif a == "2":
                        mode = "student"
                    elif a == "3":
                        mode = "subject"
                    elif a == "4":
                        mode = "classes"
                    elif a == "5":
                        print("Admin logged out.")
                        admin_on = False
                    else:
                        print("Invalid choice.")

                # ------------------------- 1. TEACHER -------------------------
                elif mode == "teacher":
                    print("\n--- ADMIN > TEACHER ---")
                    print("[1] Add Teacher Account")
                    print("[2] View Teachers")
                    print("[3] Remove Teacher")
                    print("[4] Back")
                    tm = input("Choose: ").strip()

                    if tm == "1":
                        print("\n--- ADD TEACHER ACCOUNT ---")
                        t_first = input("First name: ").strip()
                        t_last = input("Last name: ").strip()
                        t_pass = input("Password: ").strip()
                        t_address = input("Address: ").strip()

                        bad = False
                        for text in [t_first, t_last, t_address, t_pass]:
                            if "|" in text or ";" in text or "~" in text:
                                bad = True

                        if t_first == "" or t_last == "" or t_address == "" or t_pass == "":
                            print("All fields are required.")
                        elif bad:
                            print("Please do not use the characters | ; ~ in the details.")
                        else:
                            highest = 0
                            for t in teachers:
                                num = t["id"][1:]
                                if num.isdigit() and int(num) > highest:
                                    highest = int(num)
                            t_id = "T" + f"{highest + 1:03d}"
                            teachers.append({"id": t_id, "password": t_pass, "last": t_last,
                                             "first": t_first, "address": t_address})
                            print(f"\nTeacher account created. Teacher ID: {t_id}")
                        show_table = True

                    elif tm == "2":
                        show_table = True

                    # ---------- 3. REMOVE TEACHER ----------
                    elif tm == "3":
                        if len(teachers) == 0:
                            print("No teacher accounts to remove.")
                        else:
                            # ----- TABLE: TEACHERS (only ID and name are needed) -----
                            print("\n" + "=" * 48)
                            print(f"{'TEACHERS':^48}")
                            print("=" * 48)
                            print(f"{'Teacher ID':<12}{'Last Name':<18}{'First Name'}")
                            print("-" * 48)
                            for t in teachers:
                                print(f"{t['id']:<12}{t['last']:<18}{t['first']}")
                            print("-" * 48)
                            rem_id = input("\nTeacher ID to remove: ").strip().upper()

                            target = None
                            for t in teachers:
                                if t["id"] == rem_id:
                                    target = t

                            if target is None:
                                print("Teacher not found.")
                            else:
                                sure = input(f"Remove {target['last']}, {target['first']} ({rem_id})? Type Y to confirm: ").strip().upper()
                                if sure == "Y":
                                    # classes taught by this teacher are kept, but left without a teacher
                                    freed = 0
                                    for cl in classes:
                                        if cl["teacher"] == rem_id:
                                            cl["teacher"] = ""
                                            freed = freed + 1
                                    teachers.remove(target)
                                    print(f"Teacher {rem_id} removed.")
                                    if freed > 0:
                                        print(f"{freed} class(es) now have no teacher. Assign a new one in Admin > Classes.")
                                else:
                                    print("Removal cancelled.")
                        show_table = True

                    elif tm == "4":
                        mode = "main"

                    else:
                        print("Invalid choice.")

                    if show_table:
                        # ----- TABLE: TEACHER ACCOUNTS -----
                        if len(teachers) == 0:
                            print("\nNo teacher accounts yet.")
                        else:
                            print("\n" + "=" * 90)
                            print(f"{'TEACHER ACCOUNTS':^90}")
                            print("=" * 90)
                            print(f"{'Teacher ID':<12}{'Last Name':<18}{'First Name':<18}{'Address':<30}{'Password'}")
                            print("-" * 90)
                            for t in teachers:
                                print(f"{t['id']:<12}{t['last']:<18}{t['first']:<18}{t['address']:<30}{t['password']}")
                            print("-" * 90)

                # ------------------------- 2. STUDENT -------------------------
                elif mode == "student":
                    print("\n--- ADMIN > STUDENT ---")
                    print("[1] Add Student Account")
                    print("[2] View Students")
                    print("[3] Remove Student")
                    print("[4] Back")
                    sm = input("Choose: ").strip()

                    if sm == "1":
                        print("\n--- ADD STUDENT ACCOUNT ---")
                        s_first = input("First name: ").strip()
                        s_last = input("Last name: ").strip()
                        s_age = input("Age: ").strip()
                        s_address = input("Address: ").strip()
                        s_contact = input("Contact number: ").strip()
                        s_pass = input("Password: ").strip()

                        bad = False
                        for text in [s_first, s_last, s_age, s_address, s_contact, s_pass]:
                            if "|" in text or ";" in text or "~" in text:
                                bad = True

                        if s_first == "" or s_last == "" or s_age == "" or s_address == "" or s_contact == "" or s_pass == "":
                            print("All fields are required.")
                        elif not s_age.isdigit() or int(s_age) < 1:
                            print("Age must be a whole number.")
                        elif bad:
                            print("Please do not use the characters | ; ~ in the details.")
                        else:
                            highest = 0
                            for st in students:
                                num = st["id"][1:]
                                if num.isdigit() and int(num) > highest:
                                    highest = int(num)
                            s_id = "S" + f"{highest + 1:03d}"
                            students.append({"id": s_id, "password": s_pass, "last": s_last, "first": s_first,
                                             "age": s_age, "address": s_address, "contact": s_contact, "section": ""})
                            print(f"\nStudent account created. Student ID: {s_id}")
                            print("Tip: add the student to a section in Admin > Classes.")
                        show_table = True

                    elif sm == "2":
                        show_table = True

                    # ---------- 3. REMOVE STUDENT ----------
                    elif sm == "3":
                        if len(students) == 0:
                            print("No student accounts to remove.")
                        else:
                            # ----- TABLE: STUDENTS (ID, name and section are needed) -----
                            print("\n" + "=" * 54)
                            print(f"{'STUDENTS':^54}")
                            print("=" * 54)
                            print(f"{'Student ID':<12}{'Last Name':<16}{'First Name':<16}{'Section'}")
                            print("-" * 54)
                            for st in students:
                                sec_text = st["section"]
                                if sec_text == "":
                                    sec_text = "(none)"
                                print(f"{st['id']:<12}{st['last']:<16}{st['first']:<16}{sec_text}")
                            print("-" * 54)
                            rem_id = input("\nStudent ID to remove: ").strip().upper()

                            target = None
                            for st in students:
                                if st["id"] == rem_id:
                                    target = st

                            if target is None:
                                print("Student not found.")
                            else:
                                print("Note: this student's attendance records will also be deleted.")
                                sure = input(f"Remove {target['last']}, {target['first']} ({rem_id})? Type Y to confirm: ").strip().upper()
                                if sure == "Y":
                                    kept = []
                                    for r in attendance:
                                        if r["student_id"] != rem_id:
                                            kept.append(r)
                                    deleted = len(attendance) - len(kept)
                                    attendance = kept
                                    students.remove(target)
                                    print(f"Student {rem_id} removed.")
                                    if deleted > 0:
                                        print(f"{deleted} attendance record(s) of this student were also deleted.")
                                else:
                                    print("Removal cancelled.")
                        show_table = True

                    elif sm == "4":
                        mode = "main"

                    else:
                        print("Invalid choice.")

                    if show_table:
                        # ----- TABLE: STUDENT ACCOUNTS -----
                        if len(students) == 0:
                            print("\nNo students yet.")
                        else:
                            print("\n" + "=" * 100)
                            print(f"{'STUDENT ACCOUNTS':^100}")
                            print("=" * 100)
                            print(f"{'Student ID':<12}{'Last Name':<16}{'First Name':<16}{'Age':<6}{'Address':<24}{'Contact No.':<15}{'Password'}")
                            print("-" * 100)
                            for st in students:
                                print(f"{st['id']:<12}{st['last']:<16}{st['first']:<16}{st['age']:<6}{st['address']:<24}{st['contact']:<15}{st['password']}")
                            print("-" * 100)

                # ------------------------- 3. SUBJECT -------------------------
                elif mode == "subject":
                    print("\n--- ADMIN > SUBJECT ---")
                    print("[1] Add Subject")
                    print("[2] View Subjects")
                    print("[3] Back")
                    jm = input("Choose: ").strip()

                    if jm == "1":
                        print("\n--- ADD SUBJECT ---")
                        code = input("Subject code: ").strip().upper()
                        name = input("Subject name: ").strip()
                        units = input("Credit units: ").strip()

                        exists = False
                        for s in subjects:
                            if s["code"] == code:
                                exists = True

                        bad = False
                        for text in [code, name]:
                            if "|" in text or ";" in text or "~" in text:
                                bad = True

                        if code == "" or name == "" or units == "":
                            print("Subject code, name and credit units are all required.")
                        elif not units.isdigit() or int(units) < 1:
                            print("Credit units must be a whole number (1 or more).")
                        elif bad:
                            print("Please do not use the characters | ; ~ in the details.")
                        elif exists:
                            print("That subject code already exists.")
                        else:
                            subjects.append({"code": code, "name": name, "units": units})
                            print("Subject added.")
                        show_table = True

                    elif jm == "2":
                        show_table = True

                    elif jm == "3":
                        mode = "main"

                    else:
                        print("Invalid choice.")

                    if show_table:
                        # ----- TABLE: SUBJECTS -----
                        if len(subjects) == 0:
                            print("\nNo subjects yet.")
                        else:
                            print("\n" + "=" * 62)
                            print(f"{'SUBJECTS':^62}")
                            print("=" * 62)
                            print(f"{'Subject Code':<16}{'Subject Name':<34}{'Credit Units'}")
                            print("-" * 62)
                            for s in subjects:
                                print(f"{s['code']:<16}{s['name']:<34}{s['units']}")
                            print("-" * 62)

                # ------------------------- 4. CLASSES -------------------------
                # A class = one subject inside one section. Each class has a Class ID.
                elif mode == "classes":
                    print("\n--- ADMIN > CLASSES ---")
                    print("[1] Create Section")
                    print("[2] Add Subjects to Section  (creates a Class ID for each)")
                    print("[3] Add Teacher to Class     (using the Class ID)")
                    print("[4] Add Students to Section")
                    print("[5] View Classes")
                    print("[6] View Section")
                    print("[7] Remove Class             (using the Class ID)")
                    print("[8] Back")
                    cm = input("Choose: ").strip()

                    # ---------- 1. CREATE SECTION ----------
                    if cm == "1":
                        print("\n--- CREATE SECTION ---")
                        sec = input("New section name: ").strip().upper()

                        if sec == "":
                            print("Section name cannot be empty.")
                        elif "|" in sec or ";" in sec or "~" in sec:
                            print("Please do not use the characters | ; ~ in the section name.")
                        elif sec in sections:
                            print("That section already exists.")
                        else:
                            sections.append(sec)
                            print(f"Section {sec} created.")
                            print("Tip: next, add subjects to it (option 2).")
                        show_classes = True

                    # ---------- 2. ADD SUBJECTS TO SECTION (makes a class for each) ----------
                    # A section can hold as many subjects as you want. You choose the
                    # section once, then keep adding subjects until you answer N.
                    elif cm == "2":
                        if len(sections) == 0:
                            print("Create a section first.")
                        elif len(subjects) == 0:
                            print("Add subjects first (Admin > Subject).")
                        else:
                            # ----- STEP 1: TABLE: SECTIONS (only the section name is needed) -----
                            print("\n" + "=" * 30)
                            print(f"{'SECTIONS':^30}")
                            print("=" * 30)
                            print("Section")
                            print("-" * 30)
                            for sec_name in sections:
                                print(sec_name)
                            print("-" * 30)
                            sec = input("\nSection: ").strip().upper()

                            if sec not in sections:
                                print("Section not found.")
                            else:
                                adding = True
                                while adding:
                                    # subjects that are not in this section yet
                                    available = []
                                    for s in subjects:
                                        taken = False
                                        for cl in classes:
                                            if cl["section"] == sec and cl["code"] == s["code"]:
                                                taken = True
                                        if not taken:
                                            available.append(s)

                                    if len(available) == 0:
                                        print(f"\nEvery subject is already in section {sec}.")
                                        adding = False
                                    else:
                                        # ----- STEP 2: TABLE: SUBJECTS NOT YET IN THIS SECTION -----
                                        title = "SUBJECTS NOT YET IN SECTION " + sec
                                        print("\n" + "=" * 60)
                                        print(f"{title:^60}")
                                        print("=" * 60)
                                        print(f"{'Subject Code':<16}{'Subject Name'}")
                                        print("-" * 60)
                                        for s in available:
                                            print(f"{s['code']:<16}{s['name']}")
                                        print("-" * 60)
                                        code = input("\nSubject code to add: ").strip().upper()

                                        found = False
                                        for s in subjects:
                                            if s["code"] == code:
                                                found = True

                                        already = False
                                        for cl in classes:
                                            if cl["section"] == sec and cl["code"] == code:
                                                already = True

                                        if not found:
                                            print("Subject not found.")
                                        elif already:
                                            print("That subject is already in this section.")
                                        else:
                                            highest = 0
                                            for cl in classes:
                                                num = cl["id"][1:]
                                                if num.isdigit() and int(num) > highest:
                                                    highest = int(num)
                                            new_id = "C" + f"{highest + 1:03d}"
                                            classes.append({"id": new_id, "section": sec, "code": code, "teacher": ""})
                                            print(f"{code} added to section {sec}.  Class ID: {new_id}")

                                        again = input(f"Add another subject to section {sec}? (Y/N): ").strip().upper()
                                        if again != "Y":
                                            adding = False
                                print("Tip: assign a teacher to each class (option 3).")
                        show_classes = True

                    # ---------- 3. ADD TEACHER TO CLASS (by Class ID) ----------
                    elif cm == "3":
                        if len(teachers) == 0:
                            print("No teacher accounts yet. Add a teacher first (Admin > Teacher).")
                        elif len(classes) == 0:
                            print("No classes yet. Add a subject to a section first (option 2).")
                        else:
                            # ----- STEP 1: TABLE: CLASSES (Class ID, section, subject, current teacher) -----
                            print("\n" + "=" * 95)
                            print(f"{'CLASSES':^95}")
                            print("=" * 95)
                            print(f"{'Class ID':<10}{'Section':<12}{'Subject Code':<16}{'Subject Name':<28}{'Teacher'}")
                            print("-" * 95)
                            for cl in classes:
                                subj_name = ""
                                for s in subjects:
                                    if s["code"] == cl["code"]:
                                        subj_name = s["name"]
                                teacher_text = "(none yet)"
                                for t in teachers:
                                    if t["id"] == cl["teacher"]:
                                        teacher_text = t["id"] + " - " + t["last"] + ", " + t["first"]
                                print(f"{cl['id']:<10}{cl['section']:<12}{cl['code']:<16}{subj_name:<28}{teacher_text}")
                            print("-" * 95)
                            cid = input("\nClass ID: ").strip().upper()

                            target = None
                            for cl in classes:
                                if cl["id"] == cid:
                                    target = cl

                            if target is None:
                                print("Class ID not found.")
                            else:
                                # ----- STEP 2: TABLE: TEACHERS (only ID and name are needed) -----
                                print("\n" + "=" * 48)
                                print(f"{'TEACHERS':^48}")
                                print("=" * 48)
                                print(f"{'Teacher ID':<12}{'Last Name':<18}{'First Name'}")
                                print("-" * 48)
                                for t in teachers:
                                    print(f"{t['id']:<12}{t['last']:<18}{t['first']}")
                                print("-" * 48)
                                t_id = input("\nTeacher ID: ").strip().upper()

                                teacher_ok = False
                                for t in teachers:
                                    if t["id"] == t_id:
                                        teacher_ok = True

                                if not teacher_ok:
                                    print("Teacher not found.")
                                else:
                                    old_teacher = target["teacher"]
                                    target["teacher"] = t_id
                                    print(f"Teacher {t_id} assigned to class {cid} ({target['section']} | {target['code']}).")
                                    if old_teacher != "" and old_teacher != t_id:
                                        print(f"(Previous teacher {old_teacher} was replaced.)")
                        show_classes = True

                    # ---------- 4. ADD STUDENTS TO SECTION ----------
                    # A section can hold as many students as you want. You choose the
                    # section once, then keep adding students until you answer N.
                    elif cm == "4":
                        if len(students) == 0:
                            print("No students yet. Add a student first (Admin > Student).")
                        elif len(sections) == 0:
                            print("Create a section first.")
                        else:
                            # ----- STEP 1: TABLE: SECTIONS (only the section name is needed) -----
                            print("\n" + "=" * 30)
                            print(f"{'SECTIONS':^30}")
                            print("=" * 30)
                            print("Section")
                            print("-" * 30)
                            for sec_name in sections:
                                print(sec_name)
                            print("-" * 30)
                            sec = input("\nSection: ").strip().upper()

                            if sec not in sections:
                                print("Section not found.")
                            else:
                                adding = True
                                while adding:
                                    # students that are not in this section yet
                                    available = []
                                    for st in students:
                                        if st["section"] != sec:
                                            available.append(st)

                                    if len(available) == 0:
                                        print(f"\nEvery student is already in section {sec}.")
                                        adding = False
                                    else:
                                        # ----- STEP 2: TABLE: STUDENTS NOT YET IN THIS SECTION -----
                                        title = "STUDENTS NOT YET IN SECTION " + sec
                                        print("\n" + "=" * 60)
                                        print(f"{title:^60}")
                                        print("=" * 60)
                                        print(f"{'Student ID':<12}{'Last Name':<18}{'First Name':<18}{'Current Section'}")
                                        print("-" * 60)
                                        for st in available:
                                            sec_text = st["section"]
                                            if sec_text == "":
                                                sec_text = "(none)"
                                            print(f"{st['id']:<12}{st['last']:<18}{st['first']:<18}{sec_text}")
                                        print("-" * 60)
                                        s_id = input("\nStudent ID to add: ").strip().upper()

                                        target = None
                                        for st in students:
                                            if st["id"] == s_id:
                                                target = st

                                        if target is None:
                                            print("Student not found.")
                                        elif target["section"] == sec:
                                            print("That student is already in this section.")
                                        else:
                                            old_section = target["section"]
                                            target["section"] = sec
                                            print(f"{target['first']} {target['last']} is now in section {sec}.")
                                            if old_section != "":
                                                print(f"(Moved from section {old_section}.)")

                                        again = input(f"Add another student to section {sec}? (Y/N): ").strip().upper()
                                        if again != "Y":
                                            adding = False
                                show_section = sec

                    # ---------- 5. VIEW CLASSES (shows only the classes table) ----------
                    elif cm == "5":
                        show_classes = True

                    # ---------- 6. VIEW SECTION (admin chooses which section to see) ----------
                    elif cm == "6":
                        if len(sections) == 0:
                            print("No sections yet. Create a section first (option 1).")
                        else:
                            # ----- TABLE: SECTIONS (only the section name is needed) -----
                            print("\n" + "=" * 30)
                            print(f"{'SECTIONS':^30}")
                            print("=" * 30)
                            print("Section")
                            print("-" * 30)
                            for sec_name in sections:
                                print(sec_name)
                            print("-" * 30)
                            sec = input("\nSection to view: ").strip().upper()

                            if sec not in sections:
                                print("Section not found.")
                            else:
                                show_section = sec

                    # ---------- 7. REMOVE CLASS (by Class ID) ----------
                    elif cm == "7":
                        if len(classes) == 0:
                            print("No classes to remove.")
                        else:
                            # ----- TABLE: CLASSES (Class ID, section, subject, teacher) -----
                            print("\n" + "=" * 95)
                            print(f"{'CLASSES':^95}")
                            print("=" * 95)
                            print(f"{'Class ID':<10}{'Section':<12}{'Subject Code':<16}{'Subject Name':<28}{'Teacher'}")
                            print("-" * 95)
                            for cl in classes:
                                subj_name = ""
                                for s in subjects:
                                    if s["code"] == cl["code"]:
                                        subj_name = s["name"]
                                teacher_text = "(none yet)"
                                for t in teachers:
                                    if t["id"] == cl["teacher"]:
                                        teacher_text = t["id"] + " - " + t["last"] + ", " + t["first"]
                                print(f"{cl['id']:<10}{cl['section']:<12}{cl['code']:<16}{subj_name:<28}{teacher_text}")
                            print("-" * 95)
                            cid = input("\nClass ID to remove: ").strip().upper()

                            target = None
                            for cl in classes:
                                if cl["id"] == cid:
                                    target = cl

                            if target is None:
                                print("Class ID not found.")
                            else:
                                print("Note: the attendance records of this class will also be deleted.")
                                sure = input(f"Remove class {cid} ({target['section']} | {target['code']})? Type Y to confirm: ").strip().upper()
                                if sure == "Y":
                                    kept = []
                                    for r in attendance:
                                        if not (r["code"] == target["code"] and r["section"] == target["section"]):
                                            kept.append(r)
                                    deleted = len(attendance) - len(kept)
                                    attendance = kept
                                    classes.remove(target)
                                    print(f"Class {cid} removed.")
                                    if deleted > 0:
                                        print(f"{deleted} attendance record(s) of this class were also deleted.")
                                else:
                                    print("Removal cancelled.")
                        show_classes = True

                    # ---------- 8. BACK ----------
                    elif cm == "8":
                        mode = "main"

                    else:
                        print("Invalid choice.")

                    if show_classes:
                        # ----- TABLE: CLASSES (every section, its subjects and teachers) -----
                        if len(sections) == 0:
                            print("\nNo classes yet. Create a section first.")
                        else:
                            print("\n" + "=" * 105)
                            print(f"{'CLASSES':^105}")
                            print("=" * 105)
                            print(f"{'Class ID':<10}{'Section':<12}{'Subject Code':<16}{'Subject Name':<28}{'Credit Units':<14}{'Teacher'}")
                            print("-" * 105)
                            for sec_name in sections:
                                count = 0
                                for cl in classes:
                                    if cl["section"] == sec_name:
                                        count = count + 1
                                        subj_name = ""
                                        units = ""
                                        for s in subjects:
                                            if s["code"] == cl["code"]:
                                                subj_name = s["name"]
                                                units = s["units"]
                                        teacher_text = "(none yet)"
                                        for t in teachers:
                                            if t["id"] == cl["teacher"]:
                                                teacher_text = t["id"] + " - " + t["last"] + ", " + t["first"]
                                        print(f"{cl['id']:<10}{cl['section']:<12}{cl['code']:<16}{subj_name:<28}{units:<14}{teacher_text}")
                                if count == 0:
                                    print(f"{'-':<10}{sec_name:<12}(no subjects yet)")
                            print("-" * 105)

                    if show_section != "":
                        # ----- TABLE: STUDENTS IN THE CHOSEN SECTION -----
                        count = 0
                        for st in students:
                            if st["section"] == show_section:
                                count = count + 1

                        if count == 0:
                            print(f"\nNo students in section {show_section} yet.")
                        else:
                            title = "SECTION " + show_section + " - STUDENTS"
                            print("\n" + "=" * 48)
                            print(f"{title:^48}")
                            print("=" * 48)
                            print(f"{'Student ID':<12}{'Last Name':<18}{'First Name'}")
                            print("-" * 48)
                            for st in students:
                                if st["section"] == show_section:
                                    print(f"{st['id']:<12}{st['last']:<18}{st['first']}")
                            print("-" * 48)

                # ---------- SAVE DATA (after every admin action) ----------
                fh = open(DATA_FILE, "w")
                for s in subjects:
                    fh.write("SUBJECT|" + s["code"] + "|" + s["name"] + "|" + s["units"] + "\n")
                for t in teachers:
                    fh.write("TEACHER|" + t["id"] + "|" + t["password"] + "|" + t["last"] + "|" + t["first"] + "|" + t["address"] + "\n")
                for st in students:
                    fh.write("STUDENT|" + st["id"] + "|" + st["password"] + "|" + st["last"] + "|" + st["first"] + "|" + st["age"] + "|" + st["address"] + "|" + st["contact"] + "|" + st["section"] + "\n")
                for sec_name in sections:
                    fh.write("SECTION|" + sec_name + "\n")
                for cl in classes:
                    fh.write("CLASS|" + cl["id"] + "|" + cl["section"] + "|" + cl["code"] + "|" + cl["teacher"] + "\n")
                for r in attendance:
                    fh.write("ATTENDANCE|" + r["date"] + "|" + r["code"] + "|" + r["section"] + "|" + r["student_id"] + "|" + r["status"] + "\n")
                fh.close()
        else:
            print("Invalid admin username or password.")

    # =================================================================
    #                             TEACHER
    # =================================================================
    elif role == "2":
        t_id = input("Teacher ID: ").strip().upper()
        t_pass = input("Password: ").strip()

        me = None
        for t in teachers:
            if t["id"] == t_id and t["password"] == t_pass:
                me = t

        if me is None:
            print("Invalid teacher ID or password.")
        else:
            print(f"\nWelcome, {me['first']} {me['last']}!")
            teacher_on = True
            while teacher_on:
                # the classes assigned to this teacher (each one has a Class ID)
                my_classes = []
                for cl in classes:
                    if cl["teacher"] == me["id"]:
                        my_classes.append(cl)

                print("\n--- TEACHER MENU ---")
                print("[1] View My Classes")
                print("[2] View Students")
                print("[3] Check Attendance")
                print("[4] View Attendance")
                print("[5] Logout")
                tc = input("Choose: ").strip()

                # ---------- 1. VIEW MY CLASSES ----------
                if tc == "1":
                    # ----- TABLE: MY CLASSES (full details) -----
                    if len(my_classes) == 0:
                        print("You have no classes assigned yet.")
                    else:
                        print("\n" + "=" * 88)
                        print(f"{'MY CLASSES':^88}")
                        print("=" * 88)
                        print(f"{'Class ID':<10}{'Section':<12}{'Subject Code':<16}{'Subject Name':<28}{'Credit Units':<14}{'Students'}")
                        print("-" * 88)
                        for c in my_classes:
                            subj_name = ""
                            units = ""
                            for s in subjects:
                                if s["code"] == c["code"]:
                                    subj_name = s["name"]
                                    units = s["units"]
                            enrolled = 0
                            for st in students:
                                if st["section"] == c["section"]:
                                    enrolled = enrolled + 1
                            print(f"{c['id']:<10}{c['section']:<12}{c['code']:<16}{subj_name:<28}{units:<14}{enrolled}")
                        print("-" * 88)

                # ---------- 2. VIEW STUDENTS ----------
                elif tc == "2":
                    # ----- TABLE: MY CLASSES (only what is needed to pick one) -----
                    if len(my_classes) == 0:
                        print("You have no classes assigned yet.")
                    else:
                        print("\n" + "=" * 66)
                        print(f"{'MY CLASSES':^66}")
                        print("=" * 66)
                        print(f"{'Class ID':<10}{'Section':<12}{'Subject Code':<16}{'Subject Name'}")
                        print("-" * 66)
                        for c in my_classes:
                            subj_name = ""
                            for s in subjects:
                                if s["code"] == c["code"]:
                                    subj_name = s["name"]
                            print(f"{c['id']:<10}{c['section']:<12}{c['code']:<16}{subj_name}")
                        print("-" * 66)

                        cid = input("\nClass ID: ").strip().upper()
                        chosen = None
                        for c in my_classes:
                            if c["id"] == cid:
                                chosen = c

                        if chosen is None:
                            print("That Class ID is not one of your classes.")
                        else:
                            code = chosen["code"]
                            sec = chosen["section"]

                            # ----- TABLE: STUDENTS IN THIS CLASS -----
                            title = "STUDENTS - CLASS " + cid + " (" + sec + " | " + code + ")"
                            print("\n" + "=" * 66)
                            print(f"{title:^66}")
                            print("=" * 66)
                            print(f"{'Student ID':<14}{'Last Name':<18}{'First Name':<18}{'Latest Status'}")
                            print("-" * 66)
                            count = 0
                            for st in students:
                                if st["section"] == sec:
                                    count = count + 1
                                    status = "No record"
                                    latest = ""
                                    for r in attendance:
                                        if r["student_id"] == st["id"] and r["code"] == code and r["section"] == sec:
                                            if r["date"] >= latest:
                                                latest = r["date"]
                                                status = r["status"]
                                    print(f"{st['id']:<14}{st['last']:<18}{st['first']:<18}{status}")
                            print("-" * 66)

                            if count == 0:
                                print("No students are in this section yet.")
                            else:
                                print("(Latest Status = most recent attendance recorded)")

                # ---------- 3. CHECK ATTENDANCE ----------
                elif tc == "3":
                    # ----- TABLE: MY CLASSES (only what is needed to pick one) -----
                    if len(my_classes) == 0:
                        print("You have no classes assigned yet.")
                    else:
                        print("\n" + "=" * 66)
                        print(f"{'MY CLASSES':^66}")
                        print("=" * 66)
                        print(f"{'Class ID':<10}{'Section':<12}{'Subject Code':<16}{'Subject Name'}")
                        print("-" * 66)
                        for c in my_classes:
                            subj_name = ""
                            for s in subjects:
                                if s["code"] == c["code"]:
                                    subj_name = s["name"]
                            print(f"{c['id']:<10}{c['section']:<12}{c['code']:<16}{subj_name}")
                        print("-" * 66)

                        cid = input("\nClass ID: ").strip().upper()
                        chosen = None
                        for c in my_classes:
                            if c["id"] == cid:
                                chosen = c

                        if chosen is None:
                            print("That Class ID is not one of your classes.")
                        else:
                            code = chosen["code"]
                            sec = chosen["section"]
                            # The date is taken automatically from the computer's clock (today),
                            # so the teacher never types a date and a wrong date is impossible.
                            d = str(date.today())

                            class_students = []
                            for st in students:
                                if st["section"] == sec:
                                    class_students.append(st)

                            if len(class_students) == 0:
                                print("No students are in this section yet.")
                            else:
                                already_done = 0
                                for r in attendance:
                                    if r["date"] == d and r["code"] == code and r["section"] == sec:
                                        already_done = already_done + 1
                                if already_done > 0:
                                    print("\nNote: attendance for this class was already recorded today. Your entries will update it.")
                                print(f"\nChecking attendance: Class {cid} | {code} | {sec} | {d} (today)")
                                print("[P] Present   [A] Absent   [L] Late   [E] Excused\n")
                                for st in class_students:
                                    mark = ""
                                    while mark != "P" and mark != "A" and mark != "L" and mark != "E":
                                        mark = input(f"{st['id']} - {st['last']}, {st['first']}: ").strip().upper()
                                        if mark != "P" and mark != "A" and mark != "L" and mark != "E":
                                            print("Enter P, A, L or E only.")

                                    if mark == "P":
                                        status = "Present"
                                    elif mark == "A":
                                        status = "Absent"
                                    elif mark == "L":
                                        status = "Late"
                                    else:
                                        status = "Excused"

                                    updated = False
                                    for r in attendance:
                                        if r["date"] == d and r["code"] == code and r["section"] == sec and r["student_id"] == st["id"]:
                                            r["status"] = status
                                            updated = True
                                    if not updated:
                                        attendance.append({"date": d, "code": code, "section": sec,
                                                           "student_id": st["id"], "status": status})
                                print("\nAttendance saved.")

                # ---------- 4. VIEW ATTENDANCE ----------
                elif tc == "4":
                    # ----- TABLE: MY CLASSES (only what is needed to pick one) -----
                    if len(my_classes) == 0:
                        print("You have no classes assigned yet.")
                    else:
                        print("\n" + "=" * 66)
                        print(f"{'MY CLASSES':^66}")
                        print("=" * 66)
                        print(f"{'Class ID':<10}{'Section':<12}{'Subject Code':<16}{'Subject Name'}")
                        print("-" * 66)
                        for c in my_classes:
                            subj_name = ""
                            for s in subjects:
                                if s["code"] == c["code"]:
                                    subj_name = s["name"]
                            print(f"{c['id']:<10}{c['section']:<12}{c['code']:<16}{subj_name}")
                        print("-" * 66)

                        cid = input("\nClass ID: ").strip().upper()
                        chosen = None
                        for c in my_classes:
                            if c["id"] == cid:
                                chosen = c

                        if chosen is None:
                            print("That Class ID is not one of your classes.")
                        else:
                            code = chosen["code"]
                            sec = chosen["section"]
                            d = input("Date (YYYY-MM-DD) or press Enter for all dates: ").strip()

                            # ----- TABLE: ATTENDANCE RECORDS -----
                            title = "ATTENDANCE - CLASS " + cid + " (" + sec + " | " + code + ")"
                            print("\n" + "=" * 70)
                            print(f"{title:^70}")
                            print("=" * 70)
                            print(f"{'Date':<14}{'Student ID':<14}{'Name':<30}{'Status'}")
                            print("-" * 70)
                            count = 0
                            for r in attendance:
                                if r["code"] == code and r["section"] == sec and (d == "" or r["date"] == d):
                                    stu_name = ""
                                    for st in students:
                                        if st["id"] == r["student_id"]:
                                            stu_name = st["last"] + ", " + st["first"]
                                    print(f"{r['date']:<14}{r['student_id']:<14}{stu_name:<30}{r['status']}")
                                    count = count + 1
                            print("-" * 70)

                            if count == 0:
                                print("No attendance records found.")

                # ---------- 5. LOGOUT ----------
                elif tc == "5":
                    print("Teacher logged out.")
                    teacher_on = False

                else:
                    print("Invalid choice.")

                # ---------- SAVE DATA (after every teacher action) ----------
                fh = open(DATA_FILE, "w")
                for s in subjects:
                    fh.write("SUBJECT|" + s["code"] + "|" + s["name"] + "|" + s["units"] + "\n")
                for t in teachers:
                    fh.write("TEACHER|" + t["id"] + "|" + t["password"] + "|" + t["last"] + "|" + t["first"] + "|" + t["address"] + "\n")
                for st in students:
                    fh.write("STUDENT|" + st["id"] + "|" + st["password"] + "|" + st["last"] + "|" + st["first"] + "|" + st["age"] + "|" + st["address"] + "|" + st["contact"] + "|" + st["section"] + "\n")
                for sec_name in sections:
                    fh.write("SECTION|" + sec_name + "\n")
                for cl in classes:
                    fh.write("CLASS|" + cl["id"] + "|" + cl["section"] + "|" + cl["code"] + "|" + cl["teacher"] + "\n")
                for r in attendance:
                    fh.write("ATTENDANCE|" + r["date"] + "|" + r["code"] + "|" + r["section"] + "|" + r["student_id"] + "|" + r["status"] + "\n")
                fh.close()

    # =================================================================
    #                             STUDENT
    # =================================================================
    elif role == "3":
        s_id = input("Student ID: ").strip().upper()
        s_pass = input("Password: ").strip()

        me = None
        for st in students:
            if st["id"] == s_id and st["password"] == s_pass:
                me = st

        if me is None:
            print("Invalid student ID or password.")
        else:
            print(f"\nWelcome, {me['first']} {me['last']}!")
            student_on = True
            while student_on:
                # the classes (subjects) of this student's section
                my_subjects = []
                for cl in classes:
                    if cl["section"] == me["section"]:
                        my_subjects.append(cl)

                print("\n--- STUDENT MENU ---")
                print("[1] View Profile")
                print("[2] View Attendance by Subject")
                print("[3] Logout")
                sc = input("Choose: ").strip()

                # ---------- 1. VIEW PROFILE ----------
                if sc == "1":
                    print("\n" + "=" * 40)
                    print(f"{'MY PROFILE':^40}")
                    print("=" * 40)
                    print(f"Student ID : {me['id']}")
                    print(f"Name       : {me['first']} {me['last']}")
                    print(f"Age        : {me['age']}")
                    print(f"Address    : {me['address']}")
                    print(f"Contact No.: {me['contact']}")
                    if me["section"] == "":
                        print("Section    : (none yet)")
                    else:
                        print(f"Section    : {me['section']}")
                    print("=" * 40)
                    # ----- TABLE: MY SUBJECTS (full details) -----
                    if len(my_subjects) == 0:
                        print("You are not enrolled in any subject yet. (Ask the admin to add you to a section.)")
                    else:
                        print("\n" + "=" * 80)
                        print(f"{'MY SUBJECTS':^80}")
                        print("=" * 80)
                        print(f"{'Subject Code':<16}{'Subject Name':<30}{'Credit Units':<14}{'Teacher'}")
                        print("-" * 80)
                        for item in my_subjects:
                            subj_name = ""
                            units = ""
                            for s in subjects:
                                if s["code"] == item["code"]:
                                    subj_name = s["name"]
                                    units = s["units"]
                            teacher_text = "(none yet)"
                            for t in teachers:
                                if t["id"] == item["teacher"]:
                                    teacher_text = t["last"] + ", " + t["first"]
                            print(f"{item['code']:<16}{subj_name:<30}{units:<14}{teacher_text}")
                        print("-" * 80)

                # ---------- 2. VIEW ATTENDANCE BY SUBJECT ----------
                elif sc == "2":
                    # ----- TABLE: MY SUBJECTS (only the code and name are needed) -----
                    if len(my_subjects) == 0:
                        print("You are not enrolled in any subject yet. (Ask the admin to add you to a section.)")
                    else:
                        print("\n" + "=" * 46)
                        print(f"{'MY SUBJECTS':^46}")
                        print("=" * 46)
                        print(f"{'Subject Code':<16}{'Subject Name'}")
                        print("-" * 46)
                        for item in my_subjects:
                            subj_name = ""
                            for s in subjects:
                                if s["code"] == item["code"]:
                                    subj_name = s["name"]
                            print(f"{item['code']:<16}{subj_name}")
                        print("-" * 46)

                        code = input("\nEnter subject code: ").strip().upper()

                        enrolled = False
                        for item in my_subjects:
                            if item["code"] == code:
                                enrolled = True

                        if not enrolled:
                            print("You are not enrolled in that subject.")
                        else:
                            # ----- TABLE: MY ATTENDANCE IN THIS SUBJECT -----
                            title = "MY ATTENDANCE - " + code
                            print("\n" + "=" * 30)
                            print(f"{title:^30}")
                            print("=" * 30)
                            print(f"{'Date':<14}{'Status'}")
                            print("-" * 30)
                            total = 0
                            present = 0
                            absent = 0
                            late = 0
                            excused = 0
                            for r in attendance:
                                if r["student_id"] == me["id"] and r["code"] == code:
                                    print(f"{r['date']:<14}{r['status']}")
                                    total = total + 1
                                    if r["status"] == "Present":
                                        present = present + 1
                                    elif r["status"] == "Absent":
                                        absent = absent + 1
                                    elif r["status"] == "Late":
                                        late = late + 1
                                    else:
                                        excused = excused + 1
                            print("-" * 30)

                            if total == 0:
                                print("No attendance records yet.")
                            else:
                                rate = (present + late) / total * 100
                                print(f"Present: {present}  Absent: {absent}  Late: {late}  Excused: {excused}")
                                print(f"Total classes: {total}")
                                print(f"Attendance rate (Present + Late): {rate:.1f}%")

                # ---------- 3. LOGOUT ----------
                elif sc == "3":
                    print("Student logged out.")
                    student_on = False

                else:
                    print("Invalid choice.")

    # =================================================================
    #                              EXIT
    # =================================================================
    elif role == "4":
        running = False

    else:
        print("Invalid choice. Please enter 1-4.")

    # =================================================================
    #             SAVE DATA (after every session, and on Exit)
    # =================================================================
    fh = open(DATA_FILE, "w")
    for s in subjects:
        fh.write("SUBJECT|" + s["code"] + "|" + s["name"] + "|" + s["units"] + "\n")
    for t in teachers:
        fh.write("TEACHER|" + t["id"] + "|" + t["password"] + "|" + t["last"] + "|" + t["first"] + "|" + t["address"] + "\n")
    for st in students:
        fh.write("STUDENT|" + st["id"] + "|" + st["password"] + "|" + st["last"] + "|" + st["first"] + "|" + st["age"] + "|" + st["address"] + "|" + st["contact"] + "|" + st["section"] + "\n")
    for sec_name in sections:
        fh.write("SECTION|" + sec_name + "\n")
    for cl in classes:
        fh.write("CLASS|" + cl["id"] + "|" + cl["section"] + "|" + cl["code"] + "|" + cl["teacher"] + "\n")
    for r in attendance:
        fh.write("ATTENDANCE|" + r["date"] + "|" + r["code"] + "|" + r["section"] + "|" + r["student_id"] + "|" + r["status"] + "\n")
    fh.close()

    if role == "4":
        print("All data saved to attendance_records.txt.")
        print("Goodbye!")