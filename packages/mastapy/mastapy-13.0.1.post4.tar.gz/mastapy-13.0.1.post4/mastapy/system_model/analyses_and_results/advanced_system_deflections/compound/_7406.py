"""AbstractAssemblyCompoundAdvancedSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
    _7485,
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_ABSTRACT_ASSEMBLY_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound",
    "AbstractAssemblyCompoundAdvancedSystemDeflection",
)

if TYPE_CHECKING:
    from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
        _7270,
    )
    from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
        _7412,
        _7413,
        _7416,
        _7419,
        _7424,
        _7426,
        _7427,
        _7432,
        _7437,
        _7440,
        _7443,
        _7447,
        _7449,
        _7455,
        _7461,
        _7463,
        _7466,
        _7470,
        _7474,
        _7477,
        _7480,
        _7486,
        _7490,
        _7497,
        _7500,
        _7504,
        _7507,
        _7508,
        _7513,
        _7516,
        _7519,
        _7523,
        _7531,
        _7534,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import _7546, _7543
    from mastapy.system_model.analyses_and_results import _2651


__docformat__ = "restructuredtext en"
__all__ = ("AbstractAssemblyCompoundAdvancedSystemDeflection",)


Self = TypeVar("Self", bound="AbstractAssemblyCompoundAdvancedSystemDeflection")


class AbstractAssemblyCompoundAdvancedSystemDeflection(
    _7485.PartCompoundAdvancedSystemDeflection
):
    """AbstractAssemblyCompoundAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE = _ABSTRACT_ASSEMBLY_COMPOUND_ADVANCED_SYSTEM_DEFLECTION
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_AbstractAssemblyCompoundAdvancedSystemDeflection"
    )

    class _Cast_AbstractAssemblyCompoundAdvancedSystemDeflection:
        """Special nested class for casting AbstractAssemblyCompoundAdvancedSystemDeflection to subclasses."""

        def __init__(
            self: "AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
            parent: "AbstractAssemblyCompoundAdvancedSystemDeflection",
        ):
            self._parent = parent

        @property
        def part_compound_advanced_system_deflection(
            self: "AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
        ) -> "_7485.PartCompoundAdvancedSystemDeflection":
            return self._parent._cast(_7485.PartCompoundAdvancedSystemDeflection)

        @property
        def part_compound_analysis(
            self: "AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
        ) -> "_7546.PartCompoundAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7546

            return self._parent._cast(_7546.PartCompoundAnalysis)

        @property
        def design_entity_compound_analysis(
            self: "AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
        ) -> "_7543.DesignEntityCompoundAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7543

            return self._parent._cast(_7543.DesignEntityCompoundAnalysis)

        @property
        def design_entity_analysis(
            self: "AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def agma_gleason_conical_gear_set_compound_advanced_system_deflection(
            self: "AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
        ) -> "_7412.AGMAGleasonConicalGearSetCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7412,
            )

            return self._parent._cast(
                _7412.AGMAGleasonConicalGearSetCompoundAdvancedSystemDeflection
            )

        @property
        def assembly_compound_advanced_system_deflection(
            self: "AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
        ) -> "_7413.AssemblyCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7413,
            )

            return self._parent._cast(_7413.AssemblyCompoundAdvancedSystemDeflection)

        @property
        def belt_drive_compound_advanced_system_deflection(
            self: "AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
        ) -> "_7416.BeltDriveCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7416,
            )

            return self._parent._cast(_7416.BeltDriveCompoundAdvancedSystemDeflection)

        @property
        def bevel_differential_gear_set_compound_advanced_system_deflection(
            self: "AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
        ) -> "_7419.BevelDifferentialGearSetCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7419,
            )

            return self._parent._cast(
                _7419.BevelDifferentialGearSetCompoundAdvancedSystemDeflection
            )

        @property
        def bevel_gear_set_compound_advanced_system_deflection(
            self: "AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
        ) -> "_7424.BevelGearSetCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7424,
            )

            return self._parent._cast(
                _7424.BevelGearSetCompoundAdvancedSystemDeflection
            )

        @property
        def bolted_joint_compound_advanced_system_deflection(
            self: "AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
        ) -> "_7426.BoltedJointCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7426,
            )

            return self._parent._cast(_7426.BoltedJointCompoundAdvancedSystemDeflection)

        @property
        def clutch_compound_advanced_system_deflection(
            self: "AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
        ) -> "_7427.ClutchCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7427,
            )

            return self._parent._cast(_7427.ClutchCompoundAdvancedSystemDeflection)

        @property
        def concept_coupling_compound_advanced_system_deflection(
            self: "AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
        ) -> "_7432.ConceptCouplingCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7432,
            )

            return self._parent._cast(
                _7432.ConceptCouplingCompoundAdvancedSystemDeflection
            )

        @property
        def concept_gear_set_compound_advanced_system_deflection(
            self: "AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
        ) -> "_7437.ConceptGearSetCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7437,
            )

            return self._parent._cast(
                _7437.ConceptGearSetCompoundAdvancedSystemDeflection
            )

        @property
        def conical_gear_set_compound_advanced_system_deflection(
            self: "AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
        ) -> "_7440.ConicalGearSetCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7440,
            )

            return self._parent._cast(
                _7440.ConicalGearSetCompoundAdvancedSystemDeflection
            )

        @property
        def coupling_compound_advanced_system_deflection(
            self: "AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
        ) -> "_7443.CouplingCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7443,
            )

            return self._parent._cast(_7443.CouplingCompoundAdvancedSystemDeflection)

        @property
        def cvt_compound_advanced_system_deflection(
            self: "AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
        ) -> "_7447.CVTCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7447,
            )

            return self._parent._cast(_7447.CVTCompoundAdvancedSystemDeflection)

        @property
        def cycloidal_assembly_compound_advanced_system_deflection(
            self: "AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
        ) -> "_7449.CycloidalAssemblyCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7449,
            )

            return self._parent._cast(
                _7449.CycloidalAssemblyCompoundAdvancedSystemDeflection
            )

        @property
        def cylindrical_gear_set_compound_advanced_system_deflection(
            self: "AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
        ) -> "_7455.CylindricalGearSetCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7455,
            )

            return self._parent._cast(
                _7455.CylindricalGearSetCompoundAdvancedSystemDeflection
            )

        @property
        def face_gear_set_compound_advanced_system_deflection(
            self: "AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
        ) -> "_7461.FaceGearSetCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7461,
            )

            return self._parent._cast(_7461.FaceGearSetCompoundAdvancedSystemDeflection)

        @property
        def flexible_pin_assembly_compound_advanced_system_deflection(
            self: "AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
        ) -> "_7463.FlexiblePinAssemblyCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7463,
            )

            return self._parent._cast(
                _7463.FlexiblePinAssemblyCompoundAdvancedSystemDeflection
            )

        @property
        def gear_set_compound_advanced_system_deflection(
            self: "AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
        ) -> "_7466.GearSetCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7466,
            )

            return self._parent._cast(_7466.GearSetCompoundAdvancedSystemDeflection)

        @property
        def hypoid_gear_set_compound_advanced_system_deflection(
            self: "AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
        ) -> "_7470.HypoidGearSetCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7470,
            )

            return self._parent._cast(
                _7470.HypoidGearSetCompoundAdvancedSystemDeflection
            )

        @property
        def klingelnberg_cyclo_palloid_conical_gear_set_compound_advanced_system_deflection(
            self: "AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
        ) -> "_7474.KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7474,
            )

            return self._parent._cast(
                _7474.KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedSystemDeflection
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_advanced_system_deflection(
            self: "AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
        ) -> "_7477.KlingelnbergCycloPalloidHypoidGearSetCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7477,
            )

            return self._parent._cast(
                _7477.KlingelnbergCycloPalloidHypoidGearSetCompoundAdvancedSystemDeflection
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_advanced_system_deflection(
            self: "AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
        ) -> "_7480.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7480,
            )

            return self._parent._cast(
                _7480.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection
            )

        @property
        def part_to_part_shear_coupling_compound_advanced_system_deflection(
            self: "AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
        ) -> "_7486.PartToPartShearCouplingCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7486,
            )

            return self._parent._cast(
                _7486.PartToPartShearCouplingCompoundAdvancedSystemDeflection
            )

        @property
        def planetary_gear_set_compound_advanced_system_deflection(
            self: "AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
        ) -> "_7490.PlanetaryGearSetCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7490,
            )

            return self._parent._cast(
                _7490.PlanetaryGearSetCompoundAdvancedSystemDeflection
            )

        @property
        def rolling_ring_assembly_compound_advanced_system_deflection(
            self: "AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
        ) -> "_7497.RollingRingAssemblyCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7497,
            )

            return self._parent._cast(
                _7497.RollingRingAssemblyCompoundAdvancedSystemDeflection
            )

        @property
        def root_assembly_compound_advanced_system_deflection(
            self: "AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
        ) -> "_7500.RootAssemblyCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7500,
            )

            return self._parent._cast(
                _7500.RootAssemblyCompoundAdvancedSystemDeflection
            )

        @property
        def specialised_assembly_compound_advanced_system_deflection(
            self: "AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
        ) -> "_7504.SpecialisedAssemblyCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7504,
            )

            return self._parent._cast(
                _7504.SpecialisedAssemblyCompoundAdvancedSystemDeflection
            )

        @property
        def spiral_bevel_gear_set_compound_advanced_system_deflection(
            self: "AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
        ) -> "_7507.SpiralBevelGearSetCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7507,
            )

            return self._parent._cast(
                _7507.SpiralBevelGearSetCompoundAdvancedSystemDeflection
            )

        @property
        def spring_damper_compound_advanced_system_deflection(
            self: "AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
        ) -> "_7508.SpringDamperCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7508,
            )

            return self._parent._cast(
                _7508.SpringDamperCompoundAdvancedSystemDeflection
            )

        @property
        def straight_bevel_diff_gear_set_compound_advanced_system_deflection(
            self: "AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
        ) -> "_7513.StraightBevelDiffGearSetCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7513,
            )

            return self._parent._cast(
                _7513.StraightBevelDiffGearSetCompoundAdvancedSystemDeflection
            )

        @property
        def straight_bevel_gear_set_compound_advanced_system_deflection(
            self: "AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
        ) -> "_7516.StraightBevelGearSetCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7516,
            )

            return self._parent._cast(
                _7516.StraightBevelGearSetCompoundAdvancedSystemDeflection
            )

        @property
        def synchroniser_compound_advanced_system_deflection(
            self: "AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
        ) -> "_7519.SynchroniserCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7519,
            )

            return self._parent._cast(
                _7519.SynchroniserCompoundAdvancedSystemDeflection
            )

        @property
        def torque_converter_compound_advanced_system_deflection(
            self: "AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
        ) -> "_7523.TorqueConverterCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7523,
            )

            return self._parent._cast(
                _7523.TorqueConverterCompoundAdvancedSystemDeflection
            )

        @property
        def worm_gear_set_compound_advanced_system_deflection(
            self: "AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
        ) -> "_7531.WormGearSetCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7531,
            )

            return self._parent._cast(_7531.WormGearSetCompoundAdvancedSystemDeflection)

        @property
        def zerol_bevel_gear_set_compound_advanced_system_deflection(
            self: "AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
        ) -> "_7534.ZerolBevelGearSetCompoundAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7534,
            )

            return self._parent._cast(
                _7534.ZerolBevelGearSetCompoundAdvancedSystemDeflection
            )

        @property
        def abstract_assembly_compound_advanced_system_deflection(
            self: "AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
        ) -> "AbstractAssemblyCompoundAdvancedSystemDeflection":
            return self._parent

        def __getattr__(
            self: "AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
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
        instance_to_wrap: "AbstractAssemblyCompoundAdvancedSystemDeflection.TYPE",
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_analysis_cases(
        self: Self,
    ) -> "List[_7270.AbstractAssemblyAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.AbstractAssemblyAdvancedSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def assembly_analysis_cases_ready(
        self: Self,
    ) -> "List[_7270.AbstractAssemblyAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.AbstractAssemblyAdvancedSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: Self,
    ) -> "AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection":
        return self._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection(self)
