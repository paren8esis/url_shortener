from django.test import TestCase

from url_shortener.models import Letter, Word


class ModelTests(TestCase):

    def setUp(self):
        '''
        Populates the database with some sample objects.
        '''
        let_m = Letter(letter='m', current_index=5)
        let_m.save()
        let_a = Letter(letter='a')
        let_a.save()

        Word(word='mara', letter=let_m, word_id=2).save()
        Word(word='anna', letter=let_a, word_id=0).save()

    def test_population_script(self):
        '''
        Checks if the script populate_database.py exists and if it contains the
        function populate().
        '''
        try:
            from populate_database import populate
        except ImportError:
            print('The module populate_database does not exist')
        except NameError:
            print('The function populate() does not exist or is not correct')

    def get_letter_object(self, letter):
        '''
        Returns a Letter object.
        '''
        try:
            let = Letter.objects.get(letter=letter)
        except Letter.DoesNotExist:
            let = None
        return let

    def test_letter_m_added(self):
        '''
        Checks if Letter object 'm' was successfully added to the database.
        '''
        let = self.get_letter_object(letter='m')
        self.assertIsNotNone(let)

    def test_letter_m_with_current_index_added(self):
        '''
        Checks if the attribute 'current_index' of the Letter object 'm' was
        succesffully added to the database.
        '''
        let = self.get_letter_object(letter='m')
        self.assertEquals(let.current_index, 5)

    def test_letter_a_added(self):
        '''
        Checks if Letter object 'a' was successfully added to the database.
        '''
        let = self.get_letter_object(letter='a')
        self.assertIsNotNone(let)

    def test_letter_a_with_current_index_added(self):
        '''
        Checks if the attribute 'current_index' of the Letter object 'a' was
        succesffully added to the database with its default value 0.
        '''
        let = self.get_letter_object(letter='a')
        self.assertEquals(let.current_index, 0)

    def test_letter_insertion_with_invalid_letter(self):
        from django.core.exceptions import ValidationError
        try:
            let = Letter(letter='ma')
            let.save()
            self.fail("Inserted Letter object with letter field of length 2.")
        except ValidationError:
            pass
