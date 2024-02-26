from .enums import RunMode, SsmlVersion, Voice
from typing import Callable

class Settings(object):
    text_limit = 1500
    elastic_value = 200
    support_file_type = [".txt", ".ssml", ".xml"]
    each_task_text_limit = text_limit + elastic_value
    print_log = False
    is_live_play_audio = False

class ConverterConfig(object):
    _tokens:list = []
    _server_url:str = ""
    _ssml_version = '1.2'
    _ssml_lang = "zh-TW"
    _run_mode: RunMode = RunMode.NORMAL
    _voice:Voice = None # 聲音預設值為None
    _callback_functions = []


    def __init__(self, tokens:list = [], server_url = "https://www.aivoice.com.tw/business/enterprise") -> None:
        self.set_tokens(tokens)
        self.set_server(server_url)

    
    def set_tokens(self, tokens = []) -> None:
        if type(tokens) != list:
            raise TypeError("Parameter 'tokens(list)' type error.")

        self._tokens = tokens
        self._notify_update_config_callback()


    def get_tokens(self) -> list:
        return self._tokens


    def set_server(self, server_url = "") -> None:
        if type(server_url) != str:
            raise TypeError("Parameter 'server_url(str)' type error.")

        self._server_url = server_url
        self._notify_update_config_callback()


    def get_server(self) -> str:
        return self._server_url


    def set_voice(self, voice:Voice) -> None:
        if type(voice) != Voice:
            raise TypeError("Parameter 'voice(Voice)' type error.")

        self._voice = voice
        self._notify_update_config_callback()

    def change_voice_value_to_name(self, voice_value:str) -> Voice:
        for vo in Voice:
            if voice_value == vo.value:
                return vo

    def get_voice(self) -> str:
        return self._voice.value


    def get_ssml_version(self) -> str:
        return self._ssml_version


    def get_ssml_lang(self) -> str:
        return self._ssml_lang

    def set_run_mode(self, run_mode:RunMode) -> None:
        self._run_mode = run_mode
        self._notify_update_config_callback()

    def get_run_mode(self) -> RunMode:
        return self._run_mode

    def _get_all_config(self) -> dict:
        return {
            "tokens": self._tokens,
            "serverUrl": self._server_url,
            "ssmlVersion": self._ssml_version,
            "ssmlLang": self._ssml_lang,
            "runModel": self._run_mode,
        }

    def set_update_config_callback(self, callback:Callable[[dict], None] = None):
        self._callback_functions.append(callback)

    def _notify_update_config_callback(self):
        if len(self._callback_functions) > 0:
            for callback in self._callback_functions:
                callback(self._get_all_config())