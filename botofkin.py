import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
from bs4 import BeautifulSoup

# Hàm gửi tin nhắn cập nhật thông tin thời tiết
async def send_periodic_weather_info(context):
    while True:
        await asyncio.sleep(1800)  # Chờ 300 giây (05 phút)
        weather_info, weather_images = get_weather_info_with_images()
        group_id = -4114009569  # ID của nhóm, thay thế bằng ID thực tế của nhóm
        await send_weather_info_with_images(context, group_id, weather_info, weather_images)

# Hàm lấy thông tin thời tiết từ trang web kèm theo hình ảnh và icon
def get_weather_info_with_images():
    weather_info = []
    weather_images = []
    response = requests.get('https://dubaothoitiet.info/thoi-tiet/thoi-tiet-da-nang')
    soup = BeautifulSoup(response.text, 'html.parser')
    mydivs = soup.find_all('div', class_='col-lg-8')
    for div in mydivs:
        weather_info.append(div.text.strip())
        images = div.find_all('img')  # Tìm tất cả các thẻ <img> trong div
        for image in images:
            weather_images.append(image['src'])  # Lấy đường dẫn hình ảnh từ thuộc tính 'src'
    return weather_info, weather_images

# Hàm gửi tin nhắn thời tiết kèm theo hình ảnh và icon
async def send_weather_info_with_images(context, group_id, weather_info, weather_images):
    message = "\n".join(weather_info)
    await context.bot.send_message(chat_id=group_id, text=f'Thông tin thời tiết Đà Nẵng:\n{message}')
    for image_url in weather_images:
        await context.bot.send_photo(chat_id=group_id, photo=image_url)
    await context.bot.send_message(chat_id=group_id, text="Xem chi tiết trên trang web: https://dubaothoitiet.info/thoi-tiet/thoi-tiet-da-nang")

# Xử lý lệnh /hello
async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Xin chào {update.effective_user.first_name}')

# Khởi tạo ứng dụng
app = ApplicationBuilder().token("6656439753:AAFYIEP_YIU3HX7-Igg4BtlTsz17rs-4BSE").build() 

# Thêm xử lý lệnh
app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("weather", send_periodic_weather_info))


# Lập lịch gửi tin nhắn cập nhật thông tin mỗi 30 phút
app.job_queue.run_repeating(send_periodic_weather_info, interval=1800, first=0)


# Khởi động ứng dụng
app.run_polling()

