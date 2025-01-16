# Импорт необходимых библиотек
import requests  # Библиотека для выполнения HTTP-запросов к API
import os       # Библиотека для работы с операционной системой и переменными окружения
from dotenv import load_dotenv  # Библиотека для загрузки переменных окружения из .env файла
from utils.logger import AppLogger  # Импорт собственного логгера для отслеживания работы
from utils.cache import ChatCache

# Загрузка переменных окружения из .env файла при импорте модуля
load_dotenv()

class OpenRouterClient:
    """
    Клиент для взаимодействия с OpenRouter API.
    
    OpenRouter - это сервис, предоставляющий унифицированный доступ к различным
    языковым моделям (GPT, Claude и др.) через единый API интерфейс.
    """
    
    def __init__(self, api_key = None):
        """
        Инициализация клиента OpenRouter.
        
        Настраивает:
        - Систему логирования
        - API ключ и базовый URL из переменных окружения
        - Заголовки для HTTP запросов
        - Список доступных моделей
        
        Raises:
            ValueError: Если API ключ не найден в переменных окружения
        """
        # Инициализация логгера для отслеживания работы клиента
        self.logger = AppLogger()
        
        if(api_key == None):
            cache = ChatCache()
            # Получение необходимых параметров из переменных окружения
            # self.api_key = os.getenv("OPENROUTER_API_KEY")  # API ключ для авторизации
            self.api_key = cache.get_api_key()
            cache = None
        else:
            self.api_key = api_key

        self.base_url = os.getenv("BASE_URL")          # Базовый URL API
        
        # Проверка наличия API ключа
        if not self.api_key:
            # Логирование критической ошибки
            self.logger.error("OpenRouter API key not found")
            # Выбрасывание исключения с понятным сообщением
            raise ValueError("OpenRouter API key not found")

        # Настройка заголовков для всех API запросов
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",  # Токен для авторизации запросов
            "Content-Type": "application/json"          # Указание формата данных
        }

        # Логирование успешной инициализации клиента
        self.logger.info("OpenRouterClient initialized successfully")
        
        # Загрузка списка доступных моделей при инициализации
        self.available_models = self.get_models()
    
    def get_models(self):
        """
        Получение списка доступных языковых моделей.
        
        Returns:
            list: Список словарей с информацией о моделях:
                 [{"id": "model-id", "name": "Model Name"}, ...]
                 
        Note:
            При ошибке запроса возвращает список базовых моделей по умолчанию
        """
        # Логирование начала запроса списка моделей
        self.logger.debug("Fetching available models")
        
        try:
            # Выполнение GET запроса к API для получения списка моделей
            response = requests.get(
                f"{self.base_url}/models",
                headers=self.headers
            )
            # Преобразование ответа из JSON в словарь Python
            models_data = response.json()
            
            # Логирование успешного получения списка моделей
            self.logger.info(f"Retrieved {len(models_data["data"])} models")
            
            # Преобразование данных в нужный формат
            return [
                {
                    "id": model["id"],     # Идентификатор модели для API
                    "name": model["name"]   # Человекочитаемое название модели
                }
                for model in models_data["data"]
            ]
        except Exception as e:
            # Список моделей по умолчанию при ошибке API
            models_default = [
                {"id": "deepseek-coder", "name": "DeepSeek"},
                {"id": "claude-3-sonnet", "name": "Claude 3.5 Sonnet"},
                {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo"}
            ]
            # Логирование ошибки и возврата списка по умолчанию
            self.logger.info(f"Retrieved {len(models_default)} models with Error: {e}")
            return models_default

    def send_message(self, message: str, model: str):
        """
        Отправка сообщения выбранной языковой модели.
        
        Args:
            message (str): Текст сообщения для отправки
            model (str): Идентификатор выбранной модели
            
        Returns:
            dict: Ответ от API, содержащий либо ответ модели, либо информацию об ошибке
        """
        # Логирование отправки сообщения
        self.logger.debug(f"Sending message to model: {model}")
        
        # Формирование данных для отправки в API
        data = {
            "model": model,  # Идентификатор выбранной модели
            "messages": [{"role": "user", "content": message}]  # Сообщение в формате API
        }
        
        try:
            # Логирование начала выполнения запроса
            self.logger.debug("Making API request")

            # Отправка POST запроса к API
            response = requests.post(
                f"{self.base_url}/chat/completions",  # Эндпоинт для чата
                headers=self.headers,                 # Заголовки с авторизацией
                json=data                            # Данные запроса
            )
            
            # Проверка на ошибки HTTP
            response.raise_for_status()
            
            # Логирование успешного получения ответа
            self.logger.info("Successfully received response from API")
            
            # Возврат данных ответа
            return response.json()

        except Exception as e:
            # Формирование информативного сообщения об ошибке
            error_msg = f"API request failed: {str(e)}"
            # Логирование ошибки с полным стектрейсом для отладки
            self.logger.error(error_msg, exc_info=True)
            # Возврат сообщения об ошибке в формате ответа API
            return {"error": str(e)}       

    def get_balance(self):
        """
        Получение текущего баланса аккаунта.
        
        Returns:
            str: Строка с балансом в формате '$X.XX' или 'Ошибка' при неудаче
        """
        try:
            # Запрос баланса через API
            response = requests.get(
                f"{self.base_url}/credits",  # Эндпоинт для проверки баланса
                headers=self.headers         # Заголовки с авторизацией
            )
            # Получение данных из ответа
            data = response.json()
            if data:
                data = data.get('data')
                # Вычисление доступного баланса (всего кредитов минус использовано)
                return f"${(data.get('total_credits', 0)-data.get('total_usage', 0)):.2f}"
            return "Ошибка"
        except Exception as e:
            # Формирование сообщения об ошибке
            error_msg = f"API request failed: {str(e)}"
            # Логирование ошибки с полным стектрейсом
            self.logger.error(error_msg, exc_info=True)
            # Возврат сообщения об ошибке
            return "Ошибка"
