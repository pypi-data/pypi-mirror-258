"""SpecialisedAssemblyCompoundHarmonicAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5879
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_SPECIALISED_ASSEMBLY_COMPOUND_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound",
    "SpecialisedAssemblyCompoundHarmonicAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.analyses_and_results.harmonic_analyses import _5810
    from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
        _5885,
        _5889,
        _5892,
        _5897,
        _5899,
        _5900,
        _5905,
        _5910,
        _5913,
        _5916,
        _5920,
        _5922,
        _5928,
        _5934,
        _5936,
        _5939,
        _5943,
        _5947,
        _5950,
        _5953,
        _5959,
        _5963,
        _5970,
        _5980,
        _5981,
        _5986,
        _5989,
        _5992,
        _5996,
        _6004,
        _6007,
        _5958,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import _7546, _7543
    from mastapy.system_model.analyses_and_results import _2651


__docformat__ = "restructuredtext en"
__all__ = ("SpecialisedAssemblyCompoundHarmonicAnalysis",)


Self = TypeVar("Self", bound="SpecialisedAssemblyCompoundHarmonicAnalysis")


class SpecialisedAssemblyCompoundHarmonicAnalysis(
    _5879.AbstractAssemblyCompoundHarmonicAnalysis
):
    """SpecialisedAssemblyCompoundHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE = _SPECIALISED_ASSEMBLY_COMPOUND_HARMONIC_ANALYSIS
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_SpecialisedAssemblyCompoundHarmonicAnalysis"
    )

    class _Cast_SpecialisedAssemblyCompoundHarmonicAnalysis:
        """Special nested class for casting SpecialisedAssemblyCompoundHarmonicAnalysis to subclasses."""

        def __init__(
            self: "SpecialisedAssemblyCompoundHarmonicAnalysis._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis",
            parent: "SpecialisedAssemblyCompoundHarmonicAnalysis",
        ):
            self._parent = parent

        @property
        def abstract_assembly_compound_harmonic_analysis(
            self: "SpecialisedAssemblyCompoundHarmonicAnalysis._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis",
        ) -> "_5879.AbstractAssemblyCompoundHarmonicAnalysis":
            return self._parent._cast(_5879.AbstractAssemblyCompoundHarmonicAnalysis)

        @property
        def part_compound_harmonic_analysis(
            self: "SpecialisedAssemblyCompoundHarmonicAnalysis._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis",
        ) -> "_5958.PartCompoundHarmonicAnalysis":
            from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
                _5958,
            )

            return self._parent._cast(_5958.PartCompoundHarmonicAnalysis)

        @property
        def part_compound_analysis(
            self: "SpecialisedAssemblyCompoundHarmonicAnalysis._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis",
        ) -> "_7546.PartCompoundAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7546

            return self._parent._cast(_7546.PartCompoundAnalysis)

        @property
        def design_entity_compound_analysis(
            self: "SpecialisedAssemblyCompoundHarmonicAnalysis._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis",
        ) -> "_7543.DesignEntityCompoundAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7543

            return self._parent._cast(_7543.DesignEntityCompoundAnalysis)

        @property
        def design_entity_analysis(
            self: "SpecialisedAssemblyCompoundHarmonicAnalysis._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def agma_gleason_conical_gear_set_compound_harmonic_analysis(
            self: "SpecialisedAssemblyCompoundHarmonicAnalysis._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis",
        ) -> "_5885.AGMAGleasonConicalGearSetCompoundHarmonicAnalysis":
            from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
                _5885,
            )

            return self._parent._cast(
                _5885.AGMAGleasonConicalGearSetCompoundHarmonicAnalysis
            )

        @property
        def belt_drive_compound_harmonic_analysis(
            self: "SpecialisedAssemblyCompoundHarmonicAnalysis._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis",
        ) -> "_5889.BeltDriveCompoundHarmonicAnalysis":
            from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
                _5889,
            )

            return self._parent._cast(_5889.BeltDriveCompoundHarmonicAnalysis)

        @property
        def bevel_differential_gear_set_compound_harmonic_analysis(
            self: "SpecialisedAssemblyCompoundHarmonicAnalysis._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis",
        ) -> "_5892.BevelDifferentialGearSetCompoundHarmonicAnalysis":
            from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
                _5892,
            )

            return self._parent._cast(
                _5892.BevelDifferentialGearSetCompoundHarmonicAnalysis
            )

        @property
        def bevel_gear_set_compound_harmonic_analysis(
            self: "SpecialisedAssemblyCompoundHarmonicAnalysis._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis",
        ) -> "_5897.BevelGearSetCompoundHarmonicAnalysis":
            from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
                _5897,
            )

            return self._parent._cast(_5897.BevelGearSetCompoundHarmonicAnalysis)

        @property
        def bolted_joint_compound_harmonic_analysis(
            self: "SpecialisedAssemblyCompoundHarmonicAnalysis._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis",
        ) -> "_5899.BoltedJointCompoundHarmonicAnalysis":
            from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
                _5899,
            )

            return self._parent._cast(_5899.BoltedJointCompoundHarmonicAnalysis)

        @property
        def clutch_compound_harmonic_analysis(
            self: "SpecialisedAssemblyCompoundHarmonicAnalysis._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis",
        ) -> "_5900.ClutchCompoundHarmonicAnalysis":
            from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
                _5900,
            )

            return self._parent._cast(_5900.ClutchCompoundHarmonicAnalysis)

        @property
        def concept_coupling_compound_harmonic_analysis(
            self: "SpecialisedAssemblyCompoundHarmonicAnalysis._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis",
        ) -> "_5905.ConceptCouplingCompoundHarmonicAnalysis":
            from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
                _5905,
            )

            return self._parent._cast(_5905.ConceptCouplingCompoundHarmonicAnalysis)

        @property
        def concept_gear_set_compound_harmonic_analysis(
            self: "SpecialisedAssemblyCompoundHarmonicAnalysis._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis",
        ) -> "_5910.ConceptGearSetCompoundHarmonicAnalysis":
            from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
                _5910,
            )

            return self._parent._cast(_5910.ConceptGearSetCompoundHarmonicAnalysis)

        @property
        def conical_gear_set_compound_harmonic_analysis(
            self: "SpecialisedAssemblyCompoundHarmonicAnalysis._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis",
        ) -> "_5913.ConicalGearSetCompoundHarmonicAnalysis":
            from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
                _5913,
            )

            return self._parent._cast(_5913.ConicalGearSetCompoundHarmonicAnalysis)

        @property
        def coupling_compound_harmonic_analysis(
            self: "SpecialisedAssemblyCompoundHarmonicAnalysis._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis",
        ) -> "_5916.CouplingCompoundHarmonicAnalysis":
            from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
                _5916,
            )

            return self._parent._cast(_5916.CouplingCompoundHarmonicAnalysis)

        @property
        def cvt_compound_harmonic_analysis(
            self: "SpecialisedAssemblyCompoundHarmonicAnalysis._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis",
        ) -> "_5920.CVTCompoundHarmonicAnalysis":
            from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
                _5920,
            )

            return self._parent._cast(_5920.CVTCompoundHarmonicAnalysis)

        @property
        def cycloidal_assembly_compound_harmonic_analysis(
            self: "SpecialisedAssemblyCompoundHarmonicAnalysis._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis",
        ) -> "_5922.CycloidalAssemblyCompoundHarmonicAnalysis":
            from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
                _5922,
            )

            return self._parent._cast(_5922.CycloidalAssemblyCompoundHarmonicAnalysis)

        @property
        def cylindrical_gear_set_compound_harmonic_analysis(
            self: "SpecialisedAssemblyCompoundHarmonicAnalysis._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis",
        ) -> "_5928.CylindricalGearSetCompoundHarmonicAnalysis":
            from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
                _5928,
            )

            return self._parent._cast(_5928.CylindricalGearSetCompoundHarmonicAnalysis)

        @property
        def face_gear_set_compound_harmonic_analysis(
            self: "SpecialisedAssemblyCompoundHarmonicAnalysis._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis",
        ) -> "_5934.FaceGearSetCompoundHarmonicAnalysis":
            from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
                _5934,
            )

            return self._parent._cast(_5934.FaceGearSetCompoundHarmonicAnalysis)

        @property
        def flexible_pin_assembly_compound_harmonic_analysis(
            self: "SpecialisedAssemblyCompoundHarmonicAnalysis._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis",
        ) -> "_5936.FlexiblePinAssemblyCompoundHarmonicAnalysis":
            from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
                _5936,
            )

            return self._parent._cast(_5936.FlexiblePinAssemblyCompoundHarmonicAnalysis)

        @property
        def gear_set_compound_harmonic_analysis(
            self: "SpecialisedAssemblyCompoundHarmonicAnalysis._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis",
        ) -> "_5939.GearSetCompoundHarmonicAnalysis":
            from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
                _5939,
            )

            return self._parent._cast(_5939.GearSetCompoundHarmonicAnalysis)

        @property
        def hypoid_gear_set_compound_harmonic_analysis(
            self: "SpecialisedAssemblyCompoundHarmonicAnalysis._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis",
        ) -> "_5943.HypoidGearSetCompoundHarmonicAnalysis":
            from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
                _5943,
            )

            return self._parent._cast(_5943.HypoidGearSetCompoundHarmonicAnalysis)

        @property
        def klingelnberg_cyclo_palloid_conical_gear_set_compound_harmonic_analysis(
            self: "SpecialisedAssemblyCompoundHarmonicAnalysis._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis",
        ) -> "_5947.KlingelnbergCycloPalloidConicalGearSetCompoundHarmonicAnalysis":
            from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
                _5947,
            )

            return self._parent._cast(
                _5947.KlingelnbergCycloPalloidConicalGearSetCompoundHarmonicAnalysis
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_harmonic_analysis(
            self: "SpecialisedAssemblyCompoundHarmonicAnalysis._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis",
        ) -> "_5950.KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysis":
            from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
                _5950,
            )

            return self._parent._cast(
                _5950.KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysis
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_harmonic_analysis(
            self: "SpecialisedAssemblyCompoundHarmonicAnalysis._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis",
        ) -> "_5953.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis":
            from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
                _5953,
            )

            return self._parent._cast(
                _5953.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis
            )

        @property
        def part_to_part_shear_coupling_compound_harmonic_analysis(
            self: "SpecialisedAssemblyCompoundHarmonicAnalysis._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis",
        ) -> "_5959.PartToPartShearCouplingCompoundHarmonicAnalysis":
            from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
                _5959,
            )

            return self._parent._cast(
                _5959.PartToPartShearCouplingCompoundHarmonicAnalysis
            )

        @property
        def planetary_gear_set_compound_harmonic_analysis(
            self: "SpecialisedAssemblyCompoundHarmonicAnalysis._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis",
        ) -> "_5963.PlanetaryGearSetCompoundHarmonicAnalysis":
            from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
                _5963,
            )

            return self._parent._cast(_5963.PlanetaryGearSetCompoundHarmonicAnalysis)

        @property
        def rolling_ring_assembly_compound_harmonic_analysis(
            self: "SpecialisedAssemblyCompoundHarmonicAnalysis._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis",
        ) -> "_5970.RollingRingAssemblyCompoundHarmonicAnalysis":
            from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
                _5970,
            )

            return self._parent._cast(_5970.RollingRingAssemblyCompoundHarmonicAnalysis)

        @property
        def spiral_bevel_gear_set_compound_harmonic_analysis(
            self: "SpecialisedAssemblyCompoundHarmonicAnalysis._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis",
        ) -> "_5980.SpiralBevelGearSetCompoundHarmonicAnalysis":
            from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
                _5980,
            )

            return self._parent._cast(_5980.SpiralBevelGearSetCompoundHarmonicAnalysis)

        @property
        def spring_damper_compound_harmonic_analysis(
            self: "SpecialisedAssemblyCompoundHarmonicAnalysis._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis",
        ) -> "_5981.SpringDamperCompoundHarmonicAnalysis":
            from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
                _5981,
            )

            return self._parent._cast(_5981.SpringDamperCompoundHarmonicAnalysis)

        @property
        def straight_bevel_diff_gear_set_compound_harmonic_analysis(
            self: "SpecialisedAssemblyCompoundHarmonicAnalysis._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis",
        ) -> "_5986.StraightBevelDiffGearSetCompoundHarmonicAnalysis":
            from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
                _5986,
            )

            return self._parent._cast(
                _5986.StraightBevelDiffGearSetCompoundHarmonicAnalysis
            )

        @property
        def straight_bevel_gear_set_compound_harmonic_analysis(
            self: "SpecialisedAssemblyCompoundHarmonicAnalysis._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis",
        ) -> "_5989.StraightBevelGearSetCompoundHarmonicAnalysis":
            from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
                _5989,
            )

            return self._parent._cast(
                _5989.StraightBevelGearSetCompoundHarmonicAnalysis
            )

        @property
        def synchroniser_compound_harmonic_analysis(
            self: "SpecialisedAssemblyCompoundHarmonicAnalysis._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis",
        ) -> "_5992.SynchroniserCompoundHarmonicAnalysis":
            from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
                _5992,
            )

            return self._parent._cast(_5992.SynchroniserCompoundHarmonicAnalysis)

        @property
        def torque_converter_compound_harmonic_analysis(
            self: "SpecialisedAssemblyCompoundHarmonicAnalysis._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis",
        ) -> "_5996.TorqueConverterCompoundHarmonicAnalysis":
            from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
                _5996,
            )

            return self._parent._cast(_5996.TorqueConverterCompoundHarmonicAnalysis)

        @property
        def worm_gear_set_compound_harmonic_analysis(
            self: "SpecialisedAssemblyCompoundHarmonicAnalysis._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis",
        ) -> "_6004.WormGearSetCompoundHarmonicAnalysis":
            from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
                _6004,
            )

            return self._parent._cast(_6004.WormGearSetCompoundHarmonicAnalysis)

        @property
        def zerol_bevel_gear_set_compound_harmonic_analysis(
            self: "SpecialisedAssemblyCompoundHarmonicAnalysis._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis",
        ) -> "_6007.ZerolBevelGearSetCompoundHarmonicAnalysis":
            from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
                _6007,
            )

            return self._parent._cast(_6007.ZerolBevelGearSetCompoundHarmonicAnalysis)

        @property
        def specialised_assembly_compound_harmonic_analysis(
            self: "SpecialisedAssemblyCompoundHarmonicAnalysis._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis",
        ) -> "SpecialisedAssemblyCompoundHarmonicAnalysis":
            return self._parent

        def __getattr__(
            self: "SpecialisedAssemblyCompoundHarmonicAnalysis._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis",
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
        self: Self, instance_to_wrap: "SpecialisedAssemblyCompoundHarmonicAnalysis.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_analysis_cases(
        self: Self,
    ) -> "List[_5810.SpecialisedAssemblyHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.SpecialisedAssemblyHarmonicAnalysis]

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
    ) -> "List[_5810.SpecialisedAssemblyHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.SpecialisedAssemblyHarmonicAnalysis]

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
    ) -> "SpecialisedAssemblyCompoundHarmonicAnalysis._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis":
        return self._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis(self)
