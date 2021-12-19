import http

from django.http import HttpResponseNotFound, Http404
from django.test import TestCase, Client

from TAInformation.models import Course, User

class TestViewCoursesInstructor(TestCase):
    def setUp(self):
        self.client = Client()
        self.defaultCourse = Course(None,
                                    {"course_name": "english", "instructor_id": 1, "meeting_time": "M-W 1:00 - 2:15",
                                     "semester": "Spring 2022"})

        self.noNameCourse = Course(None, {"course_name": None, "instructor_id": 1, "meeting_time": "M-W 1:00 - 2:15",
                                          "semester": "Spring 2022"})
        self.user = User(1, "testInstructor", "Instructor", "testInstructor@test.com", "3452 Tester Lane, TestVille",2,"(414)222-2571").save()

    def test_default(self):
        response = self.client.post("/course",
                                    {"course_name": "english", "instructor_id": 1, "meeting_time": "M-W 1:00 - 2:15",
                                     "semester": "Spring 2022"}, follow=True)
        self.assertEqual(
            self.Course.addCourse({"course_name": "english", "instructor_id": 1, "meeting_time": "M-W 1:00 - 2:15",
                                   "semester": "Spring 2022"}), response)

    def test_no_name(self):
        response = self.client.post("/course",
                                    {"course_name": None, "instructor_id": 1, "meeting_time": "M-W 1:00 - 2:15",
                                     "semester": "Spring 2022"}, follow=True)
        failure_msg = "Missing required fields. Please enter all fields before continuing"
        self.assertEqual(response.context["message"], msg=failure_msg)

    def test_no_instructor(self):
        response = self.client.post("/course",
                                    {"course_name": "math", "instructor_id": 0, "meeting_time": "M-W 1:00 - 2:15",
                                     "semester": "Spring 2022"}, follow=True)
        failure_msg = "Missing required fields. Please enter all fields before continuing "
        self.assertEqual(response.context["message"], msg=failure_msg)

    def test_other_instructor(self):
        response = self.client.post("/course",
                                    {"course_name": "math", "instructor_id": 2, "meeting_time": "M-W 1:00 - 2:15",
                                     "semester": "Spring 2022"}, follow=True)
        failure_msg = "Displaying course for other instructor, should be empty"
        self.assertEqual(HttpResponseNotFound.status_code , response.status_code, msg=failure_msg)

    def test_no_meetingtime(self):
        response = self.client.post("/course",
                                    {"course_name": "english", "instructor_id": 1, "meeting_time": None,
                                     "semester": "Spring 2022"}, follow=True)
        failure_msg = "Missing required fields. Please enter all fields before continuing "
        self.assertEqual(response.context["message"], msg=failure_msg)

    def test_no_semester(self):
        response = self.client.post("/course",
                                    {"course_name": "Geo Sci 101", "instructor_id": 1, "meeting_time": "M-W 1:00 - 2:15",
                                     "semester": None}, follow=True)
        failure_msg = "Missing required fields. Please enter all fields before continuing "
        self.assertEqual(response.context["message"], msg=failure_msg)

    def test_already_exists(self):
        response = self.client.post("/course",
                                    {"course_name": "math", "instructor_id": 1, "meeting_time": "M-W 1:00 - 2:15",
                                     "semester": "Spring 2022"}, follow=True)
        failure_msg = "Missing required fields. Please enter all fields before continuing "
        self.assertNotEqual(response.context["message"], msg=failure_msg)

        response = self.client.post("/course",
                                    {"course_name": "math", "instructor_id": 1, "meeting_time": "M-W 1:00 - 2:15",
                                     "semester": "Spring 2022"}, follow=True)
        self.assertEqual(response.context["message"], msg=failure_msg)

