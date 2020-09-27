import markdown2
from django.shortcuts import render
from . import util
from markdown2 import Markdown
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms
import secrets

class EntryForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput)
    content = forms.CharField(widget=forms.Textarea)
    editconfirmation= forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)

def index(request):
    return render(request, "encyclopedia/index.html", {"entry_pages": util.list_entries()})

def newentry(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if (util.get_entry(title) is None or form.cleaned_data["editconfirmation"] is True):
                util.save_entry(title,content)
                return HttpResponseRedirect(reverse("entrypage", kwargs={'entryname': title}))
            else:
                return render(request, "encyclopedia/newentrypage.html", {"form": form, "pageexists": True, "entry": title})
        else:
            return render(request, "encyclopedia/newentrypage.html", {"form": form, "pageexists": False})
    else:
        return render(request,"encyclopedia/newentrypage.html", {"form": EntryForm(), "pageexists": False,})

def entry(request, entryname):
    markdowner = Markdown()
    entrypagedata = util.get_entry(entryname)
    if entrypagedata is not None:
        return render(request, "encyclopedia/entrypage.html", {"entry": markdowner.convert(entrypagedata),"entryname": entryname})
    else:
        return render(request, "encyclopedia/nopage.html", {"entryname": entryname})

def search(request):
    searchword = request.GET.get('q')
    y=util.list_entries()
    if(util.get_entry(searchword) is not None):
        return HttpResponseRedirect(reverse("entrypage", kwargs={'entryname': searchword }))
    else:
        searchlist=[]
        for i in y:
            if searchword.lower() in i.lower():
                searchlist.append(i)
        return render(request, "encyclopedia/index.html", {"entry_pages": searchlist,"searchword": searchword, "search": True})

def edit(request, entryname):
    entrypagedata = util.get_entry(entryname)
    if entrypagedata is not None:
        form = EntryForm()
        form.fields["title"].initial = entryname
        form.fields["content"].initial = entrypagedata
        form.fields["editconfirmation"].initial = True
        return render(request, "encyclopedia/newentrypage.html", {"form": form,"edit": form.fields["editconfirmation"].initial, "entryname": form.fields["title"].initial})
    else:
        return render(request, "encyclopedia/nopage.html")

def random(request):
    entrypagelist = util.list_entries()
    randomentrypage = secrets.choice(entrypagelist)
    return HttpResponseRedirect(reverse("entrypage", kwargs={'entryname': randomentrypage}))
