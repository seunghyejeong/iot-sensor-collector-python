import unittest
from main import app
from unittest.mock import Mock

class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_acceleration_endpoint(self):
        # /acceleration 엔드포인트에 POST 요청 보내기
        response = self.app.post('/acceleration', json={"x": 1.0, "y": 2.0, "z": 3.0})
        # 응답 확인
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Acceleration Data received", response.data)

    def test_location_endpoint(self):
        # /location 엔드포인트에 POST 요청 보내기
        response = self.app.post('/location', json={"latitude": 37.123, "longitude": -122.456})
        
        # 응답 확인
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Location Data received", response.data)

# 클라이언트 연결테스트 
    def test_mqtt_client_connection_status(self):
        # Mock MQTT client 생성
        mock_mqtt_client = Mock()

        # IsConnected 메서드가 True를 반환하도록 설정
        mock_mqtt_client.IsConnected.return_value = True

        # Flask 애플리케이션에 모의(Mock) 객체 연결
        app.mqtt_client = mock_mqtt_client

        # /acceleration 엔드포인트에 POST 요청 보내기
        response = self.app.post('/acceleration', json={"x": 1.0, "y": 2.0, "z": 3.0})

        # 응답 확인
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Acceleration Data received", response.data)


    # 에러 핸들링 
    def test_mqtt_connection_error_handling(self):
        # Mock MQTT client 생성
        mock_mqtt_client = Mock()

        # Connect 메서드가 에러를 반환하도록 설정
        mock_token = Mock()
        mock_token.Wait.return_value = False  # 연결 실패를 시뮬레이션
        mock_token.Error.return_value = "Connection error"
        mock_mqtt_client.Connect.return_value = mock_token

        # Flask 애플리케이션에 모의(Mock) 객체 연결
        app.mqtt_client = mock_mqtt_client

        # /acceleration 엔드포인트에 POST 요청 보내기
        response = self.app.post('/acceleration', json={"x": 1.0, "y": 2.0, "z": 3.0})

        # 응답 확인
        self.assertEqual(response.status_code, 500)
        self.assertIn(b"Failed to connect to MQTT broker", response.data)


    # 데이터 유효성 테스트 
    def test_acceleration_endpoint_invalid_data(self):
        # /acceleration 엔드포인트에 잘못된 JSON 데이터를 포함하는 POST 요청 보내기
        response = self.app.post('/acceleration', json={"x": "-3", "y": 2.0, "z": 3.0})

        # 응답 확인
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Invalid data format", response.data)

if __name__ == '__main__':
    unittest.main()
