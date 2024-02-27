"""BevelGearLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6814
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_BEVEL_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "BevelGearLoadCase"
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.gears import _2519
    from mastapy.system_model.analyses_and_results.static_loads import (
        _6823,
        _6826,
        _6827,
        _6954,
        _6960,
        _6963,
        _6966,
        _6967,
        _6986,
        _6845,
        _6891,
        _6925,
        _6838,
        _6929,
    )
    from mastapy.system_model.analyses_and_results import _2657, _2653, _2651


__docformat__ = "restructuredtext en"
__all__ = ("BevelGearLoadCase",)


Self = TypeVar("Self", bound="BevelGearLoadCase")


class BevelGearLoadCase(_6814.AGMAGleasonConicalGearLoadCase):
    """BevelGearLoadCase

    This is a mastapy class.
    """

    TYPE = _BEVEL_GEAR_LOAD_CASE
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_BevelGearLoadCase")

    class _Cast_BevelGearLoadCase:
        """Special nested class for casting BevelGearLoadCase to subclasses."""

        def __init__(
            self: "BevelGearLoadCase._Cast_BevelGearLoadCase",
            parent: "BevelGearLoadCase",
        ):
            self._parent = parent

        @property
        def agma_gleason_conical_gear_load_case(
            self: "BevelGearLoadCase._Cast_BevelGearLoadCase",
        ) -> "_6814.AGMAGleasonConicalGearLoadCase":
            return self._parent._cast(_6814.AGMAGleasonConicalGearLoadCase)

        @property
        def conical_gear_load_case(
            self: "BevelGearLoadCase._Cast_BevelGearLoadCase",
        ) -> "_6845.ConicalGearLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6845

            return self._parent._cast(_6845.ConicalGearLoadCase)

        @property
        def gear_load_case(
            self: "BevelGearLoadCase._Cast_BevelGearLoadCase",
        ) -> "_6891.GearLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6891

            return self._parent._cast(_6891.GearLoadCase)

        @property
        def mountable_component_load_case(
            self: "BevelGearLoadCase._Cast_BevelGearLoadCase",
        ) -> "_6925.MountableComponentLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6925

            return self._parent._cast(_6925.MountableComponentLoadCase)

        @property
        def component_load_case(
            self: "BevelGearLoadCase._Cast_BevelGearLoadCase",
        ) -> "_6838.ComponentLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6838

            return self._parent._cast(_6838.ComponentLoadCase)

        @property
        def part_load_case(
            self: "BevelGearLoadCase._Cast_BevelGearLoadCase",
        ) -> "_6929.PartLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6929

            return self._parent._cast(_6929.PartLoadCase)

        @property
        def part_analysis(
            self: "BevelGearLoadCase._Cast_BevelGearLoadCase",
        ) -> "_2657.PartAnalysis":
            from mastapy.system_model.analyses_and_results import _2657

            return self._parent._cast(_2657.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "BevelGearLoadCase._Cast_BevelGearLoadCase",
        ) -> "_2653.DesignEntitySingleContextAnalysis":
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "BevelGearLoadCase._Cast_BevelGearLoadCase",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def bevel_differential_gear_load_case(
            self: "BevelGearLoadCase._Cast_BevelGearLoadCase",
        ) -> "_6823.BevelDifferentialGearLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6823

            return self._parent._cast(_6823.BevelDifferentialGearLoadCase)

        @property
        def bevel_differential_planet_gear_load_case(
            self: "BevelGearLoadCase._Cast_BevelGearLoadCase",
        ) -> "_6826.BevelDifferentialPlanetGearLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6826

            return self._parent._cast(_6826.BevelDifferentialPlanetGearLoadCase)

        @property
        def bevel_differential_sun_gear_load_case(
            self: "BevelGearLoadCase._Cast_BevelGearLoadCase",
        ) -> "_6827.BevelDifferentialSunGearLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6827

            return self._parent._cast(_6827.BevelDifferentialSunGearLoadCase)

        @property
        def spiral_bevel_gear_load_case(
            self: "BevelGearLoadCase._Cast_BevelGearLoadCase",
        ) -> "_6954.SpiralBevelGearLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6954

            return self._parent._cast(_6954.SpiralBevelGearLoadCase)

        @property
        def straight_bevel_diff_gear_load_case(
            self: "BevelGearLoadCase._Cast_BevelGearLoadCase",
        ) -> "_6960.StraightBevelDiffGearLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6960

            return self._parent._cast(_6960.StraightBevelDiffGearLoadCase)

        @property
        def straight_bevel_gear_load_case(
            self: "BevelGearLoadCase._Cast_BevelGearLoadCase",
        ) -> "_6963.StraightBevelGearLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6963

            return self._parent._cast(_6963.StraightBevelGearLoadCase)

        @property
        def straight_bevel_planet_gear_load_case(
            self: "BevelGearLoadCase._Cast_BevelGearLoadCase",
        ) -> "_6966.StraightBevelPlanetGearLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6966

            return self._parent._cast(_6966.StraightBevelPlanetGearLoadCase)

        @property
        def straight_bevel_sun_gear_load_case(
            self: "BevelGearLoadCase._Cast_BevelGearLoadCase",
        ) -> "_6967.StraightBevelSunGearLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6967

            return self._parent._cast(_6967.StraightBevelSunGearLoadCase)

        @property
        def zerol_bevel_gear_load_case(
            self: "BevelGearLoadCase._Cast_BevelGearLoadCase",
        ) -> "_6986.ZerolBevelGearLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6986

            return self._parent._cast(_6986.ZerolBevelGearLoadCase)

        @property
        def bevel_gear_load_case(
            self: "BevelGearLoadCase._Cast_BevelGearLoadCase",
        ) -> "BevelGearLoadCase":
            return self._parent

        def __getattr__(self: "BevelGearLoadCase._Cast_BevelGearLoadCase", name: str):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "BevelGearLoadCase.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2519.BevelGear":
        """mastapy.system_model.part_model.gears.BevelGear

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: Self) -> "BevelGearLoadCase._Cast_BevelGearLoadCase":
        return self._Cast_BevelGearLoadCase(self)
