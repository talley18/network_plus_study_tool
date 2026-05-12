# ============================================================
# 1. Imports & Global Constants
# ============================================================

import json
import random
import os
import sys
import time


def resource_path(relative_path):
    # When running as an EXE, PyInstaller sets sys._MEIPASS
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    # When running normally (python test_sim.py)
    return os.path.join(os.path.abspath("."), relative_path)

def type_out(text, speed=0.01):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

#New
def glow_text(text):
    # Layered ANSI glow effect
    bright = "\033[92m"      # bright green
    dim = "\033[32m"         # dimmer green
    bold = "\033[1m"
    reset = "\033[0m"

    # Outer glow (dim)
    line1 = dim + text + reset
    # Inner glow (bright + bold)
    line2 = bold + bright + text + reset

    return line1 + "\n" + line2

def crt_flicker(text, speed=0.008):
    for char in text:
        sys.stdout.write("\033[92m" + char + "\033[0m")
        sys.stdout.flush()
        time.sleep(speed + random.uniform(0, 0.003))
    print()



# ===== Color Codes =====
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"

# ===== Pre-Styled Text =====
CORRECT_TEXT = f"{GREEN}✔ Correct!{RESET}"
INCORRECT_TEXT = f"{RED}✘ Incorrect.{RESET}"

PASS_TEXT = f"{GREEN}✔ PASS{RESET}"
FAIL_TEXT = f"{RED}✘ FAIL{RESET}"

INFO_TEXT = f"{CYAN}ℹ Info:{RESET}"
WARNING_TEXT = f"{YELLOW}⚠ Warning:{RESET}"

#New 
def title_block():
    print("╔══════════════════════════════════════════════╗")
    print("║        NETWORK+ STUDY TERMINAL               ║")
    print("╚══════════════════════════════════════════════╝")
    print()



# ============================================================
# 2. Data Structures & Mappings
#    - Domain mapping
#    - Acronym dictionary (loaded from JSON)
# ============================================================

DOMAINS = {
    "1": ("Networking Fundamentals", "fundamentals.json"),
    "2": ("Network Implementations", "implementations.json"),
    "3": ("Network Operations", "operations.json"),
    "4": ("Network Security", "security.json"),
    "5": ("Network Troubleshooting", "troubleshooting.json"),
}

    
EXAM_WEIGHTS = {
    "Networking Fundamentals": 0.24,
    "Network Implementations": 0.19,
    "Network Operations": 0.16,
    "Network Security": 0.19,
    "Network Troubleshooting": 0.22
}
 

# ============================================================
# 3. Loaders
#    - Question loader
#    - Acronym loader
#new loader added 5/10/20
# ============================================================

#chaged 5/11/26
ACRONYM_FILE = "acronyms.json"

QUESTIONS_DIR = "questions"

def load_questions(filename):
    """Load questions from a JSON file inside /questions."""
    relative = os.path.join(QUESTIONS_DIR, filename)
    path = resource_path(relative)
    with open(path, "r") as f:
        return json.load(f)

def load_all_questions():
    all_questions = {}
    for key, (name, filename) in DOMAINS.items():
        all_questions[name] = load_questions(filename)
    return all_questions

def load_acronyms():
    try:
        path = resource_path(os.path.join(QUESTIONS_DIR, ACRONYM_FILE))
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("[ERROR] Acronym file not found.")
        return []
    
###New loader added acronym Dir 5/11/26###

def load_acronym_reference():
    relative = os.path.join(QUESTIONS_DIR, "list_acronymsAZ.json")
    path = resource_path(relative)
    with open(path, "r") as f:
        return json.load(f)



# debugger addtion 
# ⭐ Load ALL questions once at startup
#all_questions = load_all_questions()

# ⭐ DEBUG: Print counts per domain
##for domain, qlist in all_questions.items():
    #print(domain, len(qlist))

# ⭐ DEBUG: Combined total
#combined = []
#for qlist in all_questions.values():
    #combined.extend(qlist)

#print("=== DEBUG: Total questions loaded ===", len(combined))

# ============================================================
# 4. Utility Functions
#    - Randomizers
#    - Validators
#    - Subnetting helpers (future)
# ============================================================



def pick_random_questions(questions, max_count=10):
    num_to_ask = min(max_count, len(questions))
    return random.sample(questions, num_to_ask)

#new
def randomize_acronyms(acronym_list):
    random.shuffle(acronym_list)
    return acronym_list
#end new 






# ============================================================
# 5. Study Modes
#    - Study Mode
#    - Mastery Mode
#    - Subnetting Mode (future)
# ============================================================

