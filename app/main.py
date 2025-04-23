from fastapi import FastAPI

from app.config import load_config
from app.models.models import Feedback, User, UserCreate, UserInfo

from .logger import logger


app = FastAPI()
# user = User(name="John Doe", id=1, age=20)
fake_users = [{"username": "vasya", "user_info": "любит колбасу"}, {"username": "katya", "user_info": "любит петь"}]
feedback_lst = []
db_users: list[UserCreate] = []

sample_product_1 = {"product_id": 123, "name": "Smartphone", "category": "Electronics", "price": 599.99}

sample_product_2 = {"product_id": 456, "name": "Phone Case", "category": "Accessories", "price": 19.99}

sample_product_3 = {"product_id": 789, "name": "Iphone", "category": "Electronics", "price": 1299.99}

sample_product_4 = {"product_id": 101, "name": "Headphones", "category": "Accessories", "price": 99.99}

sample_product_5 = {"product_id": 202, "name": "Smartwatch", "category": "Electronics", "price": 299.99}

sample_products = [sample_product_1, sample_product_2, sample_product_3, sample_product_4, sample_product_5]

config = load_config()
if config.debug:
    app.debug = True
else:
    app.debug = False


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/custom")
def read_custom():
    return "Custom"


@app.get("/db")
def get_db_info():
    logger.info(f"Connecting to database: {config.db.database_url}")
    return {"database_url": config.db.database_url}


# @app.get("/user", response_model=User)
# def get_user():
#     return user


@app.post("/user")
def check_user_age(user: User):
    if user.age >= 18:
        user.is_adult = True
    return user


@app.get("/users/{username}")
def get_user(username: str):
    for user in fake_users:
        if user["username"] == username:
            return user
    return {"username": "Not found"}


@app.get("/users/")
def read_users(limit: int = 10):
    return fake_users[:limit]


@app.post("/add_user", response_model=UserInfo)
def add_user(user: UserInfo):
    fake_users.append({"username": user.username, "user_info": user.user_info})
    return user


@app.post("/feedback")
def feedback(feedback: Feedback):
    feedback_lst.append({"name": feedback.name, "comments": feedback.message})
    return f"Feedback received. Thank you, {feedback.name}!"


@app.get("/comments")
def get_comments():
    return feedback_lst


@app.post("/create_user", response_model=UserCreate)
def create_user(new_user: UserCreate):
    db_users.append(new_user)
    return new_user


@app.get("/show_users")
def show_users():
    if db_users:
        return db_users
    else:
        return {"message": "No users found"}


@app.get("/product/{product_id}")
def get_product(product_id: int):
    return [product for product in sample_products if product["product_id"] == product_id][0]


@app.get("/products/search")
def search(keyword: str, category: str = None, limit: int = 10):
    result = list(filter(lambda item: keyword.lower() in item["name"].lower(), sample_products))
    if category:
        result = list(filter(lambda item: item["category"] == category, result))
    return result[:limit]


if __name__ == "__main__":
    print(get_product(123))
