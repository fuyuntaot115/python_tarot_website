from webapp import app 
from flask import render_template, send_from_directory
from webapp import cards
import os
import random

# 广告文件路由
@app.route('/ads.txt')
def ads_txt():
    return send_from_directory(os.path.dirname(app.root_path), 'ads.txt')

# 首页
@app.route('/')
def index():
    return render_template(
        "index.html", 
        title="Home",
        description="Free online tarot readings, including one-card and three-card spreads. Learn tarot meanings and improve your interpretation skills with our study guide.",
        keywords="free tarot reading, online tarot, one card reading, three card spread, tarot meanings"
    )

# 塔罗学习页面
@app.route('/tarot-study', strict_slashes=False)
def all_cards():
    return render_template(
        "tarot_study.html",
        title="Tarot Study Guide",
        description="Comprehensive tarot study guide: meanings of wands, coins, cups, and swords. Learn tarot card interpretations for beginners and advanced readers.",
        keywords="tarot study, tarot card meanings, wands, coins, cups, swords, tarot guide"
    )

# 推荐阅读页面
@app.route('/reading-list', strict_slashes=False)
def reading_list():
    return render_template(
        "reading_list.html",
        title="Recommended Tarot Books",
        description="Curated list of tarot books for beginners and advanced readers. Enhance your tarot knowledge with these essential resources.",
        keywords="tarot books, tarot reading guides, best tarot books, tarot resources"
    )

# 单张牌占卜
@app.route('/one-card', strict_slashes=False)
def one_card():
    my_deck = cards.get_deck()
    my_card = cards.get_card(my_deck)
    
    card_title = f"{my_card[0]['name']} Tarot Card"
    card_desc = f"Interpretation of the {my_card[0]['name']} tarot card, including its meaning and reversed meaning."
    
    if my_card[0]['cardtype'] == "major":
        return render_template(
            "one_card.html",
            name=my_card[0]['name'],
            title=card_title,
            description=card_desc,
            keywords=f"{my_card[0]['name']}, major arcana, tarot meaning, reversed tarot",
            rev=my_card[1],
            meaning=my_card[0]['desc'],
            message=my_card[0]['message'],
            reversed_meaning=my_card[0]['rdesc'],
            image=my_card[0]['image'],
            url=my_card[0]['url'],
            cardtype=my_card[0]['cardtype']
        )
    else:
        return render_template(
            "one_card.html",
            name=my_card[0]['name'],
            title=card_title,
            description=card_desc,
            keywords=f"{my_card[0]['name']}, minor arcana, tarot meaning, reversed tarot",
            rev=my_card[1],
            meaning=my_card[0]['desc'],
            reversed_meaning=my_card[0]['rdesc'],
            image=my_card[0]['image'],
            url=my_card[0]['url'],
            cardtype=my_card[0]['cardtype']
        )

# 三张牌占卜
@app.route('/three-cards', strict_slashes=False)
def more_cards():
    my_deck = cards.get_deck()
    hand = []
    num = 1
    while num < 4:
        my_card = cards.get_card(my_deck)
        hand.append(my_card)
        num += 1
    return render_template(
        "three_cards.html", 
        hand=hand, 
        title="Three Card Tarot Spread",
        description="Three card tarot spread interpretation: past, present, and future insights. Get guidance on your current situation with this classic spread.",
        keywords="three card spread, tarot past present future, tarot spread interpretation"
    )

# 特定牌详情
@app.route('/one-card/<card_url>')
def specific_card(card_url):
    my_deck = cards.get_deck()
    my_card = list(filter(lambda c: c['url'] == card_url, my_deck))[0]
    
    # 导航链接处理
    if my_card['sequence'] > 1:
        previous_card_url = f'/one-card/{list(filter(lambda c: c["sequence"] == (my_card["sequence"] -1), my_deck))[0]["url"]}'
    else:
        previous_card_url = '/tarot-study'
        
    if my_card['sequence'] < 78:
        next_card_url = f'/one-card/{list(filter(lambda c: c["sequence"] == (my_card["sequence"] +1), my_deck))[0]["url"]}'
    else:
        next_card_url = '/tarot-study'
    
    card_title = f"{my_card['name']} Tarot Card Details"
    card_desc = f"Detailed interpretation of the {my_card['name']} tarot card, including symbolism, meanings, and reversed interpretations."
    
    if my_card['cardtype'] == "major":
        return render_template(
            "specific_card.html",
            name=my_card['name'],
            title=card_title,
            description=card_desc,
            keywords=f"{my_card['name']}, major arcana, tarot symbolism, {my_card['hebrew_letter']}, qabalah",
            meaning=my_card['desc'],
            message=my_card['message'],
            reversed_meaning=my_card['rdesc'],
            hebrew_letter=my_card['hebrew_letter'],
            qabalah=my_card['qabalah'],
            meditation=my_card['meditation'],
            image=my_card['image'],
            previous=previous_card_url,
            next=next_card_url,
            sequence=my_card['sequence'],
            cardtype=my_card['cardtype']
        )
    else:
        return render_template(
            "specific_card.html",
            name=my_card['name'],
            title=card_title,
            description=card_desc,
            keywords=f"{my_card['name']}, minor arcana, tarot symbolism, {my_card['qabalah']}",
            meaning=my_card['desc'],
            reversed_meaning=my_card['rdesc'],
            qabalah=my_card['qabalah'],
            image=my_card['image'],
            previous=previous_card_url,
            next=next_card_url,
            sequence=my_card['sequence'],
            cardtype=my_card['cardtype']
        )