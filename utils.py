from dataclasses import dataclass
from math import ceil
from decimal import Decimal, ROUND_HALF_UP

@dataclass
class RoomDimensions:
    length1: float
    length2: float
    width1: float
    width2: float

@dataclass
class CeilingCalculation:
    parameters_full: int
    parameters_extra: float
    main_rods: int
    cross_rods: int
    connecting_clips: int
    screws: int
    total_parameter_length: float
    main_rods_length: float
    cross_rods_length: float

def calculate_rod_length_with_overlap(length: float, standard_length: float = 12.0, overlap: float = 4/12) -> tuple[int, float]:
    """Calculate number of rods needed and extra length including overlaps"""
    if length <= standard_length:
        return 1, length
    
    # Calculate full rods needed
    full_rods = ceil(length / standard_length)
    # Calculate total length including overlaps
    total_length = length + ((full_rods - 1) * overlap)
    
    return full_rods, total_length

def calculate_parameters(dimensions: RoomDimensions) -> tuple[int, float]:
    """Calculate parameters needed for the perimeter"""
    STANDARD_LENGTH = 12  # feet
    OVERLAP = 4/12  # 4 inches in feet
    
    total_perimeter = dimensions.length1 + dimensions.length2 + dimensions.width1 + dimensions.width2
    full_rods, total_length = calculate_rod_length_with_overlap(total_perimeter)
    
    extra_length = total_length % STANDARD_LENGTH
    if extra_length > 0:
        extra_length = round(extra_length, 2)
    
    return full_rods, extra_length

def calculate_main_rods(length: float) -> tuple[int, float]:
    """Calculate main rods with 4ft spacing and 2ft from walls"""
    FIRST_ROD_DISTANCE = 2  # feet from wall
    ROD_SPACING = 4  # feet between rods
    STANDARD_LENGTH = 12  # feet
    
    usable_length = length - (2 * FIRST_ROD_DISTANCE)
    num_rods = ceil(usable_length / ROD_SPACING) + 1
    
    # Calculate total length needed including overlaps
    total_rods, total_length = calculate_rod_length_with_overlap(length)
    
    return num_rods, total_length

def calculate_cross_rods(width: float) -> tuple[int, float]:
    """Calculate cross rods with 2ft spacing and 2ft from walls"""
    FIRST_ROD_DISTANCE = 2  # feet from wall
    ROD_SPACING = 2  # feet between centers
    STANDARD_LENGTH = 12  # feet
    
    usable_width = width - (2 * FIRST_ROD_DISTANCE)
    num_rods = ceil(usable_width / ROD_SPACING) + 1
    
    # Calculate total length needed including overlaps
    total_rods, total_length = calculate_rod_length_with_overlap(width)
    
    return num_rods, total_length

def calculate_ceiling_requirements(dimensions: RoomDimensions) -> CeilingCalculation:
    # Calculate parameters
    params_full, params_extra = calculate_parameters(dimensions)
    
    # Calculate main and cross rods
    max_length = max(dimensions.length1, dimensions.length2)
    max_width = max(dimensions.width1, dimensions.width2)
    
    main_rods_count, main_rods_length = calculate_main_rods(max_length)
    cross_rods_count, cross_rods_length = calculate_cross_rods(max_width)
    
    # Calculate connecting clips (each intersection of main and cross rods)
    connecting_clips = main_rods_count * cross_rods_count
    
    # Calculate screws (12 per 12 feet of parameter)
    total_parameter_length = (params_full * 12) + params_extra
    screws = ceil(total_parameter_length)  # 1 screw per foot
    
    return CeilingCalculation(
        parameters_full=params_full,
        parameters_extra=params_extra,
        main_rods=main_rods_count,
        cross_rods=cross_rods_count,
        connecting_clips=connecting_clips,
        screws=screws * 12,  # 12 screws per foot
        total_parameter_length=total_parameter_length,
        main_rods_length=main_rods_length,
        cross_rods_length=cross_rods_length
    )