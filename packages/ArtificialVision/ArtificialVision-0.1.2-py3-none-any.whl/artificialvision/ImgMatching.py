import cv2
import numpy as np

def get_matching_score(source, target, type=0, threshold=0.5):
    # SIFT 검출기 초기화
    sift = cv2.SIFT_create()

    if type == 0:  # 이미지
        kp1, des1 = sift.detectAndCompute(source, None)
        kp2, des2 = sift.detectAndCompute(target, None)

    elif type == 1:  # 비디오
        ret1, frame1 = source.read()
        ret2, frame2 = target.read()
        if not ret1 or not ret2:
            return None  # 프레임 읽기 오류
        kp1, des1 = sift.detectAndCompute(frame1, None)
        kp2, des2 = sift.detectAndCompute(frame2, None)

    # BFMatcher 초기화
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    # 좋은 매치 찾기 위한 비율 테스트 적용
    good_matches = [m for m, n in matches if m.distance < threshold * n.distance]

    # 좋은 매치의 개수를 기반으로 한 매칭 점수 계산
    matching_score = len(good_matches) / max(len(des1), len(des2))
    return matching_score

def get_matching_result(source, target, type=0, threshold=0.5):
    sift = cv2.SIFT_create()

    if type == 0:  # 이미지
        kp1, des1 = sift.detectAndCompute(source, None)
        kp2, des2 = sift.detectAndCompute(target, None)
        img_matches = np.empty((max(source.shape[0], target.shape[0]), source.shape[1]+target.shape[1], 3), dtype=np.uint8)

    elif type == 1:  # 비디오
        ret1, frame1 = source.read()
        ret2, frame2 = target.read()
        if not ret1 or not ret2:
            return None  # 프레임 읽기 오류
        kp1, des1 = sift.detectAndCompute(frame1, None)
        kp2, des2 = sift.detectAndCompute(frame2, None)
        img_matches = np.empty((max(frame1.shape[0], frame2.shape[0]), frame1.shape[1]+frame2.shape[1], 3), dtype=np.uint8)

    # BFMatcher 초기화
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    # 좋은 매치 찾기 위한 비율 테스트 적용
    good_matches = [m for m, n in matches if m.distance < threshold * n.distance]

    # 매치 그리기
    cv2.drawMatchesKnn(source, kp1, target, kp2, good_matches, img_matches, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    return img_matches
