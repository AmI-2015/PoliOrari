import datetime

import politoschedule

if __name__ == "__main__":

    # Find all courses matching a given text (teacher or course name)

    search_text = "Corno"

    courses = politoschedule.find_courses_by_text(search_text)

    print "Courses matching '%s':" % search_text
    for course in courses:
        print "\t%s (%s) - prof. %s - key %s" % (course.topic, course.alpha_range, course.teacher, course.key)

    # Find all events (classes, exams) involving one of the courses

    course_keys = [course.key for course in courses]  # generate a list with the keys of all found courses
    events = politoschedule.find_events_by_courses(course_keys, datetime.date.today())

    # note: if you have just one course to search, use find_events_by_courses([key], datetime.date.today())
    # because the first parameter must be a list: [key]

    print "Related events:"
    for event in events:
        print "\t%s -> %s: %s (%s) [Room %s]" % (event.start, event.end, event.topic, event.teacher, event.roomname)

    rooms = politoschedule.get_all_classrooms()
    print "There are %d classrooms" % len(rooms)
    for room in rooms:
        print "\tRoom %s (Campus %s, Building %s), type %s, seats %d, (%.6f,%.6f)" % (
            room.name, room.campus, room.building,
            room.type, room.seats,
            room.lat, room.lon)

    test_room = '3I'
    print "Today's events in classroom "+test_room

    room_events = politoschedule.find_events_by_room(test_room, datetime.date.today())

    for event in room_events:
        print "\t%s -> %s: %s (%s) [Room %s]" % (event.start, event.end, event.topic, event.teacher, event.roomname)