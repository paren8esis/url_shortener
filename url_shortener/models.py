from django.db import models


class Letter(models.Model):
    '''
    Letter model.
    '''
    letter = models.CharField(max_length=1, unique=True)
    current_index = models.IntegerField(default=0)
    num_words = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.letter

    def save(self, *args, **kwargs):
        '''
        Sqlite does not enforce the max length of VARCHAR on object creation,
        so we must do it manually.
        https://sqlite.org/faq.html#q9
        '''
        self.full_clean()
        super(Letter, self).save(*args, **kwargs)


class Word(models.Model):
    '''
    Word model.
    '''
    letter = models.ForeignKey(Letter, on_delete=models.PROTECT)
    word = models.CharField(max_length=128)
    word_id = models.PositiveIntegerField()

    def __str__(self):
        return self.word
