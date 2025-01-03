# Bling OAuth 2.0 授权代码示例

本项目是一个示例代码，演示如何通过 OAuth 2.0 授权码模式，获取 [Bling](https://bling.com.br/) API 的访问令牌。代码主要使用 Python 实现，提供了完整的授权流程和交互逻辑。

## 功能特点

- **生成授权 URL**：引导用户前往授权页面完成登录和授权。
- **提取授权码**：从用户提供的回调 URL 中提取授权码。
- **获取访问令牌**：通过授权码向 Bling 授权服务器请求访问令牌。
- **自动打开浏览器**：简化用户授权流程。

## 文件结构

```
├── BlingAuth.py   # 主代码文件，包含 OAuth 逻辑
├── README.md      # 使用说明
└── requirements.txt # 项目依赖
```

## 环境要求

- Python 3.7 及以上
- 依赖包（见 `requirements.txt`）

## 安装步骤

1. 克隆项目到本地：

   ```bash
   git clone https://github.com/XiaobaiBC/bling-oauth-example.git
   cd bling-oauth-example
   ```

2. 安装依赖：

   ```bash
   pip install -r requirements.txt
   ```

3. 修改代码中的 `client_id`、`client_secret` 和 `redirect_uri` 为你的实际值。

## 使用方法

1. 运行代码：

   ```bash
   python BlingAuth.py
   ```

2. 程序会生成授权 URL，并自动在浏览器中打开。若未自动打开，请手动复制 URL 到浏览器访问。

3. 用户完成授权后，Bling 会将用户重定向到你的 `redirect_uri`，例如：

   ```
   https://www.***.com/?code=abc123&state=21
   ```

4. 将完整的回调 URL 粘贴回程序。

5. 程序会提取授权码，并尝试获取访问令牌。如果成功，将输出以下信息：

   ```
   成功获取访问令牌:
   Access Token: your_access_token
   Refresh Token: your_refresh_token
   Token Type: Bearer
   Expires In: 3600 seconds
   ```

## 注意事项

1. **安全性**：
   - 请勿将 `client_secret` 硬编码在代码中，建议使用环境变量或配置文件存储敏感信息。
   - 请确保 `redirect_uri` 与应用配置的回调地址一致。

2. **错误处理**：
   - 如果返回错误，请检查授权码是否正确，以及网络是否正常。
   - Bling API 响应的状态码和错误信息可以帮助定位问题。

3. **刷新令牌**：
   - 本代码未实现刷新令牌逻辑，建议在生产环境中补充。

## 依赖包

- `requests`：用于发送 HTTP 请求。
- `urllib.parse`：用于解析 URL。
- `webbrowser`：用于打开浏览器。

安装依赖：

```bash
pip install requests
```

## 示例截图

运行流程示例：

1. 授权 URL 输出与自动打开：

   ```
   授权URL:
   https://bling.com.br/Api/v3/oauth/authorize?response_type=code&client_id=your_client_id&redirect_uri=https://www.bodor.cn/&state=21
   ```

   ![授权页面示例](https://via.placeholder.com/800x400.png)

2. 成功获取访问令牌：

   ```
   成功获取访问令牌:
   Access Token: abcdefghijklmnopqrstuvwxyz123456
   Refresh Token: uvwxyz987654321
   Token Type: Bearer
   Expires In: 3600 seconds
   ```

## 许可协议

本项目采用 [MIT License](LICENSE) 开源许可证。你可以自由使用、修改和分发，但请保留原作者信息。

## 联系方式

如有任何问题或建议，欢迎通过以下方式联系：

- 作者邮箱：zhengzaiga@gmail.com
