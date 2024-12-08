
from langgraph.graph import StateGraph, START, END

from app.agents.nodes import web_crawler, text_generator, image_generator, AgentState


def create_post_creator_agent():
    # Define a new graph
    workflow = StateGraph(AgentState)
    # Define the states
    workflow.add_node("web_crawler", web_crawler)
    workflow.add_node("text_generator", text_generator)
    workflow.add_node("image_generator", image_generator)
    # Define the transitions
    workflow.add_edge("web_crawler", "text_generator")
    workflow.add_edge("web_crawler", "image_generator")
    # Define the start and end states
    workflow.add_edge(START, "web_crawler")
    workflow.add_edge("text_generator", END)
    workflow.add_edge("image_generator", END)
    # Return the graph

    graph = workflow.compile()

    return graph


def create_post(agent, initial_input):

    final_state = agent.invoke(initial_input)

    return (
        final_state["generated_text"],
        final_state["generated_image_url"],
        "whatever2",
        "whatever3",
    )
