import json
import time
import copy
import threading
import wave
import sys
import re

import simpleaudio as sa

import io

from .enums import ConverterStatus, Voice, RunMode
from .config import ConverterConfig, Settings
from .textedit import TextEditor
from .units import RestfulApiHandler, Tools, Calculator


status_and_error_codes = {
    200: '成功',

    40101: 'jwt token 過期',
    40102: 'jwt token 無法解析',
    40103: 'email 存在，但密碼錯誤',
    40104: '使用者不在訂單區間中',

    40301: '沒有使用此 model 的權限',

    42201: '參數內容錯誤',
    42202: '送來的檔案非 jpg, jpeg, png, 或檔案過大',
    42203: '缺少 authorization header',
    42204: '所選擇的 synthesis 非 processing or waiting',
    42205: '所選擇的 synthesis 非 error',
    42206: '所選擇的 synthesis 非 success or error',
    42207: '超過單次合成字數',
    42208: '超過一個月可合成的字數',
    42209: '超過可保留的合成紀錄數',
    42210: '目前在隊列內或合成中的任務已達到上限',
    42211: '超過可保留的草稿紀錄數',
    42212: 'ssml 格式錯誤',

    40401: 'user id 不存在',
    40402: 'jwt token 不存在',
    40403: 'draft 不存在',
    40404: 'synthesis 不存在',
    40405: 'order num 不存在',
    40406: 'model 不存在',

    40901: 'order num 重複新增',
    40902: 'user 已經註冊，但尚未認證',
    40903: 'user 已經註冊，且認證完畢',

    50001: 'server 發生未知錯誤',

    50301: '寄 email 發生錯誤',
    50302: '資料庫發生錯誤',
}


class ConverterResult(object):
    """
    status：轉換器的狀態\n
    data：[{"id": (int)task_id, "data": (byte)auido_data}]\n
    detail：結果說明\n
    error_msg：error message
    """
    status:ConverterStatus
    task_data = [] # [{"id": (int)task_id, "data": (byte)auido_data}]
    detail:str
    error_message:str
    

    def __init__(self, status:ConverterStatus, data, detail, error_msg) -> None:
        self.status = status
        self.task_data = data
        self.detail = detail
        self.error_message = error_msg

    def save(self, filename = "aivoice", is_merge = False) -> None:
        """
        filename：檔案名稱，預設為'aivoice'\n
        is_merge：如果音檔數量超過一個，是否將其合併為一個檔案\n
        """
        task_list_length = len(self.task_data)
        if task_list_length > 0:
            if is_merge and (task_list_length > 1):
                audio_data = []
                for each_data in self.task_data:
                    audio_data.append(each_data['data'])
                Tools().merge_wav_file(filename, audio_data)
            else:
                count = 1
                for each_data in self.task_data:
                    file_number = "-" + str(count)
                    if task_list_length == 1:
                        file_number = ""

                    if each_data['data'] != None:
                        Tools().save_wav_file(filename + file_number, each_data['data'])
                    count += 1

class LivePlayAudioTask:
    _is_finished:bool = False
    _data = None

    def __init__(self, is_finished, data):
        self._is_finished = is_finished
        self._data = data

    def get_is_finished(self):
        return self._is_finished

    def get_data(self):
        return self._data

