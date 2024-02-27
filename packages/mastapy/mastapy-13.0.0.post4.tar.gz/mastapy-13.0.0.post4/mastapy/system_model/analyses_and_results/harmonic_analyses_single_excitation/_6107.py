"""SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
    _6007,
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_SPECIALISED_ASSEMBLY_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation",
    "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2476
    from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
        _6013,
        _6017,
        _6020,
        _6025,
        _6026,
        _6030,
        _6035,
        _6038,
        _6041,
        _6046,
        _6048,
        _6050,
        _6056,
        _6062,
        _6064,
        _6067,
        _6072,
        _6076,
        _6079,
        _6082,
        _6091,
        _6093,
        _6100,
        _6110,
        _6113,
        _6116,
        _6119,
        _6123,
        _6127,
        _6134,
        _6137,
        _6088,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import _7547, _7544
    from mastapy.system_model.analyses_and_results import _2657, _2653, _2651


__docformat__ = "restructuredtext en"
__all__ = ("SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",)


Self = TypeVar("Self", bound="SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation")


class SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation(
    _6007.AbstractAssemblyHarmonicAnalysisOfSingleExcitation
):
    """SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    """

    TYPE = _SPECIALISED_ASSEMBLY_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation"
    )

    class _Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation:
        """Special nested class for casting SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation to subclasses."""

        def __init__(
            self: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
            parent: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
        ):
            self._parent = parent

        @property
        def abstract_assembly_harmonic_analysis_of_single_excitation(
            self: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
        ) -> "_6007.AbstractAssemblyHarmonicAnalysisOfSingleExcitation":
            return self._parent._cast(
                _6007.AbstractAssemblyHarmonicAnalysisOfSingleExcitation
            )

        @property
        def part_harmonic_analysis_of_single_excitation(
            self: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
        ) -> "_6088.PartHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6088,
            )

            return self._parent._cast(_6088.PartHarmonicAnalysisOfSingleExcitation)

        @property
        def part_static_load_analysis_case(
            self: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
        ) -> "_7547.PartStaticLoadAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
        ) -> "_7544.PartAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7544

            return self._parent._cast(_7544.PartAnalysisCase)

        @property
        def part_analysis(
            self: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
        ) -> "_2657.PartAnalysis":
            from mastapy.system_model.analyses_and_results import _2657

            return self._parent._cast(_2657.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
        ) -> "_2653.DesignEntitySingleContextAnalysis":
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def agma_gleason_conical_gear_set_harmonic_analysis_of_single_excitation(
            self: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
        ) -> "_6013.AGMAGleasonConicalGearSetHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6013,
            )

            return self._parent._cast(
                _6013.AGMAGleasonConicalGearSetHarmonicAnalysisOfSingleExcitation
            )

        @property
        def belt_drive_harmonic_analysis_of_single_excitation(
            self: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
        ) -> "_6017.BeltDriveHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6017,
            )

            return self._parent._cast(_6017.BeltDriveHarmonicAnalysisOfSingleExcitation)

        @property
        def bevel_differential_gear_set_harmonic_analysis_of_single_excitation(
            self: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
        ) -> "_6020.BevelDifferentialGearSetHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6020,
            )

            return self._parent._cast(
                _6020.BevelDifferentialGearSetHarmonicAnalysisOfSingleExcitation
            )

        @property
        def bevel_gear_set_harmonic_analysis_of_single_excitation(
            self: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
        ) -> "_6025.BevelGearSetHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6025,
            )

            return self._parent._cast(
                _6025.BevelGearSetHarmonicAnalysisOfSingleExcitation
            )

        @property
        def bolted_joint_harmonic_analysis_of_single_excitation(
            self: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
        ) -> "_6026.BoltedJointHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6026,
            )

            return self._parent._cast(
                _6026.BoltedJointHarmonicAnalysisOfSingleExcitation
            )

        @property
        def clutch_harmonic_analysis_of_single_excitation(
            self: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
        ) -> "_6030.ClutchHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6030,
            )

            return self._parent._cast(_6030.ClutchHarmonicAnalysisOfSingleExcitation)

        @property
        def concept_coupling_harmonic_analysis_of_single_excitation(
            self: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
        ) -> "_6035.ConceptCouplingHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6035,
            )

            return self._parent._cast(
                _6035.ConceptCouplingHarmonicAnalysisOfSingleExcitation
            )

        @property
        def concept_gear_set_harmonic_analysis_of_single_excitation(
            self: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
        ) -> "_6038.ConceptGearSetHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6038,
            )

            return self._parent._cast(
                _6038.ConceptGearSetHarmonicAnalysisOfSingleExcitation
            )

        @property
        def conical_gear_set_harmonic_analysis_of_single_excitation(
            self: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
        ) -> "_6041.ConicalGearSetHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6041,
            )

            return self._parent._cast(
                _6041.ConicalGearSetHarmonicAnalysisOfSingleExcitation
            )

        @property
        def coupling_harmonic_analysis_of_single_excitation(
            self: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
        ) -> "_6046.CouplingHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6046,
            )

            return self._parent._cast(_6046.CouplingHarmonicAnalysisOfSingleExcitation)

        @property
        def cvt_harmonic_analysis_of_single_excitation(
            self: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
        ) -> "_6048.CVTHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6048,
            )

            return self._parent._cast(_6048.CVTHarmonicAnalysisOfSingleExcitation)

        @property
        def cycloidal_assembly_harmonic_analysis_of_single_excitation(
            self: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
        ) -> "_6050.CycloidalAssemblyHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6050,
            )

            return self._parent._cast(
                _6050.CycloidalAssemblyHarmonicAnalysisOfSingleExcitation
            )

        @property
        def cylindrical_gear_set_harmonic_analysis_of_single_excitation(
            self: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
        ) -> "_6056.CylindricalGearSetHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6056,
            )

            return self._parent._cast(
                _6056.CylindricalGearSetHarmonicAnalysisOfSingleExcitation
            )

        @property
        def face_gear_set_harmonic_analysis_of_single_excitation(
            self: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
        ) -> "_6062.FaceGearSetHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6062,
            )

            return self._parent._cast(
                _6062.FaceGearSetHarmonicAnalysisOfSingleExcitation
            )

        @property
        def flexible_pin_assembly_harmonic_analysis_of_single_excitation(
            self: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
        ) -> "_6064.FlexiblePinAssemblyHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6064,
            )

            return self._parent._cast(
                _6064.FlexiblePinAssemblyHarmonicAnalysisOfSingleExcitation
            )

        @property
        def gear_set_harmonic_analysis_of_single_excitation(
            self: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
        ) -> "_6067.GearSetHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6067,
            )

            return self._parent._cast(_6067.GearSetHarmonicAnalysisOfSingleExcitation)

        @property
        def hypoid_gear_set_harmonic_analysis_of_single_excitation(
            self: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
        ) -> "_6072.HypoidGearSetHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6072,
            )

            return self._parent._cast(
                _6072.HypoidGearSetHarmonicAnalysisOfSingleExcitation
            )

        @property
        def klingelnberg_cyclo_palloid_conical_gear_set_harmonic_analysis_of_single_excitation(
            self: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
        ) -> "_6076.KlingelnbergCycloPalloidConicalGearSetHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6076,
            )

            return self._parent._cast(
                _6076.KlingelnbergCycloPalloidConicalGearSetHarmonicAnalysisOfSingleExcitation
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_set_harmonic_analysis_of_single_excitation(
            self: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
        ) -> "_6079.KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6079,
            )

            return self._parent._cast(
                _6079.KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysisOfSingleExcitation
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_harmonic_analysis_of_single_excitation(
            self: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
        ) -> "_6082.KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6082,
            )

            return self._parent._cast(
                _6082.KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysisOfSingleExcitation
            )

        @property
        def part_to_part_shear_coupling_harmonic_analysis_of_single_excitation(
            self: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
        ) -> "_6091.PartToPartShearCouplingHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6091,
            )

            return self._parent._cast(
                _6091.PartToPartShearCouplingHarmonicAnalysisOfSingleExcitation
            )

        @property
        def planetary_gear_set_harmonic_analysis_of_single_excitation(
            self: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
        ) -> "_6093.PlanetaryGearSetHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6093,
            )

            return self._parent._cast(
                _6093.PlanetaryGearSetHarmonicAnalysisOfSingleExcitation
            )

        @property
        def rolling_ring_assembly_harmonic_analysis_of_single_excitation(
            self: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
        ) -> "_6100.RollingRingAssemblyHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6100,
            )

            return self._parent._cast(
                _6100.RollingRingAssemblyHarmonicAnalysisOfSingleExcitation
            )

        @property
        def spiral_bevel_gear_set_harmonic_analysis_of_single_excitation(
            self: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
        ) -> "_6110.SpiralBevelGearSetHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6110,
            )

            return self._parent._cast(
                _6110.SpiralBevelGearSetHarmonicAnalysisOfSingleExcitation
            )

        @property
        def spring_damper_harmonic_analysis_of_single_excitation(
            self: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
        ) -> "_6113.SpringDamperHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6113,
            )

            return self._parent._cast(
                _6113.SpringDamperHarmonicAnalysisOfSingleExcitation
            )

        @property
        def straight_bevel_diff_gear_set_harmonic_analysis_of_single_excitation(
            self: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
        ) -> "_6116.StraightBevelDiffGearSetHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6116,
            )

            return self._parent._cast(
                _6116.StraightBevelDiffGearSetHarmonicAnalysisOfSingleExcitation
            )

        @property
        def straight_bevel_gear_set_harmonic_analysis_of_single_excitation(
            self: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
        ) -> "_6119.StraightBevelGearSetHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6119,
            )

            return self._parent._cast(
                _6119.StraightBevelGearSetHarmonicAnalysisOfSingleExcitation
            )

        @property
        def synchroniser_harmonic_analysis_of_single_excitation(
            self: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
        ) -> "_6123.SynchroniserHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6123,
            )

            return self._parent._cast(
                _6123.SynchroniserHarmonicAnalysisOfSingleExcitation
            )

        @property
        def torque_converter_harmonic_analysis_of_single_excitation(
            self: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
        ) -> "_6127.TorqueConverterHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6127,
            )

            return self._parent._cast(
                _6127.TorqueConverterHarmonicAnalysisOfSingleExcitation
            )

        @property
        def worm_gear_set_harmonic_analysis_of_single_excitation(
            self: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
        ) -> "_6134.WormGearSetHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6134,
            )

            return self._parent._cast(
                _6134.WormGearSetHarmonicAnalysisOfSingleExcitation
            )

        @property
        def zerol_bevel_gear_set_harmonic_analysis_of_single_excitation(
            self: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
        ) -> "_6137.ZerolBevelGearSetHarmonicAnalysisOfSingleExcitation":
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6137,
            )

            return self._parent._cast(
                _6137.ZerolBevelGearSetHarmonicAnalysisOfSingleExcitation
            )

        @property
        def specialised_assembly_harmonic_analysis_of_single_excitation(
            self: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
        ) -> "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation":
            return self._parent

        def __getattr__(
            self: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation",
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
        instance_to_wrap: "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation.TYPE",
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self: Self) -> "_2476.SpecialisedAssembly":
        """mastapy.system_model.part_model.SpecialisedAssembly

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation":
        return self._Cast_SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation(self)
