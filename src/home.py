from src.base_pages.base import *

class HomePage():

    implicit_wait = 300
    TIMEOUT = 30

    def __init__(self, driver):
        self.driver = driver
        self.driver.implicitly_wait(self.implicit_wait)

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
        finally:
            # try 블록 이후에 원래의 implicit_wait 값으로 복원
            self.driver.implicitly_wait(self.implicit_wait)
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
        finally:
            # try 블록 이후에 원래의 implicit_wait 값으로 복원
            self.driver.implicitly_wait(self.implicit_wait)
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
        finally:
            # try 블록 이후에 원래의 implicit_wait 값으로 복원
            self.driver.implicitly_wait(self.implicit_wait)
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
        finally:
            # try 블록 이후에 원래의 implicit_wait 값으로 복원
            self.driver.implicitly_wait(self.implicit_wait)

    def __select_home_section(self, section_name):

        """

        메인 페이지 > 해당 섹션 진입
        :param(str): section_name
        :return 없음
        :example: HomeGnbPageParam.__select_home_section(self,section_name)

        """
        # Given 초기화
        runtext = '앱 재실행 - Given 초기화'
        print("#", runtext, "시작")
        app_package = 'com.ebay.kr.gmarket'
        app_activity = 'com.ebay.kr.gmarket.eBayKoreaGmarketActivity'
        self.driver.start_activity(app_package=app_package, app_activity=app_activity)
        print("#", runtext, "종료")

        HomePage.__event_popup_all_close(self)

        # 메인 페이지 > 탭+버튼 클릭
        time.sleep(2)
        runtext = '메인 페이지 > 탭+버튼 클릭'
        print("#", runtext, "시작")
        xpath = '//android.widget.ImageButton[@content-desc="메뉴 편집"]'
        element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element.click()
        print("#", runtext, "종료")

        xpath = '//android.widget.TextView[@resource-id="com.ebay.kr.gmarket:id/tvTitle" and @text="{0}"]'.format(
            section_name)
        HomePage.__scroll_mobile_app(self, "1", xpath, 3, 30)

        runtext = '해당섹션 클릭'
        print("#", runtext, "시작")
        xpath = '//android.widget.TextView[@resource-id="com.ebay.kr.gmarket:id/tvTitle" and @text="{0}"]'.format(
            section_name)
        time.sleep(10)
        element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element.click()
        print("#", runtext, "종료")

    url = 'https://signinssl-dev.gmarket.co.kr/'
    def input_move_login_screen(self, use_type):
        """

        Gmarket 로그인 화면 이동 (팝업 처리 및 로그인 화면 이동)
        :param: 없음
        :return: 없음
        :example: common_page_param.input_move_login_screen(2)

        """
        url = 'https://signinssl-dev.gmarket.co.kr/'

        if use_type == 2:
            self.driver.get(self.url)
            runtext = 'log_on_page > 계정 입력'
            id = "typeMemberInputId"
            element = self.driver.find_element(By.ID, id)
            element.send_keys("cease2505")
            print("#", runtext)

            runtext = 'log_on_page > 비밀 번호 입력'
            id = "typeMemberInputPassword"
            element = self.driver.find_element(By.ID, id)
            element.send_keys("test1004")
            time.sleep(2)
            print("#", runtext)

            runtext = 'log_on_page > 로그인 버튼 클릭'
            id = "btn_memberLogin"
            element = self.driver.find_element(By.ID, id)
            element.click()
            print("#", runtext)

            runtext = 'vip 페이지로 이동'
            vip_url = 'http://item-dev.gmarket.co.kr/item?goodscode='
            goods_number = "1102941477"
            self.driver.get(vip_url + str(goods_number))  # 브라우저 URL 불러오기
            print("#", runtext)

            runtext = 'vip 페이지 > 구매하기 클릭'
            id = 'coreInsOrderBtn'
            element = self.driver.find_element(By.ID, id)
            element.click()
            print("#", runtext)

            runtext = '주문서 > 구매하기 클릭'

            xpath = '//*[@id="content"]/div/div[2]/div/div[2]/div/div/button'
            element = self.driver.find_element(By.XPATH, xpath)
            element.click()
            time.sleep(5)
            print("얼럿창 확인")
            try:
                alert = self.driver.switch_to.alert
                alert.accept()
                time.sleep(5)
                xpath = '//*[@id="content"]/div/div[2]/div/div[2]/div/div/button'
                element = self.driver.find_element(By.XPATH, xpath)
                element.click()
            except:
                print("얼럿창 미노출")
            print("#", runtext)
        else:
            print("#", "권한 팝업 처리하지 않음")


    def ss_1_2_1_1(self, use_type, *args):
        """
        1.2.1-1) 베스트 > 기본기능
        :param (int) use_type: 사용 여부 (1: 미사용 / 2:사용)
        :param (list) args[0]: 위로 가기 버튼
        :param (str) args[1]: 전체 베스트 버튼
        :return: 없음
        :example: gmarket_regression_vip_page_param.ss_1_2_1_1(2,*args)
        """

        if use_type == 2:
            print("#", "LP 1.2.1-1 Test Case 실행")
            runtext = '메인페이지 > 베스트 섹션 으로 이동'
            print("#", runtext, "시작")
            HomePage.__select_home_section(self,"베스트")
            print("#", runtext, "종료")


            # runtext = '메인페이지 >베스트 섹션 탑버튼 노출 확인'
            # time.sleep(2)
            # print("#", runtext, "시작")
            # id = "com.ebay.kr.gmarket:id/topButton"
            # HomePage.__scroll_mobile_app_type(self, "1", "id", id, 5, 10)
            # element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, id)))
            # value = element.get_attribute('content-desc')
            # assert_that(value).is_in(args[0])  # 위로 가기
            # print("#", runtext, "종료")
            #
            # runtext = '메인페이지 >베스트 섹션 탑버튼 클릭시 동작 확인'
            # time.sleep(2)
            # print("#", runtext, "시작")
            # element.click()
            # xpath = '//android.widget.TextView[@resource-id="com.ebay.kr.gmarket:id/tv_title" and @text="전체 베스트"]'
            # HomePage.__scroll_mobile_app(self, "2", xpath, 10, 10)
            # element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            # value = element.text
            # assert_that(value).is_in(args[1])  # 전체 베스트
            # print("#", runtext, "종료")
            #
            # # 책&문화 > 새로고침 동작 확인
            # runtext = '책&문화 > 새로고침 동작 확인'
            # print("#", runtext, "시작")
            # xpath = '//android.widget.TextView[@resource-id="com.ebay.kr.gmarket:id/tv_title" and @text="전체 베스트"]'
            # HomePage.__scroll_mobile_app(self, "2", xpath, 10, 10)
            # element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            # value = element.text
            # assert_that(value).is_in(args[1])  # 전체 베스트
            # print("#", runtext, "종료")


        else:
            print("#", "BEST 1.2.1-1 Test Case 실행 생략")

    def ss_1_2_1_4(self, use_type, *args):
        """
        1.2.1-1) 베스트 > 기본기능
        :param (int) use_type: 사용 여부 (1: 미사용 / 2:사용)
        :param (list) args[0]: 위로 가기 버튼
        :param (str) args[1]: 전체 베스트 버튼
        :return: 없음
        :example: gmarket_regression_vip_page_param.ss_1_2_1_1(2,*args)
        """

        if use_type == 2:
            print("#", "LP 1.2.1-4 Test Case 실행")
            runtext = '메인페이지 > 베스트 섹션 으로 이동'
            print("#", runtext, "시작")
            HomePage.__select_home_section(self, "베스트")
            print("#", runtext, "종료")

            HomePage.__lr_scroll_for_find_element()

            runtext = '메인페이지 >베스트 섹션 탑버튼 노출 확인'
            time.sleep(2)
            print("#", runtext, "시작")
            xpath = "//android.widget.TextView[@resource-id=\"com.ebay.kr.gmarket:id/tvIndex\" and @text=\"10\"]"
            HomePage.__scroll_mobile_app(self, "1", xpath, 4, 20)
            xpath = '//android.widget.GridView[@resource-id="com.ebay.kr.gmarket:id/list"]/android.view.ViewGroup/android.widget.ImageView'
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            print("#", runtext, "종료")

        else:
            print("#", "BEST 1.2.1-1 Test Case 실행 생략")