def study_mode():
    print("\n=== NSTPT STUDY MODE ===")
    print("Choose a domain to practice:\n")

    for key, (name, _) in DOMAINS.items():
        print(f"{key}. {name}")
    print("Q. Return to main menu\n")

    choice = input("Select a domain: ").strip().lower()

    if choice == "q":
        return

    if choice not in DOMAINS:
        print("Invalid choice.\n")
        return

    domain_name, filename = DOMAINS[choice]
    questions = load_questions(filename)

    if not questions:
        print("No questions found for this domain.\n")
        return

    print(f"\n--- {domain_name} ---")


    session_questions = pick_random_questions(questions)


    correct_count = 0

    for q in session_questions:
        print("\n" + q["question"])
        for i, option in enumerate(q["choices"], 1):
            print(f"{i}. {option}")

        answer = input("Your answer (number or 'q' to quit): ").strip().lower()

        if answer == "q":
            break

        if not answer.isdigit():
            print("Please enter a number.")
            continue

        idx = int(answer) - 1

        if 0 <= idx < len(q["choices"]):
            chosen = q["choices"][idx]
            if chosen.lower() == q["answer"].lower():
                print (CORRECT_TEXT)
                correct_count += 1
            else:
                print(f"{INCORRECT_TEXT} correct answer: {q['answer']}")
                print("Explanation:", q["explanation"])
        else:
            print("Invalid choice.")

    print(f"\nSession complete. Correct: {correct_count}/{len(session_questions)}\n")

# ⭐ INSERT THIS FUNCTION HERE ⭐
def ask_question_mastery(q):
    print(q["question"])
    for i, choice in enumerate(q["choices"], 1):
        print(f"{i}. {choice}")

    answer = input("Your answer(or q to quit): ").strip().lower()

    if answer == "q":
        return "quit"

    if not answer.isdigit() or int(answer) not in range(1, len(q["choices"]) + 1):
        print("Invalid input. Marked as incorrect.\n")
        print(f"{CORRECT_TEXT}  answer: {q['answer']}\n")
        return False

    selected_choice = q["choices"][int(answer) - 1]

    if selected_choice == q["answer"]:
        print(f"{CORRECT_TEXT}\n")
        return True
    else:
        print(INCORRECT_TEXT)
        print(f"Correct answer: {q['answer']}\n")
        return False

# Mastery Mode 


def mastery_mode(all_questions):
    print("\n=== NSTPT MASTERY MODE ===")
    print("30 questions. Immediate feedback. Repeat until perfect.\n")

    # Flatten all domain lists into one big list
    combined = []
    for domain_list in all_questions.values():
        combined.extend(domain_list)

    # Pick 30 random questions
    session = random.sample(combined, min(30, len(combined)))

    missed = []

    # First pass
    for q in session:
        result = ask_question_mastery(q)

        if result == "quit":
            print("\nExiting Mastery Mode early.\n")
            return

        if not result:
            missed.append(q)

    # Retry loop
    round_num = 2
    while missed:
        print(f"\n--- Round {round_num}: Retrying {len(missed)} missed questions ---\n")
        retry = missed
        missed = []

        for q in retry:
            result = ask_question_mastery(q)

            if result == "quit":
                print("\nExiting Mastery Mode early.\n")
                return

            if not result:
                missed.append(q)

        round_num += 1

    print("\n🔥 Mastery Achieved! You answered all 30 questions correctly! 🔥\n")
    
#New acronym_mode 5/10/26
def acronym_mode():
    acronyms = load_acronyms()
    if not acronyms:
        print("No acronym data found.")
        return

    score = 0
    total = len(acronyms)

    random.shuffle(acronyms)

    for item in acronyms:
        print("\n====================================")
        print(item["question"])

        # Make a shuffled copy of the choices
        shuffled_choices = item["choices"][:]
        random.shuffle(shuffled_choices)

        # Display shuffled choices
        for i, choice in enumerate(shuffled_choices, start=1):
            print(f"{i}. {choice}")

        user_input = input("Your answer (or 'q' to quit): ").strip().lower()

        if user_input == 'q':
            print("Exiting Acronym Mode...")
            break

        if not user_input.isdigit() or not (1 <= int(user_input) <= len(shuffled_choices)):
            print("Invalid input. Skipping question.")
            continue

        # Get the selected answer from the SHUFFLED list
        user_choice = shuffled_choices[int(user_input) - 1]

        # Check correctness
        if user_choice == item["answer"]:
            print(GREEN + CORRECT_TEXT + RESET)
            score += 1
        else:
            print(RED + f"✘ Incorrect. Correct answer: {item['answer']}" + RESET)

        print(f"Explanation: {item['explanation']}")

    print("\n====================================")
    print("Acronym Quiz Complete")
    print(f"Score: {score}/{total}")
    print("====================================")

 
##new mode acronym listings 5/11/26

