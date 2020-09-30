#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Contains Django code for the Wiki Project"""


import markdown2
import secrets

from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import util
from markdown2 import Markdown

#Class Creation for Each Entry
class EntryForm(forms.Form):
    """Class for each entry form and its relevant components."""
    title = forms.CharField(widget=forms.TextInput)
    content = forms.CharField(widget=forms.Textarea)
    edit_confirmation= forms.BooleanField(initial=False,
                                          widget=forms.HiddenInput(),
                                          required=False)

# Index Page
def index(request):
    """Simply returns the index page."""
    return render(request, "encyclopedia/index.html", {"entry_pages": util.list_entries()})

# Generate a New Entry Page
def new_entry(request):
    """Contains the relevant possibilities/code for a new entry page."""
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if (util.get_entry(title) is None or form.cleaned_data["edit_confirmation"] is True):
                util.save_entry(title,content)
                return HttpResponseRedirect(reverse("entry_page", kwargs={'entry_name': title}))
            else:
                return render(request, "encyclopedia/newentrypage.html", {"form": form,
                                                                          "page_exists": True,
                                                                          "entry": title}
                             )
        else:
            return render(request, "encyclopedia/newentrypage.html",
                          {"form": form,
                           "page_exists": False
                          }
                         )
    else:
        return render(request,"encyclopedia/newentrypage.html", {"form": EntryForm(),
                                                                 "page_exists": False,
                                                                }
                     )

#Existing Entry Page Functions    
def entry(request, entry_name):
    """Contains code to retrieve existing entry pages."""
    markdowner = Markdown()
    entry_page_data = util.get_entry(entry_name)
    if entry_page_data is not None:
        return render(request, "encyclopedia/entrypage.html",
                      {"entry": markdowner.convert(entry_page_data),
                       "entry_name": entry_name
                      }
                     )
    else:
        return render(request, "encyclopedia/nopage.html", {"entry_name": entry_name})

#Search Function    
def search(request):
    """Contains code to execute search queries."""
    search_word = request.GET.get('q')
    y=util.list_entries()
    if(util.get_entry(search_word) is not None):
        return HttpResponseRedirect(reverse("entry_page",
                                            kwargs={'entry_name': search_word }
                                           )
                                   )
    else:
        search_list=[]
        for i in y:
            if search_word.lower() in i.lower():
                search_list.append(i)
        return render(request, "encyclopedia/index.html",
                      {"entry_pages": search_list,
                       "search_word": search_word,
                       "search": True
                      }
                     )

# Edit Function    
def edit(request, entry_name):
    """Contains code to edit existing entry pages"""
    entry_page_data = util.get_entry(entry_name)
    if entry_page_data is not None:
        form = EntryForm()
        form.fields["title"].initial = entry_name
        form.fields["content"].initial = entry_page_data
        form.fields["edit_confirmation"].initial = True
        return render(request, "encyclopedia/newentrypage.html",
                      {"form": form,
                       "edit": form.fields["edit_confirmation"].initial, 
                       "entryname": form.fields["title"].initial
                      }
                     )
    else:
        return render(request, "encyclopedia/nopage.html")

# Random Page Generator    
def random(request):
    """Contains code to generate a randome existing entry page."""
    entry_page_list = util.list_entries()
    random_entry_page = secrets.choice(entry_page_list)
    return HttpResponseRedirect(reverse("entry_page",
                                        kwargs={'entry_name': random_entry_page}
                                       )
                               )
