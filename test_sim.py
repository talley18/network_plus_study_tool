# ============================================================
# 1. Imports & Global Constants
# ============================================================

import json
import random
import os

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
 #new 5/5/26

ACRONYM_FILE = "questions/acronyms.json"


# ============================================================
# 3. Loaders
#    - Question loader
#    - Acronym loader
# ============================================================

QUESTIONS_DIR = "questions"


def load_questions(filename):
    """Load questions from a JSON file inside /questions."""
    path = os.path.join(QUESTIONS_DIR, filename)
    with open(path, "r") as f:
        return json.load(f)
    

def load_all_questions():
    all_questions = {}
    for key, (name, filename) in DOMAINS.items():
        all_questions[name] = load_questions(filename)
    return all_questions

#new 

def load_acronyms():
    try:
        with open(ACRONYM_FILE, "r") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print("[ERROR] Acronym file not found.")
        return []
    
#end new 5/5/26

# debugger addtion 
# ⭐ Load ALL questions once at startup
all_questions = load_all_questions()

# ⭐ DEBUG: Print counts per domain
print("=== DEBUG: Questions per domain ===")
for domain, qlist in all_questions.items():
    print(domain, len(qlist))

# ⭐ DEBUG: Combined total
combined = []
for qlist in all_questions.values():
    combined.extend(qlist)

print("=== DEBUG: Total questions loaded ===", len(combined))

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

# stuff moved form here to sec4
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
                print("Correct!")
                correct_count += 1
            else:
                print(f"Incorrect. Correct answer: {q['answer']}")
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
        print(f"Correct answer: {q['answer']}\n")
        return False

    selected_choice = q["choices"][int(answer) - 1]

    if selected_choice == q["answer"]:
        print("✔ Correct!\n")
        return True
    else:
        print("✘ Incorrect.")
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
    
#New acronym_mode

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

        for i, choice in enumerate(item["choices"], start=1):
            print(f"{i}. {choice}")

        user_input = input("Your answer (1-4): ").strip()

        if not user_input.isdigit() or not (1 <= int(user_input) <= len(item["choices"])):
            print("Invalid input. Skipping question.")
            continue

        user_choice = item["choices"][int(user_input) - 1]

        if user_choice == item["answer"]:
            print("✔ Correct!")
        else:
            print(f"✘ Incorrect. Correct answer: {item['answer']}")

        print(f"Explanation: {item['explanation']}")

    print("\n====================================")
    print("Acronym Quiz Complete")
    print(f"Score: {score}/{total}")
    print("====================================")




#end new 5/5/26   



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
        num = int(90 * weight)

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
        print("Running a short 5-question exam for debugging.\n")
    else:
        print("\n=== NSTPT EXAM SIMULATION ===")
        print("90 questions, weighted by domain.")
        print("Type 'q' to quit early.\n")

    all_questions = load_all_questions()

    if test_mode:
        # Pull 5 random questions from ALL domains combined
        combined = []
        for domain_list in all_questions.values():
            combined.extend(domain_list)
        exam = random.sample(combined, min(5, len(combined)))
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

    if scaled_score >= 720:
        print("Status: PASS")
    else:
        print("Status: FAIL")

    print("\nReview missed questions? (y/n)")
    if input("> ").strip().lower() == "y":
        for q in missed:
            print("\n" + q["question"])
            print("Correct answer:", q["answer"])
            print("Explanation:", q["explanation"])

        


# ============================================================
# 7. Main Menu / Main Function
# ============================================================

def main():
    print("=== NPST ===")
    print("Network Pluse Study Tool")
    print("Type 'quit' at any time to exit.\n")

    while True:
        print("Main Menu:")
        print("1. Study Mode (by domain)")
        print("2. Full Exam Simulation")
        print("3. Test Mode (short exam)")
        print("4. Mastery Mode (30-question perfect run) ")
        print("5. Acronym Study Mode")

        choice = input("Select an option: ").strip().lower()

        if choice == "quit":
            print("Exiting NSTPT. Study strong.")
            break

        if choice == "1":
            study_mode()

        elif choice == "2":
            exam_simulation()

        elif choice == "3":     #test mode option
            exam_simulation(test_mode=True)

        elif choice == "4":
            mastery_mode(all_questions)
        #new
        elif choice == "5":
            acronym_mode()
        #end new 5/5/26

        else:
            print("Invalid choice.\n")

# ============================================================
# 7.5  Program Entry Point (ALWAYS LAST)
# ============================================================

if __name__ == "__main__":  
    main()