from Repository.LessonRepository import LessonRepository


def get_schedule(schedule_id: int):
    lessonRepository = LessonRepository()
    schedule = lessonRepository.get_lessons_by_schedule(schedule_id=schedule_id)
    return None
