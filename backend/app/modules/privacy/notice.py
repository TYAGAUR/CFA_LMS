"""Privacy notice shown before consent (C-03 §2). Bump NOTICE_VERSION on material change."""

NOTICE_VERSION = "2026-11-v1"

NOTICE = {
    "version": NOTICE_VERSION,
    "title": "How we use your information",
    "sections": [
        {"heading": "What we collect",
         "text": "Your name, mobile number, optional email, date of birth (only to check whether you are under 18), "
                 "your course registration and payments, and your learning progress on this platform."},
        {"heading": "Why we use it",
         "text": "To create your account, let you study the subjects you registered for, track your progress, "
                 "process fee payments, keep the platform secure, and meet legal obligations."},
        {"heading": "Optional uses",
         "text": "Only if you agree: usage analytics to improve the product, and messages about new batches and "
                 "events. You can change these choices any time under Profile → Privacy."},
        {"heading": "Students under 18",
         "text": "A parent or legal guardian must give consent before the account is activated. Usage analytics "
                 "and leaderboard display are switched off for students under 18."},
        {"heading": "Who we share it with",
         "text": "Only service providers that run the platform for us (hosting in India, SMS, email, video "
                 "delivery and the payment gateway). Card and bank details are entered on the payment "
                 "gateway's page and never reach us."},
        {"heading": "Your rights",
         "text": "You can ask for a copy of your data, correct it, ask us to delete it, nominate someone to act "
                 "for you, and raise a grievance with our Grievance Officer. You may also complain to the Data "
                 "Protection Board of India."},
        {"heading": "Contact",
         "text": "Grievance Officer: [name], grievance@[domain] (placeholder until appointed)."},
    ],
    "optional_purposes": [
        {"purpose": "product_analytics", "label": "Help improve the product (usage analytics)", "adults_only": True},
        {"purpose": "marketing_messages", "label": "Send me updates about batches and events", "adults_only": False},
    ],
}
