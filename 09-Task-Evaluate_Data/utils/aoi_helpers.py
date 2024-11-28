
# AOIs
from collections import OrderedDict
from pathlib import Path
from typing import Any, Sequence

import cv2
import numpy as np
import pandas as pd
from tqdm.notebook import tqdm
from utils.aoi_settings import (AOI_AFFECTED, AOI_HIERARCHY, AOI_NO, AOI_SIZE,
                                COLOR_AOI_NAME_MAPPING, COLOR_AOI_NO,
                                POS_BOTTOM, POS_LEFT, POS_RIGHT, POS_TOP)
from utils.file_settings import SNIPPET_COLUMN_NUMBER, SNIPPET_COLUMN_VERSION
from utils.snippet_helpers import (get_corresponding_snippet, get_snippet_base,
                                   get_snippet_number, get_snippet_version)
from utils.snippet_settings import (CONDITION, CONDITION_CLEAN,
                                    CONDITION_VARIANT_MATCH, SNIPPET_CLEAN,
                                    SNIPPET_OBF)
from utils.textconstants import OPTIMAL, SNIPPET

#############################
# AOI detection & retrieval from (screenshot) images
#############################


# ##
# * get all pixels in the colors of the AOIs from the image (in binary view)
# * detect contours


def detect_possible_AOI_contours_from_screenshot(image_path: Path, temp_folder: Path = None) -> tuple[np.ndarray, Sequence]:
    '''detects contours representing possible AOIs in AOI colors

    contour detection based on https://thinkinfi.com/shape-detection-using-opencv-and-python/?utm_content=cmp-true

    Arguments:
    * image_path: the path the screenshot image is stored to 
    * temp_folder: folder path to store pre-results for debugging

    returns: 
    * open image array
    * sequence of contours
    '''
    # read image as array
    image = cv2.imread(image_path.as_posix())
    image_aois = np.copy(image)
    # Set colors that are expected as AOIs to a COLOR_AOI_NO (not white as white is used as background) and others all to black
    for aoi_c in COLOR_AOI_NAME_MAPPING.keys():
        image_aois[np.where((image_aois == aoi_c).all(axis=2))] = COLOR_AOI_NO
        r_aoi_c = tuple(reversed(aoi_c))
        image_aois[np.where(
            (image_aois == r_aoi_c).all(axis=2))] = COLOR_AOI_NO
    image_aois[np.where((image_aois != COLOR_AOI_NO).any(axis=2))] = [0, 0, 0]
    if not temp_folder is None:
        cv2.imwrite(
            (temp_folder/f'{image_path.stem}_test_ignore.png').as_posix(), image_aois)
    # Convert input image to grayscale to reduce color channel dimension
    gray_img = cv2.cvtColor(image_aois, cv2.COLOR_BGR2GRAY)
    if not temp_folder is None:
        cv2.imwrite(
            (temp_folder/f'{image_path.stem}_test_gray.png').as_posix(), gray_img)

    # Threshold the grayscale to filter out possible aoi contours
    ret, binary_image = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY)
    if not temp_folder is None:
        cv2.imwrite(
            (temp_folder/f'{image_path.stem}_test_bin.png').as_posix(), binary_image)
    # refill places where two rectangles overlap at the left side of the image inside the screenshot
    SECOND_RECTANGLE_START = 558
    refill_candidates = np.where(
        binary_image[:, SECOND_RECTANGLE_START] == 255)[0]
    refill_candidates = refill_candidates[np.where(
        binary_image[refill_candidates, SECOND_RECTANGLE_START-1] == 0)[0]]
    if refill_candidates.shape[0]:
        binary_image[refill_candidates.min():refill_candidates.max(
        ), SECOND_RECTANGLE_START:SECOND_RECTANGLE_START+2] = 255
        if not temp_folder is None:
            cv2.imwrite(
                (temp_folder/f'{image_path.stem}_test_refill.png').as_posix(), binary_image)
    # Detect contours
    contours, hierarchy = cv2.findContours(
        binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # or fill missing pixels between | and _ for snippet no. 5
    return image, contours


def realign(v1: int, v2: int) -> tuple[bool, int | str]:
    '''realigns two numbers to their center point if they are close, otherwise returns failure

    Arguments:
    * v1, v2: two numbers that should be aligned

    returns:
    * whether the alignment has worked
    * the mean value if it worked, otherwise an error string
    '''
    if (abs(v1-v2) < 3):
        return True, int((v1+v2)/2)
    else:
        return False, f'Distance between values too large: {v1}, {v2}'


def get_rectangles_from_contours(contours: Sequence) -> list[tuple[list[list], dict[str, int], float]]:
    '''checks the given contours for rectangles suitable for AOIs, removes (near) duplicates

    contour checks based on https://thinkinfi.com/shape-detection-using-opencv-and-python/?utm_content=cmp-true

    Checks contain:
    * polygons of 4 points
    * certain area size
    * if rectangles are slightly misaligned (less than 3 pixels vertically or horizontally), correct the alignment

    The resulting rectangles are sorted by area size (in reverse) and similar ones are removed.

    Arguments: sequence of contours: the contours recognized in the image to be checked for rectangles

    returns: a list of rectangles described by (the 4 rectangle points as coordinates sorted in ascending order (identical for all points), the 4 borders of the rectangle, the area the rectangle surrounds)
    '''
    rectangle_data = []
    # for each detected contours
    for contour_num, contour in enumerate(contours):
        # Find points of detected contour
        end_points = cv2.approxPolyDP(
            contour, 0.01 * cv2.arcLength(contour, True), True)
        points_no = len(end_points)
        if points_no != 4:  # make sure it's a 4-polygon
            # print(contour_num, 'not rectangle', points_no, end_points)
            continue
        # Make sure contour area is large enough (Rejecting unwanted contours)
        area = cv2.contourArea(contour)
        if area < 10:
            continue
        rectangle_points = sorted(
            [[end_points[i][0][0], end_points[i][0][1]] for i in range(4)])
        # make sure it's a real rectangle by checking x and y coordinates, if only small difference, realign
        if (rectangle_points[0][0] != rectangle_points[1][0]) or (rectangle_points[2][0] != rectangle_points[3][0]):
            realigned_1 = realign(
                rectangle_points[0][0], rectangle_points[1][0])
            realigned_2 = realign(
                rectangle_points[2][0], rectangle_points[3][0])
            if realigned_1[0] and realigned_2[0]:
                rectangle_points[0][0], rectangle_points[1][0] = realigned_1[1], realigned_1[1]
                rectangle_points[2][0], rectangle_points[3][0] = realigned_2[1], realigned_2[1]
                rectangle_points.sort()
            else:
                print(contour_num, 'not aligned 1', rectangle_points)
                continue
        if (rectangle_points[0][1] != rectangle_points[2][1]) or (rectangle_points[1][1] != rectangle_points[3][1]):
            realigned_1 = realign(
                rectangle_points[0][1], rectangle_points[2][1])
            realigned_2 = realign(
                rectangle_points[1][1], rectangle_points[3][1])
            if realigned_1[0] and realigned_2[0]:
                rectangle_points[0][1], rectangle_points[2][1] = realigned_1[1], realigned_1[1]
                rectangle_points[1][1], rectangle_points[3][1] = realigned_2[1], realigned_2[1]
                rectangle_points.sort()
            else:
                print(contour_num, 'not aligned 2', rectangle_points)
                continue
        # print(contour_num, 'RP:', rectangle_points)

        # transform 4 coordinates to border dict
        named_rectangle_points = {
            POS_TOP: int(min(r[1] for r in rectangle_points)),
            POS_LEFT: int(min(r[0] for r in rectangle_points)),
            POS_BOTTOM: int(max(r[1] for r in rectangle_points)),
            POS_RIGHT: int(max(r[0] for r in rectangle_points)),
        }
        rectangle_data.append((rectangle_points, named_rectangle_points, area))

    # sort by area, biggest first
    rectangle_data.sort(key=lambda x: x[-1], reverse=True)
    # check if identical / very similar rectangles given
    i = 0
    while i < len(rectangle_data)-1:
        named_rectangle_points = rectangle_data[i][1]
        named_rectangle_points_other = rectangle_data[i+1][1]
        similar = True
        for position in named_rectangle_points:
            if abs(named_rectangle_points[position]-named_rectangle_points_other[position]) > 3:
                similar = False
        if similar:
            rectangle_data.pop(i+1)
        else:
            i += 1
    return rectangle_data


# * from those rectangles sorted by area, get the color of the original image (using 4 endpoints, middle of the lower resp. right border)
# * identify their level by using levels derived from the 6 color samples
# * only levels lower than the ones used before are considered for the next one
# * return per aoi the four boundaries top, left, bottom, right


def get_AOIs_from_rectangles(image_path: Path, image: Any, named_rectangles: list[tuple[list[list], dict[str, int], float]], temp_folder: Path = None) -> dict[str, dict[str, int]]:
    '''takes the rectangles and assigns them to AOI levels 

    rectangles must be sorted by area (3rd argument) descending, and are assigned to highest-level first

    Arguments:
    * image_path: the path the screenshot image is stored to 
    * image: open image array
    * named_rectangles: a list of rectangles described by (the 4 rectangle points as coordinates, the 4 borders of the rectangle, the area the rectangle surrounds)
    * temp_folder: folder path to store pre-results for debugging

    returns: the AOIs and its border values for each
    '''
    AOIs = {}
    accepted_levels = list(reversed(AOI_HIERARCHY))

    for (rectangle_points, named_rectangle_points, _) in named_rectangles:
        # as top and left is sometimes overtaken by another AoI on image borders, add middle of lower and right border to the points to consider
        points_on_rectangle = rectangle_points+[
            [named_rectangle_points[POS_RIGHT], int(
                (named_rectangle_points[POS_BOTTOM]+named_rectangle_points[POS_TOP])/2)],
            [int((named_rectangle_points[POS_RIGHT]+named_rectangle_points[POS_LEFT])/2),
             named_rectangle_points[POS_BOTTOM]],
            [named_rectangle_points[POS_LEFT], int(
                (named_rectangle_points[POS_BOTTOM]+named_rectangle_points[POS_TOP])/2)],
            [int((named_rectangle_points[POS_RIGHT]+named_rectangle_points[POS_LEFT])/2), named_rectangle_points[POS_TOP]]]

        # find AoI color & hierarchy per point
        possible_levels = {}
        for point in points_on_rectangle:
            # reverse x and y to index ndarray correctly
            point_color = tuple(image[tuple(reversed(point))])
            # reverse color as library uses BGR scheme
            point_level = COLOR_AOI_NAME_MAPPING.get(
                tuple(point_color[::-1]), AOI_NO)
            if not point_level == AOI_NO:
                if not point_level in possible_levels:
                    possible_levels[point_level] = [point_color, 0]
                possible_levels[point_level][1] += 1
        if len(possible_levels) > 1:
            print(f'Multiple levels for {image_path} found: {possible_levels}')
        possible_levels_new = OrderedDict()
        for level in sorted(possible_levels.keys(), key=lambda key: possible_levels[key]):
            possible_levels_new[level] = possible_levels[level]

        # get highest acceptable level from possible levels as level to use
        aoi_level = None
        for level in possible_levels_new:
            if level in accepted_levels:
                aoi_level = level
                accepted_levels = accepted_levels[accepted_levels.index(
                    level)+1:]
                break
        if aoi_level == None:
            aoi_level = AOI_NO
            print(image_path.stem,
                  'AOI was detected but could not be identified.')
        AOIs[aoi_level] = named_rectangle_points

    if not temp_folder is None:
        # mark aoi in image for debugging by overlaying it with its color in the real image
        rectangle_color = tuple(
            possible_levels_new.get(aoi_level, [(0, 0, 0), 0])[0])
        image = cv2.rectangle(image, tuple(rectangle_points[0]), tuple(rectangle_points[3]),
                              (int(rectangle_color[0]), int(rectangle_color[1]), int(rectangle_color[2])), 4)
        cv2.imwrite(
            (temp_folder/f'{image_path.stem}_test_aois.png').as_posix(), image)
    return AOIs


def check_matching_AOIs(all_aois: dict[str, dict[str, dict[str, float]]]) -> list[dict[str, list[str]]]:
    '''checks whether the snippets within a pair contain aois with identical levels
     Argument: all_aois: the aois per snippet and level given by the 4 borders
     returns: a list of all snippet pairs with unequal aoi leveling'''
    checked_snippet_bases = []
    unmatching_snippets = []
    for snippet, snippet_aois in tqdm(all_aois.items()):
        snippet_base = get_snippet_base(snippet)
        if snippet_base in checked_snippet_bases:
            continue
        other_snippet = get_corresponding_snippet(snippet)
        aoi_levels = set(snippet_aois.keys())
        other_aoi_levels = set(all_aois[other_snippet].keys())
        if aoi_levels != other_aoi_levels:
            unmatching_snippets.append(
                {snippet: aoi_levels, other_snippet: other_aoi_levels})
        checked_snippet_bases.append(snippet_base)
    return unmatching_snippets


def get_optimal_AOI(AOIs: dict[str, dict[str, int]]) -> dict[str, int] | None:
    f'''gets optimal AOI to reach (most constrained AOI that still follows hierarchical boundaries)

    Arguments:
    * AOIs: the AOIs to browse, each given by AOI name and inside given via the 4 position markers '{POS_TOP}', '{POS_LEFT}', '{POS_BOTTOM}', '{POS_RIGHT}'

    returns: the hierarchically lowest AOI that still complies with the hierarchy
        (eg. OP can sometimes be not in NEXP, therefore it returns NEXP instead of OP)
        if not existing any, return None
    '''
    if len(AOIs) == 0:
        print(f'No AOI found')
        return AOI_NO, None
    elif len(AOIs) == 1:
        if AOI_NO in AOIs:
            print(f'Only AOI without hierarchy found, AOIs: {AOIs}')
            return AOI_NO, None
        return list(AOIs.keys())[0], AOIs[list(AOIs.keys())[0]]
    # Check AOI (haoi) from lowest to highest level
    for i, haoi in enumerate(AOI_HIERARCHY):
        if not haoi in AOIs:
            continue
        within_limits = True
        for hhaoi in AOI_HIERARCHY[i+1:]:
            if hhaoi in AOIs:
                # check that this AOI (haoi) is inside those above (hhaoi)
                if (check_point_in_area(AOIs[haoi][POS_LEFT], AOIs[haoi][POS_TOP], 0, 0, AOIs[hhaoi]) and
                        check_point_in_area(AOIs[haoi][POS_RIGHT], AOIs[haoi][POS_BOTTOM], 0, 0, AOIs[hhaoi])):
                    return haoi, AOIs[haoi]
                else:
                    # print(
                    #     f'Most constrained AOI {haoi} not within hierarchical boundary of {hhaoi}: \n{haoi}: {AOIs[haoi]}\n{hhaoi}: {AOIs[hhaoi]}')
                    within_limits = False
                    break
        if within_limits:
            return haoi, AOIs[haoi]
    return AOI_NO, None


def get_AOI_size_per_snippet_pair(all_aois: dict[str, dict[str, dict[str, float]]]) -> pd.DataFrame:
    '''create a dataframe with AoI size per snippet pair, condition and AoI level

    Argument: all_aois: all AoIs

    returns: a dataframe with AoI size per snippet pair, condition and AoI level (columns CONDITION, AOI_NO,SNIPPET, AOI_SIZE, OPTIMAL)
    '''
    level_area_data = pd.DataFrame(
        columns=[CONDITION, AOI_NO, SNIPPET, f'{SNIPPET}_base', SNIPPET_COLUMN_NUMBER, SNIPPET_COLUMN_VERSION,
                 AOI_SIZE, OPTIMAL, POS_BOTTOM, POS_LEFT, POS_RIGHT, POS_TOP])

    checked_snippet_bases = []
    for snippet in tqdm(all_aois):
        snippet_base = get_snippet_base(snippet)
        if snippet_base in checked_snippet_bases:
            continue
        other_snippet = get_corresponding_snippet(snippet)
        if SNIPPET_OBF in snippet:
            clean_snippet, obf_snippet = other_snippet, snippet
        elif SNIPPET_CLEAN in snippet:
            clean_snippet, obf_snippet = snippet, other_snippet
        else:
            raise Exception(
                f'Snippet should contain either {SNIPPET_CLEAN} or {SNIPPET_OBF}')
        optimal_AOI_level = AOI_HIERARCHY[
            max(AOI_HIERARCHY.index(get_optimal_AOI(all_aois[clean_snippet])[0]),
                AOI_HIERARCHY.index(get_optimal_AOI(all_aois[obf_snippet])[0]))]

        base_entry = {SNIPPET: clean_snippet,
                      CONDITION: CONDITION_VARIANT_MATCH[SNIPPET_CLEAN],
                      f'{SNIPPET}_base': snippet_base,
                      SNIPPET_COLUMN_VERSION: get_snippet_version(clean_snippet),
                      SNIPPET_COLUMN_NUMBER: get_snippet_number(clean_snippet),
                      }
        for aoi_level, aoi in all_aois[clean_snippet].items():
            level_area_data.loc[len(level_area_data)] = {AOI_NO: aoi_level,
                                                         AOI_SIZE: abs(aoi[POS_TOP]-aoi[POS_BOTTOM]) * abs(aoi[POS_LEFT]-aoi[POS_RIGHT]),
                                                         OPTIMAL: aoi_level == optimal_AOI_level} | base_entry | aoi
        base_entry = base_entry | {
            SNIPPET: obf_snippet, CONDITION: CONDITION_VARIANT_MATCH[SNIPPET_OBF]
        }
        for aoi_level, aoi in all_aois[obf_snippet].items():
            level_area_data.loc[len(level_area_data)] = {AOI_NO: aoi_level,
                                                         AOI_SIZE: abs(aoi[POS_TOP]-aoi[POS_BOTTOM]) * abs(aoi[POS_LEFT]-aoi[POS_RIGHT]),
                                                         OPTIMAL: aoi_level == optimal_AOI_level} | base_entry | aoi
        checked_snippet_bases.append(snippet_base)
    return level_area_data


def check_point_in_area(x: float, y: float, radius_x: float, radius_y: float, area: dict[str, int]) -> bool:
    f'''checks whether the point or the surrounding range can be found inside the area

    Arguments:
    * x, y: the position of the point to check
    * radius_x, radius_y: the area around the point counting as one (given as diameter in form of a rectangle)
    * area: the area to check for, given via the 4 position markers '{POS_TOP}', '{POS_LEFT}', '{POS_BOTTOM}', '{POS_RIGHT}'

    returns: whether the point (including range) is (partly) inside the area
    '''
    left_x_border, right_x_border = x-radius_x, x+radius_x
    top_y_border, bottom_y_border = y-radius_y, y+radius_y
    if right_x_border < area[POS_LEFT]:
        return False
    if left_x_border > area[POS_RIGHT]:
        return False
    if top_y_border > area[POS_BOTTOM]:
        return False
    if bottom_y_border < area[POS_TOP]:
        return False
    # print(f'Area ({x},{y}) with ranges {range_x}, {range_y} in area {area}')
    return True


def get_distance_to_area(x: float, y: float, range_x: float, range_y: float, area: dict[str, int]) -> float:
    f'''checks whether the point or the surrounding range can be found inside the area

    Arguments:
    * x, y: the position of the point to check
    * range_x, range_y: the area around the point counting as one (given as diameter in form of a rectangle)
    * area: the area to check for, given via the 4 position markers '{POS_TOP}', '{POS_LEFT}', '{POS_BOTTOM}', '{POS_RIGHT}'

    returns:
    * the minimal Euclidean distance of the point (including range) to the area
    * a list of direction markers (0-2) that describe the relative position of the point with regard to the area ('{POS_TOP}' means that the point is above the area)
    '''
    direction_markers = []
    left_x_border, right_x_border = x-range_x/2, x+range_x/2
    top_y_border, bottom_y_border = y-range_y/2, y+range_y/2
    left_distance = max(0, area[POS_LEFT]-right_x_border)
    right_distance = max(0, left_x_border-area[POS_RIGHT])
    assert ((right_distance == 0) or (left_distance == 0))
    if right_distance > 0:
        direction_markers.append(POS_RIGHT)
    elif left_distance > 0:
        direction_markers.append(POS_LEFT)
    top_distance = max(0, area[POS_TOP]-bottom_y_border)
    bottom_distance = max(0, top_y_border - area[POS_BOTTOM])
    assert ((top_distance == 0) or (bottom_distance == 0))
    if top_distance > 0:
        direction_markers.append(POS_TOP)
    elif bottom_distance > 0:
        direction_markers.append(POS_BOTTOM)
    x_distance = max(left_distance, right_distance)
    y_distance = max(top_distance, bottom_distance)
    return np.linalg.norm([x_distance, y_distance]), direction_markers
