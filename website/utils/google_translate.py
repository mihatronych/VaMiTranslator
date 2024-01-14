from googletrans import Translator

translator = Translator()


def translate(source_string):
    return translator.translate(source_string, src='ru', dest='uk').text
