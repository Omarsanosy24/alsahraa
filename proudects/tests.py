import json
from datetime import datetime

data = [
    {
        "name": "ITSE204 CourseProject1",
        "sections": [
            {
                "No.": "1",
                "lessons": [
                    {
                        "sec": {
                            "course": 1,
                            "sectionNo": "1"
                        },
                        "from": "08:00",
                        "to": "10:00 ",
                        "place": "N228",
                        "teacher": "JACQUELINE FATYARA",
                        "day": "monday"
                    }
                ]
            },
            {
                "No.": "2",
                "lessons": [
                    {
                        "sec": {
                            "course": 1,
                            "sectionNo": "2"
                        },
                        "from": "12:00",
                        "to": "14:00",
                        "place": "BS002",
                        "teacher": "Dr.YusraMohammedAl Roshid",
                        "day": "tuesday"
                    }
                ]
            },
            {
                "No.": "3",
                "lessons": [
                    {
                        "sec": {
                            "course": 1,
                            "sectionNo": "3"
                        },
                        "from": "10:00",
                        "to": "12:00 ",
                        "place": "N228",
                        "teacher": "Wardha",
                        "day": "monday"
                    }
                ]
            }
        ]
    },
    {
        "name": "ITSE204 CourseProject2",
        "sections": [
            {
                "No.": "1",
                "lessons": [
                    {
                        "sec": {
                            "course": 1,
                            "sectionNo": "1"
                        },
                        "from": "08:00",
                        "to": "10:00 ",
                        "place": "N228",
                        "teacher": "JACQUELINE FATYARA",
                        "day": "monday"
                    }
                ]
            },
            {
                "No.": "2",
                "lessons": [
                    {
                        "sec": {
                            "course": 1,
                            "sectionNo": "2"
                        },
                        "from": "12:00",
                        "to": "14:00",
                        "place": "BS002",
                        "teacher": "Dr.YusraMohammedAl Roshid",
                        "day": "tuesday"
                    }
                ]
            },
            {
                "No.": "3",
                "lessons": [
                    {
                        "sec": {
                            "course": 1,
                            "sectionNo": "3"
                        },
                        "from": "10:00",
                        "to": "12:00 ",
                        "place": "N228",
                        "teacher": "Wardha",
                        "day": "monday"
                    }
                ]
            }
        ]
    }
]

# تحديد الوقت المطلوب للفرز
target_time = datetime.strptime("10:00", "%H:%M")

# تحويل الوقت المطلوب إلى عدد دقائق منتصف الليل
target_time_in_minutes = (target_time - target_time.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds() / 60

# حساب الفرق الزمني بين وقت الدرس والوقت المحدد
def time_diff(lesson):
    lesson_time = datetime.strptime(lesson["from"], "%H:%M")
    lesson_time_in_minutes = (lesson_time - lesson_time.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds() / 60
    return abs(lesson_time_in_minutes - target_time_in_minutes)

# ترتيب الأقسام بناءً على الفرق الزمني
for course in data:
    for section in course["sections"]:
        section["lessons"] = sorted(section["lessons"], key=time_diff)

# طباعة بيانات الأقسام المرتبة
print(json.dumps(data, indent=2))


