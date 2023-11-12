import logging

class AppLogging:
    def __init__(self):
        self._setBasicConfig()

    def _setBasicConfig(self):        
        logging.basicConfig(
            filename="./log/app.log", 
            encoding="utf-8", 
            level=logging.INFO, 
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

    def info(self, message: str) -> None:
        logging.info(message)
    
