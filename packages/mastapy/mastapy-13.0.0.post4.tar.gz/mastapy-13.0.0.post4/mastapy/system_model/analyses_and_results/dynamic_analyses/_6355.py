"""MountableComponentDynamicAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6301
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_MOUNTABLE_COMPONENT_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses",
    "MountableComponentDynamicAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2464
    from mastapy.system_model.analyses_and_results.dynamic_analyses import (
        _6280,
        _6284,
        _6287,
        _6290,
        _6291,
        _6292,
        _6299,
        _6304,
        _6305,
        _6308,
        _6312,
        _6315,
        _6318,
        _6323,
        _6326,
        _6331,
        _6336,
        _6340,
        _6344,
        _6347,
        _6350,
        _6353,
        _6354,
        _6356,
        _6360,
        _6363,
        _6364,
        _6365,
        _6366,
        _6367,
        _6371,
        _6374,
        _6377,
        _6382,
        _6383,
        _6386,
        _6389,
        _6390,
        _6392,
        _6393,
        _6394,
        _6397,
        _6398,
        _6399,
        _6400,
        _6401,
        _6404,
        _6357,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import (
        _7546,
        _7547,
        _7544,
    )
    from mastapy.system_model.analyses_and_results import _2657, _2653, _2651


__docformat__ = "restructuredtext en"
__all__ = ("MountableComponentDynamicAnalysis",)


Self = TypeVar("Self", bound="MountableComponentDynamicAnalysis")


class MountableComponentDynamicAnalysis(_6301.ComponentDynamicAnalysis):
    """MountableComponentDynamicAnalysis

    This is a mastapy class.
    """

    TYPE = _MOUNTABLE_COMPONENT_DYNAMIC_ANALYSIS
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_MountableComponentDynamicAnalysis")

    class _Cast_MountableComponentDynamicAnalysis:
        """Special nested class for casting MountableComponentDynamicAnalysis to subclasses."""

        def __init__(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
            parent: "MountableComponentDynamicAnalysis",
        ):
            self._parent = parent

        @property
        def component_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6301.ComponentDynamicAnalysis":
            return self._parent._cast(_6301.ComponentDynamicAnalysis)

        @property
        def part_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6357.PartDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6357

            return self._parent._cast(_6357.PartDynamicAnalysis)

        @property
        def part_fe_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_7546.PartFEAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7546

            return self._parent._cast(_7546.PartFEAnalysis)

        @property
        def part_static_load_analysis_case(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_7547.PartStaticLoadAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_7544.PartAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7544

            return self._parent._cast(_7544.PartAnalysisCase)

        @property
        def part_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_2657.PartAnalysis":
            from mastapy.system_model.analyses_and_results import _2657

            return self._parent._cast(_2657.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_2653.DesignEntitySingleContextAnalysis":
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def agma_gleason_conical_gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6280.AGMAGleasonConicalGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6280

            return self._parent._cast(_6280.AGMAGleasonConicalGearDynamicAnalysis)

        @property
        def bearing_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6284.BearingDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6284

            return self._parent._cast(_6284.BearingDynamicAnalysis)

        @property
        def bevel_differential_gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6287.BevelDifferentialGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6287

            return self._parent._cast(_6287.BevelDifferentialGearDynamicAnalysis)

        @property
        def bevel_differential_planet_gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6290.BevelDifferentialPlanetGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6290

            return self._parent._cast(_6290.BevelDifferentialPlanetGearDynamicAnalysis)

        @property
        def bevel_differential_sun_gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6291.BevelDifferentialSunGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6291

            return self._parent._cast(_6291.BevelDifferentialSunGearDynamicAnalysis)

        @property
        def bevel_gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6292.BevelGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6292

            return self._parent._cast(_6292.BevelGearDynamicAnalysis)

        @property
        def clutch_half_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6299.ClutchHalfDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6299

            return self._parent._cast(_6299.ClutchHalfDynamicAnalysis)

        @property
        def concept_coupling_half_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6304.ConceptCouplingHalfDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6304

            return self._parent._cast(_6304.ConceptCouplingHalfDynamicAnalysis)

        @property
        def concept_gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6305.ConceptGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6305

            return self._parent._cast(_6305.ConceptGearDynamicAnalysis)

        @property
        def conical_gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6308.ConicalGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6308

            return self._parent._cast(_6308.ConicalGearDynamicAnalysis)

        @property
        def connector_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6312.ConnectorDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6312

            return self._parent._cast(_6312.ConnectorDynamicAnalysis)

        @property
        def coupling_half_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6315.CouplingHalfDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6315

            return self._parent._cast(_6315.CouplingHalfDynamicAnalysis)

        @property
        def cvt_pulley_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6318.CVTPulleyDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6318

            return self._parent._cast(_6318.CVTPulleyDynamicAnalysis)

        @property
        def cylindrical_gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6323.CylindricalGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6323

            return self._parent._cast(_6323.CylindricalGearDynamicAnalysis)

        @property
        def cylindrical_planet_gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6326.CylindricalPlanetGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6326

            return self._parent._cast(_6326.CylindricalPlanetGearDynamicAnalysis)

        @property
        def face_gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6331.FaceGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6331

            return self._parent._cast(_6331.FaceGearDynamicAnalysis)

        @property
        def gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6336.GearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6336

            return self._parent._cast(_6336.GearDynamicAnalysis)

        @property
        def hypoid_gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6340.HypoidGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6340

            return self._parent._cast(_6340.HypoidGearDynamicAnalysis)

        @property
        def klingelnberg_cyclo_palloid_conical_gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6344.KlingelnbergCycloPalloidConicalGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6344

            return self._parent._cast(
                _6344.KlingelnbergCycloPalloidConicalGearDynamicAnalysis
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6347.KlingelnbergCycloPalloidHypoidGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6347

            return self._parent._cast(
                _6347.KlingelnbergCycloPalloidHypoidGearDynamicAnalysis
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6350.KlingelnbergCycloPalloidSpiralBevelGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6350

            return self._parent._cast(
                _6350.KlingelnbergCycloPalloidSpiralBevelGearDynamicAnalysis
            )

        @property
        def mass_disc_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6353.MassDiscDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6353

            return self._parent._cast(_6353.MassDiscDynamicAnalysis)

        @property
        def measurement_component_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6354.MeasurementComponentDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6354

            return self._parent._cast(_6354.MeasurementComponentDynamicAnalysis)

        @property
        def oil_seal_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6356.OilSealDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6356

            return self._parent._cast(_6356.OilSealDynamicAnalysis)

        @property
        def part_to_part_shear_coupling_half_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6360.PartToPartShearCouplingHalfDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6360

            return self._parent._cast(_6360.PartToPartShearCouplingHalfDynamicAnalysis)

        @property
        def planet_carrier_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6363.PlanetCarrierDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6363

            return self._parent._cast(_6363.PlanetCarrierDynamicAnalysis)

        @property
        def point_load_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6364.PointLoadDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6364

            return self._parent._cast(_6364.PointLoadDynamicAnalysis)

        @property
        def power_load_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6365.PowerLoadDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6365

            return self._parent._cast(_6365.PowerLoadDynamicAnalysis)

        @property
        def pulley_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6366.PulleyDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6366

            return self._parent._cast(_6366.PulleyDynamicAnalysis)

        @property
        def ring_pins_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6367.RingPinsDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6367

            return self._parent._cast(_6367.RingPinsDynamicAnalysis)

        @property
        def rolling_ring_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6371.RollingRingDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6371

            return self._parent._cast(_6371.RollingRingDynamicAnalysis)

        @property
        def shaft_hub_connection_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6374.ShaftHubConnectionDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6374

            return self._parent._cast(_6374.ShaftHubConnectionDynamicAnalysis)

        @property
        def spiral_bevel_gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6377.SpiralBevelGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6377

            return self._parent._cast(_6377.SpiralBevelGearDynamicAnalysis)

        @property
        def spring_damper_half_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6382.SpringDamperHalfDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6382

            return self._parent._cast(_6382.SpringDamperHalfDynamicAnalysis)

        @property
        def straight_bevel_diff_gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6383.StraightBevelDiffGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6383

            return self._parent._cast(_6383.StraightBevelDiffGearDynamicAnalysis)

        @property
        def straight_bevel_gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6386.StraightBevelGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6386

            return self._parent._cast(_6386.StraightBevelGearDynamicAnalysis)

        @property
        def straight_bevel_planet_gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6389.StraightBevelPlanetGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6389

            return self._parent._cast(_6389.StraightBevelPlanetGearDynamicAnalysis)

        @property
        def straight_bevel_sun_gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6390.StraightBevelSunGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6390

            return self._parent._cast(_6390.StraightBevelSunGearDynamicAnalysis)

        @property
        def synchroniser_half_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6392.SynchroniserHalfDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6392

            return self._parent._cast(_6392.SynchroniserHalfDynamicAnalysis)

        @property
        def synchroniser_part_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6393.SynchroniserPartDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6393

            return self._parent._cast(_6393.SynchroniserPartDynamicAnalysis)

        @property
        def synchroniser_sleeve_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6394.SynchroniserSleeveDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6394

            return self._parent._cast(_6394.SynchroniserSleeveDynamicAnalysis)

        @property
        def torque_converter_pump_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6397.TorqueConverterPumpDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6397

            return self._parent._cast(_6397.TorqueConverterPumpDynamicAnalysis)

        @property
        def torque_converter_turbine_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6398.TorqueConverterTurbineDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6398

            return self._parent._cast(_6398.TorqueConverterTurbineDynamicAnalysis)

        @property
        def unbalanced_mass_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6399.UnbalancedMassDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6399

            return self._parent._cast(_6399.UnbalancedMassDynamicAnalysis)

        @property
        def virtual_component_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6400.VirtualComponentDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6400

            return self._parent._cast(_6400.VirtualComponentDynamicAnalysis)

        @property
        def worm_gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6401.WormGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6401

            return self._parent._cast(_6401.WormGearDynamicAnalysis)

        @property
        def zerol_bevel_gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6404.ZerolBevelGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6404

            return self._parent._cast(_6404.ZerolBevelGearDynamicAnalysis)

        @property
        def mountable_component_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "MountableComponentDynamicAnalysis":
            return self._parent

        def __getattr__(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
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
        self: Self, instance_to_wrap: "MountableComponentDynamicAnalysis.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2464.MountableComponent":
        """mastapy.system_model.part_model.MountableComponent

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis":
        return self._Cast_MountableComponentDynamicAnalysis(self)
