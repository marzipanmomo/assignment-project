from django.db.models import Q
from .models import Product, Category
import difflib

# synonyms
SYNONYMS = {
    'couch': ['sofa'],
    'sofa': ['couch'],
    'nightstand': ['bedside'],
    'drawers': ['dresser', 'bedside'],
}

def word_variants(word):
    word = word.lower()
    variants = {word}

    if len(word) > 3:
        if word.endswith('ves'): # ves -> f
            variants.update({word[:-3] + 'f', word[:-3] + 'fe'})
        if word.endswith('ies'): # ies -> y
            variants.add(word[:-3] + 'y')
        if word.endswith('es'): # es -> nothing
            variants.add(word[:-2])
        if word.endswith('s'): # s -> nothing
            variants.add(word[:-1])
        if word.endswith('f'): # f -> ves
            variants.add(word[:-1] + 'ves')
        if word.endswith('y'): # y -> ies
            variants.add(word[:-1] + 'ies')

    for v in list(variants):
        variants.update(SYNONYMS.get(v,[]))
    return variants

def word_query(word):
    q = Q()
    for v in word_variants(word):
        q |= (
            Q(name__icontains=v)
            | Q(description__icontains=v)
            | Q(option__icontains=v)
            | Q(categories__name__icontains=v)
        )
    return q

def suggest_query(query):
    texts = list(Product.objects.values_list('name', flat=True))
    texts += list(Category.objects.values_list('name', flat=True))
    vocab = {w.lower().strip('-&') for t in texts for w in t.split()}

    corrected, changed = [], False
    for word in query.lower().split():
        if word in vocab:
            corrected.append(word)
            continue
        match = difflib.get_close_matches(word, vocab, n=1, cutoff=0.75)
        if match:
            corrected.append(match[0])
            changed = True
        else:
            corrected.append(word)
    return ' '.join(corrected) if changed else None