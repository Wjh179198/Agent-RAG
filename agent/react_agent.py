from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

from model.factory import chat_model
from utils.prompt_loader_util import load_system_prompts
from agent.tools.agnet_tools import rag_summarize, get_current_month, get_user_id, get_user_location, fetch_external_data, fill_context_for_report, get_weather
from agent.tools.middleware import monitor_tool, log_before_model, report_prompt_switch

class ReactAgent:
    def __init__(self):
        self.agent = create_agent(
            model=chat_model,
            system_prompt=load_system_prompts(),
            tools=[rag_summarize, get_current_month, get_user_id, get_weather, fill_context_for_report, fetch_external_data, get_user_location],
            middleware=[monitor_tool, log_before_model, report_prompt_switch]
        )

    def execute_stream(self, query: str):
        input_dict = {
            "messages": [
                HumanMessage(content=query)
            ]
        }

        for chunk in self.agent.stream(input_dict, stream_mode="values", context={"report": False}):
            latest_message = chunk["messages"][-1]
            if latest_message.content:
               yield latest_message.content.strip() + "\n"


if __name__ == "__main__":
    agent = ReactAgent()
    for chunk in agent.execute_stream("扫地机器人在我所在的地区如何保养"):
        print(chunk, end="", flush=True)
