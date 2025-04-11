from langchain.prompts import ChatPromptTemplate

system_template = "You will be provided with statements, and your task is to convert them to standard English."

style_prompts = {
    "default": "",
    "academic": " Ensure that the language used is appropriate for an academic research publication.",
    "ielts": " Using fancy words. Ensure that the language used meets the standards required for an IELTS score of 8.0.",
    "informal": " Make it informal like talking to a friend."
}

prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_template + "{style}"),
    ("user", "{text}")
])