# Reading QR code from Webcam and store unique QR code into CSV file.
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import imutils
import time
import cv2


ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="data.csv",)
args = vars(ap.parse_args())
vs = VideoStream(src=0).start()
time.sleep(2.0)
csv = open(args["output"], "w")
found = set()
count=0

while True:

    frame = vs.read()
    frame = imutils.resize(frame, width=600)
    readers = pyzbar.decode(frame)

    for barcode in readers:
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        text = "{}".format(barcodeData)
        cv2.putText(frame, f'QR code Detected {count}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        if barcodeData not in found:

            csv.write("{}\n".format(barcodeData))
            csv.flush()
            count=count+1

            found.clear()
            found.add(barcodeData)

    cv2.imshow("QR Reader", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break


print(f'Found {count} QR codes')
csv.close()
cv2.destroyAllWindows()
vs.stop()