import os
import openai
import json
import LibHanger.Library.uwLogger as Logger

class opaipyBase():
    
    """
    opaipyBase
    """
    
    class aiLang():
        
        """
        言語設定
        """
        
        jp = 'Jp'
        """ 日本語 """

        en = 'En'
        """ 英語 """

    class promtDictElement():
        
        """
        PromptDict要素
        """
        
        systemContent = 'systemContent'
        """ systemContent """

        userContent = 'userContent'
        """ userContent """

        assistantContent = 'assistantContent'
        """ assistantContent """
        
    def __init__(self, _rootPath, _organization, _api_key, _jsonFilePath) -> None:
        
        """
        コンストラクタ
        
        Parameters
        ----------
        _rootPath : str
            Root path
        _organization : str
            organization
        _api_key : str
            api_key
        _jsonFilePath : str
            Promt jsonFile path
        """

        # 認証情報
        openai.organization = _organization
        openai.api_key = _api_key

        # ルートパス
        self.rootPathFull = _rootPath
        self.rootPath = os.path.dirname(_rootPath)

        # openai - response
        self.response = None

        # PromptJsonFile Path
        self.jsonFilePath = _jsonFilePath

        # PromptList
        self.promptList = []
        
    @property
    def responseMessage(self):
        
        """
        OpenAIからの返答
        """
        return self.response['choices'][0]['message']['content']
    
    @property
    def prompt(self) -> list:
        
        """
        Promptリスト
        """
        return self.promptList
    
    def setPrompt(self, _jsonFileName):
        
        """
        プロンプトをセットする
        
        Parameters
        ----------
        _jsonFileName : str
            プロンプトのjsonファイル名
        """

        # ファイル名
        jsonFilePath = os.path.join(
            os.path.dirname(self.rootPath), 
            self.jsonFilePath,
            _jsonFileName)
        
        # jsonファイルチェック
        if not os.path.exists(jsonFilePath):
            Logger.logging.info('jsonfile is not found.')
            return

        # jsonファイルOpen
        with open(jsonFilePath, encoding="utf-8") as f:
            self.promptList = json.loads(f.read())
        
    def request(self):
        
        """
        openAIから返答を取得する

        Parameters
        ----------
        None
        """

        # openaiの返答を取得する
        self.response = openai.ChatCompletion.create(
            model= self.promptList['model'],
            messages=[
                {"role": "system", "content": self.getContent(self.promtDictElement.systemContent)},
                {"role": "user", "content": self.getContent(self.promtDictElement.userContent)},
                {"role": "assistant", "content": self.getContent(self.promtDictElement.assistantContent)},
            ],)

    def getContent(self, _targetContent):
        
        """
        Contentを取得する
        
        Parameters
        ----------
        _targetContent : str or list
            対象のContent
        """
        
        if isinstance(self.promptList[_targetContent], list):
            return '\n'.join(self.promptList[_targetContent])
        else:
            return self.promptList[_targetContent]
    