def acronym_directory():
    acronyms = load_acronym_reference()

    if not acronyms:
        print("No acronym data found.")
        return

    print(GREEN + "\n===========================================")
    print("        ACRONYM DIRECTORY (A–Z)")
    print("===========================================\n" + RESET)

    for item in sorted(acronyms, key=lambda x: x["acronym"]):
        line = f"{item['acronym']} : {item['definition']}"
        type_out(GREEN + line + RESET, speed=0.002)

    print(GREEN + "\n===========================================\n" + RESET)

# ============================================================
# 6. Exam System
#    - Exam generator
#    - Exam simulation loop
# ============================================================


def generate_exam(all_questions):
    exam_questions = []

    for domain, weight in EXAM_WEIGHTS.items():
        domain_questions = all_questions[domain]

        # Number of questions for this domain
        num = round(90 * weight)

        # If your pool is small, sample with min()
        selected = random.sample(domain_questions, min(num, len(domain_questions)))

        exam_questions.extend(selected)

    # Shuffle the final exam
    random.shuffle(exam_questions)

    return exam_questions


#Exam simulatoin loop 

def exam_simulation(test_mode=False):

    if test_mode:
        print("\n=== NSTPT TEST MODE ===")
        print("Running a short 10-question exam for debugging.\n")
    else:
        print("\n=== NSTPT EXAM SIMULATION ===")
        print("90 questions, weighted by domain.")
        print("Type 'q' to quit early.\n")

    all_questions = load_all_questions()

    if test_mode:
        # Pull 10 random questions from ALL domains combined
        combined = []
        for domain_list in all_questions.values():
            combined.extend(domain_list)
        exam = random.sample(combined, min(10, len(combined)))
    else:
        exam = generate_exam(all_questions)

    score = 0
    missed = []

    for i, q in enumerate(exam, 1):
        print(f"\nQuestion {i}/{len(exam)}")
        print(q["question"])

        for idx, choice in enumerate(q["choices"], 1):
            print(f"{idx}. {choice}")

        answer = input("Your answer: ").strip().lower()

        if answer == "q":
            break

        if not answer.isdigit():
            print("Invalid input.")
            continue

        index = int(answer) - 1

        if 0 <= index < len(q["choices"]):
            chosen = q["choices"][index]
            if chosen.lower() == q["answer"].lower():
                score += 1
            else:
                missed.append(q)
        else:
            print("Invalid choice.")


    # Score conversion (CompTIA style)




    total_questions = len(exam)
    scaled_score = int(100 + (score / total_questions) * 800)

    print("\n=== EXAM COMPLETE ===")
    print(f"Correct: {score}/90")
    print(f"Score: {scaled_score} (Pass: 720)\n")

    #### pasth test test ## scaled_score = 800   # force a passing score for testing


# new 5/9/26 start Kiwi passed 

    if scaled_score >= 720:
        print("\n🎉🎉🎉  YOU PASSED!  🎉🎉🎉\n")
        print(r"""
 /\_/\  
( o.o )   < Kiwi approves!
 > ^ <
    """)
        print("Welcome to IT.")
        print("Now go fix the printer down in HR.\n")

    else:
            print("\nYou'll get it next time — review your missed questions and try again.\n")


    print("\nReview missed questions? (y/n)")
    if input("> ").strip().lower() == "y":
        for q in missed:
            print("\n" + q["question"])
            print("Correct answer:", q["answer"])
            print("Explanation:", q["explanation"])

#end new 5/9/26 Kiwi passed             

        


# ============================================================
# 7. Main Menu / Main Function
# ============================================================
##new Minu 5/11/26##
def main():
    title_block()
    print("Network Pluse Study Tool")
    print("Type 'quit' at any time to exit.\n")

    while True:
        print("Main Menu:")
        print("1. Study Mode (by domain)")
        print("2. Mini Test (10 questions)")
        print("3. Mastery Mode (30-question perfect run)") 
        print("4. Full Exam Simulation 90 Questions")
        print("5. Acronym Study Mode")
        print("6. In Development Acronym listings")
        print("7. In Development")
        print("8. In Development Sotry Mode (Escape the OSI model)")
        print("9.In Development Subnet Study “Your Doom is below the net”")


        choice = input("Select an option: ").strip().lower()

        if choice == "quit":
            print("Exiting NSTPT. Study strong.")
            break

        elif choice == "1":
            study_mode()

        elif choice == "4":
            exam_simulation()

        elif choice == "2":     #test mode option
            exam_simulation(test_mode=True)

        elif choice == "3":
            all_questions = load_all_questions()
            mastery_mode(all_questions)

        elif choice == "5":
            acronym_mode()

        elif choice == "6":
            acronym_directory()

        else:
            print("Invalid choice.\n")

# ============================================================
# 7.5  Program Entry Point (ALWAYS LAST)
# ============================================================

if __name__ == "__main__":  
    main()