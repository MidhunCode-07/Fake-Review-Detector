from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import math
from collections import Counter

app = Flask(__name__)
CORS(app)

# ─── Fake Review Detection Logic ───────────────────────────────────────────────

FAKE_KEYWORDS = [
    "must buy", "best product ever", "life changing", "amazing product",
    "highly recommend", "five stars", "perfect", "love it", "great value",
    "exceeded expectations", "100%", "buy now", "dont hesitate", "hurry",
    "limited time", "click here", "visit our", "check out my",
    "i was skeptical", "i was hesitant", "changed my life",
    "my husband", "my wife", "my friend", "they told me",
]

SUSPICIOUS_PATTERNS = [
    r'\b(buy|purchase|order)\s+(now|today|immediately)\b',
    r'\b(free|discount|sale|offer|deal)\b',
    r'\bverified\s+purchase\b.*\b(not|never)\b',
    r'[A-Z]{3,}',  # Excessive caps
    r'(!{2,})',     # Multiple exclamation marks
    r'(\w)\1{3,}',  # Repeated characters
    r'\b\d+\s*(?:stars?|\/5|out of 5)\b',  # Rating mentioned in text
]

def analyze_review(review_text, rating):
    """Analyze a single review and return a suspicion score (0-100)."""
    score = 0
    flags = []
    text_lower = review_text.lower()

    # 1. Keyword check
    keyword_hits = [kw for kw in FAKE_KEYWORDS if kw in text_lower]
    if keyword_hits:
        score += min(len(keyword_hits) * 8, 30)
        flags.append(f"Suspicious keywords: {', '.join(keyword_hits[:3])}")

    # 2. Pattern matching
    for pattern in SUSPICIOUS_PATTERNS:
        if re.search(pattern, review_text, re.IGNORECASE):
            score += 10
            flags.append(f"Suspicious pattern detected")
            break

    # 3. Text length analysis
    words = review_text.split()
    if len(words) < 5:
        score += 20
        flags.append("Extremely short review")
    elif len(words) > 300:
        score += 10
        flags.append("Unusually long review")

    # 4. Repetition analysis
    word_counts = Counter(words)
    total_words = len(words)
    if total_words > 0:
        most_common_ratio = word_counts.most_common(1)[0][1] / total_words
        if most_common_ratio > 0.15:
            score += 15
            flags.append("High word repetition")

    # 5. Punctuation abuse
    exclamation_count = review_text.count('!')
    if exclamation_count > 3:
        score += min(exclamation_count * 3, 15)
        flags.append(f"Excessive exclamation marks ({exclamation_count})")

    # 6. Rating extremity with generic language
    if rating in [1, 5]:
        generic_phrases = ["great", "terrible", "best", "worst", "amazing", "horrible"]
        generic_hits = sum(1 for p in generic_phrases if p in text_lower)
        if generic_hits >= 2:
            score += 10
            flags.append("Extreme rating with generic language")

    # 7. No specific product details
    specificity_words = ["because", "however", "although", "specifically", "compared",
                         "feature", "quality", "material", "design", "size", "color"]
    specificity_count = sum(1 for w in specificity_words if w in text_lower)
    if specificity_count == 0 and len(words) < 30:
        score += 10
        flags.append("Lacks specific product details")

    # 8. Sentiment vs Rating mismatch
    positive_words = ["good", "great", "excellent", "love", "perfect", "wonderful"]
    negative_words = ["bad", "terrible", "awful", "hate", "horrible", "worst", "broken"]
    pos_count = sum(1 for w in positive_words if w in text_lower)
    neg_count = sum(1 for w in negative_words if w in text_lower)

    if rating >= 4 and neg_count > pos_count:
        score += 20
        flags.append("Negative sentiment with high rating (mismatch)")
    elif rating <= 2 and pos_count > neg_count:
        score += 20
        flags.append("Positive sentiment with low rating (mismatch)")

    score = min(score, 100)
    is_fake = score >= 45

    return {
        "score": score,
        "is_fake": is_fake,
        "confidence": get_confidence_label(score),
        "flags": list(set(flags))[:4]
    }


def get_confidence_label(score):
    if score >= 70:
        return "High"
    elif score >= 45:
        return "Medium"
    elif score >= 25:
        return "Low"
    else:
        return "Genuine"


