from openai import OpenAI
from communicators import OpenAICommunicator


if __name__ == '__main__':
    communicator = OpenAICommunicator()
    client: OpenAI = communicator.api_client
    assistant = communicator.api_client.beta.assistants.create(
        name="dj-rest-auth Assistant",
        instructions="You are a personal code and knowledge assistant specialized "
                     "in the Python with current focus on 'dj-rest-auth' package "
                     "for Django REST framework. You can access and reference the "
                     "source documentation available at "
                     "'https://dj-rest-auth.readthedocs.io/en/latest/'. "
                     "Also, you can access all the links provided on the page. "
                     "You should provide the best practices and approaches based "
                     "on this documentation. You should provide the information "
                     "based on the keywords in the prompt. If the prompt starts "
                     "with 'text', you should provide more theoretical information"
                     " without the code implementations. If the prompt starts with"
                     " 'code 2' you should provide two code snippets based on the "
                     "request, there shouldn't be any instructions only the code "
                     "snippets.",
        model='gpt-4-1106-preview',
        tools=[{"type": "code_interpreter"}],
    )
    # 'asst_8WdE55QoODCILZPPv9GLSpIx'
    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="'code-2' I need code for implementing the authentication "
                "endpoint with Google account."
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id='asst_8WdE55QoODCILZPPv9GLSpIx',
    )
    run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )
    a = 2
