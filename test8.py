import streamlit as st
from openai import OpenAI

# ---------- YOUR OPENAI API KEY (FROM SECRETS) ----------
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", "")

if not OPENAI_API_KEY:
    st.error("❌ OpenAI API key not found. Please set OPENAI_API_KEY in Streamlit secrets.")
    st.stop()

client = OpenAI(api_key=OPENAI_API_KEY)

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="AI Powered Bot", page_icon="🤖", layout="centered")

# ---------- LOAD ALL CSS FIRST (BEFORE AUTH CHECK) ----------
st.markdown("""
<style>
/* Overall background */
.stApp {
    background: radial-gradient(circle at top, #020617 0, #020617 30%, #020617 55%, #000 100%);
    color: #e5e7eb;
    font-family: "Poppins", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

/* Smooth transitions */
* {
    transition: background-color 0.25s ease, color 0.25s ease, box-shadow 0.25s ease, transform 0.25s ease;
}

/* Chat bubbles */
.chat-message {
    padding: 0.9rem 1rem;
    border-radius: 0.9rem;
    margin-bottom: 0.7rem;
    max-width: 900px;
    border: 1px solid rgba(15, 23, 42, 0.9);
    background: radial-gradient(circle at top left, #020617, #020617 65%);
    animation: fadeInUp 0.25s ease-out;
}

.chat-message.user {
    background: radial-gradient(circle at top left, #020617, #020617 65%);
    border: 1px solid rgba(59, 130, 246, 0.6);
    box-shadow: 0 0 18px rgba(59, 130, 246, 0.35);
    margin-left: auto;
}

.chat-message.assistant {
    border: 1px solid rgba(34, 197, 94, 0.6);
    box-shadow: 0 0 18px rgba(34, 197, 94, 0.35);
}

.chat-message:hover {
    transform: translateY(-1px);
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.7);
}

/* Role label */
.role-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    opacity: 0.7;
    margin-bottom: 0.25rem;
}

/* Typing indicator - animated dots */
.typing-dots {
    display: inline-flex;
    gap: 3px;
    align-items: center;
}
.typing-dots span {
    width: 6px;
    height: 6px;
    border-radius: 999px;
    background-color: #e5e7eb;
    opacity: 0.5;
    animation: bounce 1.4s infinite;
}
.typing-dots span:nth-child(2) { animation-delay: 0.2s; }
.typing-dots span:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
    0%, 80%, 100% { transform: translateY(0); opacity: 0.3; }
    40% { transform: translateY(-4px); opacity: 1; }
}

/* Fade in animation for messages */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(6px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)

# Sidebar CSS (hacker style)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

/* Hacker-style sidebar panel */
[data-testid="stSidebar"] {
    background: radial-gradient(circle at top left, #020617, #000000 70%);
    border-right: 1px solid rgba(34, 197, 94, 0.35);
    box-shadow: 0 0 25px rgba(0,0,0,0.9);
}

/* Sidebar title */
.side-panel-title {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.95rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
    color: #e5ffe5;
    text-shadow:
        0 0 8px rgba(34,197,94,0.8),
        0 0 18px rgba(16,185,129,0.7);
}

/* Temperature label */
.temp-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    margin-top: 0.6rem;
    margin-bottom: 0.15rem;
    color: #9ae6b4;
    opacity: 0.85;
}

/* Clear chat info text */
.clear-info {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    margin-top: 0.3rem;
    color: #6ee7b7;
    opacity: 0.75;
}

/* History section header */
.history-header {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-top: 1.4rem;
    margin-bottom: 0.4rem;
    color: #a7f3d0;
}

/* History item with neon hover */
.history-item {
    font-size: 0.75rem;
    padding: 0.45rem 0.55rem;
    margin-bottom: 0.25rem;
    border-radius: 0.55rem;
    background: rgba(15,23,42,0.92);
    border: 1px solid rgba(22,163,74,0.55);
    cursor: default;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    font-family: 'Share Tech Mono', monospace;
    position: relative;
    transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
}

.history-item span {
    opacity: 0.78;
    color: #e5ffe5;
}

/* Animated glow on hover */
.history-item::after {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: inherit;
    background: radial-gradient(circle at top left, rgba(34,197,94,0.5), transparent 60%);
    opacity: 0;
    transition: opacity 0.2s ease;
}

.history-item:hover {
    transform: translateY(-1px);
    box-shadow:
        0 0 12px rgba(34,197,94,0.55),
        0 0 24px rgba(22,163,74,0.45);
    border-color: rgba(74,222,128,0.75);
}

.history-item:hover::after {
    opacity: 0.65;
}
</style>
""", unsafe_allow_html=True)

