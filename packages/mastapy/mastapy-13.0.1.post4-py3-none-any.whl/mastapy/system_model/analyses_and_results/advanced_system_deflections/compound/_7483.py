"""MountableComponentCompoundAdvancedSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
    _7431,
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_MOUNTABLE_COMPONENT_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound",
    "MountableComponentCompoundAdvancedSystemDeflection",
)

if TYPE_CHECKING:
    from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
        _7353,
    )
    from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
        _7410,
        _7414,
        _7417,
        _7420,
        _7421,
        _7422,
        _7429,
        _7434,
        _7435,
        _7438,
        _7442,
        _7445,
        _7448,
        _7453,
        _7456,
        _7459,
        _7464,
        _7468,
        _7472,
        _7475,
        _7478,
        _7481,
        _7482,
        _7484,
        _7488,
        _7491,
        _7492,
        _7493,
        _7494,
        _7495,
        _7498,
        _7502,
        _7505,
        _7510,
        _7511,
        _7514,
        _7517,
        _7518,
        _7520,
        _7521,
        _7522,
        _7525,
        _7526,
        _7527,
        _7528,
        _7529,
        _7532,
        _7485,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import _7546, _7543
    from mastapy.system_model.analyses_and_results import _2651


__docformat__ = "restructuredtext en"
__all__ = ("MountableComponentCompoundAdvancedSystemDeflection",)


Self = TypeVar("Self", bound="MountableComponentCompoundAdvancedSystemDeflection")


class MountableComponentCompoundAdvancedSystemDeflection(
    _7431.ComponentCompoundAdvancedSystemDeflection
):
    """MountableComponentCompoundAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE = _MOUNTABLE_COMPONENT_COMPOUND_ADVANCED_SYSTEM_DEFLECTION
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_MountableComponentCompoundAdvancedSystemDeflection"
    )

    class _Cast_MountableComponentCompoundAdvancedSystemDeflection:
        """Special nested class for casting MountableComponentCompoundAdvancedSystemDeflection to subclasses."""

        def __init__(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
            parent: "MountableComponentCompoundAdvancedSystemDeflection",
        ):
            self._parent = parent

        @property
        def component_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7431.ComponentCompoundAdvancedSystemDeflection":
            return self._parent._cast(_7431.ComponentCompoundAdvancedSystemDeflection)

        @property
        def part_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7485.PartCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7485,
            )

            return self._parent._cast(_7485.PartCompoundAdvancedSystemDeflection)

        @property
        def part_compound_analysis(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7546.PartCompoundAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7546

            return self._parent._cast(_7546.PartCompoundAnalysis)

        @property
        def design_entity_compound_analysis(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7543.DesignEntityCompoundAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7543

            return self._parent._cast(_7543.DesignEntityCompoundAnalysis)

        @property
        def design_entity_analysis(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def agma_gleason_conical_gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7410.AGMAGleasonConicalGearCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7410,
            )

            return self._parent._cast(
                _7410.AGMAGleasonConicalGearCompoundAdvancedSystemDeflection
            )

        @property
        def bearing_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7414.BearingCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7414,
            )

            return self._parent._cast(_7414.BearingCompoundAdvancedSystemDeflection)

        @property
        def bevel_differential_gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7417.BevelDifferentialGearCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7417,
            )

            return self._parent._cast(
                _7417.BevelDifferentialGearCompoundAdvancedSystemDeflection
            )

        @property
        def bevel_differential_planet_gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7420.BevelDifferentialPlanetGearCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7420,
            )

            return self._parent._cast(
                _7420.BevelDifferentialPlanetGearCompoundAdvancedSystemDeflection
            )

        @property
        def bevel_differential_sun_gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7421.BevelDifferentialSunGearCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7421,
            )

            return self._parent._cast(
                _7421.BevelDifferentialSunGearCompoundAdvancedSystemDeflection
            )

        @property
        def bevel_gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7422.BevelGearCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7422,
            )

            return self._parent._cast(_7422.BevelGearCompoundAdvancedSystemDeflection)

        @property
        def clutch_half_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7429.ClutchHalfCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7429,
            )

            return self._parent._cast(_7429.ClutchHalfCompoundAdvancedSystemDeflection)

        @property
        def concept_coupling_half_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7434.ConceptCouplingHalfCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7434,
            )

            return self._parent._cast(
                _7434.ConceptCouplingHalfCompoundAdvancedSystemDeflection
            )

        @property
        def concept_gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7435.ConceptGearCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7435,
            )

            return self._parent._cast(_7435.ConceptGearCompoundAdvancedSystemDeflection)

        @property
        def conical_gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7438.ConicalGearCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7438,
            )

            return self._parent._cast(_7438.ConicalGearCompoundAdvancedSystemDeflection)

        @property
        def connector_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7442.ConnectorCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7442,
            )

            return self._parent._cast(_7442.ConnectorCompoundAdvancedSystemDeflection)

        @property
        def coupling_half_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7445.CouplingHalfCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7445,
            )

            return self._parent._cast(
                _7445.CouplingHalfCompoundAdvancedSystemDeflection
            )

        @property
        def cvt_pulley_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7448.CVTPulleyCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7448,
            )

            return self._parent._cast(_7448.CVTPulleyCompoundAdvancedSystemDeflection)

        @property
        def cylindrical_gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7453.CylindricalGearCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7453,
            )

            return self._parent._cast(
                _7453.CylindricalGearCompoundAdvancedSystemDeflection
            )

        @property
        def cylindrical_planet_gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7456.CylindricalPlanetGearCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7456,
            )

            return self._parent._cast(
                _7456.CylindricalPlanetGearCompoundAdvancedSystemDeflection
            )

        @property
        def face_gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7459.FaceGearCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7459,
            )

            return self._parent._cast(_7459.FaceGearCompoundAdvancedSystemDeflection)

        @property
        def gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7464.GearCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7464,
            )

            return self._parent._cast(_7464.GearCompoundAdvancedSystemDeflection)

        @property
        def hypoid_gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7468.HypoidGearCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7468,
            )

            return self._parent._cast(_7468.HypoidGearCompoundAdvancedSystemDeflection)

        @property
        def klingelnberg_cyclo_palloid_conical_gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> (
            "_7472.KlingelnbergCycloPalloidConicalGearCompoundAdvancedSystemDeflection"
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7472,
            )

            return self._parent._cast(
                _7472.KlingelnbergCycloPalloidConicalGearCompoundAdvancedSystemDeflection
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7475.KlingelnbergCycloPalloidHypoidGearCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7475,
            )

            return self._parent._cast(
                _7475.KlingelnbergCycloPalloidHypoidGearCompoundAdvancedSystemDeflection
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7478.KlingelnbergCycloPalloidSpiralBevelGearCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7478,
            )

            return self._parent._cast(
                _7478.KlingelnbergCycloPalloidSpiralBevelGearCompoundAdvancedSystemDeflection
            )

        @property
        def mass_disc_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7481.MassDiscCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7481,
            )

            return self._parent._cast(_7481.MassDiscCompoundAdvancedSystemDeflection)

        @property
        def measurement_component_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7482.MeasurementComponentCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7482,
            )

            return self._parent._cast(
                _7482.MeasurementComponentCompoundAdvancedSystemDeflection
            )

        @property
        def oil_seal_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7484.OilSealCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7484,
            )

            return self._parent._cast(_7484.OilSealCompoundAdvancedSystemDeflection)

        @property
        def part_to_part_shear_coupling_half_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7488.PartToPartShearCouplingHalfCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7488,
            )

            return self._parent._cast(
                _7488.PartToPartShearCouplingHalfCompoundAdvancedSystemDeflection
            )

        @property
        def planet_carrier_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7491.PlanetCarrierCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7491,
            )

            return self._parent._cast(
                _7491.PlanetCarrierCompoundAdvancedSystemDeflection
            )

        @property
        def point_load_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7492.PointLoadCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7492,
            )

            return self._parent._cast(_7492.PointLoadCompoundAdvancedSystemDeflection)

        @property
        def power_load_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7493.PowerLoadCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7493,
            )

            return self._parent._cast(_7493.PowerLoadCompoundAdvancedSystemDeflection)

        @property
        def pulley_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7494.PulleyCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7494,
            )

            return self._parent._cast(_7494.PulleyCompoundAdvancedSystemDeflection)

        @property
        def ring_pins_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7495.RingPinsCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7495,
            )

            return self._parent._cast(_7495.RingPinsCompoundAdvancedSystemDeflection)

        @property
        def rolling_ring_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7498.RollingRingCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7498,
            )

            return self._parent._cast(_7498.RollingRingCompoundAdvancedSystemDeflection)

        @property
        def shaft_hub_connection_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7502.ShaftHubConnectionCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7502,
            )

            return self._parent._cast(
                _7502.ShaftHubConnectionCompoundAdvancedSystemDeflection
            )

        @property
        def spiral_bevel_gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7505.SpiralBevelGearCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7505,
            )

            return self._parent._cast(
                _7505.SpiralBevelGearCompoundAdvancedSystemDeflection
            )

        @property
        def spring_damper_half_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7510.SpringDamperHalfCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7510,
            )

            return self._parent._cast(
                _7510.SpringDamperHalfCompoundAdvancedSystemDeflection
            )

        @property
        def straight_bevel_diff_gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7511.StraightBevelDiffGearCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7511,
            )

            return self._parent._cast(
                _7511.StraightBevelDiffGearCompoundAdvancedSystemDeflection
            )

        @property
        def straight_bevel_gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7514.StraightBevelGearCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7514,
            )

            return self._parent._cast(
                _7514.StraightBevelGearCompoundAdvancedSystemDeflection
            )

        @property
        def straight_bevel_planet_gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7517.StraightBevelPlanetGearCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7517,
            )

            return self._parent._cast(
                _7517.StraightBevelPlanetGearCompoundAdvancedSystemDeflection
            )

        @property
        def straight_bevel_sun_gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7518.StraightBevelSunGearCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7518,
            )

            return self._parent._cast(
                _7518.StraightBevelSunGearCompoundAdvancedSystemDeflection
            )

        @property
        def synchroniser_half_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7520.SynchroniserHalfCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7520,
            )

            return self._parent._cast(
                _7520.SynchroniserHalfCompoundAdvancedSystemDeflection
            )

        @property
        def synchroniser_part_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7521.SynchroniserPartCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7521,
            )

            return self._parent._cast(
                _7521.SynchroniserPartCompoundAdvancedSystemDeflection
            )

        @property
        def synchroniser_sleeve_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7522.SynchroniserSleeveCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7522,
            )

            return self._parent._cast(
                _7522.SynchroniserSleeveCompoundAdvancedSystemDeflection
            )

        @property
        def torque_converter_pump_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7525.TorqueConverterPumpCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7525,
            )

            return self._parent._cast(
                _7525.TorqueConverterPumpCompoundAdvancedSystemDeflection
            )

        @property
        def torque_converter_turbine_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7526.TorqueConverterTurbineCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7526,
            )

            return self._parent._cast(
                _7526.TorqueConverterTurbineCompoundAdvancedSystemDeflection
            )

        @property
        def unbalanced_mass_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7527.UnbalancedMassCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7527,
            )

            return self._parent._cast(
                _7527.UnbalancedMassCompoundAdvancedSystemDeflection
            )

        @property
        def virtual_component_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7528.VirtualComponentCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7528,
            )

            return self._parent._cast(
                _7528.VirtualComponentCompoundAdvancedSystemDeflection
            )

        @property
        def worm_gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7529.WormGearCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7529,
            )

            return self._parent._cast(_7529.WormGearCompoundAdvancedSystemDeflection)

        @property
        def zerol_bevel_gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7532.ZerolBevelGearCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7532,
            )

            return self._parent._cast(
                _7532.ZerolBevelGearCompoundAdvancedSystemDeflection
            )

        @property
        def mountable_component_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "MountableComponentCompoundAdvancedSystemDeflection":
            return self._parent

        def __getattr__(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
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
        instance_to_wrap: "MountableComponentCompoundAdvancedSystemDeflection.TYPE",
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases(
        self: Self,
    ) -> "List[_7353.MountableComponentAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.MountableComponentAdvancedSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def component_analysis_cases_ready(
        self: Self,
    ) -> "List[_7353.MountableComponentAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.MountableComponentAdvancedSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: Self,
    ) -> "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection":
        return self._Cast_MountableComponentCompoundAdvancedSystemDeflection(self)
