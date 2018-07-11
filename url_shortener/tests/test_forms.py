from django.test import TestCase
from url_shortener.forms import URLForm


class FormTests(TestCase):

    def test_form_valid_data(self):
        '''
        Checks the validity of URLForm when the data entered are valid.
        '''
        # Basic URL
        form = URLForm({'url': 'https://www.techcrunch.com/some-slug-here-starting-from-s'})
        self.assertTrue(form.is_valid())

        # URL containing multiple paths
        form = URLForm({'url': 'https://www.techcrunch.com/some/slug/here-starting-from-s'})
        self.assertTrue(form.is_valid())

        # URL starting with 'http' instead of 'https'
        form = URLForm({'url': 'http://www.techcrunch.com/some-slug'})
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        '''
        Checks the validity of URLForm when the data entered are not valid.
        '''
        form = URLForm({'url': ''})
        self.assertFalse(form.is_valid())

        form = URLForm({'url': 'www.techcrunch.c/some-slug'})
        self.assertFalse(form.is_valid())

        form = URLForm({'url': '.com/some-slug'})
        self.assertFalse(form.is_valid())
