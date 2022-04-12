


from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from . import util
import random

# from markdown2 import Markdown
# importing a specific function called "Markdown" from markdown2 which converts markdown to html
# markdowner = Markdown ()
import markdown2

class newEntryForm(forms.Form):
    # define the fields we'd like the field to have
    # title = forms.CharField(label="wiki entry title", max_length=100)
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'title', 'style': 'width: 300px;', 'class': 'form-control'}))
    # content = forms.TextArea(label="Enter the content here", max_length=1000)
    content = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'placeholder' : 'content', 'style' : 'width: 400px', 'class': 'form-control'}))
    # edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)
    edit = forms.BooleanField(widget=forms.HiddenInput(), required=False, initial=False)

def index(request):
    # store the titles and content inside of the user's session
    # if "titles" not in request.session:
    #     request.session["titles"] = []
    # if "content" not in request.session:
    #     request.session["content"] = []
    if "entries" not in request.session:
        request.session["entries"] = util.list_entries()

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
# end index function


def entry(request, title):
    # markdowner = markdown()
    content = util.get_entry(title)
    if content == None:
        return render(request, "encyclopedia/invalidEntry.html", {
            "title": title
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "content":(content),
            "title": title
        })
# end entry function

def search(request):
    # print("hello")
    recommendEntries = False
    
    if request.method == "GET":
        title = request.GET.get('q')
        content = util.get_entry(title)
        # if the entry/title is in the list of entries
        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": content
            })
        else:
            ## let the user know of a matching entry
            ## ex user enters py
            ## we should suggest python
            possibleEntries = []
            recommendEntries = True
            entries = util.list_entries()
            for e in entries:
                if title.lower() in e.lower():
                    possibleEntries.append(e)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                # "content": context,
                "recommendEntries": recommendEntries,
                "possibleEntries": possibleEntries
            })
# end search function
   
def newEntry(request):
    # isUpdate = False
    if request.method == "POST":
        # request.POST contains all the data the user submitted on the form
        form = newEntryForm(request.POST)
      
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            edit = form.cleaned_data["edit"]
            # edit = form.cleaned_data["edit"]
            # edit = form.cleaned_data["edit"]
            # get a reference to that entry
            ###### Need to do something here to prevent it from not letting us
            ###### Update our entries
            newEntry = util.get_entry(title)
            if newEntry is not None and edit is False:  ### and update is False
                # item already exists
                content = "This entry already exists!"
            else: 
                # it's a new entry and we should save it in the list of entries 
                util.save_entry(title, content)

            ## adding a list to the list
            # appending lists
            request.session['entries'] += [newEntry]
            # return HttpResponseRedirect(reverse("wiki:entry"))
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": content
                ##### edit should be enabled
            })
        else:
            return render(request, "enyclopedia/newEntry.html", {
                # return existing form
                "form": form
            }) 

    return render(request, "encyclopedia/newEntry.html", {
        # return a new form
        "form": newEntryForm()
    }) # end newEntry function
    

def editEntry(request):
    # update = True
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        ## creating a dictionary of prepopulated values for the form
        # data_dict = {'title': title, "content": content, 'edit': True}

        form = newEntryForm()
        form.fields['content'].initial = content
        form.fields['edit'].initial = True
        # form.fields['title'].disabled = True
        form.fields['title'].initial = title
        form.fields['title'].widget = forms.HiddenInput()
        # edit.disable()
        # print myForm.cleaned_data.get('description')
        return render(request, "encyclopedia/newEntry.html", {
            "form": form,
            "title": title,
            "update": True
        })
## end edit entry

def randomEntry(request):
    entries = util.list_entries()
    # randomEntryNum = random.randint(0, len(entries)-1)
    # entry = entries[randomEntryNum]
    entryTitle = random.choice(entries)
    content = util.get_entry(entryTitle)
    # randomEntry = 
    # return render(request, "encyclopedia/entry.html", {
    #     "title": entryTitle,
    #     "content": content
    #     # "randomEntryNum": randomEntryNum
    # })
    # return HttpResponseRedirect(reverse("entry", kwargs={"entry": entry}))

    ## will call the entry view function and pass it the argument entry (title)
    return HttpResponseRedirect(reverse("wiki:entry", kwargs={"title": entryTitle}))





    # return render(request, "encyclopedia/editEntry.html", {

    #  })

        # if (util.get_entry(title) is not None):
            # return HttpResponseRedirect(reverse("wiki:entry", kwargs={'entry':title}))
        # return HttpResponseRedirect(reverse("entry", kwargs={'entry':title}))