from chat.utils.chat_completion import gpt_chat_completion as completion


async def chat_exit(context: list):
    messages = context.copy()
    messages.append(
        {
            "role": "system",
            "content": """create a json summary of the previous food order. First write the customer information,\
              Then itemize the price for each item\
              The fields should be 1) pizza, include size 2) list of toppings for each dish 3) list of drinks,\
              include size   4) list of sides include size  5)total price """,
        },
    )

    response = await completion(messages)
    print(response)
