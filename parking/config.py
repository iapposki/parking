import os
import dotenv

dotenv.load_dotenv()

booking_timeout_interval = os.getenv("TIMEOUT_BOOKING")
