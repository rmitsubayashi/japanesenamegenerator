from django.shortcuts import render
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from kanji_generator import KanjiGenerator

kanji_generator = KanjiGenerator()

def index(request):
    context = {}
    if request.method == "POST":
        name = request.POST["name"]
        user_properties = request.POST["user_properties"]
        user_properties_arr = user_properties.split(',')
        kanjis = kanji_generator.generateKanji(name, user_properties_arr)
        relevantPhrases = set()
        for k in kanjis:
            relevantPhrases.update(k.relevant_phrases)
        context['kanjis'] = kanjis
        context['relevant_phrases'] = relevantPhrases
        context["name"] = name
        context["user_properties"] = user_properties
    return render(request, "web_app/index.html", context)