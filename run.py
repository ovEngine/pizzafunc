from openai import AssistantEventHandler

class EventHandler(AssistantEventHandler):
    def on_event(self, event):
        if event.event == 'thread.run.requires_action':
            run_id = event.data.id
            self.handle_requires_action(event.data, run_id)

    def handle_requires_action(self, data, run_id):
        tool_outputs = []
        for tool in data.required_action.submit_tool_outputs.tool_calls:
            if tool.function.name == "capture_pizza_order":
                order_details = {"toppings": ["mushrooms", "onions", "extra cheese"], "size": "Large", "order_time": "2023-04-22T15:00:00Z"}
                tool_outputs.append({"tool_call_id": tool.id, "output": order_details})
            elif tool.function.name == "send_order_to_server":
                tool_outputs.append({"tool_call_id": tool.id, "output": "Order sent successfully"})
        self.submit_tool_outputs(tool_outputs, run_id)

    def submit_tool_outputs(self, tool_outputs, run_id):
        with client.beta.threads.runs.submit_tool_outputs_stream(
            thread_id=self.current_run.thread_id,
            run_id=self.current_run.id,
            tool_outputs=tool_outputs,
            event_handler=self
        ) as stream:
            for text in stream.text_deltas:
                print(text, end="", flush=True)
            print()

with client.beta.threads.runs.stream(
  thread_id=thread.id,
  assistant_id=assistant.id,
  event_handler=EventHandler()
) as stream:
  stream.until_done()
