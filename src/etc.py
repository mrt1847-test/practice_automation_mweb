import time

from src.base_pages.base import *
import pytesseract
from PIL import Image
import base64
from io import BytesIO
import platform
import cv2

class EtcFunction():
    IMPLICIT_WAIT_TIME = 10
    TIMEOUT = 30

    def __init__(self, driver):
        self.driver = driver
        self.driver.implicitly_wait(self.IMPLICIT_WAIT_TIME)
        self.timeout = self.TIMEOUT

    def __reset_given(self):
        # Given 초기화
        runtext = '앱 재실행 - Given 초기화'
        print("#", runtext, "시작")
        app_package = 'com.ebay.kr.gmarket'
        app_activity = 'com.ebay.kr.gmarket.eBayKoreaGmarketActivity'
        self.driver.start_activity(app_package=app_package, app_activity=app_activity)
        print("#", runtext, "종료")

    def __scroll_mobile_app(self, location, xpath, scroll_amount, max_scroll_count):
        """

        요소가 화면에 보일때까지 스크롤
        :param (str) location : 스크롤하려는 방향 / 1: 아래에서 위로 스와이프 / 2: 위에서 아래로 스와이프
        :param (str) xpath: 찾으려는 요소
        :param (int) scroll_amount: 한번 스크롤시 이동하는 정도(1~10 사이에서 결정하며 숫자가 클수록 많이 이동)
        :param (int) max_scroll_count: 최대 스크롤 횟수 (스크롤 횟수에 도달할때까지 요소를 찾지 못하면 raise 발생)
        :return: 없음
        :example: __scroll_mobile_app(self,"1",xpath,3,20) # 해당 요소를 찾을 때까지 아래에서 위로 최대 20번 스크롤 진행

        """
        scroll_count = 0
        size = self.driver.get_window_size()
        width = size['width']
        height = size['height']

        k = (height / 20) * scroll_amount

        while True:
            try:
                time.sleep(5)
                self.driver.implicitly_wait(5)
                element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
                if element.location['y'] > (height * 2 / 3):
                    loc = element.location
                    new_y = loc['y']
                    self.driver.swipe(width / 2, height / 2, width / 2, (height / 2) - k / 2)
                    if element.location['y'] == new_y:
                        print("스와이프 끝부분 도달")
                        break
                    print("위치 조정")
                elif element.location['y'] < (height * 1 / 3):
                    loc = element.location
                    new_y = loc['y']
                    self.driver.swipe(width / 2, height / 2, width / 2, (height / 2) + k / 2)
                    if element.location['y'] == new_y:
                        print("스와이프 끝부분 도달")
                        break
                    print("위치 조정")
                else:
                    print("요소 발견됨")
                    break
            except:
                scroll_count += 1
                if scroll_count > max_scroll_count:
                    print("최대 스크롤 횟수 초과")
                    raise Exception("요소를 찾을 수 없음")

                print("스크롤 진행 중 ({}회)".format(scroll_count))
                if location == "1":
                    self.driver.swipe(width / 2, height / 2, width / 2, (height / 2) - k)
                elif location == "2":
                    self.driver.swipe(width / 2, height / 2, width / 2, (height / 2) + k)
                else:
                    print("#", "스와이프할 방향을 지정해주세요.")
                    raise

            finally:
                # try 블록 이후에 원래의 implicit_wait 값으로 복원
                self.driver.implicitly_wait(self.implicit_wait)

    def __scroll_mobile_app_type(self, location, type, value, scroll_amount, max_scroll_count):
        """

        요소가 화면에 보일때까지 스크롤
        :param (str) location : 스크롤하려는 방향 / 1: 아래에서 위로 스와이프 / 2: 위에서 아래로 스와이프
        :param (str) type : Object Type (id or xpath)
        :param (str) value: Object Value
        :param (int) scroll_amount: 한번 스크롤시 이동하는 정도(1~10 사이에서 결정하며 숫자가 클수록 많이 이동)
        :param (int) max_scroll_count: 최대 스크롤 횟수 (스크롤 횟수에 도달할때까지 요소를 찾지 못하면 raise 발생)
        :return: 없음
        :example: __scroll_mobile_app(self,"1",xpath,3,20) # 해당 요소를 찾을 때까지 아래에서 위로 최대 20번 스크롤 진행

        """
        scroll_count = 0
        size = self.driver.get_window_size()
        width = size['width']
        height = size['height']

        k = (height / 20) * scroll_amount
        time.sleep(5)

        while True:
            try:
                self.driver.implicitly_wait(5)

                if type == "xpath":
                    element = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, value)))
                elif type == "id":
                    element = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.ID, value)))

                if element.location['y'] > (height * 2 / 3):
                    loc = element.location
                    new_y = loc['y']
                    self.driver.swipe(width / 2, height / 2, width / 2, (height / 2) - k / 2)
                    if element.location['y'] == new_y:
                        print("스와이프 끝부분 도달")
                        break
                    print("위치 조정")
                elif element.location['y'] < (height * 1 / 3):
                    loc = element.location
                    new_y = loc['y']
                    self.driver.swipe(width / 2, height / 2, width / 2, (height / 2) + k / 2)
                    if element.location['y'] == new_y:
                        print("스와이프 끝부분 도달")
                        break
                    print("위치 조정")
                else:
                    print("요소 발견됨")
                    break
            except:
                scroll_count += 1
                if scroll_count > max_scroll_count:
                    print("최대 스크롤 횟수 초과")
                    raise Exception("요소를 찾을 수 없음")

                print("스크롤 진행 중 ({}회)".format(scroll_count))
                if location == "1":
                    self.driver.swipe(width / 2, height / 2, width / 2, (height / 2) - k)
                elif location == "2":
                    self.driver.swipe(width / 2, height / 2, width / 2, (height / 2) + k)
                else:
                    print("#", "스와이프할 방향을 지정해주세요.")
                    raise

            finally:
                # try 블록 이후에 원래의 implicit_wait 값으로 복원
                self.driver.implicitly_wait(self.implicit_wait)

    def __lr_scroll_for_find_element(self, location, xpath1, xpath2, scroll_amount, max_scroll_count):
        """

        요소가 화면에 보일때까지 스크롤
        :param (str) location : 스크롤하려는 방향 / 1: 오른쪽에서 왼쪽으로 스와이프 / 2: 왼쪽에서 오른쪽으로 스와이프
        :param (str) xpath1: 기준점으로 삼는 요소
        :param (str) xpath2: 찾으려는 요소
        :param (int) scroll_amount: 한번 스크롤시 이동하는 정도(1~10 사이에서 결정하며 숫자가 클수록 많이 이동)
        :param (int) max_scroll_count: 최대 스크롤 횟수 (스크롤 횟수에 도달할때까지 요소를 찾지 못하면 raise 발생)
        :return: 없음
        :example: __lr_scroll_for_find_element(self,"1",xpath1,xpath2,3,20) # 해당 요소를 찾을 때까지 아래에서 위로 최대 20번 스크롤 진행

        """
        size = self.driver.get_window_size()
        width = size['width']
        scroll_count = 0
        element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath1)))
        loc = element.location
        new_x = loc['x']
        new_y = loc['y']

        k = (width / 20) * scroll_amount

        while True:
            try:
                self.driver.implicitly_wait(5)
                element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath2)))
                if element.location['x'] > (width * 2 / 3):
                    loc = element.location
                    new_x = loc['x']
                    self.driver.swipe(width / 2, new_y, ((width / 2) - (k / 2)), new_y)
                    if element.location['x'] == new_x:
                        print("스와이프 끝부분 도달")
                        break
                    print("위치 조정")
                elif element.location['x'] < (width * 1 / 3):
                    loc = element.location
                    new_x = loc['x']
                    self.driver.swipe(width / 2, new_y, ((width / 2) + (k / 2)), new_y)
                    if element.location['x'] == new_x:
                        print("스와이프 끝부분 도달")
                        break
                    print("위치 조정")
                else:
                    print("요소 발견됨")
                    break
            except:
                scroll_count += 1
                if scroll_count > max_scroll_count:
                    print("최대 스크롤 횟수 초과")
                    raise Exception("요소를 찾을 수 없음")

                print("스크롤 진행 중 ({}회)".format(scroll_count))
                if location == "1":
                    self.driver.swipe(width / 2, new_y, width / 2 - k, new_y)
                elif location == "2":
                    self.driver.swipe(width / 2, new_y, width / 2 + k, new_y)
                else:
                    print("#", "스와이프할 방향을 지정해주세요.")
                    raise

            finally:
                # try 블록 이후에 원래의 implicit_wait 값으로 복원
                self.driver.implicitly_wait(self.implicit_wait)

    def __lr_scroll_by_amount(self, location, xpath, scroll_number, scroll_amount):
        """

        입력된 횟수만큼 좌우 스와이프
        :param (str) location : 스크롤하려는 방향 / 1: 오른쪽에서 왼쪽으로 스와이프 / 2: 왼쪽에서 오른쪽으로 스와이프
        :param (str) xpath: 기준점으로 삼는 요소
        :param (int) scroll_amount: 한번 스크롤시 이동하는 정도(1~10 사이에서 결정하며 숫자가 클수록 많이 이동)
        :return: 없음
        :example: __lr_scroll_for_find_element(self,"1",xpath,2,3) # 입력된 횟수만큼 좌우 스와이프 반복

        """

        size = self.driver.get_window_size()
        width = size['width']
        scroll_count = 0
        element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        loc = element.location
        new_x = loc['x']
        new_y = loc['y']

        k = (width / 20) * scroll_amount

        for _ in range(scroll_number):
            if location == "1":
                self.driver.swipe(width / 2, new_y, width / 2 - k, new_y)
            elif location == "2":
                self.driver.swipe(width / 2, new_y, width / 2 + k, new_y)
            else:
                print("#", "스와이프할 방향을 지정해주세요.")
                raise

    def __webview_xpath_select(self, xpath):
        """gmarket_regression_python_amapp_page

        웹뷰로 변경 후, 해당 xpath 찾기
        :param (str) xpath: 찾으려는 요소
        :example: __webview_xpath_select(self, xpath)
        """

        runtext = 'webView 요소 찾음'
        print(self.driver.contexts)  # 컨텍스트 리스트 확인
        webview = self.driver.contexts[1]  # 웹뷰 컨텍스트 변수 지정
        self.driver.switch_to.context(webview)  # 웹뷰 컨텍스트로 전환
        print("Switching to context:", webview)
        print(self.driver.window_handles)  # 웹뷰 윈도우 전체 핸들 출력
        print(self.driver.current_window_handle)  # 웹뷰 윈도우 현재 핸들 출력

        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
            try:
                # 특정 try 블록 전에 implicit_wait를 10초로 설정
                self.driver.implicitly_wait(10)
                print("self.driver.window_handles:", self.driver.window_handles)
                element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, xpath)))
                print(f"요소 객체 찾음: {handle}")
                break
            except:
                print(f"요소 객체 못찾음: {handle}")
                continue
            finally:
                # try 블록 이후에 원래의 implicit_wait 값으로 복원
                self.driver.implicitly_wait(15)

        if 'element' in locals():
            element.click()
            time.sleep(5)
            self.driver.switch_to.context('NATIVE_APP')
            time.sleep(3)
            print("#", runtext)
        else:
            print("요소 객체를 찾지 못했습니다.")
            self.driver.switch_to.context('NATIVE_APP')

    def __webview_xpath_validation(self, xpath, validation):
        """gmarket_regression_python_amapp_page

        웹뷰로 변경 후, 해당 xpath 의 값과 실제 기대결과 값과 비교
        :param (str) xpath: 찾으려는 요소
        :example: __webview_xpath_select(self, xpath)
        """

        runtext = 'webView 요소 찾음'
        print(self.driver.contexts)  # 컨텍스트 리스트 확인
        webview = self.driver.contexts[1]  # 웹뷰 컨텍스트 변수 지정
        print("Available contexts:", self.driver.contexts)
        print("Switching to context:", webview)
        self.driver.switch_to.context(webview)  # 웹뷰 컨텍스트로 전환
        print(self.driver.window_handles)  # 웹뷰 윈도우 전체 핸들 출력
        print(self.driver.current_window_handle)  # 웹뷰 윈도우 현재 핸들 출력

        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
            try:
                # 특정 try 블록 전에 implicit_wait를 10초로 설정
                self.driver.implicitly_wait(10)
                print("self.driver.window_handles:", self.driver.window_handles)
                time.sleep(5)
                element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, xpath)))
                value=element.text
                print(f"요소 객체 찾음: {handle}")
                break
            except:
                print(f"요소 객체 못찾음: {handle}")
                continue
            finally:
                # try 블록 이후에 원래의 implicit_wait 값으로 복원
                self.driver.implicitly_wait(15)
        self.driver.switch_to.context('NATIVE_APP')
        assert_that(value).is_in(validation)
        print("#", runtext)

    def __webview_xpath_find_elements(self, xpath):
        """gmarket_regression_python_amapp_page

        웹뷰로 변경 후, 해당 xpath 찾기
        :param (str) xpath: 찾으려는 요소
        :example: __webview_xpath_select(self, xpath)
        """

        runtext = 'webView 요소 찾음'
        print(self.driver.contexts)  # 컨텍스트 리스트 확인
        webview = self.driver.contexts[1]  # 웹뷰 컨텍스트 변수 지정
        self.driver.switch_to.context(webview)  # 웹뷰 컨텍스트로 전환
        print(self.driver.window_handles)  # 웹뷰 윈도우 전체 핸들 출력
        print(self.driver.current_window_handle)  # 웹뷰 윈도우 현재 핸들 출력

        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
            try:
                # 특정 try 블록 전에 implicit_wait를 10초로 설정
                self.driver.implicitly_wait(10)
                print("self.driver.window_handles:", self.driver.window_handles)
                element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
                print(f"요소 객체 찾음: {handle}")
                return element
                break
            except:
                print(f"요소 객체 못찾음: {handle}")
                raise
            finally:
                # try 블록 이후에 원래의 implicit_wait 값으로 복원
                self.driver.implicitly_wait(15)

        self.driver.switch_to.context('NATIVE_APP')

    def __event_popup_all_close(self):
        """
        팝업 모두 닫기
        :param : 없음
        :example: __webview_xpath_select(self)
        """
        time.sleep(10)
        self.driver.implicitly_wait(5)
        runtext = 'MyG > 빅스 초특가 팝업 닫기'
        print("#", runtext, "시작")
        try:
            xpath = '//android.widget.RelativeLayout[@content-desc="닫기"]/android.widget.ImageView'
            element = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            element.click()
        except:
            print("인증 경고 팝업 처리 > 빅스 초특가 팝업 없음")
        # 중복 쿠폰 & 멤버쉽 팝업 처리
        self.driver.implicitly_wait(5)
        runtext = '메인페이지 > 중복 쿠폰 & 멤버쉽 팝업 닫기'
        print("#", runtext, "시작")
        try:
            id = 'com.ebay.kr.gmarket:id/ivClose'
            element = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.ID, id)))
            element.click()
        except:
            print("메인페이지 > 중복 쿠폰 & 멤버쉽 팝업 노출 없음")

        print("#", runtext, "종료")
        # 빅스마일데이 이벤트 (에스파 PICK)
        self.driver.implicitly_wait(5)
        runtext = '메인페이지 > 빅스마일데이 이벤트 (에스파 PICK) 팝업 닫기'
        print("#", runtext, "시작")
        try:
            id = 'com.ebay.kr.gmarket:id/rlBottomAdClose'
            element = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.ID, id)))
            element.click()
        except:
            print("빅스마일데이 이벤트 (에스파 PICK) 팝업 노출 없음")

        # 빅스마일데이 이벤트 (에스파 PICK)
        self.driver.implicitly_wait(5)
        runtext = '메인페이지 > 빅스마일데이 이벤트 (에스파 PICK) 팝업 닫기'
        print("#", runtext, "시작")
        try:
            id = 'com.ebay.kr.gmarket:id/rlBottomAdClose'
            element = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.ID, id)))
            element.click()
            print("#", runtext, "종료")
        except:
            print("빅스마일데이 이벤트 (에스파 PICK) 팝업 노출 없음")

    def analyse_image(self, xpath):
        os_version = platform.platform()
        if 'Windows' in os_version:
            pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        else:
            pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"
        # 이미지 로드
        try:
            element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            screenshot_base64 = element.screenshot_as_base64
            image_data = base64.b64decode(screenshot_base64)
            img = Image.open(BytesIO(image_data))
            img.save("loaded_image.png")  # 디버깅용 저장
            print("이미지 로드 완료")
        except Exception as e:
            print(f"이미지 로드 실패: {e}")

        try:
            recognized_text = pytesseract.image_to_string(img, config="--psm 13")
            print(f"인식된 텍스트: {recognized_text}")
            return recognized_text
        except Exception as e:
            print(f"텍스트 인식 실패: {e}")

    def analyse_webview_image(self, xpath):
        os_version = platform.platform()
        if 'Windows' in os_version:
            pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        else:
            pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

        print(self.driver.contexts)  # 컨텍스트 리스트 확인
        webview = self.driver.contexts[1]  # 웹뷰 컨텍스트 변수 지정
        time.sleep(5)
        self.driver.switch_to.context(webview)  # 웹뷰 컨텍스트로 전환
        print(self.driver.window_handles)  # 웹뷰 윈도우 전체 핸들 출력
        print(self.driver.current_window_handle)  # 웹뷰 윈도우 현재 핸들 출력

        # 이미지 로드
        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
            try:
                screenshot_base64 = self.driver.get_screenshot_as_base64()
                image_data = base64.b64decode(screenshot_base64)
                img = Image.open(BytesIO(image_data))
                img.save("img/smile_pay_all.png")  # 디버깅용 저장
                iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
                # print(f"Total iframes found: {len(iframes)}")
                # for index, iframe in enumerate(iframes):
                #     iframe_id = iframe.get_attribute('id')
                #     iframe_name = iframe.get_attribute('name')
                #     iframe_title = iframe.get_attribute('title')
                #     print(f"Iframe {index}: id='{iframe_id}', name='{iframe_name}', title='{iframe_title}'")
                last_three = xpath[-3:]
                numbers = re.findall(r'\d', last_three)
                num = ''.join(numbers)
                self.driver.switch_to.frame(iframes[0])
                print("Switched to iframe.")
                element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
                screenshot_base64 = element.screenshot_as_base64
                image_data = base64.b64decode(screenshot_base64)
                img = Image.open(BytesIO(image_data))
                img.save(f"img/number{num}.png")  # 디버깅용 저장
                img = cv2.imread(f"img/number{num}.png", cv2.IMREAD_GRAYSCALE)
                img = cv2.resize(img, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
                # img = cv2.Canny(img, 50, 150)
                img = cv2.medianBlur(img, 3)
                _, img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)

                img = cv2.convertScaleAbs(img, alpha=2, beta=0)  # 대비 강화
                cv2.imwrite(f"img/grey_number{num}.png", img)
                print("이미지 로드 완료")
            except Exception as e:
                print(f"이미지 로드 실패: {e}")
        custom_config = r'--oem 1 --psm 6 -c tessedit_char_whitelist=0123456789'
        try:
            recognized_text = pytesseract.image_to_string(img, config=custom_config)
            print(f"인식된 텍스트: {recognized_text}")
        except Exception as e:
            print(f"텍스트 인식 실패: {e}")

        self.driver.switch_to.default_content()
        print("Switched back to default content.")
        return recognized_text[:1]


    def __navigate_to_target_goods_page(self, goods_name):
        try:

            # 팝업 처리
            EtcFunction.__event_popup_all_close(self)

            # 지마켓메인 검색창 클릭
            runtext = '메인 페이지 > 검색창 클릭'
            print("#", runtext, "시작")
            time.sleep(5)
            self.driver.implicitly_wait(5)
            try:  # 빅스마일데이일 경우 검색창
                id = 'com.ebay.kr.gmarket:id/tvSearchBar'
                element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, id)))
                element.click()
            except:  # 빅스마일데이가 아닐경우 검색창
                id = 'com.ebay.kr.gmarket:id/rlSearchBar'
                element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, id)))
                element.click()
            print("#", runtext, "종료")

            # 지마켓메인 검색창 텍스트 입력
            runtext = '메인 페이지 > 검색창 텍스트 입력'
            print("#", runtext, "시작")
            id = "com.ebay.kr.gmarket:id/searchEditText"
            element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.ID, id)))
            element.send_keys(goods_name)
            print("#", runtext, "종료")

            # 지마켓메인 검색창 리턴
            runtext = '메인 페이지 > 검색창 텍스트 리턴'
            print("#", runtext, "시작")
            xpath = '//android.widget.ImageView[@content-desc="입력된 단어로 검색"]'
            element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            element.click()
            print("#", runtext, "종료")

            # # 지마켓메인 검색창 리턴
            # runtext = '메인 페이지 > 검색창 텍스트 리턴 > 입력 및 검색된 텍스트 비교'
            # print("#", runtext, "시작")
            # id = "com.ebay.kr.gmarket:id/searchKeyword"
            # element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, id)))
            # value = element.text
            # assert_that(value).is_in(goods_name)
            # print("#", runtext, "종료")

            # 지마켓메인 SRP 상품 클릭
            runtext = '메인 페이지 > 검색 > SRP 상품 클릭'
            print("#", runtext, "시작")
            time.sleep(10)
            id = "com.ebay.kr.gmarket:id/clCardContainer"
            element = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.ID, id)))
            element.click()
            print("#", runtext, "종료")

            # 빅스 초특가 팝업 처리
            EtcFunction.__event_popup_all_close(self)

        except Exception as e:
            print('Order Test Error', e)
            raise


    def input_login_account_type(self, use_type):
        """

        Gmarket 회원 타입별 로그인 진행
        :param (int) use_type: 1 : 사용 안함, 2: 사용
        :param (str) login_type: 1 : 자동화 계정으로 로그인 / 2 : 직접 입력하여 로그인
        :param (str) id_type: 자동 로그인 시 자동화 계정 타입
        :param (str) args[0]: 수동 로그인 시 계정 명
        :param (str) args[1]: 수동 로그인 시 계정 비밀번호

        :return: 없음
        :example:
        자동화 계정 로그인 시 : common_page_param.input_login_account_type(2,"1","일반회원")
        수동 계정 로그인 시 : common_page_param.input_login_account_type(2,"2","수동 로그인 계정 명","수동 로그인 계정 비밀번호")

        """

        if use_type == 2:
            # 로그인 버튼 클릭
            runtext = '로그인 버튼 클릭'
            print("#", runtext, "시작")
            id = "com.ebay.kr.gmarket:id/clSubTitle"
            element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, id)))
            element.click()
            print("#", runtext, "종료")


            runtext = 'log_on_page > 계정 입력'
            print("#", runtext, "시작")
            xpath = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.view.View[1]/android.view.View[1]/android.widget.EditText'
            element = WebDriverWait(self.driver, 40).until(EC.presence_of_element_located((By.XPATH, xpath)))
            element.send_keys("cease2504")
            print("#", runtext, "종료")

            runtext = 'log_on_page > 비밀 번호 입력'
            print("#", runtext, "시작")
            xpath = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.view.View[1]/android.view.View[2]/android.widget.EditText'
            element = self.driver.find_element(By.XPATH, xpath)
            element.send_keys("1q2w3e4r!@")
            print("#", runtext, "종료")

            runtext = 'log_on_page > 로그인 버튼 클릭'
            print("#", runtext, "시작")
            xpath = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.widget.Button'
            element = self.driver.find_element(By.XPATH, xpath)
            element.click()
            print("#", runtext, "종료")

            time.sleep(10)

        else:
            print("#", "로그인 회원 타입 선택 없음")
            raise

    def smile_pay_num(self, use_type,*args):
        if use_type == 2:
            print("#", "ShoppingCart 1.7.1-2 Test Case 실행")
            # Given 초기화
            EtcFunction.__reset_given(self)

            EtcFunction.__navigate_to_target_goods_page(self,"3840412506")

            runtext = '메인페이지 > VIP 페이지 > 구매하기 버튼 클릭'
            print("#", runtext, "시작")
            time.sleep(1)
            xpath = '(//android.view.ViewGroup[@resource-id="com.ebay.kr.gmarket:id/clBtn"])[2]'
            element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            element.click()
            print("#", runtext, "종료")

            runtext = '메인페이지 > VIP 페이지 > 구매하기 클릭'
            print("#", runtext, "시작")
            time.sleep(3)
            xpath = '//android.widget.TextView[@content-desc="구매하기"]'
            element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            element.click()
            print("#", runtext, "종료")

            runtext = '메인페이지 > VIP 페이지 > 주문서 > 구매하기 클릭'
            print("#", runtext, "시작")
            time.sleep(20)
            # xpath = '//android.widget.Button[@text="15,000원 결제하기"]'
            # element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            # element.click()
            xpath ='//*[@class="button__total-price"]'
            EtcFunction.__webview_xpath_select(self, xpath)
            print("#", runtext, "종료")
            sm_num=[]
            for i in range(11):
                xpath = f'(//*[@class="KeyboardsNumbers__Grid__Item"])[{i+1}]'
                # xpath = f'#BaseContainer > div.css-ds1oq4 > div.KeyboardsNumbers__Grid > div:nth-child({i+1}) > button'
                value=EtcFunction.analyse_webview_image(self, xpath)
                value = value.replace('\n','')
                sm_num.append(value)
                self.driver.switch_to.context('NATIVE_APP')
            print(sm_num)

            runtext = '메인페이지 > VIP 페이지 > 주문서 > 구매하기 클릭 > 스마일페이 결제 비밀번호 입력'
            print("#", runtext, "시작")
            print(self.driver.contexts)  # 컨텍스트 리스트 확인
            webview = self.driver.contexts[1]  # 웹뷰 컨텍스트 변수 지정
            time.sleep(5)
            self.driver.switch_to.context(webview)  # 웹뷰 컨텍스트로 전환
            print(self.driver.window_handles)  # 웹뷰 윈도우 전체 핸들 출력
            print(self.driver.current_window_handle)  # 웹뷰 윈도우 현재 핸들 출력

            for handle in self.driver.window_handles:
                self.driver.switch_to.window(handle)

                iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
                # print(f"Total iframes found: {len(iframes)}")
                # for index, iframe in enumerate(iframes):
                #     iframe_id = iframe.get_attribute('id')
                #     iframe_name = iframe.get_attribute('name')
                #     iframe_title = iframe.get_attribute('title')
                #     print(f"Iframe {index}: id='{iframe_id}', name='{iframe_name}', title='{iframe_title}'")
                self.driver.switch_to.frame(iframes[0])

                sec_num = ""
                for i in sec_num:
                    x= sm_num.index(i)+1
                    xpath = f'(//*[@class="KeyboardsNumbers__Grid__Item"])[{x}]'
                    element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
                    element.click()
            print("#", runtext, "종료")
            self.driver.switch_to.context('NATIVE_APP')

            sm_num = ",".join(sm_num)
            return sm_num
