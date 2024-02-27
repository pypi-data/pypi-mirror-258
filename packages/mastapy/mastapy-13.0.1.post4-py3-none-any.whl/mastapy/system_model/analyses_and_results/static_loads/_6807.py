"""AbstractAssemblyLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6929
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_ABSTRACT_ASSEMBLY_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "AbstractAssemblyLoadCase",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2434
    from mastapy.system_model.analyses_and_results.static_loads import (
        _6816,
        _6819,
        _6822,
        _6825,
        _6830,
        _6831,
        _6835,
        _6841,
        _6844,
        _6849,
        _6854,
        _6856,
        _6858,
        _6866,
        _6887,
        _6889,
        _6896,
        _6908,
        _6915,
        _6918,
        _6921,
        _6932,
        _6934,
        _6946,
        _6949,
        _6953,
        _6956,
        _6959,
        _6962,
        _6965,
        _6969,
        _6974,
        _6985,
        _6988,
    )
    from mastapy.system_model.analyses_and_results import _2657, _2653, _2651


__docformat__ = "restructuredtext en"
__all__ = ("AbstractAssemblyLoadCase",)


Self = TypeVar("Self", bound="AbstractAssemblyLoadCase")


class AbstractAssemblyLoadCase(_6929.PartLoadCase):
    """AbstractAssemblyLoadCase

    This is a mastapy class.
    """

    TYPE = _ABSTRACT_ASSEMBLY_LOAD_CASE
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_AbstractAssemblyLoadCase")

    class _Cast_AbstractAssemblyLoadCase:
        """Special nested class for casting AbstractAssemblyLoadCase to subclasses."""

        def __init__(
            self: "AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase",
            parent: "AbstractAssemblyLoadCase",
        ):
            self._parent = parent

        @property
        def part_load_case(
            self: "AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase",
        ) -> "_6929.PartLoadCase":
            return self._parent._cast(_6929.PartLoadCase)

        @property
        def part_analysis(
            self: "AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase",
        ) -> "_2657.PartAnalysis":
            from mastapy.system_model.analyses_and_results import _2657

            return self._parent._cast(_2657.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase",
        ) -> "_2653.DesignEntitySingleContextAnalysis":
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def agma_gleason_conical_gear_set_load_case(
            self: "AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase",
        ) -> "_6816.AGMAGleasonConicalGearSetLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6816

            return self._parent._cast(_6816.AGMAGleasonConicalGearSetLoadCase)

        @property
        def assembly_load_case(
            self: "AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase",
        ) -> "_6819.AssemblyLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6819

            return self._parent._cast(_6819.AssemblyLoadCase)

        @property
        def belt_drive_load_case(
            self: "AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase",
        ) -> "_6822.BeltDriveLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6822

            return self._parent._cast(_6822.BeltDriveLoadCase)

        @property
        def bevel_differential_gear_set_load_case(
            self: "AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase",
        ) -> "_6825.BevelDifferentialGearSetLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6825

            return self._parent._cast(_6825.BevelDifferentialGearSetLoadCase)

        @property
        def bevel_gear_set_load_case(
            self: "AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase",
        ) -> "_6830.BevelGearSetLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6830

            return self._parent._cast(_6830.BevelGearSetLoadCase)

        @property
        def bolted_joint_load_case(
            self: "AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase",
        ) -> "_6831.BoltedJointLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6831

            return self._parent._cast(_6831.BoltedJointLoadCase)

        @property
        def clutch_load_case(
            self: "AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase",
        ) -> "_6835.ClutchLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6835

            return self._parent._cast(_6835.ClutchLoadCase)

        @property
        def concept_coupling_load_case(
            self: "AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase",
        ) -> "_6841.ConceptCouplingLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6841

            return self._parent._cast(_6841.ConceptCouplingLoadCase)

        @property
        def concept_gear_set_load_case(
            self: "AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase",
        ) -> "_6844.ConceptGearSetLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6844

            return self._parent._cast(_6844.ConceptGearSetLoadCase)

        @property
        def conical_gear_set_load_case(
            self: "AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase",
        ) -> "_6849.ConicalGearSetLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6849

            return self._parent._cast(_6849.ConicalGearSetLoadCase)

        @property
        def coupling_load_case(
            self: "AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase",
        ) -> "_6854.CouplingLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6854

            return self._parent._cast(_6854.CouplingLoadCase)

        @property
        def cvt_load_case(
            self: "AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase",
        ) -> "_6856.CVTLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6856

            return self._parent._cast(_6856.CVTLoadCase)

        @property
        def cycloidal_assembly_load_case(
            self: "AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase",
        ) -> "_6858.CycloidalAssemblyLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6858

            return self._parent._cast(_6858.CycloidalAssemblyLoadCase)

        @property
        def cylindrical_gear_set_load_case(
            self: "AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase",
        ) -> "_6866.CylindricalGearSetLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6866

            return self._parent._cast(_6866.CylindricalGearSetLoadCase)

        @property
        def face_gear_set_load_case(
            self: "AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase",
        ) -> "_6887.FaceGearSetLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6887

            return self._parent._cast(_6887.FaceGearSetLoadCase)

        @property
        def flexible_pin_assembly_load_case(
            self: "AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase",
        ) -> "_6889.FlexiblePinAssemblyLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6889

            return self._parent._cast(_6889.FlexiblePinAssemblyLoadCase)

        @property
        def gear_set_load_case(
            self: "AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase",
        ) -> "_6896.GearSetLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6896

            return self._parent._cast(_6896.GearSetLoadCase)

        @property
        def hypoid_gear_set_load_case(
            self: "AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase",
        ) -> "_6908.HypoidGearSetLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6908

            return self._parent._cast(_6908.HypoidGearSetLoadCase)

        @property
        def klingelnberg_cyclo_palloid_conical_gear_set_load_case(
            self: "AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase",
        ) -> "_6915.KlingelnbergCycloPalloidConicalGearSetLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6915

            return self._parent._cast(
                _6915.KlingelnbergCycloPalloidConicalGearSetLoadCase
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_set_load_case(
            self: "AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase",
        ) -> "_6918.KlingelnbergCycloPalloidHypoidGearSetLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6918

            return self._parent._cast(
                _6918.KlingelnbergCycloPalloidHypoidGearSetLoadCase
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_load_case(
            self: "AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase",
        ) -> "_6921.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6921

            return self._parent._cast(
                _6921.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase
            )

        @property
        def part_to_part_shear_coupling_load_case(
            self: "AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase",
        ) -> "_6932.PartToPartShearCouplingLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6932

            return self._parent._cast(_6932.PartToPartShearCouplingLoadCase)

        @property
        def planetary_gear_set_load_case(
            self: "AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase",
        ) -> "_6934.PlanetaryGearSetLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6934

            return self._parent._cast(_6934.PlanetaryGearSetLoadCase)

        @property
        def rolling_ring_assembly_load_case(
            self: "AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase",
        ) -> "_6946.RollingRingAssemblyLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6946

            return self._parent._cast(_6946.RollingRingAssemblyLoadCase)

        @property
        def root_assembly_load_case(
            self: "AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase",
        ) -> "_6949.RootAssemblyLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6949

            return self._parent._cast(_6949.RootAssemblyLoadCase)

        @property
        def specialised_assembly_load_case(
            self: "AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase",
        ) -> "_6953.SpecialisedAssemblyLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6953

            return self._parent._cast(_6953.SpecialisedAssemblyLoadCase)

        @property
        def spiral_bevel_gear_set_load_case(
            self: "AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase",
        ) -> "_6956.SpiralBevelGearSetLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6956

            return self._parent._cast(_6956.SpiralBevelGearSetLoadCase)

        @property
        def spring_damper_load_case(
            self: "AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase",
        ) -> "_6959.SpringDamperLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6959

            return self._parent._cast(_6959.SpringDamperLoadCase)

        @property
        def straight_bevel_diff_gear_set_load_case(
            self: "AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase",
        ) -> "_6962.StraightBevelDiffGearSetLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6962

            return self._parent._cast(_6962.StraightBevelDiffGearSetLoadCase)

        @property
        def straight_bevel_gear_set_load_case(
            self: "AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase",
        ) -> "_6965.StraightBevelGearSetLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6965

            return self._parent._cast(_6965.StraightBevelGearSetLoadCase)

        @property
        def synchroniser_load_case(
            self: "AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase",
        ) -> "_6969.SynchroniserLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6969

            return self._parent._cast(_6969.SynchroniserLoadCase)

        @property
        def torque_converter_load_case(
            self: "AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase",
        ) -> "_6974.TorqueConverterLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6974

            return self._parent._cast(_6974.TorqueConverterLoadCase)

        @property
        def worm_gear_set_load_case(
            self: "AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase",
        ) -> "_6985.WormGearSetLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6985

            return self._parent._cast(_6985.WormGearSetLoadCase)

        @property
        def zerol_bevel_gear_set_load_case(
            self: "AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase",
        ) -> "_6988.ZerolBevelGearSetLoadCase":
            from mastapy.system_model.analyses_and_results.static_loads import _6988

            return self._parent._cast(_6988.ZerolBevelGearSetLoadCase)

        @property
        def abstract_assembly_load_case(
            self: "AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase",
        ) -> "AbstractAssemblyLoadCase":
            return self._parent

        def __getattr__(
            self: "AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase", name: str
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "AbstractAssemblyLoadCase.TYPE"):
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
    ) -> "AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase":
        return self._Cast_AbstractAssemblyLoadCase(self)
