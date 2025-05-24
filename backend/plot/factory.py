from backend.plot.builders.pie import PieBuilder
from backend.plot.builders.bar import BarBuilder
from backend.plot.builders.line import LineBuilder
from backend.plot.builders.area import AreaBuilder
from backend.services.files import FilesService
from .builders import IBuilder

BUILDER_MAP = {
    "pie": PieBuilder,
    "bar": BarBuilder,
    "line": LineBuilder,
    "area": AreaBuilder,
}


def get_builder(kind: str, files_service: FilesService) -> IBuilder:
    """
    Factory to get the correct builder instance for the given chart type.
    Args:
        kind: Type of plot ('line', 'bar', 'pie', 'area')
        files_service: Instance of FilesService
    Returns:
        IBuilder: The builder instance for the chart type
    Raises:
        ValueError: If the kind is not supported
    """
    if kind not in BUILDER_MAP:
        raise ValueError(f"Unsupported plot kind: {kind}")
    return BUILDER_MAP[kind](files_service)
