import random
from datetime import datetime, timedelta, timezone
import sqlalchemy as sa
from app import app, db
from app.models import User, Post

NAMES = ["john", "susan", "mary", "david", "anna"]
BODIES = [
    "Szép nap van ma!",
    "Just finished chapter 8 of the Flask tutorial.",
    "Who wants to go hiking this weekend?",
    "A bosszuállók egy király film",
    "Learning Python is fun.",
    "Coffee first, code later.",
    "Hello, world!",
    "Anyone here likes chess?",
    "Új projekt indul holnap.",
    "Debugging all day, but it works now.",
]

random.seed(1)

with app.app_context():
    # users
    users = []
    for name in NAMES:
        u = db.session.scalar(sa.select(User).where(User.username == name))
        if u is None:
            u = User(username=name, email=f"{name}@example.com",
                     about_me=f"Hi, I am {name}.")
            u.set_password("test123")
            db.session.add(u)
        users.append(u)
    db.session.commit()

    # each user follows the next two users in the list
    for i, u in enumerate(users):
        u.follow(users[(i + 1) % len(users)])
        u.follow(users[(i + 2) % len(users)])
    db.session.commit()

    # posts (only if there are none yet)
    if db.session.scalar(sa.select(sa.func.count()).select_from(Post)) == 0:
        now = datetime.now(timezone.utc)
        for i in range(30):
            author = users[i % len(users)]
            post = Post(body=f"{random.choice(BODIES)} (#{i + 1})",
                        author=author,
                        timestamp=now - timedelta(minutes=7 * i))
            db.session.add(post)
        db.session.commit()

    print("Users:", db.session.scalar(sa.select(sa.func.count()).select_from(User)))
    print("Posts:", db.session.scalar(sa.select(sa.func.count()).select_from(Post)))