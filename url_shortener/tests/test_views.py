from django.test import TestCase
from django.urls import reverse


class AboutViewTests(TestCase):

    def test_about_page_exists(self):
        '''
        Checks if the About page exists.
        '''
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_about_using_template(self):
        '''
        Check the template used to render the About page.
        '''
        response = self.client.get(reverse('about'))
        self.assertTemplateUsed(response, 'url_shortener/about.html')


class ResultViewTests(TestCase):

    def test_result_page_exists(self):
        '''
        Checks if the Result page exists.
        '''
        response = self.client.get(reverse('result'))
        self.assertEqual(response.status_code, 200)

    def test_result_using_template(self):
        '''
        Check the template used to render the Result page.
        '''
        response = self.client.get(reverse('result'))
        self.assertTemplateUsed(response, 'url_shortener/result.html')

    def test_result_view_with_no_url_given(self):
        '''
        If no URL was given by the user, an appropriate message should be
        displayed.
        '''
        response = self.client.get(reverse('result'))
        self.assertContains(response,
                            "Oh my, no URL was provided! Please go back and try again.")
        self.assertIsNone(response.context['url'])
        self.assertIsNone(response.context['no_letters'])


class IndexViewTests(TestCase):

    def test_index_page_exists(self):
        '''
        Checks if the Index page exists.
        '''
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_index_using_template(self):
        '''
        Check the template used to render the Index page.
        '''
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'url_shortener/index.html')

    def test_index_with_get_method(self):
        '''
        Check if the Index page returns the URLForm when request method is GET.
        '''
        response = self.client.get(reverse('index'))
        self.assertIn('form', response.context)

    def test_index_with_no_letters_found(self):
        '''
        Check if the Index page returns appropriate context variable when no
        available letters were found for the URL shortening.
        '''
        # Populate the database with some sample objects
        from url_shortener.models import Letter
        Letter(letter='a', current_index=-1).save()
        Letter(letter='b', current_index=-1).save()

        # Check the view's response
        response = self.client.post(reverse('index'),
                                    {'url': 'https://www.techcrunch.com/ab'})
        self.assertTrue(response.context['no_letters'])

        response = self.client.post(reverse('index'),
                                    {'url': 'https://www.techcrunch.com/----'})
        self.assertTrue(response.context['no_letters'])

        response = self.client.post(reverse('index'),
                                    {'url': 'https://www.techcrunch.com/-aa-b'})
        self.assertTrue(response.context['no_letters'])

    def test_index_with_successful_url_shortening_on_first_letter(self):
        '''
        Check if the Index page returns appropriate context variable when the
        shortening is successful by using only the first letter of the original
        URL.
        '''
        # Populate the database with some sample objects
        from url_shortener.models import Letter, Word
        let_a = Letter(letter='a', current_index=0, num_words=1)
        let_a.save()
        Word(word='aaa', word_id=0, letter=let_a).save()
        let_b = Letter(letter='b', current_index=0, num_words=1)
        let_b.save()
        Word(word='baa', word_id=0, letter=let_b).save()

        # Check the view's response
        response = self.client.post(reverse('index'),
                                    {'url': 'https://www.techcrunch.com/ab'})
        self.assertEqual(response.context['url'], 'http://example.com/aaa')

    def test_index_with_successful_shortening_on_second_letter(self):
        '''
        Check if the Index page returns appropriate context variable when the
        shortening is successful by using the second letter of the original
        URL.
        '''
        # Populate the database with some sample objects
        from url_shortener.models import Letter, Word
        Letter(letter='a', current_index=-1).save()
        let_b = Letter(letter='b', current_index=0, num_words=1)
        let_b.save()
        let_c = Letter(letter='c', current_index=0, num_words=1)
        let_c.save()
        Word(word='baa', word_id=0, letter=let_b).save()
        Word(word='caa', word_id=0, letter=let_c).save()

        # Check the view's response
        response = self.client.post(reverse('index'),
                                    {'url': 'https://www.techcrunch.com/abc'})
        self.assertEqual(response.context['url'], 'http://example.com/baa')

    def test_index_with_letters_not_in_database(self):
        '''
        Check if the Index page returns appropriate context variable when the
        original URL contains letters that do not exist in the database.
        '''
        # Populate the database with some sample objects
        from url_shortener.models import Letter, Word
        Letter(letter='a', current_index=-1).save()
        let = Letter(letter='b', current_index=0, num_words=1)
        let.save()
        Word(word='baa', word_id=0, letter=let).save()

        # Check the view's response
        response = self.client.post(reverse('index'),
                                    {'url': 'https://www.techcrunch.com/--ab'})
        self.assertEqual(response.context['url'], 'http://example.com/baa')

    def test_index_letter_current_index_incrementation(self):
        '''
        Checks if the current_index attribute of the Letter object is
        incremented successfully when the word it points to is used.
        '''
        from url_shortener.models import Letter, Word
        let = Letter(letter='a', current_index=0, num_words=2)
        let.save()
        Word(word='aaa', word_id=0, letter=let).save()
        Word(word='aaaaa', word_id=1, letter=let).save()

        # Use first word
        self.client.post(reverse('index'),
                         {'url': 'https://www.techcrunch.com/abc'})

        let = Letter.objects.get(letter='a')
        self.assertEquals(let.current_index, 1)

        # Use second word
        self.client.post(reverse('index'),
                         {'url': 'https://www.techcrunch.com/abc'})

        let = Letter.objects.get(letter='a')
        self.assertEquals(let.current_index, -1)
