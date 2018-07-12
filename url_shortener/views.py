from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist

from url_shortener.forms import URLForm
from url_shortener.models import Word, Letter
    

def index(request):
    '''
    This is the Index view.
    '''
    if request.method == 'GET':
        # A GET request
        form = URLForm()
    else:
        # A POST request
        form = URLForm(request.POST)

        # If data is valid, proceed to shorten the URL and redirect the user
        if form.is_valid():
            url = form.cleaned_data['url']

            url_path = url.split('/')[-1]
            found = False
            # Look for first available letter in URL path
            for i in range(len(url_path)):
                try:
                    letter_obj = Letter.objects.get(letter=url_path[i])

                    if letter_obj.current_index != -1:   # Available letter found
                        found = True
                        break
                except ObjectDoesNotExist:
                    # We don't have any words matching to that particular letter
                    continue

            # Check if an available letter was found
            if found:
                # Create new URL and update the letter's current_index
                # attribute
                new_path = Word.objects.filter(letter=letter_obj,
                                               word_id=letter_obj.current_index).first().word
                if letter_obj.current_index == letter_obj.num_words-1:
                    letter_obj.current_index = -1
                else:
                    letter_obj.current_index += 1
                letter_obj.save()

                new_url = 'http://example.com/' + new_path
                return render(request, 'url_shortener/result.html',
                              context={'url': new_url})
            else:   # No available letters found - return appropriate message
                return render(request, 'url_shortener/result.html',
                              context={'no_letters': True})
    return render(request, 'url_shortener/index.html', context={'form': form})


def about(request):
    '''
    This is the About view.
    '''
    return render(request, 'url_shortener/about.html', context={})


def result(request):
    '''
    This is the Result page.
    '''
    return render(request, 'url_shortener/result.html',
                  context={'url': None, 'no_letters': None})
