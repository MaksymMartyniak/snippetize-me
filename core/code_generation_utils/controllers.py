from abc import ABC, abstractmethod


class BaseController(ABC):
    def __init__(self, api_client):
        self.api_client = api_client

    @abstractmethod
    def create_prompt(self, *args, **kwargs) -> str:
        """Update a general prompt request msg with addons"""
        raise NotImplementedError

    @abstractmethod
    def parse_response(self, response) -> dict:
        """Method for parsing prompt response"""
        raise NotImplementedError

    @abstractmethod
    def generate_code_snippets(self, *args, **kwargs) -> dict:
        """Method for generating code snippets"""
        raise NotImplementedError


class OpenAIController(BaseController):
    def create_prompt(self, language, framework, prompt_text):
        return (f"Language: {language}\nFramework: {framework}\n"
                f"Prompt: {prompt_text}")

    def parse_response(self, response):
        snippets = response.get('choices')[0].get('text').split('\n\n')
        return {
            "First snippet": snippets[0],
            "Second snippet": snippets[1],
            "Comparison": snippets[2]
        }

    def generate_code_snippets(self, language, framework, prompt_text):
        prompt = self.create_prompt(language, framework, prompt_text)
        # todo: create a decorator function that will calculate request time
        # todo: add ability to select a model
        # todo: create a decorator which will count tokens based on the
        #  response usage field, to not go out from the limits
        # todo: generate a prompt template based on the prompt engineering
        #  and its best practices. Source to cover: https://platform.openai.com/docs/guides/prompt-engineering
        # todo: maybe the DB schema should be extended with the desired API
        #  for example: OpenAI, Google etc. fields: allowed models – 3.5 / 4 etc.
        chat_completion = self.api_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-3.5-turbo",
        )
        a = chat_completion
        return self.parse_response(chat_completion)


if __name__ == '__main__':
    from core.code_generation_utils.communicators import OpenAICommunicator
    communicator = OpenAICommunicator()
    open_ai_ctrl = OpenAIController(communicator.api_client)
    result = open_ai_ctrl.generate_code_snippets(
        "Python",
        "Django",
        "Generate a model in models.py file for the order, provide "
        "some default fields and methods."
    )
    print(result)
