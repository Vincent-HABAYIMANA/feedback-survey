"""Per-category form templates the model recommends after classification.

Each template provides two title patterns:
  - `title_with_topic`: used when we extract a meaningful topic from the
    user's input (e.g. "Restaurant", "Mobile App").
  - `title_default`: used when the extracted topic is empty or generic.

Plus a description and a list of recommended fields.
"""

TEMPLATES = {
    "customer-satisfaction": {
        "title_with_topic": "{topic_title} — customer satisfaction survey",
        "title_default": "Customer satisfaction survey",
        "description": (
            "Thank you for being a customer. Your honest feedback helps us "
            "improve. This short survey takes about 2 minutes."
        ),
        "fields": [
            {"field_type": "short_text", "label": "Your name", "required": False},
            {"field_type": "email", "label": "Email address", "required": False,
             "help_text": "We'll only use this if you ask us to follow up."},
            {"field_type": "rating", "label": "Overall, how satisfied are you?",
             "required": True, "config": {"max": 5}},
            {"field_type": "multiple_choice", "label": "How likely are you to recommend us?",
             "required": True,
             "config": {"options": ["Very likely", "Somewhat likely", "Neutral",
                                     "Somewhat unlikely", "Very unlikely"]}},
            {"field_type": "checkboxes", "label": "What did you like most?",
             "required": False,
             "config": {"options": ["Quality", "Speed", "Price",
                                     "Customer service", "Ease of use"]}},
            {"field_type": "long_text", "label": "What could we do better?",
             "required": False,
             "placeholder": "Anything specific you'd like to share..."},
            {"field_type": "multiple_choice", "label": "May we contact you about your feedback?",
             "required": False, "config": {"options": ["Yes", "No"]}},
        ],
    },
    "product-feedback": {
        "title_with_topic": "{topic_title} — product feedback",
        "title_default": "Product feedback",
        "description": (
            "Help shape the future of our product. Your input goes directly "
            "to the team building it."
        ),
        "fields": [
            {"field_type": "short_text", "label": "Your name", "required": False},
            {"field_type": "email", "label": "Email", "required": False},
            {"field_type": "rating", "label": "How would you rate the product overall?",
             "required": True, "config": {"max": 5}},
            {"field_type": "multiple_choice", "label": "How often do you use it?",
             "required": True,
             "config": {"options": ["Daily", "A few times a week", "Weekly",
                                     "Monthly", "Less often"]}},
            {"field_type": "checkboxes", "label": "Which parts do you use most?",
             "required": False,
             "config": {"options": ["Core feature A", "Core feature B",
                                     "Integrations", "Reports", "Mobile"]}},
            {"field_type": "long_text", "label": "What feature is missing that you'd love to see?",
             "required": False},
            {"field_type": "long_text", "label": "Any bugs or rough edges?", "required": False},
        ],
    },
    "event-feedback": {
        "title_with_topic": "{topic_title} — attendee feedback",
        "title_default": "Event feedback",
        "description": (
            "Thanks for joining us. We'd love to know how it went and what "
            "we can improve for next time."
        ),
        "fields": [
            {"field_type": "short_text", "label": "Your name", "required": False},
            {"field_type": "email", "label": "Email", "required": False},
            {"field_type": "rating", "label": "How would you rate the event overall?",
             "required": True, "config": {"max": 5}},
            {"field_type": "rating", "label": "Quality of speakers / content",
             "required": True, "config": {"max": 5}},
            {"field_type": "rating", "label": "Venue and organisation",
             "required": True, "config": {"max": 5}},
            {"field_type": "checkboxes", "label": "What did you enjoy?",
             "required": False,
             "config": {"options": ["The talks", "Networking", "Workshops",
                                     "Food & drinks", "Venue"]}},
            {"field_type": "long_text", "label": "What could we improve next time?",
             "required": False},
            {"field_type": "multiple_choice", "label": "Would you attend again?",
             "required": False, "config": {"options": ["Yes", "Maybe", "No"]}},
        ],
    },
    "course-feedback": {
        "title_with_topic": "{topic_title} — course evaluation",
        "title_default": "Course evaluation",
        "description": (
            "Your honest feedback helps us improve the course for future "
            "students. All answers are confidential."
        ),
        "fields": [
            {"field_type": "short_text", "label": "Student name (optional)", "required": False},
            {"field_type": "rating", "label": "Overall course rating",
             "required": True, "config": {"max": 5}},
            {"field_type": "rating", "label": "Clarity of the instructor",
             "required": True, "config": {"max": 5}},
            {"field_type": "rating", "label": "Pace of the course",
             "required": True, "config": {"max": 5}},
            {"field_type": "multiple_choice", "label": "How relevant was the content to your goals?",
             "required": True,
             "config": {"options": ["Very relevant", "Somewhat relevant",
                                     "Neutral", "Not very relevant", "Not relevant at all"]}},
            {"field_type": "long_text", "label": "What did you learn that was most useful?",
             "required": False},
            {"field_type": "long_text", "label": "What would make this course better?",
             "required": False},
        ],
    },
    "employee-feedback": {
        "title_with_topic": "{topic_title} — employee feedback",
        "title_default": "Employee engagement survey",
        "description": (
            "We want every team member to be heard. This survey is "
            "confidential and your responses help leadership understand how "
            "we can do better."
        ),
        "fields": [
            {"field_type": "rating", "label": "How happy are you at work right now?",
             "required": True, "config": {"max": 5}},
            {"field_type": "rating", "label": "I feel my work is valued",
             "required": True, "config": {"max": 5}},
            {"field_type": "rating", "label": "I have the resources I need to do my job well",
             "required": True, "config": {"max": 5}},
            {"field_type": "multiple_choice", "label": "How likely are you to recommend us as a place to work?",
             "required": True,
             "config": {"options": ["Very likely", "Likely", "Neutral",
                                     "Unlikely", "Very unlikely"]}},
            {"field_type": "long_text", "label": "What is working well?", "required": False},
            {"field_type": "long_text", "label": "What should we improve?", "required": False},
        ],
    },
    "contact": {
        "title_with_topic": "Contact us — {topic_title}",
        "title_default": "Contact us",
        "description": (
            "Send us a message and we'll get back to you as soon as we can."
        ),
        "fields": [
            {"field_type": "short_text", "label": "Your name", "required": True},
            {"field_type": "email", "label": "Email", "required": True},
            {"field_type": "phone", "label": "Phone (optional)", "required": False},
            {"field_type": "dropdown", "label": "What is this about?",
             "required": True,
             "config": {"options": ["General inquiry", "Sales", "Support",
                                     "Partnership", "Other"]}},
            {"field_type": "long_text", "label": "Your message", "required": True,
             "placeholder": "Tell us how we can help..."},
        ],
    },
    "rsvp": {
        "title_with_topic": "RSVP — {topic_title}",
        "title_default": "Event RSVP",
        "description": (
            "Please let us know whether you can make it so we can plan "
            "ahead. Submit by the RSVP deadline."
        ),
        "fields": [
            {"field_type": "short_text", "label": "Your full name", "required": True},
            {"field_type": "email", "label": "Email", "required": True},
            {"field_type": "phone", "label": "Phone (optional)", "required": False},
            {"field_type": "multiple_choice", "label": "Will you attend?",
             "required": True, "config": {"options": ["Yes", "No", "Maybe"]}},
            {"field_type": "number", "label": "Number of guests (including yourself)",
             "required": True},
            {"field_type": "dropdown", "label": "Dietary requirements",
             "required": False,
             "config": {"options": ["None", "Vegetarian", "Vegan",
                                     "Gluten-free", "Other (note below)"]}},
            {"field_type": "long_text", "label": "Anything we should know?",
             "required": False},
        ],
    },
    "bug-report": {
        "title_with_topic": "Report a problem — {topic_title}",
        "title_default": "Report a problem",
        "description": (
            "Help us fix it. Please describe what happened and how to "
            "reproduce it. Screenshots are very useful."
        ),
        "fields": [
            {"field_type": "short_text", "label": "Your name", "required": False},
            {"field_type": "email", "label": "Your email (so we can follow up)",
             "required": True},
            {"field_type": "short_text", "label": "What were you trying to do?",
             "required": True},
            {"field_type": "long_text", "label": "What happened instead?",
             "required": True},
            {"field_type": "long_text", "label": "Steps to reproduce",
             "required": False,
             "placeholder": "1. Go to ...\n2. Click ...\n3. See ..."},
            {"field_type": "dropdown", "label": "How severe is this?",
             "required": True,
             "config": {"options": ["Blocks me completely", "Major problem",
                                     "Minor problem", "Cosmetic"]}},
            {"field_type": "short_text", "label": "Browser or device",
             "required": False},
            {"field_type": "file", "label": "Screenshot or attachment",
             "required": False},
        ],
    },
}


