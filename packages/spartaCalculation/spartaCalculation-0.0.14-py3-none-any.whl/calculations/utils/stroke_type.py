from glom import glom

from calculations.types.enums.stroke_types import (
    STROKE_TYPES,
    STROKE_TYPES_FOR_150IM,
    STROKE_TYPES_FOR_200_400IM,
    STROKE_TYPES_FOR_MIXED_RELAY,
)
from calculations.types.services.calculations.lane import LaneInformation


def determine_stroke_type(index: int, lane_info: LaneInformation) -> str:
    stroke_type = glom(lane_info, "stroke_type")
    distance = glom(lane_info, "lap_distance")
    relay_type = glom(lane_info, "relay_type", default="").lower()

    if "medley" in relay_type:
        return STROKE_TYPES_FOR_MIXED_RELAY[index]

    if stroke_type not in STROKE_TYPES.MEDLEY.value:
        return stroke_type

    if distance == 150:
        return STROKE_TYPES_FOR_150IM[index]

    if distance == 200:
        return STROKE_TYPES_FOR_200_400IM[index]

    if distance == 400:
        refined_index = int(index / 2)

        return STROKE_TYPES_FOR_200_400IM[refined_index]
    
    return stroke_type
