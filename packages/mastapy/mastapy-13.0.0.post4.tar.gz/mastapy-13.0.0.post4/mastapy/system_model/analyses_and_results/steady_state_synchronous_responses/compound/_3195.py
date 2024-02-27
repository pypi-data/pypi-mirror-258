"""PartCompoundSteadyStateSynchronousResponse"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import conversion
from mastapy.system_model.analyses_and_results.analysis_cases import _7545
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_PART_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound",
    "PartCompoundSteadyStateSynchronousResponse",
)

if TYPE_CHECKING:
    from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3063,
    )
    from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
        _3116,
        _3117,
        _3118,
        _3120,
        _3122,
        _3123,
        _3124,
        _3126,
        _3127,
        _3129,
        _3130,
        _3131,
        _3132,
        _3134,
        _3135,
        _3136,
        _3137,
        _3139,
        _3141,
        _3142,
        _3144,
        _3145,
        _3147,
        _3148,
        _3150,
        _3152,
        _3153,
        _3155,
        _3157,
        _3158,
        _3159,
        _3161,
        _3163,
        _3165,
        _3166,
        _3167,
        _3168,
        _3169,
        _3171,
        _3172,
        _3173,
        _3174,
        _3176,
        _3177,
        _3178,
        _3180,
        _3182,
        _3184,
        _3185,
        _3187,
        _3188,
        _3190,
        _3191,
        _3192,
        _3193,
        _3194,
        _3196,
        _3198,
        _3200,
        _3201,
        _3202,
        _3203,
        _3204,
        _3205,
        _3207,
        _3208,
        _3210,
        _3211,
        _3212,
        _3214,
        _3215,
        _3217,
        _3218,
        _3220,
        _3221,
        _3223,
        _3224,
        _3226,
        _3227,
        _3228,
        _3229,
        _3230,
        _3231,
        _3232,
        _3233,
        _3235,
        _3236,
        _3237,
        _3238,
        _3239,
        _3241,
        _3242,
        _3244,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import _7542
    from mastapy.system_model.analyses_and_results import _2651


__docformat__ = "restructuredtext en"
__all__ = ("PartCompoundSteadyStateSynchronousResponse",)


Self = TypeVar("Self", bound="PartCompoundSteadyStateSynchronousResponse")


class PartCompoundSteadyStateSynchronousResponse(_7545.PartCompoundAnalysis):
    """PartCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE = _PART_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_PartCompoundSteadyStateSynchronousResponse"
    )

    class _Cast_PartCompoundSteadyStateSynchronousResponse:
        """Special nested class for casting PartCompoundSteadyStateSynchronousResponse to subclasses."""

        def __init__(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
            parent: "PartCompoundSteadyStateSynchronousResponse",
        ):
            self._parent = parent

        @property
        def part_compound_analysis(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_7545.PartCompoundAnalysis":
            return self._parent._cast(_7545.PartCompoundAnalysis)

        @property
        def design_entity_compound_analysis(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_7542.DesignEntityCompoundAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7542

            return self._parent._cast(_7542.DesignEntityCompoundAnalysis)

        @property
        def design_entity_analysis(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def abstract_assembly_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3116.AbstractAssemblyCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3116,
            )

            return self._parent._cast(
                _3116.AbstractAssemblyCompoundSteadyStateSynchronousResponse
            )

        @property
        def abstract_shaft_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3117.AbstractShaftCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3117,
            )

            return self._parent._cast(
                _3117.AbstractShaftCompoundSteadyStateSynchronousResponse
            )

        @property
        def abstract_shaft_or_housing_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3118.AbstractShaftOrHousingCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3118,
            )

            return self._parent._cast(
                _3118.AbstractShaftOrHousingCompoundSteadyStateSynchronousResponse
            )

        @property
        def agma_gleason_conical_gear_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3120.AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3120,
            )

            return self._parent._cast(
                _3120.AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponse
            )

        @property
        def agma_gleason_conical_gear_set_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3122.AGMAGleasonConicalGearSetCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3122,
            )

            return self._parent._cast(
                _3122.AGMAGleasonConicalGearSetCompoundSteadyStateSynchronousResponse
            )

        @property
        def assembly_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3123.AssemblyCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3123,
            )

            return self._parent._cast(
                _3123.AssemblyCompoundSteadyStateSynchronousResponse
            )

        @property
        def bearing_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3124.BearingCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3124,
            )

            return self._parent._cast(
                _3124.BearingCompoundSteadyStateSynchronousResponse
            )

        @property
        def belt_drive_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3126.BeltDriveCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3126,
            )

            return self._parent._cast(
                _3126.BeltDriveCompoundSteadyStateSynchronousResponse
            )

        @property
        def bevel_differential_gear_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3127.BevelDifferentialGearCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3127,
            )

            return self._parent._cast(
                _3127.BevelDifferentialGearCompoundSteadyStateSynchronousResponse
            )

        @property
        def bevel_differential_gear_set_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3129.BevelDifferentialGearSetCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3129,
            )

            return self._parent._cast(
                _3129.BevelDifferentialGearSetCompoundSteadyStateSynchronousResponse
            )

        @property
        def bevel_differential_planet_gear_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3130.BevelDifferentialPlanetGearCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3130,
            )

            return self._parent._cast(
                _3130.BevelDifferentialPlanetGearCompoundSteadyStateSynchronousResponse
            )

        @property
        def bevel_differential_sun_gear_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3131.BevelDifferentialSunGearCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3131,
            )

            return self._parent._cast(
                _3131.BevelDifferentialSunGearCompoundSteadyStateSynchronousResponse
            )

        @property
        def bevel_gear_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3132.BevelGearCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3132,
            )

            return self._parent._cast(
                _3132.BevelGearCompoundSteadyStateSynchronousResponse
            )

        @property
        def bevel_gear_set_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3134.BevelGearSetCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3134,
            )

            return self._parent._cast(
                _3134.BevelGearSetCompoundSteadyStateSynchronousResponse
            )

        @property
        def bolt_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3135.BoltCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3135,
            )

            return self._parent._cast(_3135.BoltCompoundSteadyStateSynchronousResponse)

        @property
        def bolted_joint_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3136.BoltedJointCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3136,
            )

            return self._parent._cast(
                _3136.BoltedJointCompoundSteadyStateSynchronousResponse
            )

        @property
        def clutch_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3137.ClutchCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3137,
            )

            return self._parent._cast(
                _3137.ClutchCompoundSteadyStateSynchronousResponse
            )

        @property
        def clutch_half_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3139.ClutchHalfCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3139,
            )

            return self._parent._cast(
                _3139.ClutchHalfCompoundSteadyStateSynchronousResponse
            )

        @property
        def component_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3141.ComponentCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3141,
            )

            return self._parent._cast(
                _3141.ComponentCompoundSteadyStateSynchronousResponse
            )

        @property
        def concept_coupling_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3142.ConceptCouplingCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3142,
            )

            return self._parent._cast(
                _3142.ConceptCouplingCompoundSteadyStateSynchronousResponse
            )

        @property
        def concept_coupling_half_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3144.ConceptCouplingHalfCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3144,
            )

            return self._parent._cast(
                _3144.ConceptCouplingHalfCompoundSteadyStateSynchronousResponse
            )

        @property
        def concept_gear_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3145.ConceptGearCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3145,
            )

            return self._parent._cast(
                _3145.ConceptGearCompoundSteadyStateSynchronousResponse
            )

        @property
        def concept_gear_set_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3147.ConceptGearSetCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3147,
            )

            return self._parent._cast(
                _3147.ConceptGearSetCompoundSteadyStateSynchronousResponse
            )

        @property
        def conical_gear_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3148.ConicalGearCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3148,
            )

            return self._parent._cast(
                _3148.ConicalGearCompoundSteadyStateSynchronousResponse
            )

        @property
        def conical_gear_set_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3150.ConicalGearSetCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3150,
            )

            return self._parent._cast(
                _3150.ConicalGearSetCompoundSteadyStateSynchronousResponse
            )

        @property
        def connector_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3152.ConnectorCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3152,
            )

            return self._parent._cast(
                _3152.ConnectorCompoundSteadyStateSynchronousResponse
            )

        @property
        def coupling_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3153.CouplingCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3153,
            )

            return self._parent._cast(
                _3153.CouplingCompoundSteadyStateSynchronousResponse
            )

        @property
        def coupling_half_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3155.CouplingHalfCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3155,
            )

            return self._parent._cast(
                _3155.CouplingHalfCompoundSteadyStateSynchronousResponse
            )

        @property
        def cvt_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3157.CVTCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3157,
            )

            return self._parent._cast(_3157.CVTCompoundSteadyStateSynchronousResponse)

        @property
        def cvt_pulley_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3158.CVTPulleyCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3158,
            )

            return self._parent._cast(
                _3158.CVTPulleyCompoundSteadyStateSynchronousResponse
            )

        @property
        def cycloidal_assembly_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3159.CycloidalAssemblyCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3159,
            )

            return self._parent._cast(
                _3159.CycloidalAssemblyCompoundSteadyStateSynchronousResponse
            )

        @property
        def cycloidal_disc_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3161.CycloidalDiscCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3161,
            )

            return self._parent._cast(
                _3161.CycloidalDiscCompoundSteadyStateSynchronousResponse
            )

        @property
        def cylindrical_gear_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3163.CylindricalGearCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3163,
            )

            return self._parent._cast(
                _3163.CylindricalGearCompoundSteadyStateSynchronousResponse
            )

        @property
        def cylindrical_gear_set_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3165.CylindricalGearSetCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3165,
            )

            return self._parent._cast(
                _3165.CylindricalGearSetCompoundSteadyStateSynchronousResponse
            )

        @property
        def cylindrical_planet_gear_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3166.CylindricalPlanetGearCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3166,
            )

            return self._parent._cast(
                _3166.CylindricalPlanetGearCompoundSteadyStateSynchronousResponse
            )

        @property
        def datum_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3167.DatumCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3167,
            )

            return self._parent._cast(_3167.DatumCompoundSteadyStateSynchronousResponse)

        @property
        def external_cad_model_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3168.ExternalCADModelCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3168,
            )

            return self._parent._cast(
                _3168.ExternalCADModelCompoundSteadyStateSynchronousResponse
            )

        @property
        def face_gear_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3169.FaceGearCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3169,
            )

            return self._parent._cast(
                _3169.FaceGearCompoundSteadyStateSynchronousResponse
            )

        @property
        def face_gear_set_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3171.FaceGearSetCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3171,
            )

            return self._parent._cast(
                _3171.FaceGearSetCompoundSteadyStateSynchronousResponse
            )

        @property
        def fe_part_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3172.FEPartCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3172,
            )

            return self._parent._cast(
                _3172.FEPartCompoundSteadyStateSynchronousResponse
            )

        @property
        def flexible_pin_assembly_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3173.FlexiblePinAssemblyCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3173,
            )

            return self._parent._cast(
                _3173.FlexiblePinAssemblyCompoundSteadyStateSynchronousResponse
            )

        @property
        def gear_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3174.GearCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3174,
            )

            return self._parent._cast(_3174.GearCompoundSteadyStateSynchronousResponse)

        @property
        def gear_set_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3176.GearSetCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3176,
            )

            return self._parent._cast(
                _3176.GearSetCompoundSteadyStateSynchronousResponse
            )

        @property
        def guide_dxf_model_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3177.GuideDxfModelCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3177,
            )

            return self._parent._cast(
                _3177.GuideDxfModelCompoundSteadyStateSynchronousResponse
            )

        @property
        def hypoid_gear_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3178.HypoidGearCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3178,
            )

            return self._parent._cast(
                _3178.HypoidGearCompoundSteadyStateSynchronousResponse
            )

        @property
        def hypoid_gear_set_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3180.HypoidGearSetCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3180,
            )

            return self._parent._cast(
                _3180.HypoidGearSetCompoundSteadyStateSynchronousResponse
            )

        @property
        def klingelnberg_cyclo_palloid_conical_gear_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3182.KlingelnbergCycloPalloidConicalGearCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3182,
            )

            return self._parent._cast(
                _3182.KlingelnbergCycloPalloidConicalGearCompoundSteadyStateSynchronousResponse
            )

        @property
        def klingelnberg_cyclo_palloid_conical_gear_set_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3184.KlingelnbergCycloPalloidConicalGearSetCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3184,
            )

            return self._parent._cast(
                _3184.KlingelnbergCycloPalloidConicalGearSetCompoundSteadyStateSynchronousResponse
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3185.KlingelnbergCycloPalloidHypoidGearCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3185,
            )

            return self._parent._cast(
                _3185.KlingelnbergCycloPalloidHypoidGearCompoundSteadyStateSynchronousResponse
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3187.KlingelnbergCycloPalloidHypoidGearSetCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3187,
            )

            return self._parent._cast(
                _3187.KlingelnbergCycloPalloidHypoidGearSetCompoundSteadyStateSynchronousResponse
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3188.KlingelnbergCycloPalloidSpiralBevelGearCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3188,
            )

            return self._parent._cast(
                _3188.KlingelnbergCycloPalloidSpiralBevelGearCompoundSteadyStateSynchronousResponse
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3190.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3190,
            )

            return self._parent._cast(
                _3190.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponse
            )

        @property
        def mass_disc_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3191.MassDiscCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3191,
            )

            return self._parent._cast(
                _3191.MassDiscCompoundSteadyStateSynchronousResponse
            )

        @property
        def measurement_component_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3192.MeasurementComponentCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3192,
            )

            return self._parent._cast(
                _3192.MeasurementComponentCompoundSteadyStateSynchronousResponse
            )

        @property
        def mountable_component_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3193.MountableComponentCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3193,
            )

            return self._parent._cast(
                _3193.MountableComponentCompoundSteadyStateSynchronousResponse
            )

        @property
        def oil_seal_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3194.OilSealCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3194,
            )

            return self._parent._cast(
                _3194.OilSealCompoundSteadyStateSynchronousResponse
            )

        @property
        def part_to_part_shear_coupling_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3196.PartToPartShearCouplingCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3196,
            )

            return self._parent._cast(
                _3196.PartToPartShearCouplingCompoundSteadyStateSynchronousResponse
            )

        @property
        def part_to_part_shear_coupling_half_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3198.PartToPartShearCouplingHalfCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3198,
            )

            return self._parent._cast(
                _3198.PartToPartShearCouplingHalfCompoundSteadyStateSynchronousResponse
            )

        @property
        def planetary_gear_set_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3200.PlanetaryGearSetCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3200,
            )

            return self._parent._cast(
                _3200.PlanetaryGearSetCompoundSteadyStateSynchronousResponse
            )

        @property
        def planet_carrier_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3201.PlanetCarrierCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3201,
            )

            return self._parent._cast(
                _3201.PlanetCarrierCompoundSteadyStateSynchronousResponse
            )

        @property
        def point_load_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3202.PointLoadCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3202,
            )

            return self._parent._cast(
                _3202.PointLoadCompoundSteadyStateSynchronousResponse
            )

        @property
        def power_load_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3203.PowerLoadCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3203,
            )

            return self._parent._cast(
                _3203.PowerLoadCompoundSteadyStateSynchronousResponse
            )

        @property
        def pulley_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3204.PulleyCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3204,
            )

            return self._parent._cast(
                _3204.PulleyCompoundSteadyStateSynchronousResponse
            )

        @property
        def ring_pins_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3205.RingPinsCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3205,
            )

            return self._parent._cast(
                _3205.RingPinsCompoundSteadyStateSynchronousResponse
            )

        @property
        def rolling_ring_assembly_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3207.RollingRingAssemblyCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3207,
            )

            return self._parent._cast(
                _3207.RollingRingAssemblyCompoundSteadyStateSynchronousResponse
            )

        @property
        def rolling_ring_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3208.RollingRingCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3208,
            )

            return self._parent._cast(
                _3208.RollingRingCompoundSteadyStateSynchronousResponse
            )

        @property
        def root_assembly_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3210.RootAssemblyCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3210,
            )

            return self._parent._cast(
                _3210.RootAssemblyCompoundSteadyStateSynchronousResponse
            )

        @property
        def shaft_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3211.ShaftCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3211,
            )

            return self._parent._cast(_3211.ShaftCompoundSteadyStateSynchronousResponse)

        @property
        def shaft_hub_connection_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3212.ShaftHubConnectionCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3212,
            )

            return self._parent._cast(
                _3212.ShaftHubConnectionCompoundSteadyStateSynchronousResponse
            )

        @property
        def specialised_assembly_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3214.SpecialisedAssemblyCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3214,
            )

            return self._parent._cast(
                _3214.SpecialisedAssemblyCompoundSteadyStateSynchronousResponse
            )

        @property
        def spiral_bevel_gear_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3215.SpiralBevelGearCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3215,
            )

            return self._parent._cast(
                _3215.SpiralBevelGearCompoundSteadyStateSynchronousResponse
            )

        @property
        def spiral_bevel_gear_set_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3217.SpiralBevelGearSetCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3217,
            )

            return self._parent._cast(
                _3217.SpiralBevelGearSetCompoundSteadyStateSynchronousResponse
            )

        @property
        def spring_damper_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3218.SpringDamperCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3218,
            )

            return self._parent._cast(
                _3218.SpringDamperCompoundSteadyStateSynchronousResponse
            )

        @property
        def spring_damper_half_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3220.SpringDamperHalfCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3220,
            )

            return self._parent._cast(
                _3220.SpringDamperHalfCompoundSteadyStateSynchronousResponse
            )

        @property
        def straight_bevel_diff_gear_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3221.StraightBevelDiffGearCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3221,
            )

            return self._parent._cast(
                _3221.StraightBevelDiffGearCompoundSteadyStateSynchronousResponse
            )

        @property
        def straight_bevel_diff_gear_set_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3223.StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3223,
            )

            return self._parent._cast(
                _3223.StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponse
            )

        @property
        def straight_bevel_gear_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3224.StraightBevelGearCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3224,
            )

            return self._parent._cast(
                _3224.StraightBevelGearCompoundSteadyStateSynchronousResponse
            )

        @property
        def straight_bevel_gear_set_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3226.StraightBevelGearSetCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3226,
            )

            return self._parent._cast(
                _3226.StraightBevelGearSetCompoundSteadyStateSynchronousResponse
            )

        @property
        def straight_bevel_planet_gear_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3227.StraightBevelPlanetGearCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3227,
            )

            return self._parent._cast(
                _3227.StraightBevelPlanetGearCompoundSteadyStateSynchronousResponse
            )

        @property
        def straight_bevel_sun_gear_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3228.StraightBevelSunGearCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3228,
            )

            return self._parent._cast(
                _3228.StraightBevelSunGearCompoundSteadyStateSynchronousResponse
            )

        @property
        def synchroniser_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3229.SynchroniserCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3229,
            )

            return self._parent._cast(
                _3229.SynchroniserCompoundSteadyStateSynchronousResponse
            )

        @property
        def synchroniser_half_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3230.SynchroniserHalfCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3230,
            )

            return self._parent._cast(
                _3230.SynchroniserHalfCompoundSteadyStateSynchronousResponse
            )

        @property
        def synchroniser_part_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3231.SynchroniserPartCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3231,
            )

            return self._parent._cast(
                _3231.SynchroniserPartCompoundSteadyStateSynchronousResponse
            )

        @property
        def synchroniser_sleeve_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3232.SynchroniserSleeveCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3232,
            )

            return self._parent._cast(
                _3232.SynchroniserSleeveCompoundSteadyStateSynchronousResponse
            )

        @property
        def torque_converter_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3233.TorqueConverterCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3233,
            )

            return self._parent._cast(
                _3233.TorqueConverterCompoundSteadyStateSynchronousResponse
            )

        @property
        def torque_converter_pump_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3235.TorqueConverterPumpCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3235,
            )

            return self._parent._cast(
                _3235.TorqueConverterPumpCompoundSteadyStateSynchronousResponse
            )

        @property
        def torque_converter_turbine_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3236.TorqueConverterTurbineCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3236,
            )

            return self._parent._cast(
                _3236.TorqueConverterTurbineCompoundSteadyStateSynchronousResponse
            )

        @property
        def unbalanced_mass_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3237.UnbalancedMassCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3237,
            )

            return self._parent._cast(
                _3237.UnbalancedMassCompoundSteadyStateSynchronousResponse
            )

        @property
        def virtual_component_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3238.VirtualComponentCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3238,
            )

            return self._parent._cast(
                _3238.VirtualComponentCompoundSteadyStateSynchronousResponse
            )

        @property
        def worm_gear_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3239.WormGearCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3239,
            )

            return self._parent._cast(
                _3239.WormGearCompoundSteadyStateSynchronousResponse
            )

        @property
        def worm_gear_set_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3241.WormGearSetCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3241,
            )

            return self._parent._cast(
                _3241.WormGearSetCompoundSteadyStateSynchronousResponse
            )

        @property
        def zerol_bevel_gear_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3242.ZerolBevelGearCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3242,
            )

            return self._parent._cast(
                _3242.ZerolBevelGearCompoundSteadyStateSynchronousResponse
            )

        @property
        def zerol_bevel_gear_set_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "_3244.ZerolBevelGearSetCompoundSteadyStateSynchronousResponse":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
                _3244,
            )

            return self._parent._cast(
                _3244.ZerolBevelGearSetCompoundSteadyStateSynchronousResponse
            )

        @property
        def part_compound_steady_state_synchronous_response(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
        ) -> "PartCompoundSteadyStateSynchronousResponse":
            return self._parent

        def __getattr__(
            self: "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse",
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
        self: Self, instance_to_wrap: "PartCompoundSteadyStateSynchronousResponse.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases(
        self: Self,
    ) -> "List[_3063.PartSteadyStateSynchronousResponse]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.PartSteadyStateSynchronousResponse]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def component_analysis_cases_ready(
        self: Self,
    ) -> "List[_3063.PartSteadyStateSynchronousResponse]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.PartSteadyStateSynchronousResponse]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: Self,
    ) -> "PartCompoundSteadyStateSynchronousResponse._Cast_PartCompoundSteadyStateSynchronousResponse":
        return self._Cast_PartCompoundSteadyStateSynchronousResponse(self)
