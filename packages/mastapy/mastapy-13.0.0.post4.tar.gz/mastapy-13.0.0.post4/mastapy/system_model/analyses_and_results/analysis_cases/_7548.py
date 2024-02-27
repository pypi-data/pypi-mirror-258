"""PartTimeSeriesLoadAnalysisCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy.system_model.analyses_and_results.analysis_cases import _7544
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_PART_TIME_SERIES_LOAD_ANALYSIS_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AnalysisCases",
    "PartTimeSeriesLoadAnalysisCase",
)

if TYPE_CHECKING:
    from mastapy.system_model.analyses_and_results.mbd_analyses import (
        _5375,
        _5376,
        _5377,
        _5380,
        _5381,
        _5383,
        _5384,
        _5387,
        _5389,
        _5390,
        _5391,
        _5392,
        _5394,
        _5395,
        _5396,
        _5397,
        _5399,
        _5400,
        _5403,
        _5405,
        _5406,
        _5408,
        _5409,
        _5411,
        _5412,
        _5414,
        _5416,
        _5417,
        _5419,
        _5420,
        _5421,
        _5423,
        _5426,
        _5427,
        _5428,
        _5429,
        _5430,
        _5432,
        _5433,
        _5434,
        _5435,
        _5438,
        _5439,
        _5440,
        _5442,
        _5443,
        _5450,
        _5451,
        _5453,
        _5454,
        _5456,
        _5457,
        _5458,
        _5462,
        _5463,
        _5465,
        _5466,
        _5468,
        _5469,
        _5471,
        _5472,
        _5473,
        _5474,
        _5475,
        _5476,
        _5478,
        _5480,
        _5481,
        _5484,
        _5485,
        _5488,
        _5490,
        _5491,
        _5493,
        _5494,
        _5496,
        _5497,
        _5499,
        _5500,
        _5501,
        _5502,
        _5503,
        _5504,
        _5505,
        _5506,
        _5509,
        _5510,
        _5512,
        _5513,
        _5514,
        _5517,
        _5518,
        _5520,
        _5521,
    )
    from mastapy.system_model.analyses_and_results import _2657, _2653, _2651


__docformat__ = "restructuredtext en"
__all__ = ("PartTimeSeriesLoadAnalysisCase",)


Self = TypeVar("Self", bound="PartTimeSeriesLoadAnalysisCase")


class PartTimeSeriesLoadAnalysisCase(_7544.PartAnalysisCase):
    """PartTimeSeriesLoadAnalysisCase

    This is a mastapy class.
    """

    TYPE = _PART_TIME_SERIES_LOAD_ANALYSIS_CASE
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_PartTimeSeriesLoadAnalysisCase")

    class _Cast_PartTimeSeriesLoadAnalysisCase:
        """Special nested class for casting PartTimeSeriesLoadAnalysisCase to subclasses."""

        def __init__(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
            parent: "PartTimeSeriesLoadAnalysisCase",
        ):
            self._parent = parent

        @property
        def part_analysis_case(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_7544.PartAnalysisCase":
            return self._parent._cast(_7544.PartAnalysisCase)

        @property
        def part_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_2657.PartAnalysis":
            from mastapy.system_model.analyses_and_results import _2657

            return self._parent._cast(_2657.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_2653.DesignEntitySingleContextAnalysis":
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def abstract_assembly_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5375.AbstractAssemblyMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5375

            return self._parent._cast(_5375.AbstractAssemblyMultibodyDynamicsAnalysis)

        @property
        def abstract_shaft_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5376.AbstractShaftMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5376

            return self._parent._cast(_5376.AbstractShaftMultibodyDynamicsAnalysis)

        @property
        def abstract_shaft_or_housing_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5377.AbstractShaftOrHousingMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5377

            return self._parent._cast(
                _5377.AbstractShaftOrHousingMultibodyDynamicsAnalysis
            )

        @property
        def agma_gleason_conical_gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5380.AGMAGleasonConicalGearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5380

            return self._parent._cast(
                _5380.AGMAGleasonConicalGearMultibodyDynamicsAnalysis
            )

        @property
        def agma_gleason_conical_gear_set_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5381.AGMAGleasonConicalGearSetMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5381

            return self._parent._cast(
                _5381.AGMAGleasonConicalGearSetMultibodyDynamicsAnalysis
            )

        @property
        def assembly_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5383.AssemblyMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5383

            return self._parent._cast(_5383.AssemblyMultibodyDynamicsAnalysis)

        @property
        def bearing_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5384.BearingMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5384

            return self._parent._cast(_5384.BearingMultibodyDynamicsAnalysis)

        @property
        def belt_drive_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5387.BeltDriveMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5387

            return self._parent._cast(_5387.BeltDriveMultibodyDynamicsAnalysis)

        @property
        def bevel_differential_gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5389.BevelDifferentialGearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5389

            return self._parent._cast(
                _5389.BevelDifferentialGearMultibodyDynamicsAnalysis
            )

        @property
        def bevel_differential_gear_set_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5390.BevelDifferentialGearSetMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5390

            return self._parent._cast(
                _5390.BevelDifferentialGearSetMultibodyDynamicsAnalysis
            )

        @property
        def bevel_differential_planet_gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5391.BevelDifferentialPlanetGearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5391

            return self._parent._cast(
                _5391.BevelDifferentialPlanetGearMultibodyDynamicsAnalysis
            )

        @property
        def bevel_differential_sun_gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5392.BevelDifferentialSunGearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5392

            return self._parent._cast(
                _5392.BevelDifferentialSunGearMultibodyDynamicsAnalysis
            )

        @property
        def bevel_gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5394.BevelGearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5394

            return self._parent._cast(_5394.BevelGearMultibodyDynamicsAnalysis)

        @property
        def bevel_gear_set_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5395.BevelGearSetMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5395

            return self._parent._cast(_5395.BevelGearSetMultibodyDynamicsAnalysis)

        @property
        def bolted_joint_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5396.BoltedJointMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5396

            return self._parent._cast(_5396.BoltedJointMultibodyDynamicsAnalysis)

        @property
        def bolt_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5397.BoltMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5397

            return self._parent._cast(_5397.BoltMultibodyDynamicsAnalysis)

        @property
        def clutch_half_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5399.ClutchHalfMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5399

            return self._parent._cast(_5399.ClutchHalfMultibodyDynamicsAnalysis)

        @property
        def clutch_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5400.ClutchMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5400

            return self._parent._cast(_5400.ClutchMultibodyDynamicsAnalysis)

        @property
        def component_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5403.ComponentMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5403

            return self._parent._cast(_5403.ComponentMultibodyDynamicsAnalysis)

        @property
        def concept_coupling_half_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5405.ConceptCouplingHalfMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5405

            return self._parent._cast(
                _5405.ConceptCouplingHalfMultibodyDynamicsAnalysis
            )

        @property
        def concept_coupling_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5406.ConceptCouplingMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5406

            return self._parent._cast(_5406.ConceptCouplingMultibodyDynamicsAnalysis)

        @property
        def concept_gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5408.ConceptGearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5408

            return self._parent._cast(_5408.ConceptGearMultibodyDynamicsAnalysis)

        @property
        def concept_gear_set_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5409.ConceptGearSetMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5409

            return self._parent._cast(_5409.ConceptGearSetMultibodyDynamicsAnalysis)

        @property
        def conical_gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5411.ConicalGearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5411

            return self._parent._cast(_5411.ConicalGearMultibodyDynamicsAnalysis)

        @property
        def conical_gear_set_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5412.ConicalGearSetMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5412

            return self._parent._cast(_5412.ConicalGearSetMultibodyDynamicsAnalysis)

        @property
        def connector_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5414.ConnectorMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5414

            return self._parent._cast(_5414.ConnectorMultibodyDynamicsAnalysis)

        @property
        def coupling_half_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5416.CouplingHalfMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5416

            return self._parent._cast(_5416.CouplingHalfMultibodyDynamicsAnalysis)

        @property
        def coupling_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5417.CouplingMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5417

            return self._parent._cast(_5417.CouplingMultibodyDynamicsAnalysis)

        @property
        def cvt_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5419.CVTMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5419

            return self._parent._cast(_5419.CVTMultibodyDynamicsAnalysis)

        @property
        def cvt_pulley_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5420.CVTPulleyMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5420

            return self._parent._cast(_5420.CVTPulleyMultibodyDynamicsAnalysis)

        @property
        def cycloidal_assembly_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5421.CycloidalAssemblyMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5421

            return self._parent._cast(_5421.CycloidalAssemblyMultibodyDynamicsAnalysis)

        @property
        def cycloidal_disc_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5423.CycloidalDiscMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5423

            return self._parent._cast(_5423.CycloidalDiscMultibodyDynamicsAnalysis)

        @property
        def cylindrical_gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5426.CylindricalGearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5426

            return self._parent._cast(_5426.CylindricalGearMultibodyDynamicsAnalysis)

        @property
        def cylindrical_gear_set_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5427.CylindricalGearSetMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5427

            return self._parent._cast(_5427.CylindricalGearSetMultibodyDynamicsAnalysis)

        @property
        def cylindrical_planet_gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5428.CylindricalPlanetGearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5428

            return self._parent._cast(
                _5428.CylindricalPlanetGearMultibodyDynamicsAnalysis
            )

        @property
        def datum_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5429.DatumMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5429

            return self._parent._cast(_5429.DatumMultibodyDynamicsAnalysis)

        @property
        def external_cad_model_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5430.ExternalCADModelMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5430

            return self._parent._cast(_5430.ExternalCADModelMultibodyDynamicsAnalysis)

        @property
        def face_gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5432.FaceGearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5432

            return self._parent._cast(_5432.FaceGearMultibodyDynamicsAnalysis)

        @property
        def face_gear_set_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5433.FaceGearSetMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5433

            return self._parent._cast(_5433.FaceGearSetMultibodyDynamicsAnalysis)

        @property
        def fe_part_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5434.FEPartMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5434

            return self._parent._cast(_5434.FEPartMultibodyDynamicsAnalysis)

        @property
        def flexible_pin_assembly_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5435.FlexiblePinAssemblyMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5435

            return self._parent._cast(
                _5435.FlexiblePinAssemblyMultibodyDynamicsAnalysis
            )

        @property
        def gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5438.GearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5438

            return self._parent._cast(_5438.GearMultibodyDynamicsAnalysis)

        @property
        def gear_set_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5439.GearSetMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5439

            return self._parent._cast(_5439.GearSetMultibodyDynamicsAnalysis)

        @property
        def guide_dxf_model_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5440.GuideDxfModelMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5440

            return self._parent._cast(_5440.GuideDxfModelMultibodyDynamicsAnalysis)

        @property
        def hypoid_gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5442.HypoidGearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5442

            return self._parent._cast(_5442.HypoidGearMultibodyDynamicsAnalysis)

        @property
        def hypoid_gear_set_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5443.HypoidGearSetMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5443

            return self._parent._cast(_5443.HypoidGearSetMultibodyDynamicsAnalysis)

        @property
        def klingelnberg_cyclo_palloid_conical_gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5450.KlingelnbergCycloPalloidConicalGearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5450

            return self._parent._cast(
                _5450.KlingelnbergCycloPalloidConicalGearMultibodyDynamicsAnalysis
            )

        @property
        def klingelnberg_cyclo_palloid_conical_gear_set_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5451.KlingelnbergCycloPalloidConicalGearSetMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5451

            return self._parent._cast(
                _5451.KlingelnbergCycloPalloidConicalGearSetMultibodyDynamicsAnalysis
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5453.KlingelnbergCycloPalloidHypoidGearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5453

            return self._parent._cast(
                _5453.KlingelnbergCycloPalloidHypoidGearMultibodyDynamicsAnalysis
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_set_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5454.KlingelnbergCycloPalloidHypoidGearSetMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5454

            return self._parent._cast(
                _5454.KlingelnbergCycloPalloidHypoidGearSetMultibodyDynamicsAnalysis
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5456.KlingelnbergCycloPalloidSpiralBevelGearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5456

            return self._parent._cast(
                _5456.KlingelnbergCycloPalloidSpiralBevelGearMultibodyDynamicsAnalysis
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> (
            "_5457.KlingelnbergCycloPalloidSpiralBevelGearSetMultibodyDynamicsAnalysis"
        ):
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5457

            return self._parent._cast(
                _5457.KlingelnbergCycloPalloidSpiralBevelGearSetMultibodyDynamicsAnalysis
            )

        @property
        def mass_disc_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5458.MassDiscMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5458

            return self._parent._cast(_5458.MassDiscMultibodyDynamicsAnalysis)

        @property
        def measurement_component_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5462.MeasurementComponentMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5462

            return self._parent._cast(
                _5462.MeasurementComponentMultibodyDynamicsAnalysis
            )

        @property
        def mountable_component_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5463.MountableComponentMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5463

            return self._parent._cast(_5463.MountableComponentMultibodyDynamicsAnalysis)

        @property
        def oil_seal_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5465.OilSealMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5465

            return self._parent._cast(_5465.OilSealMultibodyDynamicsAnalysis)

        @property
        def part_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5466.PartMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5466

            return self._parent._cast(_5466.PartMultibodyDynamicsAnalysis)

        @property
        def part_to_part_shear_coupling_half_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5468.PartToPartShearCouplingHalfMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5468

            return self._parent._cast(
                _5468.PartToPartShearCouplingHalfMultibodyDynamicsAnalysis
            )

        @property
        def part_to_part_shear_coupling_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5469.PartToPartShearCouplingMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5469

            return self._parent._cast(
                _5469.PartToPartShearCouplingMultibodyDynamicsAnalysis
            )

        @property
        def planetary_gear_set_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5471.PlanetaryGearSetMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5471

            return self._parent._cast(_5471.PlanetaryGearSetMultibodyDynamicsAnalysis)

        @property
        def planet_carrier_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5472.PlanetCarrierMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5472

            return self._parent._cast(_5472.PlanetCarrierMultibodyDynamicsAnalysis)

        @property
        def point_load_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5473.PointLoadMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5473

            return self._parent._cast(_5473.PointLoadMultibodyDynamicsAnalysis)

        @property
        def power_load_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5474.PowerLoadMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5474

            return self._parent._cast(_5474.PowerLoadMultibodyDynamicsAnalysis)

        @property
        def pulley_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5475.PulleyMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5475

            return self._parent._cast(_5475.PulleyMultibodyDynamicsAnalysis)

        @property
        def ring_pins_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5476.RingPinsMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5476

            return self._parent._cast(_5476.RingPinsMultibodyDynamicsAnalysis)

        @property
        def rolling_ring_assembly_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5478.RollingRingAssemblyMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5478

            return self._parent._cast(
                _5478.RollingRingAssemblyMultibodyDynamicsAnalysis
            )

        @property
        def rolling_ring_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5480.RollingRingMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5480

            return self._parent._cast(_5480.RollingRingMultibodyDynamicsAnalysis)

        @property
        def root_assembly_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5481.RootAssemblyMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5481

            return self._parent._cast(_5481.RootAssemblyMultibodyDynamicsAnalysis)

        @property
        def shaft_hub_connection_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5484.ShaftHubConnectionMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5484

            return self._parent._cast(_5484.ShaftHubConnectionMultibodyDynamicsAnalysis)

        @property
        def shaft_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5485.ShaftMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5485

            return self._parent._cast(_5485.ShaftMultibodyDynamicsAnalysis)

        @property
        def specialised_assembly_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5488.SpecialisedAssemblyMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5488

            return self._parent._cast(
                _5488.SpecialisedAssemblyMultibodyDynamicsAnalysis
            )

        @property
        def spiral_bevel_gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5490.SpiralBevelGearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5490

            return self._parent._cast(_5490.SpiralBevelGearMultibodyDynamicsAnalysis)

        @property
        def spiral_bevel_gear_set_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5491.SpiralBevelGearSetMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5491

            return self._parent._cast(_5491.SpiralBevelGearSetMultibodyDynamicsAnalysis)

        @property
        def spring_damper_half_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5493.SpringDamperHalfMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5493

            return self._parent._cast(_5493.SpringDamperHalfMultibodyDynamicsAnalysis)

        @property
        def spring_damper_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5494.SpringDamperMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5494

            return self._parent._cast(_5494.SpringDamperMultibodyDynamicsAnalysis)

        @property
        def straight_bevel_diff_gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5496.StraightBevelDiffGearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5496

            return self._parent._cast(
                _5496.StraightBevelDiffGearMultibodyDynamicsAnalysis
            )

        @property
        def straight_bevel_diff_gear_set_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5497.StraightBevelDiffGearSetMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5497

            return self._parent._cast(
                _5497.StraightBevelDiffGearSetMultibodyDynamicsAnalysis
            )

        @property
        def straight_bevel_gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5499.StraightBevelGearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5499

            return self._parent._cast(_5499.StraightBevelGearMultibodyDynamicsAnalysis)

        @property
        def straight_bevel_gear_set_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5500.StraightBevelGearSetMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5500

            return self._parent._cast(
                _5500.StraightBevelGearSetMultibodyDynamicsAnalysis
            )

        @property
        def straight_bevel_planet_gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5501.StraightBevelPlanetGearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5501

            return self._parent._cast(
                _5501.StraightBevelPlanetGearMultibodyDynamicsAnalysis
            )

        @property
        def straight_bevel_sun_gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5502.StraightBevelSunGearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5502

            return self._parent._cast(
                _5502.StraightBevelSunGearMultibodyDynamicsAnalysis
            )

        @property
        def synchroniser_half_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5503.SynchroniserHalfMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5503

            return self._parent._cast(_5503.SynchroniserHalfMultibodyDynamicsAnalysis)

        @property
        def synchroniser_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5504.SynchroniserMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5504

            return self._parent._cast(_5504.SynchroniserMultibodyDynamicsAnalysis)

        @property
        def synchroniser_part_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5505.SynchroniserPartMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5505

            return self._parent._cast(_5505.SynchroniserPartMultibodyDynamicsAnalysis)

        @property
        def synchroniser_sleeve_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5506.SynchroniserSleeveMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5506

            return self._parent._cast(_5506.SynchroniserSleeveMultibodyDynamicsAnalysis)

        @property
        def torque_converter_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5509.TorqueConverterMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5509

            return self._parent._cast(_5509.TorqueConverterMultibodyDynamicsAnalysis)

        @property
        def torque_converter_pump_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5510.TorqueConverterPumpMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5510

            return self._parent._cast(
                _5510.TorqueConverterPumpMultibodyDynamicsAnalysis
            )

        @property
        def torque_converter_turbine_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5512.TorqueConverterTurbineMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5512

            return self._parent._cast(
                _5512.TorqueConverterTurbineMultibodyDynamicsAnalysis
            )

        @property
        def unbalanced_mass_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5513.UnbalancedMassMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5513

            return self._parent._cast(_5513.UnbalancedMassMultibodyDynamicsAnalysis)

        @property
        def virtual_component_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5514.VirtualComponentMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5514

            return self._parent._cast(_5514.VirtualComponentMultibodyDynamicsAnalysis)

        @property
        def worm_gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5517.WormGearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5517

            return self._parent._cast(_5517.WormGearMultibodyDynamicsAnalysis)

        @property
        def worm_gear_set_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5518.WormGearSetMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5518

            return self._parent._cast(_5518.WormGearSetMultibodyDynamicsAnalysis)

        @property
        def zerol_bevel_gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5520.ZerolBevelGearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5520

            return self._parent._cast(_5520.ZerolBevelGearMultibodyDynamicsAnalysis)

        @property
        def zerol_bevel_gear_set_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5521.ZerolBevelGearSetMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5521

            return self._parent._cast(_5521.ZerolBevelGearSetMultibodyDynamicsAnalysis)

        @property
        def part_time_series_load_analysis_case(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "PartTimeSeriesLoadAnalysisCase":
            return self._parent

        def __getattr__(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "PartTimeSeriesLoadAnalysisCase.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cast_to(
        self: Self,
    ) -> "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase":
        return self._Cast_PartTimeSeriesLoadAnalysisCase(self)
