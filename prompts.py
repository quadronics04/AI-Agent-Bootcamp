def create_concept_prompt(topic: str) -> str:
    """Create a prompt for explaining a concept."""

    return f"""
You are a patient teacher helping a Grade XII student.

Explain the following concept:

{topic}

Structure your response as follows:

1. Simple definition
2. Step-by-step explanation
3. One real-life example
4. Important points to remember
5. Short summary

Use clear language and avoid unnecessary jargon.
""".strip()


def create_summary_prompt(text: str) -> str:
    """Create a prompt for summarising text."""

    return f"""
Summarise the following text for a Grade XII student.

Requirements:

- Preserve the original meaning
- Use simple English
- Present the main ideas in 4 to 6 bullet points
- Mention the most important conclusion
- Do not introduce unsupported information

Text:

{text}
""".strip()


def create_quiz_prompt(topic: str) -> str:
    """Create a prompt for generating a quiz."""

    return f"""
Create a Grade XII-level quiz on the following topic:

{topic}

Include:

1. Three multiple-choice questions
2. Four options for every multiple-choice question
3. Two short-answer questions
4. A separate answer key
5. A brief explanation for each answer

Keep the questions clear and educational.
""".strip()


def create_code_explanation_prompt(code: str) -> str:
    """Create a prompt for explaining Python code."""

    return f"""
You are teaching Python to a Grade XII student who knows basic programming.

Analyse the following Python code:

--- START OF CODE ---

{code}

--- END OF CODE ---

Explain:

1. What the program does
2. What each important section does
3. Any syntax or logical errors
4. Possible improvements
5. One example of the expected output

Do not make the explanation unnecessarily advanced.
""".strip()


def create_general_question_prompt(question: str) -> str:
    """Create a prompt for answering a general question."""

    return f"""
Answer the following question for a Grade XII student:

{question}

Requirements:

- Be accurate
- Use clear language
- Explain important terms
- Use an example where useful
- State clearly when information is uncertain
""".strip()


def create_study_plan_prompt(
    subject: str,
    days: int,
    hours_per_day: float
) -> str:
    """Create a prompt for generating a study plan."""

    return f"""
Create a practical study plan for a Grade XII student.

Subject: {subject}
Number of days available: {days}
Study time available per day: {hours_per_day} hours

Requirements:

1. Create a day-wise plan
2. Divide time between learning, practice and revision
3. Include short breaks
4. Include at least one revision session
5. Include a final self-test
6. Keep the workload realistic
7. Present the plan in a clear table
""".strip()