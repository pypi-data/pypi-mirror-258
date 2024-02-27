"""MountableComponentDynamicAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6302
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_MOUNTABLE_COMPONENT_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses",
    "MountableComponentDynamicAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2464
    from mastapy.system_model.analyses_and_results.dynamic_analyses import (
        _6281,
        _6285,
        _6288,
        _6291,
        _6292,
        _6293,
        _6300,
        _6305,
        _6306,
        _6309,
        _6313,
        _6316,
        _6319,
        _6324,
        _6327,
        _6332,
        _6337,
        _6341,
        _6345,
        _6348,
        _6351,
        _6354,
        _6355,
        _6357,
        _6361,
        _6364,
        _6365,
        _6366,
        _6367,
        _6368,
        _6372,
        _6375,
        _6378,
        _6383,
        _6384,
        _6387,
        _6390,
        _6391,
        _6393,
        _6394,
        _6395,
        _6398,
        _6399,
        _6400,
        _6401,
        _6402,
        _6405,
        _6358,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import (
        _7547,
        _7548,
        _7545,
    )
    from mastapy.system_model.analyses_and_results import _2657, _2653, _2651


__docformat__ = "restructuredtext en"
__all__ = ("MountableComponentDynamicAnalysis",)


Self = TypeVar("Self", bound="MountableComponentDynamicAnalysis")


class MountableComponentDynamicAnalysis(_6302.ComponentDynamicAnalysis):
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
        ) -> "_6302.ComponentDynamicAnalysis":
            return self._parent._cast(_6302.ComponentDynamicAnalysis)

        @property
        def part_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6358.PartDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6358

            return self._parent._cast(_6358.PartDynamicAnalysis)

        @property
        def part_fe_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_7547.PartFEAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartFEAnalysis)

        @property
        def part_static_load_analysis_case(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_7548.PartStaticLoadAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7548

            return self._parent._cast(_7548.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_7545.PartAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7545

            return self._parent._cast(_7545.PartAnalysisCase)

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
        ) -> "_6281.AGMAGleasonConicalGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6281

            return self._parent._cast(_6281.AGMAGleasonConicalGearDynamicAnalysis)

        @property
        def bearing_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6285.BearingDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6285

            return self._parent._cast(_6285.BearingDynamicAnalysis)

        @property
        def bevel_differential_gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6288.BevelDifferentialGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6288

            return self._parent._cast(_6288.BevelDifferentialGearDynamicAnalysis)

        @property
        def bevel_differential_planet_gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6291.BevelDifferentialPlanetGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6291

            return self._parent._cast(_6291.BevelDifferentialPlanetGearDynamicAnalysis)

        @property
        def bevel_differential_sun_gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6292.BevelDifferentialSunGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6292

            return self._parent._cast(_6292.BevelDifferentialSunGearDynamicAnalysis)

        @property
        def bevel_gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6293.BevelGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6293

            return self._parent._cast(_6293.BevelGearDynamicAnalysis)

        @property
        def clutch_half_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6300.ClutchHalfDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6300

            return self._parent._cast(_6300.ClutchHalfDynamicAnalysis)

        @property
        def concept_coupling_half_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6305.ConceptCouplingHalfDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6305

            return self._parent._cast(_6305.ConceptCouplingHalfDynamicAnalysis)

        @property
        def concept_gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6306.ConceptGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6306

            return self._parent._cast(_6306.ConceptGearDynamicAnalysis)

        @property
        def conical_gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6309.ConicalGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6309

            return self._parent._cast(_6309.ConicalGearDynamicAnalysis)

        @property
        def connector_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6313.ConnectorDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6313

            return self._parent._cast(_6313.ConnectorDynamicAnalysis)

        @property
        def coupling_half_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6316.CouplingHalfDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6316

            return self._parent._cast(_6316.CouplingHalfDynamicAnalysis)

        @property
        def cvt_pulley_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6319.CVTPulleyDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6319

            return self._parent._cast(_6319.CVTPulleyDynamicAnalysis)

        @property
        def cylindrical_gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6324.CylindricalGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6324

            return self._parent._cast(_6324.CylindricalGearDynamicAnalysis)

        @property
        def cylindrical_planet_gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6327.CylindricalPlanetGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6327

            return self._parent._cast(_6327.CylindricalPlanetGearDynamicAnalysis)

        @property
        def face_gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6332.FaceGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6332

            return self._parent._cast(_6332.FaceGearDynamicAnalysis)

        @property
        def gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6337.GearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6337

            return self._parent._cast(_6337.GearDynamicAnalysis)

        @property
        def hypoid_gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6341.HypoidGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6341

            return self._parent._cast(_6341.HypoidGearDynamicAnalysis)

        @property
        def klingelnberg_cyclo_palloid_conical_gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6345.KlingelnbergCycloPalloidConicalGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6345

            return self._parent._cast(
                _6345.KlingelnbergCycloPalloidConicalGearDynamicAnalysis
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6348.KlingelnbergCycloPalloidHypoidGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6348

            return self._parent._cast(
                _6348.KlingelnbergCycloPalloidHypoidGearDynamicAnalysis
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6351.KlingelnbergCycloPalloidSpiralBevelGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6351

            return self._parent._cast(
                _6351.KlingelnbergCycloPalloidSpiralBevelGearDynamicAnalysis
            )

        @property
        def mass_disc_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6354.MassDiscDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6354

            return self._parent._cast(_6354.MassDiscDynamicAnalysis)

        @property
        def measurement_component_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6355.MeasurementComponentDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6355

            return self._parent._cast(_6355.MeasurementComponentDynamicAnalysis)

        @property
        def oil_seal_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6357.OilSealDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6357

            return self._parent._cast(_6357.OilSealDynamicAnalysis)

        @property
        def part_to_part_shear_coupling_half_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6361.PartToPartShearCouplingHalfDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6361

            return self._parent._cast(_6361.PartToPartShearCouplingHalfDynamicAnalysis)

        @property
        def planet_carrier_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6364.PlanetCarrierDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6364

            return self._parent._cast(_6364.PlanetCarrierDynamicAnalysis)

        @property
        def point_load_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6365.PointLoadDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6365

            return self._parent._cast(_6365.PointLoadDynamicAnalysis)

        @property
        def power_load_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6366.PowerLoadDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6366

            return self._parent._cast(_6366.PowerLoadDynamicAnalysis)

        @property
        def pulley_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6367.PulleyDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6367

            return self._parent._cast(_6367.PulleyDynamicAnalysis)

        @property
        def ring_pins_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6368.RingPinsDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6368

            return self._parent._cast(_6368.RingPinsDynamicAnalysis)

        @property
        def rolling_ring_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6372.RollingRingDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6372

            return self._parent._cast(_6372.RollingRingDynamicAnalysis)

        @property
        def shaft_hub_connection_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6375.ShaftHubConnectionDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6375

            return self._parent._cast(_6375.ShaftHubConnectionDynamicAnalysis)

        @property
        def spiral_bevel_gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6378.SpiralBevelGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6378

            return self._parent._cast(_6378.SpiralBevelGearDynamicAnalysis)

        @property
        def spring_damper_half_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6383.SpringDamperHalfDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6383

            return self._parent._cast(_6383.SpringDamperHalfDynamicAnalysis)

        @property
        def straight_bevel_diff_gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6384.StraightBevelDiffGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6384

            return self._parent._cast(_6384.StraightBevelDiffGearDynamicAnalysis)

        @property
        def straight_bevel_gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6387.StraightBevelGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6387

            return self._parent._cast(_6387.StraightBevelGearDynamicAnalysis)

        @property
        def straight_bevel_planet_gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6390.StraightBevelPlanetGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6390

            return self._parent._cast(_6390.StraightBevelPlanetGearDynamicAnalysis)

        @property
        def straight_bevel_sun_gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6391.StraightBevelSunGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6391

            return self._parent._cast(_6391.StraightBevelSunGearDynamicAnalysis)

        @property
        def synchroniser_half_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6393.SynchroniserHalfDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6393

            return self._parent._cast(_6393.SynchroniserHalfDynamicAnalysis)

        @property
        def synchroniser_part_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6394.SynchroniserPartDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6394

            return self._parent._cast(_6394.SynchroniserPartDynamicAnalysis)

        @property
        def synchroniser_sleeve_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6395.SynchroniserSleeveDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6395

            return self._parent._cast(_6395.SynchroniserSleeveDynamicAnalysis)

        @property
        def torque_converter_pump_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6398.TorqueConverterPumpDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6398

            return self._parent._cast(_6398.TorqueConverterPumpDynamicAnalysis)

        @property
        def torque_converter_turbine_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6399.TorqueConverterTurbineDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6399

            return self._parent._cast(_6399.TorqueConverterTurbineDynamicAnalysis)

        @property
        def unbalanced_mass_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6400.UnbalancedMassDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6400

            return self._parent._cast(_6400.UnbalancedMassDynamicAnalysis)

        @property
        def virtual_component_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6401.VirtualComponentDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6401

            return self._parent._cast(_6401.VirtualComponentDynamicAnalysis)

        @property
        def worm_gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6402.WormGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6402

            return self._parent._cast(_6402.WormGearDynamicAnalysis)

        @property
        def zerol_bevel_gear_dynamic_analysis(
            self: "MountableComponentDynamicAnalysis._Cast_MountableComponentDynamicAnalysis",
        ) -> "_6405.ZerolBevelGearDynamicAnalysis":
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6405

            return self._parent._cast(_6405.ZerolBevelGearDynamicAnalysis)

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