def compute_product_stats(reviews):
    fake = [r for r in reviews if r["analysis"]["is_fake"]]
    genuine = [r for r in reviews if not r["analysis"]["is_fake"]]

    all_ratings = [r["rating"] for r in reviews]
    genuine_ratings = [r["rating"] for r in genuine]

    avg_all = sum(all_ratings) / len(all_ratings) if all_ratings else 0
    avg_genuine = sum(genuine_ratings) / len(genuine_ratings) if genuine_ratings else 0

    # Rating distribution
    rating_dist = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for r in reviews:
        rating_dist[r["rating"]] += 1

    # Detect rating manipulation
    extremes = rating_dist[1] + rating_dist[5]
    middle = rating_dist[2] + rating_dist[3] + rating_dist[4]
    rating_manipulation = extremes > middle * 1.5 if middle > 0 else False

    return {
        "total": len(reviews),
        "fake_count": len(fake),
        "genuine_count": len(genuine),
        "fake_percentage": round(len(fake) / len(reviews) * 100, 1) if reviews else 0,
        "avg_rating_all": round(avg_all, 2),
        "avg_rating_genuine": round(avg_genuine, 2),
        "rating_distribution": rating_dist,
        "rating_manipulation_detected": rating_manipulation,
        "trust_score": max(0, round(100 - (len(fake) / len(reviews) * 100 * 0.8), 1)) if reviews else 0
    }


# ─── API Routes ─────────────────────────────────────────────────────────────────

@app.route('/api/analyze', methods=['POST'])
def analyze_reviews():
    data = request.json
    product_name = data.get("product_name", "Unknown Product")
    reviews_raw = data.get("reviews", [])

    if not reviews_raw:
        return jsonify({"error": "No reviews provided"}), 400

    analyzed_reviews = []
    for r in reviews_raw:
        analysis = analyze_review(r.get("text", ""), r.get("rating", 3))
        analyzed_reviews.append({
            "id": r.get("id"),
            "author": r.get("author", "Anonymous"),
            "rating": r.get("rating", 3),
            "text": r.get("text", ""),
            "date": r.get("date", ""),
            "platform": r.get("platform", "Unknown"),
            "analysis": analysis
        })

    stats = compute_product_stats(analyzed_reviews)

    return jsonify({
        "product_name": product_name,
        "stats": stats,
        "reviews": analyzed_reviews
    })


@app.route('/api/demo', methods=['GET'])
def demo_data():
    """Returns demo reviews for testing."""
    product = request.args.get("product", "Wireless Earbuds Pro X200")
    demo_reviews = [
        {"id": 1, "author": "Sarah M.", "rating": 5, "platform": "Amazon",
         "date": "2024-01-15", "text": "These earbuds have excellent noise cancellation. I use them during my morning commute and the battery lasts about 7 hours which matches the description. The fit is comfortable for my ears, though the case is a bit bulky."},
        {"id": 2, "author": "J_reviewer99", "rating": 5, "platform": "Amazon",
         "date": "2024-01-16", "text": "BEST PRODUCT EVER!!! Must buy now!!! Life changing!!! Amazing amazing amazing!! Highly recommend to everyone!!!"},
        {"id": 3, "author": "TechReview2024", "rating": 4, "platform": "Flipkart",
         "date": "2024-01-18", "text": "Good sound quality for the price. Bass is decent but not exceptional. Pairing was straightforward. However the mic quality during calls is mediocre - my colleagues said I sounded distant."},
        {"id": 4, "author": "HappyCustomer", "rating": 5, "platform": "Amazon",
         "date": "2024-01-19", "text": "My wife told me about this product and I was skeptical at first but now my life has completely changed! Visit our website for more deals like this one!"},
        {"id": 5, "author": "Mike T.", "rating": 2, "platform": "Flipkart",
         "date": "2024-01-20", "text": "Disappointed with the build quality. The right earbud stopped working after 3 weeks of normal use. Customer support took 2 weeks to respond. For this price point I expected better durability."},
        {"id": 6, "author": "FakeUser_Bot", "rating": 1, "platform": "Amazon",
         "date": "2024-01-21", "text": "Terrible!!! Worst product EVER!! Do NOT buy this!! Everyone should avoid this completely bad product!!!"},
        {"id": 7, "author": "Priya R.", "rating": 4, "platform": "Myntra",
         "date": "2024-01-22", "text": "I've been using these for about 2 months now. Sound quality is good for music and podcasts. The touch controls are responsive. My only complaint is that they fall out slightly during intense workouts."},
        {"id": 8, "author": "anonymous1234", "rating": 5, "platform": "Amazon",
         "date": "2024-01-23", "text": "100% recommend buy now hurry limited time offer dont hesitate perfect product amazing deal!!"},
        {"id": 9, "author": "David K.", "rating": 3, "platform": "Amazon",
         "date": "2024-01-24", "text": "Average product. Sound is okay, connectivity is stable within 10 meters. The case charges the earbuds about 3 times. Not worth the full price but decent in a sale."},
        {"id": 10, "author": "Verified_Buyer", "rating": 5, "platform": "Flipkart",
         "date": "2024-01-25", "text": "Exceeded expectations! The active noise cancellation blocks out my noisy office effectively. Setup took under a minute. The companion app provides useful EQ controls. Wearing them 4-5 hours daily with no discomfort."},
    ]
    return jsonify({"product": product, "reviews": demo_reviews})


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "version": "1.0.0"})


if __name__ == '__main__':
    print("🔍 Fake Review Detector API running on http://localhost:5000")
    app.run(debug=True, port=5000)