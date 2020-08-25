d = {
    "en": f"""
Hello!

Send me the text you want to post on Instagram. If it's shorter than 2200 characters, I'll add linebreaks to it. If it is longer, I'll put the rest of it on pictures.
        """,
    "ru": f"""
Привет! 

Отправь мне текст, который хочешь опубликовать в Instagram. Если он короче 2200 символов, я расставлю в нем переносы строк. А если длиннее, то сверстаю текст в картинки.  
        """,
}
def MESSAGE_START(l="en"):
    return d[l] if l in d else d["en"]


def RENDERED(l="en"):
    d = {
        "en": f"""
If bot gives an error or you want to propose a feature, feel free to message the developer @chakchurina. 
        """,
        "ru": f"""
Если что-то пошло не так или есть, что сказать, напишите разработчику: @chakchurina.  
        """,
}
    return d[l] if l in d else d["en"]


def MESSAGE_TEMPLATE(l="en"):
    d = {
        "en": "",
        "ru": "",
    }
    return d[l] if l in d else d["en"]