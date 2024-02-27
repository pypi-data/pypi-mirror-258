"""PartTimeSeriesLoadAnalysisCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy.system_model.analyses_and_results.analysis_cases import _7545
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_PART_TIME_SERIES_LOAD_ANALYSIS_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AnalysisCases",
    "PartTimeSeriesLoadAnalysisCase",
)

if TYPE_CHECKING:
    from mastapy.system_model.analyses_and_results.mbd_analyses import (
        _5376,
        _5377,
        _5378,
        _5381,
        _5382,
        _5384,
        _5385,
        _5388,
        _5390,
        _5391,
        _5392,
        _5393,
        _5395,
        _5396,
        _5397,
        _5398,
        _5400,
        _5401,
        _5404,
        _5406,
        _5407,
        _5409,
        _5410,
        _5412,
        _5413,
        _5415,
        _5417,
        _5418,
        _5420,
        _5421,
        _5422,
        _5424,
        _5427,
        _5428,
        _5429,
        _5430,
        _5431,
        _5433,
        _5434,
        _5435,
        _5436,
        _5439,
        _5440,
        _5441,
        _5443,
        _5444,
        _5451,
        _5452,
        _5454,
        _5455,
        _5457,
        _5458,
        _5459,
        _5463,
        _5464,
        _5466,
        _5467,
        _5469,
        _5470,
        _5472,
        _5473,
        _5474,
        _5475,
        _5476,
        _5477,
        _5479,
        _5481,
        _5482,
        _5485,
        _5486,
        _5489,
        _5491,
        _5492,
        _5494,
        _5495,
        _5497,
        _5498,
        _5500,
        _5501,
        _5502,
        _5503,
        _5504,
        _5505,
        _5506,
        _5507,
        _5510,
        _5511,
        _5513,
        _5514,
        _5515,
        _5518,
        _5519,
        _5521,
        _5522,
    )
    from mastapy.system_model.analyses_and_results import _2657, _2653, _2651


__docformat__ = "restructuredtext en"
__all__ = ("PartTimeSeriesLoadAnalysisCase",)


Self = TypeVar("Self", bound="PartTimeSeriesLoadAnalysisCase")


class PartTimeSeriesLoadAnalysisCase(_7545.PartAnalysisCase):
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
        ) -> "_7545.PartAnalysisCase":
            return self._parent._cast(_7545.PartAnalysisCase)

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
        ) -> "_5376.AbstractAssemblyMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5376

            return self._parent._cast(_5376.AbstractAssemblyMultibodyDynamicsAnalysis)

        @property
        def abstract_shaft_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5377.AbstractShaftMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5377

            return self._parent._cast(_5377.AbstractShaftMultibodyDynamicsAnalysis)

        @property
        def abstract_shaft_or_housing_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5378.AbstractShaftOrHousingMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5378

            return self._parent._cast(
                _5378.AbstractShaftOrHousingMultibodyDynamicsAnalysis
            )

        @property
        def agma_gleason_conical_gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5381.AGMAGleasonConicalGearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5381

            return self._parent._cast(
                _5381.AGMAGleasonConicalGearMultibodyDynamicsAnalysis
            )

        @property
        def agma_gleason_conical_gear_set_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5382.AGMAGleasonConicalGearSetMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5382

            return self._parent._cast(
                _5382.AGMAGleasonConicalGearSetMultibodyDynamicsAnalysis
            )

        @property
        def assembly_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5384.AssemblyMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5384

            return self._parent._cast(_5384.AssemblyMultibodyDynamicsAnalysis)

        @property
        def bearing_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5385.BearingMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5385

            return self._parent._cast(_5385.BearingMultibodyDynamicsAnalysis)

        @property
        def belt_drive_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5388.BeltDriveMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5388

            return self._parent._cast(_5388.BeltDriveMultibodyDynamicsAnalysis)

        @property
        def bevel_differential_gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5390.BevelDifferentialGearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5390

            return self._parent._cast(
                _5390.BevelDifferentialGearMultibodyDynamicsAnalysis
            )

        @property
        def bevel_differential_gear_set_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5391.BevelDifferentialGearSetMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5391

            return self._parent._cast(
                _5391.BevelDifferentialGearSetMultibodyDynamicsAnalysis
            )

        @property
        def bevel_differential_planet_gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5392.BevelDifferentialPlanetGearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5392

            return self._parent._cast(
                _5392.BevelDifferentialPlanetGearMultibodyDynamicsAnalysis
            )

        @property
        def bevel_differential_sun_gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5393.BevelDifferentialSunGearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5393

            return self._parent._cast(
                _5393.BevelDifferentialSunGearMultibodyDynamicsAnalysis
            )

        @property
        def bevel_gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5395.BevelGearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5395

            return self._parent._cast(_5395.BevelGearMultibodyDynamicsAnalysis)

        @property
        def bevel_gear_set_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5396.BevelGearSetMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5396

            return self._parent._cast(_5396.BevelGearSetMultibodyDynamicsAnalysis)

        @property
        def bolted_joint_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5397.BoltedJointMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5397

            return self._parent._cast(_5397.BoltedJointMultibodyDynamicsAnalysis)

        @property
        def bolt_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5398.BoltMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5398

            return self._parent._cast(_5398.BoltMultibodyDynamicsAnalysis)

        @property
        def clutch_half_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5400.ClutchHalfMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5400

            return self._parent._cast(_5400.ClutchHalfMultibodyDynamicsAnalysis)

        @property
        def clutch_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5401.ClutchMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5401

            return self._parent._cast(_5401.ClutchMultibodyDynamicsAnalysis)

        @property
        def component_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5404.ComponentMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5404

            return self._parent._cast(_5404.ComponentMultibodyDynamicsAnalysis)

        @property
        def concept_coupling_half_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5406.ConceptCouplingHalfMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5406

            return self._parent._cast(
                _5406.ConceptCouplingHalfMultibodyDynamicsAnalysis
            )

        @property
        def concept_coupling_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5407.ConceptCouplingMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5407

            return self._parent._cast(_5407.ConceptCouplingMultibodyDynamicsAnalysis)

        @property
        def concept_gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5409.ConceptGearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5409

            return self._parent._cast(_5409.ConceptGearMultibodyDynamicsAnalysis)

        @property
        def concept_gear_set_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5410.ConceptGearSetMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5410

            return self._parent._cast(_5410.ConceptGearSetMultibodyDynamicsAnalysis)

        @property
        def conical_gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5412.ConicalGearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5412

            return self._parent._cast(_5412.ConicalGearMultibodyDynamicsAnalysis)

        @property
        def conical_gear_set_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5413.ConicalGearSetMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5413

            return self._parent._cast(_5413.ConicalGearSetMultibodyDynamicsAnalysis)

        @property
        def connector_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5415.ConnectorMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5415

            return self._parent._cast(_5415.ConnectorMultibodyDynamicsAnalysis)

        @property
        def coupling_half_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5417.CouplingHalfMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5417

            return self._parent._cast(_5417.CouplingHalfMultibodyDynamicsAnalysis)

        @property
        def coupling_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5418.CouplingMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5418

            return self._parent._cast(_5418.CouplingMultibodyDynamicsAnalysis)

        @property
        def cvt_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5420.CVTMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5420

            return self._parent._cast(_5420.CVTMultibodyDynamicsAnalysis)

        @property
        def cvt_pulley_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5421.CVTPulleyMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5421

            return self._parent._cast(_5421.CVTPulleyMultibodyDynamicsAnalysis)

        @property
        def cycloidal_assembly_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5422.CycloidalAssemblyMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5422

            return self._parent._cast(_5422.CycloidalAssemblyMultibodyDynamicsAnalysis)

        @property
        def cycloidal_disc_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5424.CycloidalDiscMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5424

            return self._parent._cast(_5424.CycloidalDiscMultibodyDynamicsAnalysis)

        @property
        def cylindrical_gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5427.CylindricalGearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5427

            return self._parent._cast(_5427.CylindricalGearMultibodyDynamicsAnalysis)

        @property
        def cylindrical_gear_set_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5428.CylindricalGearSetMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5428

            return self._parent._cast(_5428.CylindricalGearSetMultibodyDynamicsAnalysis)

        @property
        def cylindrical_planet_gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5429.CylindricalPlanetGearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5429

            return self._parent._cast(
                _5429.CylindricalPlanetGearMultibodyDynamicsAnalysis
            )

        @property
        def datum_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5430.DatumMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5430

            return self._parent._cast(_5430.DatumMultibodyDynamicsAnalysis)

        @property
        def external_cad_model_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5431.ExternalCADModelMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5431

            return self._parent._cast(_5431.ExternalCADModelMultibodyDynamicsAnalysis)

        @property
        def face_gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5433.FaceGearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5433

            return self._parent._cast(_5433.FaceGearMultibodyDynamicsAnalysis)

        @property
        def face_gear_set_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5434.FaceGearSetMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5434

            return self._parent._cast(_5434.FaceGearSetMultibodyDynamicsAnalysis)

        @property
        def fe_part_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5435.FEPartMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5435

            return self._parent._cast(_5435.FEPartMultibodyDynamicsAnalysis)

        @property
        def flexible_pin_assembly_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5436.FlexiblePinAssemblyMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5436

            return self._parent._cast(
                _5436.FlexiblePinAssemblyMultibodyDynamicsAnalysis
            )

        @property
        def gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5439.GearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5439

            return self._parent._cast(_5439.GearMultibodyDynamicsAnalysis)

        @property
        def gear_set_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5440.GearSetMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5440

            return self._parent._cast(_5440.GearSetMultibodyDynamicsAnalysis)

        @property
        def guide_dxf_model_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5441.GuideDxfModelMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5441

            return self._parent._cast(_5441.GuideDxfModelMultibodyDynamicsAnalysis)

        @property
        def hypoid_gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5443.HypoidGearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5443

            return self._parent._cast(_5443.HypoidGearMultibodyDynamicsAnalysis)

        @property
        def hypoid_gear_set_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5444.HypoidGearSetMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5444

            return self._parent._cast(_5444.HypoidGearSetMultibodyDynamicsAnalysis)

        @property
        def klingelnberg_cyclo_palloid_conical_gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5451.KlingelnbergCycloPalloidConicalGearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5451

            return self._parent._cast(
                _5451.KlingelnbergCycloPalloidConicalGearMultibodyDynamicsAnalysis
            )

        @property
        def klingelnberg_cyclo_palloid_conical_gear_set_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5452.KlingelnbergCycloPalloidConicalGearSetMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5452

            return self._parent._cast(
                _5452.KlingelnbergCycloPalloidConicalGearSetMultibodyDynamicsAnalysis
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5454.KlingelnbergCycloPalloidHypoidGearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5454

            return self._parent._cast(
                _5454.KlingelnbergCycloPalloidHypoidGearMultibodyDynamicsAnalysis
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_set_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5455.KlingelnbergCycloPalloidHypoidGearSetMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5455

            return self._parent._cast(
                _5455.KlingelnbergCycloPalloidHypoidGearSetMultibodyDynamicsAnalysis
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5457.KlingelnbergCycloPalloidSpiralBevelGearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5457

            return self._parent._cast(
                _5457.KlingelnbergCycloPalloidSpiralBevelGearMultibodyDynamicsAnalysis
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> (
            "_5458.KlingelnbergCycloPalloidSpiralBevelGearSetMultibodyDynamicsAnalysis"
        ):
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5458

            return self._parent._cast(
                _5458.KlingelnbergCycloPalloidSpiralBevelGearSetMultibodyDynamicsAnalysis
            )

        @property
        def mass_disc_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5459.MassDiscMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5459

            return self._parent._cast(_5459.MassDiscMultibodyDynamicsAnalysis)

        @property
        def measurement_component_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5463.MeasurementComponentMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5463

            return self._parent._cast(
                _5463.MeasurementComponentMultibodyDynamicsAnalysis
            )

        @property
        def mountable_component_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5464.MountableComponentMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5464

            return self._parent._cast(_5464.MountableComponentMultibodyDynamicsAnalysis)

        @property
        def oil_seal_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5466.OilSealMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5466

            return self._parent._cast(_5466.OilSealMultibodyDynamicsAnalysis)

        @property
        def part_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5467.PartMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5467

            return self._parent._cast(_5467.PartMultibodyDynamicsAnalysis)

        @property
        def part_to_part_shear_coupling_half_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5469.PartToPartShearCouplingHalfMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5469

            return self._parent._cast(
                _5469.PartToPartShearCouplingHalfMultibodyDynamicsAnalysis
            )

        @property
        def part_to_part_shear_coupling_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5470.PartToPartShearCouplingMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5470

            return self._parent._cast(
                _5470.PartToPartShearCouplingMultibodyDynamicsAnalysis
            )

        @property
        def planetary_gear_set_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5472.PlanetaryGearSetMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5472

            return self._parent._cast(_5472.PlanetaryGearSetMultibodyDynamicsAnalysis)

        @property
        def planet_carrier_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5473.PlanetCarrierMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5473

            return self._parent._cast(_5473.PlanetCarrierMultibodyDynamicsAnalysis)

        @property
        def point_load_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5474.PointLoadMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5474

            return self._parent._cast(_5474.PointLoadMultibodyDynamicsAnalysis)

        @property
        def power_load_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5475.PowerLoadMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5475

            return self._parent._cast(_5475.PowerLoadMultibodyDynamicsAnalysis)

        @property
        def pulley_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5476.PulleyMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5476

            return self._parent._cast(_5476.PulleyMultibodyDynamicsAnalysis)

        @property
        def ring_pins_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5477.RingPinsMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5477

            return self._parent._cast(_5477.RingPinsMultibodyDynamicsAnalysis)

        @property
        def rolling_ring_assembly_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5479.RollingRingAssemblyMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5479

            return self._parent._cast(
                _5479.RollingRingAssemblyMultibodyDynamicsAnalysis
            )

        @property
        def rolling_ring_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5481.RollingRingMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5481

            return self._parent._cast(_5481.RollingRingMultibodyDynamicsAnalysis)

        @property
        def root_assembly_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5482.RootAssemblyMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5482

            return self._parent._cast(_5482.RootAssemblyMultibodyDynamicsAnalysis)

        @property
        def shaft_hub_connection_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5485.ShaftHubConnectionMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5485

            return self._parent._cast(_5485.ShaftHubConnectionMultibodyDynamicsAnalysis)

        @property
        def shaft_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5486.ShaftMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5486

            return self._parent._cast(_5486.ShaftMultibodyDynamicsAnalysis)

        @property
        def specialised_assembly_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5489.SpecialisedAssemblyMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5489

            return self._parent._cast(
                _5489.SpecialisedAssemblyMultibodyDynamicsAnalysis
            )

        @property
        def spiral_bevel_gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5491.SpiralBevelGearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5491

            return self._parent._cast(_5491.SpiralBevelGearMultibodyDynamicsAnalysis)

        @property
        def spiral_bevel_gear_set_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5492.SpiralBevelGearSetMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5492

            return self._parent._cast(_5492.SpiralBevelGearSetMultibodyDynamicsAnalysis)

        @property
        def spring_damper_half_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5494.SpringDamperHalfMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5494

            return self._parent._cast(_5494.SpringDamperHalfMultibodyDynamicsAnalysis)

        @property
        def spring_damper_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5495.SpringDamperMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5495

            return self._parent._cast(_5495.SpringDamperMultibodyDynamicsAnalysis)

        @property
        def straight_bevel_diff_gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5497.StraightBevelDiffGearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5497

            return self._parent._cast(
                _5497.StraightBevelDiffGearMultibodyDynamicsAnalysis
            )

        @property
        def straight_bevel_diff_gear_set_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5498.StraightBevelDiffGearSetMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5498

            return self._parent._cast(
                _5498.StraightBevelDiffGearSetMultibodyDynamicsAnalysis
            )

        @property
        def straight_bevel_gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5500.StraightBevelGearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5500

            return self._parent._cast(_5500.StraightBevelGearMultibodyDynamicsAnalysis)

        @property
        def straight_bevel_gear_set_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5501.StraightBevelGearSetMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5501

            return self._parent._cast(
                _5501.StraightBevelGearSetMultibodyDynamicsAnalysis
            )

        @property
        def straight_bevel_planet_gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5502.StraightBevelPlanetGearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5502

            return self._parent._cast(
                _5502.StraightBevelPlanetGearMultibodyDynamicsAnalysis
            )

        @property
        def straight_bevel_sun_gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5503.StraightBevelSunGearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5503

            return self._parent._cast(
                _5503.StraightBevelSunGearMultibodyDynamicsAnalysis
            )

        @property
        def synchroniser_half_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5504.SynchroniserHalfMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5504

            return self._parent._cast(_5504.SynchroniserHalfMultibodyDynamicsAnalysis)

        @property
        def synchroniser_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5505.SynchroniserMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5505

            return self._parent._cast(_5505.SynchroniserMultibodyDynamicsAnalysis)

        @property
        def synchroniser_part_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5506.SynchroniserPartMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5506

            return self._parent._cast(_5506.SynchroniserPartMultibodyDynamicsAnalysis)

        @property
        def synchroniser_sleeve_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5507.SynchroniserSleeveMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5507

            return self._parent._cast(_5507.SynchroniserSleeveMultibodyDynamicsAnalysis)

        @property
        def torque_converter_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5510.TorqueConverterMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5510

            return self._parent._cast(_5510.TorqueConverterMultibodyDynamicsAnalysis)

        @property
        def torque_converter_pump_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5511.TorqueConverterPumpMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5511

            return self._parent._cast(
                _5511.TorqueConverterPumpMultibodyDynamicsAnalysis
            )

        @property
        def torque_converter_turbine_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5513.TorqueConverterTurbineMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5513

            return self._parent._cast(
                _5513.TorqueConverterTurbineMultibodyDynamicsAnalysis
            )

        @property
        def unbalanced_mass_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5514.UnbalancedMassMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5514

            return self._parent._cast(_5514.UnbalancedMassMultibodyDynamicsAnalysis)

        @property
        def virtual_component_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5515.VirtualComponentMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5515

            return self._parent._cast(_5515.VirtualComponentMultibodyDynamicsAnalysis)

        @property
        def worm_gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5518.WormGearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5518

            return self._parent._cast(_5518.WormGearMultibodyDynamicsAnalysis)

        @property
        def worm_gear_set_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5519.WormGearSetMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5519

            return self._parent._cast(_5519.WormGearSetMultibodyDynamicsAnalysis)

        @property
        def zerol_bevel_gear_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5521.ZerolBevelGearMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5521

            return self._parent._cast(_5521.ZerolBevelGearMultibodyDynamicsAnalysis)

        @property
        def zerol_bevel_gear_set_multibody_dynamics_analysis(
            self: "PartTimeSeriesLoadAnalysisCase._Cast_PartTimeSeriesLoadAnalysisCase",
        ) -> "_5522.ZerolBevelGearSetMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5522

            return self._parent._cast(_5522.ZerolBevelGearSetMultibodyDynamicsAnalysis)

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
