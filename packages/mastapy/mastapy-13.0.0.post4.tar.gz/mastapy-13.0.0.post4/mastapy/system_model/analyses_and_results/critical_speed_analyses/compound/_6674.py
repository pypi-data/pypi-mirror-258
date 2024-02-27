"""AbstractAssemblyCompoundCriticalSpeedAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import (
    _6753,
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_ABSTRACT_ASSEMBLY_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound",
    "AbstractAssemblyCompoundCriticalSpeedAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6542
    from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import (
        _6680,
        _6681,
        _6684,
        _6687,
        _6692,
        _6694,
        _6695,
        _6700,
        _6705,
        _6708,
        _6711,
        _6715,
        _6717,
        _6723,
        _6729,
        _6731,
        _6734,
        _6738,
        _6742,
        _6745,
        _6748,
        _6754,
        _6758,
        _6765,
        _6768,
        _6772,
        _6775,
        _6776,
        _6781,
        _6784,
        _6787,
        _6791,
        _6799,
        _6802,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import _7545, _7542
    from mastapy.system_model.analyses_and_results import _2651


__docformat__ = "restructuredtext en"
__all__ = ("AbstractAssemblyCompoundCriticalSpeedAnalysis",)


Self = TypeVar("Self", bound="AbstractAssemblyCompoundCriticalSpeedAnalysis")


class AbstractAssemblyCompoundCriticalSpeedAnalysis(
    _6753.PartCompoundCriticalSpeedAnalysis
):
    """AbstractAssemblyCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE = _ABSTRACT_ASSEMBLY_COMPOUND_CRITICAL_SPEED_ANALYSIS
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis"
    )

    class _Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis:
        """Special nested class for casting AbstractAssemblyCompoundCriticalSpeedAnalysis to subclasses."""

        def __init__(
            self: "AbstractAssemblyCompoundCriticalSpeedAnalysis._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis",
            parent: "AbstractAssemblyCompoundCriticalSpeedAnalysis",
        ):
            self._parent = parent

        @property
        def part_compound_critical_speed_analysis(
            self: "AbstractAssemblyCompoundCriticalSpeedAnalysis._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis",
        ) -> "_6753.PartCompoundCriticalSpeedAnalysis":
            return self._parent._cast(_6753.PartCompoundCriticalSpeedAnalysis)

        @property
        def part_compound_analysis(
            self: "AbstractAssemblyCompoundCriticalSpeedAnalysis._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis",
        ) -> "_7545.PartCompoundAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7545

            return self._parent._cast(_7545.PartCompoundAnalysis)

        @property
        def design_entity_compound_analysis(
            self: "AbstractAssemblyCompoundCriticalSpeedAnalysis._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis",
        ) -> "_7542.DesignEntityCompoundAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7542

            return self._parent._cast(_7542.DesignEntityCompoundAnalysis)

        @property
        def design_entity_analysis(
            self: "AbstractAssemblyCompoundCriticalSpeedAnalysis._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def agma_gleason_conical_gear_set_compound_critical_speed_analysis(
            self: "AbstractAssemblyCompoundCriticalSpeedAnalysis._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis",
        ) -> "_6680.AGMAGleasonConicalGearSetCompoundCriticalSpeedAnalysis":
            from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import (
                _6680,
            )

            return self._parent._cast(
                _6680.AGMAGleasonConicalGearSetCompoundCriticalSpeedAnalysis
            )

        @property
        def assembly_compound_critical_speed_analysis(
            self: "AbstractAssemblyCompoundCriticalSpeedAnalysis._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis",
        ) -> "_6681.AssemblyCompoundCriticalSpeedAnalysis":
            from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import (
                _6681,
            )

            return self._parent._cast(_6681.AssemblyCompoundCriticalSpeedAnalysis)

        @property
        def belt_drive_compound_critical_speed_analysis(
            self: "AbstractAssemblyCompoundCriticalSpeedAnalysis._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis",
        ) -> "_6684.BeltDriveCompoundCriticalSpeedAnalysis":
            from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import (
                _6684,
            )

            return self._parent._cast(_6684.BeltDriveCompoundCriticalSpeedAnalysis)

        @property
        def bevel_differential_gear_set_compound_critical_speed_analysis(
            self: "AbstractAssemblyCompoundCriticalSpeedAnalysis._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis",
        ) -> "_6687.BevelDifferentialGearSetCompoundCriticalSpeedAnalysis":
            from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import (
                _6687,
            )

            return self._parent._cast(
                _6687.BevelDifferentialGearSetCompoundCriticalSpeedAnalysis
            )

        @property
        def bevel_gear_set_compound_critical_speed_analysis(
            self: "AbstractAssemblyCompoundCriticalSpeedAnalysis._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis",
        ) -> "_6692.BevelGearSetCompoundCriticalSpeedAnalysis":
            from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import (
                _6692,
            )

            return self._parent._cast(_6692.BevelGearSetCompoundCriticalSpeedAnalysis)

        @property
        def bolted_joint_compound_critical_speed_analysis(
            self: "AbstractAssemblyCompoundCriticalSpeedAnalysis._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis",
        ) -> "_6694.BoltedJointCompoundCriticalSpeedAnalysis":
            from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import (
                _6694,
            )

            return self._parent._cast(_6694.BoltedJointCompoundCriticalSpeedAnalysis)

        @property
        def clutch_compound_critical_speed_analysis(
            self: "AbstractAssemblyCompoundCriticalSpeedAnalysis._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis",
        ) -> "_6695.ClutchCompoundCriticalSpeedAnalysis":
            from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import (
                _6695,
            )

            return self._parent._cast(_6695.ClutchCompoundCriticalSpeedAnalysis)

        @property
        def concept_coupling_compound_critical_speed_analysis(
            self: "AbstractAssemblyCompoundCriticalSpeedAnalysis._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis",
        ) -> "_6700.ConceptCouplingCompoundCriticalSpeedAnalysis":
            from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import (
                _6700,
            )

            return self._parent._cast(
                _6700.ConceptCouplingCompoundCriticalSpeedAnalysis
            )

        @property
        def concept_gear_set_compound_critical_speed_analysis(
            self: "AbstractAssemblyCompoundCriticalSpeedAnalysis._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis",
        ) -> "_6705.ConceptGearSetCompoundCriticalSpeedAnalysis":
            from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import (
                _6705,
            )

            return self._parent._cast(_6705.ConceptGearSetCompoundCriticalSpeedAnalysis)

        @property
        def conical_gear_set_compound_critical_speed_analysis(
            self: "AbstractAssemblyCompoundCriticalSpeedAnalysis._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis",
        ) -> "_6708.ConicalGearSetCompoundCriticalSpeedAnalysis":
            from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import (
                _6708,
            )

            return self._parent._cast(_6708.ConicalGearSetCompoundCriticalSpeedAnalysis)

        @property
        def coupling_compound_critical_speed_analysis(
            self: "AbstractAssemblyCompoundCriticalSpeedAnalysis._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis",
        ) -> "_6711.CouplingCompoundCriticalSpeedAnalysis":
            from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import (
                _6711,
            )

            return self._parent._cast(_6711.CouplingCompoundCriticalSpeedAnalysis)

        @property
        def cvt_compound_critical_speed_analysis(
            self: "AbstractAssemblyCompoundCriticalSpeedAnalysis._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis",
        ) -> "_6715.CVTCompoundCriticalSpeedAnalysis":
            from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import (
                _6715,
            )

            return self._parent._cast(_6715.CVTCompoundCriticalSpeedAnalysis)

        @property
        def cycloidal_assembly_compound_critical_speed_analysis(
            self: "AbstractAssemblyCompoundCriticalSpeedAnalysis._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis",
        ) -> "_6717.CycloidalAssemblyCompoundCriticalSpeedAnalysis":
            from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import (
                _6717,
            )

            return self._parent._cast(
                _6717.CycloidalAssemblyCompoundCriticalSpeedAnalysis
            )

        @property
        def cylindrical_gear_set_compound_critical_speed_analysis(
            self: "AbstractAssemblyCompoundCriticalSpeedAnalysis._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis",
        ) -> "_6723.CylindricalGearSetCompoundCriticalSpeedAnalysis":
            from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import (
                _6723,
            )

            return self._parent._cast(
                _6723.CylindricalGearSetCompoundCriticalSpeedAnalysis
            )

        @property
        def face_gear_set_compound_critical_speed_analysis(
            self: "AbstractAssemblyCompoundCriticalSpeedAnalysis._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis",
        ) -> "_6729.FaceGearSetCompoundCriticalSpeedAnalysis":
            from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import (
                _6729,
            )

            return self._parent._cast(_6729.FaceGearSetCompoundCriticalSpeedAnalysis)

        @property
        def flexible_pin_assembly_compound_critical_speed_analysis(
            self: "AbstractAssemblyCompoundCriticalSpeedAnalysis._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis",
        ) -> "_6731.FlexiblePinAssemblyCompoundCriticalSpeedAnalysis":
            from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import (
                _6731,
            )

            return self._parent._cast(
                _6731.FlexiblePinAssemblyCompoundCriticalSpeedAnalysis
            )

        @property
        def gear_set_compound_critical_speed_analysis(
            self: "AbstractAssemblyCompoundCriticalSpeedAnalysis._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis",
        ) -> "_6734.GearSetCompoundCriticalSpeedAnalysis":
            from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import (
                _6734,
            )

            return self._parent._cast(_6734.GearSetCompoundCriticalSpeedAnalysis)

        @property
        def hypoid_gear_set_compound_critical_speed_analysis(
            self: "AbstractAssemblyCompoundCriticalSpeedAnalysis._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis",
        ) -> "_6738.HypoidGearSetCompoundCriticalSpeedAnalysis":
            from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import (
                _6738,
            )

            return self._parent._cast(_6738.HypoidGearSetCompoundCriticalSpeedAnalysis)

        @property
        def klingelnberg_cyclo_palloid_conical_gear_set_compound_critical_speed_analysis(
            self: "AbstractAssemblyCompoundCriticalSpeedAnalysis._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis",
        ) -> (
            "_6742.KlingelnbergCycloPalloidConicalGearSetCompoundCriticalSpeedAnalysis"
        ):
            from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import (
                _6742,
            )

            return self._parent._cast(
                _6742.KlingelnbergCycloPalloidConicalGearSetCompoundCriticalSpeedAnalysis
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_critical_speed_analysis(
            self: "AbstractAssemblyCompoundCriticalSpeedAnalysis._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis",
        ) -> "_6745.KlingelnbergCycloPalloidHypoidGearSetCompoundCriticalSpeedAnalysis":
            from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import (
                _6745,
            )

            return self._parent._cast(
                _6745.KlingelnbergCycloPalloidHypoidGearSetCompoundCriticalSpeedAnalysis
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_critical_speed_analysis(
            self: "AbstractAssemblyCompoundCriticalSpeedAnalysis._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis",
        ) -> "_6748.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundCriticalSpeedAnalysis":
            from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import (
                _6748,
            )

            return self._parent._cast(
                _6748.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundCriticalSpeedAnalysis
            )

        @property
        def part_to_part_shear_coupling_compound_critical_speed_analysis(
            self: "AbstractAssemblyCompoundCriticalSpeedAnalysis._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis",
        ) -> "_6754.PartToPartShearCouplingCompoundCriticalSpeedAnalysis":
            from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import (
                _6754,
            )

            return self._parent._cast(
                _6754.PartToPartShearCouplingCompoundCriticalSpeedAnalysis
            )

        @property
        def planetary_gear_set_compound_critical_speed_analysis(
            self: "AbstractAssemblyCompoundCriticalSpeedAnalysis._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis",
        ) -> "_6758.PlanetaryGearSetCompoundCriticalSpeedAnalysis":
            from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import (
                _6758,
            )

            return self._parent._cast(
                _6758.PlanetaryGearSetCompoundCriticalSpeedAnalysis
            )

        @property
        def rolling_ring_assembly_compound_critical_speed_analysis(
            self: "AbstractAssemblyCompoundCriticalSpeedAnalysis._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis",
        ) -> "_6765.RollingRingAssemblyCompoundCriticalSpeedAnalysis":
            from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import (
                _6765,
            )

            return self._parent._cast(
                _6765.RollingRingAssemblyCompoundCriticalSpeedAnalysis
            )

        @property
        def root_assembly_compound_critical_speed_analysis(
            self: "AbstractAssemblyCompoundCriticalSpeedAnalysis._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis",
        ) -> "_6768.RootAssemblyCompoundCriticalSpeedAnalysis":
            from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import (
                _6768,
            )

            return self._parent._cast(_6768.RootAssemblyCompoundCriticalSpeedAnalysis)

        @property
        def specialised_assembly_compound_critical_speed_analysis(
            self: "AbstractAssemblyCompoundCriticalSpeedAnalysis._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis",
        ) -> "_6772.SpecialisedAssemblyCompoundCriticalSpeedAnalysis":
            from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import (
                _6772,
            )

            return self._parent._cast(
                _6772.SpecialisedAssemblyCompoundCriticalSpeedAnalysis
            )

        @property
        def spiral_bevel_gear_set_compound_critical_speed_analysis(
            self: "AbstractAssemblyCompoundCriticalSpeedAnalysis._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis",
        ) -> "_6775.SpiralBevelGearSetCompoundCriticalSpeedAnalysis":
            from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import (
                _6775,
            )

            return self._parent._cast(
                _6775.SpiralBevelGearSetCompoundCriticalSpeedAnalysis
            )

        @property
        def spring_damper_compound_critical_speed_analysis(
            self: "AbstractAssemblyCompoundCriticalSpeedAnalysis._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis",
        ) -> "_6776.SpringDamperCompoundCriticalSpeedAnalysis":
            from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import (
                _6776,
            )

            return self._parent._cast(_6776.SpringDamperCompoundCriticalSpeedAnalysis)

        @property
        def straight_bevel_diff_gear_set_compound_critical_speed_analysis(
            self: "AbstractAssemblyCompoundCriticalSpeedAnalysis._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis",
        ) -> "_6781.StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis":
            from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import (
                _6781,
            )

            return self._parent._cast(
                _6781.StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis
            )

        @property
        def straight_bevel_gear_set_compound_critical_speed_analysis(
            self: "AbstractAssemblyCompoundCriticalSpeedAnalysis._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis",
        ) -> "_6784.StraightBevelGearSetCompoundCriticalSpeedAnalysis":
            from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import (
                _6784,
            )

            return self._parent._cast(
                _6784.StraightBevelGearSetCompoundCriticalSpeedAnalysis
            )

        @property
        def synchroniser_compound_critical_speed_analysis(
            self: "AbstractAssemblyCompoundCriticalSpeedAnalysis._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis",
        ) -> "_6787.SynchroniserCompoundCriticalSpeedAnalysis":
            from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import (
                _6787,
            )

            return self._parent._cast(_6787.SynchroniserCompoundCriticalSpeedAnalysis)

        @property
        def torque_converter_compound_critical_speed_analysis(
            self: "AbstractAssemblyCompoundCriticalSpeedAnalysis._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis",
        ) -> "_6791.TorqueConverterCompoundCriticalSpeedAnalysis":
            from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import (
                _6791,
            )

            return self._parent._cast(
                _6791.TorqueConverterCompoundCriticalSpeedAnalysis
            )

        @property
        def worm_gear_set_compound_critical_speed_analysis(
            self: "AbstractAssemblyCompoundCriticalSpeedAnalysis._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis",
        ) -> "_6799.WormGearSetCompoundCriticalSpeedAnalysis":
            from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import (
                _6799,
            )

            return self._parent._cast(_6799.WormGearSetCompoundCriticalSpeedAnalysis)

        @property
        def zerol_bevel_gear_set_compound_critical_speed_analysis(
            self: "AbstractAssemblyCompoundCriticalSpeedAnalysis._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis",
        ) -> "_6802.ZerolBevelGearSetCompoundCriticalSpeedAnalysis":
            from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import (
                _6802,
            )

            return self._parent._cast(
                _6802.ZerolBevelGearSetCompoundCriticalSpeedAnalysis
            )

        @property
        def abstract_assembly_compound_critical_speed_analysis(
            self: "AbstractAssemblyCompoundCriticalSpeedAnalysis._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis",
        ) -> "AbstractAssemblyCompoundCriticalSpeedAnalysis":
            return self._parent

        def __getattr__(
            self: "AbstractAssemblyCompoundCriticalSpeedAnalysis._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis",
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
        instance_to_wrap: "AbstractAssemblyCompoundCriticalSpeedAnalysis.TYPE",
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_analysis_cases(
        self: Self,
    ) -> "List[_6542.AbstractAssemblyCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.AbstractAssemblyCriticalSpeedAnalysis]

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
    ) -> "List[_6542.AbstractAssemblyCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.AbstractAssemblyCriticalSpeedAnalysis]

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
    ) -> "AbstractAssemblyCompoundCriticalSpeedAnalysis._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis":
        return self._Cast_AbstractAssemblyCompoundCriticalSpeedAnalysis(self)
