import re

def parse_resume_text(text):
    parsed = {}
    lines = text.split('\n')

    parsed['Name'] = lines[0].strip() if lines else 'Not found'

    email_match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    parsed['Email'] = email_match.group() if email_match else 'Not found'

    phone_match = re.search(r'(\+?01[0-2,5]\d{8})', text)
    parsed['Phone'] = phone_match.group() if phone_match else 'Not found'

    skill_keywords = ['Python', 'JavaScript', 'React', 'Node.js', 'SQL', 'HTML', 'CSS', 'AI', 'Machine Learning']
    parsed['Skills'] = [s for s in skill_keywords if s.lower() in text.lower()] or ['Not found']

    education_words = ['Bachelor', 'Master', 'University', 'Degree']
    parsed['Education'] = [line for line in lines if any(w in line for w in education_words)] or ['Not found']

    exp_words = ['experience', 'worked', 'intern', 'responsible', 'position']
    parsed['Experience'] = [line for line in lines if any(w in line.lower() for w in exp_words)] or ['Not found']

    langs = ['Arabic', 'English', 'French', 'German', 'Spanish']
    parsed['Languages'] = [line for line in lines if any(l in line for l in langs)] or ['Not found']

    return parsed
