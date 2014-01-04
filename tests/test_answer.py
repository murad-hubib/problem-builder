
# Imports ###########################################################

from mentoring.test_base import MentoringBaseTest


# Classes ###########################################################

class AnswerBlockTest(MentoringBaseTest):

    def test_answer_edit(self):
        """
        Answers of same name should share value accross blocks
        """
        # Answer should initially be blank on all instances with the same answer name
        mentoring = self.go_to_page('Answer Edit 2')
        answer1_bis = mentoring.find_element_by_css_selector('.xblock textarea')
        answer1_readonly = mentoring.find_element_by_css_selector('blockquote.answer.read_only')
        self.assertEqual(answer1_bis.get_attribute('value'), '')
        self.assertEqual(answer1_readonly.text, '')

        # Another answer with the same name
        mentoring = self.go_to_page('Answer Edit 1')
        header1 = self.browser.find_element_by_css_selector('h1')
        self.assertEqual(header1.text, 'XBlock: Answer Edit 1')

        # Check <html> child
        p = mentoring.find_element_by_css_selector('div.xblock > p')
        self.assertEqual(p.text, 'This should be displayed in the answer_edit scenario')

        # Initial unsubmitted text
        answer1 = mentoring.find_element_by_css_selector('textarea')
        self.assertEqual(answer1.text, '')
        progress = mentoring.find_element_by_css_selector('.progress > .indicator')
        self.assertEqual(progress.text, '(Not completed)')
        self.assertFalse(progress.find_elements_by_xpath('./*'))

        # Submit without answer
        submit = mentoring.find_element_by_css_selector('input.submit')
        submit.click()
        self.assertEqual(answer1.get_attribute('value'), '')
        self.assertEqual(progress.text, '(Not completed)')
        self.assertFalse(progress.find_elements_by_xpath('./*'))

        # Submit an answer
        answer1.send_keys('This is the answer')
        submit.click()

        self.assertEqual(answer1.get_attribute('value'), 'This is the answer')
        self.assertEqual(progress.text, '')
        self.assertTrue(progress.find_elements_by_css_selector('img'))

        # Answer content should show on a different instance with the same name
        mentoring = self.go_to_page('Answer Edit 2')
        answer1_bis = mentoring.find_element_by_css_selector('.xblock textarea')
        answer1_readonly = mentoring.find_element_by_css_selector('blockquote.answer.read_only')
        self.assertEqual(answer1_bis.get_attribute('value'), 'This is the answer')
        self.assertEqual(answer1_readonly.text, 'This is the answer')

    def test_answer_blank_read_only(self):
        """
        Read-only answers should not prevent completion when blank
        """
        # Check initial state
        mentoring = self.go_to_page('Answer Blank Read Only')
        answer = mentoring.find_element_by_css_selector('blockquote.answer.read_only')
        self.assertEqual(answer.text, '')
        progress = mentoring.find_element_by_css_selector('.progress > .indicator')
        self.assertEqual(progress.text, '(Not completed)')

        # Submit should allow to complete
        submit = mentoring.find_element_by_css_selector('input.submit')
        submit.click()
        self.assertEqual(progress.text, '')
        self.assertTrue(progress.find_elements_by_css_selector('img'))

