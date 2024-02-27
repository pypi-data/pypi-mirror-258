"""AGMAGleasonConicalGearDynamicAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6308
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_AGMA_GLEASON_CONICAL_GEAR_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses",
    "AGMAGleasonConicalGearDynamicAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.gears import _2513
    from mastapy.system_model.analyses_and_results.dynamic_analyses import (
        _6287,
        _6290,
        _6291,
        _6292,
        _6340,
        _6377,
        _6383,
        _6386,
        _6389,
        _6390,
        _6404,
        _6336,
        _6355,
        _6301,
        _6357,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import (
        _7546,
        _7547,
        _7544,
    )
    from mastapy.system_model.analyses_and_results import _2657, _2653, _2651


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGearDynamicAnalysis",)


Self = TypeVar("Self", bound="AGMAGleasonConicalGearDynamicAnalysis")


class AGMAGleasonConicalGearDynamicAnalysis(_6308.ConicalGearDynamicAnalysis):
    """AGMAGleasonConicalGearDynamicAnalysis

    This is a mastapy class.
    """

    TYPE = _AGMA_GLEASON_CONICAL_GEAR_DYNAMIC_ANALYSIS
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_AGMAGleasonConicalGearDynamicAnalysis"
    )

    class _Cast_AGMAGleasonConicalGearDynamicAnalysis:
        """Special nested class for casting AGMAGleasonConicalGearDynamicAnalysis to subclasses."""

        def __init__(
            self: "AGMAGleasonConicalGearDynamicAnalysis._Cast_AGMAGleasonConicalGearDynamicAnalysis",
            parent: "AGMAGleasonConicalGearDynamicAnalysis",
        ):
            self._parent = parent

        @property
        def conical_gear_dynamic_analysis(
            self: "AGMAGleasonConicalGearDynamicAnalysis._Cast_AGMAGleasonConicalGearDynamicAnalysis",
        ) -> "_6308.ConicalGearDynamicAnalysis":
            return self._parent._cast(_6308.ConicalGearDynamicAnalysis)

        @property
        def gear_dynamic_analysis(
            self: "AGMAGleasonConicalGearDynamicAnalysis._Cast_AGMAGleasonConicalGearDynamicAnalysis",
        ) -> "_6336.GearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6336

            return self._parent._cast(_6336.GearDynamicAnalysis)

        @property
        def mountable_component_dynamic_analysis(
            self: "AGMAGleasonConicalGearDynamicAnalysis._Cast_AGMAGleasonConicalGearDynamicAnalysis",
        ) -> "_6355.MountableComponentDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6355

            return self._parent._cast(_6355.MountableComponentDynamicAnalysis)

        @property
        def component_dynamic_analysis(
            self: "AGMAGleasonConicalGearDynamicAnalysis._Cast_AGMAGleasonConicalGearDynamicAnalysis",
        ) -> "_6301.ComponentDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6301

            return self._parent._cast(_6301.ComponentDynamicAnalysis)

        @property
        def part_dynamic_analysis(
            self: "AGMAGleasonConicalGearDynamicAnalysis._Cast_AGMAGleasonConicalGearDynamicAnalysis",
        ) -> "_6357.PartDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6357

            return self._parent._cast(_6357.PartDynamicAnalysis)

        @property
        def part_fe_analysis(
            self: "AGMAGleasonConicalGearDynamicAnalysis._Cast_AGMAGleasonConicalGearDynamicAnalysis",
        ) -> "_7546.PartFEAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7546

            return self._parent._cast(_7546.PartFEAnalysis)

        @property
        def part_static_load_analysis_case(
            self: "AGMAGleasonConicalGearDynamicAnalysis._Cast_AGMAGleasonConicalGearDynamicAnalysis",
        ) -> "_7547.PartStaticLoadAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "AGMAGleasonConicalGearDynamicAnalysis._Cast_AGMAGleasonConicalGearDynamicAnalysis",
        ) -> "_7544.PartAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7544

            return self._parent._cast(_7544.PartAnalysisCase)

        @property
        def part_analysis(
            self: "AGMAGleasonConicalGearDynamicAnalysis._Cast_AGMAGleasonConicalGearDynamicAnalysis",
        ) -> "_2657.PartAnalysis":
            from mastapy.system_model.analyses_and_results import _2657

            return self._parent._cast(_2657.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "AGMAGleasonConicalGearDynamicAnalysis._Cast_AGMAGleasonConicalGearDynamicAnalysis",
        ) -> "_2653.DesignEntitySingleContextAnalysis":
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "AGMAGleasonConicalGearDynamicAnalysis._Cast_AGMAGleasonConicalGearDynamicAnalysis",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def bevel_differential_gear_dynamic_analysis(
            self: "AGMAGleasonConicalGearDynamicAnalysis._Cast_AGMAGleasonConicalGearDynamicAnalysis",
        ) -> "_6287.BevelDifferentialGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6287

            return self._parent._cast(_6287.BevelDifferentialGearDynamicAnalysis)

        @property
        def bevel_differential_planet_gear_dynamic_analysis(
            self: "AGMAGleasonConicalGearDynamicAnalysis._Cast_AGMAGleasonConicalGearDynamicAnalysis",
        ) -> "_6290.BevelDifferentialPlanetGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6290

            return self._parent._cast(_6290.BevelDifferentialPlanetGearDynamicAnalysis)

        @property
        def bevel_differential_sun_gear_dynamic_analysis(
            self: "AGMAGleasonConicalGearDynamicAnalysis._Cast_AGMAGleasonConicalGearDynamicAnalysis",
        ) -> "_6291.BevelDifferentialSunGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6291

            return self._parent._cast(_6291.BevelDifferentialSunGearDynamicAnalysis)

        @property
        def bevel_gear_dynamic_analysis(
            self: "AGMAGleasonConicalGearDynamicAnalysis._Cast_AGMAGleasonConicalGearDynamicAnalysis",
        ) -> "_6292.BevelGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6292

            return self._parent._cast(_6292.BevelGearDynamicAnalysis)

        @property
        def hypoid_gear_dynamic_analysis(
            self: "AGMAGleasonConicalGearDynamicAnalysis._Cast_AGMAGleasonConicalGearDynamicAnalysis",
        ) -> "_6340.HypoidGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6340

            return self._parent._cast(_6340.HypoidGearDynamicAnalysis)

        @property
        def spiral_bevel_gear_dynamic_analysis(
            self: "AGMAGleasonConicalGearDynamicAnalysis._Cast_AGMAGleasonConicalGearDynamicAnalysis",
        ) -> "_6377.SpiralBevelGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6377

            return self._parent._cast(_6377.SpiralBevelGearDynamicAnalysis)

        @property
        def straight_bevel_diff_gear_dynamic_analysis(
            self: "AGMAGleasonConicalGearDynamicAnalysis._Cast_AGMAGleasonConicalGearDynamicAnalysis",
        ) -> "_6383.StraightBevelDiffGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6383

            return self._parent._cast(_6383.StraightBevelDiffGearDynamicAnalysis)

        @property
        def straight_bevel_gear_dynamic_analysis(
            self: "AGMAGleasonConicalGearDynamicAnalysis._Cast_AGMAGleasonConicalGearDynamicAnalysis",
        ) -> "_6386.StraightBevelGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6386

            return self._parent._cast(_6386.StraightBevelGearDynamicAnalysis)

        @property
        def straight_bevel_planet_gear_dynamic_analysis(
            self: "AGMAGleasonConicalGearDynamicAnalysis._Cast_AGMAGleasonConicalGearDynamicAnalysis",
        ) -> "_6389.StraightBevelPlanetGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6389

            return self._parent._cast(_6389.StraightBevelPlanetGearDynamicAnalysis)

        @property
        def straight_bevel_sun_gear_dynamic_analysis(
            self: "AGMAGleasonConicalGearDynamicAnalysis._Cast_AGMAGleasonConicalGearDynamicAnalysis",
        ) -> "_6390.StraightBevelSunGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6390

            return self._parent._cast(_6390.StraightBevelSunGearDynamicAnalysis)

        @property
        def zerol_bevel_gear_dynamic_analysis(
            self: "AGMAGleasonConicalGearDynamicAnalysis._Cast_AGMAGleasonConicalGearDynamicAnalysis",
        ) -> "_6404.ZerolBevelGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6404

            return self._parent._cast(_6404.ZerolBevelGearDynamicAnalysis)

        @property
        def agma_gleason_conical_gear_dynamic_analysis(
            self: "AGMAGleasonConicalGearDynamicAnalysis._Cast_AGMAGleasonConicalGearDynamicAnalysis",
        ) -> "AGMAGleasonConicalGearDynamicAnalysis":
            return self._parent

        def __getattr__(
            self: "AGMAGleasonConicalGearDynamicAnalysis._Cast_AGMAGleasonConicalGearDynamicAnalysis",
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
        self: Self, instance_to_wrap: "AGMAGleasonConicalGearDynamicAnalysis.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2513.AGMAGleasonConicalGear":
        """mastapy.system_model.part_model.gears.AGMAGleasonConicalGear

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "AGMAGleasonConicalGearDynamicAnalysis._Cast_AGMAGleasonConicalGearDynamicAnalysis":
        return self._Cast_AGMAGleasonConicalGearDynamicAnalysis(self)
