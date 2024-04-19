import time

from openai import OpenAI
import json

client = OpenAI(
    api_key="",
)

assistant_id = ""

def show_json(obj):
    print(json.loads(obj.model_dump_json()))

def get_response(thread_id):
    return client.beta.threads.messages.list(thread_id=thread_id, order="asc")

def create_new_thread():
    return client.beta.threads.create()


def start_session_stream(thread):
    message = client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=""
    )
    # Execute our run
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )

    # Wait for completion
    wait_on_run(run, thread.id)
    return get_response(thread.id)

def post_message_stream(thread_id, input):
    message = client.beta.threads.messages.create(
        thread_id=thread_id, role="user", content=input
    )
    # Execute our run
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )

    # Wait for completion
    wait_on_run(run, thread_id)
    return get_response(thread_id)

def wait_on_run(run, thread_id):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run
