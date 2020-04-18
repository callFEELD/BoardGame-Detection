import cv2
from src import board_detection as bd
from src import figure_detection as fd
import math
import time


class Detector:
    debug = True
    layers = []

    def set_debug(self, boolean: bool):
        self.debug = boolean

    def add_debug_layer(self, name: str):
        self.layers.append(
            {
                "name": f"Debug Function: {name}",
                "image": self.debug_image
            }
        )

    def show_debug_layers(self):
        for layer in self.layers:
            cv2.imshow(layer["name"], layer["image"])


class BoardDetector(Detector):
    default_options = {
        "prepare": {
            "resize": [512, 512]
        },
        "corners": {
            "maxcorners": 500,
            "qualitylevel": 0.01,
            "mindistance": 20
        },
        "lines": {
            "harris": {
                "rho": 1,
                "theta": 0.01,
                "threshold": 350
            },
            "filter": {
                "rho": 20,
                "theta": 0.15
            }
        },
        "similarpoints": {
            "range": 9
        },
        "correctlines": {
            "amount": 9
        }
    }

    def __init__(self):
        self.options = self.default_options

    def update_options(self, options):
        self.options.update(options)

    def _prepare_image(self, frame):
        opt = self.options["prepare"]
        # prepare the input frame
        self.frame = frame
        self.res_frame = cv2.resize(self.frame, (opt["resize"][0], opt["resize"][1]))
        self.cframe = self.res_frame.copy()
        self.gray_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

    def _corner_detection(self, frame):
        opt = self.options["corners"]

        self.debug_image = frame.copy()
        self.harris_corners = bd.find_corners(
            frame, opt["maxcorners"], opt["qualitylevel"], opt["mindistance"]
        )
        # remap the corners to points
        corners = []
        if self.harris_corners is not None:
            for corner in self.harris_corners:
                corners.append(corner[0])
                if self.debug:
                    cv2.circle(self.debug_image, (int(corner[0][0]), int(corner[0][1])), 3, (0, 0, 255))

        self.add_debug_layer("corner detection")
        return corners

    def _line_detection(self, frame):
        opt = self.options["lines"]

        # find lines based of a canny image (binary image)
        self.debug_image = frame.copy()
        canny = cv2.Canny(frame, 100, 300)

        self.hough_lines = bd.find_lines(
            canny, opt["harris"]["rho"], opt["harris"]["theta"],
            opt["harris"]["threshold"]
        )
        self.hough_lines = bd.filter_lines(
            self.hough_lines, opt["filter"]["rho"], opt["filter"]["theta"]
        )

        # prepare the lines to find the intersections
        lines = []
        if self.hough_lines is not None:
            for i in range(0, len(self.hough_lines)):
                rho = self.hough_lines[i][0][0]
                theta = self.hough_lines[i][0][1]
                a = math.cos(theta)
                b = math.sin(theta)
                x0 = a * rho
                y0 = b * rho
                pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
                pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
                lines.append(
                    (x0 + 1000*(-b), int(y0 + 1000*(a)),
                     int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
                )
                cv2.line(self.debug_image, pt1, pt2, 255, 1)

        self.add_debug_layer("line detection")
        return lines

    def _calculate_intersections(self, lines):
        self.debug_image = self.res_frame.copy()
        # get the intersections
        intersec_obj = bd.get_intersections(lines)
        # filter intersections that are not in the image
        bd.filter_intersections(intersec_obj, self.debug_image, display=True)

        self.add_debug_layer("calculate intersections")
        return intersec_obj

    def _find_similar_corners_to_intersections(self, intersections,
                                               corners, in_range):
        # find the intersections that are close to the corners
        # remove the other ones
        self.debug_image = self.res_frame.copy()
        for i, line in enumerate(intersections):
            to_be_removed = []
            for intersec in line["intersections"]:
                close = False
                for corner in corners:
                    if bd.is_close_to(intersec["position"], corner, radian=in_range):
                        cv2.circle(self.debug_image, (int(intersec["position"][0]), int(intersec["position"][1])), 3, (255, 255, 0))
                        close = True
                        break
                if not close:
                    to_be_removed.append(intersec)
            for remove in to_be_removed:
                intersections[i]["intersections"].remove(remove)

        self.add_debug_layer("similar corner and intersections")
        return intersections

    def _find_correct_lines(self, intersec_obj, amount):
        # only enable the lines with at least 9 correct points
        correct_lines = []
        for line in intersec_obj:
            if len(line["intersections"]) >= amount:
                correct_lines.append(line["line"])
        return correct_lines

    def _find_correct_points(self, correct_lines, intersec_obj):
        self.debug_image = self.res_frame.copy()
        correct_points = []
        for line in intersec_obj:
            if line["line"] in correct_lines:
                for intersec in line["intersections"]:
                    if intersec["line"] in correct_lines:
                        # check if already added
                        if intersec["position"] not in correct_points:
                            correct_points.append(intersec["position"])
                            cv2.circle(self.debug_image, (int(intersec["position"][0]), int(intersec["position"][1])), 6, (0, 255, 0))
        self.add_debug_layer("find correct points")
        return correct_points

    def _get_board_perspective(self, points, min_points):
        if len(points) >= min_points:
            return bd.get_chessboard_perspective(self.res_frame, points)
        else:
            return None

    def find_board(self, image):
        self._prepare_image(image)
        # find the specific features for the board detection
        corners = self._corner_detection(self.res_frame)
        lines = self._line_detection(self.res_frame)

        # find the intersections of the lines
        intersections = self._calculate_intersections(lines)
        # find intersections that are in a range of the corners
        similar_intersections = \
            self._find_similar_corners_to_intersections(
                intersections, corners,
                self.options["similarpoints"]["range"]
            )

        # select the lines that have at least 9 similar points
        correct_lines = self._find_correct_lines(
            similar_intersections, self.options["correctlines"]["amount"]
        )
        # select the similar intersection points only from the correct lanes
        correct_points = self._find_correct_points(
            correct_lines, similar_intersections
        )

        # get the chessboard perspective, if the amount of
        # correct points is equal or larger than 9*9
        board_perspective = self._get_board_perspective(
            correct_points, 9*9
        )

        return board_perspective

    def find_board_from_cap(self, source, max_waiting_seconds=30):
        self.cap = cv2.VideoCapture(source)
        while True:
            start_time = time.time()
            ret, frame = self.cap.read()
            if ret:
                board_perspective = self.find_board(frame)

                if board_perspective is not None:
                    return board_perspective

            # if the board was not found in 5 seconds, break the loop
            if (time.time() - start_time) > max_waiting_seconds:
                return None


class FigureDetector(Detector):

    def __init__(self):
        pass

    def find_circles(self, board_perspective):
        self.debug_image = board_perspective.copy()
        self.hough_circles = fd.find_circles(board_perspective)
        circles = []
        for i in self.hough_circles[0,:]:
            circles.append({"x": i[0], "y": i[1], "r": i[2]})
            cv2.circle(self.debug_image,(i[0],i[1]),i[2],(0,255,0),2)
            cv2.circle(self.debug_image,(i[0],i[1]),2,(0,0,255),3)

        self.add_debug_layer("find circles")
        return circles

    def find_piece_chessboard_position(self, pieces, square_pos):
        positions = []
        for r, row in enumerate(square_pos):
            for i, square in enumerate(row):
                for piece in pieces:
                    if piece["x"] >= square["x"][0] and piece["x"] <= square["x"][1] \
                        and piece["y"] >= square["y"][0] and piece["y"] <= square["y"][1]:
                        positions.append([r, i])
        return positions

    def find_pieces(self, board_perspective):
        # frist find the circles on the board
        circles = self.find_circles(board_perspective)
        # divide the board into the 8x8 grid
        squares, square_pos = bd.divide_chessboard(board_perspective)
        # find which circle is on wich square
        fig = self.find_piece_chessboard_position(circles, square_pos)

        return fig
