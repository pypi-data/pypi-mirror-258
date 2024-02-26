from fyodorov_llm_agents.tools.tool import Tool as ToolModel
import yaml

def parse_yaml(yaml_str: str) -> ToolModel:
    if not yaml_str:
        raise ValueError('YAML string is required')
    print(f"Parsing YAML: {yaml_str}")
    yaml_str = yaml_str.strip()
    yaml_dict = yaml.safe_load(yaml_str)
    print(f"YAML dict: {yaml_dict}")
    # tool = ToolModel.from_yaml(yaml_str)
    return tool
