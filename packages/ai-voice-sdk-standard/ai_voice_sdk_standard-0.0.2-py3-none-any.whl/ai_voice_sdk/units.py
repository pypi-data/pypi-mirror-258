import requests
import json
import wave
import io

from .config import Settings
from .config import ConverterConfig
from .enums import Voice

class RestfulApiHandler(object):
    _config:ConverterConfig

    _server_support_json_status_code = [200, 300, 400, 401, 403, 404, 409, 422, 500, 503]

    def __init__(self, config:ConverterConfig) -> None:
        requests.packages.urllib3.disable_warnings()
        self._config = config

    def _restful_sender(self, api_url:str, payload:map, token="") -> requests.models.Response:
        url = f"{self._config.get_server()}{api_url}"
        headers = {'content-type': 'application/json', 'Authorization': f'{token}'}
        
        return requests.post(url, headers=headers, json=payload, timeout=10, verify=False)


    def _restful_getter(self, api_url:str, params=None, token="") -> requests.models.Response:
        url = f"{self._config.get_server()}{api_url}"
        headers = {'Authorization': f'{token}'}

        return requests.get(url, params=params, headers=headers, timeout=10, verify=False)


    def _response_handler(self, result:requests.models.Response) -> json:
        if result.status_code == 200:
            if Settings.print_log:
                print(f"Restful API: Success {result.status_code}")
        else:
            if Settings.print_log:
                print(f"Error in undefined status code: {result.status_code}")
        return {"data": result.json(), "code": result.status_code}


    def get_models(self, token: str) -> json:
        api_url = "/api/v1/models/api_token"

        try:
            result = self._restful_getter(api_url, token=token)
            return self._response_handler(result)
        except Exception as error:
            raise Exception(f"An unexpected error occurred: {error}")


    def add_ssml_task(self, ssml_text:str, token:str = "") -> json:
        # print(f'add_ssml_task: {ssml_text}, {token}')
        if token == "":
            raise RuntimeError("token is 'empty'")

        if self._config._voice.value == None:
            raise RuntimeError("Converter voice is 'None'")

        api_url = "/api/v1/syntheses/api_token"

        content = ''
        if 'voice' in ssml_text:
            content = ssml_text
        else:
            content = f'<voice name="{self._config._voice.value}">\
                {ssml_text}\
            </voice>'

        payload = {
            "ssml": f'<speak xmlns="http://www.w3.org/2001/10/synthesis" version="{self._config.get_ssml_version()}" xml:lang="{self._config.get_ssml_lang()}">\
                {content}\
            </speak>'
        }
        if len(payload['ssml']) > 2000:
            return {"data": "超過單次合成字數", "code": 42207}

        try:
            result = self._restful_sender(api_url, payload, token)
            return self._response_handler(result)
        except Exception as error:
            raise Exception(f"An unexpected error occurred: {error}")


    def get_task_status(self, task_id:str, token:str) -> json:
        api_url = f"/api/v1/syntheses/{task_id}/api_token"

        try:
            result = self._restful_getter(api_url, token = token)
            return self._response_handler(result)
        except Exception as error:
            raise Exception(f"An unexpected error occurred: {error}")


    def get_task_audio(self, task_id:str, token:str) -> json:
        api_url = f'/api/v1/syntheses/{task_id}/api_token'

        try:
            result = self._restful_getter(api_url, params={'synthesis_id': task_id}, token=token)
            result = self._restful_getter(result.json()['synthesis_path'].replace(self._config.get_server(), ""), token=token)

            if result.headers['Content-Type'] == "audio/x-wav":
                return {"data": result.content, "code": 200}
            else:
                return self._response_handler(result)
        except Exception as error:
            raise Exception(f"An unexpected error occurred: {error}")


class Tools(object):

    def __init__(self) -> None:
        self._support_file_type = Settings.support_file_type


    def save_wav_file(self, file_name:str, data:bytes):
        try:
            with open(f"{file_name}.wav", 'wb') as write_index:
                write_index.write(data)
                write_index.close()
        except Exception:
            raise IOError("Save wav file fail.")


    def merge_wav_file(self, filename:str, audio_data_list:list):
        try:
            merge_data = []
            for audio_data in audio_data_list:
                reader = wave.open(io.BytesIO(audio_data), 'rb')
                merge_data.append([reader.getparams(), reader.readframes(reader.getnframes())])
                reader.close()

            writer = wave.open(f"{filename}.wav", 'wb')
            writer.setparams(merge_data[0][0])
            for data in merge_data:
                writer.writeframes(data[1])
            writer.close()
        except Exception:
            raise IOError("Merge wav file fail.")


    def open_file(self, file_path:str, encode = "utf-8") -> str:
        text = ""
        try:
            with open(file_path, 'r', encoding = encode) as f:
                text = f.read()
                f.close()
        except FileNotFoundError as error:
            raise FileNotFoundError(f"No such file or directory: {file_path}")
        except Exception as error:
            raise Exception(f"An unexpected error occurred: {error}")

        return text


class Calculator:
    def __init__(self) -> None:
        pass

    def second_to_millisecond(self, second:int) -> float:
        return second / 1000