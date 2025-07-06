# Ecommerce Project

This is an Ecommerce project built with Django. The project includes features such as product listing, product detail view, user authentication, wishlist functionality, and more.

## Features

- User authentication (login, registration, logout)
- Product listing and detail view
- Add to cart and wishlist functionality
- Checkout process

## Requirements

The project requires the following dependencies:
- python==3.10
- asgiref==3.8.1
- Django==5.1.2
- pillow==11.0.0
- python-dotenv==1.0.1
- sqlparse==0.5.1
- typing_extensions==4.12.2

## Installation

1. Clone the repository:

```bash
git clone https://github.com/razig17/ecommerce.git
cd ecommerce
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Set up the environment variables:

Create a [`.env`] file in the project root and add the following variables:

```bash
SECRET_KEY=your_secret_key 
```
if you don't know how to get it use

```env
SECRET_KEY="wwf*2#86t64!fgh6yav$aoeuo@u2o@fy&*gg76q!&%6x_wbduad"
```
5. Apply the migrations:

```bash
python manage.py migrate
```

6. Create a superuser:

```bash
python manage.py createsuperuser
```

With the superuser account, you can:

- Access the Django admin interface at `http://127.0.0.1:8000/admin/`.
- Manage users, products, orders, and other models.
- Add, edit, and delete records in the database.
- Perform administrative tasks such as managing site settings and configurations.

7. Run the development server:

```bash
python manage.py runserver
```

8. Open your browser and go to `http://127.0.0.1:8000/` to see the application.

## Usage

- Register a new user or log in with the superuser account.
- Browse the products and add them to your cart or wishlist.
- Proceed to checkout to place an order.

## Contributing

If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [`LICENSE`]( LICENSE) file for more information.
