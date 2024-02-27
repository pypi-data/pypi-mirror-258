"""ComponentCompoundAdvancedTimeSteppingAnalysisForModulation"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import conversion
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
    _7220,
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_COMPONENT_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound",
    "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
)

if TYPE_CHECKING:
    from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
        _7036,
    )
    from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
        _7142,
        _7143,
        _7145,
        _7149,
        _7152,
        _7155,
        _7156,
        _7157,
        _7160,
        _7164,
        _7169,
        _7170,
        _7173,
        _7177,
        _7180,
        _7183,
        _7186,
        _7188,
        _7191,
        _7192,
        _7193,
        _7194,
        _7197,
        _7199,
        _7202,
        _7203,
        _7207,
        _7210,
        _7213,
        _7216,
        _7217,
        _7218,
        _7219,
        _7223,
        _7226,
        _7227,
        _7228,
        _7229,
        _7230,
        _7233,
        _7236,
        _7237,
        _7240,
        _7245,
        _7246,
        _7249,
        _7252,
        _7253,
        _7255,
        _7256,
        _7257,
        _7260,
        _7261,
        _7262,
        _7263,
        _7264,
        _7267,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import _7546, _7543
    from mastapy.system_model.analyses_and_results import _2651


__docformat__ = "restructuredtext en"
__all__ = ("ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",)


Self = TypeVar(
    "Self", bound="ComponentCompoundAdvancedTimeSteppingAnalysisForModulation"
)


class ComponentCompoundAdvancedTimeSteppingAnalysisForModulation(
    _7220.PartCompoundAdvancedTimeSteppingAnalysisForModulation
):
    """ComponentCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    """

    TYPE = _COMPONENT_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION
    _CastSelf = TypeVar(
        "_CastSelf",
        bound="_Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
    )

    class _Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation:
        """Special nested class for casting ComponentCompoundAdvancedTimeSteppingAnalysisForModulation to subclasses."""

        def __init__(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
            parent: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ):
            self._parent = parent

        @property
        def part_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7220.PartCompoundAdvancedTimeSteppingAnalysisForModulation":
            return self._parent._cast(
                _7220.PartCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def part_compound_analysis(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7546.PartCompoundAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7546

            return self._parent._cast(_7546.PartCompoundAnalysis)

        @property
        def design_entity_compound_analysis(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7543.DesignEntityCompoundAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7543

            return self._parent._cast(_7543.DesignEntityCompoundAnalysis)

        @property
        def design_entity_analysis(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def abstract_shaft_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7142.AbstractShaftCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7142,
            )

            return self._parent._cast(
                _7142.AbstractShaftCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def abstract_shaft_or_housing_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7143.AbstractShaftOrHousingCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7143,
            )

            return self._parent._cast(
                _7143.AbstractShaftOrHousingCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def agma_gleason_conical_gear_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7145.AGMAGleasonConicalGearCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7145,
            )

            return self._parent._cast(
                _7145.AGMAGleasonConicalGearCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def bearing_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7149.BearingCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7149,
            )

            return self._parent._cast(
                _7149.BearingCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def bevel_differential_gear_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7152.BevelDifferentialGearCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7152,
            )

            return self._parent._cast(
                _7152.BevelDifferentialGearCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def bevel_differential_planet_gear_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7155.BevelDifferentialPlanetGearCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7155,
            )

            return self._parent._cast(
                _7155.BevelDifferentialPlanetGearCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def bevel_differential_sun_gear_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7156.BevelDifferentialSunGearCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7156,
            )

            return self._parent._cast(
                _7156.BevelDifferentialSunGearCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def bevel_gear_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7157.BevelGearCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7157,
            )

            return self._parent._cast(
                _7157.BevelGearCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def bolt_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7160.BoltCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7160,
            )

            return self._parent._cast(
                _7160.BoltCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def clutch_half_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7164.ClutchHalfCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7164,
            )

            return self._parent._cast(
                _7164.ClutchHalfCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def concept_coupling_half_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> (
            "_7169.ConceptCouplingHalfCompoundAdvancedTimeSteppingAnalysisForModulation"
        ):
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7169,
            )

            return self._parent._cast(
                _7169.ConceptCouplingHalfCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def concept_gear_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7170.ConceptGearCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7170,
            )

            return self._parent._cast(
                _7170.ConceptGearCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def conical_gear_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7173.ConicalGearCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7173,
            )

            return self._parent._cast(
                _7173.ConicalGearCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def connector_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7177.ConnectorCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7177,
            )

            return self._parent._cast(
                _7177.ConnectorCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def coupling_half_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7180.CouplingHalfCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7180,
            )

            return self._parent._cast(
                _7180.CouplingHalfCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def cvt_pulley_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7183.CVTPulleyCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7183,
            )

            return self._parent._cast(
                _7183.CVTPulleyCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def cycloidal_disc_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7186.CycloidalDiscCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7186,
            )

            return self._parent._cast(
                _7186.CycloidalDiscCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def cylindrical_gear_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7188.CylindricalGearCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7188,
            )

            return self._parent._cast(
                _7188.CylindricalGearCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def cylindrical_planet_gear_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7191.CylindricalPlanetGearCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7191,
            )

            return self._parent._cast(
                _7191.CylindricalPlanetGearCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def datum_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7192.DatumCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7192,
            )

            return self._parent._cast(
                _7192.DatumCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def external_cad_model_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7193.ExternalCADModelCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7193,
            )

            return self._parent._cast(
                _7193.ExternalCADModelCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def face_gear_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7194.FaceGearCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7194,
            )

            return self._parent._cast(
                _7194.FaceGearCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def fe_part_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7197.FEPartCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7197,
            )

            return self._parent._cast(
                _7197.FEPartCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def gear_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7199.GearCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7199,
            )

            return self._parent._cast(
                _7199.GearCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def guide_dxf_model_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7202.GuideDxfModelCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7202,
            )

            return self._parent._cast(
                _7202.GuideDxfModelCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def hypoid_gear_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7203.HypoidGearCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7203,
            )

            return self._parent._cast(
                _7203.HypoidGearCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def klingelnberg_cyclo_palloid_conical_gear_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7207.KlingelnbergCycloPalloidConicalGearCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7207,
            )

            return self._parent._cast(
                _7207.KlingelnbergCycloPalloidConicalGearCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7210.KlingelnbergCycloPalloidHypoidGearCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7210,
            )

            return self._parent._cast(
                _7210.KlingelnbergCycloPalloidHypoidGearCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7213.KlingelnbergCycloPalloidSpiralBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7213,
            )

            return self._parent._cast(
                _7213.KlingelnbergCycloPalloidSpiralBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def mass_disc_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7216.MassDiscCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7216,
            )

            return self._parent._cast(
                _7216.MassDiscCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def measurement_component_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7217.MeasurementComponentCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7217,
            )

            return self._parent._cast(
                _7217.MeasurementComponentCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def mountable_component_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> (
            "_7218.MountableComponentCompoundAdvancedTimeSteppingAnalysisForModulation"
        ):
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7218,
            )

            return self._parent._cast(
                _7218.MountableComponentCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def oil_seal_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7219.OilSealCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7219,
            )

            return self._parent._cast(
                _7219.OilSealCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def part_to_part_shear_coupling_half_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7223.PartToPartShearCouplingHalfCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7223,
            )

            return self._parent._cast(
                _7223.PartToPartShearCouplingHalfCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def planet_carrier_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7226.PlanetCarrierCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7226,
            )

            return self._parent._cast(
                _7226.PlanetCarrierCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def point_load_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7227.PointLoadCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7227,
            )

            return self._parent._cast(
                _7227.PointLoadCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def power_load_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7228.PowerLoadCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7228,
            )

            return self._parent._cast(
                _7228.PowerLoadCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def pulley_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7229.PulleyCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7229,
            )

            return self._parent._cast(
                _7229.PulleyCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def ring_pins_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7230.RingPinsCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7230,
            )

            return self._parent._cast(
                _7230.RingPinsCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def rolling_ring_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7233.RollingRingCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7233,
            )

            return self._parent._cast(
                _7233.RollingRingCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def shaft_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7236.ShaftCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7236,
            )

            return self._parent._cast(
                _7236.ShaftCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def shaft_hub_connection_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> (
            "_7237.ShaftHubConnectionCompoundAdvancedTimeSteppingAnalysisForModulation"
        ):
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7237,
            )

            return self._parent._cast(
                _7237.ShaftHubConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def spiral_bevel_gear_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7240.SpiralBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7240,
            )

            return self._parent._cast(
                _7240.SpiralBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def spring_damper_half_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7245.SpringDamperHalfCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7245,
            )

            return self._parent._cast(
                _7245.SpringDamperHalfCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def straight_bevel_diff_gear_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7246.StraightBevelDiffGearCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7246,
            )

            return self._parent._cast(
                _7246.StraightBevelDiffGearCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def straight_bevel_gear_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7249.StraightBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7249,
            )

            return self._parent._cast(
                _7249.StraightBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def straight_bevel_planet_gear_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7252.StraightBevelPlanetGearCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7252,
            )

            return self._parent._cast(
                _7252.StraightBevelPlanetGearCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def straight_bevel_sun_gear_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7253.StraightBevelSunGearCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7253,
            )

            return self._parent._cast(
                _7253.StraightBevelSunGearCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def synchroniser_half_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7255.SynchroniserHalfCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7255,
            )

            return self._parent._cast(
                _7255.SynchroniserHalfCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def synchroniser_part_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7256.SynchroniserPartCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7256,
            )

            return self._parent._cast(
                _7256.SynchroniserPartCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def synchroniser_sleeve_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> (
            "_7257.SynchroniserSleeveCompoundAdvancedTimeSteppingAnalysisForModulation"
        ):
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7257,
            )

            return self._parent._cast(
                _7257.SynchroniserSleeveCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def torque_converter_pump_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> (
            "_7260.TorqueConverterPumpCompoundAdvancedTimeSteppingAnalysisForModulation"
        ):
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7260,
            )

            return self._parent._cast(
                _7260.TorqueConverterPumpCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def torque_converter_turbine_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7261.TorqueConverterTurbineCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7261,
            )

            return self._parent._cast(
                _7261.TorqueConverterTurbineCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def unbalanced_mass_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7262.UnbalancedMassCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7262,
            )

            return self._parent._cast(
                _7262.UnbalancedMassCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def virtual_component_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7263.VirtualComponentCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7263,
            )

            return self._parent._cast(
                _7263.VirtualComponentCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def worm_gear_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7264.WormGearCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7264,
            )

            return self._parent._cast(
                _7264.WormGearCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def zerol_bevel_gear_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7267.ZerolBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
                _7267,
            )

            return self._parent._cast(
                _7267.ZerolBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def component_compound_advanced_time_stepping_analysis_for_modulation(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
        ) -> "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation":
            return self._parent

        def __getattr__(
            self: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
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
        instance_to_wrap: "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation.TYPE",
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases(
        self: Self,
    ) -> "List[_7036.ComponentAdvancedTimeSteppingAnalysisForModulation]":
        """List[mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.ComponentAdvancedTimeSteppingAnalysisForModulation]

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
    ) -> "List[_7036.ComponentAdvancedTimeSteppingAnalysisForModulation]":
        """List[mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.ComponentAdvancedTimeSteppingAnalysisForModulation]

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
    ) -> "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation":
        return self._Cast_ComponentCompoundAdvancedTimeSteppingAnalysisForModulation(
            self
        )
