from __future__ import annotations
from typing import Dict, List
from tasktiger import Task, TaskNotFound
from tasktiger._internal import COMPLETED
import textwrap

WRAP_MAX_CHARS = 40

class Graph:
    def __init__(self):
        """
        Generate vis-network graph for task workflow display
        """

    def generate(self, tiger, queue, state, task_id) -> VisData:
        nodes: Dict[str, VisNode] = {}
        edges: Dict[str, VisEdge] = {}
        visited: set[str] = set()
        try:
            task: Task = Task.from_id(tiger, queue, state, task_id)
        except:
            # check completion state
            if state != COMPLETED:
                task: Task = Task.from_id(tiger, queue, COMPLETED, task_id)
        self.generate_node_edges(task, nodes, edges, visited)

        visData: VisData = VisData(list(nodes.values()), list(edges.values()))
        return visData

    def generate_node_edges(
        self,
        task: Task,
        nodes: Dict[str, VisNode],
        edges: Dict[str, VisNode],
        visited: set[str],
        level: int = 0
    ):
        if not task:
            return

        node: VisNode | None = None

        if task.id in visited:
            return
        label = self.get_label(task)
        # colors for nodes can be set in groups on the js side
        node: VisNode = VisNode(task.id, label)
        nodes[task.id] = node
        node.level = level
        visited.add(task.id)
        if task.state:
            node.group = task.state
        else:
            node.group = "unknown"
        nodes
        if task.depends:
            dep_tasks: List[Task] = task.get_dependencies()
            for dep_task in dep_tasks:
                self.generate_node_edges(dep_task, nodes, edges, visited, level + 1)
                edge_id: str = dep_task.id + "->" + node.id
                if edge_id not in edges:
                    edge = VisEdge(edge_id, "", dep_task.id, node.id, arrows=Arrows())
                    # colors cannot be set in groups so we set here
                    edge.color = Color("#6466f3")
                    edges[edge_id] = edge

    def get_label(self, task: Task):
        label = "ID: " + task.id[0:6] + "\n"
        if task.state:
            label += "Run At: " + task.ts.strftime("%Y-%m-%d %H:%M:%S") + "\n"
            label += "Queue: " + task.queue + "\n"
            label += "State: " + task.state + "\n"
            label += "Func: " + task.serialized_func + "\n"
            label += "args: " + self.wrap(str(task.args)) + "\n"
            label += "kwargs: " + self.wrap(str(task.kwargs)) + "\n"
        else:
            label += "Not Found" + "\n"
        return label

    def wrap(self, text: str):
        return textwrap.fill(text, width=WRAP_MAX_CHARS)

class VisData:
    def __init__(self, nodes: List[VisNode], edges: List[VisEdge]):
        self.nodes = nodes
        self.edges = edges


class VisNode:
    def __init__(self, id: str, label: str, group: str = None):
        self.id: str = id
        self.label: str = label
        self.level: int = 0
        if group:
            self.group: str = group


# cannot use from and to for attributes
# so we implement edges as a dict instead
class VisEdge(Dict):
    def __init__(
        self,
        id: str,
        label: str,
        From: str,
        To: str,
        arrows: Arrows | None = None,
        color: Color | None = None,
    ):
        self["id"] = id
        self["label"] = label
        self["from"] = From
        self["to"] = To
        if arrows:
            self["arrows"] = arrows
        if color:
            self["color"] = color
        self["smooth"] = False


class Arrows:
    def __init__(self):
        self.to = {"enabled": True, "type": "arrow"}


class Color:
    def __init__(
        self,
        color: str | None,
        highlight: str | None = None,
        hover: str | None = None,
        opacity: float = 0,
    ):
        self.color = color
        if highlight:
            self.highlight = highlight
        if hover:
            self.hover = hover
        if opacity:
            self.opacity = opacity