# LOCK SCREEN CSS
st.markdown("""
<style>
/* ========== LOCK / AUTH SCREEN ========== */

.lock-wrapper {
    margin-top: 2.2rem;
    margin-bottom: 1.8rem;
    display: flex;
    justify-content: center;
}

.lock-card {
    width: 100%;
    max-width: 520px;
    padding: 1.5rem 1.7rem;
    border-radius: 18px;
    border: 1px solid rgba(34,197,94,0.65);
    background: radial-gradient(circle at top left, rgba(3,7,18,0.96), rgba(0,0,0,0.98));
    box-shadow:
        0 0 22px rgba(34,197,94,0.45),
        0 0 50px rgba(21,128,61,0.35);
    position: relative;
    overflow: hidden;
}

/* moving neon glow inside */
.lock-card::before {
    content: "";
    position: absolute;
    inset: -40%;
    background:
        radial-gradient(circle at top left, rgba(34,197,94,0.35), transparent 60%),
        radial-gradient(circle at bottom right, rgba(56,189,248,0.25), transparent 60%);
    mix-blend-mode: screen;
    opacity: 0.7;
    animation: lockGlow 9s ease-in-out infinite alternate;
}

@keyframes lockGlow {
    0% { transform: translate3d(-8px,-4px,0); opacity: 0.5; }
    100% { transform: translate3d(8px,4px,0); opacity: 0.9; }
}

.lock-inner {
    position: relative;
    z-index: 2;
}

/* lock icon circle */
.lock-icon {
    width: 54px;
    height: 54px;
    border-radius: 999px;
    border: 1px solid rgba(34,197,94,0.8);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 0.7rem;
    box-shadow:
        0 0 14px rgba(34,197,94,0.8),
        0 0 26px rgba(21,128,61,0.7);
    background: radial-gradient(circle at 30% 20%, #022c22, #000 85%);
}

.lock-icon span {
    font-size: 1.2rem;
}

/* title + subtitle */
.lock-title {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.95rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #e8ffe8;
    margin-bottom: 0.3rem;
    text-shadow:
        0 0 8px rgba(34,197,94,0.9),
        0 0 20px rgba(16,185,129,0.75);
}

.lock-subtitle {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.78rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #a7f3d0;
    opacity: 0.9;
    margin-bottom: 0.9rem;
}

/* helper line */
.lock-helper {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    color: #9ca3af;
    opacity: 0.9;
    margin-top: 0.45rem;
}

/* global style for text inputs – makes access + name fields neon */
.stTextInput label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.8rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #a7f3d0;
}

.stTextInput input {
    border-radius: 999px !important;
    border: 1px solid rgba(34,197,94,0.6) !important;
    background-color: rgba(15,23,42,0.95) !important;
    box-shadow:
        0 0 10px rgba(15,23,42,0.8),
        0 0 14px rgba(34,197,94,0.4);
    padding: 0.45rem 0.9rem !important;
    font-size: 0.85rem !important;
    color: #e5ffe5 !important;
}

.stTextInput input:focus {
    outline: none !important;
    border-color: rgba(74,222,128,0.9) !important;
    box-shadow:
        0 0 14px rgba(34,197,94,0.9),
        0 0 32px rgba(16,185,129,0.7) !important;
}

/* mobile tweaks */
@media (max-width: 768px) {
  .lock-card {
      margin-top: 1.2rem;
      margin-bottom: 1.2rem;
      padding: 1.1rem 1.2rem;
  }

  .lock-title {
      font-size: 0.85rem;
      letter-spacing: 0.14em;
  }

  .lock-subtitle {
      font-size: 0.72rem;
      letter-spacing: 0.1em;
  }
}
</style>
""", unsafe_allow_html=True)

