# import basic modules required
import cv2
import os
import traceback
import numpy as np


#  MANUAL CONFIGURATION
# ~====================~

# replace this with a different
# module if you want to capture your
# frames from somewhere else
# (such as a live feed)
# make sure to include a get_frame() method!
import get_frame as get_frame

# optionally upscale the image
# if you're working with smaller frames
# (upscaled after processing is complete)
upscale_to = (1000, 600)
upscale = False

# show/hide error messages
display_error_messages = True
error_message_colour = (255, 255, 255)

# pick which file to run the filter
# from - this can be any python file
# but make sure to include the filter
# start and filter end markers!
filter_filename = 'filter.py'

# ~====================~


# just a default filter_image function
# used so that the program doesn't crash
# if there's no filter defined in the
# filter file
def filter_image(image): return image


# track exceptions & save the last output
# image, so that we can display exceptions
# to the user without spamming them over
# and over in the console
last_exception = None
last_output_image = None

last_update_mtime = -1

while 1:
    image = get_frame.get_frame()

    if last_output_image is None:
        last_output_image = image

    current_update_mtime = os.path.getmtime(filter_filename)
    if current_update_mtime > last_update_mtime:
        last_update_mtime = current_update_mtime

        filter_code = open(filter_filename, 'r').read().split(
            '# start filter', 1)[-1].split(
            '# end filter', 1)[0]
        execution_valid = True
        try:
            exec(filter_code)
            image_out = filter_image(image)
            if image_out is not None:
                last_output_image = image_out.copy()
        except Exception as e:
            this_exception = traceback.format_exc()
            if last_exception != this_exception:
                last_exception = this_exception
                print()
                print("  Exception")
                print(" ~=========~")
                print()
                print(this_exception)
            image_out = last_output_image
            execution_valid = False

    try:
        if upscale:
            resized_image = cv2.resize(image_out, upscale_to)
        else:
            resized_image = image_out

        # write some error message text onto the displayed image
        if not execution_valid:
            exception_msg = f"{filter_filename} exception"
            (w, h), b = cv2.getTextSize(exception_msg, cv2.FONT_HERSHEY_COMPLEX, 0.6, 1)
            cv2.rectangle(resized_image, (0, 0), (w+5, h+b+4), (0, 0, 0), -1)
            cv2.putText(resized_image,
                        exception_msg, (2, 16),
                        cv2.FONT_HERSHEY_COMPLEX, 0.6,
                        (255, 255, 255), 1)
            if display_error_messages:
                write_lines = [x for x in last_exception.split('\n') if x]
                largest_w = 5
                for line in write_lines:
                    if not line:
                        continue
                    (w, h), b = cv2.getTextSize(
                        line, cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.6, 1)
                    w += 5
                    h += 6
                    if w > largest_w:
                        largest_w = w
                cv2.rectangle(resized_image, (0, 20),
                              (largest_w, 30+len(write_lines)*16),
                              (0, 0, 0), -1)
                for index, line in enumerate(write_lines):
                    x, y = (2, 32+16*index)
                    cv2.putText(resized_image,
                                line, (x, y+5),
                                cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.6,
                                error_message_colour, 1)

        cv2.imshow('Filtered Image', resized_image)

    except:
        pass

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
