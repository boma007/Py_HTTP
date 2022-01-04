#
# 前提
# pip install requests
#

import requests

    response = None
    for i in range(max_retries):
        try:
            response = requests.get(
                url=url, auth=basic_auth_param, proxies=proxy_param
            )  # 標準のリトライ数は0回
            response.raise_for_status() #200番台以外で例外を挙げる
            break
        except requests.exceptions.ConnectTimeout:
            logging.warning(f"{url} との接続確立中にタイムアウトしました。")
        except requests.exceptions.ReadTimeout:
            logging.warning(f"通信中の {url} からの応答でタイムアウトしました。")
        except requests.exceptions.ConnectionError as e:
            if any(
                [isinstance(arg, urllib3.exceptions.MaxRetryError) for arg in e.args]
            ):  # リトライのエラーは不要
                logging.warning(f"{url} へのHTTPリクエストに失敗しました。{i + 1}回目。")
            else:
                logging.warning(f"{url} へのHTTPリクエストに失敗しました。{i + 1}回目。e = {e}")

        if i + 1 != max_retries:
            logging.info(f"{retry_wait_time}秒後にリトライします。")
            time.sleep(retry_wait_time)

    else: # for文が回り切った場合の処理
        logging.info(f"合計{max_retries}回の {url} へのHTTPリクエストに全て失敗しました。")
        return None

    if response is not None:
        return response.content


    for i in range(max_retries):
        try:
            response = requests.post(url=url, json=params, verify=False, auth=basic_auth_param, proxies=proxy_param)
            response.raise_for_status()
            break
        except requests.exceptions.HTTPError:
            if response.status_code == 500:
                data = response.json()  # {'errors': [{'code': 999, 'message': 'Already registered: https://example.com}]}
                if "Already registered" in data["errors"][0]["message"]:
                    logging.warning(f"{url}は既に登録されています。")
                    break
        except requests.exceptions.ConnectTimeout:
            logging.warning(f"{url} との接続確立中にタイムアウトしました。")
        except requests.exceptions.ReadTimeout:
            logging.warning(f"通信中の {url} からの応答でタイムアウトしました。")
        except requests.exceptions.ConnectionError as e:
            if any(
                [isinstance(arg, urllib3.exceptions.MaxRetryError) for arg in e.args]
            ):  # リトライのエラーは不要
                logging.warning(f"{url} へのHTTPリクエストに失敗しました。{i + 1}回目。")
            else:
                logging.warning(f"{url} へのHTTPリクエストに失敗しました。{i + 1}回目。e = {e}")

        if i + 1 != max_retries:
            logging.info(f"{retry_wait_time}秒後にリトライします。")
            time.sleep(retry_wait_time)

    else:  # for文が回り切った場合の処理
        logging.info(f"合計{max_retries}回の {url} へのHTTPリクエストに全て失敗しました。")
        raise Exception(f"合計{max_retries}回の {url} へのHTTPリクエストに全て失敗しました。")
