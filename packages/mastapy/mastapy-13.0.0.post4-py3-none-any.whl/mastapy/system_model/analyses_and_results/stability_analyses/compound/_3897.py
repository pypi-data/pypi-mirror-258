"""AbstractAssemblyCompoundStabilityAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import conversion
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3976
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_ABSTRACT_ASSEMBLY_COMPOUND_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound",
    "AbstractAssemblyCompoundStabilityAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.analyses_and_results.stability_analyses import _3763
    from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
        _3903,
        _3904,
        _3907,
        _3910,
        _3915,
        _3917,
        _3918,
        _3923,
        _3928,
        _3931,
        _3934,
        _3938,
        _3940,
        _3946,
        _3952,
        _3954,
        _3957,
        _3961,
        _3965,
        _3968,
        _3971,
        _3977,
        _3981,
        _3988,
        _3991,
        _3995,
        _3998,
        _3999,
        _4004,
        _4007,
        _4010,
        _4014,
        _4022,
        _4025,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import _7545, _7542
    from mastapy.system_model.analyses_and_results import _2651


__docformat__ = "restructuredtext en"
__all__ = ("AbstractAssemblyCompoundStabilityAnalysis",)


Self = TypeVar("Self", bound="AbstractAssemblyCompoundStabilityAnalysis")


class AbstractAssemblyCompoundStabilityAnalysis(_3976.PartCompoundStabilityAnalysis):
    """AbstractAssemblyCompoundStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _ABSTRACT_ASSEMBLY_COMPOUND_STABILITY_ANALYSIS
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_AbstractAssemblyCompoundStabilityAnalysis"
    )

    class _Cast_AbstractAssemblyCompoundStabilityAnalysis:
        """Special nested class for casting AbstractAssemblyCompoundStabilityAnalysis to subclasses."""

        def __init__(
            self: "AbstractAssemblyCompoundStabilityAnalysis._Cast_AbstractAssemblyCompoundStabilityAnalysis",
            parent: "AbstractAssemblyCompoundStabilityAnalysis",
        ):
            self._parent = parent

        @property
        def part_compound_stability_analysis(
            self: "AbstractAssemblyCompoundStabilityAnalysis._Cast_AbstractAssemblyCompoundStabilityAnalysis",
        ) -> "_3976.PartCompoundStabilityAnalysis":
            return self._parent._cast(_3976.PartCompoundStabilityAnalysis)

        @property
        def part_compound_analysis(
            self: "AbstractAssemblyCompoundStabilityAnalysis._Cast_AbstractAssemblyCompoundStabilityAnalysis",
        ) -> "_7545.PartCompoundAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7545

            return self._parent._cast(_7545.PartCompoundAnalysis)

        @property
        def design_entity_compound_analysis(
            self: "AbstractAssemblyCompoundStabilityAnalysis._Cast_AbstractAssemblyCompoundStabilityAnalysis",
        ) -> "_7542.DesignEntityCompoundAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7542

            return self._parent._cast(_7542.DesignEntityCompoundAnalysis)

        @property
        def design_entity_analysis(
            self: "AbstractAssemblyCompoundStabilityAnalysis._Cast_AbstractAssemblyCompoundStabilityAnalysis",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def agma_gleason_conical_gear_set_compound_stability_analysis(
            self: "AbstractAssemblyCompoundStabilityAnalysis._Cast_AbstractAssemblyCompoundStabilityAnalysis",
        ) -> "_3903.AGMAGleasonConicalGearSetCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3903,
            )

            return self._parent._cast(
                _3903.AGMAGleasonConicalGearSetCompoundStabilityAnalysis
            )

        @property
        def assembly_compound_stability_analysis(
            self: "AbstractAssemblyCompoundStabilityAnalysis._Cast_AbstractAssemblyCompoundStabilityAnalysis",
        ) -> "_3904.AssemblyCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3904,
            )

            return self._parent._cast(_3904.AssemblyCompoundStabilityAnalysis)

        @property
        def belt_drive_compound_stability_analysis(
            self: "AbstractAssemblyCompoundStabilityAnalysis._Cast_AbstractAssemblyCompoundStabilityAnalysis",
        ) -> "_3907.BeltDriveCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3907,
            )

            return self._parent._cast(_3907.BeltDriveCompoundStabilityAnalysis)

        @property
        def bevel_differential_gear_set_compound_stability_analysis(
            self: "AbstractAssemblyCompoundStabilityAnalysis._Cast_AbstractAssemblyCompoundStabilityAnalysis",
        ) -> "_3910.BevelDifferentialGearSetCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3910,
            )

            return self._parent._cast(
                _3910.BevelDifferentialGearSetCompoundStabilityAnalysis
            )

        @property
        def bevel_gear_set_compound_stability_analysis(
            self: "AbstractAssemblyCompoundStabilityAnalysis._Cast_AbstractAssemblyCompoundStabilityAnalysis",
        ) -> "_3915.BevelGearSetCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3915,
            )

            return self._parent._cast(_3915.BevelGearSetCompoundStabilityAnalysis)

        @property
        def bolted_joint_compound_stability_analysis(
            self: "AbstractAssemblyCompoundStabilityAnalysis._Cast_AbstractAssemblyCompoundStabilityAnalysis",
        ) -> "_3917.BoltedJointCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3917,
            )

            return self._parent._cast(_3917.BoltedJointCompoundStabilityAnalysis)

        @property
        def clutch_compound_stability_analysis(
            self: "AbstractAssemblyCompoundStabilityAnalysis._Cast_AbstractAssemblyCompoundStabilityAnalysis",
        ) -> "_3918.ClutchCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3918,
            )

            return self._parent._cast(_3918.ClutchCompoundStabilityAnalysis)

        @property
        def concept_coupling_compound_stability_analysis(
            self: "AbstractAssemblyCompoundStabilityAnalysis._Cast_AbstractAssemblyCompoundStabilityAnalysis",
        ) -> "_3923.ConceptCouplingCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3923,
            )

            return self._parent._cast(_3923.ConceptCouplingCompoundStabilityAnalysis)

        @property
        def concept_gear_set_compound_stability_analysis(
            self: "AbstractAssemblyCompoundStabilityAnalysis._Cast_AbstractAssemblyCompoundStabilityAnalysis",
        ) -> "_3928.ConceptGearSetCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3928,
            )

            return self._parent._cast(_3928.ConceptGearSetCompoundStabilityAnalysis)

        @property
        def conical_gear_set_compound_stability_analysis(
            self: "AbstractAssemblyCompoundStabilityAnalysis._Cast_AbstractAssemblyCompoundStabilityAnalysis",
        ) -> "_3931.ConicalGearSetCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3931,
            )

            return self._parent._cast(_3931.ConicalGearSetCompoundStabilityAnalysis)

        @property
        def coupling_compound_stability_analysis(
            self: "AbstractAssemblyCompoundStabilityAnalysis._Cast_AbstractAssemblyCompoundStabilityAnalysis",
        ) -> "_3934.CouplingCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3934,
            )

            return self._parent._cast(_3934.CouplingCompoundStabilityAnalysis)

        @property
        def cvt_compound_stability_analysis(
            self: "AbstractAssemblyCompoundStabilityAnalysis._Cast_AbstractAssemblyCompoundStabilityAnalysis",
        ) -> "_3938.CVTCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3938,
            )

            return self._parent._cast(_3938.CVTCompoundStabilityAnalysis)

        @property
        def cycloidal_assembly_compound_stability_analysis(
            self: "AbstractAssemblyCompoundStabilityAnalysis._Cast_AbstractAssemblyCompoundStabilityAnalysis",
        ) -> "_3940.CycloidalAssemblyCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3940,
            )

            return self._parent._cast(_3940.CycloidalAssemblyCompoundStabilityAnalysis)

        @property
        def cylindrical_gear_set_compound_stability_analysis(
            self: "AbstractAssemblyCompoundStabilityAnalysis._Cast_AbstractAssemblyCompoundStabilityAnalysis",
        ) -> "_3946.CylindricalGearSetCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3946,
            )

            return self._parent._cast(_3946.CylindricalGearSetCompoundStabilityAnalysis)

        @property
        def face_gear_set_compound_stability_analysis(
            self: "AbstractAssemblyCompoundStabilityAnalysis._Cast_AbstractAssemblyCompoundStabilityAnalysis",
        ) -> "_3952.FaceGearSetCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3952,
            )

            return self._parent._cast(_3952.FaceGearSetCompoundStabilityAnalysis)

        @property
        def flexible_pin_assembly_compound_stability_analysis(
            self: "AbstractAssemblyCompoundStabilityAnalysis._Cast_AbstractAssemblyCompoundStabilityAnalysis",
        ) -> "_3954.FlexiblePinAssemblyCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3954,
            )

            return self._parent._cast(
                _3954.FlexiblePinAssemblyCompoundStabilityAnalysis
            )

        @property
        def gear_set_compound_stability_analysis(
            self: "AbstractAssemblyCompoundStabilityAnalysis._Cast_AbstractAssemblyCompoundStabilityAnalysis",
        ) -> "_3957.GearSetCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3957,
            )

            return self._parent._cast(_3957.GearSetCompoundStabilityAnalysis)

        @property
        def hypoid_gear_set_compound_stability_analysis(
            self: "AbstractAssemblyCompoundStabilityAnalysis._Cast_AbstractAssemblyCompoundStabilityAnalysis",
        ) -> "_3961.HypoidGearSetCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3961,
            )

            return self._parent._cast(_3961.HypoidGearSetCompoundStabilityAnalysis)

        @property
        def klingelnberg_cyclo_palloid_conical_gear_set_compound_stability_analysis(
            self: "AbstractAssemblyCompoundStabilityAnalysis._Cast_AbstractAssemblyCompoundStabilityAnalysis",
        ) -> "_3965.KlingelnbergCycloPalloidConicalGearSetCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3965,
            )

            return self._parent._cast(
                _3965.KlingelnbergCycloPalloidConicalGearSetCompoundStabilityAnalysis
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_stability_analysis(
            self: "AbstractAssemblyCompoundStabilityAnalysis._Cast_AbstractAssemblyCompoundStabilityAnalysis",
        ) -> "_3968.KlingelnbergCycloPalloidHypoidGearSetCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3968,
            )

            return self._parent._cast(
                _3968.KlingelnbergCycloPalloidHypoidGearSetCompoundStabilityAnalysis
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_stability_analysis(
            self: "AbstractAssemblyCompoundStabilityAnalysis._Cast_AbstractAssemblyCompoundStabilityAnalysis",
        ) -> (
            "_3971.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundStabilityAnalysis"
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3971,
            )

            return self._parent._cast(
                _3971.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundStabilityAnalysis
            )

        @property
        def part_to_part_shear_coupling_compound_stability_analysis(
            self: "AbstractAssemblyCompoundStabilityAnalysis._Cast_AbstractAssemblyCompoundStabilityAnalysis",
        ) -> "_3977.PartToPartShearCouplingCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3977,
            )

            return self._parent._cast(
                _3977.PartToPartShearCouplingCompoundStabilityAnalysis
            )

        @property
        def planetary_gear_set_compound_stability_analysis(
            self: "AbstractAssemblyCompoundStabilityAnalysis._Cast_AbstractAssemblyCompoundStabilityAnalysis",
        ) -> "_3981.PlanetaryGearSetCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3981,
            )

            return self._parent._cast(_3981.PlanetaryGearSetCompoundStabilityAnalysis)

        @property
        def rolling_ring_assembly_compound_stability_analysis(
            self: "AbstractAssemblyCompoundStabilityAnalysis._Cast_AbstractAssemblyCompoundStabilityAnalysis",
        ) -> "_3988.RollingRingAssemblyCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3988,
            )

            return self._parent._cast(
                _3988.RollingRingAssemblyCompoundStabilityAnalysis
            )

        @property
        def root_assembly_compound_stability_analysis(
            self: "AbstractAssemblyCompoundStabilityAnalysis._Cast_AbstractAssemblyCompoundStabilityAnalysis",
        ) -> "_3991.RootAssemblyCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3991,
            )

            return self._parent._cast(_3991.RootAssemblyCompoundStabilityAnalysis)

        @property
        def specialised_assembly_compound_stability_analysis(
            self: "AbstractAssemblyCompoundStabilityAnalysis._Cast_AbstractAssemblyCompoundStabilityAnalysis",
        ) -> "_3995.SpecialisedAssemblyCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3995,
            )

            return self._parent._cast(
                _3995.SpecialisedAssemblyCompoundStabilityAnalysis
            )

        @property
        def spiral_bevel_gear_set_compound_stability_analysis(
            self: "AbstractAssemblyCompoundStabilityAnalysis._Cast_AbstractAssemblyCompoundStabilityAnalysis",
        ) -> "_3998.SpiralBevelGearSetCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3998,
            )

            return self._parent._cast(_3998.SpiralBevelGearSetCompoundStabilityAnalysis)

        @property
        def spring_damper_compound_stability_analysis(
            self: "AbstractAssemblyCompoundStabilityAnalysis._Cast_AbstractAssemblyCompoundStabilityAnalysis",
        ) -> "_3999.SpringDamperCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3999,
            )

            return self._parent._cast(_3999.SpringDamperCompoundStabilityAnalysis)

        @property
        def straight_bevel_diff_gear_set_compound_stability_analysis(
            self: "AbstractAssemblyCompoundStabilityAnalysis._Cast_AbstractAssemblyCompoundStabilityAnalysis",
        ) -> "_4004.StraightBevelDiffGearSetCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _4004,
            )

            return self._parent._cast(
                _4004.StraightBevelDiffGearSetCompoundStabilityAnalysis
            )

        @property
        def straight_bevel_gear_set_compound_stability_analysis(
            self: "AbstractAssemblyCompoundStabilityAnalysis._Cast_AbstractAssemblyCompoundStabilityAnalysis",
        ) -> "_4007.StraightBevelGearSetCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _4007,
            )

            return self._parent._cast(
                _4007.StraightBevelGearSetCompoundStabilityAnalysis
            )

        @property
        def synchroniser_compound_stability_analysis(
            self: "AbstractAssemblyCompoundStabilityAnalysis._Cast_AbstractAssemblyCompoundStabilityAnalysis",
        ) -> "_4010.SynchroniserCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _4010,
            )

            return self._parent._cast(_4010.SynchroniserCompoundStabilityAnalysis)

        @property
        def torque_converter_compound_stability_analysis(
            self: "AbstractAssemblyCompoundStabilityAnalysis._Cast_AbstractAssemblyCompoundStabilityAnalysis",
        ) -> "_4014.TorqueConverterCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _4014,
            )

            return self._parent._cast(_4014.TorqueConverterCompoundStabilityAnalysis)

        @property
        def worm_gear_set_compound_stability_analysis(
            self: "AbstractAssemblyCompoundStabilityAnalysis._Cast_AbstractAssemblyCompoundStabilityAnalysis",
        ) -> "_4022.WormGearSetCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _4022,
            )

            return self._parent._cast(_4022.WormGearSetCompoundStabilityAnalysis)

        @property
        def zerol_bevel_gear_set_compound_stability_analysis(
            self: "AbstractAssemblyCompoundStabilityAnalysis._Cast_AbstractAssemblyCompoundStabilityAnalysis",
        ) -> "_4025.ZerolBevelGearSetCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _4025,
            )

            return self._parent._cast(_4025.ZerolBevelGearSetCompoundStabilityAnalysis)

        @property
        def abstract_assembly_compound_stability_analysis(
            self: "AbstractAssemblyCompoundStabilityAnalysis._Cast_AbstractAssemblyCompoundStabilityAnalysis",
        ) -> "AbstractAssemblyCompoundStabilityAnalysis":
            return self._parent

        def __getattr__(
            self: "AbstractAssemblyCompoundStabilityAnalysis._Cast_AbstractAssemblyCompoundStabilityAnalysis",
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
        self: Self, instance_to_wrap: "AbstractAssemblyCompoundStabilityAnalysis.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_analysis_cases(
        self: Self,
    ) -> "List[_3763.AbstractAssemblyStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.AbstractAssemblyStabilityAnalysis]

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
    ) -> "List[_3763.AbstractAssemblyStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.AbstractAssemblyStabilityAnalysis]

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
    ) -> "AbstractAssemblyCompoundStabilityAnalysis._Cast_AbstractAssemblyCompoundStabilityAnalysis":
        return self._Cast_AbstractAssemblyCompoundStabilityAnalysis(self)
