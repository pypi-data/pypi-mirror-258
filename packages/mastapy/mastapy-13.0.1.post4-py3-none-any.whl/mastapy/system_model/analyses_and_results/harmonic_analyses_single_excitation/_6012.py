"""AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
    _6040,
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_AGMA_GLEASON_CONICAL_GEAR_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation",
    "AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.gears import _2513
    from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
        _6019,
        _6022,
        _6023,
        _6024,
        _6071,
        _6109,
        _6115,
        _6118,
        _6121,
        _6122,
        _6136,
        _6066,
        _6087,
        _6033,
        _6089,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import _7548, _7545
    from mastapy.system_model.analyses_and_results import _2657, _2653, _2651


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation",)


Self = TypeVar("Self", bound="AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation")


class AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation(
    _6040.ConicalGearHarmonicAnalysisOfSingleExcitation
):
    """AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    """

    TYPE = _AGMA_GLEASON_CONICAL_GEAR_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION
    _CastSelf = TypeVar(
        "_CastSelf",
        bound="_Cast_AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation",
    )

    class _Cast_AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation:
        """Special nested class for casting AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation to subclasses."""

        def __init__(
            self: "AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation._Cast_AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation",
            parent: "AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation",
        ):
            self._parent = parent

        @property
        def conical_gear_harmonic_analysis_of_single_excitation(
            self: "AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation._Cast_AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation",
        ) -> "_6040.ConicalGearHarmonicAnalysisOfSingleExcitation":
            return self._parent._cast(
                _6040.ConicalGearHarmonicAnalysisOfSingleExcitation
            )

        @property
        def gear_harmonic_analysis_of_single_excitation(
            self: "AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation._Cast_AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation",
        ) -> "_6066.GearHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6066,
            )

            return self._parent._cast(_6066.GearHarmonicAnalysisOfSingleExcitation)

        @property
        def mountable_component_harmonic_analysis_of_single_excitation(
            self: "AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation._Cast_AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation",
        ) -> "_6087.MountableComponentHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6087,
            )

            return self._parent._cast(
                _6087.MountableComponentHarmonicAnalysisOfSingleExcitation
            )

        @property
        def component_harmonic_analysis_of_single_excitation(
            self: "AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation._Cast_AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation",
        ) -> "_6033.ComponentHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6033,
            )

            return self._parent._cast(_6033.ComponentHarmonicAnalysisOfSingleExcitation)

        @property
        def part_harmonic_analysis_of_single_excitation(
            self: "AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation._Cast_AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation",
        ) -> "_6089.PartHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6089,
            )

            return self._parent._cast(_6089.PartHarmonicAnalysisOfSingleExcitation)

        @property
        def part_static_load_analysis_case(
            self: "AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation._Cast_AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation",
        ) -> "_7548.PartStaticLoadAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7548

            return self._parent._cast(_7548.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation._Cast_AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation",
        ) -> "_7545.PartAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7545

            return self._parent._cast(_7545.PartAnalysisCase)

        @property
        def part_analysis(
            self: "AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation._Cast_AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation",
        ) -> "_2657.PartAnalysis":
            from mastapy.system_model.analyses_and_results import _2657

            return self._parent._cast(_2657.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation._Cast_AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation",
        ) -> "_2653.DesignEntitySingleContextAnalysis":
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation._Cast_AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def bevel_differential_gear_harmonic_analysis_of_single_excitation(
            self: "AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation._Cast_AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation",
        ) -> "_6019.BevelDifferentialGearHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6019,
            )

            return self._parent._cast(
                _6019.BevelDifferentialGearHarmonicAnalysisOfSingleExcitation
            )

        @property
        def bevel_differential_planet_gear_harmonic_analysis_of_single_excitation(
            self: "AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation._Cast_AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation",
        ) -> "_6022.BevelDifferentialPlanetGearHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6022,
            )

            return self._parent._cast(
                _6022.BevelDifferentialPlanetGearHarmonicAnalysisOfSingleExcitation
            )

        @property
        def bevel_differential_sun_gear_harmonic_analysis_of_single_excitation(
            self: "AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation._Cast_AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation",
        ) -> "_6023.BevelDifferentialSunGearHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6023,
            )

            return self._parent._cast(
                _6023.BevelDifferentialSunGearHarmonicAnalysisOfSingleExcitation
            )

        @property
        def bevel_gear_harmonic_analysis_of_single_excitation(
            self: "AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation._Cast_AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation",
        ) -> "_6024.BevelGearHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6024,
            )

            return self._parent._cast(_6024.BevelGearHarmonicAnalysisOfSingleExcitation)

        @property
        def hypoid_gear_harmonic_analysis_of_single_excitation(
            self: "AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation._Cast_AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation",
        ) -> "_6071.HypoidGearHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6071,
            )

            return self._parent._cast(
                _6071.HypoidGearHarmonicAnalysisOfSingleExcitation
            )

        @property
        def spiral_bevel_gear_harmonic_analysis_of_single_excitation(
            self: "AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation._Cast_AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation",
        ) -> "_6109.SpiralBevelGearHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6109,
            )

            return self._parent._cast(
                _6109.SpiralBevelGearHarmonicAnalysisOfSingleExcitation
            )

        @property
        def straight_bevel_diff_gear_harmonic_analysis_of_single_excitation(
            self: "AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation._Cast_AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation",
        ) -> "_6115.StraightBevelDiffGearHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6115,
            )

            return self._parent._cast(
                _6115.StraightBevelDiffGearHarmonicAnalysisOfSingleExcitation
            )

        @property
        def straight_bevel_gear_harmonic_analysis_of_single_excitation(
            self: "AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation._Cast_AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation",
        ) -> "_6118.StraightBevelGearHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6118,
            )

            return self._parent._cast(
                _6118.StraightBevelGearHarmonicAnalysisOfSingleExcitation
            )

        @property
        def straight_bevel_planet_gear_harmonic_analysis_of_single_excitation(
            self: "AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation._Cast_AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation",
        ) -> "_6121.StraightBevelPlanetGearHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6121,
            )

            return self._parent._cast(
                _6121.StraightBevelPlanetGearHarmonicAnalysisOfSingleExcitation
            )

        @property
        def straight_bevel_sun_gear_harmonic_analysis_of_single_excitation(
            self: "AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation._Cast_AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation",
        ) -> "_6122.StraightBevelSunGearHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6122,
            )

            return self._parent._cast(
                _6122.StraightBevelSunGearHarmonicAnalysisOfSingleExcitation
            )

        @property
        def zerol_bevel_gear_harmonic_analysis_of_single_excitation(
            self: "AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation._Cast_AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation",
        ) -> "_6136.ZerolBevelGearHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6136,
            )

            return self._parent._cast(
                _6136.ZerolBevelGearHarmonicAnalysisOfSingleExcitation
            )

        @property
        def agma_gleason_conical_gear_harmonic_analysis_of_single_excitation(
            self: "AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation._Cast_AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation",
        ) -> "AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation":
            return self._parent

        def __getattr__(
            self: "AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation._Cast_AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation",
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
        self: Self,
        instance_to_wrap: "AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation.TYPE",
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
    ) -> "AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation._Cast_AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation":
        return self._Cast_AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation(self)
