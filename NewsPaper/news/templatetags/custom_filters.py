from django import template

register = template.Library()

# Список нежелательных слов
CENSORED_WORDS = [
    'редиска', 'дурак', 'плохой', 'глупый',  
]

@register.filter
def censor(value):
    if not isinstance(value, str):
        return value
    
    words = value.split()
    censored_text = []
    
    for word in words:
        # Проверяем слово без учета регистра
        if word.lower() in [w.lower() for w in CENSORED_WORDS]:
            # Заменяем все буквы кроме первой на '*'
            if len(word) > 1:
                censored_word = word[0] + '*' * (len(word) - 1)
            else:
                censored_word = '*'
            censored_text.append(censored_word)
        else:
            censored_text.append(word)
    
    return ' '.join(censored_text)