"""NodeGroup"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy.nodal_analysis.dev_tools_analyses import _183
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_NODE_GROUP = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses", "NodeGroup"
)

if TYPE_CHECKING:
    from mastapy.nodal_analysis.component_mode_synthesis import _227
    from mastapy.nodal_analysis.dev_tools_analyses import _182


__docformat__ = "restructuredtext en"
__all__ = ("NodeGroup",)


Self = TypeVar("Self", bound="NodeGroup")


class NodeGroup(_183.FEEntityGroupInteger):
    """NodeGroup

    This is a mastapy class.
    """

    TYPE = _NODE_GROUP
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_NodeGroup")

    class _Cast_NodeGroup:
        """Special nested class for casting NodeGroup to subclasses."""

        def __init__(self: "NodeGroup._Cast_NodeGroup", parent: "NodeGroup"):
            self._parent = parent

        @property
        def fe_entity_group_integer(
            self: "NodeGroup._Cast_NodeGroup",
        ) -> "_183.FEEntityGroupInteger":
            return self._parent._cast(_183.FEEntityGroupInteger)

        @property
        def fe_entity_group(self: "NodeGroup._Cast_NodeGroup") -> "_182.FEEntityGroup":
            from mastapy.nodal_analysis.dev_tools_analyses import _182

            return self._parent._cast(_182.FEEntityGroup)

        @property
        def cms_node_group(self: "NodeGroup._Cast_NodeGroup") -> "_227.CMSNodeGroup":
            from mastapy.nodal_analysis.component_mode_synthesis import _227

            return self._parent._cast(_227.CMSNodeGroup)

        @property
        def node_group(self: "NodeGroup._Cast_NodeGroup") -> "NodeGroup":
            return self._parent

        def __getattr__(self: "NodeGroup._Cast_NodeGroup", name: str):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "NodeGroup.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cast_to(self: Self) -> "NodeGroup._Cast_NodeGroup":
        return self._Cast_NodeGroup(self)
