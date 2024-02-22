"""Agent and Agent group definitions and settings dataclasses."""
import dataclasses
import io
import re
import logging
import json
from typing import List, Optional, Any

import docker

from ostorlab.agent.schema import loader
from ostorlab.runtimes.proto import agent_instance_settings_pb2
from ostorlab.utils import defintions, version

MAX_AGENT_REPLICAS = 100

logger = logging.getLogger(__name__)


def _process_agent_replicas(replicas: int) -> int:
    """Add an upper & lower bounds to the number of replicas allowed for an Agent instance."""
    if replicas <= 0:
        return 1
    elif replicas > MAX_AGENT_REPLICAS:
        return MAX_AGENT_REPLICAS
    else:
        return replicas


@dataclasses.dataclass
class AgentSettings:
    """Agent instance lists the settings of running instance of an agent."""

    key: str
    version: Optional[str] = None
    bus_url: Optional[str] = ""
    bus_exchange_topic: Optional[str] = ""
    bus_management_url: Optional[str] = ""
    bus_vhost: Optional[str] = ""
    args: List[defintions.Arg] = dataclasses.field(default_factory=list)
    constraints: List[str] = dataclasses.field(default_factory=list)
    mounts: Optional[List[str]] = dataclasses.field(default_factory=list)
    restart_policy: str = ""
    mem_limit: Optional[int] = None
    open_ports: List[defintions.PortMapping] = dataclasses.field(default_factory=list)
    replicas: int = 1
    healthcheck_host: str = "0.0.0.0"
    healthcheck_port: int = 5000
    redis_url: Optional[str] = None
    tracing_collector_url: Optional[str] = None
    caps: Optional[List[str]] = None
    cyclic_processing_limit: Optional[int] = None
    depth_processing_limit: Optional[int] = None
    accepted_agents: Optional[List[str]] = None
    in_selectors: Optional[List[str]] = dataclasses.field(default_factory=list)

    @property
    def container_image(self):
        """Agent image name."""
        image = self.key.replace("/", "_")
        logger.debug("Searching container name %s with version %s", image, self.version)
        client = docker.from_env()
        matching_tag_versions = []
        for img in client.images.list():
            for t in img.tags:
                splitted_tag = t.split(":")
                if len(splitted_tag) == 2:
                    t_name, t_tag = splitted_tag
                else:
                    t_name = ":".join(splitted_tag[:-1])
                    t_tag = splitted_tag[-1]
                if t_name == image and self.version is None:
                    try:
                        matching_tag_versions.append(version.Version(t_tag[1:]))
                    except ValueError:
                        logger.warning("Invalid version %s", t_tag[1:])
                elif t_name == image and self.version is not None:
                    if re.match(self.version, t_tag[1:]) is not None:
                        try:
                            matching_tag_versions.append(version.Version(t_tag[1:]))
                        except ValueError:
                            logger.warning("Invalid version %s", t_tag[1:])

        if not matching_tag_versions:
            return None

        matching_version = max(matching_tag_versions)
        return f"{image}:v{matching_version}"

    @classmethod
    def from_proto(cls, proto: bytes) -> "AgentSettings":
        """Constructs an agent definition from a binary proto settings.

        Args:
            proto: binary proto settings file.

        Returns:
            AgentInstanceSettings object.
        """
        instance = agent_instance_settings_pb2.AgentInstanceSettings()
        instance.ParseFromString(proto)
        return cls(
            key=instance.key,
            bus_url=instance.bus_url,
            bus_exchange_topic=instance.bus_exchange_topic,
            bus_management_url=instance.bus_management_url,
            bus_vhost=instance.bus_vhost,
            args=[
                defintions.Arg(name=a.name, type=a.type, value=a.value)
                for a in instance.args
            ],
            constraints=instance.constraints,
            mounts=instance.mounts,
            restart_policy=instance.restart_policy,
            mem_limit=instance.mem_limit,
            open_ports=[
                defintions.PortMapping(
                    source_port=p.source_port, destination_port=p.destination_port
                )
                for p in instance.open_ports
            ],
            replicas=instance.replicas,
            healthcheck_host=instance.healthcheck_host,
            healthcheck_port=instance.healthcheck_port,
            redis_url=instance.redis_url,
            tracing_collector_url=instance.tracing_collector_url,
            caps=instance.caps,
            cyclic_processing_limit=instance.cyclic_processing_limit,
            depth_processing_limit=instance.depth_processing_limit,
            accepted_agents=instance.accepted_agents,
            in_selectors=instance.in_selectors,
        )

    def to_raw_proto(self) -> bytes:
        """Transforms agent instance settings into a raw proto bytes.

        Returns:
            Bytes as a serialized proto.
        """
        instance = agent_instance_settings_pb2.AgentInstanceSettings()
        instance.key = self.key
        instance.bus_url = self.bus_url
        instance.bus_exchange_topic = self.bus_exchange_topic
        instance.bus_management_url = self.bus_management_url
        instance.bus_vhost = self.bus_vhost

        for arg in self.args:
            arg_instance = instance.args.add()
            arg_instance.name = arg.name
            arg_instance.type = arg.type
            if isinstance(arg.value, bytes) and arg_instance.type != "binary":
                raise ValueError(
                    f"type {arg_instance.type} for not match value of type binary"
                )

            if isinstance(arg.value, bytes) and arg_instance.type == "binary":
                arg_instance.value = arg.value
            else:
                try:
                    arg_instance.value = json.dumps(arg.value).encode()
                except TypeError as e:
                    raise ValueError(
                        f"type {arg_instance.value} is not JSON serializable"
                    ) from e

        instance.constraints.extend(self.constraints)
        instance.mounts.extend(self.mounts)
        instance.restart_policy = self.restart_policy
        instance.in_selectors.extend(self.in_selectors)
        if self.mem_limit is not None:
            instance.mem_limit = self.mem_limit

        for open_port in self.open_ports:
            open_port_instance = instance.open_ports.add()
            open_port_instance.source_port = open_port.source_port
            open_port_instance.destination_port = open_port.destination_port

        instance.replicas = self.replicas
        instance.healthcheck_host = self.healthcheck_host
        instance.healthcheck_port = self.healthcheck_port
        instance.caps.extend(self.caps)

        if self.cyclic_processing_limit is not None:
            instance.cyclic_processing_limit = self.cyclic_processing_limit

        if self.depth_processing_limit is not None:
            instance.depth_processing_limit = self.depth_processing_limit

        if self.accepted_agents is not None:
            instance.accepted_agents.extend(self.accepted_agents)

        if self.redis_url is not None:
            instance.redis_url = self.redis_url

        if self.tracing_collector_url is not None:
            instance.tracing_collector_url = self.tracing_collector_url

        return instance.SerializeToString()