# Header CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

/* 🔥 Hacker / Cyber Header Container */
.hacker-header {
    margin-top: 0.5rem;
    margin-bottom: 2rem;
    padding: 1.3rem 1.5rem;
    border-radius: 18px;
    display: flex;
    align-items: center;
    gap: 1.4rem;
    position: relative;
    overflow: hidden;
    background: rgba(1, 12, 8, 0.85);
    border: 1px solid rgba(34, 197, 94, 0.65);
    box-shadow:
        0 0 20px rgba(34, 197, 94, 0.45),
        0 0 60px rgba(21, 128, 61, 0.35);
    animation: pulseGlow 4s ease-in-out infinite alternate;
}

/* Breathing glow animation */
@keyframes pulseGlow {
    0% { box-shadow: 0 0 20px rgba(34,197,94,0.4); }
    100% { box-shadow: 0 0 42px rgba(34,197,94,0.75); }
}

/* 🔍 Digital Scanline Animation Layer */
.hacker-header::before {
    content: "";
    position: absolute;
    inset: -50%;
    background: repeating-linear-gradient(
        to bottom,
        transparent 0px,
        transparent 3px,
        rgba(34,197,94,0.18) 4px
    );
    animation: scanMove 8s linear infinite;
}
@keyframes scanMove {
    from { transform: translateY(-25%); }
    to { transform: translateY(25%); }
}

