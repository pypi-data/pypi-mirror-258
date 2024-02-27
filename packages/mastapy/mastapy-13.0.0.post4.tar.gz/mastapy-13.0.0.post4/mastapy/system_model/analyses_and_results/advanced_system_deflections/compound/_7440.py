"""ConnectionCompoundAdvancedSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import conversion
from mastapy.system_model.analyses_and_results.analysis_cases import _7538
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_CONNECTION_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound",
    "ConnectionCompoundAdvancedSystemDeflection",
)

if TYPE_CHECKING:
    from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
        _7307,
    )
    from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
        _7408,
        _7410,
        _7414,
        _7417,
        _7422,
        _7427,
        _7429,
        _7432,
        _7435,
        _7438,
        _7443,
        _7445,
        _7449,
        _7451,
        _7453,
        _7459,
        _7464,
        _7468,
        _7470,
        _7472,
        _7475,
        _7478,
        _7486,
        _7488,
        _7495,
        _7498,
        _7502,
        _7505,
        _7508,
        _7511,
        _7514,
        _7523,
        _7529,
        _7532,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import _7542
    from mastapy.system_model.analyses_and_results import _2651


__docformat__ = "restructuredtext en"
__all__ = ("ConnectionCompoundAdvancedSystemDeflection",)


Self = TypeVar("Self", bound="ConnectionCompoundAdvancedSystemDeflection")


class ConnectionCompoundAdvancedSystemDeflection(_7538.ConnectionCompoundAnalysis):
    """ConnectionCompoundAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE = _CONNECTION_COMPOUND_ADVANCED_SYSTEM_DEFLECTION
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_ConnectionCompoundAdvancedSystemDeflection"
    )

    class _Cast_ConnectionCompoundAdvancedSystemDeflection:
        """Special nested class for casting ConnectionCompoundAdvancedSystemDeflection to subclasses."""

        def __init__(
            self: "ConnectionCompoundAdvancedSystemDeflection._Cast_ConnectionCompoundAdvancedSystemDeflection",
            parent: "ConnectionCompoundAdvancedSystemDeflection",
        ):
            self._parent = parent

        @property
        def connection_compound_analysis(
            self: "ConnectionCompoundAdvancedSystemDeflection._Cast_ConnectionCompoundAdvancedSystemDeflection",
        ) -> "_7538.ConnectionCompoundAnalysis":
            return self._parent._cast(_7538.ConnectionCompoundAnalysis)

        @property
        def design_entity_compound_analysis(
            self: "ConnectionCompoundAdvancedSystemDeflection._Cast_ConnectionCompoundAdvancedSystemDeflection",
        ) -> "_7542.DesignEntityCompoundAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7542

            return self._parent._cast(_7542.DesignEntityCompoundAnalysis)

        @property
        def design_entity_analysis(
            self: "ConnectionCompoundAdvancedSystemDeflection._Cast_ConnectionCompoundAdvancedSystemDeflection",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def abstract_shaft_to_mountable_component_connection_compound_advanced_system_deflection(
            self: "ConnectionCompoundAdvancedSystemDeflection._Cast_ConnectionCompoundAdvancedSystemDeflection",
        ) -> "_7408.AbstractShaftToMountableComponentConnectionCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7408,
            )

            return self._parent._cast(
                _7408.AbstractShaftToMountableComponentConnectionCompoundAdvancedSystemDeflection
            )

        @property
        def agma_gleason_conical_gear_mesh_compound_advanced_system_deflection(
            self: "ConnectionCompoundAdvancedSystemDeflection._Cast_ConnectionCompoundAdvancedSystemDeflection",
        ) -> "_7410.AGMAGleasonConicalGearMeshCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7410,
            )

            return self._parent._cast(
                _7410.AGMAGleasonConicalGearMeshCompoundAdvancedSystemDeflection
            )

        @property
        def belt_connection_compound_advanced_system_deflection(
            self: "ConnectionCompoundAdvancedSystemDeflection._Cast_ConnectionCompoundAdvancedSystemDeflection",
        ) -> "_7414.BeltConnectionCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7414,
            )

            return self._parent._cast(
                _7414.BeltConnectionCompoundAdvancedSystemDeflection
            )

        @property
        def bevel_differential_gear_mesh_compound_advanced_system_deflection(
            self: "ConnectionCompoundAdvancedSystemDeflection._Cast_ConnectionCompoundAdvancedSystemDeflection",
        ) -> "_7417.BevelDifferentialGearMeshCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7417,
            )

            return self._parent._cast(
                _7417.BevelDifferentialGearMeshCompoundAdvancedSystemDeflection
            )

        @property
        def bevel_gear_mesh_compound_advanced_system_deflection(
            self: "ConnectionCompoundAdvancedSystemDeflection._Cast_ConnectionCompoundAdvancedSystemDeflection",
        ) -> "_7422.BevelGearMeshCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7422,
            )

            return self._parent._cast(
                _7422.BevelGearMeshCompoundAdvancedSystemDeflection
            )

        @property
        def clutch_connection_compound_advanced_system_deflection(
            self: "ConnectionCompoundAdvancedSystemDeflection._Cast_ConnectionCompoundAdvancedSystemDeflection",
        ) -> "_7427.ClutchConnectionCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7427,
            )

            return self._parent._cast(
                _7427.ClutchConnectionCompoundAdvancedSystemDeflection
            )

        @property
        def coaxial_connection_compound_advanced_system_deflection(
            self: "ConnectionCompoundAdvancedSystemDeflection._Cast_ConnectionCompoundAdvancedSystemDeflection",
        ) -> "_7429.CoaxialConnectionCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7429,
            )

            return self._parent._cast(
                _7429.CoaxialConnectionCompoundAdvancedSystemDeflection
            )

        @property
        def concept_coupling_connection_compound_advanced_system_deflection(
            self: "ConnectionCompoundAdvancedSystemDeflection._Cast_ConnectionCompoundAdvancedSystemDeflection",
        ) -> "_7432.ConceptCouplingConnectionCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7432,
            )

            return self._parent._cast(
                _7432.ConceptCouplingConnectionCompoundAdvancedSystemDeflection
            )

        @property
        def concept_gear_mesh_compound_advanced_system_deflection(
            self: "ConnectionCompoundAdvancedSystemDeflection._Cast_ConnectionCompoundAdvancedSystemDeflection",
        ) -> "_7435.ConceptGearMeshCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7435,
            )

            return self._parent._cast(
                _7435.ConceptGearMeshCompoundAdvancedSystemDeflection
            )

        @property
        def conical_gear_mesh_compound_advanced_system_deflection(
            self: "ConnectionCompoundAdvancedSystemDeflection._Cast_ConnectionCompoundAdvancedSystemDeflection",
        ) -> "_7438.ConicalGearMeshCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7438,
            )

            return self._parent._cast(
                _7438.ConicalGearMeshCompoundAdvancedSystemDeflection
            )

        @property
        def coupling_connection_compound_advanced_system_deflection(
            self: "ConnectionCompoundAdvancedSystemDeflection._Cast_ConnectionCompoundAdvancedSystemDeflection",
        ) -> "_7443.CouplingConnectionCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7443,
            )

            return self._parent._cast(
                _7443.CouplingConnectionCompoundAdvancedSystemDeflection
            )

        @property
        def cvt_belt_connection_compound_advanced_system_deflection(
            self: "ConnectionCompoundAdvancedSystemDeflection._Cast_ConnectionCompoundAdvancedSystemDeflection",
        ) -> "_7445.CVTBeltConnectionCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7445,
            )

            return self._parent._cast(
                _7445.CVTBeltConnectionCompoundAdvancedSystemDeflection
            )

        @property
        def cycloidal_disc_central_bearing_connection_compound_advanced_system_deflection(
            self: "ConnectionCompoundAdvancedSystemDeflection._Cast_ConnectionCompoundAdvancedSystemDeflection",
        ) -> "_7449.CycloidalDiscCentralBearingConnectionCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7449,
            )

            return self._parent._cast(
                _7449.CycloidalDiscCentralBearingConnectionCompoundAdvancedSystemDeflection
            )

        @property
        def cycloidal_disc_planetary_bearing_connection_compound_advanced_system_deflection(
            self: "ConnectionCompoundAdvancedSystemDeflection._Cast_ConnectionCompoundAdvancedSystemDeflection",
        ) -> "_7451.CycloidalDiscPlanetaryBearingConnectionCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7451,
            )

            return self._parent._cast(
                _7451.CycloidalDiscPlanetaryBearingConnectionCompoundAdvancedSystemDeflection
            )

        @property
        def cylindrical_gear_mesh_compound_advanced_system_deflection(
            self: "ConnectionCompoundAdvancedSystemDeflection._Cast_ConnectionCompoundAdvancedSystemDeflection",
        ) -> "_7453.CylindricalGearMeshCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7453,
            )

            return self._parent._cast(
                _7453.CylindricalGearMeshCompoundAdvancedSystemDeflection
            )

        @property
        def face_gear_mesh_compound_advanced_system_deflection(
            self: "ConnectionCompoundAdvancedSystemDeflection._Cast_ConnectionCompoundAdvancedSystemDeflection",
        ) -> "_7459.FaceGearMeshCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7459,
            )

            return self._parent._cast(
                _7459.FaceGearMeshCompoundAdvancedSystemDeflection
            )

        @property
        def gear_mesh_compound_advanced_system_deflection(
            self: "ConnectionCompoundAdvancedSystemDeflection._Cast_ConnectionCompoundAdvancedSystemDeflection",
        ) -> "_7464.GearMeshCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7464,
            )

            return self._parent._cast(_7464.GearMeshCompoundAdvancedSystemDeflection)

        @property
        def hypoid_gear_mesh_compound_advanced_system_deflection(
            self: "ConnectionCompoundAdvancedSystemDeflection._Cast_ConnectionCompoundAdvancedSystemDeflection",
        ) -> "_7468.HypoidGearMeshCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7468,
            )

            return self._parent._cast(
                _7468.HypoidGearMeshCompoundAdvancedSystemDeflection
            )

        @property
        def inter_mountable_component_connection_compound_advanced_system_deflection(
            self: "ConnectionCompoundAdvancedSystemDeflection._Cast_ConnectionCompoundAdvancedSystemDeflection",
        ) -> "_7470.InterMountableComponentConnectionCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7470,
            )

            return self._parent._cast(
                _7470.InterMountableComponentConnectionCompoundAdvancedSystemDeflection
            )

        @property
        def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_advanced_system_deflection(
            self: "ConnectionCompoundAdvancedSystemDeflection._Cast_ConnectionCompoundAdvancedSystemDeflection",
        ) -> "_7472.KlingelnbergCycloPalloidConicalGearMeshCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7472,
            )

            return self._parent._cast(
                _7472.KlingelnbergCycloPalloidConicalGearMeshCompoundAdvancedSystemDeflection
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_advanced_system_deflection(
            self: "ConnectionCompoundAdvancedSystemDeflection._Cast_ConnectionCompoundAdvancedSystemDeflection",
        ) -> "_7475.KlingelnbergCycloPalloidHypoidGearMeshCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7475,
            )

            return self._parent._cast(
                _7475.KlingelnbergCycloPalloidHypoidGearMeshCompoundAdvancedSystemDeflection
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_advanced_system_deflection(
            self: "ConnectionCompoundAdvancedSystemDeflection._Cast_ConnectionCompoundAdvancedSystemDeflection",
        ) -> "_7478.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7478,
            )

            return self._parent._cast(
                _7478.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundAdvancedSystemDeflection
            )

        @property
        def part_to_part_shear_coupling_connection_compound_advanced_system_deflection(
            self: "ConnectionCompoundAdvancedSystemDeflection._Cast_ConnectionCompoundAdvancedSystemDeflection",
        ) -> "_7486.PartToPartShearCouplingConnectionCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7486,
            )

            return self._parent._cast(
                _7486.PartToPartShearCouplingConnectionCompoundAdvancedSystemDeflection
            )

        @property
        def planetary_connection_compound_advanced_system_deflection(
            self: "ConnectionCompoundAdvancedSystemDeflection._Cast_ConnectionCompoundAdvancedSystemDeflection",
        ) -> "_7488.PlanetaryConnectionCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7488,
            )

            return self._parent._cast(
                _7488.PlanetaryConnectionCompoundAdvancedSystemDeflection
            )

        @property
        def ring_pins_to_disc_connection_compound_advanced_system_deflection(
            self: "ConnectionCompoundAdvancedSystemDeflection._Cast_ConnectionCompoundAdvancedSystemDeflection",
        ) -> "_7495.RingPinsToDiscConnectionCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7495,
            )

            return self._parent._cast(
                _7495.RingPinsToDiscConnectionCompoundAdvancedSystemDeflection
            )

        @property
        def rolling_ring_connection_compound_advanced_system_deflection(
            self: "ConnectionCompoundAdvancedSystemDeflection._Cast_ConnectionCompoundAdvancedSystemDeflection",
        ) -> "_7498.RollingRingConnectionCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7498,
            )

            return self._parent._cast(
                _7498.RollingRingConnectionCompoundAdvancedSystemDeflection
            )

        @property
        def shaft_to_mountable_component_connection_compound_advanced_system_deflection(
            self: "ConnectionCompoundAdvancedSystemDeflection._Cast_ConnectionCompoundAdvancedSystemDeflection",
        ) -> (
            "_7502.ShaftToMountableComponentConnectionCompoundAdvancedSystemDeflection"
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7502,
            )

            return self._parent._cast(
                _7502.ShaftToMountableComponentConnectionCompoundAdvancedSystemDeflection
            )

        @property
        def spiral_bevel_gear_mesh_compound_advanced_system_deflection(
            self: "ConnectionCompoundAdvancedSystemDeflection._Cast_ConnectionCompoundAdvancedSystemDeflection",
        ) -> "_7505.SpiralBevelGearMeshCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7505,
            )

            return self._parent._cast(
                _7505.SpiralBevelGearMeshCompoundAdvancedSystemDeflection
            )

        @property
        def spring_damper_connection_compound_advanced_system_deflection(
            self: "ConnectionCompoundAdvancedSystemDeflection._Cast_ConnectionCompoundAdvancedSystemDeflection",
        ) -> "_7508.SpringDamperConnectionCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7508,
            )

            return self._parent._cast(
                _7508.SpringDamperConnectionCompoundAdvancedSystemDeflection
            )

        @property
        def straight_bevel_diff_gear_mesh_compound_advanced_system_deflection(
            self: "ConnectionCompoundAdvancedSystemDeflection._Cast_ConnectionCompoundAdvancedSystemDeflection",
        ) -> "_7511.StraightBevelDiffGearMeshCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7511,
            )

            return self._parent._cast(
                _7511.StraightBevelDiffGearMeshCompoundAdvancedSystemDeflection
            )

        @property
        def straight_bevel_gear_mesh_compound_advanced_system_deflection(
            self: "ConnectionCompoundAdvancedSystemDeflection._Cast_ConnectionCompoundAdvancedSystemDeflection",
        ) -> "_7514.StraightBevelGearMeshCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7514,
            )

            return self._parent._cast(
                _7514.StraightBevelGearMeshCompoundAdvancedSystemDeflection
            )

        @property
        def torque_converter_connection_compound_advanced_system_deflection(
            self: "ConnectionCompoundAdvancedSystemDeflection._Cast_ConnectionCompoundAdvancedSystemDeflection",
        ) -> "_7523.TorqueConverterConnectionCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7523,
            )

            return self._parent._cast(
                _7523.TorqueConverterConnectionCompoundAdvancedSystemDeflection
            )

        @property
        def worm_gear_mesh_compound_advanced_system_deflection(
            self: "ConnectionCompoundAdvancedSystemDeflection._Cast_ConnectionCompoundAdvancedSystemDeflection",
        ) -> "_7529.WormGearMeshCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7529,
            )

            return self._parent._cast(
                _7529.WormGearMeshCompoundAdvancedSystemDeflection
            )

        @property
        def zerol_bevel_gear_mesh_compound_advanced_system_deflection(
            self: "ConnectionCompoundAdvancedSystemDeflection._Cast_ConnectionCompoundAdvancedSystemDeflection",
        ) -> "_7532.ZerolBevelGearMeshCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7532,
            )

            return self._parent._cast(
                _7532.ZerolBevelGearMeshCompoundAdvancedSystemDeflection
            )

        @property
        def connection_compound_advanced_system_deflection(
            self: "ConnectionCompoundAdvancedSystemDeflection._Cast_ConnectionCompoundAdvancedSystemDeflection",
        ) -> "ConnectionCompoundAdvancedSystemDeflection":
            return self._parent

        def __getattr__(
            self: "ConnectionCompoundAdvancedSystemDeflection._Cast_ConnectionCompoundAdvancedSystemDeflection",
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
        self: Self, instance_to_wrap: "ConnectionCompoundAdvancedSystemDeflection.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_analysis_cases(
        self: Self,
    ) -> "List[_7307.ConnectionAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.ConnectionAdvancedSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ConnectionAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def connection_analysis_cases_ready(
        self: Self,
    ) -> "List[_7307.ConnectionAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.ConnectionAdvancedSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ConnectionAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: Self,
    ) -> "ConnectionCompoundAdvancedSystemDeflection._Cast_ConnectionCompoundAdvancedSystemDeflection":
        return self._Cast_ConnectionCompoundAdvancedSystemDeflection(self)
