from selenium import webdriver
from selenium.webdriver.common.by import By
from typing import List
import io
import json
import re

import sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from src.model.kanji import Kanji
from src.model.kanji import Pronunciation
import src.util.language_utils as utils

def parse():
    joyo_kanjis = _parseJoyoKanji()
    # _parseJinmeiyoKanji()
    _saveKanjis(joyo_kanjis)

# 常用漢字
def _parseJoyoKanji() -> List[Kanji]:
    driver = _getJoyoKanjiDriver()
    wrapper_class = driver.find_element(By.CLASS_NAME, "mw-parser-output")
    all_tables = wrapper_class.find_elements_by_css_selector("table")
    table = all_tables[1].find_elements_by_css_selector("tbody")[0]
    rows = table.find_elements_by_css_selector("tr")
    print(len(rows))
    kanjis = []
    for row in rows:
        kanji = row.find_elements_by_css_selector("a")[0].text
        pronunciations = row.find_elements_by_css_selector("td")[8].text
        pronunciations = pronunciations.strip()
        pronunciations = pronunciations.split('、')
        # some pronunciations have annotations ie いばら[10]
        pronunciations = [re.sub("\[[0-9]+\]", "", p) for p in pronunciations]
        # some pronunciations are in parenthesis(全角)
        # 括弧でくくられた音訓は「特別なものか、又は用法のごく狭いもの」
        # we can try adjusting weight of parenthesis pronunciations later?
        pronunciations = [re.sub("[（）]", "", p) for p in pronunciations]
        # 音読み is in katakana
        language_utils = utils.LanguageUtils()
        pronunciations = [language_utils.convertKatakanaToKana(p) for p in pronunciations]
        for p in pronunciations:
            main_and_okurigana = p.split('-')
            pronunciation_class: Pronunciation
            if len(main_and_okurigana) == 1:
                pronunciation_class = Pronunciation(main_and_okurigana[0], "")
            else:
                pronunciation_class = Pronunciation(main_and_okurigana[0], main_and_okurigana[1])
            kanjis.append(Kanji(kanji, pronunciation_class))
        
    return kanjis


def _getJoyoKanjiDriver():
    driver = webdriver.Chrome()
    driver.get("https://ja.wikipedia.org/wiki/%E5%B8%B8%E7%94%A8%E6%BC%A2%E5%AD%97%E4%B8%80%E8%A6%A7")
    return driver


# 人名用漢字 (not in 常用漢字)
def _parseJinmeiyoKanji():
    pass

def _saveKanjis(kanjis: List[Kanji]):
    with io.open('data/kanji_pronunciations.txt', mode='w', encoding='utf-8') as file:
        for kanji in kanjis:
            json_str = json.dumps(kanji.__dict__, default=lambda obj: obj.__dict__)
            file.write(json_str)
            file.write('\n')
        file.close()

            

parse()