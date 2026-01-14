from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping, Sequence

try:
    import yaml
except ImportError as exc:
    raise RuntimeError(
        "PyYAML is required to load runtime agent configuration files."
    ) from exc


AGENTS_DIR = Path(__file__).resolve().parent


@dataclass(frozen=True)
class AgentConfig:
    name: str
    display_name: str
    system_prompt: str
    safe_tools: tuple[str, ...] = field(default_factory=tuple)
    sensitive_tools: tuple[str, ...] = field(default_factory=tuple)
    delegation_tools: tuple[str, ...] = field(default_factory=tuple)
    requires_confirmation: tuple[str, ...] = field(default_factory=tuple)
    interrupt_before: tuple[str, ...] = field(default_factory=tuple)
    escalation_tool: str | None = None
    graph_node: str | None = None
    entry_node: str | None = None


def _as_tuple(raw: Any) -> tuple[str, ...]:
    if raw is None:
        return ()
    if not isinstance(raw, list):
        raise ValueError(f"Expected a list value, received {type(raw).__name__}")
    if not all(isinstance(item, str) for item in raw):
        raise ValueError("Expected all list items to be strings")
    return tuple(raw)


def _from_dict(raw: Mapping[str, Any], source: Path) -> AgentConfig:
    for key in ("name", "display_name", "system_prompt"):
        if not raw.get(key):
            raise ValueError(f"{source} is missing required field: {key}")

    sensitive_tools = _as_tuple(raw.get("sensitive_tools"))
    requires_confirmation = _as_tuple(raw.get("requires_confirmation"))
    missing_confirmation = sorted(set(sensitive_tools) - set(requires_confirmation))
    if missing_confirmation:
        raise ValueError(
            f"{source} sensitive tools must require confirmation: "
            f"{', '.join(missing_confirmation)}"
        )

    return AgentConfig(
        name=str(raw["name"]),
        display_name=str(raw["display_name"]),
        system_prompt=str(raw["system_prompt"]).strip(),
        safe_tools=_as_tuple(raw.get("safe_tools")),
        sensitive_tools=sensitive_tools,
        delegation_tools=_as_tuple(raw.get("delegation_tools")),
        requires_confirmation=requires_confirmation,
        interrupt_before=_as_tuple(raw.get("interrupt_before")),
        escalation_tool=raw.get("escalation_tool"),
        graph_node=raw.get("graph_node"),
        entry_node=raw.get("entry_node"),
    )


@lru_cache(maxsize=None)
def load_agent_config(agent_name: str) -> AgentConfig:
    source = AGENTS_DIR / f"{agent_name}.yaml"
    if not source.exists():
        raise FileNotFoundError(f"Agent config not found: {source}")

    with source.open("r", encoding="utf-8") as file:
        raw = yaml.safe_load(file) or {}

    if not isinstance(raw, dict):
        raise ValueError(f"{source} must contain a YAML mapping")

    config = _from_dict(raw, source)
    if config.name != agent_name:
        raise ValueError(
            f"{source} has name '{config.name}', expected '{agent_name}'"
        )
    return config


def load_all_agent_configs() -> dict[str, AgentConfig]:
    return {
        source.stem: load_agent_config(source.stem)
        for source in sorted(AGENTS_DIR.glob("*.yaml"))
    }


def resolve_tools(
    config: AgentConfig,
    tool_registry: Mapping[str, Any],
    sections: Sequence[str],
) -> list[Any]:
    tool_names: list[str] = []
    for section in sections:
        section_names = getattr(config, section)
        tool_names.extend(section_names)

    missing = [name for name in tool_names if name not in tool_registry]
    if missing:
        raise ValueError(
            f"Agent '{config.name}' references unknown tools: {', '.join(missing)}"
        )

    return [tool_registry[name] for name in tool_names]
