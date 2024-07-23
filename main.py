import openai
from dotenv import find_dotenv, load_dotenv
import time
import logging
from datetime import datetime

# === Set up the OpenAI client and create an assistant ===
load_dotenv() # Load the .env file
client = openai.OpenAI() # Initialize the OpenAI client
model = 'gpt-4o-mini'

#the outcommented code only needs to be run once to create the assistant
# personal_trainer_assistant = client.beta.assistants.create(
#     name = 'Personal Trainer Assistant',
#     instructions = 'you are the best personal trainer and nutritionist who knows how to get clients to build lean muscles. You have trained high-caliber athletes and movie stars.',
#     tools=[{"type": "code_interpreter"}],
#     model = model,
# )

# === Create a thread and send a message to the assistant ===

# thread = client.beta.threads.create()


# === Hardcode the IDs for the thread and assistant ===
thread_id = 'thread_2XpEiNZTwEuCAQ5HL5FN7cAU'
assistant_id = 'asst_0Ri6RR6IDtAqwjC5f2VA87BM'
print("Thread ID:", thread_id)  # Print the thread ID
print("Assistant ID:", assistant_id)  # Print the assistant ID

# === Send a message to the assistant ===
# message = "I need to build some muscle doing a calithenics workout style, while also maintaining mobility and flexibility, can you help?"
message = input("Enter your message to your personal trainer: ")
message = client.beta.threads.messages.create(
  thread_id=thread_id,
  role="user",
  content= message
)

# === Run the assistant ===
run = client.beta.threads.runs.create(
    thread_id=thread_id,
    model=model,
    assistant_id=assistant_id,
    instructions ="address the user as Arnold Schwarzenegger"
)

def thinking(client, thread_id, run_id, sleep_interval=5):
    """

    Waits for a run to complete and prints the elapsed time.
    :param client: The OpenAI client object.
    :param thread_id: The ID of the thread.
    :param run_id: The ID of the run.
    :param sleep_interval: Time in seconds to wait between checks.
    """
    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id) # The function retrieves the current status of the run using the retrieve method.
            if run.completed_at: # This checks if the run has a completion timestamp, indicating that the run has finished.
                elapsed_time = run.completed_at - run.created_at # Calculates the elapsed time by subtracting the creation time from the completion time.
                formatted_elapsed_time = time.strftime(# Formats the elapsed time in hours, minutes, and seconds.
                    "%H:%M:%S", time.gmtime(elapsed_time) 
                )
                print(f"Run completed in {formatted_elapsed_time}")
                logging.info(f"Run completed in {formatted_elapsed_time}") #  Logs the formatted elapsed time.
                # Get messages here once Run is completed!
                messages = client.beta.threads.messages.list(thread_id=thread_id) #Retrieves the list of messages in the thread.
                last_message = messages.data[0] # Gets the last message in the list.
                response = last_message.content[0].text.value # Extracts the text value from the last message.
                print(f"Assistant Response: {response}")
                break
        except Exception as e:
            logging.error(f"An error occurred while retrieving the run: {e}")
            break
        logging.info("Waiting for run to complete...")
        time.sleep(sleep_interval)

# === Call the thinking function ===
thinking(client=client, thread_id=thread_id, run_id=run.id)


run_steps = client.beta.threads.runs.steps.list(thread_id=thread_id, run_id=run.id)
print(f"Steps---> {run_steps.data[0]}")