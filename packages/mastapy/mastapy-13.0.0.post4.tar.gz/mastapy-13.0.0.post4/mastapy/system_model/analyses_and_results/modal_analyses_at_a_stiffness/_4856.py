"""AbstractAssemblyModalAnalysisAtAStiffness"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
    _4937,
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_ABSTRACT_ASSEMBLY_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness",
    "AbstractAssemblyModalAnalysisAtAStiffness",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2434
    from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
        _4862,
        _4863,
        _4866,
        _4869,
        _4874,
        _4875,
        _4879,
        _4884,
        _4887,
        _4890,
        _4895,
        _4897,
        _4899,
        _4905,
        _4912,
        _4914,
        _4917,
        _4921,
        _4925,
        _4928,
        _4931,
        _4940,
        _4942,
        _4949,
        _4952,
        _4956,
        _4959,
        _4962,
        _4965,
        _4968,
        _4972,
        _4976,
        _4983,
        _4986,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import _7547, _7544
    from mastapy.system_model.analyses_and_results import _2657, _2653, _2651


__docformat__ = "restructuredtext en"
__all__ = ("AbstractAssemblyModalAnalysisAtAStiffness",)


Self = TypeVar("Self", bound="AbstractAssemblyModalAnalysisAtAStiffness")


class AbstractAssemblyModalAnalysisAtAStiffness(_4937.PartModalAnalysisAtAStiffness):
    """AbstractAssemblyModalAnalysisAtAStiffness

    This is a mastapy class.
    """

    TYPE = _ABSTRACT_ASSEMBLY_MODAL_ANALYSIS_AT_A_STIFFNESS
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_AbstractAssemblyModalAnalysisAtAStiffness"
    )

    class _Cast_AbstractAssemblyModalAnalysisAtAStiffness:
        """Special nested class for casting AbstractAssemblyModalAnalysisAtAStiffness to subclasses."""

        def __init__(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
            parent: "AbstractAssemblyModalAnalysisAtAStiffness",
        ):
            self._parent = parent

        @property
        def part_modal_analysis_at_a_stiffness(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
        ) -> "_4937.PartModalAnalysisAtAStiffness":
            return self._parent._cast(_4937.PartModalAnalysisAtAStiffness)

        @property
        def part_static_load_analysis_case(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
        ) -> "_7547.PartStaticLoadAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
        ) -> "_7544.PartAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7544

            return self._parent._cast(_7544.PartAnalysisCase)

        @property
        def part_analysis(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
        ) -> "_2657.PartAnalysis":
            from mastapy.system_model.analyses_and_results import _2657

            return self._parent._cast(_2657.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
        ) -> "_2653.DesignEntitySingleContextAnalysis":
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def agma_gleason_conical_gear_set_modal_analysis_at_a_stiffness(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
        ) -> "_4862.AGMAGleasonConicalGearSetModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4862,
            )

            return self._parent._cast(
                _4862.AGMAGleasonConicalGearSetModalAnalysisAtAStiffness
            )

        @property
        def assembly_modal_analysis_at_a_stiffness(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
        ) -> "_4863.AssemblyModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4863,
            )

            return self._parent._cast(_4863.AssemblyModalAnalysisAtAStiffness)

        @property
        def belt_drive_modal_analysis_at_a_stiffness(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
        ) -> "_4866.BeltDriveModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4866,
            )

            return self._parent._cast(_4866.BeltDriveModalAnalysisAtAStiffness)

        @property
        def bevel_differential_gear_set_modal_analysis_at_a_stiffness(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
        ) -> "_4869.BevelDifferentialGearSetModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4869,
            )

            return self._parent._cast(
                _4869.BevelDifferentialGearSetModalAnalysisAtAStiffness
            )

        @property
        def bevel_gear_set_modal_analysis_at_a_stiffness(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
        ) -> "_4874.BevelGearSetModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4874,
            )

            return self._parent._cast(_4874.BevelGearSetModalAnalysisAtAStiffness)

        @property
        def bolted_joint_modal_analysis_at_a_stiffness(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
        ) -> "_4875.BoltedJointModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4875,
            )

            return self._parent._cast(_4875.BoltedJointModalAnalysisAtAStiffness)

        @property
        def clutch_modal_analysis_at_a_stiffness(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
        ) -> "_4879.ClutchModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4879,
            )

            return self._parent._cast(_4879.ClutchModalAnalysisAtAStiffness)

        @property
        def concept_coupling_modal_analysis_at_a_stiffness(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
        ) -> "_4884.ConceptCouplingModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4884,
            )

            return self._parent._cast(_4884.ConceptCouplingModalAnalysisAtAStiffness)

        @property
        def concept_gear_set_modal_analysis_at_a_stiffness(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
        ) -> "_4887.ConceptGearSetModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4887,
            )

            return self._parent._cast(_4887.ConceptGearSetModalAnalysisAtAStiffness)

        @property
        def conical_gear_set_modal_analysis_at_a_stiffness(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
        ) -> "_4890.ConicalGearSetModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4890,
            )

            return self._parent._cast(_4890.ConicalGearSetModalAnalysisAtAStiffness)

        @property
        def coupling_modal_analysis_at_a_stiffness(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
        ) -> "_4895.CouplingModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4895,
            )

            return self._parent._cast(_4895.CouplingModalAnalysisAtAStiffness)

        @property
        def cvt_modal_analysis_at_a_stiffness(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
        ) -> "_4897.CVTModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4897,
            )

            return self._parent._cast(_4897.CVTModalAnalysisAtAStiffness)

        @property
        def cycloidal_assembly_modal_analysis_at_a_stiffness(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
        ) -> "_4899.CycloidalAssemblyModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4899,
            )

            return self._parent._cast(_4899.CycloidalAssemblyModalAnalysisAtAStiffness)

        @property
        def cylindrical_gear_set_modal_analysis_at_a_stiffness(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
        ) -> "_4905.CylindricalGearSetModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4905,
            )

            return self._parent._cast(_4905.CylindricalGearSetModalAnalysisAtAStiffness)

        @property
        def face_gear_set_modal_analysis_at_a_stiffness(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
        ) -> "_4912.FaceGearSetModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4912,
            )

            return self._parent._cast(_4912.FaceGearSetModalAnalysisAtAStiffness)

        @property
        def flexible_pin_assembly_modal_analysis_at_a_stiffness(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
        ) -> "_4914.FlexiblePinAssemblyModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4914,
            )

            return self._parent._cast(
                _4914.FlexiblePinAssemblyModalAnalysisAtAStiffness
            )

        @property
        def gear_set_modal_analysis_at_a_stiffness(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
        ) -> "_4917.GearSetModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4917,
            )

            return self._parent._cast(_4917.GearSetModalAnalysisAtAStiffness)

        @property
        def hypoid_gear_set_modal_analysis_at_a_stiffness(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
        ) -> "_4921.HypoidGearSetModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4921,
            )

            return self._parent._cast(_4921.HypoidGearSetModalAnalysisAtAStiffness)

        @property
        def klingelnberg_cyclo_palloid_conical_gear_set_modal_analysis_at_a_stiffness(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
        ) -> "_4925.KlingelnbergCycloPalloidConicalGearSetModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4925,
            )

            return self._parent._cast(
                _4925.KlingelnbergCycloPalloidConicalGearSetModalAnalysisAtAStiffness
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_set_modal_analysis_at_a_stiffness(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
        ) -> "_4928.KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4928,
            )

            return self._parent._cast(
                _4928.KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtAStiffness
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_modal_analysis_at_a_stiffness(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
        ) -> (
            "_4931.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtAStiffness"
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4931,
            )

            return self._parent._cast(
                _4931.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtAStiffness
            )

        @property
        def part_to_part_shear_coupling_modal_analysis_at_a_stiffness(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
        ) -> "_4940.PartToPartShearCouplingModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4940,
            )

            return self._parent._cast(
                _4940.PartToPartShearCouplingModalAnalysisAtAStiffness
            )

        @property
        def planetary_gear_set_modal_analysis_at_a_stiffness(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
        ) -> "_4942.PlanetaryGearSetModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4942,
            )

            return self._parent._cast(_4942.PlanetaryGearSetModalAnalysisAtAStiffness)

        @property
        def rolling_ring_assembly_modal_analysis_at_a_stiffness(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
        ) -> "_4949.RollingRingAssemblyModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4949,
            )

            return self._parent._cast(
                _4949.RollingRingAssemblyModalAnalysisAtAStiffness
            )

        @property
        def root_assembly_modal_analysis_at_a_stiffness(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
        ) -> "_4952.RootAssemblyModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4952,
            )

            return self._parent._cast(_4952.RootAssemblyModalAnalysisAtAStiffness)

        @property
        def specialised_assembly_modal_analysis_at_a_stiffness(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
        ) -> "_4956.SpecialisedAssemblyModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4956,
            )

            return self._parent._cast(
                _4956.SpecialisedAssemblyModalAnalysisAtAStiffness
            )

        @property
        def spiral_bevel_gear_set_modal_analysis_at_a_stiffness(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
        ) -> "_4959.SpiralBevelGearSetModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4959,
            )

            return self._parent._cast(_4959.SpiralBevelGearSetModalAnalysisAtAStiffness)

        @property
        def spring_damper_modal_analysis_at_a_stiffness(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
        ) -> "_4962.SpringDamperModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4962,
            )

            return self._parent._cast(_4962.SpringDamperModalAnalysisAtAStiffness)

        @property
        def straight_bevel_diff_gear_set_modal_analysis_at_a_stiffness(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
        ) -> "_4965.StraightBevelDiffGearSetModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4965,
            )

            return self._parent._cast(
                _4965.StraightBevelDiffGearSetModalAnalysisAtAStiffness
            )

        @property
        def straight_bevel_gear_set_modal_analysis_at_a_stiffness(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
        ) -> "_4968.StraightBevelGearSetModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4968,
            )

            return self._parent._cast(
                _4968.StraightBevelGearSetModalAnalysisAtAStiffness
            )

        @property
        def synchroniser_modal_analysis_at_a_stiffness(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
        ) -> "_4972.SynchroniserModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4972,
            )

            return self._parent._cast(_4972.SynchroniserModalAnalysisAtAStiffness)

        @property
        def torque_converter_modal_analysis_at_a_stiffness(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
        ) -> "_4976.TorqueConverterModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4976,
            )

            return self._parent._cast(_4976.TorqueConverterModalAnalysisAtAStiffness)

        @property
        def worm_gear_set_modal_analysis_at_a_stiffness(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
        ) -> "_4983.WormGearSetModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4983,
            )

            return self._parent._cast(_4983.WormGearSetModalAnalysisAtAStiffness)

        @property
        def zerol_bevel_gear_set_modal_analysis_at_a_stiffness(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
        ) -> "_4986.ZerolBevelGearSetModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4986,
            )

            return self._parent._cast(_4986.ZerolBevelGearSetModalAnalysisAtAStiffness)

        @property
        def abstract_assembly_modal_analysis_at_a_stiffness(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
        ) -> "AbstractAssemblyModalAnalysisAtAStiffness":
            return self._parent

        def __getattr__(
            self: "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness",
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
        self: Self, instance_to_wrap: "AbstractAssemblyModalAnalysisAtAStiffness.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2434.AbstractAssembly":
        """mastapy.system_model.part_model.AbstractAssembly

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_design(self: Self) -> "_2434.AbstractAssembly":
        """mastapy.system_model.part_model.AbstractAssembly

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
    ) -> "AbstractAssemblyModalAnalysisAtAStiffness._Cast_AbstractAssemblyModalAnalysisAtAStiffness":
        return self._Cast_AbstractAssemblyModalAnalysisAtAStiffness(self)
