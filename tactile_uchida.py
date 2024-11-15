import serial
import time
import sys
import os
import csv

class SerialLogger:
    def __init__(self, port, baud_rate=9600, timeout=1, port_num=8, threshold=30, wait_time=0.2):
        """
        シリアルポートからデータを読み取り、CSVに保存するクラス
        
        :param port: シリアルポートのパス（例: '/dev/ttyACM0' または 'COM3'）
        :param baud_rate: ボーレート（デフォルト: 9600）
        :param timeout: タイムアウト時間（デフォルト: 1秒）
        :param port_num: センサーの数（デフォルト: 8）
        :param threshold: しきい値（デフォルト: 30）
        :param wait_time: データ取得の待機時間（デフォルト: 0.2秒）
        """
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.port_num = port_num
        self.threshold = threshold
        self.wait_time = wait_time

        # ./dataディレクトリが存在しない場合は作成
        if not os.path.exists('./data'):
            os.makedirs('./data')

        # ログファイル名の生成
        start_time = time.strftime("%Y%m%d_%H%M%S")  # 年月日_時分秒の形式
        self.log_file = f"./data/{start_time}.csv"

        # シリアルポートをオープン
        try:
            self.ser = serial.Serial(self.port, self.baud_rate, timeout=self.timeout)
            print(f"Connected to {self.port} at {self.baud_rate} baud.")
        except serial.SerialException as e:
            print(f"Failed to connect to {self.port}: {e}")
            sys.exit(1)

        # CSVファイルを開く
        self.f = open(self.log_file, 'a', newline='')
        self.writer = csv.writer(self.f)

        # ヘッダーを書き込む
        header = [f'Sensor{i}' for i in range(1, self.port_num+1)] + ['Timestamp']  # センサー1からport_numまでのヘッダー
        self.writer.writerow(header)

    def process_data(self):
        """シリアルデータを処理してCSVに書き込む"""
        try:
            while True:
                if self.ser.in_waiting > 0:
                    # シリアルからのデータを読み取る
                    line = self.ser.readline().decode('utf-8', errors='ignore').rstrip()
                    # 受信したデータをカンマで分割してリストにする
                    sensor_data = line.split(',')
                    # データがport_num個のセンサーからのものであることを確認
                    if len(sensor_data) == self.port_num:
                        # 現在の時刻を取得 (YYYY-MM-DD HH:MM:SS.milliseconds形式)
                        timestamp_ = time.time()
                        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp_)) + f".{int((timestamp_ % 1) * 1000):03d}"

                        data_array = [int(data.strip()) for data in sensor_data]

                        # しきい値を上回れば1、下回れば0を格納
                        threshold_array = [1 if value > self.threshold else 0 for value in data_array]

                        # 出力を消去して新しいデータを表示
                        print(f"\r{timestamp}: {data_array}", end="")  # 現在のタイムスタンプとセンサーのデータを表示
                        output_line = threshold_array + [timestamp]   # タイムスタンプを追加
                        self.writer.writerow(output_line)  # CSVファイルに書き込む
                        self.f.flush()  # ファイルへの書き込みを即時に反映
                time.sleep(self.wait_time)  # CPU使用率を下げるための待機
        except KeyboardInterrupt:
            # Ctrl+Cで終了した場合
            print("\nProgram interrupted. Exiting...")
        finally:
            self.cleanup()

    def cleanup(self):
        """クリーンアップ処理"""
        # シリアルポートを閉じる
        self.ser.close()
        self.f.close()
        print(f"Serial port {self.port} closed.")

