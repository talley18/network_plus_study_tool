
Read me for Networking study tool program. 
Network Study Tool (NTS)

A small learning project created to help users study for the CompTIA Network+ (N10-008) exam. NPST is a terminal-based study tool with multiple learning modes, a full test simulator, and early groundwork for gamification and story-driven practice.
Full Test Simulator
•	Loads questions from XML files
•	Randomized question order
•	Correct/incorrect scoring
•	Designed to mimic the feel of a real Network+ exam
•	Supports expanding question banks through simple XML editing
Study Modes
•	Acronym lookup
•	OSI layer reference
•	Topic focused question practice
•	Quick review utilities for last minute studying
Early Gamification Elements
Work in progress.
•	XP system prototype
•	Terminal style “retro” UI
•	Plans for achievements, unlockables, and progression
Planned Story Mode
Story Mode is planned as a future expansion where users explore a fictional world inspired by the OSI model. Each area would reinforce real networking concepts through guided exploration and interactive challenges.
•	Layer themed areas
•	NPCs representing protocols
•	Puzzles based on real networking concepts
•	A fun way to reinforce exam material
XML Question Format
The test simulator uses a simple XML structure to define each question and its supporting information:
•	Question text
•	Correct answer
•	Wrong answers
•	Category tags
•	Optional metadata for future gamification
This structure makes it easy to expand the question bank, organize questions by topic, or build custom study modules.
How to Run
1.	Install Python 3.10+
2.	Clone the repository
3.	Run the simulator:
Example command: python main.py
Contributions
This is an amateur learning project, and contributions are welcome. You can help by suggesting improvements, opening issues, forking the repository, or submitting pull requests.
Contact
For questions about the XML format or test simulator logic, review the questions/ folder or reach out directly.
