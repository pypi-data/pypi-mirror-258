"""BevelGearSetLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6815
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_BEVEL_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "BevelGearSetLoadCase"
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.gears import _2520
    from mastapy.system_model.analyses_and_results.static_loads import (
        _6824,
        _6955,
        _6961,
        _6964,
        _6987,
        _6848,
        _6895,
        _6952,
        _6806,
        _6928,
    )
    from mastapy.system_model.analyses_and_results import _2657, _2653, _2651


__docformat__ = "restructuredtext en"
__all__ = ("BevelGearSetLoadCase",)


Self = TypeVar("Self", bound="BevelGearSetLoadCase")


class BevelGearSetLoadCase(_6815.AGMAGleasonConicalGearSetLoadCase):
    """BevelGearSetLoadCase

    This is a mastapy class.
    """

    TYPE = _BEVEL_GEAR_SET_LOAD_CASE
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_BevelGearSetLoadCase")

    class _Cast_BevelGearSetLoadCase:
        """Special nested class for casting BevelGearSetLoadCase to subclasses."""

        def __init__(
            self: "BevelGearSetLoadCase._Cast_BevelGearSetLoadCase",
            parent: "BevelGearSetLoadCase",
        ):
            self._parent = parent

        @property
        def agma_gleason_conical_gear_set_load_case(
            self: "BevelGearSetLoadCase._Cast_BevelGearSetLoadCase",
        ) -> "_6815.AGMAGleasonConicalGearSetLoadCase":
            return self._parent._cast(_6815.AGMAGleasonConicalGearSetLoadCase)

        @property
        def conical_gear_set_load_case(
            self: "BevelGearSetLoadCase._Cast_BevelGearSetLoadCase",
        ) -> "_6848.ConicalGearSetLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6848

            return self._parent._cast(_6848.ConicalGearSetLoadCase)

        @property
        def gear_set_load_case(
            self: "BevelGearSetLoadCase._Cast_BevelGearSetLoadCase",
        ) -> "_6895.GearSetLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6895

            return self._parent._cast(_6895.GearSetLoadCase)

        @property
        def specialised_assembly_load_case(
            self: "BevelGearSetLoadCase._Cast_BevelGearSetLoadCase",
        ) -> "_6952.SpecialisedAssemblyLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6952

            return self._parent._cast(_6952.SpecialisedAssemblyLoadCase)

        @property
        def abstract_assembly_load_case(
            self: "BevelGearSetLoadCase._Cast_BevelGearSetLoadCase",
        ) -> "_6806.AbstractAssemblyLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6806

            return self._parent._cast(_6806.AbstractAssemblyLoadCase)

        @property
        def part_load_case(
            self: "BevelGearSetLoadCase._Cast_BevelGearSetLoadCase",
        ) -> "_6928.PartLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6928

            return self._parent._cast(_6928.PartLoadCase)

        @property
        def part_analysis(
            self: "BevelGearSetLoadCase._Cast_BevelGearSetLoadCase",
        ) -> "_2657.PartAnalysis":
            from mastapy.system_model.analyses_and_results import _2657

            return self._parent._cast(_2657.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "BevelGearSetLoadCase._Cast_BevelGearSetLoadCase",
        ) -> "_2653.DesignEntitySingleContextAnalysis":
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "BevelGearSetLoadCase._Cast_BevelGearSetLoadCase",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def bevel_differential_gear_set_load_case(
            self: "BevelGearSetLoadCase._Cast_BevelGearSetLoadCase",
        ) -> "_6824.BevelDifferentialGearSetLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6824

            return self._parent._cast(_6824.BevelDifferentialGearSetLoadCase)

        @property
        def spiral_bevel_gear_set_load_case(
            self: "BevelGearSetLoadCase._Cast_BevelGearSetLoadCase",
        ) -> "_6955.SpiralBevelGearSetLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6955

            return self._parent._cast(_6955.SpiralBevelGearSetLoadCase)

        @property
        def straight_bevel_diff_gear_set_load_case(
            self: "BevelGearSetLoadCase._Cast_BevelGearSetLoadCase",
        ) -> "_6961.StraightBevelDiffGearSetLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6961

            return self._parent._cast(_6961.StraightBevelDiffGearSetLoadCase)

        @property
        def straight_bevel_gear_set_load_case(
            self: "BevelGearSetLoadCase._Cast_BevelGearSetLoadCase",
        ) -> "_6964.StraightBevelGearSetLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6964

            return self._parent._cast(_6964.StraightBevelGearSetLoadCase)

        @property
        def zerol_bevel_gear_set_load_case(
            self: "BevelGearSetLoadCase._Cast_BevelGearSetLoadCase",
        ) -> "_6987.ZerolBevelGearSetLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6987

            return self._parent._cast(_6987.ZerolBevelGearSetLoadCase)

        @property
        def bevel_gear_set_load_case(
            self: "BevelGearSetLoadCase._Cast_BevelGearSetLoadCase",
        ) -> "BevelGearSetLoadCase":
            return self._parent

        def __getattr__(
            self: "BevelGearSetLoadCase._Cast_BevelGearSetLoadCase", name: str
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "BevelGearSetLoadCase.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self: Self) -> "_2520.BevelGearSet":
        """mastapy.system_model.part_model.gears.BevelGearSet

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: Self) -> "BevelGearSetLoadCase._Cast_BevelGearSetLoadCase":
        return self._Cast_BevelGearSetLoadCase(self)
