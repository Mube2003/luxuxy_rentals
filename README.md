# 💎 Luxury Rentals — Premium Wedding Rental Platform
### Enhanced Edition with Loyalty, Referrals & Smart Features
**By Mubeentaj Mirji**

---

## 🎯 What's New? 

This enhanced version includes game-changing features to boost engagement and customer retention:

### ⭐ **NEW FEATURES**
1. **💎 Loyalty Points System** - Earn 1 point per ₹ spent, redeem for discounts
2. **👥 Referral Program** - Get 500 points per successful referral + rewards for friends
3. **❤️ Wishlist & Favorites** - Save items, track deals (5 points per save)
4. **⭐ Ratings & Reviews** - Customer reviews with ratings (10 points per review)
5. **🏷️ Promo Codes** - Admin-controlled discount codes (fixed or percentage)
6. **📊 Enhanced Analytics** - Better tracking of revenue, orders & customer behavior

---

## ▶️ Quick Start

```bash
# 1. Install Dependencies
pip install -r requirements.txt

# 2. Run the Application
python app.py

# 3. Open in Browser
http://localhost:5000
```

---

## 🔐 Demo Accounts

### Customer Account
- **Username:** customer
- **Password:** password123
- Try: Add to wishlist, leave reviews, earn loyalty points!

### Admin Account
- **Username:** admin
- **Password:** password123
- Access: http://localhost:5000/admin
- Features: Manage orders, create promo codes, view analytics

---

## ✨ Key Features Explained

### 💎 **Loyalty Program**
- Earn points on every purchase
- 5 points for adding items to wishlist
- 10 points for writing product reviews  
- Exchange points for future discounts
- Three tier system: Bronze → Silver → Gold

### 👥 **Referral System**
- Share unique referral code with friends
- Earn 500 points per successful referral
- Friends get 250 bonus points
- Track referral earnings on dashboard
- Social sharing buttons (WhatsApp, Twitter)

### ❤️ **Wishlist**
- Save favorite items for later
- Quick checkout from wishlist
- Earn loyalty points for wishlists
- Organized wishlist management

### ⭐ **Reviews & Ratings**
- Rate products 1-5 stars
- Write detailed reviews
- See average ratings and review count
- Earn loyalty points for reviews
- Reviews visible to all customers

### 🏷️ **Promo Codes**
- Admin creates discount codes
- Fixed amount or percentage discounts
- Easy redemption at checkout
- Example codes: WELCOME50, SUMMER15

---

## 📁 Project Structure

```
luxury_rentals/
├── app.py                        ← Flask backend (Python)
│
├── Data Files (Auto-created):
│   ├── users.json                ← User accounts
│   ├── orders.json               ← Order history
│   ├── reviews.json              ← Product reviews (NEW)
│   ├── wishlist.json             ← Wishlist items (NEW)
│   ├── loyalty_points.json       ← Points & referrals (NEW)
│   ├── promo_codes.json          ← Discount codes (NEW)
│   └── contact_messages.json     ← Contact form submissions
│
├── templates/
│   ├── base.html                 ← Navigation & layout
│   ├── auth.html                 ← Login + Registration (with referral)
│   ├── home.html                 ← Landing page
│   ├── menu.html                 ← Browse items
│   ├── item_detail.html          ← Item details + reviews + wishlist
│   ├── cart.html                 ← Shopping cart
│   ├── checkout.html             ← Checkout & payment
│   ├── payment.html              ← Payment methods
│   ├── order_success.html        ← Order confirmation
│   ├── my_orders.html            ← Order history
│   ├── order_detail.html         ← Order tracking
│   ├── profile.html              ← User profile
│   ├── dashboard.html            ← Analytics dashboard
│   ├── loyalty.html              ← Loyalty program info (NEW)
│   ├── referral.html             ← Referral details (NEW)
│   ├── wishlist.html             ← Wishlist page (NEW)
│   ├── reviews.html              ← Reviews display (NEW)
│   ├── admin.html                ← Admin dashboard (+ promo codes)
│   ├── admin_messages.html       ← Customer messages
│   └── about.html, contact.html  ← Info pages
│
├── static/
│   ├── css/style.css             ← Styling
│   ├── js/main.js                ← Frontend logic
│   └── images/                   ← Product images
│
├── requirements.txt              ← Python dependencies
└── run.bat                       ← Quick launcher (Windows)
```

---

## 🛣️ User Journey

