import requests
import datetime

def get_suntime(city):
  """
  获取指定城市的日出和日落时间

  Args:
    city: 城市的英文名称

  Returns:
    一个字典，包含日出和日落时间
  """

  # 使用 API 密钥替换 `YOUR_API_KEY`
  url = f"https://api.sunrise-sunset.org/json?lat=37.386091&lng=-122.083851&date=2023-08-03&formatted=0&apiKey=YOUR_API_KEY"
  response = requests.get(url)
  data = response.json()

  sunrise = datetime.datetime.strptime(data["results"]["sunrise"], "%H:%M:%S")
  sunset = datetime.datetime.strptime(data["results"]["sunset"], "%H:%M:%S")

  return {"sunrise": sunrise, "sunset": sunset}
