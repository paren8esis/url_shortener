#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django import forms


class URLForm(forms.Form):
    '''
    This class defines a form which takes a URL as input.

    Attributes
    ----------
    url : django.forms.URLField
        The input URL.
    '''
    url = forms.URLField(max_length=400,
                         help_text="Please enter the URL you want to shorten.")
