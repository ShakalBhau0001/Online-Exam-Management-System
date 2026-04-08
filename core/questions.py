import random
import copy

QUESTION_BANK = {
    "java": [
        {
            "question": "Java is a __________ language.",
            "options": ["Procedural", "Object-Oriented", "Functional", "Assembly"],
            "answer": 1,
        },
        {
            "question": "Which keyword creates an object?",
            "options": ["create", "object", "new", "make"],
            "answer": 2,
        },
        {
            "question": "Entry point of a Java program?",
            "options": ["start()", "main()", "run()", "init()"],
            "answer": 1,
        },
        {
            "question": "JVM stands for?",
            "options": [
                "Java Virtual Machine",
                "Java Verified Method",
                "Java Visual Mode",
                "Java Variable Manager",
            ],
            "answer": 0,
        },
        {
            "question": "Which is NOT a Java primitive type?",
            "options": ["int", "float", "String", "boolean"],
            "answer": 2,
        },
        {
            "question": "Which concept means hiding internal details?",
            "options": ["Inheritance", "Polymorphism", "Encapsulation", "Abstraction"],
            "answer": 2,
        },
        {
            "question": "Size of int in Java?",
            "options": ["16 bits", "32 bits", "64 bits", "8 bits"],
            "answer": 1,
        },
        {
            "question": "Superclass of all Java classes?",
            "options": ["Main", "System", "Object", "Base"],
            "answer": 2,
        },
        {
            "question": "Keyword to prevent inheritance?",
            "options": ["static", "private", "final", "abstract"],
            "answer": 2,
        },
        {
            "question": "OOP stands for?",
            "options": [
                "Object Oriented Programming",
                "Open Operational Protocol",
                "Online Output Processing",
                "Object Output Platform",
            ],
            "answer": 0,
        },
        {
            "question": "Used to handle exceptions?",
            "options": ["try-catch", "if-else", "switch", "for-loop"],
            "answer": 0,
        },
        {
            "question": "Default value of boolean in Java?",
            "options": ["true", "false", "0", "null"],
            "answer": 1,
        },
        {
            "question": "Keyword for inheritance?",
            "options": ["implements", "extends", "inherits", "super"],
            "answer": 1,
        },
        {
            "question": "'this' refers to?",
            "options": ["Parent class", "Current object", "Static method", "Interface"],
            "answer": 1,
        },
        {
            "question": "Collection with no duplicates?",
            "options": ["ArrayList", "LinkedList", "HashSet", "Vector"],
            "answer": 2,
        },
    ],
    "python": [
        {
            "question": "Python is which type of language?",
            "options": ["Compiled", "Interpreted", "Assembly", "Machine"],
            "answer": 1,
        },
        {
            "question": "Which keyword defines a function?",
            "options": ["function", "def", "fun", "define"],
            "answer": 1,
        },
        {
            "question": "Python list is?",
            "options": ["Immutable", "Mutable", "Fixed", "Static"],
            "answer": 1,
        },
        {
            "question": "Output of type(3.14)?",
            "options": ["int", "str", "float", "double"],
            "answer": 2,
        },
        {
            "question": "Which is used for comments?",
            "options": ["//", "/* */", "#", "--"],
            "answer": 2,
        },
        {
            "question": "Which data type is immutable?",
            "options": ["list", "dict", "tuple", "set"],
            "answer": 2,
        },
        {
            "question": "Keyword to import a module?",
            "options": ["include", "import", "require", "use"],
            "answer": 1,
        },
        {
            "question": "What does len([1,2,3]) return?",
            "options": ["2", "3", "4", "Error"],
            "answer": 1,
        },
        {
            "question": "Used to create a class?",
            "options": ["def", "class", "object", "type"],
            "answer": 1,
        },
        {
            "question": "Which is NOT a Python loop?",
            "options": ["for", "while", "do-while", "None of these"],
            "answer": 2,
        },
        {
            "question": "Python file extension?",
            "options": [".py", ".pt", ".pyt", ".python"],
            "answer": 0,
        },
        {
            "question": "Output of 10//3?",
            "options": ["3.33", "3", "4", "Error"],
            "answer": 1,
        },
        {
            "question": "Which creates a dictionary?",
            "options": ["[]", "()", "{}", "<>"],
            "answer": 2,
        },
        {
            "question": "None represents?",
            "options": ["0", "False", "Null value", "Empty string"],
            "answer": 2,
        },
        {
            "question": "What is PEP 8?",
            "options": ["Python version", "Style guide", "Package manager", "Debugger"],
            "answer": 1,
        },
    ],
    "dbms": [
        {
            "question": "DBMS stands for?",
            "options": [
                "Data Backup Management System",
                "Database Management System",
                "Data Binary Management System",
                "None",
            ],
            "answer": 1,
        },
        {
            "question": "SQL stands for?",
            "options": [
                "Structured Query Language",
                "Simple Query Language",
                "Standard Query Logic",
                "None",
            ],
            "answer": 0,
        },
        {
            "question": "Which is a DDL command?",
            "options": ["SELECT", "INSERT", "CREATE", "UPDATE"],
            "answer": 2,
        },
        {
            "question": "Primary key can be?",
            "options": ["NULL", "Duplicate", "Unique & Not Null", "Any value"],
            "answer": 2,
        },
        {
            "question": "Foreign key references?",
            "options": [
                "Same table",
                "Primary key of another table",
                "Any column",
                "Index",
            ],
            "answer": 1,
        },
        {
            "question": "Which JOIN returns all rows from both tables?",
            "options": ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL OUTER JOIN"],
            "answer": 3,
        },
        {
            "question": "Normalization is used to?",
            "options": [
                "Add redundancy",
                "Remove redundancy",
                "Speed up queries",
                "None",
            ],
            "answer": 1,
        },
        {
            "question": "ACID stands for?",
            "options": [
                "Atomicity Consistency Isolation Durability",
                "All Consistent Integrated Data",
                "None",
                "Async Concurrent Indexed Data",
            ],
            "answer": 0,
        },
        {
            "question": "Which command removes a table completely?",
            "options": ["DELETE", "TRUNCATE", "DROP", "REMOVE"],
            "answer": 2,
        },
        {
            "question": "Which is a NoSQL database?",
            "options": ["MySQL", "PostgreSQL", "MongoDB", "Oracle"],
            "answer": 2,
        },
        {
            "question": "GROUP BY is used with?",
            "options": ["WHERE", "HAVING", "ORDER BY", "JOIN"],
            "answer": 1,
        },
        {
            "question": "Which is a DML command?",
            "options": ["CREATE", "DROP", "INSERT", "ALTER"],
            "answer": 2,
        },
        {
            "question": "View in DBMS is?",
            "options": ["Physical table", "Virtual table", "Index", "Trigger"],
            "answer": 1,
        },
        {
            "question": "ER stands for?",
            "options": ["Entity Relation", "Error Report", "Execution Result", "None"],
            "answer": 0,
        },
        {
            "question": "Candidate key is?",
            "options": [
                "Any key",
                "Key that can be primary key",
                "Foreign key",
                "None",
            ],
            "answer": 1,
        },
    ],
}

SUBJECTS = {
    "Java Programming": "java",
    "Python Basics": "python",
    "DBMS": "dbms",
}

TOTAL_QUESTIONS = 10
TIMER_SECONDS = 600  # 10 minutes
PASS_PERCENT = 0.6  # 60%


def get_shuffled_questions(subject_key: str) -> list:
    qs = copy.deepcopy(QUESTION_BANK.get(subject_key, QUESTION_BANK["java"]))
    random.shuffle(qs)
    qs = qs[:TOTAL_QUESTIONS]
    for q in qs:
        combined = list(zip(q["options"], range(4)))
        random.shuffle(combined)
        opts, idxs = zip(*combined)
        q["options"] = list(opts)
        q["answer"] = list(idxs).index(q["answer"])
    return qs
