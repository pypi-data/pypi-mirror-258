"""MountableComponentHarmonicAnalysisOfSingleExcitation"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
    _6032,
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_MOUNTABLE_COMPONENT_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation",
    "MountableComponentHarmonicAnalysisOfSingleExcitation",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2464
    from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
        _6011,
        _6015,
        _6018,
        _6021,
        _6022,
        _6023,
        _6029,
        _6034,
        _6036,
        _6039,
        _6043,
        _6045,
        _6049,
        _6054,
        _6057,
        _6060,
        _6065,
        _6070,
        _6074,
        _6077,
        _6080,
        _6083,
        _6084,
        _6087,
        _6090,
        _6094,
        _6095,
        _6096,
        _6097,
        _6098,
        _6102,
        _6105,
        _6108,
        _6112,
        _6114,
        _6117,
        _6120,
        _6121,
        _6122,
        _6124,
        _6125,
        _6128,
        _6129,
        _6130,
        _6131,
        _6132,
        _6135,
        _6088,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import _7547, _7544
    from mastapy.system_model.analyses_and_results import _2657, _2653, _2651


__docformat__ = "restructuredtext en"
__all__ = ("MountableComponentHarmonicAnalysisOfSingleExcitation",)


Self = TypeVar("Self", bound="MountableComponentHarmonicAnalysisOfSingleExcitation")


class MountableComponentHarmonicAnalysisOfSingleExcitation(
    _6032.ComponentHarmonicAnalysisOfSingleExcitation
):
    """MountableComponentHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    """

    TYPE = _MOUNTABLE_COMPONENT_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_MountableComponentHarmonicAnalysisOfSingleExcitation"
    )

    class _Cast_MountableComponentHarmonicAnalysisOfSingleExcitation:
        """Special nested class for casting MountableComponentHarmonicAnalysisOfSingleExcitation to subclasses."""

        def __init__(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
            parent: "MountableComponentHarmonicAnalysisOfSingleExcitation",
        ):
            self._parent = parent

        @property
        def component_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6032.ComponentHarmonicAnalysisOfSingleExcitation":
            return self._parent._cast(_6032.ComponentHarmonicAnalysisOfSingleExcitation)

        @property
        def part_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6088.PartHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6088,
            )

            return self._parent._cast(_6088.PartHarmonicAnalysisOfSingleExcitation)

        @property
        def part_static_load_analysis_case(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_7547.PartStaticLoadAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_7544.PartAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7544

            return self._parent._cast(_7544.PartAnalysisCase)

        @property
        def part_analysis(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_2657.PartAnalysis":
            from mastapy.system_model.analyses_and_results import _2657

            return self._parent._cast(_2657.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_2653.DesignEntitySingleContextAnalysis":
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def agma_gleason_conical_gear_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6011.AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6011,
            )

            return self._parent._cast(
                _6011.AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation
            )

        @property
        def bearing_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6015.BearingHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6015,
            )

            return self._parent._cast(_6015.BearingHarmonicAnalysisOfSingleExcitation)

        @property
        def bevel_differential_gear_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6018.BevelDifferentialGearHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6018,
            )

            return self._parent._cast(
                _6018.BevelDifferentialGearHarmonicAnalysisOfSingleExcitation
            )

        @property
        def bevel_differential_planet_gear_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6021.BevelDifferentialPlanetGearHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6021,
            )

            return self._parent._cast(
                _6021.BevelDifferentialPlanetGearHarmonicAnalysisOfSingleExcitation
            )

        @property
        def bevel_differential_sun_gear_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6022.BevelDifferentialSunGearHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6022,
            )

            return self._parent._cast(
                _6022.BevelDifferentialSunGearHarmonicAnalysisOfSingleExcitation
            )

        @property
        def bevel_gear_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6023.BevelGearHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6023,
            )

            return self._parent._cast(_6023.BevelGearHarmonicAnalysisOfSingleExcitation)

        @property
        def clutch_half_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6029.ClutchHalfHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6029,
            )

            return self._parent._cast(
                _6029.ClutchHalfHarmonicAnalysisOfSingleExcitation
            )

        @property
        def concept_coupling_half_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6034.ConceptCouplingHalfHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6034,
            )

            return self._parent._cast(
                _6034.ConceptCouplingHalfHarmonicAnalysisOfSingleExcitation
            )

        @property
        def concept_gear_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6036.ConceptGearHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6036,
            )

            return self._parent._cast(
                _6036.ConceptGearHarmonicAnalysisOfSingleExcitation
            )

        @property
        def conical_gear_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6039.ConicalGearHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6039,
            )

            return self._parent._cast(
                _6039.ConicalGearHarmonicAnalysisOfSingleExcitation
            )

        @property
        def connector_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6043.ConnectorHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6043,
            )

            return self._parent._cast(_6043.ConnectorHarmonicAnalysisOfSingleExcitation)

        @property
        def coupling_half_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6045.CouplingHalfHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6045,
            )

            return self._parent._cast(
                _6045.CouplingHalfHarmonicAnalysisOfSingleExcitation
            )

        @property
        def cvt_pulley_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6049.CVTPulleyHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6049,
            )

            return self._parent._cast(_6049.CVTPulleyHarmonicAnalysisOfSingleExcitation)

        @property
        def cylindrical_gear_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6054.CylindricalGearHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6054,
            )

            return self._parent._cast(
                _6054.CylindricalGearHarmonicAnalysisOfSingleExcitation
            )

        @property
        def cylindrical_planet_gear_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6057.CylindricalPlanetGearHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6057,
            )

            return self._parent._cast(
                _6057.CylindricalPlanetGearHarmonicAnalysisOfSingleExcitation
            )

        @property
        def face_gear_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6060.FaceGearHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6060,
            )

            return self._parent._cast(_6060.FaceGearHarmonicAnalysisOfSingleExcitation)

        @property
        def gear_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6065.GearHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6065,
            )

            return self._parent._cast(_6065.GearHarmonicAnalysisOfSingleExcitation)

        @property
        def hypoid_gear_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6070.HypoidGearHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6070,
            )

            return self._parent._cast(
                _6070.HypoidGearHarmonicAnalysisOfSingleExcitation
            )

        @property
        def klingelnberg_cyclo_palloid_conical_gear_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6074.KlingelnbergCycloPalloidConicalGearHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6074,
            )

            return self._parent._cast(
                _6074.KlingelnbergCycloPalloidConicalGearHarmonicAnalysisOfSingleExcitation
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> (
            "_6077.KlingelnbergCycloPalloidHypoidGearHarmonicAnalysisOfSingleExcitation"
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6077,
            )

            return self._parent._cast(
                _6077.KlingelnbergCycloPalloidHypoidGearHarmonicAnalysisOfSingleExcitation
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6080.KlingelnbergCycloPalloidSpiralBevelGearHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6080,
            )

            return self._parent._cast(
                _6080.KlingelnbergCycloPalloidSpiralBevelGearHarmonicAnalysisOfSingleExcitation
            )

        @property
        def mass_disc_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6083.MassDiscHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6083,
            )

            return self._parent._cast(_6083.MassDiscHarmonicAnalysisOfSingleExcitation)

        @property
        def measurement_component_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6084.MeasurementComponentHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6084,
            )

            return self._parent._cast(
                _6084.MeasurementComponentHarmonicAnalysisOfSingleExcitation
            )

        @property
        def oil_seal_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6087.OilSealHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6087,
            )

            return self._parent._cast(_6087.OilSealHarmonicAnalysisOfSingleExcitation)

        @property
        def part_to_part_shear_coupling_half_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6090.PartToPartShearCouplingHalfHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6090,
            )

            return self._parent._cast(
                _6090.PartToPartShearCouplingHalfHarmonicAnalysisOfSingleExcitation
            )

        @property
        def planet_carrier_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6094.PlanetCarrierHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6094,
            )

            return self._parent._cast(
                _6094.PlanetCarrierHarmonicAnalysisOfSingleExcitation
            )

        @property
        def point_load_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6095.PointLoadHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6095,
            )

            return self._parent._cast(_6095.PointLoadHarmonicAnalysisOfSingleExcitation)

        @property
        def power_load_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6096.PowerLoadHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6096,
            )

            return self._parent._cast(_6096.PowerLoadHarmonicAnalysisOfSingleExcitation)

        @property
        def pulley_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6097.PulleyHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6097,
            )

            return self._parent._cast(_6097.PulleyHarmonicAnalysisOfSingleExcitation)

        @property
        def ring_pins_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6098.RingPinsHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6098,
            )

            return self._parent._cast(_6098.RingPinsHarmonicAnalysisOfSingleExcitation)

        @property
        def rolling_ring_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6102.RollingRingHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6102,
            )

            return self._parent._cast(
                _6102.RollingRingHarmonicAnalysisOfSingleExcitation
            )

        @property
        def shaft_hub_connection_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6105.ShaftHubConnectionHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6105,
            )

            return self._parent._cast(
                _6105.ShaftHubConnectionHarmonicAnalysisOfSingleExcitation
            )

        @property
        def spiral_bevel_gear_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6108.SpiralBevelGearHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6108,
            )

            return self._parent._cast(
                _6108.SpiralBevelGearHarmonicAnalysisOfSingleExcitation
            )

        @property
        def spring_damper_half_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6112.SpringDamperHalfHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6112,
            )

            return self._parent._cast(
                _6112.SpringDamperHalfHarmonicAnalysisOfSingleExcitation
            )

        @property
        def straight_bevel_diff_gear_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6114.StraightBevelDiffGearHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6114,
            )

            return self._parent._cast(
                _6114.StraightBevelDiffGearHarmonicAnalysisOfSingleExcitation
            )

        @property
        def straight_bevel_gear_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6117.StraightBevelGearHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6117,
            )

            return self._parent._cast(
                _6117.StraightBevelGearHarmonicAnalysisOfSingleExcitation
            )

        @property
        def straight_bevel_planet_gear_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6120.StraightBevelPlanetGearHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6120,
            )

            return self._parent._cast(
                _6120.StraightBevelPlanetGearHarmonicAnalysisOfSingleExcitation
            )

        @property
        def straight_bevel_sun_gear_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6121.StraightBevelSunGearHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6121,
            )

            return self._parent._cast(
                _6121.StraightBevelSunGearHarmonicAnalysisOfSingleExcitation
            )

        @property
        def synchroniser_half_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6122.SynchroniserHalfHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6122,
            )

            return self._parent._cast(
                _6122.SynchroniserHalfHarmonicAnalysisOfSingleExcitation
            )

        @property
        def synchroniser_part_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6124.SynchroniserPartHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6124,
            )

            return self._parent._cast(
                _6124.SynchroniserPartHarmonicAnalysisOfSingleExcitation
            )

        @property
        def synchroniser_sleeve_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6125.SynchroniserSleeveHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6125,
            )

            return self._parent._cast(
                _6125.SynchroniserSleeveHarmonicAnalysisOfSingleExcitation
            )

        @property
        def torque_converter_pump_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6128.TorqueConverterPumpHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6128,
            )

            return self._parent._cast(
                _6128.TorqueConverterPumpHarmonicAnalysisOfSingleExcitation
            )

        @property
        def torque_converter_turbine_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6129.TorqueConverterTurbineHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6129,
            )

            return self._parent._cast(
                _6129.TorqueConverterTurbineHarmonicAnalysisOfSingleExcitation
            )

        @property
        def unbalanced_mass_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6130.UnbalancedMassHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6130,
            )

            return self._parent._cast(
                _6130.UnbalancedMassHarmonicAnalysisOfSingleExcitation
            )

        @property
        def virtual_component_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6131.VirtualComponentHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6131,
            )

            return self._parent._cast(
                _6131.VirtualComponentHarmonicAnalysisOfSingleExcitation
            )

        @property
        def worm_gear_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6132.WormGearHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6132,
            )

            return self._parent._cast(_6132.WormGearHarmonicAnalysisOfSingleExcitation)

        @property
        def zerol_bevel_gear_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "_6135.ZerolBevelGearHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6135,
            )

            return self._parent._cast(
                _6135.ZerolBevelGearHarmonicAnalysisOfSingleExcitation
            )

        @property
        def mountable_component_harmonic_analysis_of_single_excitation(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
        ) -> "MountableComponentHarmonicAnalysisOfSingleExcitation":
            return self._parent

        def __getattr__(
            self: "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation",
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
        instance_to_wrap: "MountableComponentHarmonicAnalysisOfSingleExcitation.TYPE",
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2464.MountableComponent":
        """mastapy.system_model.part_model.MountableComponent

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
    ) -> "MountableComponentHarmonicAnalysisOfSingleExcitation._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation":
        return self._Cast_MountableComponentHarmonicAnalysisOfSingleExcitation(self)
