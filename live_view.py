import cv2
cap = cv2.VideoCapture(1)

def liveView():
  while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Tapster-Before', frame)
    cv2.imshow('Tapster-After', gray)
    if cv2.waitKey(1) == ord('q'):
      break

if __name__ == '__main__':
  liveView()
