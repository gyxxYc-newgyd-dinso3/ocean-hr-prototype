"""Transparent self-report questionnaire and structured interview prompts."""
DIMENSIONS = {
    'Openness': [
        'I enjoy exploring new approaches to unfamiliar problems.',
        'I actively seek out ideas that challenge my usual way of thinking.',
        'I am comfortable learning tools or methods that are new to me.',
    ],
    'Conscientiousness': [
        'I break complex tasks into plans and track my progress.',
        'I check important details before submitting work.',
        'I reliably follow through on commitments and deadlines.',
    ],
    'Extraversion': [
        'I feel comfortable speaking up in a group discussion.',
        'I often initiate conversations with colleagues or stakeholders.',
        'I gain energy from collaborating with other people.',
    ],
    'Agreeableness': [
        'I try to understand a colleague’s perspective during disagreement.',
        'I offer help when teammates are under pressure.',
        'I communicate respectfully even when I disagree.',
    ],
    'Emotional Stability (inverse of Neuroticism)': [
        'I can usually regain focus after a stressful work situation.',
        'I can receive constructive feedback without becoming overwhelmed.',
        'When plans change unexpectedly, I can adapt and decide on next steps.',
    ],
}

INTERVIEW_QUESTIONS = {
    'Openness': [
        'Tell me about a time you had to learn an unfamiliar tool or approach. How did you proceed?',
        'Describe a situation where you proposed a different solution. What evidence supported it?',
        'How do you decide when to experiment and when to use an established process?',
    ],
    'Conscientiousness': [
        'Describe a project with competing deadlines. How did you plan and track the work?',
        'Tell me about a time you caught an important error. What checks helped you find it?',
        'What do you do when you realise a commitment may not be met on time?',
    ],
    'Extraversion': [
        'Describe how you communicate a complex idea to a group with mixed backgrounds.',
        'Tell me about a time you needed input from people who were difficult to reach.',
        'How do you contribute when a team discussion is dominated by a few voices?',
    ],
    'Agreeableness': [
        'Tell me about a professional disagreement and how you worked toward a resolution.',
        'Describe a time you helped a teammate while managing your own priorities.',
        'How would you respond if a colleague challenged your work in a meeting?',
    ],
    'Emotional Stability (inverse of Neuroticism)': [
        'Tell me about a high-pressure work situation. What actions helped you respond effectively?',
        'Describe a time you received difficult feedback. What did you do next?',
        'When a project changes suddenly, how do you reassess priorities?',
    ],
}
