

import json
import streamlit as st
import database as db

# ==================================================
# HANOUTI — MODERN MOROCCAN MARKETPLACE
# ==================================================

st.set_page_config(
    page_title="HANOUTI | Moroccan Marketplace",
    page_icon="🪬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

db.init_db()


with st.expander("Supabase products test"):
    if st.button("Test product table"):
        try:
            products = db.get_supabase_products()
            st.success(
                f"Supabase product read successful: "
                f"{len(products)} published product(s)."
            )
        except Exception as error:
            st.error("Could not read Supabase products.")
            st.caption(f"Error type: {type(error).__name__}")

# TEMPORARY: test Supabase connection
with st.expander("Supabase connection test"):
    if st.button("Test Supabase connection"):
        try:
            result = db.test_supabase_connection()
            st.success("Connected to Supabase successfully!")
            st.write("Cities table is accessible.")
            st.write(result)
        except Exception as error:
            st.error("Connection test failed.")
            st.caption(f"Error type: {type(error).__name__}")


# -------------------- TRANSLATIONS --------------------

TEXT = {
    "EN": {
        "shop": "SHOP",
        "stylist": "AI STYLIST",
        "cart": "CART",
        "account": "ACCOUNT",
        "add_items": "ADD ITEMS",
        "hero": "YOUR STYLE. YOUR RULES.",
        "subtitle": "Discover your next streetwear essential.",
        "search": "Search products",
        "category": "Category",
        "all": "All",
        "sort": "Sort by",
        "featured": "Featured",
        "low": "Price: low to high",
        "high": "Price: high to low",
        "add": "ADD TO CART",
        "details": "VIEW DETAILS ↗",
        "back": "← BACK TO SHOP",
        "empty": "No products found. Try another search.",
        "empty_cart": "Your cart is empty.",
        "remove": "REMOVE",
        "checkout": "CHECKOUT",
        "name": "Your name",
        "save": "SAVE PROFILE",
        "saved": "Profile saved!",
        "ask": "Describe your style or ask for an outfit...",
        "send": "GET STYLE ADVICE",
        "choose_size": "Choose your size",
        "quantity": "Quantity",
        "subtotal": "Subtotal",
        "total": "TOTAL",
        "language": "Language",
        "welcome": "WELCOME TO YOUR WARDROBE",
        "no_image": "No image available",
        "add_shop": "REGISTER A SHOP",
        "shop_name": "Shop name",
        "city": "City",
        "address": "Shop address",
        "phone": "Phone number",
        "save_shop": "SAVE SHOP",
        "add_product": "ADD A PRODUCT",
        "choose_shop": "Choose shop",
        "product_name": "Product name",
        "description": "Description",
        "price": "Price in MAD",
        "color": "Color",
        "sizes": "Sizes (S, M, L, XL)",
        "style": "Style",
        "image_url": "Image URL (optional)",
        "in_stock": "In stock",
        "save_product": "SAVE PRODUCT",
        "shop_saved": "Shop saved successfully!",
        "product_saved": "Product saved successfully!",
        "no_shops": "Register a shop before adding products.",
        "seller": "Shop",
    },
    "FR": {
        "shop": "BOUTIQUE",
        "stylist": "STYLISTE IA",
        "cart": "PANIER",
        "account": "COMPTE",
        "add_items": "AJOUTER",
        "hero": "TON STYLE. TES RÈGLES.",
        "subtitle": "Découvre tes prochains essentiels streetwear.",
        "search": "Rechercher un produit",
        "category": "Catégorie",
        "all": "Tout",
        "sort": "Trier par",
        "featured": "À la une",
        "low": "Prix croissant",
        "high": "Prix décroissant",
        "add": "AJOUTER AU PANIER",
        "details": "VOIR LES DÉTAILS ↗",
        "back": "← RETOUR À LA BOUTIQUE",
        "empty": "Aucun produit trouvé. Essaie une autre recherche.",
        "empty_cart": "Ton panier est vide.",
        "remove": "SUPPRIMER",
        "checkout": "COMMANDER",
        "name": "Ton nom",
        "save": "ENREGISTRER LE PROFIL",
        "saved": "Profil enregistré !",
        "ask": "Décris ton style ou demande une tenue...",
        "send": "OBTENIR DES CONSEILS",
        "choose_size": "Choisir la taille",
        "quantity": "Quantité",
        "subtotal": "Sous-total",
        "total": "TOTAL",
        "language": "Langue",
        "welcome": "BIENVENUE DANS TON DRESSING",
        "no_image": "Aucune image disponible",
        "add_shop": "ENREGISTRER UNE BOUTIQUE",
        "shop_name": "Nom de la boutique",
        "city": "Ville",
        "address": "Adresse",
        "phone": "Téléphone",
        "save_shop": "ENREGISTRER",
        "add_product": "AJOUTER UN PRODUIT",
        "choose_shop": "Choisir une boutique",
        "product_name": "Nom du produit",
        "description": "Description",
        "price": "Prix en MAD",
        "color": "Couleur",
        "sizes": "Tailles (S, M, L, XL)",
        "style": "Style",
        "image_url": "URL de l'image (facultatif)",
        "in_stock": "En stock",
        "save_product": "ENREGISTRER LE PRODUIT",
        "shop_saved": "Boutique enregistrée !",
        "product_saved": "Produit enregistré !",
        "no_shops": "Enregistre d'abord une boutique.",
        "seller": "Boutique",
    },
}

# -------------------- SESSION STATE --------------------

defaults = {
    "page": "Shop",
    "selected_product": None,
    "cart": {},
    "username": "",
    "language": "EN",
    "stylist_answer": "",
    "stylist_question": "",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

lang = st.session_state.language
t = TEXT[lang]

# -------------------- DATABASE --------------------


def load_products():
    products = []

    for row in db.get_supabase_products():
        product = dict(row)
        product["image"] = product.get("image_url", "")
        product["size"] = product.get("sizes", "")
        product["shop_name"] = product.get("shop_name", "")
        product["shop_address"] = product.get("shop_address", "")
        product["shop_phone"] = product.get("shop_phone", "")
        products.append(product)

    return products


def load_shops():
    return [dict(shop) for shop in db.get_shops()]


def get_product(product_id):
    for product in load_products():
        if product["id"] == product_id:
            return product
    return None


def money(amount):
    return f"{float(amount):,.2f} MAD"


def go_to(page):
    st.session_state.page = page


def add_to_cart(product_id, size, quantity=1):
    key = (product_id, size)
    current = st.session_state.cart.get(key, 0)
    st.session_state.cart[key] = current + int(quantity)


def cart_count():
    return sum(st.session_state.cart.values())


def cart_total():
    total = 0

    for (product_id, size), quantity in st.session_state.cart.items():
        product = get_product(product_id)

        if product:
            total += float(product["price"]) * quantity

    return total


def show_product_image(product, use_container_width=True):
    image_url = str(product.get("image", "") or "").strip()

    if image_url.startswith(("https://", "http://")):
        st.image(image_url, use_container_width=use_container_width)
    else:
        st.markdown(
            f"""
            <div style="
                background:#181818;
                border:1px solid #303030;
                padding:65px 10px;
                text-align:center;
                color:#999;
                letter-spacing:2px;
            ">
                🖤<br>{t["no_image"].upper()}
            </div>
            """,
            unsafe_allow_html=True,
        )


# -------------------- DESIGN --------------------

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: #0b0b0b;
        color: #f5f5f5;
    }

    [data-testid="stHeader"] {
        background: #0b0b0b;
    }

    [data-testid="stSidebar"] {
        background: #111111;
    }

    h1, h2, h3, p, label {
        color: #f5f5f5;
    }

    .brand {
        font-size: 35px;
        font-weight: 900;
        letter-spacing: 5px;
        text-align: center;
        padding: 15px 0 0 0;
    }

    .tagline {
        color: #a3a3a3;
        text-align: center;
        letter-spacing: 3px;
        font-size: 11px;
        margin-bottom: 20px;
    }

    .hero {
        padding: 60px 25px;
        margin: 20px 0 30px 0;
        background: linear-gradient(135deg, #222222, #101010 70%);
        border: 1px solid #303030;
        text-align: center;
        border-radius: 5px;
    }

    .hero h1 {
        font-size: clamp(30px, 5vw, 58px);
        font-weight: 900;
        letter-spacing: 2px;
        margin-bottom: 10px;
    }

    .hero p {
        color: #bdbdbd;
        letter-spacing: 1px;
    }

    .product-card {
        padding: 12px 2px 15px 2px;
        border-bottom: 1px solid #333333;
        margin-bottom: 10px;
    }

    .product-meta {
        color: #a3a3a3;
        font-size: 11px;
        letter-spacing: 1px;
        margin-top: 7px;
    }

    .product-name {
        font-size: 17px;
        font-weight: 700;
        margin-top: 8px;
    }

    .price {
        font-size: 16px;
        font-weight: 700;
        margin-top: 9px;
    }

    .section-label {
        font-size: 12px;
        color: #a3a3a3;
        letter-spacing: 3px;
        margin-bottom: 5px;
    }

    div.stButton > button {
        border-radius: 2px;
        border: 1px solid #666666;
        background: #111111;
        color: white;
        font-weight: 700;
        letter-spacing: 1px;
        min-height: 42px;
    }

    div.stButton > button:hover {
        border-color: white;
        color: white;
        background: #292929;
    }

    div.stButton > button[kind="primary"] {
        background: white;
        color: black;
        border-color: white;
    }

    div.stButton > button[kind="primary"]:hover {
        background: #dddddd;
        color: black;
    }

    [data-testid="stImage"] img {
        border-radius: 3px;
    }

    hr {
        border-color: #333333;
    }

    .footer {
        text-align: center;
        color: #777777;
        font-size: 11px;
        letter-spacing: 2px;
        padding: 30px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------- HEADER --------------------

st.markdown('<div class="brand">STYLEMIND</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="tagline">STREETWEAR · SELF-EXPRESSION · AI</div>',
    unsafe_allow_html=True,
)

language_col, space_col = st.columns([1, 4])

with language_col:
    new_language = st.selectbox(
        t["language"],
        ["EN", "FR"],
        index=0 if lang == "EN" else 1,
        key="language_picker",
    )

    if new_language != st.session_state.language:
        st.session_state.language = new_language
        st.rerun()

st.divider()

nav1, nav2, nav3, nav4, nav5 = st.columns(5)

with nav1:
    if st.button(t["shop"], use_container_width=True):
        go_to("Shop")
        st.rerun()

with nav2:
    if st.button(t["stylist"], use_container_width=True):
        go_to("Stylist")
        st.rerun()

with nav3:
    if st.button(f'{t["cart"]} ({cart_count()})', use_container_width=True):
        go_to("Cart")
        st.rerun()

with nav4:
    if st.button(t["account"], use_container_width=True):
        go_to("Account")
        st.rerun()

with nav5:
    if st.button(t["add_items"], use_container_width=True):
        go_to("Add Items")
        st.rerun()

st.divider()

# ==================================================
# SHOP PAGE
# ==================================================

if st.session_state.page == "Shop":

    st.markdown(
        f"""
        <div class="hero">
            <div class="section-label">{t["welcome"]}</div>
            <h1>{t["hero"]}</h1>
            <p>{t["subtitle"]}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    products = load_products()

    if not products:
        st.markdown("### NEW SEASON / EVERYDAY ESSENTIALS")
        st.info("No products have been listed yet.")

        if st.button(t["add_items"], type="primary"):
            go_to("Add Items")
            st.rerun()

    else:
        search_col, category_col, sort_col = st.columns([2, 1, 1])

        with search_col:
            search = st.text_input(
                t["search"],
                placeholder="Hoodie, black, sneakers...",
            ).strip().lower()

        categories = [t["all"]] + sorted({
            str(p.get("category", "Other"))
            for p in products
        })

        with category_col:
            category = st.selectbox(t["category"], categories)

        with sort_col:
            sort_option = st.selectbox(
                t["sort"],
                [t["featured"], t["low"], t["high"]],
            )

        filtered = []

        for product in products:
            searchable = " ".join([
                str(product.get("name", "")),
                str(product.get("category", "")),
                str(product.get("color", "")),
                str(product.get("style", "")),
                str(product.get("shop_name", "")),
            ]).lower()

            if search and search not in searchable:
                continue

            if category != t["all"] and category != product.get("category", ""):
                continue

            filtered.append(product)

        if sort_option == t["low"]:
            filtered.sort(key=lambda p: float(p["price"]))
        elif sort_option == t["high"]:
            filtered.sort(key=lambda p: float(p["price"]), reverse=True)

        st.write("")
        st.markdown("### NEW SEASON / EVERYDAY ESSENTIALS")

        if not filtered:
            st.info(t["empty"])

        for start in range(0, len(filtered), 3):
            row_products = filtered[start:start + 3]
            cols = st.columns(3)

            for col, product in zip(cols, row_products):
                with col:
                    show_product_image(product)

                    st.markdown(
                        f"""
                        <div class="product-card">
                            <div class="product-meta">
                                {product.get("category", "").upper()} /
                                {product.get("color", "").upper()}
                            </div>
                            <div class="product-name">{product["name"]}</div>
                            <div class="product-meta">
                                Sizes: {product.get("size") or "Not specified"}
                            </div>
                            <div class="product-meta">
                                SHOP: {product.get("shop_name") or "Local shop"}
                            </div>
                            <div class="price">{money(product["price"])}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    if st.button(
                        t["details"],
                        key=f"details_{product['id']}",
                        use_container_width=True,
                    ):
                        st.session_state.selected_product = product["id"]
                        go_to("Product")
                        st.rerun()

                    sizes = [
                        s.strip()
                        for s in str(product.get("size") or "").split(",")
                        if s.strip()
                    ] or ["One size"]

                    quick_size = st.selectbox(
                        t["choose_size"],
                        sizes,
                        key=f"quick_size_{product['id']}",
                    )

                    if st.button(
                        t["add"],
                        key=f"shop_add_{product['id']}",
                        use_container_width=True,
                    ):
                        add_to_cart(product["id"], quick_size)
                        st.toast("Added to cart ✓")

# ==================================================
# PRODUCT DETAILS
# ==================================================

elif st.session_state.page == "Product":

    product = get_product(st.session_state.selected_product)

    if product is None:
        st.warning("Product not found.")

        if st.button(t["back"]):
            go_to("Shop")
            st.rerun()

    else:
        if st.button(t["back"]):
            go_to("Shop")
            st.rerun()

        st.divider()
        image_col, info_col = st.columns([1.1, 1])

        with image_col:
            show_product_image(product)

        with info_col:
            st.markdown(
                f'<div class="section-label">STYLEMIND / '
                f'{product.get("category", "").upper()}</div>',
                unsafe_allow_html=True,
            )

            st.title(product["name"])
            st.subheader(money(product["price"]))
            st.write(product.get("description") or "No description provided.")
            st.write(f'**Color:** {product.get("color") or "—"}')
            st.write(f'**Available sizes:** {product.get("size") or "—"}')
            st.write(f'**Shop:** {product.get("shop_name") or "Local shop"}')

            if product.get("shop_address"):
                st.write(f'**Address:** {product["shop_address"]}')

            if product.get("shop_phone"):
                st.write(f'**Phone:** {product["shop_phone"]}')

            sizes = [
                s.strip()
                for s in str(product.get("size") or "").split(",")
                if s.strip()
            ] or ["One size"]

            selected_size = st.selectbox(
                t["choose_size"],
                sizes,
                key=f"detail_size_{product['id']}",
            )

            quantity = st.number_input(
                t["quantity"],
                min_value=1,
                max_value=10,
                value=1,
                step=1,
                key=f"detail_quantity_{product['id']}",
            )

            st.markdown(
                f"**{t['subtotal']}:** "
                f"{money(float(product['price']) * quantity)}"
            )

            if st.button(
                t["add"],
                type="primary",
                use_container_width=True,
                key=f"detail_add_{product['id']}",
            ):
                add_to_cart(product["id"], selected_size, quantity)
                st.success("Added to cart ✓")

# ==================================================
# AI STYLIST — GROQ API
# ==================================================

elif st.session_state.page == "Stylist":

    st.markdown(
        '<div class="section-label">YOUR PERSONAL FASHION ASSISTANT</div>',
        unsafe_allow_html=True,
    )

    st.title("Meet your AI Stylist 🖤")
    st.write(
        "Tell me what you like, where you're going, "
        "or which pieces you want to style together."
    )

    example_col1, example_col2 = st.columns(2)

    with example_col1:
        st.caption("• Build me a black streetwear outfit.")
        st.caption("• What should I wear for a casual date?")

    with example_col2:
        st.caption("• Style an oversized hoodie.")
        st.caption("• Give me a minimal outfit on a budget.")

    question = st.text_area(
        t["ask"],
        value=st.session_state.stylist_question,
        height=120,
        placeholder="I like black clothes and oversized fits...",
        key="stylist_input",
    )

    if st.button(t["send"], type="primary", use_container_width=True):
        if not question.strip():
            st.warning("Write a question first.")

        else:
            try:
                api_key = st.secrets["GROQ_API_KEY"]

                if not api_key:
                    st.error("GROQ_API_KEY is empty in Streamlit Secrets.")
                    st.stop()

                from groq import Groq

                st.session_state.stylist_question = question
                products = load_products()

                inventory = [
                    {
                        "name": p["name"],
                        "category": p.get("category", ""),
                        "price_MAD": p["price"],
                        "color": p.get("color", ""),
                        "sizes": p.get("size", ""),
                        "style": p.get("style", ""),
                        "shop": p.get("shop_name", ""),
                    }
                    for p in products
                ]

                prompt = f"""
You are StyleMind, a friendly streetwear stylist for a local
fashion marketplace in Tetouan, Morocco.

Reply in the same language as the customer.
Be helpful, clear, creative, and practical.
Recommend products from the inventory when they fit the request.
Never invent product names, prices, sizes, shops, or availability.
If no listed products match, say so honestly and give general styling
advice without pretending those items are available in the store.
Prices are in Moroccan dirhams (MAD).

AVAILABLE INVENTORY:
{json.dumps(inventory, ensure_ascii=False)}

CUSTOMER REQUEST:
{question}
"""

                client = Groq(api_key=api_key)

                with st.spinner("Your stylist is thinking..."):
                    response = client.chat.completions.create(
                        model="openai/gpt-oss-120b",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are StyleMind, a friendly personal "
                                    "streetwear stylist. Reply in the "
                                    "customer's language. Be practical and "
                                    "never fabricate store inventory."
                                ),
                            },
                            {
                                "role": "user",
                                "content": prompt,
                            },
                        ],
                        temperature=0.7,
                        max_tokens=900,
                    )

                answer = response.choices[0].message.content

                st.session_state.stylist_answer = (
                    answer or "Sorry, I couldn't create an outfit right now."
                )

            except KeyError:
                st.error(
                    "GROQ_API_KEY is missing. Add it in Streamlit Cloud "
                    "under Manage app → Settings → Secrets."
                )

            except Exception as error:
                st.session_state.stylist_answer = ""
                st.error(
                    "The AI Stylist could not get a response from Groq. "
                    "Check your API key, model availability, and app logs."
                )
                st.caption(f"Error type: {type(error).__name__}")

    if st.session_state.stylist_answer:
        st.divider()
        st.markdown("### YOUR PERSONAL STYLE NOTES")
        st.markdown(st.session_state.stylist_answer)

# ==================================================
# CART
# ==================================================

elif st.session_state.page == "Cart":

    st.title("YOUR CART")
    st.caption(f"{cart_count()} item(s) in your bag")
    st.divider()

    if not st.session_state.cart:
        st.info(t["empty_cart"])

        if st.button(t["shop"], type="primary"):
            go_to("Shop")
            st.rerun()

    else:
        for cart_key in list(st.session_state.cart.keys()):
            product_id, size = cart_key
            product = get_product(product_id)

            if product is None:
                continue

            quantity = st.session_state.cart[cart_key]
            item_col, details_col, remove_col = st.columns([1, 2, 1])

            with item_col:
                show_product_image(product)

            with details_col:
                st.markdown(f"**{product['name']}**")
                st.caption(f"Size: {size}")
                st.caption(f"Quantity: {quantity}")
                st.write(money(float(product["price"]) * quantity))

            with remove_col:
                if st.button(
                    t["remove"],
                    key=f"remove_{product_id}_{size}",
                ):
                    del st.session_state.cart[cart_key]
                    st.rerun()

            st.divider()

        st.markdown(f"## {t['total']}: {money(cart_total())}")
        st.caption(
            "Demo store: checkout and real payments are not connected yet."
        )

        if st.button(
            t["checkout"],
            type="primary",
            use_container_width=True,
        ):
            st.info("Online payments are not connected yet.")

        if st.button("CONTINUE SHOPPING"):
            go_to("Shop")
            st.rerun()

# ==================================================
# ACCOUNT
# ==================================================

elif st.session_state.page == "Account":

    st.title("YOUR STYLEMIND ACCOUNT")
    st.write("Create a demo profile to personalize your experience.")

    with st.form("account_form"):
        username = st.text_input(
            t["name"],
            value=st.session_state.username,
            placeholder="Your name",
        )

        submitted = st.form_submit_button(
            t["save"],
            use_container_width=True,
        )

        if submitted:
            st.session_state.username = username.strip()
            st.success(t["saved"])

    if st.session_state.username:
        st.divider()
        st.markdown(f"### {t['welcome']}, {st.session_state.username} 🖤")
        st.write(f"Items in your cart: {cart_count()}")
        st.write(f"Cart total: {money(cart_total())}")

    st.caption(
        "Demo profile only. Account information is not permanently saved."
    )

# ==================================================
# ADD SHOPS AND PRODUCTS
# ==================================================

elif st.session_state.page == "Add Items":

    st.markdown(
        '<div class="section-label">LOCAL FASHION / TETOUAN</div>',
        unsafe_allow_html=True,
    )
    st.title(t["add_items"])

    st.caption("Add a shop first, then list its clothes and accessories.")

    shops = load_shops()

    with st.expander(t["add_shop"], expanded=not bool(shops)):
        with st.form("shop_form", clear_on_submit=True):
            shop_name = st.text_input(t["shop_name"])
            city = st.text_input(t["city"], value="Tetouan")
            address = st.text_input(t["address"])
            phone = st.text_input(t["phone"])

            save_shop = st.form_submit_button(
                t["save_shop"],
                use_container_width=True,
            )

            if save_shop:
                if not shop_name.strip():
                    st.error("Please enter a shop name.")
                else:
                    db.add_shop(
                        name=shop_name.strip(),
                        city=city.strip() or "Tetouan",
                        address=address.strip(),
                        phone=phone.strip(),
                    )
                    st.success(t["shop_saved"])
                    st.rerun()

    st.divider()
    st.subheader(t["add_product"])

    shops = load_shops()

    if not shops:
        st.info(t["no_shops"])

    else:
        shop_options = {
            f"{shop['name']} — {shop.get('city', 'Tetouan')} (ID {shop['id']})":
            shop["id"]
            for shop in shops
        }

        with st.form("product_form", clear_on_submit=True):
            selected_shop = st.selectbox(
                t["choose_shop"],
                list(shop_options.keys()),
            )

            product_name = st.text_input(t["product_name"])

            category = st.selectbox(
                t["category"],
                [
                    "T-Shirts",
                    "Hoodies",
                    "Jackets",
                    "Pants",
                    "Shoes",
                    "Accessories",
                    "Dresses",
                    "Other",
                ],
            )

            description = st.text_area(t["description"])
            price = st.number_input(
                t["price"],
                min_value=0.0,
                value=100.0,
                step=10.0,
            )
            color = st.text_input(t["color"])
            sizes = st.text_input(t["sizes"])
            style = st.text_input(t["style"])
            image_url = st.text_input(t["image_url"])
            in_stock = st.checkbox(t["in_stock"], value=True)

            save_product = st.form_submit_button(
                t["save_product"],
                use_container_width=True,
            )

            if save_product:
                if not product_name.strip():
                    st.error("Please enter a product name.")
                elif price <= 0:
                    st.error("Price must be greater than zero.")
                else:
                    db.add_product(
                        shop_id=shop_options[selected_shop],
                        name=product_name.strip(),
                        category=category,
                        price=float(price),
                        description=description.strip(),
                        color=color.strip(),
                        sizes=sizes.strip(),
                        style=style.strip(),
                        image_url=image_url.strip(),
                        in_stock=in_stock,
                    )
                    st.success(t["product_saved"])
                    st.rerun()

    st.divider()
    st.subheader("REGISTERED SHOPS")

    shops = load_shops()

    if not shops:
        st.caption("No shops registered yet.")
    else:
        for shop in shops:
            st.markdown(
                f"**{shop['name']}** · {shop.get('city', 'Tetouan')}"
            )

            contact = " · ".join(
                part for part in [
                    shop.get("address", ""),
                    shop.get("phone", ""),
                ] if part
            )

            if contact:
                st.caption(contact)

# -------------------- FOOTER --------------------

st.divider()

st.markdown(
    '<div class="footer">STYLEMIND AI · DRESS LIKE YOURSELF</div>',
    unsafe_allow_html=True,
)
