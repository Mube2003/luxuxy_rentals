🚀 QUICK START GUIDE - NEW FEATURES
====================================

## 1️⃣ START THE APPLICATION

```bash
cd c:\Users\5\Desktop\luxury_rentals
python app.py
```

Open: http://localhost:5000


## 2️⃣ CREATE TEST ACCOUNTS

### Regular Customer
- Go to Register tab
- Fill details (referral code optional)
- Username: testuser
- Password: test123

### Admin Account (for testing)
- Username: admin
- Password: admin123 (set this first time)


## 3️⃣ TRY LOYALTY POINTS

After login:
1. Click "💎 Loyalty" in navbar
2. See your current points (0 initially)
3. Check how to earn points
4. View your referral code

How to earn points:
• Make a purchase → 1 point per ₹
• Add to wishlist → 5 points
• Write review → 10 points


## 4️⃣ TEST WISHLIST

1. Go to Menu
2. Click on any item
3. Click "❤️ Add to Wishlist" button
4. View all wishlists at "❤️ Wishlist" link
5. Click wishlist items to rent immediately


## 5️⃣ ADD REVIEWS

On item detail page:
1. Scroll to "Customer Reviews & Ratings"
2. Select star rating (click stars)
3. Write your review
4. Click "Submit Review"
5. See your review below with others
6. Earn 10 loyalty points!


## 6️⃣ TEST REFERRAL SYSTEM

1. Click "👥 Refer & Earn" in navbar
2. See your unique referral code
3. Copy code and share
4. Share via WhatsApp/Twitter buttons
5. New friends get 250 bonus points
6. You get 500 bonus points!


## 7️⃣ PLACE ORDERS & EARN POINTS

1. Add items to cart
2. Go to checkout
3. Complete order
4. Check loyalty page
5. Points = order total (₹2500 order = 2500 points!)


## 8️⃣ ADMIN: CREATE PROMO CODES

1. Go to /admin (if admin user)
2. Scroll to "🏷️ Promo Codes & Discounts"
3. Enter code name: SUMMER20
4. Enter discount: 200 (₹) or 20 (%)
5. Select type: Fixed Amount or Percentage
6. Click "Create"
7. New code appears in table below


## 9️⃣ APPLY PROMO CODES (Customer)

At checkout:
1. Enter promo code if available
2. Discount applies to order total
3. See updated total price


## 🔟 VIEW ANALYTICS

As customer:
1. Click "Dashboard" link
2. See your order history
3. View revenue charts
4. Track completed orders

As admin:
1. Go to /admin
2. See total revenue
3. View order statistics
4. Monitor user count
5. Manage all orders


## 📋 NAVIGATION MAP

Main Navigation (in navbar):
├─ Home - Landing page
├─ Menu - Browse items
├─ ❤️ Wishlist - Saved items
├─ About - About page
├─ Contact - Contact form
├─ My Orders - Order history
├─ 💎 Loyalty - Points info
├─ 👥 Refer & Earn - Referral
├─ Profile - User settings
├─ Dashboard - Personal analytics
└─ (Admin only)
   ├─ ⚙ Admin - Main dashboard
   └─ 📬 Messages - Customer messages


## 🎮 GAMIFICATION FLOW

User Registration
    ↓
+100 points (new member bonus)
    ↓
Add to Wishlist
    +5 points × items
    ↓
First Purchase
    +1 point per ₹
    ↓
Write Review
    +10 points
    ↓
Reach Silver (500 pts)
    • 10% bonus on purchases
    • Free delivery
    ↓
Refer Friends
    +500 points per referral
    +250 points to friend
    ↓
Reach Gold (2000 pts)
    • 20% bonus on purchases
    • VIP support
    • Monthly surprises


## 💰 POINTS CALCULATIONS

Points Earned:
• New registration: 100 points
• Wishlist add: 5 points each
• Product review: 10 points each
• Purchase: ₹1 = 1 point
  (₹2500 purchase = 2500 points)
• Referral: 500 points
• Referred friend: 250 points

Points Value:
• 1 point = ₹0.50
• 100 points = ₹50
• 500 points = ₹250 discount
• 2000 points = ₹1000 discount


## 🧪 TEST SCENARIOS

### Scenario 1: New User Journey
1. Register with referral code REF-ADMIN
2. Get 250 bonus points
3. Add 2 items to wishlist (+10 points)
4. Buy 1 item for ₹3000 (+3000 points)
5. Leave review (+10 points)
Total: 3270 points earned!

### Scenario 2: Referral Chain
1. User A has REF-USERA
2. User B registers with REF-USERA
3. User B gets 250 points
4. User A gets 500 points
5. User B makes purchase
6. Both users get tier benefits

### Scenario 3: Promo Code Usage
1. Admin creates: DIWALI500 (₹500 fixed)
2. Customer applies at checkout
3. Order ₹8000 → ₹7500 after promo
4. Points still earned on ₹7500
5. Admin can deactivate promo


## ⚙️ CONFIGURATION

Default Settings:
• DB_ENABLED = False (uses JSON)
• Cart storage in session
• Points in loyalty_points.json
• Reviews in reviews.json
• Wishlist in wishlist.json
• Promo codes in promo_codes.json

To use MySQL:
• Set DB_ENABLED = True in app.py
• Configure database credentials
• Run initialize_db()


## 🐛 TROUBLESHOOTING

Issue: Points not showing
→ Check loyalty_points.json exists
→ Refresh page
→ Make a purchase to trigger

Issue: Wishlist empty
→ Check wishlist.json exists
→ Click "Add to Wishlist" again
→ Clear browser cache

Issue: Review not appearing
→ Refresh page (AJAX loads)
→ Check reviews.json exists
→ Verify review was submitted

Issue: Promo code not working
→ Check code spelling (case-insensitive)
→ Verify code is active
→ Check min purchase requirement


## 📊 PERFORMANCE TIPS

Optimize experience:
• Clear browser cache regularly
• Refresh loyalty page to sync points
• Use incognito for testing multiple accounts
• Check browser console for JavaScript errors


## 🎓 LEARNING VALUE

This project demonstrates:
✓ Gamification mechanics
✓ User engagement strategies
✓ Loyalty program design
✓ Referral system implementation
✓ Database design patterns
✓ Flask best practices
✓ Full-stack development
✓ UX/UI principles


## 📞 SUPPORT

Questions about:
• Loyalty? → Go to /loyalty page
• Referrals? → Go to /referral page  
• Reviews? → Scroll to item reviews
• Admin? → Go to /admin dashboard
• Wishlists? → Click ❤️ Wishlist link


## 🎉 ENJOY!

Your luxury rentals platform is now unique with:
✓ Loyalty rewards
✓ Referral incentives
✓ Smart wishlist
✓ Social proof (reviews)
✓ Flexible discounts
✓ Better analytics

Start earning and sharing! 💎✨
