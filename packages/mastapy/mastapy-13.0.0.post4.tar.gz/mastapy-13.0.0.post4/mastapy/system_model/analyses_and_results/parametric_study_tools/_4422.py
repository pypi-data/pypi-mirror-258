"""StraightBevelGearParametricStudyTool"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4312
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "StraightBevelGearParametricStudyTool",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.gears import _2547
    from mastapy.system_model.analyses_and_results.static_loads import _6962
    from mastapy.system_model.analyses_and_results.system_deflections import _2818
    from mastapy.system_model.analyses_and_results.parametric_study_tools import (
        _4300,
        _4328,
        _4361,
        _4380,
        _4320,
        _4392,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import _7544
    from mastapy.system_model.analyses_and_results import _2657, _2653, _2651


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelGearParametricStudyTool",)


Self = TypeVar("Self", bound="StraightBevelGearParametricStudyTool")


class StraightBevelGearParametricStudyTool(_4312.BevelGearParametricStudyTool):
    """StraightBevelGearParametricStudyTool

    This is a mastapy class.
    """

    TYPE = _STRAIGHT_BEVEL_GEAR_PARAMETRIC_STUDY_TOOL
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_StraightBevelGearParametricStudyTool")

    class _Cast_StraightBevelGearParametricStudyTool:
        """Special nested class for casting StraightBevelGearParametricStudyTool to subclasses."""

        def __init__(
            self: "StraightBevelGearParametricStudyTool._Cast_StraightBevelGearParametricStudyTool",
            parent: "StraightBevelGearParametricStudyTool",
        ):
            self._parent = parent

        @property
        def bevel_gear_parametric_study_tool(
            self: "StraightBevelGearParametricStudyTool._Cast_StraightBevelGearParametricStudyTool",
        ) -> "_4312.BevelGearParametricStudyTool":
            return self._parent._cast(_4312.BevelGearParametricStudyTool)

        @property
        def agma_gleason_conical_gear_parametric_study_tool(
            self: "StraightBevelGearParametricStudyTool._Cast_StraightBevelGearParametricStudyTool",
        ) -> "_4300.AGMAGleasonConicalGearParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4300,
            )

            return self._parent._cast(_4300.AGMAGleasonConicalGearParametricStudyTool)

        @property
        def conical_gear_parametric_study_tool(
            self: "StraightBevelGearParametricStudyTool._Cast_StraightBevelGearParametricStudyTool",
        ) -> "_4328.ConicalGearParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4328,
            )

            return self._parent._cast(_4328.ConicalGearParametricStudyTool)

        @property
        def gear_parametric_study_tool(
            self: "StraightBevelGearParametricStudyTool._Cast_StraightBevelGearParametricStudyTool",
        ) -> "_4361.GearParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4361,
            )

            return self._parent._cast(_4361.GearParametricStudyTool)

        @property
        def mountable_component_parametric_study_tool(
            self: "StraightBevelGearParametricStudyTool._Cast_StraightBevelGearParametricStudyTool",
        ) -> "_4380.MountableComponentParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4380,
            )

            return self._parent._cast(_4380.MountableComponentParametricStudyTool)

        @property
        def component_parametric_study_tool(
            self: "StraightBevelGearParametricStudyTool._Cast_StraightBevelGearParametricStudyTool",
        ) -> "_4320.ComponentParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4320,
            )

            return self._parent._cast(_4320.ComponentParametricStudyTool)

        @property
        def part_parametric_study_tool(
            self: "StraightBevelGearParametricStudyTool._Cast_StraightBevelGearParametricStudyTool",
        ) -> "_4392.PartParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4392,
            )

            return self._parent._cast(_4392.PartParametricStudyTool)

        @property
        def part_analysis_case(
            self: "StraightBevelGearParametricStudyTool._Cast_StraightBevelGearParametricStudyTool",
        ) -> "_7544.PartAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7544

            return self._parent._cast(_7544.PartAnalysisCase)

        @property
        def part_analysis(
            self: "StraightBevelGearParametricStudyTool._Cast_StraightBevelGearParametricStudyTool",
        ) -> "_2657.PartAnalysis":
            from mastapy.system_model.analyses_and_results import _2657

            return self._parent._cast(_2657.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "StraightBevelGearParametricStudyTool._Cast_StraightBevelGearParametricStudyTool",
        ) -> "_2653.DesignEntitySingleContextAnalysis":
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "StraightBevelGearParametricStudyTool._Cast_StraightBevelGearParametricStudyTool",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def straight_bevel_gear_parametric_study_tool(
            self: "StraightBevelGearParametricStudyTool._Cast_StraightBevelGearParametricStudyTool",
        ) -> "StraightBevelGearParametricStudyTool":
            return self._parent

        def __getattr__(
            self: "StraightBevelGearParametricStudyTool._Cast_StraightBevelGearParametricStudyTool",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(
        self: Self, instance_to_wrap: "StraightBevelGearParametricStudyTool.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2547.StraightBevelGear":
        """mastapy.system_model.part_model.gears.StraightBevelGear

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: Self) -> "_6962.StraightBevelGearLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearLoadCase

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_system_deflection_results(
        self: Self,
    ) -> "List[_2818.StraightBevelGearSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.StraightBevelGearSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentSystemDeflectionResults

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: Self,
    ) -> "StraightBevelGearParametricStudyTool._Cast_StraightBevelGearParametricStudyTool":
        return self._Cast_StraightBevelGearParametricStudyTool(self)
