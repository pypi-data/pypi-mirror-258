#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Optional

from octodiary.types.model import DT, Type


class Notification(Type):
    datetime: Optional[DT] = None
    event_type: Optional[str] = None
    created_at: Optional[DT] = None
    updated_at: Optional[DT] = None
    subject_name: Optional[str] = None
    new_hw_description: Optional[str] = None
    teacher_name: Optional[str] = None
    new_date_assigned_on: Optional[str] = None
    new_date_prepared_for: Optional[str] = None
    student_profile_id: Optional[int] = None
    author_profile_id: Optional[int] = None
    lesson_date: Optional[str] = None
    old_mark_value: Optional[str] = None
    new_mark_value: Optional[str] = None
    new_is_exam: Optional[bool] = None
    new_mark_weight: Optional[int] = None
    control_form_name: Optional[str] = None