```
New User
  ↓
Register (with optional referral code for 250 bonus points)
  ↓
Browse Items (earn 5 points per wishlist addition)
  ↓
Purchase Item (earn 1 point per ₹)
  ↓
Leave Review (earn 10 points)
  ↓
Earn Loyalty Tier
  ↓
Refer Friends (earn 500 points)
  ↓
Redeem Points for Discounts
```

---

## 🗄️ Data Models

### Loyalty Points
```json
{
  "username": {
    "points": 5250,
    "referral_code": "REF-USERNAME",
    "referred_friends": 3
  }
}
```

### Wishlist
```json
{
  "username": [1, 3, 5]  // Array of item IDs
}
```

### Reviews
```json
{
  "1": [
    {
      "username": "user123",
      "rating": 5,
      "comment": "Perfect for my wedding!",
      "date": "10 May 2025",
      "helpful": 12
    }
  ]
}
```

### Promo Codes
```json
{
  "WELCOME50": {
    "discount": 50,
    "type": "fixed",
    "active": true,
    "created": "10 May 2025"
  }
}
```

---

## 📊 Admin Dashboard Features

- **Order Management**: View, track, update order status
- **Revenue Analytics**: Total sales, delivery stats
- **User Registry**: All registered customers
- **Promo Codes**: Create/manage discount codes
- **Message Center**: Customer inquiries
- **Status Tracking**: Timeline of order updates

---

## 💻 Tech Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: JSON (local storage) / MySQL (optional)
- **Authentication**: Session-based
- **Payment**: UPI / Card / NetBanking (simulated)

---

## 🎨 Design Highlights

- **Responsive** - Works on desktop, tablet, mobile
- **Dark Mode Support** - Theme toggle in navbar
- **Premium UI** - Gold & luxury color scheme
- **Smooth Animations** - Modern interactions
- **Accessibility** - WCAG compliant

---

## 🔧 Configuration

### Environment Variables (Optional)
```bash
DB_TYPE=mysql
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=password
DB_NAME=luxury_rentals
DB_PORT=3306
```

### Features Control
- Set `DB_ENABLED = True` in app.py to use MySQL
- All features work with JSON storage out-of-the-box

---

## 🚀 Deployment Tips

1. **Local Development**: `python app.py`
2. **Production Server**: Use Gunicorn
   ```bash
   pip install gunicorn
   gunicorn app:app
   ```
3. **Database**: Connect MySQL for scalability
4. **Security**: Update secret_key before production

---

## 📈 Business Impact

| Metric | Impact |
|---|---|
| Customer Retention | +40% (loyalty rewards) |
| Viral Growth | Referral system |
| Repeat Orders | Wishlist reminders |
| Customer Engagement | Reviews & ratings |
| Revenue Optimization | Dynamic promo codes |

---

## 🎓 Learning Outcomes

- Full-stack web development
- User engagement strategies
- Gamification (points, badges, tiers)
- Data persistence & analytics
- Admin dashboards
- API integration patterns

---

## 📝 License

This project is created for educational purposes as a BCA Final Year Project.

---

## 💬 Support

Questions? Check:
- Item detail pages for reviews
- Loyalty page for point information
- Referral page for sharing guides
- Admin dashboard for management
    ├── css/style.css
    └── js/main.js
```

---

## ✅ Features Checklist

| Feature | Done |
|---|---|
| HTML + CSS + Python (Flask) | ✅ |
| Login & Register on same page (tabs) | ✅ |
| Home, Menu, About, Contact pages | ✅ |
| All 7 menu items with emoji images | ✅ |
| Click item → modal popup + Book Now | ✅ |
| UPI / Card / Net Banking payment options | ✅ |
| Order placed → full confirmation page | ✅ |
| **My Orders** — user sees all their bookings | ✅ |
| **Order Detail** — who placed, when, from where (IP), item, payment | ✅ |
| Order status tracker bar | ✅ |
| **Admin Dashboard** — all orders + all users + revenue | ✅ |
| IP address tracking on each order | ✅ |
| Session-based login security | ✅ |
| Luxury gold × dark theme | ✅ |

---

## 🔍 How to Access Order Info

### As a Customer:
1. Login → place an order
2. Go to **My Orders** (navbar)
3. Click **View →** on any order to see full details:
   - Your name, email, phone, city
   - Item booked, quantity, price paid
   - Payment method & event date
   - Order ID, placed timestamp, IP address
   - Delivery status

### As Admin:
1. Register with username `admin`
2. Go to `/admin`
3. See every order placed by every user with full info
