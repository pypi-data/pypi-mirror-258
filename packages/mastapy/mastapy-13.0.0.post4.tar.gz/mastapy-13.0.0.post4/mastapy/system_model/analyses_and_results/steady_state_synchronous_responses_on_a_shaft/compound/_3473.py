"""SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
    _3375,
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_SPECIALISED_ASSEMBLY_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft.Compound",
    "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
)

if TYPE_CHECKING:
    from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
        _3343,
    )
    from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
        _3381,
        _3385,
        _3388,
        _3393,
        _3395,
        _3396,
        _3401,
        _3406,
        _3409,
        _3412,
        _3416,
        _3418,
        _3424,
        _3430,
        _3432,
        _3435,
        _3439,
        _3443,
        _3446,
        _3449,
        _3455,
        _3459,
        _3466,
        _3476,
        _3477,
        _3482,
        _3485,
        _3488,
        _3492,
        _3500,
        _3503,
        _3454,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import _7545, _7542
    from mastapy.system_model.analyses_and_results import _2651


__docformat__ = "restructuredtext en"
__all__ = ("SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",)


Self = TypeVar(
    "Self", bound="SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft"
)


class SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft(
    _3375.AbstractAssemblyCompoundSteadyStateSynchronousResponseOnAShaft
):
    """SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    """

    TYPE = _SPECIALISED_ASSEMBLY_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT
    _CastSelf = TypeVar(
        "_CastSelf",
        bound="_Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
    )

    class _Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft:
        """Special nested class for casting SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft to subclasses."""

        def __init__(
            self: "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft._Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
            parent: "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
        ):
            self._parent = parent

        @property
        def abstract_assembly_compound_steady_state_synchronous_response_on_a_shaft(
            self: "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft._Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3375.AbstractAssemblyCompoundSteadyStateSynchronousResponseOnAShaft":
            return self._parent._cast(
                _3375.AbstractAssemblyCompoundSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def part_compound_steady_state_synchronous_response_on_a_shaft(
            self: "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft._Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3454.PartCompoundSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
                _3454,
            )

            return self._parent._cast(
                _3454.PartCompoundSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def part_compound_analysis(
            self: "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft._Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
        ) -> "_7545.PartCompoundAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7545

            return self._parent._cast(_7545.PartCompoundAnalysis)

        @property
        def design_entity_compound_analysis(
            self: "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft._Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
        ) -> "_7542.DesignEntityCompoundAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7542

            return self._parent._cast(_7542.DesignEntityCompoundAnalysis)

        @property
        def design_entity_analysis(
            self: "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft._Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def agma_gleason_conical_gear_set_compound_steady_state_synchronous_response_on_a_shaft(
            self: "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft._Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3381.AGMAGleasonConicalGearSetCompoundSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
                _3381,
            )

            return self._parent._cast(
                _3381.AGMAGleasonConicalGearSetCompoundSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def belt_drive_compound_steady_state_synchronous_response_on_a_shaft(
            self: "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft._Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3385.BeltDriveCompoundSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
                _3385,
            )

            return self._parent._cast(
                _3385.BeltDriveCompoundSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def bevel_differential_gear_set_compound_steady_state_synchronous_response_on_a_shaft(
            self: "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft._Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3388.BevelDifferentialGearSetCompoundSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
                _3388,
            )

            return self._parent._cast(
                _3388.BevelDifferentialGearSetCompoundSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def bevel_gear_set_compound_steady_state_synchronous_response_on_a_shaft(
            self: "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft._Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3393.BevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
                _3393,
            )

            return self._parent._cast(
                _3393.BevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def bolted_joint_compound_steady_state_synchronous_response_on_a_shaft(
            self: "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft._Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3395.BoltedJointCompoundSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
                _3395,
            )

            return self._parent._cast(
                _3395.BoltedJointCompoundSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def clutch_compound_steady_state_synchronous_response_on_a_shaft(
            self: "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft._Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3396.ClutchCompoundSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
                _3396,
            )

            return self._parent._cast(
                _3396.ClutchCompoundSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def concept_coupling_compound_steady_state_synchronous_response_on_a_shaft(
            self: "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft._Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3401.ConceptCouplingCompoundSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
                _3401,
            )

            return self._parent._cast(
                _3401.ConceptCouplingCompoundSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def concept_gear_set_compound_steady_state_synchronous_response_on_a_shaft(
            self: "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft._Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3406.ConceptGearSetCompoundSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
                _3406,
            )

            return self._parent._cast(
                _3406.ConceptGearSetCompoundSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def conical_gear_set_compound_steady_state_synchronous_response_on_a_shaft(
            self: "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft._Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3409.ConicalGearSetCompoundSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
                _3409,
            )

            return self._parent._cast(
                _3409.ConicalGearSetCompoundSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def coupling_compound_steady_state_synchronous_response_on_a_shaft(
            self: "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft._Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3412.CouplingCompoundSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
                _3412,
            )

            return self._parent._cast(
                _3412.CouplingCompoundSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def cvt_compound_steady_state_synchronous_response_on_a_shaft(
            self: "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft._Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3416.CVTCompoundSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
                _3416,
            )

            return self._parent._cast(
                _3416.CVTCompoundSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def cycloidal_assembly_compound_steady_state_synchronous_response_on_a_shaft(
            self: "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft._Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3418.CycloidalAssemblyCompoundSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
                _3418,
            )

            return self._parent._cast(
                _3418.CycloidalAssemblyCompoundSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def cylindrical_gear_set_compound_steady_state_synchronous_response_on_a_shaft(
            self: "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft._Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3424.CylindricalGearSetCompoundSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
                _3424,
            )

            return self._parent._cast(
                _3424.CylindricalGearSetCompoundSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def face_gear_set_compound_steady_state_synchronous_response_on_a_shaft(
            self: "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft._Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3430.FaceGearSetCompoundSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
                _3430,
            )

            return self._parent._cast(
                _3430.FaceGearSetCompoundSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def flexible_pin_assembly_compound_steady_state_synchronous_response_on_a_shaft(
            self: "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft._Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3432.FlexiblePinAssemblyCompoundSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
                _3432,
            )

            return self._parent._cast(
                _3432.FlexiblePinAssemblyCompoundSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def gear_set_compound_steady_state_synchronous_response_on_a_shaft(
            self: "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft._Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3435.GearSetCompoundSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
                _3435,
            )

            return self._parent._cast(
                _3435.GearSetCompoundSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def hypoid_gear_set_compound_steady_state_synchronous_response_on_a_shaft(
            self: "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft._Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3439.HypoidGearSetCompoundSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
                _3439,
            )

            return self._parent._cast(
                _3439.HypoidGearSetCompoundSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def klingelnberg_cyclo_palloid_conical_gear_set_compound_steady_state_synchronous_response_on_a_shaft(
            self: "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft._Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3443.KlingelnbergCycloPalloidConicalGearSetCompoundSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
                _3443,
            )

            return self._parent._cast(
                _3443.KlingelnbergCycloPalloidConicalGearSetCompoundSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_steady_state_synchronous_response_on_a_shaft(
            self: "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft._Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3446.KlingelnbergCycloPalloidHypoidGearSetCompoundSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
                _3446,
            )

            return self._parent._cast(
                _3446.KlingelnbergCycloPalloidHypoidGearSetCompoundSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_steady_state_synchronous_response_on_a_shaft(
            self: "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft._Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3449.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
                _3449,
            )

            return self._parent._cast(
                _3449.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def part_to_part_shear_coupling_compound_steady_state_synchronous_response_on_a_shaft(
            self: "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft._Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3455.PartToPartShearCouplingCompoundSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
                _3455,
            )

            return self._parent._cast(
                _3455.PartToPartShearCouplingCompoundSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def planetary_gear_set_compound_steady_state_synchronous_response_on_a_shaft(
            self: "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft._Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3459.PlanetaryGearSetCompoundSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
                _3459,
            )

            return self._parent._cast(
                _3459.PlanetaryGearSetCompoundSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def rolling_ring_assembly_compound_steady_state_synchronous_response_on_a_shaft(
            self: "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft._Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3466.RollingRingAssemblyCompoundSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
                _3466,
            )

            return self._parent._cast(
                _3466.RollingRingAssemblyCompoundSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def spiral_bevel_gear_set_compound_steady_state_synchronous_response_on_a_shaft(
            self: "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft._Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3476.SpiralBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
                _3476,
            )

            return self._parent._cast(
                _3476.SpiralBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def spring_damper_compound_steady_state_synchronous_response_on_a_shaft(
            self: "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft._Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3477.SpringDamperCompoundSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
                _3477,
            )

            return self._parent._cast(
                _3477.SpringDamperCompoundSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def straight_bevel_diff_gear_set_compound_steady_state_synchronous_response_on_a_shaft(
            self: "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft._Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3482.StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
                _3482,
            )

            return self._parent._cast(
                _3482.StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def straight_bevel_gear_set_compound_steady_state_synchronous_response_on_a_shaft(
            self: "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft._Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3485.StraightBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
                _3485,
            )

            return self._parent._cast(
                _3485.StraightBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def synchroniser_compound_steady_state_synchronous_response_on_a_shaft(
            self: "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft._Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3488.SynchroniserCompoundSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
                _3488,
            )

            return self._parent._cast(
                _3488.SynchroniserCompoundSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def torque_converter_compound_steady_state_synchronous_response_on_a_shaft(
            self: "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft._Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3492.TorqueConverterCompoundSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
                _3492,
            )

            return self._parent._cast(
                _3492.TorqueConverterCompoundSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def worm_gear_set_compound_steady_state_synchronous_response_on_a_shaft(
            self: "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft._Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3500.WormGearSetCompoundSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
                _3500,
            )

            return self._parent._cast(
                _3500.WormGearSetCompoundSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def zerol_bevel_gear_set_compound_steady_state_synchronous_response_on_a_shaft(
            self: "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft._Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3503.ZerolBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
                _3503,
            )

            return self._parent._cast(
                _3503.ZerolBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def specialised_assembly_compound_steady_state_synchronous_response_on_a_shaft(
            self: "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft._Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
        ) -> "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft":
            return self._parent

        def __getattr__(
            self: "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft._Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
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
        instance_to_wrap: "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft.TYPE",
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_analysis_cases(
        self: Self,
    ) -> "List[_3343.SpecialisedAssemblySteadyStateSynchronousResponseOnAShaft]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.SpecialisedAssemblySteadyStateSynchronousResponseOnAShaft]

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
    ) -> "List[_3343.SpecialisedAssemblySteadyStateSynchronousResponseOnAShaft]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.SpecialisedAssemblySteadyStateSynchronousResponseOnAShaft]

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
    ) -> "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft._Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft":
        return self._Cast_SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft(
            self
        )
