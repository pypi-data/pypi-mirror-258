"""PartAdvancedTimeSteppingAnalysisForModulation"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.analysis_cases import _7547
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_PART_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation",
    "PartAdvancedTimeSteppingAnalysisForModulation",
)

if TYPE_CHECKING:
    from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
        _7009,
        _7005,
        _7006,
        _7007,
        _7013,
        _7015,
        _7016,
        _7018,
        _7020,
        _7021,
        _7023,
        _7024,
        _7025,
        _7026,
        _7028,
        _7029,
        _7030,
        _7031,
        _7033,
        _7035,
        _7036,
        _7038,
        _7039,
        _7041,
        _7042,
        _7044,
        _7046,
        _7047,
        _7049,
        _7050,
        _7052,
        _7053,
        _7054,
        _7057,
        _7059,
        _7060,
        _7061,
        _7062,
        _7063,
        _7065,
        _7066,
        _7067,
        _7068,
        _7070,
        _7071,
        _7073,
        _7075,
        _7077,
        _7079,
        _7080,
        _7082,
        _7083,
        _7085,
        _7086,
        _7087,
        _7088,
        _7089,
        _7091,
        _7093,
        _7095,
        _7096,
        _7097,
        _7098,
        _7099,
        _7100,
        _7102,
        _7103,
        _7105,
        _7106,
        _7107,
        _7109,
        _7110,
        _7112,
        _7113,
        _7115,
        _7116,
        _7118,
        _7119,
        _7121,
        _7122,
        _7123,
        _7124,
        _7125,
        _7126,
        _7127,
        _7128,
        _7130,
        _7131,
        _7132,
        _7133,
        _7134,
        _7136,
        _7137,
        _7139,
    )
    from mastapy.system_model.part_model import _2468
    from mastapy.system_model.analyses_and_results.system_deflections import _2785
    from mastapy.system_model.analyses_and_results.analysis_cases import _7544
    from mastapy.system_model.analyses_and_results import _2657, _2653, _2651


__docformat__ = "restructuredtext en"
__all__ = ("PartAdvancedTimeSteppingAnalysisForModulation",)


Self = TypeVar("Self", bound="PartAdvancedTimeSteppingAnalysisForModulation")


class PartAdvancedTimeSteppingAnalysisForModulation(_7547.PartStaticLoadAnalysisCase):
    """PartAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    """

    TYPE = _PART_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_PartAdvancedTimeSteppingAnalysisForModulation"
    )

    class _Cast_PartAdvancedTimeSteppingAnalysisForModulation:
        """Special nested class for casting PartAdvancedTimeSteppingAnalysisForModulation to subclasses."""

        def __init__(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
            parent: "PartAdvancedTimeSteppingAnalysisForModulation",
        ):
            self._parent = parent

        @property
        def part_static_load_analysis_case(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7547.PartStaticLoadAnalysisCase":
            return self._parent._cast(_7547.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7544.PartAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7544

            return self._parent._cast(_7544.PartAnalysisCase)

        @property
        def part_analysis(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_2657.PartAnalysis":
            from mastapy.system_model.analyses_and_results import _2657

            return self._parent._cast(_2657.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_2653.DesignEntitySingleContextAnalysis":
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def abstract_assembly_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7005.AbstractAssemblyAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7005,
            )

            return self._parent._cast(
                _7005.AbstractAssemblyAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def abstract_shaft_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7006.AbstractShaftAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7006,
            )

            return self._parent._cast(
                _7006.AbstractShaftAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def abstract_shaft_or_housing_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7007.AbstractShaftOrHousingAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7007,
            )

            return self._parent._cast(
                _7007.AbstractShaftOrHousingAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def agma_gleason_conical_gear_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7013.AGMAGleasonConicalGearAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7013,
            )

            return self._parent._cast(
                _7013.AGMAGleasonConicalGearAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def agma_gleason_conical_gear_set_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7015.AGMAGleasonConicalGearSetAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7015,
            )

            return self._parent._cast(
                _7015.AGMAGleasonConicalGearSetAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def assembly_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7016.AssemblyAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7016,
            )

            return self._parent._cast(
                _7016.AssemblyAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def bearing_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7018.BearingAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7018,
            )

            return self._parent._cast(
                _7018.BearingAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def belt_drive_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7020.BeltDriveAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7020,
            )

            return self._parent._cast(
                _7020.BeltDriveAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def bevel_differential_gear_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7021.BevelDifferentialGearAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7021,
            )

            return self._parent._cast(
                _7021.BevelDifferentialGearAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def bevel_differential_gear_set_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7023.BevelDifferentialGearSetAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7023,
            )

            return self._parent._cast(
                _7023.BevelDifferentialGearSetAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def bevel_differential_planet_gear_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> (
            "_7024.BevelDifferentialPlanetGearAdvancedTimeSteppingAnalysisForModulation"
        ):
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7024,
            )

            return self._parent._cast(
                _7024.BevelDifferentialPlanetGearAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def bevel_differential_sun_gear_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7025.BevelDifferentialSunGearAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7025,
            )

            return self._parent._cast(
                _7025.BevelDifferentialSunGearAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def bevel_gear_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7026.BevelGearAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7026,
            )

            return self._parent._cast(
                _7026.BevelGearAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def bevel_gear_set_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7028.BevelGearSetAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7028,
            )

            return self._parent._cast(
                _7028.BevelGearSetAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def bolt_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7029.BoltAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7029,
            )

            return self._parent._cast(
                _7029.BoltAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def bolted_joint_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7030.BoltedJointAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7030,
            )

            return self._parent._cast(
                _7030.BoltedJointAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def clutch_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7031.ClutchAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7031,
            )

            return self._parent._cast(
                _7031.ClutchAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def clutch_half_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7033.ClutchHalfAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7033,
            )

            return self._parent._cast(
                _7033.ClutchHalfAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def component_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7035.ComponentAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7035,
            )

            return self._parent._cast(
                _7035.ComponentAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def concept_coupling_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7036.ConceptCouplingAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7036,
            )

            return self._parent._cast(
                _7036.ConceptCouplingAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def concept_coupling_half_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7038.ConceptCouplingHalfAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7038,
            )

            return self._parent._cast(
                _7038.ConceptCouplingHalfAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def concept_gear_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7039.ConceptGearAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7039,
            )

            return self._parent._cast(
                _7039.ConceptGearAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def concept_gear_set_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7041.ConceptGearSetAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7041,
            )

            return self._parent._cast(
                _7041.ConceptGearSetAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def conical_gear_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7042.ConicalGearAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7042,
            )

            return self._parent._cast(
                _7042.ConicalGearAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def conical_gear_set_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7044.ConicalGearSetAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7044,
            )

            return self._parent._cast(
                _7044.ConicalGearSetAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def connector_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7046.ConnectorAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7046,
            )

            return self._parent._cast(
                _7046.ConnectorAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def coupling_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7047.CouplingAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7047,
            )

            return self._parent._cast(
                _7047.CouplingAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def coupling_half_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7049.CouplingHalfAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7049,
            )

            return self._parent._cast(
                _7049.CouplingHalfAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def cvt_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7050.CVTAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7050,
            )

            return self._parent._cast(
                _7050.CVTAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def cvt_pulley_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7052.CVTPulleyAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7052,
            )

            return self._parent._cast(
                _7052.CVTPulleyAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def cycloidal_assembly_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7053.CycloidalAssemblyAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7053,
            )

            return self._parent._cast(
                _7053.CycloidalAssemblyAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def cycloidal_disc_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7054.CycloidalDiscAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7054,
            )

            return self._parent._cast(
                _7054.CycloidalDiscAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def cylindrical_gear_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7057.CylindricalGearAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7057,
            )

            return self._parent._cast(
                _7057.CylindricalGearAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def cylindrical_gear_set_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7059.CylindricalGearSetAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7059,
            )

            return self._parent._cast(
                _7059.CylindricalGearSetAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def cylindrical_planet_gear_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7060.CylindricalPlanetGearAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7060,
            )

            return self._parent._cast(
                _7060.CylindricalPlanetGearAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def datum_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7061.DatumAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7061,
            )

            return self._parent._cast(
                _7061.DatumAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def external_cad_model_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7062.ExternalCADModelAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7062,
            )

            return self._parent._cast(
                _7062.ExternalCADModelAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def face_gear_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7063.FaceGearAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7063,
            )

            return self._parent._cast(
                _7063.FaceGearAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def face_gear_set_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7065.FaceGearSetAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7065,
            )

            return self._parent._cast(
                _7065.FaceGearSetAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def fe_part_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7066.FEPartAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7066,
            )

            return self._parent._cast(
                _7066.FEPartAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def flexible_pin_assembly_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7067.FlexiblePinAssemblyAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7067,
            )

            return self._parent._cast(
                _7067.FlexiblePinAssemblyAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def gear_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7068.GearAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7068,
            )

            return self._parent._cast(
                _7068.GearAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def gear_set_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7070.GearSetAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7070,
            )

            return self._parent._cast(
                _7070.GearSetAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def guide_dxf_model_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7071.GuideDxfModelAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7071,
            )

            return self._parent._cast(
                _7071.GuideDxfModelAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def hypoid_gear_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7073.HypoidGearAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7073,
            )

            return self._parent._cast(
                _7073.HypoidGearAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def hypoid_gear_set_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7075.HypoidGearSetAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7075,
            )

            return self._parent._cast(
                _7075.HypoidGearSetAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def klingelnberg_cyclo_palloid_conical_gear_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7077.KlingelnbergCycloPalloidConicalGearAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7077,
            )

            return self._parent._cast(
                _7077.KlingelnbergCycloPalloidConicalGearAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def klingelnberg_cyclo_palloid_conical_gear_set_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7079.KlingelnbergCycloPalloidConicalGearSetAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7079,
            )

            return self._parent._cast(
                _7079.KlingelnbergCycloPalloidConicalGearSetAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7080.KlingelnbergCycloPalloidHypoidGearAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7080,
            )

            return self._parent._cast(
                _7080.KlingelnbergCycloPalloidHypoidGearAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_set_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7082.KlingelnbergCycloPalloidHypoidGearSetAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7082,
            )

            return self._parent._cast(
                _7082.KlingelnbergCycloPalloidHypoidGearSetAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7083.KlingelnbergCycloPalloidSpiralBevelGearAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7083,
            )

            return self._parent._cast(
                _7083.KlingelnbergCycloPalloidSpiralBevelGearAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7085.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7085,
            )

            return self._parent._cast(
                _7085.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def mass_disc_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7086.MassDiscAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7086,
            )

            return self._parent._cast(
                _7086.MassDiscAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def measurement_component_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7087.MeasurementComponentAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7087,
            )

            return self._parent._cast(
                _7087.MeasurementComponentAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def mountable_component_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7088.MountableComponentAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7088,
            )

            return self._parent._cast(
                _7088.MountableComponentAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def oil_seal_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7089.OilSealAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7089,
            )

            return self._parent._cast(
                _7089.OilSealAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def part_to_part_shear_coupling_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7091.PartToPartShearCouplingAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7091,
            )

            return self._parent._cast(
                _7091.PartToPartShearCouplingAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def part_to_part_shear_coupling_half_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> (
            "_7093.PartToPartShearCouplingHalfAdvancedTimeSteppingAnalysisForModulation"
        ):
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7093,
            )

            return self._parent._cast(
                _7093.PartToPartShearCouplingHalfAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def planetary_gear_set_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7095.PlanetaryGearSetAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7095,
            )

            return self._parent._cast(
                _7095.PlanetaryGearSetAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def planet_carrier_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7096.PlanetCarrierAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7096,
            )

            return self._parent._cast(
                _7096.PlanetCarrierAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def point_load_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7097.PointLoadAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7097,
            )

            return self._parent._cast(
                _7097.PointLoadAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def power_load_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7098.PowerLoadAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7098,
            )

            return self._parent._cast(
                _7098.PowerLoadAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def pulley_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7099.PulleyAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7099,
            )

            return self._parent._cast(
                _7099.PulleyAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def ring_pins_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7100.RingPinsAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7100,
            )

            return self._parent._cast(
                _7100.RingPinsAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def rolling_ring_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7102.RollingRingAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7102,
            )

            return self._parent._cast(
                _7102.RollingRingAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def rolling_ring_assembly_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7103.RollingRingAssemblyAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7103,
            )

            return self._parent._cast(
                _7103.RollingRingAssemblyAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def root_assembly_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7105.RootAssemblyAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7105,
            )

            return self._parent._cast(
                _7105.RootAssemblyAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def shaft_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7106.ShaftAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7106,
            )

            return self._parent._cast(
                _7106.ShaftAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def shaft_hub_connection_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7107.ShaftHubConnectionAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7107,
            )

            return self._parent._cast(
                _7107.ShaftHubConnectionAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def specialised_assembly_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7109.SpecialisedAssemblyAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7109,
            )

            return self._parent._cast(
                _7109.SpecialisedAssemblyAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def spiral_bevel_gear_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7110.SpiralBevelGearAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7110,
            )

            return self._parent._cast(
                _7110.SpiralBevelGearAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def spiral_bevel_gear_set_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7112.SpiralBevelGearSetAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7112,
            )

            return self._parent._cast(
                _7112.SpiralBevelGearSetAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def spring_damper_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7113.SpringDamperAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7113,
            )

            return self._parent._cast(
                _7113.SpringDamperAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def spring_damper_half_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7115.SpringDamperHalfAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7115,
            )

            return self._parent._cast(
                _7115.SpringDamperHalfAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def straight_bevel_diff_gear_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7116.StraightBevelDiffGearAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7116,
            )

            return self._parent._cast(
                _7116.StraightBevelDiffGearAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def straight_bevel_diff_gear_set_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7118.StraightBevelDiffGearSetAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7118,
            )

            return self._parent._cast(
                _7118.StraightBevelDiffGearSetAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def straight_bevel_gear_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7119.StraightBevelGearAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7119,
            )

            return self._parent._cast(
                _7119.StraightBevelGearAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def straight_bevel_gear_set_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7121.StraightBevelGearSetAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7121,
            )

            return self._parent._cast(
                _7121.StraightBevelGearSetAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def straight_bevel_planet_gear_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7122.StraightBevelPlanetGearAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7122,
            )

            return self._parent._cast(
                _7122.StraightBevelPlanetGearAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def straight_bevel_sun_gear_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7123.StraightBevelSunGearAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7123,
            )

            return self._parent._cast(
                _7123.StraightBevelSunGearAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def synchroniser_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7124.SynchroniserAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7124,
            )

            return self._parent._cast(
                _7124.SynchroniserAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def synchroniser_half_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7125.SynchroniserHalfAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7125,
            )

            return self._parent._cast(
                _7125.SynchroniserHalfAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def synchroniser_part_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7126.SynchroniserPartAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7126,
            )

            return self._parent._cast(
                _7126.SynchroniserPartAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def synchroniser_sleeve_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7127.SynchroniserSleeveAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7127,
            )

            return self._parent._cast(
                _7127.SynchroniserSleeveAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def torque_converter_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7128.TorqueConverterAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7128,
            )

            return self._parent._cast(
                _7128.TorqueConverterAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def torque_converter_pump_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7130.TorqueConverterPumpAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7130,
            )

            return self._parent._cast(
                _7130.TorqueConverterPumpAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def torque_converter_turbine_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7131.TorqueConverterTurbineAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7131,
            )

            return self._parent._cast(
                _7131.TorqueConverterTurbineAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def unbalanced_mass_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7132.UnbalancedMassAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7132,
            )

            return self._parent._cast(
                _7132.UnbalancedMassAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def virtual_component_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7133.VirtualComponentAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7133,
            )

            return self._parent._cast(
                _7133.VirtualComponentAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def worm_gear_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7134.WormGearAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7134,
            )

            return self._parent._cast(
                _7134.WormGearAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def worm_gear_set_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7136.WormGearSetAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7136,
            )

            return self._parent._cast(
                _7136.WormGearSetAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def zerol_bevel_gear_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7137.ZerolBevelGearAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7137,
            )

            return self._parent._cast(
                _7137.ZerolBevelGearAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def zerol_bevel_gear_set_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "_7139.ZerolBevelGearSetAdvancedTimeSteppingAnalysisForModulation":
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7139,
            )

            return self._parent._cast(
                _7139.ZerolBevelGearSetAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def part_advanced_time_stepping_analysis_for_modulation(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
        ) -> "PartAdvancedTimeSteppingAnalysisForModulation":
            return self._parent

        def __getattr__(
            self: "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation",
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
        instance_to_wrap: "PartAdvancedTimeSteppingAnalysisForModulation.TYPE",
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def advanced_time_stepping_analysis_for_modulation(
        self: Self,
    ) -> "_7009.AdvancedTimeSteppingAnalysisForModulation":
        """mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.AdvancedTimeSteppingAnalysisForModulation

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AdvancedTimeSteppingAnalysisForModulation

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_design(self: Self) -> "_2468.Part":
        """mastapy.system_model.part_model.Part

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def system_deflection_results(self: Self) -> "_2785.PartSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.PartSystemDeflection

        Note:
            This property is readonly.
        """
        temp = self.wrapped.SystemDeflectionResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "PartAdvancedTimeSteppingAnalysisForModulation._Cast_PartAdvancedTimeSteppingAnalysisForModulation":
        return self._Cast_PartAdvancedTimeSteppingAnalysisForModulation(self)