class VoiceConverter(object):
    config:ConverterConfig
    text:TextEditor
    _api_handler:RestfulApiHandler
    _model:RunMode = None

    _text = []

    _task_list = [] # [{"id": "0~XX", "text": "paragraphs", "token": ""}]
    _each_task_text_limit = Settings.each_task_text_limit

    _live_get_speech_event = None
    _live_play_audio_event = None
    _live_get_speech_thread = None
    _live_play_audio_thread = None
    _live_get_speech_error_flg = {}
    _live_play_audio_error_flg = {}
    _live_play_audio_queue = []
    _live_play_audio_task = []

    def __init__(self, config = ConverterConfig()):
        self.config = copy.deepcopy(config)
        self._api_handler = RestfulApiHandler(self.config)

        self._model = config.get_run_mode()
        self.set_config_callback()
        self.text = TextEditor(self._text, self.config)

    def set_config_callback(self):
        self.config.set_update_config_callback(self._run_model_change)

    def _translate_result_code(self, result_json:json) -> str:
        code = result_json['data']['error_code']
        if code in status_and_error_codes:
            if Settings.print_log:
                print(f"[ERROR] {status_and_error_codes[code]} (Error code: {code})")
            return status_and_error_codes[code]
        else:
            if Settings.print_log:
                print(f"[ERROR] Get server not define error code. (Error code: {code})\nMessage: {result_json['data']}")
            return result_json['data']

    def insert_break_time(self, text, break_time, is_last):
        updated_text = ""
        if is_last == False:
            pattern = r'(<voice name="[^"]+">.*?)(?=<)'
            match = re.search(pattern, text)

            if match:  # 如果找到了匹配的 <voice> 元素及其之后的文本
                # 获取匹配的文本
                voice_and_following_text = match.group(1)

                # 在匹配的文本之后插入 <break> 元素
                updated_text = voice_and_following_text + break_time + text[match.end(1):]
        else:
            pattern = r'</voice>'
            replacement = f'<break time="{break_time}ms"/></voice>'
            updated_text = re.sub(pattern, replacement, text)

        return updated_text

    def check_break_element(self, text):
        # 定義正則表達式模式
        pattern = r'^\s*<break\s+time="[^"]+"\s*/>\s*$'

        # 使用正則表達式進行匹配
        match = re.match(pattern, text)

        # 檢查匹配結果
        if match:
            return True
        else:
            return False

    def _create_task_list(self):
        # task_list = [{"id": "123", "text": "msg", "token": ""}, {"id": "456", "text": "msgg", "token": ""}, {"id": "789", "text": "msggg", "token": ""}]
        self._task_list.clear()
        self._live_play_audio_task.clear()
        self._live_play_audio_queue.clear()
        self._live_get_speech_error_flg = {"error": False, "error_msg": ""}
        self._live_play_audio_error_flg = {"error": False, "error_msg": ""}

        count = 0
        is_found_break = False
        break_time = ""
        for i in range(0, len(self._text)):
            temp_text = self._text[i].text
            # print(f"temp_text: {temp_text}")
            if (i != len(self._text) - 1) and self.check_break_element(temp_text):
                # print(f"1........")
                is_found_break = True
                break_time = temp_text
                continue
            elif (i == len(self._text) - 1) and self.check_break_element(temp_text):
                # print(f"2........")
                temp_text = self._text[i-1].text
                temp_text = self.insert_break_time(temp_text, break_time, True)
            if is_found_break == True:
                # print(f"3........")
                temp_text = self.insert_break_time(temp_text, break_time, False)
                is_found_break = False

            # print(f"temp_text: {temp_text}")
            if self.config.get_run_mode() == RunMode.LIVE_PLAY_AUDIO:
                self._task_list.append({"id": "", "text": temp_text})
            else:
                if i == 0:
                    self._task_list.append({"id": "", "text": "", "token": ""})

                if len(self._task_list[count]['text'] + temp_text) > self._each_task_text_limit:
                    self._task_list.append({"id": "", "text": "", "token": ""})
                    count += 1
                self._task_list[count]['text'] = self._task_list[count]['text'] + temp_text

            self._live_play_audio_task.append({"id": "", "status": "Ready", "data": ""})

    # ---------- Config ----------

    def _voice_value_to_name(self, voice_value):
        for vo in Voice:
            if voice_value == vo.value:
                return vo

    def _run_model_change(self, value:dict):
        if 'runModel' in value and value['runModel'] == RunMode.LIVE_PLAY_AUDIO:
            self.text.clear()

    def update_config(self, config:ConverterConfig):
        """
        config：轉換器設定檔
        """
        if type(config) != ConverterConfig:
            raise TypeError("Parameter 'config(ConverterConfig)' type error.")

        self.config.set_tokens(config.get_tokens())
        self.config.set_server(config.get_server())
        self.config.set_voice(config.change_voice_value_to_name(config.get_voice()))


    # ---------- Task infomation ----------
    def get_task_list(self) -> list:
        result = []
        if len(self._task_list) < 1:
            print("[INFO] Task list is empty.")
            return result

        for task in self._task_list:
            result.append({"id": task['id'],"text": task['text']})
        return result


    def _init_threads(self):
        self._live_get_speech_event = threading.Event()
        self._live_play_audio_event = threading.Event()
        self._live_get_speech_thread = threading.Thread(target=self._run_live_get_speech, args=(self._live_get_speech_event,))
        self._live_play_audio_thread = threading.Thread(target=self._run_live_play_audio_task, args=(self._live_play_audio_event,))
        self._live_get_speech_thread.daemon = True
        self._live_play_audio_thread.daemon = True
        self._live_get_speech_thread.start()
        self._live_play_audio_thread.start()

    # ---------- Live get speech ----------
    def _run_live_get_speech(self, event):
        count = 0
        interval_time = Calculator().second_to_millisecond(100)
        try:
            while True:
                while len(self._live_play_audio_queue) > 0:
                    index = self._live_play_audio_queue[count]['index']

                    result_json = self._api_handler.get_task_status(
                        self._live_play_audio_queue[count]['id'], self._task_list[index]['token'])

                    task_status = result_json['data']['status']
                    if task_status == 'Success':
                        self._live_play_audio_task[index]['data'] = \
                            self.get_speech_by_id(self._live_play_audio_queue[count]['id'], self._task_list[index]['token'])
                        self._live_play_audio_task[index]['status'] = 'Success'
                        self._live_play_audio_queue.pop(0)
                    elif task_status == 'Error':
                         raise Exception(f"synthesis error")
                if event.is_set():
                    break
                time.sleep(interval_time)
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as error:
            self._live_get_speech_error_flg["error"] = True
            self._live_get_speech_error_flg["error_msg"] = error


    # ---------- Live play audio ----------
    def _run_live_play_audio_task(self, event):
        task_number = len(self._live_play_audio_task)
        count = 0
        interval_time = Calculator().second_to_millisecond(100)

        try:
            # print(f"count: {count}, task_number: {task_number}")
            while count < task_number:
                # print(f"thread running count: {count}...")
                # print(f"{count} thread status: {self._live_play_audio_task[count]['status']}")
                if self._live_play_audio_task[count]['status'] == 'Success':
                    # print("test1")
                    raw_data = self._live_play_audio_task[count]['data']

                    with io.BytesIO(raw_data) as stream:
                        with wave.open(stream, 'rb') as wf:
                            format_info = {
                                'num_channels': wf.getnchannels(),
                                'bytes_per_sample': wf.getsampwidth(),
                                'sample_rate': wf.getframerate()
                            }

                    wave_obj = sa.WaveObject(raw_data, format_info['num_channels'],
                                             format_info['bytes_per_sample'],
                                             format_info['sample_rate'])
                    play_obj = wave_obj.play()
                    play_obj.wait_done()

                    count += 1
                if event.is_set():
                    break
                time.sleep(interval_time)

        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as error:
            self._live_play_audio_error_flg["error"] = True
            self._live_play_audio_error_flg["error_msg"] = error
        finally:
            self._live_get_speech_event.set()


    # ---------- Task ----------
    def run(self, interval_time = 0, is_wait_speech = False) -> ConverterResult:
        """
        interval_time：伺服器忙碌時，重試合成任務間隔時間，interval_time為毫秒，最小值=0 (不重試)，最大值=10000\n
        is_wait_speech：是否等待下載完整語音，True=執行後會等待下載完整語音，Result與(func)get_speech相同
        """
        if type(interval_time) != int:
            raise TypeError("Parameter 'wait_time(int)' type error.")
        if (interval_time < 0) or (interval_time > 10000):
            raise ValueError("Parameter 'wait_time(int)' value error.")


        interval_time = Calculator().second_to_millisecond(interval_time)
        if len(self._text) < 1:
            raise ValueError("Text is empty.") # TODO 改return result?

        self._create_task_list()

        status = ConverterStatus.ConverterStartUp
        task_data = []
        detail = ""
        error_msg = ""

        task_number = len(self._task_list)
        task_count = 0
        task_status = 'None'
        result_json = {}

        tokens_queue = copy.deepcopy(self.config.get_tokens())

        current_task_queue = []

        is_live_play = self.config.get_run_mode()
        if is_live_play == RunMode.LIVE_PLAY_AUDIO:
            self._init_threads()

        status = ConverterStatus.ConverVoiceStart
        while task_count < task_number and \
            not self._live_get_speech_error_flg['error'] and \
                not self._live_play_audio_error_flg['error']:

            task = self._task_list[task_count]

            task['token'] = tokens_queue[0]
            status = ConverterStatus.ConverVoiceRunning
            detail = f"(Start Convert: {task_count + 1}/{task_number})"
            result_json = self._api_handler.add_ssml_task(task['text'], task['token'])
            task_status = 'None'

            if result_json['code'] != 422:
                task['id'] = result_json['data']['synthesis_id']

                # task in queue
                current_task_queue.append(task['id'])

                # live play mode
                self._live_play_audio_queue.append({'id': task['id'], 'index': task_count})
                self._live_play_audio_task[task_count]['status'] = 'Get_Speech'
                self._live_play_audio_task[task_count]['id'] = task['id']

                task_count += 1
            else:
                if result_json['data']['error_code'] != 42210:
                    status = ConverterStatus.ConverVoiceFail
                    task_status = 'Error'
                    error_msg = f"{self._translate_result_code(result_json)} (In process {task_count}/{task_number})"
                    break

                # multi token will skip "task in queue" function
                if len(tokens_queue) > 1:
                    tokens_queue.append(tokens_queue.pop(0))
                    continue

                count = 0
                while task_status != 'Success' and task_status != 'Error' and len(current_task_queue) > 0:
                    result_json = self._api_handler.get_task_status(current_task_queue[count], task['token'])
                    task_status = result_json['data']['status']

                    if task_status == 'Success':
                        status = ConverterStatus.ConverVoiceCompleted
                        current_task_queue.pop(count)
                    count += 1
                    if count >= len(current_task_queue):
                        count = 0
            
            # 檢查current_task_queue裡面的任務是否成功
            if task_count == task_number:
                while len(current_task_queue) > 0:
                    result_json = self._api_handler.get_task_status(current_task_queue[0], task['token'])
                    task_status = result_json['data']['status']
                    if task_status == "Error":
                        status = ConverterStatus.ConverVoiceFail
                        task_status = 'Error'
                        error_msg = "synthesis error"
                        break
                    elif result_json['code'] == 422 and result_json['data']['error_code'] != 42210:
                        status = ConverterStatus.ConverVoiceFail
                        task_status = 'Error'
                        error_msg = f"{self._translate_result_code(result_json)} (In process {task_count}/{task_number})"
                        break

                    if task_status == 'Success':
                        current_task_queue.pop(0)

            time.sleep(interval_time)

        if self._live_get_speech_error_flg['error']:
            raise Exception(f"An unexpected error occurred: {self._live_get_speech_error_flg['error_msg']}")
        if self._live_play_audio_error_flg['error']:
            raise Exception(f"An unexpected error occurred: {self._live_play_audio_error_flg['error_msg']}")

        if task_status == "Success":
            status = ConverterStatus.ConverVoiceCompleted
            if is_live_play == RunMode.LIVE_PLAY_AUDIO:
                self._live_get_speech_thread.join()
                self._live_get_speech_event.set()
                self._live_play_audio_event.set()
            if is_wait_speech == True:
                return self.get_speech()

            return ConverterResult(status, task_data, detail, error_msg)
        else:
            status = ConverterStatus.ConverVoiceFail
            detail = ""
            if is_live_play == RunMode.LIVE_PLAY_AUDIO:
                self._live_get_speech_event.set()
                self._live_play_audio_event.set()

        return ConverterResult(status, task_data, detail, error_msg)


    def set_run_model(self, model: RunMode) -> None:
        if type(model) != RunMode:
            raise TypeError("Parameter 'model(Model)' type error.")

        self._model = model
        self.text.clear()


    def check_status(self) -> ConverterResult:
        """
        合成任務狀態["Success", "Waiting", "Error", "Processing"]
        """
        if len(self._task_list) < 1:
            raise RuntimeError("Converter task list is empty, Please start convert first.")

        status = ConverterStatus.ConverterStartUp
        task_data = []
        detail = ""
        error_msg = ""

        task_number = len(self._task_list)
        task_count = 1
        for task in self._task_list:
            result_json = self._api_handler.get_task_status(task['id'], self._task_list[task_count]['token'])

            if Settings.print_log:
                print(f"[INFO] Task({task['id'][:8]}) convert status '{result_json['data']['status'].lower()}'")

                if result_json['data']['status'] == "Success":
                    status = ConverterStatus.ConverVoiceCompleted
                elif result_json['data']['status'] == "Processing":
                    status = ConverterStatus.ConverVoiceRunning
                    detail = f"Voice Converting: Task({task_count}/{task_number})"
                elif result_json['data']['status'] == "Waiting":
                    status = ConverterStatus.ServerBusy
                else:
                    error_msg = self._translate_result_code(result_json)
                    status = ConverterStatus.ConverVoiceFail

            task_data.append({"id": task['id'], "data": None})
            task_count += 1
        return ConverterResult(status, task_data, detail, error_msg)


    def get_speech(self) -> ConverterResult:
        if len(self._task_list) < 1:
            raise RuntimeError("Converter task list is empty, Please start convert first.")

        task_data = []
        error_msg = ""
        for i, task in enumerate(self._task_list):
            result_json = self._api_handler.get_task_audio(task['id'], self._task_list[i]['token'])
            if result_json['code'] != 200:
                error_msg = self._translate_result_code(result_json)
                task_data.append({"id": task['id'], "data": None})
                return ConverterResult(ConverterStatus.GetSpeechFail, task_data, "", error_msg)

            task_data.append({"id": task['id'], "data": result_json['data']})
        return ConverterResult(ConverterStatus.GetSpeechSuccess, task_data, "", error_msg)

    def get_speech_by_id(self, id, token):
        if len(self._task_list) < 1:
            raise RuntimeError("Converter task list is empty, Please start convert first.")
        result_json = self._api_handler.get_task_audio(id, token)
        if result_json['code'] != 200:
            error = self._translate_result_code(result_json)
            raise Exception(f"An unexpected error occurred: {error}")

        return result_json['data']


    def get_models(self, tokens: list) -> list:
        result = []
        for token in tokens:
            models = []
            result_json = self._api_handler.get_models(token)
            if result_json['code'] != 200:
                raise Exception(f"An unexpected error occurred: {self._translate_result_code(result_json)}")
            for model in result_json['data']:
                models.append({
                    'model_id': model['model_id'],
                    'name': model['name'],
                    'gender': model['gender'],
                    'languages': model['languages'],
                })
            result.append({
                "token": token,
                "models": models
            })
        
        return result