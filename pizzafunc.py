from openai import OpenAI
client = OpenAI()

assistant = client.beta.assistants.create(
  instructions="You are a pizza order assistant. Use the provided functions to handle orders.",
  model="gpt-4-turbo",
  tools=[
    {
      "type": "function",
      "function": {
        "name": "capture_pizza_order",
        "description": "Capture details of the pizza order from the user's request",
        "parameters": {
          "type": "object",
          "properties": {
            "toppings": {
              "type": "array",
              "items": {"type": "string"},
              "description": "List of toppings"
            },
            "size": {
              "type": "string",
              "enum": ["Small", "Medium", "Large"],
              "description": "Size of the pizza"
            }
          },
          "required": ["toppings", "size"]
        }
      }
    },
    {
      "type": "function",
      "function": {
        "name": "send_order_to_server",
        "description": "Send the captured pizza order details to a server",
        "parameters": {
          "type": "object",
          "properties": {
            "order_details": {
              "type": "object",
              "properties": {
                "toppings": {
                  "type": "array",
                  "items": {"type": "string"}
                },
                "size": {
                  "type": "string"
                },
                "order_time": {
                  "type": "string",
                  "description": "Timestamp of the order"
                }
              },
              "required": ["toppings", "size", "order_time"]
            }
          }
        }
      }
    }
  ]
)
