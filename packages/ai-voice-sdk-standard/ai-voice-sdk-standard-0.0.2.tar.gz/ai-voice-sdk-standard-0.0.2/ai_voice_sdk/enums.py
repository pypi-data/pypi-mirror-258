from enum import Enum

# orator
class Voice(Enum):
    CALM_HANNAH = 'Aaron'
    STEADFAST_AARON = 'Aurora'
    CHARMING_BELLA  = 'Bella_host'
    CHEERFUL_BELLA = 'Bella_host'
    VIBRANT_BILL = 'Bill_cheerful'
    CUSTOMER_SERVICE_CELIA = 'Celia_call_center'
    AT_EASE_HANNAH = 'Hannah_colloquial'
    INTELLECTUAL_HANNAH = 'Hannah_news'
    AT_EASE_JASON = 'Jason'
    GRACEFUL_SHAWN = 'Shawn'

class RunMode(Enum):
    NORMAL = 'NORMAL'
    LIVE_PLAY_AUDIO = 'LIVE_PLAY_AUDIO'


class SsmlVersion(Enum):
    V1 = 'version="1.1"'


class SsmlLanguage(Enum):
    TW = 'zh-TW'


class SsmlPhoneme(Enum):
    TW = 'bopomo'


class ConverterStatus(Enum):
    ConverterStartUp = 0
    ConverVoiceStart = 10
    ConverVoiceRunning = 11
    ConverVoiceCompleted = 12
    ConverVoiceFail = 13
    ServerBusy = 21
    GetSpeechSuccess = 91
    GetSpeechFail = 92
