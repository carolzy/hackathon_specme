import json
from typing import Dict


from plantuml import PlantUML


from function.gpt import GPTInstance
from function.gpt4_examples import uml_examples

PLANT_UML_SERVER: PlantUML = PlantUML(url="http://www.plantuml.com/plantuml/img/")


def process_uml_code(uml_code: str) -> str:
    return PLANT_UML_SERVER.get_url(uml_code)

# project_req, preferred_lang, preferred_ts, preferred_db, preferred_int, 
def generate_uml_code(
    project_requirements: str, framework_lang: str, framework_ts: str, framework_db: str, framework_int: str, max_retries: int = 3
) -> Dict:

    FALLBACK_ERROR_MESSAGE = {
        "url": None,
        "comments": "I'm afraid I cannot generate a diagram at the moment. Please try again",
    }

    uml_agent = GPTInstance(
        functions=[
            {
                "name": "submit_plantuml_code",
                "description": "Submit the plant UML code",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "plantuml_code": {
                            "type": "string",
                            "description": "The plantUML code to submit",
                        },
                        "context_and_reasoning": {
                            "type": "string",
                            "description": "The context and reasoning necessary for the user to understand the UML",
                        },
                    },
                    "required": ["plantuml_code", "context_and_reasoning"],
                },
            }
        ]
    )
    uml_agent.messages += uml_examples

    retries = 0

    while retries < max_retries:

        try:
            output = uml_agent(
                f"""I want to brainstorm for a new project, the idea is:\n{project_requirements}.
                These are some developer's technology preference to include, but keep in mind this is only a preference, do not include it or use it if it doesn't make sense. Do not include anything related to the front-end, authentication, or mobile. This design should be focused on the backend parts of the system. Keep it as simple as possible. Remove any unnecessary components. Also keep it as simple as possible. Here are the preferences:\n
                    1. selected programming language = {framework_lang} \n
                    2. selected API framework = {framework_ts} \n
                    3. selected database = {framework_db} \n
                    4. selected integration = {framework_int} \n

                Can you create an initial diagram (using latest version of plantUML) of how I can build it? You MUST respond with the UML diagram and nothing else. 
                """
            )

            function_call = output.function_call

            if function_call is None:
                retries += 1
                uml_agent.logger.warning("ChatGPT response unsuficient. Retrying...")
                continue

            if function_call.name!= "submit_plantuml_code":
                retries += 1
                uml_agent.logger.warning("ChatGPT response unsuficient. Retrying...")
                continue
            else:
                arguments = function_call.arguments
                arguments = json.loads(arguments)

                uml_code = arguments["plantuml_code"]
                if '@enduml' in uml_code:
                    url = process_uml_code(uml_code)
                else:
                    retries += 1
                    uml_agent.logger.warning("ChatGPT response unsuficient. Retrying...")
                    continue

                return {
                    "url": url,
                    "uml_code": uml_code,
                    "comments": arguments["context_and_reasoning"],
                }

        except json.JSONDecodeError as e:
            retries += 1
            uml_agent.logger.warning("ChatGPT response unsuficient. Retrying...")
            pass

    return FALLBACK_ERROR_MESSAGE