CATEGORY_LABELS = {
    "customer-satisfaction": "Customer satisfaction",
    "product-feedback": "Product feedback",
    "event-feedback": "Event feedback",
    "course-feedback": "Course / training evaluation",
    "employee-feedback": "Employee engagement",
    "contact": "Contact form",
    "rsvp": "RSVP / event registration",
    "bug-report": "Bug report / support ticket",
}


# Words to strip when guessing the topic noun from the user's input.
# Includes generic English stop words AND category-related noise so the
# extracted topic is a clean noun phrase like "Mobile App" or "Restaurant".
STOP_WORDS = {
    # generic
    "a", "an", "the", "for", "of", "to", "about", "with", "from", "and",
    "or", "our", "your", "my", "their", "we", "i", "you", "us", "is",
    "are", "was", "were", "be", "been", "being", "do", "does", "did",
    "have", "has", "had", "this", "that", "these", "those", "some",
    "any", "all", "via", "into", "out", "in", "on", "at", "by", "as",
    "after", "before", "during", "post", "pre", "would", "could",
    "should", "will", "want", "need", "ask", "tell", "please", "how",
    "what", "who", "when", "where", "why", "very", "more", "most",
    "less", "many", "much", "new", "old",

    # form / category vocabulary
    "form", "survey", "feedback", "evaluation", "report", "review",
    "rate", "rating", "ratings", "questionnaire", "poll",
    "satisfaction", "happiness", "engagement",
    "event", "events", "conference", "meetup", "hackathon", "webinar",
    "course", "courses", "class", "classes", "training", "lecture",
    "bug", "bugs", "issue", "issues", "problem", "problems", "ticket",
    "rsvp", "registration", "register", "signup", "sign-up", "sign",
    "contact", "inquiry", "inquiries", "lead", "demo", "callback",
    "newsletter", "waitlist", "interest",
    "product", "products", "service", "services", "feature", "features",
    "customer", "customers", "client", "clients", "user", "users",
    "people", "guest", "guests", "attendee", "attendees",
    "employee", "employees", "staff", "team", "manager", "managers",
    "student", "students", "teacher", "teachers", "instructor",
    "happy", "honest", "professional",
    "next", "last", "first", "second", "third", "year", "month", "week",
    "day", "today", "tomorrow", "yesterday", "morning", "evening",
    "annual", "quarterly", "monthly", "weekly",
}
