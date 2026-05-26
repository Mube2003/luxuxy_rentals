from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import json, os, uuid
from datetime import datetime
from functools import wraps
import mysql.connector

app = Flask(__name__)
app.secret_key = "luxury_rentals_secret_2025"

USERS_FILE  = "users.json"
ORDERS_FILE = "orders.json"
MESSAGES_FILE = "contact_messages.json"
REVIEWS_FILE = "reviews.json"
WISHLIST_FILE = "wishlist.json"
LOYALTY_FILE = "loyalty_points.json"
PROMO_FILE = "promo_codes.json"
UPLOAD_FOLDER = "static/uploads"
ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ── MySQL Configuration ───────────────────
DB_ENABLED = os.getenv('DB_ENABLED', 'False').lower() == 'true'
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'Naaz@123'),
    'database': os.getenv('DB_NAME', 'luxury_rentals'),
    'port': int(os.getenv('DB_PORT', 3306))
}

def get_db_connection():
    if DB_ENABLED:
        return mysql.connector.connect(**DB_CONFIG)
    return None

# ── JSON helpers ──────────────────────────
def load_json(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {}

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def load_messages():
    if not os.path.exists(MESSAGES_FILE):
        return []
    with open(MESSAGES_FILE, encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, list) else []


def save_messages(messages):
    with open(MESSAGES_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2)


# ── Reviews System ────────────────────────
def load_reviews():
    if not os.path.exists(REVIEWS_FILE):
        return {}
    with open(REVIEWS_FILE, encoding="utf-8") as f:
        return json.load(f)

def save_reviews(reviews):
    with open(REVIEWS_FILE, "w", encoding="utf-8") as f:
        json.dump(reviews, f, indent=2)

def get_item_reviews(item_id):
    reviews = load_reviews()
    item_reviews = reviews.get(str(item_id), [])
    if item_reviews:
        avg_rating = sum(r["rating"] for r in item_reviews) / len(item_reviews)
        return {"reviews": item_reviews, "avg_rating": round(avg_rating, 1), "count": len(item_reviews)}
    return {"reviews": [], "avg_rating": 0, "count": 0}

# ── Wishlist System ───────────────────────
def load_wishlist():
    if not os.path.exists(WISHLIST_FILE):
        return {}
    with open(WISHLIST_FILE, encoding="utf-8") as f:
        return json.load(f)

def save_wishlist(wishlist):
    with open(WISHLIST_FILE, "w", encoding="utf-8") as f:
        json.dump(wishlist, f, indent=2)

# ── Loyalty Points ────────────────────────
def load_loyalty():
    if not os.path.exists(LOYALTY_FILE):
        return {}
    with open(LOYALTY_FILE, encoding="utf-8") as f:
        return json.load(f)

def save_loyalty(loyalty):
    with open(LOYALTY_FILE, "w", encoding="utf-8") as f:
        json.dump(loyalty, f, indent=2)

def get_user_loyalty(username):
    loyalty = load_loyalty()
    if username not in loyalty:
        loyalty[username] = {"points": 0, "referral_code": f"REF-{username.upper()}", "referred_friends": 0}
        save_loyalty(loyalty)
    return loyalty[username]

def add_loyalty_points(username, points):
    loyalty = load_loyalty()
    if username not in loyalty:
        loyalty[username] = {"points": 0, "referral_code": f"REF-{username.upper()}", "referred_friends": 0}
    loyalty[username]["points"] += points
    save_loyalty(loyalty)

# ── Promo Codes ──────────────────────────
def load_promo_codes():
    if not os.path.exists(PROMO_FILE):
        return {}
    with open(PROMO_FILE, encoding="utf-8") as f:
        return json.load(f)

def save_promo_codes(promos):
    with open(PROMO_FILE, "w", encoding="utf-8") as f:
        json.dump(promos, f, indent=2)

def validate_promo_code(code):
    promos = load_promo_codes()
    if code in promos and promos[code].get("active", True):
        return promos[code]
    return None


def allowed_image(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


def save_uploaded_image(file):
    if file and file.filename and allowed_image(file.filename):
        filename = secure_filename(file.filename)
        unique_name = f"{uuid.uuid4().hex}_{filename}"
        path = os.path.join(UPLOAD_FOLDER, unique_name)
        file.save(path)
        return f"uploads/{unique_name}"
    return None

# ── Simplified Data Functions (JSON only) ─────────────────────
def load_users():
    return load_json(USERS_FILE)


def save_users(users):
    save_json(USERS_FILE, users)


def load_orders():
    return load_json(ORDERS_FILE)


def save_orders(orders):
    save_json(ORDERS_FILE, orders)


def save_order(order):
    orders = load_orders()
    orders[order["order_id"]] = order
    save_orders(orders)


# ── Catalogue ─────────────────────────────
MENU_ITEMS = [
    {
        "id": 1,
        "name": "Nikah Nama",
        "desc": "Select from multiple Nikah Nama patterns and images so you can choose the style you like best.",
        "price": 2250,
        "emoji": "📜",
        "image": "images/nikah_nama_1.jpg",
        "variants": [
            {
                "id": "nikah_nama_classic",
                "name": "Classic",
                "image": "images/nikah_nama_1.jpg",
                "price": 2250,
                "label": "Classic Pattern"
            },
            {
                "id": "nikah_nama_premium",
                "name": "Premium",
                "image": "images/nikah_nama_2.jpg",
                "price": 2880,
                "label": "Premium Pattern"
            },
            {
                "id": "nikah_nama_floral",
                "name": "Floral",
                "image": "images/nikah_nama_3.jpg",
                "price": 2520,
                "label": "Floral Pattern"
            }
        ],
        "category": "Ceremony",
        "features": [
            "Three pattern options for ceremony styling",
            "Premium certificate holder finish",
            "Suitable for formal wedding rituals",
            "Comes with a protective display cover"
        ]
    },
    {
        "id": 2,
        "name": "Nikah Pen",
        "desc": "Premium signing pen with multiple finish options for your ceremony.",
        "price": 1080,
        "emoji": "🖊️",
        "image": "images/nikah_pen_1.jpg",
        "variants": [
            {
                "id": "nikah_pen_classic",
                "name": "Classic",
                "image": "images/nikah_pen_1.jpg",
                "price": 1080,
                "label": "Classic Finish"
            },
            {
                "id": "nikah_pen_gold",
                "name": "Gold Trim",
                "image": "images/nikah_pen_2.jpg",
                "price": 1350,
                "label": "Gold Trim"
            },
            {
                "id": "nikah_pen_deluxe",
                "name": "Deluxe",
                "image": "images/nikah_pen_3.jpg",
                "price": 1620,
                "label": "Deluxe Edition"
            }
        ],
        "category": "Ceremony",
        "features": [
            "Smooth ink flow for elegant signatures",
            "Includes luxury velvet presentation box",
            "Polished pearl finish with gold trim",
            "Comfort grip for formal signing"
        ]
    },
    {
        "id": 3,
        "name": "Nikah Mirror",
        "desc": "Choose from multiple mirror frame styles for your ceremony.",
        "price": 3150,
        "emoji": "🪞",
        "image": "images/nikah_mirror_1.jpg",
        "variants": [
            {
                "id": "nikah_mirror_silver",
                "name": "Silver Floral",
                "image": "images/nikah_mirror_1.jpg",
                "price": 3150,
                "label": "Silver Floral"
            },
            {
                "id": "nikah_mirror_gold",
                "name": "Gold Frame",
                "image": "images/nikah_mirror_2.jpg",
                "price": 3420,
                "label": "Gold Frame"
            },
            {
                "id": "nikah_mirror_embossed",
                "name": "Embossed",
                "image": "images/nikah_mirror_3.jpg",
                "price": 3600,
                "label": "Embossed"
            }
        ],
        "category": "Ceremony",
        "features": [
            "Handcrafted silver floral frame",
            "Lightweight and easy to hold",
            "Beautiful ceremonial styling",
            "Perfect gift for bridal rituals"
        ]
    },
    {
        "id": 4,
        "name": "Nikah Gunghat",
        "desc": "Different bridal veil patterns to match your ceremonial style.",
        "price": 3600,
        "emoji": "👰",
        "image": "images/nikah_gunghat_1.jpg",
        "variants": [
            {
                "id": "nikah_gunghat_classic",
                "name": "Classic",
                "image": "https://images.unsplash.com/photo-1530562141207-3992e1a7eae2?w=400&h=300&fit=crop",
                "price": 3600,
                "label": "Classic Veil"
            },
            {
                "id": "nikah_gunghat_sequin",
                "name": "Sequin",
                "image": "images/nikah_gunghat_2.jpg",
                "price": 4050,
                "label": "Sequin Work"
            },
            {
                "id": "nikah_gunghat_designer",
                "name": "Designer",
                "image": "images/nikah_gunghat_3.jpg",
                "price": 4320,
                "label": "Designer Pattern"
            }
        ],
        "category": "Bridal",
        "features": [
            "Delicate zari and sequin work",
            "Soft, breathable bridal fabric",
            "Traditional design with modern comfort",
            "Finely finished edges for lasting wear"
        ]
    },
    {
        "id": 5,
        "name": "Jewellery Set",
        "desc": "Select a jewellery set pattern that matches the ceremony theme.",
        "price": 7650,
        "emoji": "💍",
        "image": "images/jewellery_set_1.jpg",
        "variants": [
            {
                "id": "jewellery_set_gold",
                "name": "Gold",
                "image": "images/jewellery_set_1.jpg",
                "price": 7650,
                "label": "Gold Set"
            },
            {
                "id": "jewellery_set_silver",
                "name": "Silver",
                "image": "images/jewellery_set_2.jpg",
                "price": 7470,
                "label": "Silver Set"
            },
            {
                "id": "jewellery_set_bridesmaid",
                "name": "Bridal",
                "image": "images/jewellery_set_3.jpg",
                "price": 8100,
                "label": "Bridal Set"
            }
        ],
        "category": "Bridal",
        "features": [
            "Full coordinating bridal set",
            "Hypoallergenic polish finish",
            "Includes necklace, earrings, bangles",
            "Designed for timeless wedding elegance"
        ]
    },
    {
        "id": 6,
        "name": "Haldi & Mehndi Plates",
        "desc": "Choose a plate pattern that fits your event’s color palette.",
        "price": 1620,
        "emoji": "🌼",
        "image": "images/haldi_mehndi_plates_1.jpg",
        "variants": [
            {
                "id": "haldi_mehndi_plates_floral",
                "name": "Floral",
                "image": "images/haldi_mehndi_plates_1.jpg",
                "price": 1620,
                "label": "Floral"
            },
            {
                "id": "haldi_mehndi_plates_royal",
                "name": "Royal",
                "image": "images/haldi_mehndi_plates_2.jpg",
                "price": 1890,
                "label": "Royal"
            },
            {
                "id": "haldi_mehndi_plates_elegant",
                "name": "Elegant",
                "image": "images/haldi_mehndi_plates_3.jpg",
                "price": 1755,
                "label": "Elegant"
            }
        ],
        "category": "Ceremony",
        "features": [
            "Hand-painted traditional styling",
            "Sturdy premium material",
            "Includes matching floral motifs",
            "Ready to display for rituals"
        ]
    },
    {
        "id": 7,
        "name": "Gajra",
        "desc": "Choose from multiple floral garland styles for bridal ceremonies.",
        "price": 540,
        "emoji": "🌸",
        "image": "images/gajra_1.jpg",
        "variants": [
            {
                "id": "gajra_jasmine",
                "name": "Jasmine",
                "image": "images/gajra_1.jpg",
                "price": 540,
                "label": "Jasmine"
            },
            {
                "id": "gajra_rose",
                "name": "Rose",
                "image": "images/gajra_2.jpg",
                "price": 585,
                "label": "Rose"
            },
            {
                "id": "gajra_mixed",
                "name": "Mixed",
                "image": "images/gajra_3.jpg",
                "price": 630,
                "label": "Mixed Flowers"
            }
        ],
        "category": "Bridal",
        "features": [
            "Fresh jasmine petals with natural fragrance",
            "Soft and lightweight for long wear",
            "Hand-tied for beautiful drape",
            "Ideal for bridal and ceremonial styling"
        ]
    },
    {
        "id": 8,
        "name": "Cerame Custom Set",
        "desc": "Upload your own photo and preview it on a premium ceremonial design mockup.",
        "price": 1999,
        "emoji": "🖼️",
        "image": "images/nikah_nama_1.jpg",
        "variants": [
            {
                "id": "cerame_custom",
                "name": "Custom Preview",
                "image": "images/nikah_nama_1.jpg",
                "price": 1999,
                "label": "Upload Your Photo"
            }
        ],
        "category": "Cerame",
        "features": [
            "Photo upload preview for your custom design",
            "Premium ceremony layout with rich detailing",
            "Best suited for personalised wedding décor",
            "Fast delivery and easy booking"
        ]
    }
]

def get_item(item_id):
    return next((i for i in MENU_ITEMS if i["id"]==item_id), None)

# ── Auth decorator ────────────────────────
def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("auth"))
        return fn(*args, **kwargs)
    return wrapper


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if "user" not in session or session.get("role") != "admin":
            return redirect(url_for("home"))
        return fn(*args, **kwargs)
    return wrapper

# ── Auth ──────────────────────────────────
@app.route("/")
def index():
    return redirect(url_for("home") if "user" in session else url_for("auth"))

@app.route("/auth", methods=["GET","POST"])
def auth():
    error = success = ""
    if request.method == "POST":
        users  = load_users()
        action = request.form.get("action")

        if action == "login":
            uname = request.form.get("username","").strip()
            pwd   = request.form.get("password","")
            if uname in users and users[uname]["password"] == pwd:
                user_data = users.get(uname, {})
                session.update({
                    "user": uname,
                    "full_name": user_data.get("full_name", uname),
                    "email": user_data.get("email", ""),
                    "role": user_data.get("role", "admin" if uname == "admin" else "customer"),
                })
                return redirect(url_for("home"))
            error = "Invalid username or password."

        elif action == "register":
            uname     = request.form.get("reg_username","").strip()
            full_name = request.form.get("reg_fullname","").strip()
            email     = request.form.get("reg_email","").strip()
            phone     = request.form.get("reg_phone","").strip()
            pwd       = request.form.get("reg_password","")
            city      = request.form.get("reg_city","").strip()

            if uname in users:
                error = "Username already exists."
            elif not all([uname,full_name,email,pwd]):
                error = "Please fill all required fields."
            else:
                users[uname] = {"password":pwd,"full_name":full_name,
                                "email":email,"phone":phone,"city":city,
                                "joined":datetime.now().strftime("%d %b %Y"),
                                "role":"customer"}
                save_users(users)
                success = "Registration successful! Please sign in."

    return render_template("auth.html", error=error, success=success)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth"))

# ── Pages ─────────────────────────────────
@app.route("/home")
@login_required
def home():
    categories = sorted({i.get("category", "Other") for i in MENU_ITEMS})
    deal_items = MENU_ITEMS[:6]
    return render_template("home.html", categories=categories, deal_items=deal_items)

@app.route("/menu")
@login_required
def menu():
    wishlist_data = load_wishlist()
    user_wishlist = wishlist_data.get(session.get("user"), [])
    categories = sorted({i.get("category", "Other") for i in MENU_ITEMS})
    return render_template("menu.html", items=MENU_ITEMS, user_wishlist=user_wishlist, categories=categories, selected_category="")

@app.route("/item/<int:item_id>", strict_slashes=False)
@login_required
def item_detail(item_id):
    item = get_item(item_id)
    if not item:
        return redirect(url_for("menu"))
    return render_template("item_detail.html", item=item)

# ── Cart Management ──────────────────────
@app.route("/add_to_cart/<int:item_id>", methods=["POST"])
@login_required
def add_to_cart(item_id):
    item = get_item(item_id)
    if not item:
        return redirect(url_for("menu"))
    
    quantity = int(request.form.get("quantity", 1))
    uploaded_image = request.files.get("custom_image")
    custom_image_path = save_uploaded_image(uploaded_image) if uploaded_image else None
    selected_image = custom_image_path or request.form.get("selected_image") or item.get("image")
    selected_price = int(request.form.get("selected_price") or item.get("price", 0))
    selected_variant = request.form.get("selected_variant") or item.get("name")
    
    # Initialize cart if not exists
    if "cart" not in session:
        session["cart"] = {}
    
    cart = session["cart"]
    item_key = f"{item_id}:{selected_image}"
    
    if item_key in cart:
        cart[item_key]["quantity"] += quantity
    else:
        cart[item_key] = {
            "id": item["id"],
            "name": item["name"],
            "price": selected_price,
            "emoji": item["emoji"],
            "quantity": quantity,
            "selected_image": selected_image,
            "image": item.get("image"),
            "selected_variant": selected_variant
        }
    
    session["cart"] = cart
    session.modified = True
    
    return redirect(url_for("cart"))

@app.route("/cart")
@login_required
def cart():
    cart_items = []
    total = 0
    
    if "cart" in session:
        for item_id, item_data in session["cart"].items():
            item_total = item_data["price"] * item_data["quantity"]
            cart_items.append({
                **item_data,
                "total": item_total
            })
            total += item_total
    
    return render_template("cart.html", cart_items=cart_items, total=total)

@app.route("/update_cart/<int:item_id>", methods=["POST"])
@login_required
def update_cart(item_id):
    if "cart" not in session:
        return redirect(url_for("cart"))
    
    item_key = str(item_id)
    action = request.form.get("action")
    
    if item_key in session["cart"]:
        if action == "increase":
            session["cart"][item_key]["quantity"] += 1
        elif action == "decrease":
            session["cart"][item_key]["quantity"] -= 1
            if session["cart"][item_key]["quantity"] <= 0:
                del session["cart"][item_key]
        elif action == "remove":
            del session["cart"][item_key]
    
    session.modified = True
    return redirect(url_for("cart"))

@app.route("/clear_cart")
@login_required
def clear_cart():
    if "cart" in session:
        session["cart"] = {}
        session.modified = True
    return redirect(url_for("cart"))

@app.route("/checkout")
@login_required
def checkout():
    if "cart" not in session or not session["cart"]:
        return redirect(url_for("cart"))
    
    cart_items = []
    total = 0
    
    for item_id, item_data in session["cart"].items():
        item_total = item_data["price"] * item_data["quantity"]
        cart_items.append({
            **item_data,
            "total": item_total
        })
        total += item_total
    
    users = load_users()
    user_data = users.get(session["user"], {})
    
    return render_template("checkout.html", cart_items=cart_items, total=total, user_data=user_data)

@app.route("/place_order_cart", methods=["POST"])
@login_required
def place_order_cart():
    if "cart" not in session or not session["cart"]:
        return redirect(url_for("cart"))
    
    users = load_users()
    user_data = users.get(session["user"], {})
    
    # Calculate totals
    subtotal = 0
    cart_items = []
    
    for item_id, item_data in session["cart"].items():
        item_total = item_data["price"] * item_data["quantity"]
        subtotal += item_total
        cart_items.append({
            **item_data,
            "total": item_total
        })
    
    delivery_fee = 500
    total = subtotal + delivery_fee
    
    # Get form data
    event_date = request.form.get("event_date", "")
    address = request.form.get("address", "")
    pay_method = request.form.get("pay_method", "UPI")
    
    # Create order
    order_id = "LR-" + str(uuid.uuid4())[:8].upper()
    quantity = sum(item["quantity"] for item in cart_items)
    order = {
        "order_id": order_id,
        "username": session["user"],
        "full_name": user_data.get("full_name", session["user"]),
        "email": user_data.get("email", ""),
        "phone": user_data.get("phone", ""),
        "city": user_data.get("city", ""),
        "address": address,
        "items": cart_items,
        "subtotal": subtotal,
        "delivery_fee": delivery_fee,
        "total": total,
        "quantity": quantity,
        "item_name": cart_items[0]["name"] if len(cart_items) == 1 else f"{len(cart_items)} items",
        "item_emoji": cart_items[0].get("emoji", "🛒") if len(cart_items) == 1 else "🛒",
        "item_category": cart_items[0].get("category", "Mixed") if len(cart_items) == 1 else "Mixed",
        "pay_method": pay_method,
        "event_date": event_date,
        "status": "Confirmed",
        "placed_at": datetime.now().strftime("%d %b %Y, %I:%M %p"),
        "placed_ip": request.remote_addr or "127.0.0.1",
    }
    
    save_order(order)
    
    # Clear cart
    session["cart"] = {}
    session.modified = True
    
    # Award loyalty points (1 point per rupee spent)
    add_loyalty_points(session["user"], int(total))
    
    return redirect(url_for("order_success", order_id=order_id))

# ── Search & Filter ───────────────────────
@app.route("/search")
@login_required
def search():
    query = request.args.get("q", "").lower()
    category = request.args.get("category", "")
    
    filtered_items = MENU_ITEMS
    
    if query:
        filtered_items = [item for item in filtered_items if query in item["name"].lower() or query in item["desc"].lower()]
    
    if category:
        filtered_items = [item for item in filtered_items if item["category"] == category]

    categories = sorted({i.get("category", "Other") for i in MENU_ITEMS})
    wishlist_data = load_wishlist()
    user_wishlist = wishlist_data.get(session.get("user"), [])
    
    return render_template("menu.html", items=filtered_items, search_query=query, selected_category=category, categories=categories, user_wishlist=user_wishlist)

@app.route("/upload_preview", methods=["POST"])
@login_required
def upload_preview():
    uploaded_image = request.files.get("image")
    source = request.form.get("source", "gallery")
    if not uploaded_image or uploaded_image.filename == "":
        return redirect(url_for("menu"))
    image_path = save_uploaded_image(uploaded_image)
    if not image_path:
        return redirect(url_for("menu"))
    return render_template("upload_preview.html", image_url=url_for("static", filename=image_path), source=source)

# ── User Profile ──────────────────────────
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    users = load_users()
    user_data = users.get(session["user"], {})
    
    if request.method == "POST":
        # Update profile
        updated_data = {
            "password": user_data.get("password"),  # Keep existing password
            "full_name": request.form.get("full_name", user_data.get("full_name", "")),
            "email": request.form.get("email", user_data.get("email", "")),
            "phone": request.form.get("phone", user_data.get("phone", "")),
            "city": request.form.get("city", user_data.get("city", "")),
            "joined": user_data.get("joined", datetime.now().strftime("%d %b %Y")),
            "role": user_data.get("role", "customer")
        }
        
        users[session["user"]] = updated_data
        save_users(users)
        
        # Update session
        session["full_name"] = updated_data["full_name"]
        session["email"] = updated_data["email"]
        
        return redirect(url_for("profile"))
    
    return render_template("profile.html", user_data=user_data)

@app.route("/about")
@login_required
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET","POST"])
@login_required
def contact():
    msg = ""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        message_text = request.form.get("message", "").strip()
        if name and email and message_text:
            stored = load_messages()
            auto_reply_text = (
                "Thank you for reaching out to Luxury Rentals. "
                "We have received your message and will get back to you shortly. "
                "This is an automated confirmation so you know your inquiry is with us."
            )
            stored.append({
                "name": name,
                "email": email,
                "phone": phone,
                "username": session.get("user", ""),
                "message": message_text,
                "sent_at": datetime.now().strftime("%d %b %Y, %I:%M %p"),
                "admin_reply": auto_reply_text,
                "reply_subject": "Re: Your inquiry to Luxury Rentals",
                "reply_sent_at": datetime.now().strftime("%d %b %Y, %I:%M %p"),
                "reply_to": email,
                "status": "Auto Replied",
            })
            save_messages(stored)
            msg = "Thank you! We will contact you soon."

    user_messages = [m for m in reversed(load_messages()) if m.get("username") == session.get("user") or m.get("email") == session.get("email")]
    return render_template("contact.html", message=msg, messages=user_messages)

# ── Payment ───────────────────────────────
@app.route("/payment/<int:item_id>")
@login_required
def payment(item_id):
    item = get_item(item_id)
    if not item:
        return redirect(url_for("menu"))
    users     = load_users()
    user_data = users.get(session["user"], {})
    return render_template("payment.html", item=item, user_data=user_data)

@app.route("/place_order", methods=["POST"])
@login_required
def place_order():
    item_id    = int(request.form.get("item_id"))
    item       = get_item(item_id)
    event_date = request.form.get("event_date","")
    address    = request.form.get("address","")
    pay_method = request.form.get("pay_method","UPI")
    quantity   = int(request.form.get("quantity",1))

    users     = load_users()
    user_data = users.get(session["user"], {})
    subtotal  = item["price"] * quantity
    total     = subtotal + 500

    order_id = "LR-" + str(uuid.uuid4())[:8].upper()
    order = {
        "order_id":   order_id,
        "username":   session["user"],
        "full_name":  user_data.get("full_name", session["user"]),
        "email":      user_data.get("email",""),
        "phone":      user_data.get("phone",""),
        "city":       user_data.get("city",""),
        "address":    address,
        "items": [{
            "id": item_id,
            "name": item["name"],
            "emoji": item["emoji"],
            "category": item["category"],
            "price": item["price"],
            "quantity": quantity,
            "total": subtotal,
        }],
        "subtotal": subtotal,
        "delivery_fee": 500,
        "total": total,
        "item_name": item["name"],
        "item_emoji": item["emoji"],
        "item_category": item["category"],
        "quantity": quantity,
        "deposit": 500,
        "pay_method": pay_method,
        "event_date": event_date,
        "status":     "Confirmed",
        "placed_at":  datetime.now().strftime("%d %b %Y, %I:%M %p"),
        "placed_ip":  request.remote_addr or "127.0.0.1",
    }

    save_order(order)
    # Award loyalty points (1 point per rupee spent)
    add_loyalty_points(session["user"], int(total))
    return redirect(url_for("order_success", order_id=order_id))

@app.route("/order_success/<order_id>")
@login_required
def order_success(order_id):
    orders = load_orders()
    order  = orders.get(order_id)
    if not order or order["username"] != session["user"]:
        return redirect(url_for("home"))
    return render_template("order_success.html", order=order)

# ── My Orders ─────────────────────────────
@app.route("/my_orders")
@login_required
def my_orders():
    orders = load_orders()
    mine   = sorted([o for o in orders.values() if o["username"]==session["user"]],
                    key=lambda x: x["placed_at"], reverse=True)
    return render_template("my_orders.html", orders=mine)

@app.route("/my_messages")
@login_required
def my_messages():
    messages = load_messages()
    mine = [m for m in reversed(messages) if m.get("username") == session["user"] or m.get("email") == session.get("email")]
    return render_template("my_messages.html", messages=mine)

@app.route("/order_detail/<order_id>")
@login_required
def order_detail(order_id):
    orders = load_orders()
    order  = orders.get(order_id)
    if not order or (order["username"] != session["user"] and session.get("role") != "admin"):
        return redirect(url_for("my_orders"))
    return render_template("order_detail.html", order=order)

@app.route("/delete_order/<order_id>", methods=["POST"])
@login_required
def delete_order(order_id):
    orders = load_orders()
    order  = orders.get(order_id)
    if not order or (order["username"] != session["user"] and session.get("role") != "admin"):
        return redirect(url_for("my_orders"))

    del orders[order_id]
    save_orders(orders)
    return redirect(url_for("my_orders"))


def _parse_placed_at(s: str):
    if not s:
        return None
    for fmt in ("%d %b %Y, %I:%M %p", "%d %b %Y"):
        try:
            return datetime.strptime(s, fmt)
        except Exception:
            pass
    return None


# ── Dashboard (User Analytics) ────────────
@app.route("/dashboard")
@admin_required
def dashboard():
    if session["user"] != "admin":
        return redirect(url_for("home"))
    orders = load_orders()
    mine = [o for o in orders.values() if o.get("username") == session.get("user")]

    # Build last 12 months buckets (oldest -> newest)
    now = datetime.now()
    months = []
    y, m = now.year, now.month
    for _ in range(12):
        months.append((y, m))
        m -= 1
        if m <= 0:
            y -= 1
            m = 12
    months.reverse()

    month_labels = [datetime(y, m, 1).strftime("%b %Y") for (y, m) in months]
    month_revenue = [0.0 for _ in months]  # using revenue as "profit" for now
    month_completed = [0 for _ in months]

    # In this app flow, orders are "completed" for analytics once confirmed or delivered.
    completed_statuses = {"Confirmed", "Delivered", "Completed"}

    recent = []
    total_revenue = 0.0
    completed_total = 0
    status_counts = {}

    for o in mine:
        placed_at = o.get("placed_at", "")
        dt = _parse_placed_at(placed_at)
        total = float(o.get("total") or 0)
        status = (o.get("status") or "").strip() or "Unknown"

        total_revenue += total
        status_counts[status] = status_counts.get(status, 0) + 1
        if status in completed_statuses:
            completed_total += 1

        if dt:
            recent.append((dt, o))
            for idx, (yy, mm) in enumerate(months):
                if dt.year == yy and dt.month == mm:
                    month_revenue[idx] += total
                    if status in completed_statuses:
                        month_completed[idx] += 1
                    break

    recent.sort(key=lambda x: x[0], reverse=True)
    recent_orders = [o for _, o in recent[:12]]

    avg_order_value = (total_revenue / len(mine)) if mine else 0.0
    pending_total = len(mine) - completed_total

    return render_template(
        "dashboard.html",
        month_labels=month_labels,
        month_revenue=month_revenue,
        month_completed=month_completed,
        total_revenue=round(total_revenue, 2),
        completed_total=completed_total,
        pending_total=pending_total,
        status_counts=status_counts,
        total_orders=len(mine),
        avg_order_value=round(avg_order_value, 2),
        recent_orders=recent_orders,
        now_label=now.strftime("%d %b %Y"),
    )

# ── Admin Dashboard ───────────────────────
@app.route("/admin")
@admin_required
def admin():
    if session["user"] != "admin":
        return redirect(url_for("home"))
    orders        = load_orders()
    users         = load_users()
    all_orders    = sorted(orders.values(), key=lambda x: x["placed_at"], reverse=True)
    total_revenue = sum(o["total"] for o in all_orders)
    
    # Calculate order statistics
    confirmed_count = sum(1 for o in all_orders if o.get("status") == "Confirmed")
    processing_count = sum(1 for o in all_orders if o.get("status") == "Processing")
    shipped_count = sum(1 for o in all_orders if o.get("status") == "Shipped")
    delivered_count = sum(1 for o in all_orders if o.get("status") == "Delivered")
    
    return render_template("admin.html", orders=all_orders,
                           users=users, total_revenue=total_revenue,
                           confirmed=confirmed_count, processing=processing_count,
                           shipped=shipped_count, delivered=delivered_count)


@app.route("/admin/messages")
@admin_required
def admin_messages():
    if session["user"] != "admin":
        return redirect(url_for("home"))
    messages = list(reversed(load_messages()))
    reply_status = request.args.get("reply_status", "")
    return render_template("admin_messages.html", messages=messages, reply_status=reply_status)

@app.route("/admin/reply_message", methods=["POST"])
@admin_required
def admin_reply():
    if session["user"] != "admin":
        return redirect(url_for("home"))

    reply_to = request.form.get("reply_to", "").strip()
    reply_subject = request.form.get("reply_subject", "").strip()
    reply_text = request.form.get("reply_message", "").strip()
    try:
        message_index = int(request.form.get("message_index", -1))
    except ValueError:
        message_index = -1

    messages = load_messages()
    if 0 <= message_index < len(messages):
        original_index = len(messages) - 1 - message_index
        if 0 <= original_index < len(messages):
            messages[original_index]["admin_reply"] = reply_text
            messages[original_index]["reply_subject"] = reply_subject
            messages[original_index]["reply_sent_at"] = datetime.now().strftime("%d %b %Y, %I:%M %p")
            messages[original_index]["reply_to"] = reply_to
            messages[original_index]["status"] = "Replied"
            save_messages(messages)
            return redirect(url_for("admin_messages", reply_status="Reply sent to %s" % reply_to))

    return redirect(url_for("admin_messages", reply_status="Unable to send reply."))

@app.route("/admin/create_promo", methods=["POST"])
@admin_required
def admin_create_promo():
    if session["user"] != "admin":
        return redirect(url_for("home"))
    
    code = request.form.get("code", "").strip().upper()
    discount = float(request.form.get("discount", 0))
    promo_type = request.form.get("type", "fixed")
    
    promos = load_promo_codes()
    promos[code] = {
        "discount": discount,
        "type": promo_type,
        "active": True,
        "created": datetime.now().strftime("%d %b %Y")
    }
    save_promo_codes(promos)
    
    return redirect(url_for("admin"))


@app.route("/admin/update_status/<order_id>", methods=["POST"])
@admin_required
def update_order_status(order_id):
    
    new_status = request.form.get("status")
    delivery_address = request.form.get("delivery_address")
    
    orders = load_orders()
    if order_id in orders:
        if new_status:
            orders[order_id]["status"] = new_status
        if delivery_address:
            orders[order_id]["delivery_address"] = delivery_address
        
        # Track status history
        if "status_history" not in orders[order_id]:
            orders[order_id]["status_history"] = []
        
        orders[order_id]["status_history"].append({
            "status": new_status or orders[order_id]["status"],
            "updated_at": datetime.now().strftime("%d %b %Y, %I:%M %p")
        })
        
        save_orders(orders)
        return redirect(url_for("admin"))
    
    return redirect(url_for("admin"))

# ── Reviews & Ratings ────────────────────
@app.route("/add_review/<int:item_id>", methods=["POST"])
@login_required
def add_review(item_id):
    item = get_item(item_id)
    if not item:
        return redirect(url_for("menu"))
    
    rating = int(request.form.get("rating", 5))
    comment = request.form.get("comment", "").strip()
    
    reviews = load_reviews()
    item_key = str(item_id)
    
    if item_key not in reviews:
        reviews[item_key] = []
    
    reviews[item_key].append({
        "username": session["user"],
        "rating": rating,
        "comment": comment,
        "date": datetime.now().strftime("%d %b %Y"),
        "helpful": 0
    })
    
    save_reviews(reviews)
    add_loyalty_points(session["user"], 10)  # 10 points for review
    
    return redirect(url_for("item_detail", item_id=item_id))

@app.route("/get_reviews/<int:item_id>")
@login_required
def get_reviews(item_id):
    review_data = get_item_reviews(item_id)
    return render_template("reviews.html", **review_data)

# ── Wishlist ──────────────────────────────
@app.route("/toggle_wishlist/<int:item_id>", methods=["POST"])
@login_required
def toggle_wishlist(item_id):
    item = get_item(item_id)
    if not item:
        return redirect(url_for("menu"))
    
    wishlist = load_wishlist()
    username = session["user"]
    
    if username not in wishlist:
        wishlist[username] = []
    
    if item_id in wishlist[username]:
        wishlist[username].remove(item_id)
    else:
        wishlist[username].append(item_id)
        add_loyalty_points(username, 5)  # 5 points for adding to wishlist
    
    save_wishlist(wishlist)
    return redirect(url_for("item_detail", item_id=item_id))

@app.route("/wishlist")
@login_required
def wishlist():
    wishlist_data = load_wishlist()
    user_wishlist = wishlist_data.get(session["user"], [])

    items = [get_item(item_id) for item_id in user_wishlist]
    items = [i for i in items if i is not None]

    loyalty_data = get_user_loyalty(session["user"])
    return render_template("wishlist.html", items=items, loyalty=loyalty_data)

# ── Referral System ───────────────────────
@app.route("/referral")
@login_required
def referral():
    loyalty_data = get_user_loyalty(session["user"])
    referral_code = loyalty_data.get("referral_code", f"REF-{session['user'].upper()}")
    referred_count = loyalty_data.get("referred_friends", 0)
    referral_bonus = referred_count * 500  # 500 points per referral
    
    return render_template("referral.html", 
                         referral_code=referral_code,
                         referred_count=referred_count,
                         referral_bonus=referral_bonus)

@app.route("/register_referral", methods=["POST"])
def register_referral():
    referral_code = request.form.get("referral_code", "").strip()
    
    # Standard registration flow
    users = load_users()
    action = request.form.get("action", "register")
    
    if action == "register":
        uname = request.form.get("reg_username", "").strip()
        full_name = request.form.get("reg_fullname", "").strip()
        email = request.form.get("reg_email", "").strip()
        phone = request.form.get("reg_phone", "").strip()
        pwd = request.form.get("reg_password", "")
        city = request.form.get("reg_city", "").strip()
        
        if uname not in users and all([uname, full_name, email, pwd]):
            users[uname] = {
                "password": pwd,
                "full_name": full_name,
                "email": email,
                "phone": phone,
                "city": city,
                "joined": datetime.now().strftime("%d %b %Y"),
                "role": "customer"
            }
            save_users(users)
            
            # Process referral
            if referral_code and referral_code.startswith("REF-"):
                referrer = referral_code.replace("REF-", "").lower()
                if referrer in users:
                    # Add points to referrer and new user
                    add_loyalty_points(referrer, 500)
                    add_loyalty_points(uname, 250)
                    
                    # Update referred count
                    loyalty = load_loyalty()
                    if referrer in loyalty:
                        loyalty[referrer]["referred_friends"] = loyalty[referrer].get("referred_friends", 0) + 1
                        save_loyalty(loyalty)
            else:
                # New user bonus
                add_loyalty_points(uname, 100)
            
            session.update({
                "user": uname,
                "full_name": full_name,
                "email": email,
                "role": "customer"
            })
            return redirect(url_for("home"))
    
    return redirect(url_for("auth"))

# ── Promo Code ────────────────────────────
@app.route("/apply_promo", methods=["POST"])
@login_required
def apply_promo():
    promo_code = request.form.get("promo_code", "").strip().upper()
    promo = validate_promo_code(promo_code)
    
    if promo:
        session["applied_promo"] = {
            "code": promo_code,
            "discount": promo.get("discount", 0),
            "type": promo.get("type", "fixed")  # fixed or percentage
        }
        return {"status": "success", "discount": promo.get("discount", 0)}
    
    return {"status": "error", "message": "Invalid promo code"}

@app.route("/remove_promo")
@login_required
def remove_promo():
    if "applied_promo" in session:
        del session["applied_promo"]
        session.modified = True
    return redirect(request.referrer or url_for("cart"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
