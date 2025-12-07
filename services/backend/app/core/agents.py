import yaml
import os
from typing import Dict, Any, Optional
import logging
from pydantic import BaseModel, Field

# Assuming Claude integration will use something similar to OpenAI's client for chat completions
# Or a specific Claude SDK, which we don't have direct access to.
# For now, we will simulate interaction or integrate with a generic LLM client (e.g., Anthropic's)

logger = logging.getLogger(__name__)

class AgentConfig(BaseModel):
    id: str
    display_name: str
    description: str
    system_prompt: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    example_invocation: Dict[str, Any]

class AgentManager:
    _agents: Dict[str, AgentConfig] = {}
    _agents_dir: str = "subagents/agents"

    @classmethod
    def load_agents(cls):
        """Loads all agent configurations from YAML files."""
        cls._agents = {}
        full_agents_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', cls._agents_dir))
        
        if not os.path.exists(full_agents_dir):
            logger.warning(f"Agents directory not found: {full_agents_dir}")
            return

        for filename in os.listdir(full_agents_dir):
            if filename.endswith(".yaml"):
                filepath = os.path.join(full_agents_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        config_data = yaml.safe_load(f)
                        agent_config = AgentConfig(**config_data)
                        cls._agents[agent_config.id] = agent_config
                        logger.info(f"Loaded agent: {agent_config.id}")
                except Exception as e:
                    logger.error(f"Error loading agent from {filepath}: {e}")
        
        if not cls._agents:
            logger.warning("No agents loaded. Check subagents/agents directory.")

    @classmethod
    def get_agent_config(cls, agent_id: str) -> Optional[AgentConfig]:
        """Retrieves a specific agent's configuration."""
        if not cls._agents:
            cls.load_agents() # Try loading if not already loaded
        return cls._agents.get(agent_id)

    @classmethod
    def run_agent(cls, agent_id: str, inputs: Dict[str, Any], llm_client: Any) -> Any:
        """
        Simulates running an agent by using its system_prompt and inputs with an LLM.
        This is a generic runner. Actual Claude integration would go here.
        `llm_client` could be an instance of ChatOpenAI, ChatAnthropic, etc.
        """
        agent_config = cls.get_agent_config(agent_id)
        if not agent_config:
            raise ValueError(f"Agent '{agent_id}' not found.")

        # Construct the prompt for the LLM
        # This is a basic prompt construction, might need refinement based on agent's system_prompt structure
        full_prompt = agent_config.system_prompt + "\n\n"
        full_prompt += "Input:\n"
        for key, value in inputs.items():
            full_prompt += f"- {key}: {value}\n"
        full_prompt += "\nYour response MUST strictly conform to the Output Schema (JSON):\n"
        full_prompt += json.dumps(agent_config.output_schema, indent=2) + "\n\n"
        full_prompt += "Output:\n"

        logger.info(f"Running agent '{agent_id}' with prompt length {len(full_prompt)}")
        logger.debug(f"Agent prompt: {full_prompt}")

        # Assuming llm_client is a LangChain-compatible ChatModel (like ChatOpenAI)
        messages = [
            {"role": "system", "content": agent_config.system_prompt},
            {"role": "user", "content": json.dumps(inputs)},
            {"role": "user", "content": f"Please provide your response strictly in JSON format matching this schema:\n{json.dumps(agent_config.output_schema, indent=2)}"}
        ]
        # It's better to pass a single structured input to LLM if it can handle tool calls / structured outputs
        # For simple text generation, combine
        
        # Claude integration via LangChain ChatModel
        from langchain_core.messages import HumanMessage, SystemMessage
        messages_for_llm = [
            SystemMessage(content=agent_config.system_prompt),
            HumanMessage(content=f"Input Parameters:\n{json.dumps(inputs, indent=2)}\n\n" \
                                 f"Please generate your response strictly in JSON format conforming to the following schema:\n" \
                                 f"{json.dumps(agent_config.output_schema, indent=2)}")
        ]

        try:
            # Assuming llm_client is an instance of ChatOpenAI or similar
            response = llm_client.invoke(messages_for_llm)
            # Claude models tend to respond with raw text, need to parse
            response_content = response.content
            
            # Attempt to parse JSON response
            parsed_output = json.loads(response_content)
            # Basic validation against output schema (can be more robust)
            # output_schema_validator = jsonschema.Draft7Validator(agent_config.output_schema)
            # if not output_schema_validator.validate(parsed_output):
            #    logger.error("Agent output did not conform to schema.")
            #    raise ValueError("Agent output did not conform to expected schema.")
            return parsed_output

        except json.JSONDecodeError as e:
            logger.error(f"Agent '{agent_id}' response was not valid JSON: {response_content[:500]}... Error: {e}")
            raise ValueError(f"Agent '{agent_id}' returned invalid JSON. Please check agent prompt or LLM response.")
        except Exception as e:
            logger.error(f"Error running agent '{agent_id}': {e}", exc_info=True)
            raise

# Initialize agents when this module is imported
AgentManager.load_agents()
