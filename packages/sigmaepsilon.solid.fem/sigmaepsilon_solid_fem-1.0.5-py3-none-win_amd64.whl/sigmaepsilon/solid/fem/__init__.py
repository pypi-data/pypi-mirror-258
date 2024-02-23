from os.path import dirname, abspath
from importlib.metadata import metadata

from .data import (
    PointData,
    CellData,
    FiniteElement,
    LineMesh,
    FemMesh,
    SolidMesh,
    MembraneMesh,
    DrillingMembraneMesh,
    SurfaceMesh,
    PlateMesh,
    SolidMesh,
)
from .structure import Structure
from .ebc import NodalSupport, NodeToNode, BodyToBody, FemEssentialBoundaryCondition
from .nbc import PointLoad, FemNaturalBoundaryCondition, FemLoad
from .config import namespace_package_name

__all__ = [
    "FemMesh",
    "SolidMesh",
    "MembraneMesh",
    "DrillingMembraneMesh",
    "LineMesh",
    "PointData",
    "CellData",
    "Structure",
    "NodalSupport",
    "NodeToNode",
    "BodyToBody",
    "PointData",
    "FiniteElement",
    "SurfaceMesh",
    "PlateMesh",
    "SolidMesh",
    "PointLoad",
    "FemNaturalBoundaryCondition",
    "FemLoad",
    "FemEssentialBoundaryCondition",
]

__pkg_name__ = namespace_package_name(dirname(abspath(__file__)), 10)
__pkg_metadata__ = metadata(__pkg_name__)
__version__ = __pkg_metadata__["version"]
__description__ = __pkg_metadata__["summary"]
del __pkg_metadata__
