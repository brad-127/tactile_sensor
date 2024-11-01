import serial
import time
import sys
import os
import csv

# シリアルポートの設定 (例: '/dev/ttyACM0' または 'COM3' など)
port = '/dev/ttyACM0'  # 必要に応じて適切なポートに変更
baud_rate = 9600
timeout = 1  # ポートを開いたときのタイムアウト時間 (秒)
wait_time = 0.2  # 書き込み周期
port_num = 8 # portの数
threshold = 30 #しきい値

# ./dataディレクトリが存在しない場合は作成
if not os.path.exists('./data'):
    os.makedirs('./data')

# スクリプトの実行開始時の時間でログファイル名を生成
start_time = time.strftime("%Y%m%d_%H%M%S")  # 年月日_時分秒の形式
log_file = f"./data/{start_time}.csv"

try:
    # シリアルポートをオープン
    ser = serial.Serial(port, baud_rate, timeout=timeout)
    print(f"Connected to {port} at {baud_rate} baud.")
except serial.SerialException as e:
    print(f"Failed to connect to {port}: {e}")
    sys.exit(1)

# CSVファイルを開く
with open(log_file, 'a', newline='') as f:
    writer = csv.writer(f)
    # ヘッダーを書き込む
    header = [f'Sensor{i}' for i in range(1, port_num+1)] + ['Timestamp']  # センサー1からport_numまでのヘッダー
    writer.writerow(header)

    try:
        while True:
            if ser.in_waiting > 0:
                # シリアルからのデータを読み取る
                line = ser.readline().decode('utf-8', errors='ignore').rstrip()
                # 受信したデータをカンマで分割してリストにする
                sensor_data = line.split(',')
                # データがport_num個のセンサーからのものであることを確認
                if len(sensor_data) == port_num:
                    # 現在の時刻を取得 (YYYY-MM-DD HH:MM:SS.milliseconds形式)
                    timestamp_ = time.time()
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp_)) + f".{int((timestamp_ % 1) * 1000):03d}"

                    data_array = [int(data.strip()) for data in sensor_data]

                    # しきい値を上回れば1、下回れば0を格納
                    threshold_array = [1 if value > threshold else 0 for value in data_array]

                    # 出力を消去して新しいデータを表示
                    print(f"\r{timestamp}: {data_array}", end="")  # 現在のタイムスタンプとセンサーのデータを表示
                    output_line = threshold_array + [timestamp]   # タイムスタンプを追加
                    writer.writerow(output_line)  # CSVファイルに書き込む
                    f.flush()  # ファイルへの書き込みを即時に反映
            time.sleep(wait_time)  # CPU使用率を下げるための待機
    except KeyboardInterrupt:
        # Ctrl+Cで終了した場合
        print("\nProgram interrupted. Exiting...")
    finally:
        # シリアルポートを閉じる
        ser.close()
        print(f"Serial port {port} closed.")
