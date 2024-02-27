"""MountableComponentCompoundAdvancedSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
    _7430,
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_MOUNTABLE_COMPONENT_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound",
    "MountableComponentCompoundAdvancedSystemDeflection",
)

if TYPE_CHECKING:
    from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
        _7352,
    )
    from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
        _7409,
        _7413,
        _7416,
        _7419,
        _7420,
        _7421,
        _7428,
        _7433,
        _7434,
        _7437,
        _7441,
        _7444,
        _7447,
        _7452,
        _7455,
        _7458,
        _7463,
        _7467,
        _7471,
        _7474,
        _7477,
        _7480,
        _7481,
        _7483,
        _7487,
        _7490,
        _7491,
        _7492,
        _7493,
        _7494,
        _7497,
        _7501,
        _7504,
        _7509,
        _7510,
        _7513,
        _7516,
        _7517,
        _7519,
        _7520,
        _7521,
        _7524,
        _7525,
        _7526,
        _7527,
        _7528,
        _7531,
        _7484,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import _7545, _7542
    from mastapy.system_model.analyses_and_results import _2651


__docformat__ = "restructuredtext en"
__all__ = ("MountableComponentCompoundAdvancedSystemDeflection",)


Self = TypeVar("Self", bound="MountableComponentCompoundAdvancedSystemDeflection")


class MountableComponentCompoundAdvancedSystemDeflection(
    _7430.ComponentCompoundAdvancedSystemDeflection
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
        ) -> "_7430.ComponentCompoundAdvancedSystemDeflection":
            return self._parent._cast(_7430.ComponentCompoundAdvancedSystemDeflection)

        @property
        def part_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7484.PartCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7484,
            )

            return self._parent._cast(_7484.PartCompoundAdvancedSystemDeflection)

        @property
        def part_compound_analysis(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7545.PartCompoundAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7545

            return self._parent._cast(_7545.PartCompoundAnalysis)

        @property
        def design_entity_compound_analysis(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7542.DesignEntityCompoundAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7542

            return self._parent._cast(_7542.DesignEntityCompoundAnalysis)

        @property
        def design_entity_analysis(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def agma_gleason_conical_gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7409.AGMAGleasonConicalGearCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7409,
            )

            return self._parent._cast(
                _7409.AGMAGleasonConicalGearCompoundAdvancedSystemDeflection
            )

        @property
        def bearing_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7413.BearingCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7413,
            )

            return self._parent._cast(_7413.BearingCompoundAdvancedSystemDeflection)

        @property
        def bevel_differential_gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7416.BevelDifferentialGearCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7416,
            )

            return self._parent._cast(
                _7416.BevelDifferentialGearCompoundAdvancedSystemDeflection
            )

        @property
        def bevel_differential_planet_gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7419.BevelDifferentialPlanetGearCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7419,
            )

            return self._parent._cast(
                _7419.BevelDifferentialPlanetGearCompoundAdvancedSystemDeflection
            )

        @property
        def bevel_differential_sun_gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7420.BevelDifferentialSunGearCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7420,
            )

            return self._parent._cast(
                _7420.BevelDifferentialSunGearCompoundAdvancedSystemDeflection
            )

        @property
        def bevel_gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7421.BevelGearCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7421,
            )

            return self._parent._cast(_7421.BevelGearCompoundAdvancedSystemDeflection)

        @property
        def clutch_half_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7428.ClutchHalfCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7428,
            )

            return self._parent._cast(_7428.ClutchHalfCompoundAdvancedSystemDeflection)

        @property
        def concept_coupling_half_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7433.ConceptCouplingHalfCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7433,
            )

            return self._parent._cast(
                _7433.ConceptCouplingHalfCompoundAdvancedSystemDeflection
            )

        @property
        def concept_gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7434.ConceptGearCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7434,
            )

            return self._parent._cast(_7434.ConceptGearCompoundAdvancedSystemDeflection)

        @property
        def conical_gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7437.ConicalGearCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7437,
            )

            return self._parent._cast(_7437.ConicalGearCompoundAdvancedSystemDeflection)

        @property
        def connector_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7441.ConnectorCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7441,
            )

            return self._parent._cast(_7441.ConnectorCompoundAdvancedSystemDeflection)

        @property
        def coupling_half_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7444.CouplingHalfCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7444,
            )

            return self._parent._cast(
                _7444.CouplingHalfCompoundAdvancedSystemDeflection
            )

        @property
        def cvt_pulley_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7447.CVTPulleyCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7447,
            )

            return self._parent._cast(_7447.CVTPulleyCompoundAdvancedSystemDeflection)

        @property
        def cylindrical_gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7452.CylindricalGearCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7452,
            )

            return self._parent._cast(
                _7452.CylindricalGearCompoundAdvancedSystemDeflection
            )

        @property
        def cylindrical_planet_gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7455.CylindricalPlanetGearCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7455,
            )

            return self._parent._cast(
                _7455.CylindricalPlanetGearCompoundAdvancedSystemDeflection
            )

        @property
        def face_gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7458.FaceGearCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7458,
            )

            return self._parent._cast(_7458.FaceGearCompoundAdvancedSystemDeflection)

        @property
        def gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7463.GearCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7463,
            )

            return self._parent._cast(_7463.GearCompoundAdvancedSystemDeflection)

        @property
        def hypoid_gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7467.HypoidGearCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7467,
            )

            return self._parent._cast(_7467.HypoidGearCompoundAdvancedSystemDeflection)

        @property
        def klingelnberg_cyclo_palloid_conical_gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> (
            "_7471.KlingelnbergCycloPalloidConicalGearCompoundAdvancedSystemDeflection"
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7471,
            )

            return self._parent._cast(
                _7471.KlingelnbergCycloPalloidConicalGearCompoundAdvancedSystemDeflection
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7474.KlingelnbergCycloPalloidHypoidGearCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7474,
            )

            return self._parent._cast(
                _7474.KlingelnbergCycloPalloidHypoidGearCompoundAdvancedSystemDeflection
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7477.KlingelnbergCycloPalloidSpiralBevelGearCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7477,
            )

            return self._parent._cast(
                _7477.KlingelnbergCycloPalloidSpiralBevelGearCompoundAdvancedSystemDeflection
            )

        @property
        def mass_disc_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7480.MassDiscCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7480,
            )

            return self._parent._cast(_7480.MassDiscCompoundAdvancedSystemDeflection)

        @property
        def measurement_component_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7481.MeasurementComponentCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7481,
            )

            return self._parent._cast(
                _7481.MeasurementComponentCompoundAdvancedSystemDeflection
            )

        @property
        def oil_seal_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7483.OilSealCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7483,
            )

            return self._parent._cast(_7483.OilSealCompoundAdvancedSystemDeflection)

        @property
        def part_to_part_shear_coupling_half_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7487.PartToPartShearCouplingHalfCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7487,
            )

            return self._parent._cast(
                _7487.PartToPartShearCouplingHalfCompoundAdvancedSystemDeflection
            )

        @property
        def planet_carrier_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7490.PlanetCarrierCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7490,
            )

            return self._parent._cast(
                _7490.PlanetCarrierCompoundAdvancedSystemDeflection
            )

        @property
        def point_load_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7491.PointLoadCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7491,
            )

            return self._parent._cast(_7491.PointLoadCompoundAdvancedSystemDeflection)

        @property
        def power_load_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7492.PowerLoadCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7492,
            )

            return self._parent._cast(_7492.PowerLoadCompoundAdvancedSystemDeflection)

        @property
        def pulley_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7493.PulleyCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7493,
            )

            return self._parent._cast(_7493.PulleyCompoundAdvancedSystemDeflection)

        @property
        def ring_pins_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7494.RingPinsCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7494,
            )

            return self._parent._cast(_7494.RingPinsCompoundAdvancedSystemDeflection)

        @property
        def rolling_ring_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7497.RollingRingCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7497,
            )

            return self._parent._cast(_7497.RollingRingCompoundAdvancedSystemDeflection)

        @property
        def shaft_hub_connection_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7501.ShaftHubConnectionCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7501,
            )

            return self._parent._cast(
                _7501.ShaftHubConnectionCompoundAdvancedSystemDeflection
            )

        @property
        def spiral_bevel_gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7504.SpiralBevelGearCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7504,
            )

            return self._parent._cast(
                _7504.SpiralBevelGearCompoundAdvancedSystemDeflection
            )

        @property
        def spring_damper_half_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7509.SpringDamperHalfCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7509,
            )

            return self._parent._cast(
                _7509.SpringDamperHalfCompoundAdvancedSystemDeflection
            )

        @property
        def straight_bevel_diff_gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7510.StraightBevelDiffGearCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7510,
            )

            return self._parent._cast(
                _7510.StraightBevelDiffGearCompoundAdvancedSystemDeflection
            )

        @property
        def straight_bevel_gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7513.StraightBevelGearCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7513,
            )

            return self._parent._cast(
                _7513.StraightBevelGearCompoundAdvancedSystemDeflection
            )

        @property
        def straight_bevel_planet_gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7516.StraightBevelPlanetGearCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7516,
            )

            return self._parent._cast(
                _7516.StraightBevelPlanetGearCompoundAdvancedSystemDeflection
            )

        @property
        def straight_bevel_sun_gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7517.StraightBevelSunGearCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7517,
            )

            return self._parent._cast(
                _7517.StraightBevelSunGearCompoundAdvancedSystemDeflection
            )

        @property
        def synchroniser_half_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7519.SynchroniserHalfCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7519,
            )

            return self._parent._cast(
                _7519.SynchroniserHalfCompoundAdvancedSystemDeflection
            )

        @property
        def synchroniser_part_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7520.SynchroniserPartCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7520,
            )

            return self._parent._cast(
                _7520.SynchroniserPartCompoundAdvancedSystemDeflection
            )

        @property
        def synchroniser_sleeve_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7521.SynchroniserSleeveCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7521,
            )

            return self._parent._cast(
                _7521.SynchroniserSleeveCompoundAdvancedSystemDeflection
            )

        @property
        def torque_converter_pump_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7524.TorqueConverterPumpCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7524,
            )

            return self._parent._cast(
                _7524.TorqueConverterPumpCompoundAdvancedSystemDeflection
            )

        @property
        def torque_converter_turbine_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7525.TorqueConverterTurbineCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7525,
            )

            return self._parent._cast(
                _7525.TorqueConverterTurbineCompoundAdvancedSystemDeflection
            )

        @property
        def unbalanced_mass_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7526.UnbalancedMassCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7526,
            )

            return self._parent._cast(
                _7526.UnbalancedMassCompoundAdvancedSystemDeflection
            )

        @property
        def virtual_component_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7527.VirtualComponentCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7527,
            )

            return self._parent._cast(
                _7527.VirtualComponentCompoundAdvancedSystemDeflection
            )

        @property
        def worm_gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7528.WormGearCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7528,
            )

            return self._parent._cast(_7528.WormGearCompoundAdvancedSystemDeflection)

        @property
        def zerol_bevel_gear_compound_advanced_system_deflection(
            self: "MountableComponentCompoundAdvancedSystemDeflection._Cast_MountableComponentCompoundAdvancedSystemDeflection",
        ) -> "_7531.ZerolBevelGearCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7531,
            )

            return self._parent._cast(
                _7531.ZerolBevelGearCompoundAdvancedSystemDeflection
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
    ) -> "List[_7352.MountableComponentAdvancedSystemDeflection]":
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
    ) -> "List[_7352.MountableComponentAdvancedSystemDeflection]":
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
