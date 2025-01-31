import requests
import base64
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs
import time
import xml.etree.ElementTree as ET
import xml.dom.minidom
from datetime import datetime, timedelta


class BlingAuth:
    def __init__(self):
        self.client_id = ""
        self.client_secret = ""
        self.redirect_uri = ""
        self.auth_url = "https://bling.com.br/Api/v3/oauth/authorize"
        self.token_url = "https://bling.com.br/Api/v3/oauth/token"
        self.state = "21"
        self.username = ""
        self.password = ""
        self.access_token = None

    def check_url_change(self, driver, original_url: str, max_attempts: int = 100, delay: float = 0.1) -> str:
        """
        监控URL变化直到检测到重定向
        """
        for _ in range(max_attempts):
            current_url = driver.current_url
            if current_url != original_url and 'bodor.cn' in current_url:
                return current_url
            time.sleep(delay)
        return None

    def get_authorization_code(self):
        """使用Selenium自动获取授权码"""
        print("\n配置浏览器选项...")
        auth_params = {
            "response_type": "code",
            "client_id": self.client_id,
            "state": self.state,
            "redirect_uri": self.redirect_uri
        }
        auth_url = f"{self.auth_url}?{'&'.join(f'{k}={v}' for k, v in auth_params.items())}"

        chrome_options = webdriver.ChromeOptions()
        chrome_options.page_load_strategy = 'none'
        chrome_options.add_argument('--headless')  # 启用无头模式（Headless Mode）。
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')

        print("启动浏览器...")
        driver = webdriver.Chrome(options=chrome_options)
        try:
            print("访问授权...")
            driver.get(auth_url)
            original_url = driver.current_url

            print("\n获取授权中（1/4）...")
            username_input = None
            for _ in range(10):
                try:
                    username_input = WebDriverWait(driver, 1).until(
                        EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/form/div[2]/input"))
                    )
                    break
                except:
                    time.sleep(1)
                    continue

            if not username_input:
                raise Exception("登录页面加载超时")

            print("\n获取授权中（2/4）...")
            password_input = driver.find_element(By.XPATH, "/html/body/div/div/div/form/div[3]/input")
            login_button = driver.find_element(By.XPATH, "/html/body/div/div/div/form/div[6]/button")

            username_input.send_keys(self.username)
            password_input.send_keys(self.password)

            print("获取授权中（3/4）...")
            login_button.click()

            print("获取授权中（4/4）...")
            current_url = self.check_url_change(driver, original_url)
            if not current_url:
                raise Exception("URL未发生预期变化")

            print(f"授权URL: {current_url}")

            parsed_url = urlparse(current_url)
            query_params = parse_qs(parsed_url.query)
            auth_code = query_params.get('code', [None])[0]

            if not auth_code:
                print("警告：未能在URL中找到授权码")

            return auth_code

        finally:
            print("结束...")
            driver.quit()

    def get_access_token(self, auth_code: str) -> dict:
        """使用授权码获取访问令牌"""
        print("准备获取访问令牌...")
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": self.redirect_uri
        }

        print("发送令牌请求...")
        response = requests.post(
            self.token_url,
            data=data,
            headers=headers
        )

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"获取访问令牌失败: {response.text}")


def main():
    auth = BlingAuth()

    try:
        print("正在获取授权码...")
        auth_code = auth.get_authorization_code()
        if not auth_code:
            raise Exception("无法获取授权码")

        print(f"获取到的授权码: {auth_code}")

        print("正在获取访问令牌...")
        token_info = auth.get_access_token(auth_code)
        print("\n成功获取访问令牌:")
        expires_in = token_info.get('expires_in')
        expires_in = datetime.now() + timedelta(seconds=expires_in)
        print(f"Access Token: {token_info.get('access_token')}")
        print(f"Token Type: {token_info.get('token_type')}")
        print(f"Expires In: {expires_in}")

        # 确保只保存 refresh_token
        refresh_token = token_info.get('refresh_token', None)
        if refresh_token:
            print(f"Refresh Token: {refresh_token}")

        # 将 expires_in 转换为可读的时间格式
        expires_in_str = expires_in.strftime('%Y-%m-%d %H:%M:%S')

        # -----保存xml认证文件到本地-----
        # 创建 XML 根元素
        root = ET.Element("TokenInfo")

        # 添加子元素
        for key, value in token_info.items():
            # 过滤掉不需要的字段（比如scope）
            if key == 'expires_in':
                value = expires_in_str  # 替换为格式化后的日期时间
            if key != 'scope':  # 排除 scope 字段
                child = ET.SubElement(root, key)
                child.text = str(value)

        # 生成 XML 字符串
        rough_string = ET.tostring(root, encoding="utf-8")

        # 使用 minidom 进行格式化
        dom = xml.dom.minidom.parseString(rough_string)
        pretty_xml = dom.toprettyxml(indent="    ")  # 设置缩进为 4 个空格

        # 保存格式化 XML 到本地文件
        xml_filename = "token_info.xml"
        with open(xml_filename, "w", encoding="utf-8") as f:
            f.write(pretty_xml)

        print(f"格式化 XML 文件已保存：{xml_filename}")
    except Exception as e:
        print(f"错误: {str(e)}")


if __name__ == "__main__":
    main()