@dataclasses.dataclass
class AgentGroupDefinition:
    """Data class holding the attributes of an agent."""

    agents: List[AgentSettings]
    name: Optional[str] = None
    description: Optional[str] = None

    @classmethod
    def from_yaml(cls, group: io.FileIO):
        """Construct AgentGroupDefinition from yaml file.

        Args:
            group : agent group .yaml file.
        """
        agent_group_def = loader.load_agent_group_yaml(group)
        agent_settings = []
        agents_names = []
        for agent in agent_group_def["agents"]:
            agents_names.append(agent.get("key"))
            agent_def = AgentSettings(
                key=agent.get("key"),
                version=agent.get("version"),
                args=[
                    defintions.Arg(
                        name=a.get("name"),
                        description=a.get("description"),
                        type=a.get("type"),
                        value=a.get("value"),
                    )
                    for a in agent.get("args", [])
                ],
                constraints=agent.get("constraints", []),
                mounts=agent.get("mounts", []),
                restart_policy=agent.get("restart_policy", ""),
                mem_limit=agent.get("mem_limit"),
                open_ports=[
                    defintions.PortMapping(
                        source_port=p.get("src_port"),
                        destination_port=p.get("dest_port"),
                    )
                    for p in agent.get("open_ports", [])
                ],
                replicas=agent.get("replicas", 1),
                caps=agent.get("caps"),
                cyclic_processing_limit=agent.get("cyclic_processing_limit"),
                depth_processing_limit=agent.get("depth_processing_limit"),
                accepted_agents=agent.get("accepted_agents"),
                in_selectors=agent.get("in_selectors", []),
            )

            agent_settings.append(agent_def)

        name = agent_group_def.get("name")
        description = agent_group_def.get(
            "description", f"""Agent group : {','.join(agents_names)}"""
        )
        return cls(agent_settings, name, description)

    @classmethod
    def from_bus_message(cls, request):
        """Construct AgentGroupDefinition from a message received in the NATs.

        Args:
            request : The received message.
        """
        agent_settings = []
        agents_names = []
        for agent in request.agents:
            agents_names.append(agent.key)
            replicas = _process_agent_replicas(agent.replicas)
            agent_args = []
            for arg in agent.args:
                value = _cast_agent_arg(arg_type=arg.type, arg_value=arg.value)
                agent_arg = defintions.Arg(
                    name=arg.name,
                    type=arg.type,
                    value=value,
                )
                agent_args.append(agent_arg)

            agent_def = AgentSettings(
                key=agent.key,
                version=agent.version,
                args=agent_args,
                replicas=replicas,
                caps=agent.caps,
                cyclic_processing_limit=agent.cyclic_processing_limit,
                depth_processing_limit=agent.depth_processing_limit,
                accepted_agents=agent.accepted_agents,
                in_selectors=agent.in_selectors,
            )

            agent_settings.append(agent_def)

        name = request.key.split("/")[-1]
        description = f"Agent group {name}: {','.join(agents_names)}"
        return cls(agent_settings, name, description)


def _cast_agent_arg(arg_type: str, arg_value: bytes) -> Any:
    if arg_type == "string":
        return str(arg_value.decode())
    elif arg_type == "number":
        return float(arg_value.decode())
    elif arg_type == "boolean":
        return arg_value.decode().lower() == "true"
    elif arg_type == "array":
        return json.loads(arg_value.decode())
    elif arg_type == "object":
        return json.loads(arg_value.decode())
    else:
        raise ValueError(f"Unsupported argument type: {arg_type}")
