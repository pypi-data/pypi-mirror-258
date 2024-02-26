# -*- coding:utf-8 -*-

import re
import xml.etree.ElementTree as ET
from typing import Callable

from .config import Settings, ConverterConfig, Voice, RunMode
from .units import Tools
import sys
import copy

class TextParagraph(object):
    _text:str
    _length:int
    _voice:Voice

    def __init__(self, text:str) -> None:
        self._text = text
        self._length = len(text)


    def update(self, text:str):
        self._text = text
        self._length = len(text)

    @property
    def text(self) -> str:
        return self._text

    def getVoice(self) -> Voice:
        return self._voice


class TextEditor(object):
    text = []
    __text_limit = Settings.text_limit
    __elastic_value = Settings.elastic_value
    _support_file_type = Settings.support_file_type

    __notice_value_update: Callable[[dict], None] = None
    config:ConverterConfig = None

    def __init__(self, text:list, config:ConverterConfig = None) -> None:
        self.text = text

        # if callback != None:
        #     self.__notice_value_update = callback
        if config != None: 
            self.config = config

    def _check_reserved_word(self, text:str) -> str:
        if '"' in text:
            # print("[DEBUG] Find reserved_word " + '"')
            text = text.replace('"', "&quot;")
        if '&' in text:
            # print("[DEBUG] Find reserved_word " + '&')
            text = text.replace('&', "&amp;")
        if "'" in text:
            # print("[DEBUG] Find reserved_word " + "'")
            text = text.replace("'", "&apos;")
        if '<' in text:
            # print("[DEBUG] Find reserved_word " + '<')
            text = text.replace('<', "&lt;")
        if '>' in text:
            # print("[DEBUG] Find reserved_word " + '>')
            text = text.replace('>', "&gt;")
        return text


    def _count_reserved_word(self, text:str) -> int:
        count = 0
        reserved_word_list = [r'"', r'&', r"'", r'<', r'>']
        for key_word in reserved_word_list:
            count += len(re.findall(key_word, text))

        return count*6


    def _check_text_length(self, text:str) -> list:
        """
        檢查傳入的文字有沒有超出限制，如果超出限制會以標點符號分割字串
        """
        limit = self.__text_limit
        result = []
        text_length = len(text)
        split_position = limit

        if self.config.get_run_mode() == RunMode.LIVE_PLAY_AUDIO:
            result = self.live_play_split_symbol(text, text_length, limit)
        else:
            result = self.normal_split_symbol(text, split_position, limit)

        return result

    def live_play_split_symbol(self, text, text_length, limit):
        result = []
        punctuation = ['。', '.',  '！', '!', '？', '?', '\n', '\t', '，', ',', '、', '　', '（', '）', '；']
        text_length = len(text)
        start_split_flag = 0
        end_split_flag = 0

        for i in range(text_length):
            count = end_split_flag - start_split_flag + 1
            current_text = text[start_split_flag: end_split_flag + 1].strip().replace('\n', '').replace('\t', '')

            if text[i] in punctuation and count >= 10:
                if current_text.strip() != "":
                    result.append(TextParagraph(current_text))
                    start_split_flag = end_split_flag + 1
            elif count > limit:
                if current_text.strip() != "":
                    result.append(TextParagraph(current_text))
                    start_split_flag = end_split_flag + 1

            end_split_flag += 1

            if end_split_flag == text_length and start_split_flag != end_split_flag:
                if current_text.strip() != "":
                    # print(f"test3 result: {current_text} {len(current_text)}")
                    result.append(TextParagraph(current_text.strip()))

        return result

    def normal_split_symbol(self, text, split_position, limit) -> list:
        result = []
        punctuation = ['。', '！', '!', '？', '?', '\n', '\t', '，', ',', '、', '　', ' ', '（', '）', '(', ')', '「', '」', '；', '﹔']
        text_length = len(text)
        reserved_lenth = 0
        merge_start_position = 0

        while(split_position < text_length):
            reserved_lenth = self._count_reserved_word(text[merge_start_position:split_position])
            if reserved_lenth >= limit:
                raise ValueError("Use too much reserved word.")

            split_position -= reserved_lenth
            # 從分割點開始向前尋找標點符號
            for i in range(split_position-1, merge_start_position, -1):
                if text[i] in punctuation:
                    split_position = i
                    break

            # 分段儲存文字
            # result.append(text[merge_start_position:split_position])
            result.append(TextParagraph(text[merge_start_position:split_position]))
            # 實際分割點(標點符號位置)設為新分割點
            merge_start_position = split_position

            split_position += limit

        # result.append(text[merge_start_position:])
        if self._count_reserved_word(text[merge_start_position:]) > self.__elastic_value: # elastic_value = 200
            raise ValueError("Use too much reserved word.")

        result.append(TextParagraph(text[merge_start_position:]))

        return result


    def _add_void_name(self, name:str, text: str):
        return f'<voice name=\'{name}\'>{text}</voice>'

    def _add_phoneme(self, text:str, ph:str):
        # print(f"_add_phoneme: {text}")
        """
        text：加入的文字\n
         ph ：指定的發音
        """

        alphabet = "bopomo"
        lang = "TW"
        return f'<phoneme alphabet="{alphabet}" lang="{lang}" ph="{ph}">{text}</phoneme>'


    def _add_break(self, break_time:int):
        """
        break_time：停頓的時間 (最大值為5000，單位ms)\n
        若輸入值大於上限值，以最大值替代
        """

        if break_time > 5000:
            if Settings.print_log:
                print("[DEBUG] Out of range, break_time max value = 5000")
            break_time = 5000
        return f'<break time="{break_time}ms"/>'


    def _add_prosody(self, text:str, rate:float, pitch:int, volume:float):
        """
        rate    : 調整語速, 最小值=0.8, 最大值=1.2\n
        pitch   : 調整音調, 最小值=-2, 最大值=2\n
        volume  : 調整音量, 最小值=-6, 最大值=6\n
        若輸入超過範圍值，皆以最大/最小值替代
        """
        tag_rate = ' rate="1.0"'
        tag_pitch = ""
        tag_volume = ""

        rate_max = 1.2
        rate_min = 0.8
        rate_default = 1.0
        pitch_max = 2
        pitch_min = -2
        pitch_default = 0
        volume_max = 6.0
        volume_min = -6.0
        volume_default = 0.0


        if type(pitch) != int:
            # print("[DEBUG] Pitch type wrong")
            pitch = int(pitch)

        if rate != rate_default:
            if rate > rate_max:
                # print("[DEBUG] Rate out of range, use the maximum to translate.")
                tag_rate = f' rate="{rate_max}"'
            elif rate < rate_min:
                # print("[DEBUG] Rate out of range, use the minimum to translate.")
                tag_rate = f' rate="{rate_min}"'
            else:
                tag_rate = f' rate="{rate}"'

        if pitch != pitch_default:
            if pitch > pitch_max:
                # print("[DEBUG] Pitch out of range, use the maximum to translate.")
                tag_pitch = f' pitch="+{pitch_max}st"'
            elif pitch < pitch_min:
                # print("[DEBUG] Pitch out of range, use the minimum to translate.")
                tag_pitch = f' pitch="{pitch_min}st"'
            else:
                if pitch > 0:
                    tag_pitch = f' pitch="+{pitch}st"'
                else:
                    tag_pitch = f' pitch="{pitch}st"'

        if volume != volume_default:
            if volume > volume_max:
                # print("[DEBUG] Volume out of range, use the maximum to translate.")
                tag_volume = f' volume="+{volume_max}dB"'
            elif volume < volume_min:
                # print("[DEBUG] Volume out of range, use the minimum to translate.")
                tag_volume = f' volume="{volume_min}dB"'
            else:
                if volume > 0:
                    tag_volume = f' volume="+{volume}dB"'
                else:
                    tag_volume = f' volume="{volume}dB"'

        return f'<prosody{tag_rate}{tag_pitch}{tag_volume}>{text}</prosody>'


    def _get_ssml_all_tags(self, element:ET.Element, layer = 1) -> list:
        """
        element: 套件解析後的element tree\n
        layer: 第幾層的節點(default layer = 1)
        """
        ssml_tags:list = [] # [layer, tag, attrib, text]
        tag:str = element.tag[element.tag.rfind('}')+1:]
        text:str = ""

        if element.text:
            text = element.text

        # Add ssml tag to list
        ssml_tags.append({"layer": layer, "tag": tag, "attrib": element.attrib, "text": text})

        for child in element:
            ssml_tags += self._get_ssml_all_tags(child, layer+1)
            if child.tail:
                ssml_tags.append({"layer": layer, "tag": "tail", "attrib": None, "text": child.tail})

        return ssml_tags



    def _ssml_tag_to_text(self, ssml_tag:dict) -> str:
        if ssml_tag['tag'] == "voice":
            return ssml_tag['text']
        elif ssml_tag['tag'] == "phoneme":
            return self._add_phoneme(ssml_tag['text'], ssml_tag['attrib']['ph'])
        elif ssml_tag['tag'] == "break":
            return self._add_break(int(ssml_tag['attrib']['time'][:-2]))
        elif ssml_tag['tag'] == "prosody":
            return self._add_prosody(ssml_tag['text'], float(ssml_tag['attrib']['rate']), \
                                     int(ssml_tag['attrib']['pitch'][:-2]), float(ssml_tag['attrib']['volume'][:-2]))
        elif ssml_tag['tag'] == "tail":
            return ssml_tag['text']
        else:
            return ""

    def _parse_voice_tag(self, ssml_tag_list:list):
        result = []
        is_found_voice_tag = False
        for tag in ssml_tag_list:
            if tag['tag'] == 'voice':
                is_found_voice_tag = True
                tag['tag'] = '<voice>'
                result.append({
                    'voice': [tag]
                })
            elif tag['layer'] != 1 and tag['layer'] != 2 \
                and is_found_voice_tag == True:

                result[len(result)-1]['voice'].append(tag)
            elif tag['layer'] == 2 and tag['tag'] == 'tail':
                is_found_voice_tag = False
                tag['tag'] = '</voice>'
                result[len(result)-1]['voice'].append(tag)

        return result

    def _parse_voice_info(self, voice_name:str, ssml_text:str):
        return f'<voice name="{voice_name}">{ssml_text}</voice>'
        
    def _format_ssml_text(self, ssml_element:ET.Element) -> list:
        is_live_play_mode = self.config.get_run_mode() == RunMode.LIVE_PLAY_AUDIO
        limit = 10 if is_live_play_mode else self.__text_limit

        ssml_tag_list = self._get_ssml_all_tags(ssml_element, 1)
        # print(f"ssml_tag_list: {ssml_tag_list}")
        text_list = []

        count = 0

        voice_tags = []
        for tag in ssml_tag_list:

            if tag['tag'] == "voice":
                voice_tags.append({"voice_name": tag['attrib']['name'], "ssml_tags": []})

            # 檢查文字長度，同時檢查保留字，並存為新的text list
            text_paragraph_list = self._check_text_length(tag['text'])
            if tag['tag'] == 'break':
                voice_tags[len(voice_tags)-1]['ssml_tags'].append({"layer": tag['layer'], "tag": tag['tag'], "attrib":tag['attrib'], "text": ""})
            for text in text_paragraph_list:
                temp_text = text._text.strip()
                if temp_text != "":
                    voice_tags[len(voice_tags)-1]['ssml_tags'].append({"layer": tag['layer'], "tag": tag['tag'], "attrib":tag['attrib'], "text": self._check_reserved_word(temp_text)})

        # ===================
        # for tag in voice_tags:
        #     print("CCC", tag)

        for voice_tag in voice_tags:

            # 更新voice要新增一個
            text_list.append("")
            # print("CCCC", voice_tag['voice_name'], voice_tag['ssml_tags'], len(voice_tag['ssml_tags'])-1)
            length = 0
            i = 0
            is_prosody = False
            prosody_layer = 1
            prosody_tag_info = ""
            is_add_font = False
            has_break_time = False
            break_time_tag = ""

            for i in range(len(voice_tag['ssml_tags'])-1):
                ssml_text = self._ssml_tag_to_text(voice_tag['ssml_tags'][i])
                ssml_text = ssml_text.strip() if is_live_play_mode else ssml_text

                if is_live_play_mode:
                    if i < len(voice_tag['ssml_tags'])-1 and voice_tag['ssml_tags'][i]['tag'] == "break":
                        is_add_font = True
                        break_time_tag = f"<break time=\"{voice_tag['ssml_tags'][i]['attrib']['time']}\"/>"
                        has_break_time = True
                        continue
                    elif i+1 == len(voice_tag['ssml_tags'])-1 and voice_tag['ssml_tags'][i+1]['tag'] == "break":
                        is_add_font = False
                        break_time_tag = f"<break time=\"{voice_tag['ssml_tags'][i]['attrib']['time']}\"/>"
                        has_break_time = True
                    elif i == len(voice_tag['ssml_tags']) and voice_tag['ssml_tags'][i]['tag'] == "break":
                        continue

                if voice_tag['ssml_tags'][i]['tag'] == "prosody":
                    # 偵測到prosody tag，針對prosody情境處裡tag
                    is_prosody = True

                    prosody_layer = voice_tag['ssml_tags'][i]['layer']
                    # print(f"ssml_text.rfind(</prosody: {ssml_text.rfind('</prosody')}")
                    ssml_text = ssml_text[:ssml_text.rfind("</prosody")] # remove '</prosody>'
                    prosody_tag_info = ssml_text[:ssml_text.find(">")+1]
                    # print("--> start", prosody_start_tag)
                if is_live_play_mode and has_break_time == True:
                    if is_add_font == True:
                        ssml_text = break_time_tag + ssml_text
                    else:
                        ssml_text = ssml_text + break_time_tag
                    has_break_time = False

                length += len(ssml_text)
                text_list[count] += ssml_text


                if is_prosody == True:
                    if voice_tag['ssml_tags'][i+1]['layer'] <= prosody_layer:
                        if (voice_tag['ssml_tags'][i+1]['layer'] == prosody_layer) and (voice_tag['ssml_tags'][i+1]['tag'] == "tail"):
                            pass
                        else:
                            # 偵測prosody tag結尾
                            is_prosody = False
                            prosody_tag_info = ""
                            # print("--> add end tad </prosody>")
                            length += len("</prosody>")
                            text_list[count] += "</prosody>"

                if length + len(self._ssml_tag_to_text(voice_tag['ssml_tags'][i+1])) > limit:
                    if ("<phoneme" in ssml_text) and is_live_play_mode:
                        # print("NOT NEW ONE")
                        pass
                    else:
                        # Add new text element
                        text_list.append("")
                        count += 1
                        length = 0

                        # Add prosody end tag to previous text
                        if is_prosody == True:
                            text_list[count-1] += "</prosody>"
                            text_list[count] += prosody_tag_info # Add prosody header tag
                        # ========================================

                        text_list[count-1] = self._parse_voice_info(voice_tag['voice_name'], text_list[count-1])


            if len(voice_tag['ssml_tags']) > 1:
                i += 1

            end_symbol = ""
            if is_prosody == True:
                end_symbol = "</prosody>"

            last_text = self._ssml_tag_to_text(voice_tag['ssml_tags'][i])
            if length + len(last_text) > limit:
                if is_live_play_mode:
                    text_list[count] = prosody_tag_info + last_text + end_symbol
                else:
                    text_list[count] += end_symbol
                    text_list.append((prosody_tag_info + last_text + end_symbol))
            else:
                text_list[count] = text_list[count] + last_text + end_symbol

            # print("CCC", voice_tag['ssml_tags'][i], i)
            count += 1
            # add voice tag
            text_list[count-1] = self._parse_voice_info(voice_tag['voice_name'], text_list[count-1])

        return text_list


    # ---------- Text ----------
    def add_text(self, text:str, position = -1):
        """
        text：加入的文字\n
        position：文字加入的位置，position = -1 或大於段落總數時會加在最後\n
        """
        if type(position) != int:
            raise TypeError("Parameter 'position(int)' type error.")
        if type(text) != str:
            raise TypeError("Parameter 'text(str)' type error.")

        
        
        text_list = self._check_text_length(text)

        if position == -1:
            position = len(self.text) + 1

        for text_each in text_list:
            new_text= self._check_reserved_word(text_each._text)
            new_text = self._add_void_name(self.config.get_voice(), new_text)
            text_each.update(new_text)

        self.text[position:position] = text_list

    
    def add_webpage_text(self, text:str, rate:float = 1.0, pitch:int = 0, volume:float = 0.0, position = -1):
        """
        text    : 加入的文字\n
        rate    : 調整語速, 最小值=0.8, 最大值=1.2\n
        pitch   : 調整音調, 最小值=-2, 最大值=2\n
        volume  : 調整音量, 最小值=-6, 最大值=6\n
        若輸入超過範圍值，皆以最大/最小值替代\n
        position：文字加入的位置，position = -1 或大於段落總數時會加在最後\n
        """
        if type(position) != int:
            raise TypeError("Parameter 'position(int)' type error.")
        if type(text) != str:
            raise TypeError("Parameter 'text(str)' type error.")
        if type(rate) != float:
            raise TypeError("Parameter 'rate(float)' type error.")
        if type(pitch) != int:
            raise TypeError("Parameter 'pitch(int)' type error.")
        if type(volume) != float:
            raise TypeError("Parameter 'volume(float)' type error.")

        if position == -1:
            position = len(self.text) + 1

        text_list = self._check_text_length(text)

        limit = self.__text_limit
        count = 0
        for text_each in text_list:
            text_each.update(self._check_reserved_word(text_each._text))

            tags = [(match.start(), match.end()) for match in re.finditer(r'\[:(.*?)\]', text_each._text)]
            length = len(text_each._text)
            for tag in tags:
                if text_each._text[tag[1]-2] == "秒":
                    length += 15 # ssml break tag 長度最大為22 比原本多15
                else:
                    length += 51 # ssml break tag 長度最大(單一文字)為58 比原本多51

                if length > limit:
                    text_list[count+1:count+1] = [TextParagraph(text_each._text[tag[1]:])]
                    text_each._text = text_each._text[:tag[1]]
                    break

            # rematch
            shift = 0
            new_tag = ""
            new_text = text_each._text
            for rematch in re.finditer(r'\[:(.*?)\]', text_each._text): # 作用與 for tag in tags: 相同
                if text_each._text[rematch.end()-2] == "秒":
                    break_time = float(text_each._text[rematch.start()+2:rematch.end()-2]) * 1000
                    new_tag = self._add_break(int(break_time))
                    new_text = new_text[:rematch.start()+shift] + new_tag + new_text[rematch.end()+shift:]
                else:
                    if text_each._text[rematch.start()-1] == ']':
                        new_tag = ""
                        continue
                    word = text_each._text[rematch.start()-1]
                    ph = text_each._text[rematch.start()+2:rematch.end()-1]
                    new_tag = self._add_phoneme(word, ph)
                    new_text = new_text[:rematch.start()+shift-1] + new_tag + new_text[rematch.end()+shift:]
                    shift -= 1
                shift += len(new_tag) - rematch.end() + rematch.start()

            text_each.update(self._add_prosody(new_text, rate, pitch, volume))
            text_each._text = self._add_void_name(self.config.get_voice(), text_each._text)
            count += 1

        self.text[position:position] = text_list


    def add_ssml_text(self, text:str, position = -1):
        """
        text：加入的文字\n
        position：文字加入的位置，position = -1 或大於段落總數時會加在最後
        """
        if type(position) != int:
            raise TypeError("Parameter 'position(int)' type error.")
        if type(text) != str:
            raise TypeError("Parameter 'text(str)' type error.")

        ssml_element:ET.Element
        try:
            ssml_element = ET.fromstring(text)
        except Exception as error:
            if type(error) == ET.ParseError:
                raise ValueError(f"Ssml string {error}")
            else:
                raise RuntimeError(f"Read ssml string fail.")

        ssml_text = self._format_ssml_text(ssml_element)
        text_list = []

        if position == -1:
            position = len(self.text) + 1

        for text in ssml_text:
            text_list.append(TextParagraph(text))

        self.text[position:position] = text_list


    def get_text(self) -> list:
        """
        獲得文章清單
        """
        if len(self.text) < 1:
            print("Text is empty.")

        result = []
        for text_each in self.text:
            result.append(text_each._text)
        return result


    def show(self):
        """
        顯示文章清單
        """
        if len(self.text) < 1:
            print("Text is empty.")

        for i in range(len(self.text)):
            print(f"{i:^3}: {self.text[i]._text}")


    def delete_paragraph(self, position:int) -> bool:
        """
        position：要刪除的段落
        return：[True, False]
        """
        if type(position) != int:
            raise TypeError("Parameter 'position(int)' type error.")

        text_length = len(self.text)
        if text_length == 0:
            print("Text is enpty.")
            return True

        if text_length <= position:
            raise ValueError("Parameter 'position(int)' value more than number of sentences.")

        del self.text[position]
        return True


    def clear(self):
        """
        清除文章所有內容
        """
        self.text.clear()


    def insert_phoneme(self, text:str, ph:str, position = -1):
        """
        text：加入的文字\n
         ph ：指定的發音\n
        position：文字加入的位置，position = -1 或大於段落總數時會加在最後\n
        """
        if type(position) != int:
            raise TypeError("Parameter 'position(int)' type error.")
        if type(text) != str:
            raise TypeError("Parameter 'text(str)' type error.")
        if type(ph) != str:
            raise TypeError("Parameter 'ph(str)' type error.")

        text_list = self._check_text_length(text)

        if position == -1:
            position = len(self.text) + 1

        for text_each in text_list:
            text_each.update(self._add_phoneme(\
                             self._check_reserved_word(text_each._text), ph))

        self.text[position:position] = text_list


    def insert_break(self, break_time:int, position = -1):
        """
        break_time：停頓的時間 (最大值為5000，單位ms)\n
        若輸入值大於上限值，以最大值替代\n
        position：文字加入的位置，position = -1 或大於段落總數時會加在最後\n
        """
        if type(position) != int:
            raise TypeError("Parameter 'position(int)' type error.")
        if type(break_time) != int:
            raise TypeError("Parameter 'break_time(int)' type error.")

        if position == -1:
            position = len(self.text) + 1

        self.text.insert(position, TextParagraph(self._add_break(break_time)))


    def insert_prosody(self, text:str, rate:float = 1.0, pitch:int = 0, volume:float = 0.0, position = -1):
        """
        rate    : 調整語速, 最小值=0.8, 最大值=1.2\n
        pitch   : 調整音調, 最小值=-2, 最大值=2\n
        volume  : 調整音量, 最小值=-6, 最大值=6\n
        若輸入超過範圍值，皆以最大/最小值替代\n
        position：文字加入的位置，position = -1 或大於段落總數時會加在最後\n
        """
        if type(position) != int:
            raise TypeError("Parameter 'position(int)' type error.")
        if type(text) != str:
            raise TypeError("Parameter 'text(str)' type error.")
        if type(rate) != float:
            raise TypeError("Parameter 'rate(float)' type error.")
        if type(pitch) != int:
            raise TypeError("Parameter 'pitch(int)' type error.")
        if type(volume) != float:
            raise TypeError("Parameter 'volume(float)' type error.")

        text_list = self._check_text_length(text)

        if position == -1:
            position = len(self.text) + 1

        for text_each in text_list:
            text_each.update(
                self._add_void_name(
                    self.config.get_voice(),
                    self._add_prosody(self._check_reserved_word(text_each._text), rate, pitch, volume)
                )
            )

        self.text[position:position] = text_list


    def insert_prosody_and_phoneme(self, text:str, ph:str, \
                                   rate:float = 1.0, pitch:int = 0, volume:float = 0.0, position = -1):
        """
        text：需要修改發音的文字\n
         ph ：指定的發音\n
        rate    : 調整語速, 最小值=0.8, 最大值=1.2\n
        pitch   : 調整音調, 最小值=-2, 最大值=2\n
        volume  : 調整音量, 最小值=-6, 最大值=6\n
        若輸入超過範圍值，皆以最大/最小值替代\n
        position：文字加入的位置，position = -1 或大於段落總數時會加在最後\n
        """
        if type(position) != int:
            raise TypeError("Parameter 'position(int)' type error.")
        if type(text) != str:
            raise TypeError("Parameter 'text(str)' type error.")
        if type(ph) != str:
            raise TypeError("Parameter 'ph(str)' type error.")
        if type(rate) != float:
            raise TypeError("Parameter 'rate(float)' type error.")
        if type(pitch) != int:
            raise TypeError("Parameter 'pitch(int)' type error.")
        if type(volume) != float:
            raise TypeError("Parameter 'volume(float)' type error.")

        text_list = self._check_text_length(text)

        if position == -1:
            position = len(self.text) + 1

        for text_each in text_list:
            text_each.update(
                self._add_void_name(
                    self.config.get_voice(),
                    self._add_prosody(self._add_phoneme(self._check_reserved_word(text_each._text), ph), rate, pitch, volume)
                )
            )
        self.text[position:position] = text_list


    def open_text_file(self, file_path:str, encode = "utf-8", position = -1):
        """
        file_path：檔案路徑\n
         encode：檔案編碼格式\n
        position：文字加入的位置，position = -1 或大於段落總數時會加在最後\n
        """
        if type(position) != int:
            raise TypeError("Parameter 'position(int)' type error.")

        extension = file_path[file_path.rfind('.'):]
        if extension in self._support_file_type == False:
            raise TypeError(f"Not support '{extension}' type.")

        text = Tools().open_file(file_path, encode)

        if extension == ".ssml" or extension == ".xml":
            self.add_ssml_text(text, position)
        else:
            self.add_text(text, position)