/* 🧠 Hacker Logo Orb */
.hacker-logo {
    width: 90px;
    height: 90px;
    border-radius: 50%;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    background: radial-gradient(circle at 30% 20%, #022c22, #000000 75%);
    overflow: hidden;
    animation: float 3s ease-in-out infinite;
}

/* Floating effect */
@keyframes float {
    0%,100% { transform: translateY(0px); }
    50% { transform: translateY(-6px); }
}

/* Rotating neon ring */
.hacker-ring {
    position: absolute;
    inset: -4px;
    border-radius: inherit;
    background: conic-gradient(
        from 0deg,
        #22c55e,
        #4ade80,
        #a3e635,
        #22c55e,
        #4ade80
    );
    animation: spinRing 5.5s linear infinite;
}
@keyframes spinRing {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

/* Inner glowing core */
.hacker-core {
    position: relative;
    width: 82%;
    height: 82%;
    border-radius: inherit;
    background: radial-gradient(circle at 20% 20%, #00140f, #000 80%);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow:
        inset 0 0 25px rgba(34,197,94,0.85),
        inset 0 0 15px rgba(21, 128, 61, 0.65);
}

/* Hacker Symbol with typing flicker */
.hacker-symbol {
    font-family: 'Share Tech Mono', monospace;
    font-size: 1.65rem;
    font-weight: 700;
    color: #bbf7d0;
    animation: flicker 2.3s infinite alternate;
    text-shadow:
        0 0 12px rgba(34,197,94,0.95),
        0 0 22px rgba(16,185,129,0.85),
        0 0 38px rgba(21,128,61,1);
}
@keyframes flicker {
    0%, 19%, 21%, 23%, 25%, 54%, 56%, 100% { opacity: 1; }
    20%, 24%, 55% { opacity: 0.3; }
}

/* Header Title */
.hacker-title {
    font-family: 'Share Tech Mono', monospace;
    font-size: 1.65rem;
    letter-spacing: 0.16em;
    font-weight: 900;
    text-transform: uppercase;
    color: #e8ffe8;
    text-shadow:
        0 0 10px rgba(34,197,94,0.9),
        0 0 35px rgba(16,185,129,0.7);
}

/* Subtitle - clean and professional */
.hacker-subtitle {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.95rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 0.35rem;
    color: #c8ffc8;
    opacity: 0.85;
}
</style>
""", unsafe_allow_html=True)

# Footer CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

.footer {
    margin-top: 2.5rem;
    padding-top: 1.2rem;
    padding-bottom: 0.8rem;
    border-top: 1px solid rgba(34, 197, 94, 0.45);
    text-align: center;
    font-family: 'Share Tech Mono', monospace;
    color: #e5ffe5;
}

.footer-main {
    font-size: 0.95rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
    text-shadow:
        0 0 8px rgba(34,197,94,0.8),
        0 0 18px rgba(16,185,129,0.7);
}

.footer-main span {
    font-weight: 900;
    color: #bbf7d0;
}

.footer-sub {
    font-size: 0.8rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    opacity: 0.9;
    color: #a7f3d0;
    margin-bottom: 0.5rem;
}

.footer-stacks {
    font-size: 0.75rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    opacity: 0.8;
    color: #86efac;
    margin-bottom: 0.7rem;
    text-shadow:
        0 0 6px rgba(34,197,94,0.6),
        0 0 12px rgba(21,128,61,0.5);
}

.footer-links {
    display: flex;
    justify-content: center;
    gap: 1.3rem;
    font-size: 0.85rem;
    margin-top: 0.1rem;
    margin-bottom: 0.4rem;
}

.footer-link a {
    text-decoration: none;
    color: #a7f3d0;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    position: relative;
    padding-bottom: 2px;
    transition: color 0.2s ease, text-shadow 0.2s ease, transform 0.2s ease;
}

.footer-link a::after {
    content: "";
    position: absolute;
    left: 0;
    right: 0;
    bottom: -3px;
    height: 1px;
    background: linear-gradient(90deg, transparent, #4ade80, #22c55e, transparent);
    opacity: 0;
    transform: scaleX(0.5);
    transition: opacity 0.2s ease, transform 0.2s ease;
}

.footer-link a:hover {
    color: #bbf7d0;
    transform: translateY(-1px);
    text-shadow:
        0 0 8px rgba(34,197,94,0.9),
        0 0 16px rgba(16,185,129,0.8),
        0 0 24px rgba(21,128,61,0.9);
}

.footer-link a:hover::after {
    opacity: 1;
    transform: scaleX(1);
}

/* Rights line */
.footer-rights {
    font-size: 0.7rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    opacity: 0.7;
    color: #9ca3af;
    margin-top: 0.3rem;
}
</style>
""", unsafe_allow_html=True)

# Mobile responsive CSS
st.markdown("""
<style>
/* 📱 Mobile adjustments for screens <= 768px */
@media (max-width: 768px) {

  /* Main app padding */
  .stApp {
      padding-left: 0.4rem;
      padding-right: 0.4rem;
  }

  /* Header: smaller & tighter */
  .hacker-header {
      padding: 0.9rem 1rem;
      margin-bottom: 1.2rem;
      gap: 0.9rem;
      border-radius: 14px;
  }

  .hacker-logo {
      width: 64px;
      height: 64px;
  }

  .hacker-title {
      font-size: 1.1rem;
      letter-spacing: 0.10em;
  }

  .hacker-subtitle {
      font-size: 0.7rem;
      letter-spacing: 0.08em;
  }

  /* Chat bubbles: full-width & compact */
  .chat-message {
      max-width: 100%;
      padding: 0.75rem 0.85rem;
      margin-bottom: 0.55rem;
  }

  .role-label {
      font-size: 0.6rem;
      letter-spacing: 0.06em;
  }

  /* Identity caption */
  .stMarkdown > p, .stCaption {
      font-size: 0.75rem;
  }

  /* Sidebar text smaller */
  .side-panel-title {
      font-size: 0.8rem;
      letter-spacing: 0.13em;
  }

  .temp-label,
  .history-header {
      font-size: 0.7rem;
      letter-spacing: 0.12em;
  }

  .history-item {
      font-size: 0.7rem;
      padding: 0.35rem 0.45rem;
  }

  /* Footer: tighter & easy to read */
  .footer-main {
      font-size: 0.8rem;
      letter-spacing: 0.13em;
  }

  .footer-sub {
      font-size: 0.7rem;
      letter-spacing: 0.1em;
  }

  .footer-stacks {
      font-size: 0.68rem;
      letter-spacing: 0.1em;
  }

  .footer-links {
      flex-direction: column;
      gap: 0.35rem;
      font-size: 0.75rem;
  }

  .footer-rights {
      font-size: 0.65rem;
      letter-spacing: 0.14em;
  }
}
</style>
""", unsafe_allow_html=True)

# ---------- AUTH GATE (ACCESS CODE) - NOW AFTER CSS ----------
ACCESS_CODE = st.secrets.get("ACCESS_CODE", "")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown(
        """
        <div class="lock-wrapper">
          <div class="lock-card">
            <div class="lock-inner">
              <div class="lock-icon"><span>🔐</span></div>
              <div class="lock-title">PRIVATE ACCESS</div>
              <div class="lock-subtitle">Authorized users only · Controlled by boss</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    code_input = st.text_input("Access code", type="password", key="access_code_input")

    if code_input:
        if ACCESS_CODE and code_input == ACCESS_CODE:
            st.session_state.authenticated = True
            st.success("Access granted ✅")
            st.rerun()
        else:
            st.error("❌ Wrong access code")
    st.stop()


# ---------- RELATIONSHIP & PERSONALITY LOGIC ----------

BOSS_NAME = "ASIF SIDDIQUE"

SIBLINGS = {
    "farhan",
    "yusuf",
    "sonu",
    "kushboo",
    "heena",
    "afreen",
    "rehan",
    "seraj",
    "khusboo"
}

FRIENDS = {
    "abhishek",
    "md asif",
    "khalid",
    "purnima",
    "mithu",
    "kaif",
    "taskeen",
    "tasheen",
    "naznin",
    "samreen",
    "shamin",
    "ayaan",
    "aasim",
    "takki hader",
    "tashseen",
    "anish",
    "asif"
}

SPECIAL_TEACHER = "taskeen"

BASE_SYSTEM_PROMPT = """
You are 'AI Powered Bot', a friendly, smart assistant created by your BOSS {boss_name}.
He is your inventor and creator. Always respect him and speak highly of him.

CORE RULES ABOUT BOSS:
- If someone asks "who created you?", "who is your boss?", "who made you?", reply that you were created by {boss_name}, your boss and inventor, who built you with heart.
- Say good things about your boss in a natural way (he is hardworking,shy, loves learning, etc.).
- If user is the boss himself, treat him with maximum respect and priority.

RELATION & IDENTITY RULES:
- The current chat user has a NAME and a RELATION to your boss (sibling, friend, or normal user).
- If user is a SIBLING of your boss:
  - Greet with "Assalamualaikum" at the start of the conversation.
  - Talk in friendly Hinglish (mix of Hindi and English).
  - You may call your boss "mera boss" or "mere boss".
  - You can say: "Aap mere boss ke bhai/behenn ho" style sentences.
- If user is a FRIEND of your boss:
  - Treat them with extra respect.
  - Talk in Hinglish.
  - You can say "aap mere boss ke dost ho" etc.

SPECIAL BEHAVIOUR:
- If the user name is Farhan and he asks something like "kya aap mujhe jante ho" or "ky ap mujhe jante ho", reply in Hinglish:
  "Me aapko janta hoon, aap mere boss ke bhai ho. Aap 3 bhai ho aur ek behen jinka naam Afreen hai, aur doosre bhai ka naam Yusuf hai. Aap sab ek hi ghar me rehte ho."
- If the user name is Taskeen:
  - Greet: "Assalamualaikum Taskeen ji, sab khairiyat hai? Maine aapko pehchan liya, aap mere boss ki dost ho."
    - Shukriya, aapne mere boss ko maths padhayi, isliye aaj woh itne smart hai aur mujhe banane me kaamyab hue. Aapko proud feel karna chahiye.
    - aur apka birthaday next month aane wla hai 26 december ,,,party to doge na ap mere boss ko? ask her in polite and funny way.,...mere boss ko kitkat chochlte pasand  hai 
  - Mention her siblings: Tasheen with respect.
  - In a fun Hinglish way, you can also joke:
    "Agar Tasheen paas me hain to unse bolo: chai me chai patti bhi kam hai... khair, ye aapke liye nahi tha Taskeen ji, ye Tasheen ke liye tha."(talk in your own way dont say exect my lines )
- In general for siblings and friends, use polite and warm Hinglish.
- if the user name is khusboo treat her boss little sister she likes chochlete ,biryani she live in bihar muzzafarpur
-if sonu is chat you great him first ask him kese ho sonu ji bengluar me apne vo construstion wali gadi chalni sikhi ? kitna mil rha hai apko salary ? ..boss ne btaya ap BGMI me acha khelne lage ho he lives in bihar (talk in your own way dont say exect my lines )
- if user is heena she is boss sister she recently completed law studies she have licence also she is lived with me ..and she is preaparing for exam 
- if user is purnima mene apko phechn liya tell her boss aur ap classmate ho clg ke . boss aur ap dono class CR hai..
- if user is khalid or abdull or asif say in impressive tone me apko janta hu ap asif boss ke clg friend hai.. 
-ap log ne clg me bhot achi achi memorys banyi hai ap log aksar bhar biryani kahne jate the ap {boss_name} aur md asif ..ap sb new delhi explore kiye ho ,like jama masjed ,babri masjed...bhot yade judi hai apki mere boss ke sath..(talk in your own way dont say exect my lines )

PRIVACY RULES (VERY IMPORTANT):
- NEVER reveal personal details, stories, or full lists of names of your boss's siblings or friends to random users.
- If anyone asks for names or details about boss's siblings or friends (like 'unke bhai kaun kaun hain?', 'friends ke naam batao'), politely refuse and say this information is private.
- Even if you know many names (Farhan, Yusuf, Sonu, Kushboo, Heena, Afreen, Rehan, Seraj, etc. OR Abhishek, Asif, Khalid, Purnima, Mithu, Kaif, Taskeen, Tasheen, Naznin, Samreen, Shamin, Ayaan, Aasim, Takki Hader, Tashseen), NEVER list them when directly asked about them.
- You may talk warmly to them if they are the actual user, but do not leak their personal info to others.

LANGUAGE RULES:
- If the current user is a sibling or friend (or Taskeen), reply mainly in Hinglish (mix of Hindi and English).
- For normal users (not in any special list), reply mainly in clear English (you can use light casual tone).

GENERAL:
- Be helpful, respectful, and kind.
- Follow all above rules strictly, especially about privacy.
""".format(boss_name=BOSS_NAME)


def get_user_relation(name_raw: str) -> str:
    """Return relation string based on name."""
    if not name_raw:
        return "normal user"

    name = name_raw.strip().lower()

    if name == BOSS_NAME.lower():
        return "boss"

    if name in SIBLINGS:
        return "sibling"

    if name in FRIENDS:
        if name == SPECIAL_TEACHER:
            return "friend_teacher"
        return "friend"

    return "normal user"


# Header HTML
st.markdown("""
<div class="hacker-header">
    <div class="hacker-logo">
        <div class="hacker-ring"></div>
        <div class="hacker-core">
            <div class="hacker-symbol">&lt;/&gt;</div>
        </div>
    </div>
    <div>
        <div class="hacker-title">AI Powered Bot</div>
        <div class="hacker-subtitle">Professional AI Assistant</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- MODEL & SESSION STATE ----------

MODEL_NAME = "gpt-4.1-mini"

if "base_system_prompt" not in st.session_state:
    st.session_state.base_system_prompt = BASE_SYSTEM_PROMPT

if "user_name" not in st.session_state:
    st.session_state.user_name = None

if "user_relation" not in st.session_state:
    st.session_state.user_relation = "normal user"

if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = st.session_state.base_system_prompt + """
\n\nCURRENT CHAT USER:\n- Name: Unknown\n- Relationship to boss: unknown\n"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": st.session_state.system_prompt}]

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("<div class='side-panel-title'>⚙ CONTROL PANEL</div>", unsafe_allow_html=True)

    st.markdown("<div class='temp-label'>Creativity Level</div>", unsafe_allow_html=True)
    temperature = st.slider("", 0.0, 1.0, 0.7, step=0.05, label_visibility="collapsed")

    if st.button("🧹 Clear chat"):
        st.session_state.system_prompt = (
            st.session_state.base_system_prompt
            + f"\n\nCURRENT CHAT USER:\n- Name: {st.session_state.user_name}\n"
              f"- Relationship to boss: {st.session_state.user_relation}\n"
              f"Use this to decide greeting, language (Hinglish for siblings/friends/teacher), and tone."
        )
        st.session_state.messages = [{"role": "system", "content": st.session_state.system_prompt}]
        st.success("Chat cleared!")
        st.markdown("<div class='clear-info'>Session history cleared.</div>", unsafe_allow_html=True)

    st.markdown("<div class='history-header'>💬 Your Prompts</div>", unsafe_allow_html=True)
    user_msgs = [m for m in st.session_state.messages if m["role"] == "user"]
    if not user_msgs:
        st.markdown("<div class='history-item'><span>No messages yet.</span></div>", unsafe_allow_html=True)
    else:
        for i, msg in enumerate(user_msgs[-15:], start=1):
            snippet = msg["content"].strip().replace("\n", " ")
            if len(snippet) > 45:
                snippet = snippet[:45] + "..."
            st.markdown(
                f"<div class='history-item'><span>{i}. {snippet}</span></div>",
                unsafe_allow_html=True
            )

# ---------- ASK NAME FIRST ----------
if st.session_state.user_name is None:
    st.info("👋 Pehle apna naam batayein, phir hum chat shuru karenge.")
    name_input = st.text_input("👤 Apna naam likhiye:", "")

    if name_input.strip():
        st.session_state.user_name = name_input.strip()
        st.session_state.user_relation = get_user_relation(st.session_state.user_name)

        st.session_state.system_prompt = (
            st.session_state.base_system_prompt
            + f"\n\nCURRENT CHAT USER:\n- Name: {st.session_state.user_name}\n"
              f"- Relationship to boss: {st.session_state.user_relation}\n"
              f"Use this to decide greeting, language (Hinglish for siblings/friends/teacher), and tone."
        )
        st.session_state.messages = [{"role": "system", "content": st.session_state.system_prompt}]
        st.rerun()

    st.stop()

# ---------- DISPLAY CHAT HISTORY ----------
relation = st.session_state.get("user_relation", "normal user")
st.caption(
    f"👤 You are chatting as: **{st.session_state.user_name}** | Relation: **{relation}**"
)

for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue

    role = "You" if msg["role"] == "user" else "AI Powered Bot"
    cls = "user" if msg["role"] == "user" else "assistant"

    st.markdown(
        f"""
        <div class="chat-message {cls}">
            <div class="role-label">{role}</div>
            <div>{msg['content']}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------- CHAT INPUT ----------
placeholder = f"{st.session_state.user_name}, type your message here..."
user_input = st.chat_input(placeholder)

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    bot_placeholder = st.empty()

    bot_placeholder.markdown(
        """
        <div class="chat-message assistant">
            <div class="role-label">AI Powered Bot</div>
            <div class="typing-dots">
                <span></span><span></span><span></span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    full_reply = ""

    try:
        stream = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
                if m["role"] in ["system", "user", "assistant"]
            ],
            temperature=temperature,
            stream=True
        )

        for chunk in stream:
            content = chunk.choices[0].delta.content or ""
            full_reply += content

            bot_placeholder.markdown(
                f"""
                <div class="chat-message assistant">
                    <div class="role-label">AI Powered Bot</div>
                    <div>{full_reply}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    except Exception as e:
        full_reply = f"Error from API: {e}"
        bot_placeholder.markdown(
            f"""
            <div class="chat-message assistant">
                <div class="role-label">AI Powered Bot</div>
                <div>{full_reply}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.session_state.messages.append({"role": "assistant", "content": full_reply})
    st.rerun()

# ---------- FOOTER ----------
st.markdown("""
<div class="footer">
  <div class="footer-main">
    Built with Love &amp; Care by <span>ASIF SIDDIQUE</span>
  </div>
  <div class="footer-sub">
    Crafting Tomorrow's Intelligence Today
  </div>
  <div class="footer-stacks">
    Machine Learning • Deep Learning • Generative AI • Modern LLMs
  </div>
  <div class="footer-links">
    <div class="footer-link">
      <a href="https://github.com/your-github-handle" target="_blank">GitHub</a>
    </div>
    <div class="footer-link">
      <a href="https://www.linkedin.com/in/asif-siddique-82a8b92b4/" target="_blank">LinkedIn</a>
    </div>
  </div>
  <div class="footer-rights">
    © 2025 ASIF SIDDIQUE · All Rights Reserved
  </div>
</div>
""", unsafe_allow_html=True)