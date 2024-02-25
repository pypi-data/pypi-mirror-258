import os
from dotenv import load_dotenv
load_dotenv()
import json
from .tools_shcema import fudstop_tools, serialize_record
from openai import OpenAI
class DynamicFunctionHandler:
    def __init__(self):
        self.functions = {}
        self.client = OpenAI(api_key=os.environ.get('OPENAI_KEY'))

    async def run_conversation(self, prompt, available_functions):
        
        # Step 1: send the conversation and available functions to the model
        messages = [{"role": "user", "content": f"{prompt}. Use the former user prompt to match it with the most suitable function - then go over the data results. You're a trade master."}]
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,
            tools=fudstop_tools,
            tool_choice="auto",  # auto is default, but we'll be explicit
        )
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        # Step 2: check if the model wanted to call a function
        if tool_calls:
            # Step 3: call the function
            # Note: the JSON response may not always be valid; be sure to handle errors


            messages.append(response_message)  # extend conversation with assistant's reply

            # Step 4: send the info for each function call and function response to the model
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)

                records = await function_to_call(**function_args)

                # Process each record for serialization
                processed_records = [serialize_record(record) for record in records]

                # Serialize the list of processed records
                serialized_response = json.dumps(processed_records)

                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": f"Here is the results: {serialized_response}",
                })

            second_response = self.client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                messages=messages,
            )  # get a new response from the model where it can see the function response
            yield second_response.choices[0].message.content
        