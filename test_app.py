from app import app
from unittest import TestCase


class SurveysTesCase(TestCase):
    def test_select_survey(self):
        with app.test_client() as client:
            import pdb; pdb.set_trace