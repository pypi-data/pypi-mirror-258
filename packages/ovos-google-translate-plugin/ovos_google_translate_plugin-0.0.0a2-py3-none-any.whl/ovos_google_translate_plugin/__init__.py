from typing import Union, List

import requests
from ovos_plugin_manager.templates.language import LanguageDetector
from ovos_plugin_manager.templates.language import LanguageTranslator


def google_tx(text, target="en", source="auto"):
    url = "https://clients5.google.com/translate_a/t"
    params = {
        "client": "dict-chrome-ex",
        "sl": source or "auto",
        "tl": target,
        "q": text
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'
    }
    try:
        request_result = requests.get(url, params=params, headers=headers).json()
        return request_result
    except:
        pass


class GoogleLangDetectPlugin(LanguageDetector):
    def detect(self, text):
        try:
            request_result = google_tx(text)
            return request_result[0][-1]
        except:
            pass

    def detect_probs(self, text):
        l = self.detect(text)
        if l:
            return {l: 1.0}
        return {}


class GoogleTranslatePlugin(LanguageTranslator):

    def translate(self,
                  text: Union[str, List[str]],
                  target: str = "",
                  source: str = "auto") -> Union[str, List[str]]:
        try:
            request_result = google_tx(text, target, source)
            return request_result[0][0]
        except:
            pass


if __name__ == "__main__":
    text = 'لماذا تفعل هذا'
    g = GoogleLangDetectPlugin()
    print(g.detect(text))
    g = GoogleTranslatePlugin()
    print(g.translate(text, "en"))
