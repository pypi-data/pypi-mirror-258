"""PartCompoundHarmonicAnalysisOfSingleExcitation"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import conversion
from mastapy.system_model.analyses_and_results.analysis_cases import _7545
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_PART_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation.Compound",
    "PartCompoundHarmonicAnalysisOfSingleExcitation",
)

if TYPE_CHECKING:
    from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
        _6088,
    )


__docformat__ = "restructuredtext en"
__all__ = ("PartCompoundHarmonicAnalysisOfSingleExcitation",)


Self = TypeVar("Self", bound="PartCompoundHarmonicAnalysisOfSingleExcitation")


class PartCompoundHarmonicAnalysisOfSingleExcitation(_7545.PartCompoundAnalysis):
    """PartCompoundHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    """

    TYPE = _PART_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_PartCompoundHarmonicAnalysisOfSingleExcitation"
    )

    class _Cast_PartCompoundHarmonicAnalysisOfSingleExcitation:
        """Special nested class for casting PartCompoundHarmonicAnalysisOfSingleExcitation to subclasses."""

        def __init__(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
            parent: "PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            self._parent = parent

        @property
        def part_compound_analysis(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            return self._parent._cast(_7545.PartCompoundAnalysis)

        @property
        def design_entity_compound_analysis(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7542

            return self._parent._cast(_7542.DesignEntityCompoundAnalysis)

        @property
        def design_entity_analysis(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def abstract_assembly_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6138,
            )

            return self._parent._cast(
                _6138.AbstractAssemblyCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def abstract_shaft_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6139,
            )

            return self._parent._cast(
                _6139.AbstractShaftCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def abstract_shaft_or_housing_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6140,
            )

            return self._parent._cast(
                _6140.AbstractShaftOrHousingCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def agma_gleason_conical_gear_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6142,
            )

            return self._parent._cast(
                _6142.AGMAGleasonConicalGearCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def agma_gleason_conical_gear_set_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6144,
            )

            return self._parent._cast(
                _6144.AGMAGleasonConicalGearSetCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def assembly_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6145,
            )

            return self._parent._cast(
                _6145.AssemblyCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def bearing_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6146,
            )

            return self._parent._cast(
                _6146.BearingCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def belt_drive_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6148,
            )

            return self._parent._cast(
                _6148.BeltDriveCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def bevel_differential_gear_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6149,
            )

            return self._parent._cast(
                _6149.BevelDifferentialGearCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def bevel_differential_gear_set_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6151,
            )

            return self._parent._cast(
                _6151.BevelDifferentialGearSetCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def bevel_differential_planet_gear_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6152,
            )

            return self._parent._cast(
                _6152.BevelDifferentialPlanetGearCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def bevel_differential_sun_gear_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6153,
            )

            return self._parent._cast(
                _6153.BevelDifferentialSunGearCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def bevel_gear_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6154,
            )

            return self._parent._cast(
                _6154.BevelGearCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def bevel_gear_set_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6156,
            )

            return self._parent._cast(
                _6156.BevelGearSetCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def bolt_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6157,
            )

            return self._parent._cast(
                _6157.BoltCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def bolted_joint_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6158,
            )

            return self._parent._cast(
                _6158.BoltedJointCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def clutch_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6159,
            )

            return self._parent._cast(
                _6159.ClutchCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def clutch_half_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6161,
            )

            return self._parent._cast(
                _6161.ClutchHalfCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def component_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6163,
            )

            return self._parent._cast(
                _6163.ComponentCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def concept_coupling_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6164,
            )

            return self._parent._cast(
                _6164.ConceptCouplingCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def concept_coupling_half_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6166,
            )

            return self._parent._cast(
                _6166.ConceptCouplingHalfCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def concept_gear_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6167,
            )

            return self._parent._cast(
                _6167.ConceptGearCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def concept_gear_set_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6169,
            )

            return self._parent._cast(
                _6169.ConceptGearSetCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def conical_gear_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6170,
            )

            return self._parent._cast(
                _6170.ConicalGearCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def conical_gear_set_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6172,
            )

            return self._parent._cast(
                _6172.ConicalGearSetCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def connector_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6174,
            )

            return self._parent._cast(
                _6174.ConnectorCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def coupling_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6175,
            )

            return self._parent._cast(
                _6175.CouplingCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def coupling_half_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6177,
            )

            return self._parent._cast(
                _6177.CouplingHalfCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def cvt_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6179,
            )

            return self._parent._cast(
                _6179.CVTCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def cvt_pulley_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6180,
            )

            return self._parent._cast(
                _6180.CVTPulleyCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def cycloidal_assembly_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6181,
            )

            return self._parent._cast(
                _6181.CycloidalAssemblyCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def cycloidal_disc_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6183,
            )

            return self._parent._cast(
                _6183.CycloidalDiscCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def cylindrical_gear_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6185,
            )

            return self._parent._cast(
                _6185.CylindricalGearCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def cylindrical_gear_set_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6187,
            )

            return self._parent._cast(
                _6187.CylindricalGearSetCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def cylindrical_planet_gear_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6188,
            )

            return self._parent._cast(
                _6188.CylindricalPlanetGearCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def datum_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6189,
            )

            return self._parent._cast(
                _6189.DatumCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def external_cad_model_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6190,
            )

            return self._parent._cast(
                _6190.ExternalCADModelCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def face_gear_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6191,
            )

            return self._parent._cast(
                _6191.FaceGearCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def face_gear_set_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6193,
            )

            return self._parent._cast(
                _6193.FaceGearSetCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def fe_part_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6194,
            )

            return self._parent._cast(
                _6194.FEPartCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def flexible_pin_assembly_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6195,
            )

            return self._parent._cast(
                _6195.FlexiblePinAssemblyCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def gear_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6196,
            )

            return self._parent._cast(
                _6196.GearCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def gear_set_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6198,
            )

            return self._parent._cast(
                _6198.GearSetCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def guide_dxf_model_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6199,
            )

            return self._parent._cast(
                _6199.GuideDxfModelCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def hypoid_gear_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6200,
            )

            return self._parent._cast(
                _6200.HypoidGearCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def hypoid_gear_set_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6202,
            )

            return self._parent._cast(
                _6202.HypoidGearSetCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def klingelnberg_cyclo_palloid_conical_gear_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6204,
            )

            return self._parent._cast(
                _6204.KlingelnbergCycloPalloidConicalGearCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def klingelnberg_cyclo_palloid_conical_gear_set_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6206,
            )

            return self._parent._cast(
                _6206.KlingelnbergCycloPalloidConicalGearSetCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6207,
            )

            return self._parent._cast(
                _6207.KlingelnbergCycloPalloidHypoidGearCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6209,
            )

            return self._parent._cast(
                _6209.KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6210,
            )

            return self._parent._cast(
                _6210.KlingelnbergCycloPalloidSpiralBevelGearCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6212,
            )

            return self._parent._cast(
                _6212.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def mass_disc_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6213,
            )

            return self._parent._cast(
                _6213.MassDiscCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def measurement_component_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6214,
            )

            return self._parent._cast(
                _6214.MeasurementComponentCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def mountable_component_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6215,
            )

            return self._parent._cast(
                _6215.MountableComponentCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def oil_seal_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6216,
            )

            return self._parent._cast(
                _6216.OilSealCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def part_to_part_shear_coupling_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6218,
            )

            return self._parent._cast(
                _6218.PartToPartShearCouplingCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def part_to_part_shear_coupling_half_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6220,
            )

            return self._parent._cast(
                _6220.PartToPartShearCouplingHalfCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def planetary_gear_set_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6222,
            )

            return self._parent._cast(
                _6222.PlanetaryGearSetCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def planet_carrier_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6223,
            )

            return self._parent._cast(
                _6223.PlanetCarrierCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def point_load_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6224,
            )

            return self._parent._cast(
                _6224.PointLoadCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def power_load_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6225,
            )

            return self._parent._cast(
                _6225.PowerLoadCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def pulley_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6226,
            )

            return self._parent._cast(
                _6226.PulleyCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def ring_pins_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6227,
            )

            return self._parent._cast(
                _6227.RingPinsCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def rolling_ring_assembly_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6229,
            )

            return self._parent._cast(
                _6229.RollingRingAssemblyCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def rolling_ring_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6230,
            )

            return self._parent._cast(
                _6230.RollingRingCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def root_assembly_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6232,
            )

            return self._parent._cast(
                _6232.RootAssemblyCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def shaft_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6233,
            )

            return self._parent._cast(
                _6233.ShaftCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def shaft_hub_connection_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6234,
            )

            return self._parent._cast(
                _6234.ShaftHubConnectionCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def specialised_assembly_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6236,
            )

            return self._parent._cast(
                _6236.SpecialisedAssemblyCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def spiral_bevel_gear_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6237,
            )

            return self._parent._cast(
                _6237.SpiralBevelGearCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def spiral_bevel_gear_set_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6239,
            )

            return self._parent._cast(
                _6239.SpiralBevelGearSetCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def spring_damper_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6240,
            )

            return self._parent._cast(
                _6240.SpringDamperCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def spring_damper_half_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6242,
            )

            return self._parent._cast(
                _6242.SpringDamperHalfCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def straight_bevel_diff_gear_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6243,
            )

            return self._parent._cast(
                _6243.StraightBevelDiffGearCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def straight_bevel_diff_gear_set_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6245,
            )

            return self._parent._cast(
                _6245.StraightBevelDiffGearSetCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def straight_bevel_gear_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6246,
            )

            return self._parent._cast(
                _6246.StraightBevelGearCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def straight_bevel_gear_set_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6248,
            )

            return self._parent._cast(
                _6248.StraightBevelGearSetCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def straight_bevel_planet_gear_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6249,
            )

            return self._parent._cast(
                _6249.StraightBevelPlanetGearCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def straight_bevel_sun_gear_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6250,
            )

            return self._parent._cast(
                _6250.StraightBevelSunGearCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def synchroniser_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6251,
            )

            return self._parent._cast(
                _6251.SynchroniserCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def synchroniser_half_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6252,
            )

            return self._parent._cast(
                _6252.SynchroniserHalfCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def synchroniser_part_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6253,
            )

            return self._parent._cast(
                _6253.SynchroniserPartCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def synchroniser_sleeve_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6254,
            )

            return self._parent._cast(
                _6254.SynchroniserSleeveCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def torque_converter_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6255,
            )

            return self._parent._cast(
                _6255.TorqueConverterCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def torque_converter_pump_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6257,
            )

            return self._parent._cast(
                _6257.TorqueConverterPumpCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def torque_converter_turbine_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6258,
            )

            return self._parent._cast(
                _6258.TorqueConverterTurbineCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def unbalanced_mass_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6259,
            )

            return self._parent._cast(
                _6259.UnbalancedMassCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def virtual_component_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6260,
            )

            return self._parent._cast(
                _6260.VirtualComponentCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def worm_gear_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6261,
            )

            return self._parent._cast(
                _6261.WormGearCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def worm_gear_set_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6263,
            )

            return self._parent._cast(
                _6263.WormGearSetCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def zerol_bevel_gear_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6264,
            )

            return self._parent._cast(
                _6264.ZerolBevelGearCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def zerol_bevel_gear_set_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
                _6266,
            )

            return self._parent._cast(
                _6266.ZerolBevelGearSetCompoundHarmonicAnalysisOfSingleExcitation
            )

        @property
        def part_compound_harmonic_analysis_of_single_excitation(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
        ) -> "PartCompoundHarmonicAnalysisOfSingleExcitation":
            return self._parent

        def __getattr__(
            self: "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
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
        instance_to_wrap: "PartCompoundHarmonicAnalysisOfSingleExcitation.TYPE",
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases(
        self: Self,
    ) -> "List[_6088.PartHarmonicAnalysisOfSingleExcitation]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.PartHarmonicAnalysisOfSingleExcitation]

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
    ) -> "List[_6088.PartHarmonicAnalysisOfSingleExcitation]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.PartHarmonicAnalysisOfSingleExcitation]

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
    ) -> "PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation":
        return self._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation(self)
